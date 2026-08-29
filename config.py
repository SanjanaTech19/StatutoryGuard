"""
StatutoryGuard Configuration & Statutory Compliance Master Database
Contains statutory rules, form metadata, deadline rules, and penalty calculation constants for Indian MCA/ROC compliance.
Includes automatic .env file loader for Supabase credentials.
"""

import os

# Automatically load .env file into os.environ if present
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file_path):
    with open(env_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

# App Information
APP_NAME = "StatutoryGuard"
APP_TAGLINE = "Zero Penalty Risk. Zero Legal Jargon. 100% Audit-Ready."
APP_VERSION = "2.0.0"

# Database & Supabase settings
DB_FILE = os.path.join(os.path.dirname(__file__), "database", "statutoryguard.db")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Secret key for Vault AES Encryption
VAULT_SECRET_KEY = os.getenv("VAULT_SECRET_KEY", "StatutoryGuardSecretKey32BytesLong!!")

# Statutory Compliances Catalog for Indian Entities
STATUTORY_FORMS_CATALOG = {
    "INC-20A": {
        "title": "Declaration of Commencement of Business",
        "description": "Mandatory filing within 180 days of incorporation prior to commencing business or exercising borrowing powers.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "incorporation",
        "days_due_after_trigger": 180,
        "fixed_due_date": None,
        "max_penalty_inr": 100000,
        "daily_penalty_inr": 1000,
        "risk_level": "CRITICAL",
        "form_category": "Incorporation",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Bank Statement showing Share Capital Deposit", "Certificate of Incorporation"]
    },
    "DIR-3 KYC": {
        "title": "Director Identification Number (DIN) KYC",
        "description": "Annual KYC verification for every individual holding an active DIN as of 31st March.",
        "applicable_entities": ["Private Limited", "One Person Company", "LLP", "Public Limited"],
        "trigger": "annual_fixed",
        "fixed_due_date": "09-30", # Sept 30 every year
        "max_penalty_inr": 5000, # Per Director DIN deactivation fee
        "daily_penalty_inr": 0,
        "risk_level": "HIGH",
        "form_category": "Director Compliance",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["PAN Card", "Aadhaar Card", "Mobile OTP", "Email OTP", "Digital Signature (DSC)"]
    },
    "ADT-1": {
        "title": "Appointment of Statutory Auditor",
        "description": "Filing to intimate ROC regarding the appointment/re-appointment of statutory auditor within 15 days of AGM.",
        "applicable_entities": ["Private Limited", "One Person Company", "Public Limited"],
        "trigger": "agm_relative",
        "days_due_after_trigger": 15,
        "fixed_due_date": "10-14", # Assuming AGM by Sept 29
        "max_penalty_inr": 50000,
        "daily_penalty_inr": 100,
        "risk_level": "HIGH",
        "form_category": "Audit & Financials",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["ADT-1 Form", "Auditor Consent Letter", "Board Resolution", "Intimation Letter to Auditor"]
    },
    "AOC-4": {
        "title": "Filing of Financial Statements & Balance Sheet",
        "description": "Filing audited financial statements, Director's Report, and Auditor's Report with ROC within 30 days of AGM.",
        "applicable_entities": ["Private Limited", "One Person Company", "Public Limited"],
        "trigger": "agm_relative",
        "days_due_after_trigger": 30,
        "fixed_due_date": "10-30", # Default Oct 30 (for AGM by Sept 30)
        "max_penalty_inr": 500000, # Can go up to ₹5 Lakhs + ₹100/day
        "daily_penalty_inr": 100,
        "risk_level": "CRITICAL",
        "form_category": "Annual Filing",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Audited Balance Sheet", "Profit & Loss Account", "Director's Report", "Auditor's Report", "Notice of AGM"]
    },
    "MGT-7 / MGT-7A": {
        "title": "Annual Return of Company",
        "description": "Filing company annual return containing details of shareholders, directors, and capital structure within 60 days of AGM.",
        "applicable_entities": ["Private Limited", "One Person Company", "Public Limited"],
        "trigger": "agm_relative",
        "days_due_after_trigger": 60,
        "fixed_due_date": "11-29", # Default Nov 29 (for AGM by Sept 30)
        "max_penalty_inr": 500000,
        "daily_penalty_inr": 100,
        "risk_level": "CRITICAL",
        "form_category": "Annual Filing",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["List of Shareholders", "List of Transfers", "Extract of Annual Return", "PCS Certification (if applicable)"]
    },
    "DPT-3": {
        "title": "Return of Deposits / Outstanding Loans",
        "description": "Annual return disclosing all deposits or transactions not considered as deposit received by the company as on March 31.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "annual_fixed",
        "fixed_due_date": "06-30", # June 30
        "max_penalty_inr": 1000000,
        "daily_penalty_inr": 500,
        "risk_level": "CRITICAL",
        "form_category": "Financial Returns",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Auditor Certificate", "List of Outstanding Debts/Loans", "Bank Statements"]
    },
    "MSME-1": {
        "title": "Half-Yearly Return of Payments to MSME Vendors",
        "description": "Filing details of outstanding payments to Micro & Small Enterprises exceeding 45 days.",
        "applicable_entities": ["Private Limited", "Public Limited", "LLP"],
        "trigger": "bi_annual",
        "fixed_due_date": ["04-30", "10-31"], # Apr 30 & Oct 31
        "max_penalty_inr": 300000,
        "daily_penalty_inr": 1000,
        "risk_level": "MEDIUM",
        "form_category": "Vendor Compliance",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["MSME Vendor Invoices", "Payment Delay Reasons", "PAN/Udyam Registration of Suppliers"]
    },
    "PAS-3": {
        "title": "Return of Allotment of Shares",
        "description": "Filing return of allotment within 30 days of equity/preference share or convertible instrument allotment.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "event_based",
        "days_due_after_trigger": 30,
        "fixed_due_date": None,
        "max_penalty_inr": 100000,
        "daily_penalty_inr": 1000,
        "risk_level": "HIGH",
        "form_category": "Event Based",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Board Resolution for Allotment", "PAS-4 Valuation Report", "List of Allottees"]
    },
    "LLP Form 11": {
        "title": "LLP Annual Return",
        "description": "Filing annual return for Limited Liability Partnership within 60 days of financial year close.",
        "applicable_entities": ["LLP"],
        "trigger": "annual_fixed",
        "fixed_due_date": "05-30", # May 30
        "max_penalty_inr": 100000,
        "daily_penalty_inr": 100,
        "risk_level": "CRITICAL",
        "form_category": "LLP Compliance",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Details of Partners", "Contribution Summary"]
    },
    "LLP Form 8": {
        "title": "LLP Statement of Account & Solvency",
        "description": "Filing statement of accounts, assets, liabilities & solvency for LLP within 30 days from 6 months of FY end.",
        "applicable_entities": ["LLP"],
        "trigger": "annual_fixed",
        "fixed_due_date": "10-30", # Oct 30
        "max_penalty_inr": 100000,
        "daily_penalty_inr": 100,
        "risk_level": "CRITICAL",
        "form_category": "LLP Compliance",
        "mca_portal_link": "https://www.mca.gov.in/mcafoportal/login.do",
        "key_documents": ["Balance Sheet of LLP", "Statement of Income & Expenditure", "Partner Solvency Declaration"]
    },
    "BOARD_MEETING_Q1": {
        "title": "Q1 Board Meeting (Apr - Jun)",
        "description": "Hold first board meeting of FY. Gap between two consecutive board meetings must not exceed 120 days.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "quarterly",
        "fixed_due_date": "06-30",
        "max_penalty_inr": 25000,
        "daily_penalty_inr": 500,
        "risk_level": "MEDIUM",
        "form_category": "Governance",
        "mca_portal_link": "",
        "key_documents": ["Notice SS-1", "Agenda", "Board Minutes Draft", "Attendance Register"]
    },
    "BOARD_MEETING_Q2": {
        "title": "Q2 Board Meeting (Jul - Sep)",
        "description": "Hold second board meeting of FY to approve financial results & AGM notice.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "quarterly",
        "fixed_due_date": "09-30",
        "max_penalty_inr": 25000,
        "daily_penalty_inr": 500,
        "risk_level": "MEDIUM",
        "form_category": "Governance",
        "mca_portal_link": "",
        "key_documents": ["Notice SS-1", "Financial Statements Draft", "AGM Notice Approval"]
    },
    "BOARD_MEETING_Q3": {
        "title": "Q3 Board Meeting (Oct - Dec)",
        "description": "Hold third board meeting of FY.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "quarterly",
        "fixed_due_date": "12-31",
        "max_penalty_inr": 25000,
        "daily_penalty_inr": 500,
        "risk_level": "MEDIUM",
        "form_category": "Governance",
        "mca_portal_link": "",
        "key_documents": ["Notice SS-1", "Agenda", "Board Minutes Draft"]
    },
    "BOARD_MEETING_Q4": {
        "title": "Q4 Board Meeting (Jan - Mar)",
        "description": "Hold fourth board meeting of FY.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "quarterly",
        "fixed_due_date": "03-31",
        "max_penalty_inr": 25000,
        "daily_penalty_inr": 500,
        "risk_level": "MEDIUM",
        "form_category": "Governance",
        "mca_portal_link": "",
        "key_documents": ["Notice SS-1", "Agenda", "Board Minutes Draft"]
    },
    "AGM": {
        "title": "Annual General Meeting (AGM)",
        "description": "Hold Annual General Meeting of shareholders within 6 months from close of financial year.",
        "applicable_entities": ["Private Limited", "Public Limited"],
        "trigger": "annual_fixed",
        "fixed_due_date": "09-30",
        "max_penalty_inr": 100000,
        "daily_penalty_inr": 5000,
        "risk_level": "CRITICAL",
        "form_category": "Governance",
        "mca_portal_link": "",
        "key_documents": ["AGM Notice (21 clear days)", "Audited Financials", "Proxy Forms", "AGM Minutes"]
    }
}

# Legal Circular Templates for AI Plain-English Translation Engine
SAMPLE_MCA_CIRCULARS = [
    {
        "id": "CIRCULAR-2024-01",
        "title": "General Circular No. 04/2024: Relaxation of additional fees and extension of last date of filing of Form DIR-3 KYC and web service DIR-3 KYC WEB",
        "date": "2024-09-20",
        "source": "Ministry of Corporate Affairs, Govt of India",
        "raw_text": """
        F. No. 01/22/2024-CL-V
        Government of India
        Ministry of Corporate Affairs
        
        Subject: Extension of timeline for filing DIR-3 KYC and DIR-3 KYC WEB without additional fees for FY 2023-24.
        
        1. In continuation of earlier circulars and keeping in view requests received from stakeholders regarding difficulty faced in OTP validation and digital signature attachment during peak MCA21 V3 portal migration, it has been decided by the Competent Authority to extend the due date.
        2. Directors holding valid DIN as on 31st March 2024 may now complete DIR-3 KYC / DIR-3 KYC WEB up to 15th October 2024 without payment of additional fee of Rs 5,000.
        3. Post 15th October 2024, the portal will automatically flag non-compliant DINs as 'Deactivated due to non-filing of DIR-3 KYC' and standard penalty under Rule 12A of Companies (Appointment and Qualification of Directors) Rules, 2014 will apply.
        4. All companies are advised to ensure immediate compliance for all listed directors on their board.
        """
    },
    {
        "id": "CIRCULAR-2024-02",
        "title": "MCA Circular on Mandatory Maintenance and Inspection of Accounts in Electronic Form with Audit Trail (Edit Log)",
        "date": "2024-04-01",
        "source": "Ministry of Corporate Affairs, Govt of India",
        "raw_text": """
        Proviso to Rule 3(1) of Companies (Accounts) Rules, 2014 states that for financial year commencing on or after April 1, 2023, every company which uses accounting software for maintaining its books of account, shall use only such accounting software which has a feature of recording audit trail of each and every transaction, creating an edit log of each change made in books of account along with the date when such changes were made and ensuring that the audit trail cannot be disabled.
        
        Statutory Auditors are mandated under Section 143(3)(j) to report explicitly in AOC-4 whether accounting software had audit trail enabled throughout the year, edit log facility was operated seamlessly, and audit trail has been preserved as per statutory record retention guidelines (8 years). Failure to comply attracts penalty under Section 128(6) of Companies Act, 2013 ranging between Rs. 50,000 to Rs. 500,000 per officer in default.
        """
    },
    {
        "id": "CIRCULAR-2024-03",
        "title": "Clarification on Commencement of Business Form INC-20A under Section 10A of Companies Act 2013",
        "date": "2024-02-15",
        "source": "Registrar of Companies (ROC), New Delhi",
        "raw_text": """
        Notice is hereby drawn to Section 10A of Companies Act 2013. A company incorporated after 2nd November 2018 having capital share shall not commence any business or exercise any borrowing powers unless a declaration is filed by a director within a period of 180 days of the date of incorporation of the company in Form INC-20A with the Registrar that every subscriber to the memorandum has paid the value of the shares agreed to be taken by him on the date of making of such declaration.
        
        If no declaration has been filed with the Registrar within 180 days and the Registrar has reasonable cause to believe that the company is not carrying on any business, the Registrar may initiate physical verification of registered office and proceedings for striking off the name of the company from the Register of Companies under Chapter XVIII. Penalty for default: Company Rs 50,000; Every officer in default Rs 1,000 per day during which default continues up to Rs 1,00,000.
        """
    }
]
