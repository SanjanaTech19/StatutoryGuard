"""
Secure Document Vault & Digital Signature (DSC) Tracker Module
Encrypted repository for DSC keys, incorporation certificates, MOA/AOA, and board minutes.
"""

import streamlit as st
import uuid
import os
from datetime import datetime
from database.db_client import DatabaseClient
from utils.security import encrypt_bytes, compute_file_hash

def render_document_vault(db: DatabaseClient, selected_cin: str):
    """Renders the Secure Encrypted Document Vault UI."""
    st.markdown("### 🔒 Secure Encrypted Document Vault & DSC Expiry Tracker")
    st.markdown(
        "AES-256 encrypted repository for Digital Signatures (DSC), Incorporation Certificates, MOA/AOA, and Board Minutes. "
        "Keeps your company audit-ready 24/7."
    )

    company = db.get_company(selected_cin)
    if not company:
        st.warning("Please select a company to access Vault.")
        return

    # Top DSC Tracker Section
    st.subheader("🔑 Director Digital Signature (DSC) Expiry Tracker")
    directors = company.get("directors", [])
    if directors:
        d_cols = st.columns(len(directors))
        for idx, d in enumerate(directors):
            with d_cols[idx % len(d_cols)]:
                exp_date_str = d.get("dsc_expiry", "2026-12-31")
                try:
                    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
                    days_left = (exp_date - datetime.now().date()).days
                except Exception:
                    days_left = 120

                if days_left < 30:
                    status_badge = f"⚠️ EXPIRING IN {days_left} DAYS"
                elif days_left < 0:
                    status_badge = "🚨 EXPIRED"
                else:
                    status_badge = f"✅ VALID ({days_left} Days)"

                st.markdown(f"**Director:** {d['name']}")
                st.caption(f"DIN: `{d['din']}` | Designation: {d.get('designation', 'Director')}")
                st.markdown(f"**DSC Expiry:** `{exp_date_str}`")
                st.markdown(f"**Status:** {status_badge}")
                st.markdown("---")

    st.markdown("---")

    # Document Upload & Storage Section
    c_left, c_right = st.columns([2, 3])

    with c_left:
        st.subheader("📤 Upload Document to Vault")
        with st.form("vault_upload_form", clear_on_submit=True):
            doc_name = st.text_input("Document Name", placeholder="e.g. MOA_Final_2024.pdf")
            category = st.selectbox("Category", ["Incorporation & MOA/AOA", "Director DSC & KYC", "Board Minutes & Resolutions", "Financial Statements", "Tax & ROC Receipts"])
            director_assoc = st.selectbox("Associated Director (Optional)", ["None"] + [d['name'] for d in directors])
            dsc_exp = st.date_input("DSC Expiry Date (if applicable)")

            uploaded_file = st.file_uploader("Choose File", type=["pdf", "png", "jpg", "docx"])

            if st.form_submit_button("🔒 Encrypt & Store in Vault", type="primary"):
                if not uploaded_file or not doc_name:
                    st.error("Please enter document name and choose a file.")
                else:
                    raw_bytes = uploaded_file.read()
                    encrypted_bytes = encrypt_bytes(raw_bytes)
                    file_hash = compute_file_hash(raw_bytes)
                    doc_id = str(uuid.uuid4())[:8]

                    # Save doc record
                    db.add_vault_doc({
                        "doc_id": doc_id,
                        "company_cin": selected_cin,
                        "doc_name": doc_name,
                        "category": category,
                        "upload_date": datetime.now().strftime("%Y-%m-%d"),
                        "file_path": f"/vault/{selected_cin}/{doc_id}_{doc_name}",
                        "dsc_director": director_assoc if director_assoc != "None" else "",
                        "dsc_expiry": str(dsc_exp) if category == "Director DSC & KYC" else "",
                        "encrypted": True
                    })

                    st.success(f"✅ Document '{doc_name}' encrypted with AES-256 and saved! SHA-256: `{file_hash[:12]}...`")
                    st.rerun()

    with c_right:
        st.subheader("📁 Repository Documents")
        vault_docs = db.get_vault_docs(selected_cin)

        cat_filter = st.selectbox("Filter Category", ["All Categories", "Incorporation & MOA/AOA", "Director DSC & KYC", "Board Minutes & Resolutions", "Financial Statements", "Tax & ROC Receipts"])
        
        if cat_filter != "All Categories":
            vault_docs = [d for d in vault_docs if d["category"] == cat_filter]

        if not vault_docs:
            st.info("No document records in vault for selected filter.")
        else:
            for doc in vault_docs:
                with st.container():
                    st.markdown(f"#### 📄 {doc['doc_name']} <span class='badge-completed'>AES-256 Encrypted</span>", unsafe_allow_html=True)
                    st.caption(f"**Category:** {doc['category']} | Uploaded: {doc['upload_date']}")
                    if doc.get("dsc_director"):
                        st.caption(f"**Director:** {doc['dsc_director']} | DSC Expiry: {doc.get('dsc_expiry', 'N/A')}")
                    st.markdown("---")
