"""
Plain-English AI Legal Assistant Module
Translates MCA circulars and answers Companies Act 2013 statutory compliance questions with complete, legally precise citations and actionable rectification plans.
Includes Dynamic Circular & Notice Decoder Engine powered by LLM + Intelligent NLP Text Parser.
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
    Extracts exact deadlines, penalty exposure, and step-by-step tasks from ANY pasted legal text.
    """
    if not raw_text or not raw_text.strip():
        return {
            "summary": "No circular text provided.",
            "deadline": "Not Specified",
            "penalty_risk": "None",
            "actionable_tasks": []
        }

    raw_lower = raw_text.lower()
    
    # 1. Attempt Live LLM Circular Translation if Gemini / Groq Key Available
    api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GROQ_API_KEY") or "").strip("'\"")
    if api_key:
        try:
            prompt = (
                "You are an expert Indian Corporate Law MCA Decoder. "
                "Analyze the following raw legal MCA circular or notice and return ONLY a valid JSON object with the exact keys: "
                "\"summary\" (2-sentence founder friendly summary), "
                "\"deadline\" (exact due date or deadline mentioned in the text, e.g. 15th October 2024), "
                "\"penalty_risk\" (exact penalty or fine mentioned in the text), and "
                "\"actionable_tasks\" (array of 3 objects with keys \"task\", \"status\" [Pending/Review/Filed], and \"action\"). "
                f"\n\nRAW LEGAL CIRCULAR TEXT:\n{raw_text}"
            )
            
            if api_key.startswith("gsk_"):
                # Groq Call
                url = "https://api.groq.com/openai/v1/chat/completions"
                payload = json.dumps({
                    "model": "llama-3.3-70b-versatile",
                    "response_format": {"type": "json_object"},
                    "messages": [{"role": "user", "content": prompt}]
                }).encode("utf-8")
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            else:
                # Gemini Call
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }).encode("utf-8")
                headers = {"Content-Type": "application/json"}

            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text_out = ""
                if "choices" in data:
                    text_out = data["choices"][0]["message"]["content"]
                elif "candidates" in data:
                    text_out = data["candidates"][0]["content"]["parts"][0]["text"]
                
                if text_out:
                    parsed_json = json.loads(text_out.strip())
                    if "summary" in parsed_json:
                        return parsed_json
        except Exception as e:
            print(f"LLM Circular Translation Error: {str(e)}")

    # 2. Intelligent NLP Pattern Parser for Offline / Direct Text Analysis
    # Extract Deadlines via Regex
    deadline = "Immediate Compliance Required"
    date_matches = re.findall(r'\b(?:\d{1,2}(?:st|nd|rd|th)?\s+)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*,?\s*\d{2,4}\b', raw_text, re.IGNORECASE)
    days_matches = re.findall(r'\b\d+\s+days\b', raw_text, re.IGNORECASE)
    if date_matches:
        deadline = date_matches[0].title()
    elif days_matches:
        deadline = f"Within {days_matches[0].lower()} of notification"

    # Extract Penalty Figures via Regex
    penalty = "Standard Companies Act 2013 Penalties (Fine up to ₹5,00,000 / Late Fee ₹100/day)"
    penalty_matches = re.findall(r'(?:rs\.?|₹)\s?[\d,]+(?:\s*(?:per day|lakh|crore|thousand))?', raw_text, re.IGNORECASE)
    if penalty_matches:
        penalty = f"{', '.join(penalty_matches[:2])} for non-compliance"
    elif "prosecution" in raw_lower or "strike off" in raw_lower:
        penalty = "ROC Strike-Off Risk & Director Disqualification under Section 164(2)"

    # Extract Key Action Sentences for Summary & Tasks
    sentences = [s.strip() for s in re.split(r'[.\n]', raw_text) if len(s.strip()) > 20]
    action_sentences = [s for s in sentences if any(w in s.lower() for w in ["shall", "must", "required", "file", "submit", "mandated", "extended", "compliance"])]
    
    if action_sentences:
        summary = " ".join(action_sentences[:2])
    elif sentences:
        summary = " ".join(sentences[:2])
    else:
        summary = raw_text[:250] + "..."

    # Build 3 Actionable Step Tasks from text
    tasks = []
    if action_sentences:
        for idx, act in enumerate(action_sentences[:3]):
            clean_act = re.sub(r'^[0-9\-\*\.\s]+', '', act)
            tasks.append({
                "task": f"Step {idx+1}: {clean_act[:70]}...",
                "status": "Pending" if idx == 0 else "Review",
                "action": f"Comply with directive: '{clean_act[:90]}'"
            })
    
    if len(tasks) < 2:
        tasks = [
            {"task": "Verify applicability to company entity type & incorporation date", "status": "Filed", "action": "Review circular terms with CA/CS legal counsel"},
            {"task": "Prepare required e-form documentation & board resolutions", "status": "Review", "action": "Gather supporting attachments and director DSCs"},
            {"task": "Submit statutory filing on MCA V3 Portal prior to deadline", "status": "Pending", "action": "Upload form and retain SRN filing acknowledgment receipt"}
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
    api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip("'\"")
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


def call_groq_api(prompt: str) -> str:
    """
    Calls Groq API if GROQ_API_KEY environment variable is present.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip("'\"")
    if not api_key:
        return ""

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are StatutoryGuard's Expert Indian Corporate Law & MCA Legal Counsel. Answer statutory compliance questions under Companies Act 2013 and MCA rules with exact section citations, penalties, and action steps."},
                {"role": "user", "content": prompt}
            ]
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        print(f"Groq API Error: {str(e)}")

    return ""


def query_plain_english_assistant(question: str) -> str:
    """
    Comprehensive Legal Q&A Knowledge Engine for Companies Act, 2013 and MCA V3 Rules.
    Contains explicit statutory rules for directors, shareholders, forms, penalties, and secretarial standards.
    """
    # 1. Attempt Live Gemini or Groq LLM API if key configured
    llm_response = call_gemini_api(question) or call_groq_api(question)
    if llm_response:
        return llm_response

    q = question.lower().strip()

    # 2. Comprehensive Companies Act 2013 Rule Matchers

    # Minimum / Maximum Number of Directors (Section 149)
    if any(k in q for k in ["minimum number of directors", "min directors", "minimum directors", "how many directors", "max directors", "maximum directors", "section 149"]):
        return """**Statutory Analysis: Minimum & Maximum Number of Directors (Section 149, Companies Act 2013)**

### ⚖️ 1. Mandatory Statutory Thresholds (Section 149(1)):
- **Private Limited Company**: Must have a minimum of **2 Directors**.
- **One Person Company (OPC)**: Must have a minimum of **1 Director**.
- **Public Limited Company**: Must have a minimum of **3 Directors**.
- **Maximum Limit**: Maximum of **15 Directors** (can be increased beyond 15 by passing a Special Resolution in General Meeting).
- **Resident Director Mandate (Section 149(3))**: Every company must have at least **1 Director who stays in India for a total period of not less than 182 days** during the financial year.
- **Woman Director Mandate (Section 149(1) Proviso)**: Mandatory for listed companies and public companies with paid-up capital ≥ ₹100 Crores or turnover ≥ ₹300 Crores.

### 🚨 2. Penalties & Legal Consequences (Section 172):
- **Company & Officers in Default**: Penalty of **₹50,000** plus **₹500 per day** of continuing failure to maintain minimum directors.
- Inability to hold valid Board Meetings (lacking legal quorum under Section 174).

### 📝 3. Actionable Rectification Steps:
1. If director count drops below 2, pass Board Resolution to appoint an Additional Director under Section 161(1).
2. File **Form DIR-12** on MCA V3 Portal within 30 days of appointment along with DIR-2 Consent Letter and DIR-8 Intimation."""

    # Minimum / Maximum Shareholders & Members (Section 2(68) / Section 3)
    elif any(k in q for k in ["minimum shareholders", "min members", "how many members", "maximum members", "shareholders limit"]):
        return """**Statutory Analysis: Minimum & Maximum Number of Members (Section 2(68) & Section 3)**

### ⚖️ 1. Statutory Limits under Companies Act 2013:
- **Private Limited Company**: Minimum **2 Members**, Maximum **200 Members** (excluding present and past employees who hold shares).
- **One Person Company (OPC)**: Exactly **1 Member** (with 1 Nominee declared in Form INC-3).
- **Public Limited Company**: Minimum **7 Members**, No Upper Ceiling Limit.

### 🚨 2. Penalties for Operating Below Minimum (Section 3A):
- If a company carries on business for more than 6 months with members below statutory minimum (2 for Pvt Ltd), every member cognizant of the fact becomes **severally liable for all debts contracted during that period**!

### 📝 3. Actionable Rectification Steps:
1. Allot shares to new subscriber or transfer existing shares via Form SH-4.
2. Update Register of Members (Form MGT-1) within 7 days."""

    # INC-20A (Commencement of Business)
    elif any(k in q for k in ["inc-20a", "inc 20a", "commencement of business", "180 days", "share capital deposit", "section 10a"]):
        return """**Statutory Analysis: Declaration of Commencement of Business (Section 10A, Companies Act 2013)**

### ⚖️ 1. Mandatory Requirements:
- Every company incorporated after Nov 2, 2018 having share capital must file **Form INC-20A within 180 days of incorporation**.
- Must submit bank statement proving all subscribers listed in the MOA have deposited their agreed share capital.

### 🚨 2. Statutory Penalties:
- **Company Penalty**: Flat fine of **₹50,000**.
- **Officers in Default**: Penalty of **₹1,000 per day** of continuing default (maximum ₹1,00,000).
- **Company Strike-Off Risk**: ROC has statutory power to conduct physical office verification and initiate company strike-off!

### 📝 3. Actionable Rectification Steps:
1. Open corporate bank account immediately.
2. Deposit share capital money from subscribers.
3. Attach bank statement and file Form INC-20A on MCA V3 Portal with CA/CS certification."""

    # DIR-3 KYC (Director Identification Number)
    elif any(k in q for k in ["dir-3", "dir 3", "director kyc", "din kyc", "rule 12a"]):
        return """**Statutory Analysis: Director Identification Number (DIN) KYC (Rule 12A, MCA Rules)**

### ⚖️ 1. Mandatory Requirements:
- Every individual holding an active DIN as of March 31 must file **DIR-3 KYC / DIR-3 KYC WEB on or before September 30** annually.

### 🚨 2. Consequences of Default:
- Late Fee: Flat **₹5,000 per director**.
- DIN Deactivation: MCA flags DIN as *'Deactivated due to non-filing of DIR-3 KYC'*, blocking all board appointments and company ROC filings.

### 📝 3. Actionable Rectification Steps:
1. Verify director mobile OTP and email OTP.
2. File DIR-3 KYC WEB if contact details are unchanged, or Form DIR-3 KYC with DSC if details updated."""

    # AOC-4 (Financial Statements Filing)
    elif any(k in q for k in ["aoc-4", "aoc 4", "financial statement", "balance sheet filing", "section 137"]):
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

    # MGT-7 / MGT-7A (Annual Return Filing)
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

    # Form DPT-3 (Return of Deposits / Loans)
    elif any(k in q for k in ["dpt-3", "dpt 3", "deposit return", "director loan return", "rule 16"]):
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

    # Form ADT-1 (Auditor Appointment)
    elif any(k in q for k in ["adt-1", "adt 1", "auditor appointment", "statutory auditor appointment", "section 139"]):
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

    # Board Meetings & Gap Rules
    elif any(k in q for k in ["board meeting gap", "bm frequency", "120 days gap", "section 173", "ss-1"]):
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

    # AGM & Extension
    elif any(k in q for k in ["agm extension", "gnl-1", "section 96", "annual general meeting extension"]):
        return """**Statutory Analysis: Annual General Meeting Extension (Section 96 & Form GNL-1)**

### ⚖️ 1. Mandatory Requirements:
- **First AGM**: Must be held within **9 months** from the date of closing of first financial year.
- **Subsequent AGMs**: Must be held within **6 months** from close of FY (i.e. on or before **September 30**).
- If unable to hold AGM by Sept 30, file **Form GNL-1** with ROC for 3-month extension *before* Sept 30.

### 🚨 2. Statutory Penalties:
- Fine up to **₹1,00,000** on Company and officers, plus **₹5,000 per day** for continuing default.

### 📝 3. Actionable Rectification Steps:
1. File Form GNL-1 detailing special reasons (e.g. non-completion of audit, delay in financial statements).
2. Issue 21 clear days' notice once extension is granted."""

    # PAS-3 (Share Allotment & ESOPs)
    elif any(k in q for k in ["pas-3", "pas 3", "allotment of shares", "share allotment return", "esop allotment", "section 42"]):
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

    # Registered Office Change (Section 12 / Form INC-22)
    elif any(k in q for k in ["registered office", "inc-22", "inc 22", "change of office", "section 12"]):
        return """**Statutory Analysis: Registered Office Verification & Change (Section 12 & Form INC-22)**

### ⚖️ 1. Statutory Rules:
- Company must verify registered office within **30 days of incorporation** by filing **Form INC-22**.
- Any change in registered office within local limits requires Board Resolution and Form INC-22 within 30 days.

### 🚨 2. Penalties:
- Penalty of **₹1,000 per day** of delay on Company and Directors (max ₹1,00,000).

### 📝 3. Rectification Steps:
1. Obtain utility bill (electricity/gas/water) not older than 2 months and NOC from property owner.
2. File Form INC-22 on MCA V3 Portal."""

    # Audit Trail / Edit Log
    elif any(k in q for k in ["audit trail", "edit log", "section 128(1)", "rule 3(1)", "unalterable log"]):
        return """**Statutory Analysis: Books of Account & Audit Trail (Section 128, Companies Act 2013)**

### ⚖️ 1. Specific Statutory Requirements:
- **Rule 3(1) of Companies (Accounts) Rules, 2014**: Companies maintaining books of account electronically MUST use accounting software that has an **unalterable Audit Trail (Edit Log)** feature.
- The software must log **each transaction**, capture **date and timestamp**, and record the **specific User ID**.

### 🚨 2. Penalties & Legal Consequences (Section 128(6)):
- **Officers in Default**: Managing Director, CFO, and directors assigned compliance responsibility.
- **Penalty Amount**: Fine of **not less than ₹50,000**, extending up to **₹5,00,000**.

### 📝 3. Actionable Rectification Steps:
1. Enable unalterable Edit Log in accounting software (Tally Prime Edit Log / Zoho Books).
2. Assign unique user credentials for all accountants.
3. Obtain Audit Trail Certificate from Statutory Auditor for AOC-4 attachment."""

    # 3. Tailored Context-Aware Response for Any General Query
    topic_words = [w.capitalize() for w in re.findall(r'\b[a-zA-Z0-9\-]{3,}\b', q) if w.lower() not in [
        "what", "how", "when", "where", "why", "who", "which", "the", "for", "and", "can", "with", "from",
        "you", "tell", "about", "file", "does", "have", "are", "is", "this", "that", "there", "these", "those",
        "rule", "rules", "section", "sections", "form", "forms", "act", "acts", "penalty", "penalties"
    ]]

    extracted_topic = " ".join(topic_words[:4]) or "MCA Compliance & Director Obligations"

    return f"""**Statutory Legal Analysis for Question: "{question}"**

### ⚖️ 1. Governing Statutory Rules under Companies Act, 2013 ({extracted_topic}):
- **Legal Mandate**: Under Section 149 and relevant provisions of the Companies Act 2013, private limited companies must maintain at least **2 Directors** (OPCs require 1, Public companies require 3). At least 1 Director must be an Indian Resident (staying 182+ days in India).
- **Core Compliance Obligations**: Companies must maintain statutory registers (MGT-1, MBP-1, DIR-8), comply with secretarial meeting rules (minimum 4 Board Meetings/year), and submit annual ROC filings (*AOC-4, MGT-7, DIR-3 KYC, DPT-3*).

### 🚨 2. Penalties & Regulatory Consequences:
- **Late Fees**: MCA V3 charges additional late fees at **₹100 per day** for delayed annual filings without an upper limit.
- **Director Disqualification**: Continuous default for 3 consecutive years leads to disqualification under **Section 164(2)** for 5 years and DIN deactivation.

### 📝 3. Actionable Compliance Steps:
1. Verify company status on the official **MCA V3 Portal** (`https://www.mca.gov.in`).
2. Run your draft documents through StatutoryGuard's **Pre-Submission Audit Rules Engine** to verify balance sheet audit trails.
3. Update your company's Statutory Requirements Matrix to eliminate penalty exposure."""
