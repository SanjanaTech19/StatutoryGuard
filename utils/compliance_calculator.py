"""
Compliance Calculator Utility
Calculates dynamic MCA/ROC filing deadlines, penalty exposures, and health scores for Indian startups.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Tuple
from config import STATUTORY_FORMS_CATALOG

# Current system anchor date
CURRENT_DATE = date(2026, 8, 28)

def calculate_statutory_tasks(company: Dict[str, Any], anchor_date: date = CURRENT_DATE) -> List[Dict[str, Any]]:
    """
    Generate list of statutory compliance tasks customized for company entity type and incorporation date.
    """
    cin = company["cin"]
    entity_type = company.get("entity_type", "Private Limited")
    inc_date_str = company.get("incorporation_date", "2023-04-15")
    
    try:
        inc_date = datetime.strptime(inc_date_str, "%Y-%m-%d").date()
    except Exception:
        inc_date = date(2023, 4, 15)

    current_fy_year = anchor_date.year if anchor_date.month > 3 else anchor_date.year - 1
    tasks = []

    for form_code, metadata in STATUTORY_FORMS_CATALOG.items():
        # Check if form applies to this entity type
        if entity_type not in metadata["applicable_entities"]:
            continue

        due_date = None

        # 1. Incorporation triggered (e.g. INC-20A within 180 days)
        if metadata["trigger"] == "incorporation":
            due_date = inc_date + timedelta(days=metadata["days_due_after_trigger"])
            # Only include if within relevant window or overdue
            if (anchor_date - inc_date).days > 365 and due_date < anchor_date:
                continue # Already past first year for old company

        # 2. Annual Fixed date (e.g. DIR-3 KYC Sept 30, DPT-3 June 30, LLP Form 11 May 30)
        elif metadata["trigger"] == "annual_fixed":
            fixed_str = metadata["fixed_due_date"]
            month, day = map(int, fixed_str.split("-"))
            due_date = date(current_fy_year, month, day)
            # If date has passed by more than 90 days, project next year's due date
            if due_date < anchor_date - timedelta(days=90):
                due_date = date(current_fy_year + 1, month, day)

        # 3. AGM Relative (e.g. AOC-4 Oct 30, MGT-7 Nov 29, ADT-1 Oct 14)
        elif metadata["trigger"] == "agm_relative":
            fixed_str = metadata["fixed_due_date"]
            month, day = map(int, fixed_str.split("-"))
            due_date = date(current_fy_year, month, day)
            if due_date < anchor_date - timedelta(days=90):
                due_date = date(current_fy_year + 1, month, day)

        # 4. Quarterly Board Meetings
        elif metadata["trigger"] == "quarterly":
            fixed_str = metadata["fixed_due_date"]
            month, day = map(int, fixed_str.split("-"))
            due_date = date(current_fy_year if month >= 4 else current_fy_year + 1, month, day)

        # 5. Bi-annual (MSME-1)
        elif metadata["trigger"] == "bi_annual":
            fixed_dates = metadata["fixed_due_date"]
            for f_str in fixed_dates:
                month, day = map(int, f_str.split("-"))
                d_date = date(current_fy_year if month >= 4 else current_fy_year + 1, month, day)
                if d_date >= anchor_date - timedelta(days=30):
                    due_date = d_date
                    break
            if not due_date:
                due_date = date(current_fy_year, 10, 31)

        if not due_date:
            due_date = anchor_date + timedelta(days=30)

        # Calculate days remaining & penalty exposure
        days_left = (due_date - anchor_date).days
        status = "Pending"
        
        # Simulated filing status for demonstration
        if days_left > 60:
            status = "Filed" if (hash(form_code + cin) % 3 == 0) else "Pending"
        elif days_left < -30:
            status = "Pending"

        task_id = f"{cin}_{form_code.replace(' ', '_').replace('/', '_')}_{due_date.year}"

        tasks.append({
            "task_id": task_id,
            "company_cin": cin,
            "form_code": form_code,
            "title": metadata["title"],
            "due_date": due_date.strftime("%Y-%m-%d"),
            "days_left": days_left,
            "status": status,
            "risk_level": metadata["risk_level"],
            "max_penalty": metadata["max_penalty_inr"],
            "daily_penalty": metadata["daily_penalty_inr"],
            "category": metadata["form_category"],
            "key_documents": metadata["key_documents"],
            "description": metadata["description"],
            "mca_portal_link": metadata.get("mca_portal_link", "")
        })

    # Sort tasks by due date ascending
    tasks.sort(key=lambda x: x["due_date"])
    return tasks


def compute_compliance_metrics(tasks: List[Dict[str, Any]], anchor_date: date = CURRENT_DATE) -> Tuple[float, float, int, int, int]:
    """
    Computes overall compliance metrics:
    Returns (health_score_pct, total_penalty_exposure_inr, total_pending, total_filed, overdue_count)
    """
    if not tasks:
        return (100.0, 0.0, 0, 0, 0)

    total_tasks = len(tasks)
    filed_count = sum(1 for t in tasks if t["status"] == "Filed")
    pending_tasks = [t for t in tasks if t["status"] != "Filed"]
    total_pending = len(pending_tasks)

    overdue_count = 0
    total_penalty = 0.0

    for t in pending_tasks:
        due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
        days_diff = (anchor_date - due).days
        if days_diff > 0:
            overdue_count += 1
            # Base penalty + daily late fee
            daily_rate = t.get("daily_penalty", 100)
            max_pen = t.get("max_penalty", 50000.0)
            calc_pen = min(max_pen, 5000.0 + (days_diff * daily_rate))
            total_penalty += calc_pen
        else:
            # Potential exposure if missed
            total_penalty += t.get("max_penalty", 50000.0) * 0.15

    # Health score formula
    health_score = round((filed_count / total_tasks) * 100.0, 1)
    if overdue_count > 0:
        health_score = max(0.0, health_score - (overdue_count * 15.0))

    return (health_score, round(total_penalty, 2), total_pending, filed_count, overdue_count)
