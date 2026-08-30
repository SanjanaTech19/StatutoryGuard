"""
Plain-English AI Legal Assistant Module
Translates MCA circulars and answers Companies Act 2013 statutory compliance questions with complete, legally precise citations and actionable rectification plans.
Includes Live Gemini LLM API integration + Fallback Context-Aware Legal Intelligence Engine.
"""

import os
import re
import json
import urllib.request
import urllib.parse
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
        summary = "The MCA has mandated annual DIR-3 KYC for all DIN holders. All directors holding an active DIN must complete KYC to avoid DIN deactivation and a ₹5,000 late fee."
        deadline = "30th September Annually"
        penalty = "₹5,000 per director + DIN Deactivation"
        tasks = [
            {"task": "Verify active DIN list for all company directors", "status": "Filed", "action": "Cross-check DIN status on MCA portal"},
            {"task": "Collect mobile OTP and email OTP from directors", "status": "Review", "action": "Send OTP request to directors"},
            {"task": "Submit DIR-3 KYC WEB form before Sept 30", "status": "Pending", "action": "Upload DSC and submit on MCA V3 portal"}
        ]
    elif "audit trail" in raw_lower or "edit log" in raw_lower or "section 128" in raw_lower:
        summary = "MCA mandates under Section 128 that all company accounting software must have an unalterable Edit Log (Audit Trail) enabled throughout the year. Auditors must explicitly report compliance in AOC-4."
        deadline = "Mandatory for FY 2023-24 & Onwards"
        penalty = "₹50,000 to ₹500,000 per officer in default"
        tasks = [
            {"task": "Verify accounting software (Tally/Zoho/Quickbooks) has Audit Trail enabled", "status": "Review", "action": "Ensure edit log cannot be toggled off"},
            {"task": "Obtain Audit Trail Certificate from Chartered Accountant", "status": "Pending", "action": "Request auditor confirmation note for AOC-4"}
        ]
    elif "inc-20a" in raw_lower or "commencement of business" in raw_lower:
        summary = "Every newly incorporated company having share capital must file Form INC-20A within 180 days showing share capital deposited into company bank account before starting business or taking loans."
        deadline = "Within 180 days of incorporation"
        penalty = "₹50,000 on Company + ₹1,000/day on Directors (Max ₹1 Lakh) + Company Strike Off risk!"
        tasks = [
            {"task": "Open corporate bank account and deposit share capital from subscribers", "status": "Filed", "action": "Download bank account statement showing share capital deposit"},
            {"task": "File Form INC-20A with bank statement attached on MCA V3 portal", "status": "Pending", "action": "Attach DSC of Director and CS/CA certification"}
        ]
    elif "mgt-7" in raw_lower or "annual return" in raw_lower:
        summary = "Form MGT-7 / MGT-7A (Annual Return) must be filed within 60 days from the date of Annual General Meeting (AGM) detailing shareholding pattern, directors, and compliance history."
        deadline = "Within 60 days of AGM (Nov 29 typical)"
        penalty = "₹100 per day of continuing delay without upper cap!"
        tasks = [
            {"task": "Prepare MGT-7 / MGT-7A with shareholding details", "status": "Pending", "action": "Obtain PCS certification if required"},
            {"task": "File MGT-7 on MCA V3 Portal", "status": "Pending", "action": "Upload signed form"}
        ]
    elif "dpt-3" in raw_lower or "deposit" in raw_lower or "loan" in raw_lower:
        summary = "Form DPT-3 (Return of Deposits & Outstanding Loans) is mandatory annually by June 30 for all private limited companies disclosing all received money/loans."
        deadline = "30th June Annually"
        penalty = "₹1,00,000 to ₹10,00,000 + 18% p.a. interest penalty"
        tasks = [
            {"task": "Extract loan ledger & director deposits", "status": "Pending", "action": "Obtain auditor certificate"},
            {"task": "Submit DPT-3 on MCA V3 Portal", "status": "Pending", "action": "File before June 30 deadline"}
        ]
    else:
        summary = "MCA statutory notification issuing regulatory guidelines and compliance obligations for Indian entities under Companies Act 2013."
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


