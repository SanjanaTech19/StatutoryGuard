"""
Centralized Statutory Dashboard Module for StatutoryGuard
Custom-maps statutory obligations based on entity type and incorporation date.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.db_client import DatabaseClient
from utils.compliance_calculator import calculate_statutory_tasks, compute_compliance_metrics
from modules.mca_scraper import MCAScraper

def render_dashboard(db: DatabaseClient, selected_cin: str):
    """Renders the main Centralized Compliance Dashboard."""
    st.markdown("### 📊 Centralized Statutory Compliance Dashboard")

    # Fetch company profile
    company = db.get_company(selected_cin)
    if not company:
        st.warning("⚠️ No company selected or found. Please register or select a startup.")
        return

    # Compute or retrieve statutory compliance tasks
    tasks = db.get_tasks_for_company(selected_cin)
    if not tasks:
        tasks = calculate_statutory_tasks(company)
        db.save_tasks(tasks)

    # Re-calculate metrics
    health_score, penalty_exposure, pending_cnt, filed_cnt, overdue_cnt = compute_compliance_metrics(tasks)

    # Top Metric Highlights
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            label="Compliance Health",
            value=f"{health_score}%",
            delta=f"{'Healthy' if health_score >= 80 else 'Attention Required'}"
        )

    with col2:
        st.metric(
            label="Statutory Penalty Exposure",
            value=f"₹{penalty_exposure:,.0f}",
            delta=f"{'- ₹5L Max Guard' if penalty_exposure > 0 else 'Zero Risk'}",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="Pending Filings",
            value=pending_cnt,
            delta=f"{overdue_cnt} Overdue" if overdue_cnt > 0 else "On Track"
        )

    with col4:
        st.metric(
            label="Filed & Verified",
            value=filed_cnt,
            delta="Audit Ready"
        )

    with col5:
        st.metric(
            label="Hours Saved/Month",
            value="18.5 hrs",
            delta="+85% Efficiency"
        )

    st.markdown("---")

    # Active Company Overview Banner
    with st.expander("🏢 Active Company Details & Master Data", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Company Name:** {company['name']}")
            st.markdown(f"**CIN:** `{company['cin']}`")
            st.markdown(f"**Entity Type:** {company['entity_type']}")
        with c2:
            st.markdown(f"**Incorporation Date:** {company['incorporation_date']}")
            st.markdown(f"**ROC Office:** {company['roc_office']}")
            st.markdown(f"**MCA Status:** `{company['mca_status']}`")
        with c3:
            st.markdown(f"**Auth Capital:** ₹{company.get('authorized_capital', 0):,.0f}")
            st.markdown(f"**Paid Capital:** ₹{company.get('paid_up_capital', 0):,.0f}")
            st.markdown(f"**Email:** {company.get('email', '')}")

    st.markdown("### 📋 Statutory Requirements Matrix")

    # Filters
    f_col1, f_col2, f_col3 = st.columns([2, 2, 3])
    with f_col1:
        status_filter = st.selectbox("Filter Status", ["All", "Pending Only", "Filed Only", "Overdue Only"])
    with f_col2:
        category_filter = st.selectbox("Filter Category", ["All Categories", "Annual Filing", "Director Compliance", "Governance", "Financial Returns", "Incorporation"])
    with f_col3:
        search_query = st.text_input("🔍 Search Form / Title", "")

    # Filter tasks array
    filtered_tasks = tasks.copy()
    if status_filter == "Pending Only":
        filtered_tasks = [t for t in filtered_tasks if t["status"] != "Filed"]
    elif status_filter == "Filed Only":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "Filed"]
    elif status_filter == "Overdue Only":
        filtered_tasks = [t for t in filtered_tasks if t["status"] != "Filed" and t.get("days_left", 0) < 0]

    if category_filter != "All Categories":
        filtered_tasks = [t for t in filtered_tasks if t.get("category") == category_filter]

    if search_query:
        filtered_tasks = [t for t in filtered_tasks if search_query.lower() in t["form_code"].lower() or search_query.lower() in t["title"].lower()]

    if not filtered_tasks:
        st.info("No compliance tasks found matching criteria.")
        return

    # Render Task Cards / Table
    for task in filtered_tasks:
        due_dt = task["due_date"]
        days_left = task.get("days_left", 0)
        status = task["status"]
        risk = task.get("risk_level", "HIGH")
        max_pen = task.get("max_penalty", 50000.0)

        # Risk badge color
        if status == "Filed":
            badge_html = '<span class="badge-completed">FILED</span>'
        elif days_left < 0:
            badge_html = f'<span class="badge-critical">OVERDUE ({abs(days_left)} days ago)</span>'
        elif days_left <= 15:
            badge_html = f'<span class="badge-high">DUE IN {days_left} DAYS</span>'
        else:
            badge_html = f'<span class="badge-medium">DUE {due_dt}</span>'

        with st.container():
            c_left, c_mid, c_right = st.columns([5, 3, 2])
            with c_left:
                st.markdown(f"#### `{task['form_code']}`: {task['title']} {badge_html}", unsafe_allow_html=True)
                st.caption(f"**Category:** {task.get('category', 'General')} | **Risk Penalty:** Up to ₹{max_pen:,.0f}")
                st.write(task.get("description", ""))

            with c_mid:
                st.markdown(f"**Due Date:** {due_dt}")
                st.markdown(f"**Status:** `{status}`")
                if task.get("srn_number"):
                    st.caption(f"SRN: `{task['srn_number']}`")

            with c_right:
                if status != "Filed":
                    with st.popover("Mark as Filed"):
                        srn_in = st.text_input("Enter MCA SRN Number", key=f"srn_{task['task_id']}")
                        filed_dt_in = st.date_input("Filing Date", key=f"fdt_{task['task_id']}")
                        if st.button("Confirm Filing", key=f"btn_{task['task_id']}", type="primary"):
                            if srn_in:
                                db.update_task_status(task["task_id"], "Filed", srn=srn_in, filed_date=str(filed_dt_in))
                                st.success("Task marked as Filed!")
                                st.rerun()
                            else:
                                st.error("Please enter SRN number.")
                else:
                    st.success("✅ Verified")

            st.markdown("---")
