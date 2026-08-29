"""
Plain-English AI Legal Assistant Module
Translates dense MCA circulars into step-by-step task lists and answers Companies Act 2013 statutory compliance questions.
"""

import re
from typing import Dict, Any
from config import SAMPLE_MCA_CIRCULARS

def translate_circular_to_plain_english(raw_text: str) -> dict:
    """
    Translates legalistic MCA circular into structured, plain-English summary & actionable task list.
    """
    raw_lower = raw_text.lower()
    
    tasks = []
    summary = ""
    deadline = "Not Specified"
    penalty = "Standard Companies Act 2013 penalties"

    if "dir-3 kyc" in raw_lower:
        summary = "The MCA has extended the DIR-3 KYC annual deadline to October 15, 2024. All directors holding a DIN must complete KYC to avoid DIN deactivation and a ₹5,000 late fee."
        deadline = "15th October 2024"
        penalty = "₹5,000 per director + DIN Deactivation"
        tasks = [
            {"task": "Verify active DIN list for all company directors", "status": "Filed", "action": "Cross-check DIN status on MCA portal"},
            {"task": "Collect mobile OTP and email OTP from directors", "status": "Review", "action": "Send OTP request to directors"},
            {"task": "Submit DIR-3 KYC WEB form before Oct 15", "status": "Pending", "action": "Upload DSC and submit on MCA V3 portal"}
        ]
    elif "audit trail" in raw_lower or "edit log" in raw_lower:
        summary = "MCA mandates that all company accounting software must have an unalterable Edit Log (Audit Trail) enabled throughout the year. Auditors must explicitly report compliance in AOC-4."
        deadline = "Immediate (Mandatory for FY 2023-24 & 2024-25)"
        penalty = "₹50,000 to ₹500,000 per officer in default"
        tasks = [
            {"task": "Verify accounting software (Tally/Zoho/Quickbooks) has Audit Trail enabled", "status": "Review", "action": "Ensure edit log cannot be toggled off"},
            {"task": "Obtain Audit Trail Certificate from Chartered Accountant", "status": "Pending", "action": "Request auditor confirmation note for AOC-4"}
        ]
    elif "inc-20a" in raw_lower or "commencement of business" in raw_lower:
        summary = "Every newly incorporated company must file Form INC-20A within 180 days showing share capital deposited into company bank account before starting business or taking loans."
        deadline = "Within 180 days of incorporation"
        penalty = "₹50,000 on Company + ₹1,000/day on Directors (Max ₹1 Lakh) + Company Strike Off risk!"
        tasks = [
            {"task": "Open corporate bank account and deposit share capital from subscribers", "status": "Filed", "action": "Download bank account statement showing share capital deposit"},
            {"task": "File Form INC-20A with bank statement attached on MCA V3 portal", "status": "Pending", "action": "Attach DSC of Director and CS/CA certification"}
        ]
    else:
        summary = "MCA notification issuing regulatory guidelines and compliance obligations for companies."
        tasks = [
            {"task": "Review circular requirements with legal counsel / CA", "status": "Review", "action": "Check applicability to startup entity type"},
            {"task": "File required form or record resolution in board minutes", "status": "Pending", "action": "Update StatutoryGuard compliance matrix"}
        ]

    return {
        "summary": summary,
        "deadline": deadline,
        "penalty_risk": penalty,
        "actionable_tasks": tasks
    }


