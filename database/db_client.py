"""
Dual Database Client for StatutoryGuard
Handles local SQLite database with optional Supabase PostgreSQL sync.
Includes User Authentication & Strict Admin Security layer.
"""

import sqlite3
import json
import os
import uuid
import urllib.request
from typing import List, Dict, Any, Optional
from config import DB_FILE, SUPABASE_URL, SUPABASE_KEY
from utils.auth_utils import hash_password, verify_password

class DatabaseClient:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        except Exception:
            self.db_path = "/tmp/statutoryguard.db"
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_sqlite()


    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_sqlite(self):
        """Initialize SQLite database tables if they do not exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Users Table (Founders & Admins)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'founder',
            company_cin TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Companies table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            cin TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            incorporation_date TEXT NOT NULL,
            authorized_capital REAL,
            paid_up_capital REAL,
            roc_office TEXT,
            directors TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            mca_status TEXT DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Compliance Tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance_tasks (
            task_id TEXT PRIMARY KEY,
            company_cin TEXT NOT NULL,
            form_code TEXT NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            risk_level TEXT DEFAULT 'HIGH',
            max_penalty REAL DEFAULT 50000.0,
            category TEXT DEFAULT 'Annual Filing',
            filed_date TEXT,
            srn_number TEXT,
            notes TEXT,
            FOREIGN KEY (company_cin) REFERENCES companies(cin)
        );
        """)

        # Document Vault table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_vault (
            doc_id TEXT PRIMARY KEY,
            company_cin TEXT NOT NULL,
            doc_name TEXT NOT NULL,
            category TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            file_path TEXT NOT NULL,
            dsc_director TEXT,
            dsc_expiry TEXT,
            encrypted INTEGER DEFAULT 1,
            file_hash TEXT,
            FOREIGN KEY (company_cin) REFERENCES companies(cin)
        );
        """)


        # Alerts log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alert_logs (
            alert_id TEXT PRIMARY KEY,
            company_cin TEXT NOT NULL,
            form_code TEXT NOT NULL,
            channel TEXT NOT NULL,
            recipient TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            status TEXT DEFAULT 'SENT',
            message TEXT NOT NULL
        );
        """)

        conn.commit()

        # Seed Default Strict Administrator Account if not present
        cursor.execute("SELECT * FROM users WHERE role = 'admin'")
        if not cursor.fetchone():
            admin_pw_hash = hash_password("AdminStrictSecret123!")
            cursor.execute("""
            INSERT INTO users (user_id, username, email, password_hash, role, company_cin, full_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                "admin-001",
                "admin",
                "admin@statutoryguard.in",
                admin_pw_hash,
                "admin",
                "SYSTEM",
                "Chief Compliance Admin"
            ))
            conn.commit()

        conn.close()

    # User Authentication & Management Operations
    def create_user(self, username: str, email: str, password: str, role: str = "founder", company_cin: Optional[str] = None, full_name: Optional[str] = None) -> tuple[bool, str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT user_id FROM users WHERE username = ? OR email = ?", (username.strip().lower(), email.strip().lower()))
        if cursor.fetchone():
            conn.close()
            return False, "Username or Email already registered!"

        user_id = str(uuid.uuid4())[:8]
        pw_hash = hash_password(password)

        try:
            cursor.execute("""
            INSERT INTO users (user_id, username, email, password_hash, role, company_cin, full_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                username.strip().lower(),
                email.strip().lower(),
                pw_hash,
                role,
                company_cin or "",
                full_name or username
            ))
            conn.commit()
            conn.close()
            return True, "User account created successfully!"
        except Exception as e:
            conn.close()
            return False, f"Failed to create user: {str(e)}"

    def authenticate_user(self, username_or_email: str, password: str) -> tuple[Optional[Dict[str, Any]], str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        user_input = username_or_email.strip().lower()
        
        cursor.execute("""
        SELECT * FROM users WHERE username = ? OR email = ?
        """, (user_input, user_input))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None, "Invalid Username/Email or Password."

        user_data = dict(row)
        if verify_password(password, user_data["password_hash"]):
            return user_data, "Authentication Successful!"
        else:
            return None, "Invalid Username/Email or Password."

    def list_users(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, email, role, company_cin, full_name, created_at FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # Company operations
    def save_company(self, company_dict: Dict[str, Any]) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        directors_json = company_dict.get("directors")
        if isinstance(directors_json, list):
            directors_json = json.dumps(directors_json)

        cursor.execute("""
        INSERT INTO companies (cin, name, entity_type, incorporation_date, authorized_capital, paid_up_capital, roc_office, directors, email, phone, address, mca_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(cin) DO UPDATE SET
            name=excluded.name,
            entity_type=excluded.entity_type,
            incorporation_date=excluded.incorporation_date,
            authorized_capital=excluded.authorized_capital,
            paid_up_capital=excluded.paid_up_capital,
            roc_office=excluded.roc_office,
            directors=excluded.directors,
            email=excluded.email,
            phone=excluded.phone,
            address=excluded.address,
            mca_status=excluded.mca_status;
        """, (
            company_dict["cin"],
            company_dict["name"],
            company_dict["entity_type"],
            company_dict["incorporation_date"],
            company_dict.get("authorized_capital", 1000000.0),
            company_dict.get("paid_up_capital", 100000.0),
            company_dict.get("roc_office", "ROC Delhi"),
            directors_json,
            company_dict.get("email", "founder@startup.in"),
            company_dict.get("phone", "+919876543210"),
            company_dict.get("address", "Bengaluru, Karnataka"),
            company_dict.get("mca_status", "ACTIVE")
        ))
        conn.commit()
        conn.close()
        return True

    def get_company(self, cin: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies WHERE cin = ?", (cin.upper(),))
        row = cursor.fetchone()
        conn.close()

        if row:
            data = dict(row)
            if data.get("directors"):
                try:
                    data["directors"] = json.loads(data["directors"])
                except Exception:
                    data["directors"] = []
            return data
        return None

    def list_companies(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        result = []
        for r in rows:
            d = dict(r)
            if d.get("directors"):
                try:
                    d["directors"] = json.loads(d["directors"])
                except Exception:
                    d["directors"] = []
            result.append(d)
        return result

    # Compliance Tasks & Custom Form Operations
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        for t in tasks:
            cursor.execute("""
            INSERT INTO compliance_tasks (task_id, company_cin, form_code, title, due_date, status, risk_level, max_penalty, category, filed_date, srn_number, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                status=excluded.status,
                filed_date=excluded.filed_date,
                srn_number=excluded.srn_number,
                notes=excluded.notes;
            """, (
                t["task_id"],
                t["company_cin"],
                t["form_code"],
                t["title"],
                t["due_date"],
                t.get("status", "Pending"),
                t.get("risk_level", "HIGH"),
                t.get("max_penalty", 50000.0),
                t.get("category", "Annual Filing"),
                t.get("filed_date"),
                t.get("srn_number"),
                t.get("notes", "")
            ))
        conn.commit()
        conn.close()
        return True

    def create_custom_task(self, task_dict: Dict[str, Any]) -> bool:
        """Allows founder or administrator to add custom statutory compliance forms."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO compliance_tasks (task_id, company_cin, form_code, title, due_date, status, risk_level, max_penalty, category, filed_date, srn_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_dict["task_id"],
            task_dict["company_cin"],
            task_dict["form_code"],
            task_dict["title"],
            task_dict["due_date"],
            task_dict.get("status", "Pending"),
            task_dict.get("risk_level", "HIGH"),
            task_dict.get("max_penalty", 50000.0),
            task_dict.get("category", "Custom Compliance"),
            None,
            None,
            task_dict.get("notes", "Custom form added by founder/admin")
        ))
        conn.commit()
        conn.close()
        return True

    def get_tasks_for_company(self, cin: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM compliance_tasks WHERE company_cin = ? ORDER BY due_date ASC", (cin.upper(),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_task_status(self, task_id: str, status: str, srn: Optional[str] = None, filed_date: Optional[str] = None) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE compliance_tasks
        SET status = ?, srn_number = ?, filed_date = ?
        WHERE task_id = ?
        """, (status, srn, filed_date, task_id))
        conn.commit()
        conn.close()
        return True

    # Vault Operations
    def add_vault_doc(self, doc_dict: Dict[str, Any]) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO document_vault (doc_id, company_cin, doc_name, category, upload_date, file_path, dsc_director, dsc_expiry, encrypted, file_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(doc_id) DO UPDATE SET
            doc_name=excluded.doc_name,
            category=excluded.category,
            dsc_expiry=excluded.dsc_expiry,
            file_hash=excluded.file_hash;
        """, (
            doc_dict["doc_id"],
            doc_dict["company_cin"],
            doc_dict["doc_name"],
            doc_dict["category"],
            doc_dict["upload_date"],
            doc_dict["file_path"],
            doc_dict.get("dsc_director", ""),
            doc_dict.get("dsc_expiry", ""),
            1 if doc_dict.get("encrypted", True) else 0,
            doc_dict.get("file_hash", "")
        ))
        conn.commit()
        conn.close()
        return True


    def get_vault_docs(self, cin: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM document_vault WHERE company_cin = ? ORDER BY upload_date DESC", (cin.upper(),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_vault_doc(self, doc_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM document_vault WHERE doc_id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


    # Alert Logs
    def log_alert(self, alert_dict: Dict[str, Any]) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO alert_logs (alert_id, company_cin, form_code, channel, recipient, sent_at, status, message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert_dict["alert_id"],
            alert_dict["company_cin"],
            alert_dict["form_code"],
            alert_dict["channel"],
            alert_dict["recipient"],
            alert_dict["sent_at"],
            alert_dict.get("status", "SENT"),
            alert_dict["message"]
        ))
        conn.commit()
        conn.close()
        return True

    def get_alert_logs(self, cin: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        if cin == "ALL":
            cursor.execute("SELECT * FROM alert_logs ORDER BY sent_at DESC")
        else:
            cursor.execute("SELECT * FROM alert_logs WHERE company_cin = ? ORDER BY sent_at DESC", (cin.upper(),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # Database Export & Backup Operations
    def export_db_snapshot(self) -> Dict[str, Any]:
        """Returns complete JSON database snapshot for backup or external database REST sync."""
        conn = self._get_connection()
        cursor = conn.cursor()

        tables = ["users", "companies", "compliance_tasks", "document_vault", "alert_logs"]
        snapshot = {}

        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            snapshot[table] = [dict(r) for r in rows]

        conn.close()
        return snapshot

    def sync_to_supabase(self) -> tuple[bool, str]:
        """
        Syncs local database records to cloud Supabase PostgreSQL via REST API if configured.
        """
        if not SUPABASE_URL or not SUPABASE_KEY:
            return False, "Supabase credentials not configured in environment variables."

        try:
            snapshot = self.export_db_snapshot()
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }

            for table_name, rows in snapshot.items():
                if not rows:
                    continue
                url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table_name}"
                data_bytes = json.dumps(rows).encode("utf-8")
                req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
                with urllib.request.urlopen(req) as resp:
                    pass

            return True, "Database successfully synced to cloud Supabase PostgreSQL!"
        except Exception as e:
            return False, f"Supabase Sync Error: {str(e)}"
