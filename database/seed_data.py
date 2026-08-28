"""
Seed Data Script for StatutoryGuard
Populates initial demo startup profiles and pre-calculated statutory compliance matrices.
"""

from database.db_client import DatabaseClient
from utils.compliance_calculator import calculate_statutory_tasks
import uuid
from datetime import datetime

DEMO_COMPANIES = [
    {
        "cin": "U72900KA2023PTC174821",
        "name": "InnovateTech Solutions Private Limited",
        "entity_type": "Private Limited",
        "incorporation_date": "2023-05-10",
        "authorized_capital": 1500000.0,
        "paid_up_capital": 500000.0,
        "roc_office": "ROC Bangalore",
        "email": "founders@innovatetech.in",
        "phone": "+919876543210",
        "address": "4th Floor, HSR Layout, Sector 6, Bengaluru, Karnataka 560102",
        "mca_status": "ACTIVE",
        "directors": [
            {"din": "08123456", "name": "Rajesh Kumar", "designation": "Managing Director", "dsc_expiry": "2026-11-20"},
            {"din": "09876543", "name": "Ananya Sharma", "designation": "Director", "dsc_expiry": "2026-09-05"}
        ]
    },
    {
        "cin": "U74999DL2022OPC398102",
        "name": "QuickVeda Healthcare OPC Private Limited",
        "entity_type": "One Person Company",
        "incorporation_date": "2022-08-14",
        "authorized_capital": 1000000.0,
        "paid_up_capital": 100000.0,
        "roc_office": "ROC Delhi",
        "email": "contact@quickveda.in",
        "phone": "+919123456789",
        "address": "Connaught Place, New Delhi, Delhi 110001",
        "mca_status": "ACTIVE",
        "directors": [
            {"din": "07654321", "name": "Vikram Sethi", "designation": "Sole Director", "dsc_expiry": "2026-08-31"}
        ]
    },
    {
        "cin": "AAX-9988",
        "name": "GreenLeaf BioTech LLP",
        "entity_type": "LLP",
        "incorporation_date": "2021-11-03",
        "authorized_capital": 500000.0,
        "paid_up_capital": 500000.0,
        "roc_office": "ROC Mumbai",
        "email": "info@greenleaf.co.in",
        "phone": "+919988776655",
        "address": "Bandra Kurla Complex, Mumbai, Maharashtra 400051",
        "mca_status": "ACTIVE",
        "directors": [
            {"din": "06543210", "name": "Siddharth Rao", "designation": "Designated Partner", "dsc_expiry": "2026-12-15"},
            {"din": "05432109", "name": "Kavita Reddy", "designation": "Designated Partner", "dsc_expiry": "2026-10-10"}
        ]
    }
]

def seed_database():
    db = DatabaseClient()
    for company in DEMO_COMPANIES:
        db.save_company(company)
        tasks = calculate_statutory_tasks(company)
        db.save_tasks(tasks)

        # Seed sample document vault item
        doc_id = str(uuid.uuid4())[:8]
        db.add_vault_doc({
            "doc_id": doc_id,
            "company_cin": company["cin"],
            "doc_name": "Certificate_of_Incorporation.pdf",
            "category": "Incorporation",
            "upload_date": "2023-05-12",
            "file_path": f"/vault/{company['cin']}/Certificate_of_Incorporation.pdf",
            "dsc_director": company["directors"][0]["name"],
            "dsc_expiry": company["directors"][0]["dsc_expiry"],
            "encrypted": True
        })

    print("Database seeded successfully with demo companies & MCA statutory matrices!")

if __name__ == "__main__":
    seed_database()
