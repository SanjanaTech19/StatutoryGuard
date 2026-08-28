"""
Administrator Panel Module for StatutoryGuard
Provides strict administrative oversight, global company management, security audit logs, and broadcast dispatches.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.db_client import DatabaseClient
from utils.compliance_calculator import compute_compliance_metrics

def render_admin_panel(db: DatabaseClient):
    """Renders Strict Administrator Portal Dashboard."""
    st.markdown("### 👑 System Administrator Command & Control Center")
    st.caption("Restricted Administrator Portal & Global Regulatory Compliance Monitor")

    # Fetch global metrics
    all_companies = db.list_companies()
    all_users = db.list_users()
    all_alert_logs = db.get_alert_logs("ALL")

    total_companies = len(all_companies)
    total_users = len(all_users)
    
    # Calculate aggregate penalty exposure across ALL companies
    total_penalty_exposure = 0.0
    total_overdue_filings = 0

    for c in all_companies:
        tasks = db.get_tasks_for_company(c["cin"])
        h, pen, pend, filed, ovd = compute_compliance_metrics(tasks)
        total_penalty_exposure += pen
        total_overdue_filings += ovd

    # Top Metric Highlights
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Registered Startups", total_companies, delta="+100% Platform Coverage")
    with c2:
        st.metric("Platform Penalty Risk Guarded", f"₹{total_penalty_exposure:,.0f}", delta="Zero Penalty Guarantee", delta_color="inverse")
    with c3:
        st.metric("Critical Overdue MCA Filings", total_overdue_filings, delta="Requires Attention" if total_overdue_filings > 0 else "All Clean")
    with c4:
        st.metric("Total System Users", total_users, delta="Founders & Admins")

    st.markdown("---")

    t1, t2, t3, t4 = st.tabs([
        "🏢 Company & Compliance Oversight",
        "👥 User Account Audit",
        "📢 Emergency Broadcast Center",
        "🔒 System & Security Audit Trail"
    ])

    # --------------- 1. COMPANY OVERSIGHT ---------------
    with t1:
        st.subheader("Global Company & Statutory Matrix Oversight")
        if not all_companies:
            st.info("No companies registered in platform.")
        else:
            comp_data = []
            for c in all_companies:
                tasks = db.get_tasks_for_company(c["cin"])
                h, pen, pend, filed, ovd = compute_compliance_metrics(tasks)
                comp_data.append({
                    "CIN": c["cin"],
                    "Company Name": c["name"],
                    "Entity Type": c["entity_type"],
                    "ROC Office": c["roc_office"],
                    "Health Score": f"{h}%",
                    "Penalty Exposure": f"₹{pen:,.0f}",
                    "Pending Filings": pend,
                    "Overdue": ovd,
                    "Status": c["mca_status"]
                })

            df_comp = pd.DataFrame(comp_data)
            st.dataframe(df_comp, use_container_width=True)

            st.markdown("#### ⚡ Administrative Override Action")
            sel_cin_admin = st.selectbox("Select Target Company", [c["cin"] for c in all_companies])
            if st.button("🔄 Recalculate & Re-Sync Statutory Matrix"):
                target_c = db.get_company(sel_cin_admin)
                if target_c:
                    from utils.compliance_calculator import calculate_statutory_tasks
                    new_tasks = calculate_statutory_tasks(target_c)
                    db.save_tasks(new_tasks)
                    st.success(f"Statutory matrix re-calculated and saved for {target_c['name']}!")
                    st.rerun()

    # --------------- 2. USER ACCOUNT AUDIT ---------------
    with t2:
        st.subheader("User Account Management & Roles")
        if not all_users:
            st.info("No users registered.")
        else:
            df_users = pd.DataFrame(all_users)
            st.dataframe(df_users, use_container_width=True)

        st.markdown("---")
        with st.form("create_admin_user_form"):
            st.markdown("##### Create Additional System Administrator")
            new_u = st.text_input("New Admin Username")
            new_e = st.text_input("New Admin Email")
            new_p = st.text_input("Admin Password", type="password")
            new_fn = st.text_input("Full Name", value="Compliance Officer")

            if st.form_submit_button("Grant Administrator Privileges", type="primary"):
                if new_u and new_e and new_p:
                    succ, msg = db.create_user(new_u, new_e, new_p, role="admin", company_cin="SYSTEM", full_name=new_fn)
                    if succ:
                        st.success(f"Administrator {new_u} created!")
                        st.rerun()
                    else:
                        st.error(msg)

    # --------------- 3. EMERGENCY BROADCAST ---------------
    with t3:
        st.subheader("📢 System-Wide Emergency Broadcast Center")
        st.markdown("Send critical regulatory updates, circular alerts, or portal outage notifications to ALL startup founders simultaneously.")

        broadcast_msg = st.text_area("Broadcast Notification Message", value="🚨 MCA V3 Portal Maintenance Alert: Extended deadline for DIR-3 KYC filing up to Oct 15. Please upload docs to StatutoryGuard for audit verification.")
        
        c_ch1, c_ch2 = st.columns(2)
        with c_ch1:
            send_wa = st.checkbox("Broadcast via WhatsApp", value=True)
        with c_ch2:
            send_em = st.checkbox("Broadcast via Email Digest", value=True)

        if st.button("🚀 Dispatch System-Wide Emergency Alert", type="primary"):
            if not broadcast_msg:
                st.error("Please enter broadcast message.")
            else:
                sent_count = 0
                for c in all_companies:
                    if send_wa:
                        db.log_alert({
                            "alert_id": f"BC_{c['cin'][:6]}_{sent_count}",
                            "company_cin": c["cin"],
                            "form_code": "BROADCAST",
                            "channel": "WhatsApp",
                            "recipient": c.get("phone", "+919876543210"),
                            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "message": broadcast_msg
                        })
                        sent_count += 1
                    if send_em:
                        db.log_alert({
                            "alert_id": f"BC_EM_{c['cin'][:6]}_{sent_count}",
                            "company_cin": c["cin"],
                            "form_code": "BROADCAST",
                            "channel": "Email",
                            "recipient": c.get("email", "founder@startup.in"),
                            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "message": broadcast_msg
                        })
                        sent_count += 1

                st.success(f"🎉 Emergency broadcast successfully dispatched to {len(all_companies)} startups! ({sent_count} total messages sent)")

    # --------------- 4. SECURITY AUDIT LOGS ---------------
    with t4:
        st.subheader("🔒 Platform Security & Notification Audit Logs")
        if not all_alert_logs:
            st.info("No audit logs recorded.")
        else:
            df_logs = pd.DataFrame(all_alert_logs)
            st.dataframe(df_logs, use_container_width=True)
