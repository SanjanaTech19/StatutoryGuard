# 🛡️ StatutoryGuard

> **AI-Driven MCA/ROC Statutory Compliance Platform for Indian Startup Founders**  
> *Zero Penalty Risk. Zero Legal Jargon. 100% Audit-Ready.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-StatutoryGuard-emerald.svg)](https://github.com/SanjanaTech19/StatutoryGuard)
[![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20Supabase-purple.svg)](#-tech-stack)

---

## 📌 Project Overview

**StatutoryGuard** eliminates statutory regulatory overhead for early-stage Indian startup founders, saving **15–20 hours monthly** and safeguarding against **₹5 Lakh statutory penalties** and MCA company strike-off risks. Founders juggle 50+ annual and event-based compliances; StatutoryGuard automates tracking, pre-submission audit verification, plain-English legal circular translation, multi-channel alerts, and secure document vaulting.

---

## ✨ Key Features

### 1. 🔑 Founder Authentication & Startup Registration
- **Founder Login Page**: Dedicated login screen featuring **Target Startup Company Selection** (dropdown & search by CIN / Company Name).
- **Startup Sign-Up & Onboarding**: Onboard new entities by entering CIN, Entity Type (*Private Limited, One Person Company, LLP*), Incorporation Date, and Founder credentials.

### 2. 📊 Centralized Statutory Dashboard
- Custom-maps statutory requirements (*AOC-4, MGT-7, DIR-3 KYC, ADT-1, INC-20A, DPT-3, MSME-1, PAS-3, Board Meetings Q1–Q4, AGM*) based on entity type and incorporation date.
- Real-time **Compliance Health Index (%)** and **Statutory Penalty Exposure Radar (₹)** with clean floating-point precision formatting.

### 3. 🛡️ Schedule III Balance Sheet Pre-Submission Audit Engine
- **Math Verification**: Validates Schedule III math equality ($\text{Total Assets} = \text{Total Liabilities} + \text{Equity}$). Detects numerical discrepancies (e.g. ₹1,00,000 difference) and flags **`[CRITICAL] BALANCE_SHEET_MATH_MISMATCH`**.
- **Signature & DIN Verification**: Flags blank signature placeholders (*`Signature: ________`*) lacking DSC / `Sd/-` attestation and validates 8-digit Director Identification Numbers (DIN).
- **SS-1 Secretarial Standard Audit**: Validates Board Resolution notice dates, quorum statements, and *Certified True Copy* stamps.

### 4. 🤖 Plain-English AI Assistant & Legal Circular Decoder
- **Strict Zero-Invention Rule**: Never infers or invents unstated deadlines or fine amounts. Returns `"Not specified in the document"` when explicit figures are absent.
- **Letterhead & Date Stripper**: Filters out document letterheads (*`MINISTRY OF CORPORATE AFFAIRS...`*, *`Date: 30 August 2026`*) so summaries start directly with plain-English legal directives.
- **Actionable Task Breakdown**: Extracts 4 distinct numbered task cards with status badges (`Pending`, `Review`, `Filed`).
- **Comprehensive Companies Act 2013 Q&A**: Hybrid Gemini 1.5 Flash / Groq Llama 3.3 70B LLM integration with fallback to verified statutory rules for **Section 128 (Audit Trail / Edit Log)**, **Section 10A (INC-20A)**, **Section 149 (Directors)**, and **Section 73 (DPT-3)**.

### 5. 🔔 Multi-Channel Alerts Hub & Cadence Radar
- **Dual WhatsApp Dispatcher**: Features 1-click **`WhatsApp Web`** (browser link) and **`WhatsApp App`** (native protocol) dispatching.
- **Gmail Pre-Fill**: 1-click Gmail Compose URL generator.
- **4-Stage Escalation Cadence**: Automated notification radar leading up to statutory due dates (*T-30, T-15, T-7, T-1 days*).
- **Calendar Sync Radar**: RFC 5545 `.ics` calendar generator with built-in 7-day alarms (`VALARM`) and Google Calendar direct sync.

### 6. 🔒 Encrypted Document Vault & DSC Expiry Radar
- **AES-256 Cryptographic Storage**: Encrypts files using Fernet 256-bit symmetric keys with SHA-256 checksum integrity verification.
- **HTML Document Viewer Tab**: Dedicated `/api/vault/view/{doc_id}` tab displaying company CIN, upload date, SHA-256 integrity stamp, and document preview.
- **Valid Binary PDF Downloads**: Streams 100% valid binary PDF 1.4 objects (`/api/vault/download/{doc_id}`) eliminating file corruption errors.
- **Director DSC Expiry Radar**: Tracks digital signature expiration dates for active directors.

### 7. ☁️ 1-Click Production Cloud Deployment
- **Pre-Configured Blueprints**: Includes production `Dockerfile`, `Procfile`, and `render.yaml` for Render, Northflank, Railway, and AWS.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend API**: Python 3.10+, FastAPI REST Server, Uvicorn, Gunicorn
- **Database**: SQLite (`statutoryguard.db`), Cloud Supabase PostgreSQL (`rcjdwxiymiekxrncdbgc`)
- **Security & Encryption**: Cryptography (AES-256 Fernet, SHA-256, PBKDF2 Password Hashing)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/SanjanaTech19/StatutoryGuard.git
cd StatutoryGuard
```

### 2. Install Dependencies & Build Frontend
```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
```

### 3. Run the Platform
```bash
python api.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🔑 Default Test Credentials

- **Founder Login**:
  - **Company**: `InnovateTech Solutions Private Limited (U72900KA2023PTC174821)`
  - **Username / Email**: `founders@innovatetech.in`
  - **Password**: `FounderSecret123!`
