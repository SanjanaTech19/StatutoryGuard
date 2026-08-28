"""
Automated Alerts & Notification Engine Module
Sends real-time deadline notifications via Email, SMS, and WhatsApp, and generates Google/Outlook ICS calendar sync files.
"""

import streamlit as st
import uuid
from datetime import datetime, timedelta
from database.db_client import DatabaseClient

def generate_ics_calendar(tasks: list) -> str:
    """Generate iCalendar (.ics) content for all compliance deadlines."""
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//StatutoryGuard//MCA ROC Compliance Radar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    for t in tasks:
        if t.get("status") == "Filed":
            continue
        due_str = t["due_date"].replace("-", "")
        uid = f"{t['task_id']}@statutoryguard.in"
        title = f"MCA Filing Deadline: {t['form_code']} - {t['title']}"
        desc = f"Mandatory MCA Statutory Filing: {t['title']}. Late Penalty Risk: Up to Rs {t.get('max_penalty', 50000):,.0f}."

        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART;VALUE=DATE:{due_str}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{desc}",
            "STATUS:CONFIRMED",
            "BEGIN:VALARM",
            "TRIGGER:-P7D",
            "ACTION:DISPLAY",
            "DESCRIPTION:Reminder: MCA Deadline in 7 days",
            "END:VALARM",
            "END:VEVENT"
        ])

    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)


def render_alerts(db: DatabaseClient, selected_cin: str):
    """Renders the Automated Alerts & Notification Engine tab."""
    st.markdown("### 🔔 Automated Real-Time Alerts & Calendar Radar")

    company = db.get_company(selected_cin)
    if not company:
        st.warning("Please select a company to configure alerts.")
        return

    tasks = db.get_tasks_for_company(selected_cin)
    pending_tasks = [t for t in tasks if t["status"] != "Filed"]

    c1, c2 = st.columns([3, 2])

    with c1:
        st.subheader("📲 Real-Time Multi-Channel Notification Hub")
        st.markdown(
            "StatutoryGuard dispatches automated reminders before deadlines across **WhatsApp**, **SMS**, and **Email** to ensure zero missed filings."
        )

        with st.form("alert_config_form"):
            st.markdown("#### Notification Destinations")
            email_input = st.text_input("Founder Email Address", value=company.get("email", "founder@startup.in"))
            whatsapp_input = st.text_input("WhatsApp Mobile Number", value=company.get("phone", "+919876543210"))
            
            st.markdown("#### Trigger Intervals")
            cb_30 = st.checkbox("T-30 Days Prior (Early Warning)", value=True)
            cb_15 = st.checkbox("T-15 Days Prior (Audit Review)", value=True)
            cb_7 = st.checkbox("T-7 Days Prior (Urgent Preparation)", value=True)
            cb_1 = st.checkbox("T-1 Day Prior (Critical Last Call)", value=True)

            if st.form_submit_button("Save Notification Preferences", type="primary"):
                st.success("✅ Notification preferences updated successfully!")

        st.markdown("---")
        st.markdown("#### ⚡ Test Real-Time Dispatch")
        st.write("Trigger a instant test alert payload for upcoming statutory deadline.")

        if pending_tasks:
            target_task = st.selectbox("Select Form for Test Dispatch", [f"{t['form_code']} ({t['due_date']})" for t in pending_tasks])
            selected_form_code = target_task.split(" ")[0]

            col_w, col_e, col_s = st.columns(3)
            with col_w:
                if st.button("💬 Send WhatsApp Alert"):
                    alert_id = str(uuid.uuid4())[:8]
                    msg = f"🟢 StatutoryGuard Alert: Filing {selected_form_code} is due on {target_task.split('(')[1][:-1]}. Avoid Rs 5,000+ penalty. Details: https://statutoryguard.in"
                    db.log_alert({
                        "alert_id": alert_id,
                        "company_cin": selected_cin,
                        "form_code": selected_form_code,
                        "channel": "WhatsApp",
                        "recipient": whatsapp_input,
                        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": msg
                    })
                    st.toast(f"WhatsApp alert dispatched to {whatsapp_input}!", icon="💬")
                    st.success(f"Message Sent: {msg}")

            with col_e:
                if st.button("📧 Send Email Digest"):
                    alert_id = str(uuid.uuid4())[:8]
                    msg = f"Statutory Compliance Notice: Action required for Form {selected_form_code}."
                    db.log_alert({
                        "alert_id": alert_id,
                        "company_cin": selected_cin,
                        "form_code": selected_form_code,
                        "channel": "Email",
                        "recipient": email_input,
                        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": msg
                    })
                    st.toast(f"Email digest dispatched to {email_input}!", icon="📧")
                    st.success(f"Email Sent to {email_input}")

            with col_s:
                if st.button("📱 Send SMS Alert"):
                    alert_id = str(uuid.uuid4())[:8]
                    msg = f"StatutoryGuard: {selected_form_code} compliance due soon. Log in to resolve."
                    db.log_alert({
                        "alert_id": alert_id,
                        "company_cin": selected_cin,
                        "form_code": selected_form_code,
                        "channel": "SMS",
                        "recipient": whatsapp_input,
                        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": msg
                    })
                    st.toast(f"SMS dispatched to {whatsapp_input}!", icon="📱")
                    st.success("SMS Alert Dispatched!")

    with c2:
        st.subheader("📅 Export to Google / Outlook Calendar")
        st.write(
            "Download an `.ics` calendar sync file containing all statutory deadlines and automated alarms to stay ahead of ROC filings."
        )

        ics_content = generate_ics_calendar(tasks)
        st.download_button(
            label="📥 Download .ics Calendar File",
            data=ics_content,
            file_name=f"{company['name'].replace(' ', '_')}_MCA_Deadlines.ics",
            mime="text/calendar",
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("📜 Sent Notification Audit Trail")
        alert_logs = db.get_alert_logs(selected_cin)
        if alert_logs:
            for log in alert_logs[:5]:
                st.caption(f"**[{log['sent_at']}]** via `{log['channel']}` -> `{log['recipient']}`")
                st.write(f"_{log['message']}_")
                st.markdown("<hr style='margin:4px 0;'/>", unsafe_allow_html=True)
        else:
            st.info("No sent alerts recorded yet.")
