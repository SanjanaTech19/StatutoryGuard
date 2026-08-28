"""
StatutoryGuard - AI-Driven Automated MCA/ROC Compliance Platform
Main Streamlit Entrypoint Application with Multi-Role Auth & Strict Admin Portal
"""

import streamlit as st
import os

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="StatutoryGuard - MCA/ROC Compliance Armour for Startups",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config import APP_NAME, APP_TAGLINE, APP_VERSION
from database.db_client import DatabaseClient
from database.seed_data import seed_database
from modules.auth import render_auth_page
from modules.admin_panel import render_admin_panel
from modules.dashboard import render_dashboard
from modules.validator import render_validator
from modules.legal_assistant import render_legal_assistant
from modules.alerts import render_alerts
from modules.document_vault import render_document_vault
from modules.mca_scraper import MCAScraper
from utils.compliance_calculator import calculate_statutory_tasks

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Database Client
db = DatabaseClient()

# Auto-seed database if empty
companies = db.list_companies()
if not companies:
    seed_database()
    companies = db.list_companies()

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "company_cin" not in st.session_state:
    st.session_state["company_cin"] = None

# Main Application Logic
if not st.session_state["authenticated"]:
    render_auth_page(db)
else:
    user = st.session_state["user"]
    role = st.session_state["role"]

    # Sidebar Branding & User Details
    st.sidebar.image("https://img.icons8.com/isometric/96/shield.png", width=64)
    st.sidebar.title("StatutoryGuard")
    st.sidebar.caption(f"{APP_TAGLINE} | v{APP_VERSION}")
    st.sidebar.markdown("---")

    # User Badge & Logout
    st.sidebar.markdown(f"👤 **Logged in as:** `{user['username']}`")
    st.sidebar.markdown(f"🔑 **Role:** `{role.upper()}`")

    if st.sidebar.button("🚪 Logout", type="secondary", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["company_cin"] = None
        st.rerun()

    st.sidebar.markdown("---")

    # Company Selection for Founder vs Admin
    company_options = {c["name"]: c["cin"] for c in companies}

    if role == "founder":
        user_cin = user.get("company_cin")
        if user_cin and user_cin in [c["cin"] for c in companies]:
            selected_cin = user_cin
            comp_obj = db.get_company(selected_cin)
            st.sidebar.markdown(f"**Active Startup:** {comp_obj['name']}")
        else:
            selected_company_name = st.sidebar.selectbox("Select Active Startup", list(company_options.keys()))
            selected_cin = company_options[selected_company_name]
    else: # Admin role
        st.sidebar.subheader("🏢 Active Startup Inspector")
        selected_company_name = st.sidebar.selectbox("Select Active Startup", list(company_options.keys()))
        selected_cin = company_options[selected_company_name]

    # Register New Startup Modal / Expander
    with st.sidebar.expander("➕ Onboard New Startup (CIN Lookup)", expanded=False):
        with st.form("onboard_form"):
            st.markdown("##### Lookup MCA Master Data by CIN")
            cin_input = st.text_input("Enter CIN Number", value="U72900KA2023PTC174821")
            
            if st.form_submit_button("Fetch & Register Company", type="primary"):
                if cin_input:
                    mca_data = MCAScraper.lookup_cin(cin_input)
                    db.save_company(mca_data)
                    tasks = calculate_statutory_tasks(mca_data)
                    db.save_tasks(tasks)
                    st.sidebar.success(f"Registered {mca_data['name']}!")
                    st.rerun()

    st.sidebar.markdown("---")

    # Quick Sidebar Stats
    company = db.get_company(selected_cin)
    if company:
        tasks = db.get_tasks_for_company(selected_cin)
        pending_cnt = sum(1 for t in tasks if t["status"] != "Filed")
        st.sidebar.metric("Entity Type", company["entity_type"])
        st.sidebar.metric("Incorporated On", company["incorporation_date"])
        st.sidebar.metric("Pending MCA Filings", pending_cnt)

    st.sidebar.markdown("---")
    st.sidebar.info("🛡️ Safeguarding against ₹5L Statutory Penalties & MCA Strike-off Risks.")

    # --- MAIN BRAND HEADER ---
    st.markdown(f"""
    <div class="brand-header">
        <div class="brand-title">🛡️ {APP_NAME}</div>
        <div class="brand-sub">{APP_TAGLINE} &bull; Tailored for Indian Startup Founders</div>
    </div>
    """, unsafe_allow_html=True)

    # --- MAIN NAVIGATION TABS BASED ON ROLE ---
    if role == "admin":
        tab_admin, tab_dashboard, tab_validator, tab_assistant, tab_alerts, tab_vault = st.tabs([
            "👑 System Admin Control Center",
            "📊 Centralized Dashboard",
            "🛡️ Pre-Submission Audit Engine",
            "🤖 Plain-English AI Assistant",
            "🔔 Automated Alerts Hub",
            "🔒 Encrypted Document Vault"
        ])

        with tab_admin:
            render_admin_panel(db)

        with tab_dashboard:
            render_dashboard(db, selected_cin)

        with tab_validator:
            render_validator()

        with tab_assistant:
            render_legal_assistant()

        with tab_alerts:
            render_alerts(db, selected_cin)

        with tab_vault:
            render_document_vault(db, selected_cin)

    else:
        tab_dashboard, tab_validator, tab_assistant, tab_alerts, tab_vault = st.tabs([
            "📊 Centralized Dashboard",
            "🛡️ Pre-Submission Audit Engine",
            "🤖 Plain-English AI Assistant",
            "🔔 Automated Alerts Hub",
            "🔒 Encrypted Document Vault"
        ])

        with tab_dashboard:
            render_dashboard(db, selected_cin)

        with tab_validator:
            render_validator()

        with tab_assistant:
            render_legal_assistant()

        with tab_alerts:
            render_alerts(db, selected_cin)

        with tab_vault:
            render_document_vault(db, selected_cin)
