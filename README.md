# 🛡️ StatutoryGuard

> **AI-Driven Automated MCA/ROC Compliance Platform for Indian Startup Founders**  
> *Zero Penalty Risk. Zero Legal Jargon. 100% Audit-Ready.*

---

## 📌 Project Overview

**StatutoryGuard** eliminates regulatory compliance overhead for early-stage Indian startup founders, saving **15–20 hours monthly** and safeguarding against **₹5 Lakh statutory penalties** and MCA company strike-off risks. Founders juggle 50+ annual and event-based compliances; StatutoryGuard automates tracking, audit verification, plain-English legal circular translation, multi-channel alerts, and secure document vaulting.

---

## ✨ Key Features

1. **📊 Centralized Statutory Dashboard**
   - Custom-maps statutory requirements (AOC-4, MGT-7, DIR-3 KYC, ADT-1, INC-20A, DPT-3, MSME-1, Board Meetings) based on entity type (*Private Limited, OPC, LLP*) and incorporation date.
   - Real-time **Compliance Health Index (%)** and **Statutory Penalty Exposure Radar (₹)**.

2. **🛡️ Audit-Ready Pre-Submission Engine (Validator)**
   - Pre-submission rules engine verifying balance sheet math equality (`Assets = Liabilities + Equity`).
   - Checks DIN formats, active director status, Secretarial Standard SS-1 notice periods, and missing director signature placeholders.

3. **🤖 Plain-English AI Assistant**
   - Translates dense MCA legal circulars into step-by-step task lists with clear status indicators (`Pending`, `Review`, `Filed`).
   - Interactive compliance Q&A bot trained on Companies Act 2013 regulations.

4. **🔔 Automated Real-Time Alerts Hub**
   - Multi-channel notification dispatchers (WhatsApp, Email, SMS) triggered before deadlines (T-30, T-15, T-7, T-1 days).
   - Generates downloadable `.ics` calendar sync files for Google / Outlook / Apple Calendars.

5. **🔒 Secure Encrypted Document Vault & DSC Tracker**
   - AES-256 encrypted repository for Digital Signatures (DSC), Certificate of Incorporation, MOA/AOA, and Board Minutes.
   - Director DSC expiration countdown radar.

6. **🔑 Multi-Role Authentication & Strict Admin Control Center**
   - **Founder Login & 1-Step Startup Sign-Up**: Company registration with MCA CIN lookup.
   - **Strict Administrator Portal**: Requires 2FA Security PIN (`998877`), featuring multi-startup compliance oversight, system-wide emergency broadcast dispatching, and security audit logs.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Custom Responsive Tailwind-inspired CSS
- **Backend & AI Core**: Python 3.11, LangChain, Hugging Face Transformers, PyPDF
- **Database & Security**: SQLite with Supabase PostgreSQL client integration, Cryptography (AES-256 Fernet, SHA-256, PBKDF2 Password Hashing)
- **Data Scraping & Integration**: MCA Master Data CIN Scraper & iCalendar ICS Generator

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/SanjanaTech19/StatutoryGuard.git
cd StatutoryGuard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## 🔑 Default Credentials for Testing

- **Administrator Portal**:
  - **Username**: `admin`
  - **Password**: `AdminStrictSecret123!`
  - **2FA Security PIN**: `998877`

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
