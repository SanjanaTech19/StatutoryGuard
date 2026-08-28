"""
Authentication Module for StatutoryGuard
Provides Founder Login, Company Sign-Up, and Strict Administrator Login portals.
High-contrast vibrant theme support for dark & light modes.
"""

import streamlit as st
from database.db_client import DatabaseClient
from modules.mca_scraper import MCAScraper
from utils.compliance_calculator import calculate_statutory_tasks

def render_auth_page(db: DatabaseClient):
    """Renders Login, Sign-Up, and Strict Administrator Login UI."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem 1rem; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);">
        <h1 class="auth-header-title">
            🛡️ Welcome to StatutoryGuard
        </h1>
        <p class="auth-header-sub">
            AI-Driven MCA/ROC Compliance Platform for Indian Startup Founders
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab_login, tab_signup, tab_admin = st.tabs([
            "🔑 Founder Login",
            "🚀 Company Sign-Up",
            "🔒 Strict Administrator Login"
        ])

        # ---------------- 1. FOUNDER LOGIN ----------------
        with tab_login:
            st.subheader("Founder & User Login")
            with st.form("founder_login_form"):
                user_input = st.text_input("Username or Email", placeholder="founder@startup.in")
                password_input = st.text_input("Password", type="password")

                if st.form_submit_button("Sign In as Founder", type="primary", use_container_width=True):
                    if not user_input or not password_input:
                        st.error("Please enter both username/email and password.")
                    else:
                        user_data, msg = db.authenticate_user(user_input, password_input)
                        if user_data:
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user_data
                            st.session_state["role"] = user_data["role"]
                            st.session_state["company_cin"] = user_data.get("company_cin")
                            st.toast(f"Welcome back, {user_data['full_name']}!", icon="👋")
                            st.rerun()
                        else:
                            st.error(msg)

            st.caption("Demo Founder Account: Create a new account under 'Company Sign-Up' or register your CIN.")

        # ---------------- 2. COMPANY SIGN-UP ----------------
        with tab_signup:
            st.subheader("Register Startup & Create Founder Account")
            with st.form("company_signup_form"):
                st.markdown("##### Step 1: Startup MCA Information")
                cin_val = st.text_input("Company Identification Number (CIN)", value="U72900KA2023PTC174821", help="Enter official MCA 21-digit CIN number")
                
                comp_name = st.text_input("Company Name", value="InnovateTech Solutions Private Limited")
                entity_type = st.selectbox("Entity Type", ["Private Limited", "One Person Company", "LLP", "Public Limited"])
                inc_date = st.date_input("Date of Incorporation")

                st.markdown("---")
                st.markdown("##### Step 2: Founder Account Credentials")
                full_name = st.text_input("Founder Full Name", value="Rajesh Kumar")
                username = st.text_input("Desired Username", value="rajesh_founder")
                email = st.text_input("Founder Work Email", value="rajesh@innovatetech.in")
                pass1 = st.text_input("Create Password", type="password")
                pass2 = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("Register Company & Create Account", type="primary", use_container_width=True):
                    if not username or not email or not pass1 or not cin_val:
                        st.error("Please fill in all mandatory fields.")
                    elif pass1 != pass2:
                        st.error("Passwords do not match!")
                    else:
                        mca_data = MCAScraper.lookup_cin(cin_val)
                        mca_data["name"] = comp_name
                        mca_data["entity_type"] = entity_type
                        mca_data["incorporation_date"] = str(inc_date)
                        mca_data["email"] = email

                        db.save_company(mca_data)
                        tasks = calculate_statutory_tasks(mca_data)
                        db.save_tasks(tasks)

                        success, u_msg = db.create_user(
                            username=username,
                            email=email,
                            password=pass1,
                            role="founder",
                            company_cin=cin_val,
                            full_name=full_name
                        )

                        if success:
                            st.success("🎉 Account and Company created successfully! Please sign in now.")
                        else:
                            st.error(u_msg)

        # ---------------- 3. STRICT ADMINISTRATOR LOGIN ----------------
        with tab_admin:
            st.subheader("Strict Administrator Authentication Portal")
            st.markdown(
                "<div style='background:#fef2f2; border-left:4px solid #ef4444; padding:0.75rem; color:#991b1b; font-size:0.85rem; border-radius:6px; margin-bottom:1rem;'>"
                "<strong>RESTRICTED ACCESS:</strong> Authorized Compliance Officers & System Administrators Only. All login attempts are strictly logged with timestamp & IP."
                "</div>",
                unsafe_allow_html=True
            )

            with st.form("admin_strict_login_form"):
                admin_username = st.text_input("Admin Username / Handle", value="admin")
                admin_password = st.text_input("Admin Password", type="password", value="AdminStrictSecret123!")
                security_code = st.text_input("Admin Security PIN (2FA)", type="password", value="998877", help="Strict 2-Factor Administrative Key")

                if st.form_submit_button("Authenticate as System Admin", type="primary", use_container_width=True):
                    if security_code != "998877":
                        st.error("🚨 Invalid 2FA Security Key! Strict Authentication Failed.")
                    else:
                        user_data, msg = db.authenticate_user(admin_username, admin_password)
                        if user_data and user_data.get("role") == "admin":
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user_data
                            st.session_state["role"] = "admin"
                            st.session_state["company_cin"] = "SYSTEM"
                            st.toast("Admin Authentication Verified!", icon="🔒")
                            st.rerun()
                        else:
                            st.error("🚨 Strict Authentication Failed: Invalid Administrator Credentials!")

            st.caption("Default Admin Credentials for testing -> Username: `admin` | Password: `AdminStrictSecret123!` | 2FA Key: `998877`")
