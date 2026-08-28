"""
Audit-Ready Pre-Submission Validator Module
Pre-submission rules engine that flags balance sheet discrepancies, missing director signatures, and board resolution mismatches.
"""

import streamlit as st
from utils.pdf_parser import AuditValidatorEngine

SAMPLE_BALANCE_SHEET_TEXT = """
BALANCE SHEET OF INNOVATETECH SOLUTIONS PRIVATE LIMITED
AS ON 31ST MARCH 2024

I. EQUITY AND LIABILITIES
1. Shareholders' Funds
   (a) Share Capital: Rs. 500,000
   (b) Reserves and Surplus: Rs. 1,200,000
   Total Equity: Rs. 1,700,000

2. Non-Current & Current Liabilities
   (a) Trade Payables: Rs. 300,000
   (b) Short Term Provisions: Rs. 150,000
   Total Liabilities: Rs. 450,000

TOTAL EQUITY & LIABILITIES: Rs. 2,150,000

II. ASSETS
1. Non-Current Assets
   (a) Property, Plant & Equipment: Rs. 800,000
2. Current Assets
   (a) Trade Receivables: Rs. 500,000
   (b) Cash and Bank Balances: Rs. 750,000
   
TOTAL ASSETS: Rs. 2,050,000

ATTESTATION & SIGNATURE:
Director DIN: 08123456
Director DIN: 09876543
Place: Bengaluru
Date: 05-09-2024
Sd/- Rajesh Kumar (Managing Director)
"""

def render_validator():
    """Renders the Pre-Submission Audit Validator UI."""
    st.markdown("### 🛡️ Audit-Ready Pre-Submission Rules Engine")
    st.markdown(
        "Upload your draft financial statements, balance sheets, or board resolutions prior to MCA portal upload. "
        "StatutoryGuard runs automated checks to eliminate rejection risk and CA audit non-conformities."
    )

    doc_type = st.radio("Select Document Type for Audit", ["Financial Statement / Balance Sheet (AOC-4)", "Board Resolution (SS-1 Compliance)", "Annual Return (MGT-7)"], horizontal=True)

    uploaded_file = st.file_uploader("Upload PDF or Text File", type=["pdf", "txt"])

    use_sample = st.checkbox("Or test with Sample Balance Sheet with intentional math discrepancy", value=False)

    text_to_audit = ""
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            pdf_bytes = uploaded_file.read()
            text_to_audit = AuditValidatorEngine.extract_text_from_pdf(pdf_bytes)
        else:
            text_to_audit = uploaded_file.read().decode("utf-8")
    elif use_sample:
        text_to_audit = SAMPLE_BALANCE_SHEET_TEXT

    if st.button("🔍 Run Audit Engine Pre-Submission Scan", type="primary"):
        if not text_to_audit:
            st.error("Please upload a document or select the sample checkbox to test.")
            return

        st.markdown("---")
        st.subheader("📋 Audit Verification Results & Discrepancy Log")

        if "Balance Sheet" in doc_type or "AOC-4" in doc_type or use_sample:
            audit_result = AuditValidatorEngine.validate_balance_sheet_text(text_to_audit)
        else:
            audit_result = AuditValidatorEngine.validate_board_resolution(text_to_audit)

        score = audit_result["score"]
        is_valid = audit_result["is_valid"]
        discrepancies = audit_result["discrepancies"]
        extracted = audit_result["extracted_data"]

        # Results Summary Banner
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Audit Readiness Score", f"{score}/100", delta="PASSED" if is_valid else "FAILED", delta_color="normal" if is_valid else "inverse")
        with c2:
            st.metric("Validation Status", "AUDIT READY" if is_valid else "REJECTION RISK", delta=f"{len(discrepancies)} Issues Found")
        with c3:
            st.metric("Extracted Figures", f"{len(extracted)} Fields Extracted")

        st.markdown("#### Extracted Financial / Governance Data")
        st.json(extracted)

        st.markdown("#### 🚨 Detailed Discrepancy Breakdown")
        if not discrepancies:
            st.success("🎉 Zero discrepancies detected! Document is 100% Audit-Ready for MCA filing.")
        else:
            for disc in discrepancies:
                severity = disc["severity"]
                if severity == "CRITICAL":
                    st.error(f"**[{severity}] {disc['rule']}**\n\n{disc['description']}")
                elif severity == "HIGH":
                    st.warning(f"**[{severity}] {disc['rule']}**\n\n{disc['description']}")
                else:
                    st.info(f"**[{severity}] {disc['rule']}**\n\n{disc['description']}")

        with st.expander("📄 View Parsed Document Text", expanded=False):
            st.code(text_to_audit, language="text")