def query_plain_english_assistant(question: str) -> str:
    """Answers founder compliance questions in plain English with statutory citations."""
    q = question.lower()

    # 1. Electronic Books of Account, Audit Trail, Edit Log & Record Retention (Section 128)
    if any(k in q for k in ["electronically", "books of account", "audit trail", "edit log", "preserve", "untraced", "user", "record", "128"]):
        return """**Compliance Analysis: Maintenance & Preservation of Electronic Books of Account (Section 128, Companies Act 2013)**

### 🚨 Statutory Violations Identified:
1. **Rule 3(1) Proviso of Companies (Accounts) Rules, 2014**:
   - Every company using accounting software must use software with an **unalterable Audit Trail (Edit Log)** feature.
   - Failure to log user IDs, date/time of transactions, or allowing untraced electronic changes directly violates Section 128(1).
2. **Section 128(5) - Failure to Preserve Records**:
   - Books of account relating to a period of at least **8 financial years** immediately preceding a financial year must be preserved in good order.
3. **Section 143(3)(j) - Auditor Audit Trail Reporting**:
   - Statutory auditors must explicitly report in Form AOC-4 whether the edit log operated seamlessly throughout the year.

---

### ⚖️ Penalties & Fines (Section 128(6)):
- **Officers in Default**: Managing Director, Whole-Time Director in charge of finance, CFO, and every other officer of the company.
- **Penalty**: Fine ranging between **₹50,000 to ₹5,00,000** or imprisonment for up to 6 months, or both.

---

### 📝 Step-by-Step Rectification Plan:
1. **Enable Audit Trail (Edit Log)**: Immediately upgrade accounting software (e.g. Tally Prime Edit Log / Zoho Books) to ensure edit logs are permanently enabled and cannot be disabled.
2. **Implement User Role Access**: Assign unique user credentials for every accountant/officer so all electronic entries trace back to individual user IDs.
3. **Restore Data Backups**: Retrieve electronic server/cloud backups to reconstruct any lost or unpreserved accounting records.
4. **Auditor Certificate**: Obtain an **Audit Trail & System Compliance Certificate** from your Statutory Auditor to attach with Form AOC-4."""

    # 2. Form INC-20A (Commencement of Business)
    elif any(k in q for k in ["inc-20a", "commencement", "180 days", "share capital deposit", "section 10a"]):
        return """**Form INC-20A (Declaration of Commencement of Business - Section 10A)**
- **Statutory Mandate:** Must be filed within **180 days of incorporation** before commencing any business operations or borrowing money.
- **Key Requirement:** Corporate bank account statement proving subscribers have deposited agreed share capital.
- **Penalties:** 
  - Company: **₹50,000**
  - Officers in Default: **₹1,000 per day** (Max ₹1,00,000)
  - ROC Action: Power to initiate **strike-off (cancellation)** of company registration under Chapter XVIII.
- **Action Plan:** Open corporate bank account immediately, deposit share capital, attach bank statement, and file Form INC-20A on MCA portal."""

    # 3. Form DIR-3 KYC & Director Identification Number
    elif any(k in q for k in ["dir-3", "kyc", "din", "director identification"]):
        return """**Form DIR-3 KYC (Director Identification Number Verification - Rule 12A)**
- **Statutory Mandate:** Annual KYC filing due by **September 30** for every individual holding a DIN as of March 31.
- **Penalties for Default:**
  - Flat late fee of **₹5,000 per director**.
  - **DIN Deactivation**: MCA marks the DIN as *'Deactivated due to non-filing of DIR-3 KYC'*, blocking all company ROC filings.
- **Action Plan:** If mobile number & email are unchanged, complete DIR-3 KYC WEB in 2 minutes using OTP validation."""

    # 4. AOC-4 (Financial Statements Filing)
    elif any(k in q for k in ["aoc-4", "aoc 4", "financial statement", "balance sheet filing", "section 137"]):
        return """**Form AOC-4 (Filing of Audited Financial Statements - Section 137)**
- **Statutory Mandate:** Must file audited Balance Sheet, Profit & Loss Account, Director's Report, and Auditor's Report within **30 days of AGM**.
- **Penalties for Default:**
  - Standard late fee: **₹100 per day of delay** without an upper cap!
  - Director Disqualification: Non-filing for 3 consecutive years leads to director disqualification under Section 164(2).
- **Action Plan:** Complete annual audit, hold AGM, obtain signed auditor's report, and file AOC-4 with ROC."""

    # 5. MGT-7 / MGT-7A (Annual Return Filing)
    elif any(k in q for k in ["mgt-7", "mgt 7", "annual return", "section 92"]):
        return """**Form MGT-7 / MGT-7A (Filing of Company Annual Return - Section 92)**
- **Statutory Mandate:** Must be filed within **60 days of AGM** containing details of shareholding, directors, and governance.
- **Penalties for Default:** Late fee of **₹100 per day** of delay per company.
- **Action Plan:** Prepare shareholder list as of FY end, get PCS certification (if applicable), and file Form MGT-7."""

    # 6. Board Meetings & Secretarial Standards
    elif any(k in q for k in ["board meeting", "how many", "gap", "quorum", "section 173", "ss-1"]):
        return """**Board Meeting Compliance (Section 173 & Secretarial Standard SS-1)**
- **Private Limited Company:** Minimum **4 board meetings per financial year**, with maximum gap between two consecutive meetings not exceeding **120 days**.
- **OPC / Small Startup:** Minimum **1 board meeting in each half of the calendar year** (gap not less than 90 days).
- **Notice Period:** Minimum **7 clear days written notice** with agenda to all directors.
- **Penalty for Default:** Fine of **₹25,000** per officer in default under Section 173(4)."""

    # 7. Corporate Social Responsibility (Section 135)
    elif any(k in q for k in ["csr", "social responsibility", "section 135", "net profit"]):
        return """**Corporate Social Responsibility (Section 135, Companies Act 2013)**
- **Applicability:** Net worth ≥ ₹500 Cr, Turnover ≥ ₹1,000 Cr, OR Net Profit ≥ ₹5 Cr in immediately preceding FY.
- **Mandate:** Spend at least **2% of average net profits** of 3 preceding FYs on CSR activities.
- **Penalties:** Company fined up to 2x unspent CSR amount; officers fined 1/10th of unspent amount (up to ₹2 Lakhs)."""

    # 8. General / Advanced Guidance Fallback Engine
    else:
        return f"""**StatutoryGuard Legal & Statutory Analysis**

### 📋 Overview for Query: "{question}"

1. **Applicable Statutory Framework**:
   - Under the **Companies Act, 2013** and MCA Rules, all Indian corporate entities (Pvt Ltd, OPC, LLP) must comply with statutory record-keeping and annual filings.
2. **Key Compliance Safeguards**:
   - **Board Minutes & Resolutions**: Record all board approvals in secretarial minutes within 30 days.
   - **Financial Record Integrity**: Maintain books of account with unalterable audit trails for at least **8 financial years** (Section 128).
   - **Annual Filings**: Ensure AOC-4 (Financials) and MGT-7 (Annual Return) are submitted on time to prevent **₹100/day** statutory penalties.
3. **Recommended Action**:
   - Verify active company status on the MCA V3 portal.
   - Run StatutoryGuard's **Pre-Submission Audit Rules Engine** on draft filings before submitting to ROC."""
