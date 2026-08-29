"""
Automated Alerts & Notification Engine Module
Sends real-time deadline notifications via Email (SMTP + mailto), SMS, and WhatsApp deep-links.
Generates Google/Outlook ICS calendar sync files.
"""

import os
import uuid
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from database.db_client import DatabaseClient

def send_smtp_email(to_email: str, subject: str, body_text: str) -> bool:
    """
    Sends actual background email via SMTP if credentials are configured in environment variables.
    """
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    if not smtp_host or not smtp_user or not smtp_pass:
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {str(e)}")
        return False

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
