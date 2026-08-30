# 🛡️ StatutoryGuard

> **AI-Driven MCA/ROC Statutory Compliance Platform for Indian Startup Founders**  
> *Zero Penalty Risk. Zero Legal Jargon. 100% Audit-Ready.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-StatutoryGuard-emerald.svg)](https://github.com/SanjanaTech19/StatutoryGuard)
[![Live Vercel App](https://img.shields.io/badge/Vercel-Live--App-black.svg?logo=vercel)](https://statutory-guard.vercel.app)
[![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20Supabase-purple.svg)](#-tech-stack)

---

## 📌 Problem Statement

Running a startup in India is tough, but managing government rules under the Ministry of Corporate Affairs (MCA) makes it even harder. Early-stage startup founders are legally required to file **over 50 mandatory forms** every year—such as annual financial returns (AOC-4, MGT-7), director KYC (DIR-3), deposit reports (DPT-3), and quarterly board meeting records.

This creates 3 major problems for founders:

1. 💰 **Heavy Daily Fines**: Missing a filing deadline results in strict daily penalties (like ₹100 per day with no upper limit, flat ₹5,000 director fees, or total fines up to **₹5 Lakhs**). In severe cases, the government can block directors or strike off the company.
2. 🤯 **Confusing Legal Jargon**: Government circulars are full of complicated legal language. Early-stage startups cannot afford expensive law firms to read and explain these rules.
3. ❌ **Form Rejections**: A simple math mistake in a balance sheet or a missing signature causes the government to reject the filing, triggering extra late fees and failing investor due diligence.

Instead of building their business, founders waste **15 to 20 hours every month** manually tracking forms and deadlines, living in constant fear of expensive legal penalties.

---

## 🛡️ The Solution: How StatutoryGuard Works

**StatutoryGuard** is an AI-driven compliance assistant that acts as a digital shield for Indian startups. It automates all Ministry of Corporate Affairs (MCA) regulatory rules so founders never miss a deadline or pay a single rupee in legal penalties.

### ⚙️ 5-Step Automated Workflow

1. 📊 **Custom Compliance Timeline**: Enter your Company CIN and Incorporation Date. StatutoryGuard instantly creates a personalized timeline showing every form you must file (`AOC-4`, `MGT-7`, `DIR-3 KYC`, `DPT-3`, `Board Meetings`), along with exact due dates and potential penalty amounts.
2. 🛡️ **Pre-Submission Audit Engine**: Before you submit financial forms to the government, upload your PDF balance sheet. StatutoryGuard automatically checks if $\text{Total Assets} = \text{Total Liabilities} + \text{Equity}$, verifies 8-digit Director DIN numbers, and flags missing signatures so the government doesn't reject your form.
3. 🤖 **Plain-English AI Legal Assistant**: When the government releases confusing new legal circulars, StatutoryGuard translates them into simple 4-step task cards, telling you exactly what to do without any legal jargon.
4. 🔔 **Multi-Channel Alerts Hub**: Stay ahead of deadlines. StatutoryGuard sends automated reminders straight to your **WhatsApp** (`WhatsApp Web` & `WhatsApp App`), **Email**, and **Google Calendar** at 30 days, 15 days, and 1 day before any form is due.
5. 🔒 **Encrypted Document Vault**: Safely store all your Digital Signatures (DSC), Incorporation Certificates, and Board Minutes in a bank-grade AES-256 encrypted vault that automatically alerts you before your director's DSC expires.

---

## 🌐 Live Web Application & Cloud Deployment

- **Live Web Application (Vercel)**: **[https://statutory-guard.vercel.app](https://statutory-guard.vercel.app)** 🚀

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

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend API**: Python 3.10+, FastAPI REST Server, Uvicorn, Gunicorn
- **Database**: SQLite (`statutoryguard.db`), Cloud Supabase PostgreSQL (`rcjdwxiymiekxrncdbgc`)
- **Security & Encryption**: Cryptography (AES-256 Fernet, SHA-256, PBKDF2 Password Hashing)
- **Deployment**: Vercel Serverless (`@vercel/python`), Docker, Render, Procfile

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

### 3. Run the Local Server
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