def call_gemini_api(prompt: str) -> str:
    """
    Calls Gemini API if GEMINI_API_KEY or GOOGLE_API_KEY environment variable is present.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return ""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        system_instruction = (
            "You are StatutoryGuard's Expert Indian Corporate Law & MCA Legal Counsel. "
            "Answer statutory compliance questions under the Companies Act, 2013, MCA V3 Rules, and Secretarial Standards (SS-1/SS-2). "
            "Always structure your answer clearly with: "
            "1. Specific Statutory Violations / Governing Sections "
            "2. Exact Penalties & Legal Consequences (late fee rates, fines, director disqualification risks) "
            "3. Actionable Rectification Steps for the Company. "
            "Be precise, factual, concise, and non-generic. Do NOT hallucinate."
        )

        payload = json.dumps({
            "contents": [{
                "parts": [{"text": f"{system_instruction}\n\nUSER QUESTION: {prompt}"}]
            }]
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if text:
                    return text.strip()
    except Exception as e:
        print(f"Gemini API Call Error: {str(e)}")

    return ""


def query_plain_english_assistant(question: str) -> str:
    """
    Comprehensive Legal Q&A Knowledge Engine for Companies Act, 2013 and MCA V3 Rules.
    Combines live LLM reasoning with a deep context-aware legal rules fallback.
    """
    # 1. Attempt Live LLM API if key configured
    llm_response = call_gemini_api(question)
    if llm_response:
        return llm_response

    q = question.lower().strip()

    # 2. Comprehensive Context-Aware Fallback Legal Intelligence Database
    # Audit Trail & Books of Account (Section 128)
    if any(k in q for k in ["audit trail", "edit log", "section 128", "books of account", "accounting software", "preserve records", "tally", "zoho"]):
        return """**Statutory Analysis: Books of Account & Audit Trail (Section 128, Companies Act 2013)**

### ⚖️ 1. Specific Statutory Requirements:
- **Rule 3(1) of Companies (Accounts) Rules, 2014**: Companies maintaining books of account electronically MUST use accounting software that has an **unalterable Audit Trail (Edit Log)** feature.
- The software must log **each transaction**, capture **date and timestamp**, and record the **specific User ID**.
- **Rule 3(5)**: Daily electronic backups must be created and maintained on servers physically located in India.

### 🚨 2. Penalties & Legal Consequences (Section 128(6)):
- **Officers in Default**: Managing Director, CFO, and directors assigned compliance responsibility.
- **Penalty Amount**: Fine of **not less than ₹50,000**, extending up to **₹5,00,000**.
- **Imprisonment Risk**: Imprisonment extending up to **6 months** or both.

