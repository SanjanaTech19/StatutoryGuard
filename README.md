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

### 1. 📊 Centralized Statutory Dashboard
- Custom-maps statutory requirements (*AOC-4, MGT-7, DIR-3 KYC, ADT-1, INC-20A, DPT-3, MSME-1, PAS-3, Board Meetings Q1–Q4, AGM*) based on entity type (*Private Limited, OPC, LLP*) and incorporation date.
- Real-time **Compliance Health Index (%)** and **Statutory Penalty Exposure Radar (₹)** with clean floating-point precision formatting.

### 2. ⚡ Founder & Administrator Power Tools
- **`+ Add Custom Form` Modal**: Create custom state/tax/internal compliance forms (*GST-3B, TDS-281, PF & ESI, ESOP PAS-3 Allotment, Rounds Valuation Renewal*).
- **VC Due Diligence Clearance Certificate**: 1-click export of an official **Statutory Compliance Clearance Certificate** with verification stamp and PDF export for investors & CAs.
- **Cap Table & ESOP Allotment PAS-3 Risk Calculator**: Interactive simulator calculating 30-day PAS-3 share allotment filing windows and daily penalty shields under Section 42 / 62.

### 3. 🛡️ Schedule III Indian Balance Sheet Pre-Submission Audit Engine
- **Indian Comma & Multi-Column Parser**: Handles Indian currency numbering (*`30,75,000`*) and multi-column financial statements (*Current Year `31-Mar-2026` vs Prior Year `31-Mar-2025`*).
- **Discrepancy Detection**: Validates `Total Assets = Total Equity & Liabilities`. Automatically detects balance sheet mismatches (e.g. ₹1,00,000 difference) and flags **`[CRITICAL] BALANCE_SHEET_MATH_MISMATCH`**.
- **Signature & DIN Verification**: Flags blank signature placeholders (*`Signature: ________`*) lacking DSC / `Sd/-` attestation and validates 8-digit Director Identification Numbers (DIN).
- **Strict Status Safeguards**: Automatically forces status to **`REJECTION RISK`** (Score < 60) whenever balance sheet math fails.

### 4. 🤖 Plain-English AI Assistant & Legal Q&A Engine
- **MCA Circular Decoder**: Translates legal circulars into structured task lists with clear status indicators (*`Pending`, `Review`, `Filed`*).
- **Comprehensive Companies Act 2013 Q&A**: Answers complex questions on **Section 128 (Audit Trail / Edit Log Rule 3(1), Section 128(5) 8-year record retention, Section 128(6) ₹50,000–₹5,00,000 fines, Section 143(3)(j) Rule 11(g) auditor reporting)** with step-by-step rectification plans.

### 5. 🔔 Automated Real-Time Alerts Hub
- Multi-channel notification dispatchers (*WhatsApp, Email, SMS*) triggered before deadlines (*T-30, T-15, T-7, T-1 days*).
- Downloadable `.ics` calendar sync files for Google, Outlook, and Apple Calendars.

### 6. 🔒 Encrypted Document Vault & DSC Expiry Radar
- AES-256 encrypted repository for Digital Signatures (DSC), Certificate of Incorporation, MOA/AOA, and Board Minutes.
- **Strict Multi-Tenant Isolation**: Enforces strict CIN isolation (`WHERE company_cin = ?`) with dynamic founder director assignment and explicit CIN ownership badges.

### 7. 🗄️ Dual Database Architecture & Cloud Supabase Integration
- **Local SQLite Persistence**: Embedded `statutoryguard.db` storing users, companies, compliance tasks, vault items, and alert logs.
- **Cloud Supabase PostgreSQL Sync**: Pre-configured for Supabase Project `rcjdwxiymiekxrncdbgc`. Includes 1-click table creation script ([supabase_schema.sql](file:///c:/Users/Rajasekar/OneDrive/Desktop/InnovatorsArena/database/supabase_schema.sql)) with permissive RLS policies.
- **Full Database Snapshot Export**: Download complete JSON database backups via `/api/admin/export-db`.

---

## 🛠️ Tech Stack

- **Frontend**: React (Vite, Tailwind CSS, Lucide Icons, Glassmorphic UI)
- **Backend API**: Python 3.11, FastAPI REST Server, Uvicorn, LangChain, PyPDF
- **Database Core**: SQLite (`statutoryguard.db`), Supabase Cloud PostgreSQL (`rcjdwxiymiekxrncdbgc`)
- **Security & Encryption**: Cryptography (AES-256 Fernet, SHA-256, PBKDF2 Password Hashing, 2FA Admin Security)

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
cd frontend && npm install && npm run build && cd ..
```

### 3. Configure Supabase Environment Variables (Optional)
Copy `.env.example` to `.env`:
```env
SUPABASE_URL=https://rcjdwxiymiekxrncdbgc.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 4. Run the Platform
```bash
python api.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🔑 Default Test Credentials

- **Founder Account (Auto Sign-In Available)**:
  - **Username**: `rajesh_founder`
  - **Password**: `FounderPass123!`
- **Administrator Control Center**:
  - **Username**: `admin`
  - **Password**: `AdminStrictSecret123!`
  - **2FA Security PIN**: `998877`

---

## 📜 License

This project is licensed under the MIT License.
