"""
Database Models and Data Structures for StatutoryGuard Platform
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import json

class CompanyModel:
    def __init__(
        self,
        cin: str,
        name: str,
        entity_type: str = "Private Limited",
        incorporation_date: str = "2023-04-15",
        authorized_capital: float = 1000000.0,
        paid_up_capital: float = 100000.0,
        roc_office: str = "ROC Delhi",
        directors: Optional[List[Dict[str, str]]] = None,
        email: str = "founder@startup.in",
        phone: str = "+919876543210",
        address: str = "Tech Park, Bengaluru, Karnataka 560001",
        mca_status: str = "ACTIVE"
    ):
        self.cin = cin.upper().strip()
        self.name = name.strip()
        self.entity_type = entity_type
        self.incorporation_date = incorporation_date
        self.authorized_capital = authorized_capital
        self.paid_up_capital = paid_up_capital
        self.roc_office = roc_office
        self.directors = directors or [
            {"din": "08123456", "name": "Rajesh Sharma", "designation": "Director", "dsc_expiry": "2026-11-30"},
            {"din": "09876543", "name": "Priya Nair", "designation": "Director", "dsc_expiry": "2026-09-15"}
        ]
        self.email = email
        self.phone = phone
        self.address = address
        self.mca_status = mca_status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cin": self.cin,
            "name": self.name,
            "entity_type": self.entity_type,
            "incorporation_date": self.incorporation_date,
            "authorized_capital": self.authorized_capital,
            "paid_up_capital": self.paid_up_capital,
            "roc_office": self.roc_office,
            "directors": json.dumps(self.directors),
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "mca_status": self.mca_status
        }


class ComplianceTaskModel:
    def __init__(
        self,
        task_id: str,
        company_cin: str,
        form_code: str,
        title: str,
        due_date: str,
        status: str = "Pending",  # Pending, Review, Filed
        risk_level: str = "HIGH", # CRITICAL, HIGH, MEDIUM
        max_penalty: float = 50000.0,
        category: str = "Annual Filing",
        filed_date: Optional[str] = None,
        srn_number: Optional[str] = None,
        notes: str = ""
    ):
        self.task_id = task_id
        self.company_cin = company_cin
        self.form_code = form_code
        self.title = title
        self.due_date = due_date
        self.status = status
        self.risk_level = risk_level
        self.max_penalty = max_penalty
        self.category = category
        self.filed_date = filed_date
        self.srn_number = srn_number
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "company_cin": self.company_cin,
            "form_code": self.form_code,
            "title": self.title,
            "due_date": self.due_date,
            "status": self.status,
            "risk_level": self.risk_level,
            "max_penalty": self.max_penalty,
            "category": self.category,
            "filed_date": self.filed_date,
            "srn_number": self.srn_number,
            "notes": self.notes
        }