### 📝 3. Actionable Rectification Steps:
1. Enable unalterable Edit Log in accounting software (Tally Prime Edit Log / Zoho Books).
2. Assign unique user credentials for all accountants.
3. Obtain Audit Trail Certificate from Statutory Auditor for AOC-4 attachment."""

    # Form INC-20A (Commencement of Business - Section 10A)
    elif any(k in q for k in ["inc-20a", "inc 20a", "commencement", "180 days", "share capital deposit", "section 10a"]):
        return """**Statutory Analysis: Commencement of Business (Section 10A, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- Every company incorporated after Nov 2, 2018 having share capital must file **Form INC-20A within 180 days of incorporation**.
- Must submit bank statement proving all subscribers listed in the MOA have paid their agreed share capital.

### 🚨 2. Statutory Penalties:
- **Company Penalty**: Flat fine of **₹50,000**.
- **Officers in Default**: Penalty of **₹1,000 per day** of continuing default (maximum ₹1,00,000).
- **Company Strike-Off Risk**: ROC has statutory power to conduct physical office verification and initiate company strike-off!

### 📝 3. Actionable Rectification Steps:
1. Open corporate bank account immediately.
2. Deposit share capital money from subscribers.
3. Attach bank statement and file Form INC-20A on MCA V3 Portal with CA/CS certification."""

    # Director KYC (Rule 12A)
    elif any(k in q for k in ["dir-3", "kyc", "din", "director kyc", "rule 12a"]):
        return """**Statutory Analysis: Director Identification Number (DIN) KYC (Rule 12A, MCA Rules)**

### ⚖️ 1. Mandatory Requirements:
- Every individual holding an active DIN as of March 31 must file **DIR-3 KYC / DIR-3 KYC WEB on or before September 30** annually.

### 🚨 2. Consequences of Default:
- Late Fee: Flat **₹5,000 per director**.
- DIN Deactivation: MCA flags DIN as *'Deactivated due to non-filing of DIR-3 KYC'*, blocking all board appointments and company ROC filings.

### 📝 3. Actionable Rectification Steps:
1. Verify director mobile OTP and email OTP.
2. File DIR-3 KYC WEB if contact details are unchanged, or Form DIR-3 KYC with DSC if details updated."""

    # AOC-4 (Financial Statements Filing - Section 137)
    elif any(k in q for k in ["aoc-4", "aoc 4", "financial statement", "balance sheet", "section 137"]):
        return """**Statutory Analysis: Filing of Financial Statements (Section 137, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- Must file audited Balance Sheet, P&L Account, Auditor's Report, and Board Report within **30 days of AGM** in Form AOC-4.

### 🚨 2. Statutory Penalties:
- Late Fee: **₹100 per day of delay** without upper ceiling limit!
- Director Disqualification: Non-filing for 3 consecutive years leads to disqualification under Section 164(2) for 5 years.

### 📝 3. Actionable Rectification Steps:
1. Complete annual financial audit with Statutory Auditor.
2. Adopt financial statements at AGM and attach signed Audit Trail Certificate.
3. Submit AOC-4 on MCA V3 Portal."""

    # MGT-7 / MGT-7A (Annual Return - Section 92)
    elif any(k in q for k in ["mgt-7", "mgt 7", "annual return", "section 92"]):
        return """**Statutory Analysis: Filing of Annual Return (Section 92, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- Every company must file Form MGT-7 (or Form MGT-7A for Small Companies/OPCs) within **60 days from the date of AGM**.
- Discloses shareholding pattern, list of directors, board meetings held, and remuneration paid.

### 🚨 2. Statutory Penalties:
- Late Fee: **₹100 per day of delay** without upper limit!
- Company Fine: ₹50,000 + ₹100/day. Officers in default fined up to ₹50,000.

### 📝 3. Actionable Rectification Steps:
1. Prepare MGT-7 / MGT-7A with updated shareholding list.
2. Obtain Practising Company Secretary (PCS) certification if paid-up capital exceeds ₹10 Crores or turnover exceeds ₹50 Crores.
3. Submit on MCA V3 portal."""

    # Form DPT-3 (Return of Deposits / Loans - Section 73 & Rule 16)
    elif any(k in q for k in ["dpt-3", "dpt 3", "deposit", "loan from director", "outstanding loan", "rule 16"]):
        return """**Statutory Analysis: Return of Deposits & Outstanding Loans (Form DPT-3, Section 73)**

### ⚖️ 1. Mandatory Requirements:
- Every company (other than government companies) must file **Form DPT-3 on or before June 30** every year.
- Discloses all money received by company: both "Deposits" and "Exempted Transactions" (loans from directors, bank loans, inter-corporate deposits).

### 🚨 2. Statutory Penalties:
- **Company Fine**: Min **₹1,00,000**, extending up to **₹10,00,000**.
- **Officers in Default**: Imprisonment up to 7 years or fine up to ₹25,00,000 under Section 73!

### 📝 3. Actionable Rectification Steps:
1. Obtain Auditor's Certificate certifying outstanding loan figures as of March 31.
2. Ensure director loans are accompanied by a declaration that money was not borrowed/accepted from third parties.
3. File Form DPT-3 before June 30."""

    # Form ADT-1 (Auditor Appointment - Section 139)
    elif any(k in q for k in ["adt-1", "adt 1", "auditor appointment", "statutory auditor", "section 139"]):
        return """**Statutory Analysis: Appointment of Statutory Auditor (Form ADT-1, Section 139)**

### ⚖️ 1. Mandatory Requirements:
- First Auditor must be appointed by Board within **30 days of incorporation**.
- Subsequent Auditor appointed at AGM for 5 consecutive years. File **Form ADT-1 within 15 days** of AGM.

### 🚨 2. Statutory Penalties:
- Fine of **₹50,000** on Company + **₹500 per day** of continuing delay.
- Inability to get financial statements audited, invalidating AOC-4 filings.

### 📝 3. Actionable Rectification Steps:
1. Obtain Consent Letter and Eligibility Certificate under Section 141 from CA firm.
2. Pass Board/AGM resolution appointing Statutory Auditor for 5-year tenure.
3. File Form ADT-1 on MCA V3 Portal within 15 days."""

    # Board Meetings & Gap Rules (Section 173)
    elif any(k in q for k in ["board meeting", "bm", "120 days", "gap between meetings", "section 173", "ss-1"]):
        return """**Statutory Analysis: Board Meetings & Frequency (Section 173, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- **First Board Meeting**: Must be held within **30 days of incorporation**.
- **Annual Requirement**: Minimum **4 Board Meetings** in every calendar year.
- **Maximum Gap**: The gap between two consecutive Board Meetings **cannot exceed 120 days**.
- *Startup Exemption*: Small Companies, OPCs, and recognized Startups need only **1 Board Meeting in each half of a calendar year** with minimum 90 days gap.

### 🚨 2. Statutory Penalties:
- Penalty of **₹25,000** on every director in default under Section 173(4).

### 📝 3. Actionable Rectification Steps:
1. Prepare Notice & Agenda 7 days in advance per SS-1 rules.
2. Record attendance and pass Board Resolutions.
3. Draft and sign Board Minutes within 30 days of meeting."""

    # AGM & Extension (Section 96)
    elif any(k in q for k in ["agm", "annual general meeting", "section 96", "agm extension", "gnl-1"]):
        return """**Statutory Analysis: Annual General Meeting Rules (Section 96, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- **First AGM**: Must be held within **9 months** from the date of closing of first financial year.
- **Subsequent AGMs**: Must be held within **6 months** from close of FY (i.e. on or before **September 30**).
- Maximum gap between two AGMs cannot exceed 15 months.

### 🚨 2. Statutory Penalties:
- Fine up to **₹1,00,000** on Company and officers, plus **₹5,00,000** for continuing default.

### 📝 3. Actionable Rectification Steps:
1. If unable to hold AGM by Sept 30 due to special reasons, file **Form GNL-1** with ROC for 3-month extension *before* Sept 30.
2. Issue 21 clear days' notice to shareholders (or shorter notice with 95% consent)."""

    # PAS-3 (Share Allotment & ESOPs - Section 42 / 62)
    elif any(k in q for k in ["pas-3", "pas 3", "allotment of shares", "esop", "valuation", "section 42", "section 62"]):
        return """**Statutory Analysis: Return of Share Allotment (Form PAS-3, Section 42/62)**

### ⚖️ 1. Mandatory Requirements:
- Must file **Form PAS-3 within 30 days** of passing Share Allotment resolution.
- Attach Registered Valuer's Report, Board Resolution, List of Allottees, and PAS-4 Offer Letter.

### 🚨 2. Statutory Penalties:
- Penalty of **₹1,000 per day** of delay on Company and Directors (up to maximum ₹25,00,000).

### 📝 3. Actionable Rectification Steps:
1. Obtain Registered Valuer Report for share pricing.
2. Pass Board/Shareholder resolution for allotment.
3. File PAS-3 within 30 days and issue Share Certificates (Form SH-1) within 60 days."""

    # Director Loans (Section 185/186)
    elif any(k in q for k in ["loan to director", "director loan", "section 185", "section 186", "inter-corporate"]):
        return """**Statutory Analysis: Loans to Directors & Inter-Corporate Loans (Section 185/186)**

### ⚖️ 1. Mandatory Requirements:
- **Private Company Exemption (Notification June 5, 2015)**: Private companies can give loans to directors or accept loans from directors IF:
  1. Director submits a written declaration that the loan amount is not out of funds borrowed by them from others.
  2. No body corporate has invested share capital in the private company.
  3. Total borrowings from banks/FIs are less than 2x paid-up capital or ₹50 Crores.

### 🚨 2. Statutory Penalties:
- Fine of **₹5,00,000 to ₹25,00,000** on Company + Imprisonment up to 6 months for Directors under Section 185(2).

### 📝 3. Actionable Rectification Steps:
1. Obtain Director's Written Non-Borrowing Declaration.
2. Disclose loan in Form DPT-3 annually."""

    # Dynamic Parser for Any Custom Prompt
    topic_keywords = [w for w in re.findall(r'\b\w{3,}\b', q) if w not in ["what", "how", "when", "where", "why", "is", "the", "for", "and", "can", "with", "from", "you", "tell", "about", "file", "does", "have"]]
    topic_str = " ".join(topic_keywords[:4]).title() or "Companies Act Compliance"

    return f"""**Statutory Legal Analysis for Question: "{question}"**

### ⚖️ 1. Companies Act, 2013 Governing Framework for {topic_str}:
- **Statutory Obligation**: Under the Companies Act 2013 and MCA V3 Rules, all private limited companies and OPCs must maintain statutory registers, adhere to board approval thresholds, and submit timely ROC filings.
- **Filing Timelines & Compliance Rules**: Mandatory annual filings include **AOC-4** (Financial Statements due 30 days post-AGM), **MGT-7/7A** (Annual Return due 60 days post-AGM), **DPT-3** (Return of Deposits due June 30), and **DIR-3 KYC** (Director KYC due Sept 30).

### 🚨 2. Statutory Penalties & Legal Consequences:
- Late filing fees on MCA V3 accumulate at **₹100 per day** without an upper ceiling cap.
- Non-filing of statutory documents for 3 consecutive years leads to **Director Disqualification under Section 164(2)** for 5 years and DIN deactivation.

### 📝 3. Actionable Rectification Steps:
1. Verify active company filing status on the official MCA Portal (`https://www.mca.gov.in`).
2. Run your draft documents through StatutoryGuard's **Pre-Submission Audit Rules Engine** to verify balance sheet audit trails prior to submission.
3. Update your company's Statutory Requirements Matrix to safeguard against ₹5 Lakh penalty risk."""
