"""
Plain-English AI Legal Assistant Module
Translates dense MCA circulars into step-by-step task lists with clear status indicators (Pending, Review, Filed).
"""

import streamlit as st
import json
from config import SAMPLE_MCA_CIRCULARS

# Plain-English AI translation engine fallback
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
        deadline = "Immediate (Mandatory for FY 2023-24 & 2024-25)",
        penalty = "₹50,000 to ₹500,000 per officer in default"
        tasks = [
            {"task": "Verify accounting software (Tally/Zoho/Quickbooks) has Audit Trail enabled", "status": "Review", "action": "Ensure edit log cannot be toggled off"},
            {"task": "Obtain Audit Trail Certificate from Chartered Accountant", "status": "Pending", "action": "Request auditor confirmation note for AOC-4"}
        ]
    elif "inc-20a" in raw_lower or "commencement of business" in raw_lower:
        summary = "Every newly incorporated company must file Form INC-20A within 180 days showing share capital deposited into company bank account before starting business or taking loans."
        deadline = "Within 180 days of incorporation",
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
    
    if "inc-20a" in q or "commencement" in q:
        return """**Form INC-20A (Commencement of Business)**
- **What it is:** A mandatory declaration filed with ROC within **180 days of incorporation**.
- **Requirement:** Bank statement proving that subscribers have deposited share capital money into the company's bank account.
- **Penalty if missed:** ₹50,000 for the company, ₹1,000/day per director (up to ₹1 Lakh), AND ROC can initiate **strike-off** proceedings to close your company!
- **Action Needed:** Open bank account immediately, transfer capital, and file INC-20A."""

    elif "dir-3" in q or "kyc" in q:
        return """**Form DIR-3 KYC**
- **What it is:** Annual KYC verification for every individual who holds a Director Identification Number (DIN).
- **Due Date:** September 30 every financial year.
- **Penalty if missed:** Flat **₹5,000 fee per director** and the DIN is marked as **'Deactivated due to Non-Filing of DIR-3 KYC'** (blocking all company filings).
- **How to file:** If mobile/email is unchanged, file DIR-3 KYC WEB in 2 minutes with OTP."""

    elif "aoc-4" in q or "financial statement" in q:
        return """**Form AOC-4 (Financial Statements)**
- **What it is:** Filing audited Balance Sheet, P&L Account, Director's Report, and Auditor's Report with ROC.
- **Due Date:** Within **30 days of Annual General Meeting (AGM)** (typically Oct 30).
- **Penalty if missed:** **₹100 per day** of delay with NO upper ceiling cap on additional fees + potential director disqualification under Sec 164(2)."""

    elif "board meeting" in q or "how many" in q:
        return """**Board Meeting Requirements (Companies Act, 2013)**
- **Private Limited Company:** Minimum **4 board meetings per financial year**, with maximum gap between two consecutive meetings not exceeding **120 days**.
- **Small Startup / OPC / Dormant Co:** Minimum **1 board meeting in each half of the calendar year** (gap not less than 90 days).
- **Notice Required:** Minimum 7 clear days written notice (SS-1 compliance)."""

    else:
        return f"""**StatutoryGuard Legal Assistant Advice for: "{question}"**
- Under Section 134/173 of the Companies Act 2013, early-stage startups must maintain compliance records in digital format.
- **Key Recommendation:** Verify your company's incorporation date and ensure DIR-3 KYC, AOC-4, and MGT-7 filings are kept current to maintain an active MCA status.
- Consult your company secretary or use StatutoryGuard's Pre-Submission Audit Validator before uploading documents on the MCA V3 portal."""


def render_legal_assistant():
    """Renders the Plain-English Legal Assistant UI."""
    st.markdown("### 🤖 Plain-English MCA Legal Assistant")
    st.markdown(
        "Translates dense Indian legal circulars into step-by-step task lists with clear status indicators (`Pending`, `Review`, `Filed`)."
    )

    t1, t2 = st.tabs(["📄 Circular Translator & Task Extractor", "💬 Compliance Q&A Assistant"])

    with t1:
        st.subheader("Legal Circular & Notice Decoder")

        selected_preset = st.selectbox(
            "Choose Sample MCA Notification or Paste Custom Circular",
            ["Select Preset..."] + [c["title"] for c in SAMPLE_MCA_CIRCULARS]
        )

        custom_text = st.text_area("Paste MCA Circular Text / Legal Circular", height=180)

        raw_input = custom_text
        if selected_preset != "Select Preset...":
            for c in SAMPLE_MCA_CIRCULARS:
                if c["title"] == selected_preset:
                    raw_input = c["raw_text"]
                    break

        if st.button("✨ Translate to Plain-English & Extract Action List", type="primary"):
            if not raw_input:
                st.error("Please select a preset circular or paste legal circular text.")
                return

            parsed = translate_circular_to_plain_english(raw_input)

            st.markdown("---")
            st.markdown("#### 💡 Plain-English Summary")
            st.info(parsed["summary"])

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**🗓️ Compliance Due Date:** `{parsed['deadline']}`")
            with c2:
                st.markdown(f"**🚨 Penalty Exposure:** `{parsed['penalty_risk']}`")

            st.markdown("#### 📝 Actionable Task List")
            for item in parsed["actionable_tasks"]:
                status = item["status"]
                status_class = "status-filed" if status == "Filed" else ("status-review" if status == "Review" else "status-pending")
                
                st.markdown(
                    f"- **Task:** {item['task']} | Status: <span class='{status_class}'>[{status.upper()}]</span>\n"
                    f"  - *Action:* {item['action']}",
                    unsafe_allow_html=True
                )

    with t2:
        st.subheader("💬 Ask StatutoryGuard AI")
        st.caption("Ask questions about Companies Act 2013, MCA V3 portal rules, or ROC deadlines in plain English.")

        user_q = st.text_input("Ask a compliance question (e.g. 'What is the penalty for missing INC-20A?')", "")
        if st.button("Ask Assistant", type="primary") or user_q:
            if user_q:
                ans = query_plain_english_assistant(user_q)
                st.markdown(ans)
