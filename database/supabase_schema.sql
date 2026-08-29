-- StatutoryGuard Supabase PostgreSQL Database Schema Initialization
-- Run this script in your Supabase SQL Editor: https://supabase.com/dashboard/project/rcjdwxiymiekxrncdbgc/sql/new

-- 1. Users Table (Founders & Administrators)
CREATE TABLE IF NOT EXISTS public.users (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'founder',
    company_cin TEXT,
    full_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Companies Table (Startup Master Data)
CREATE TABLE IF NOT EXISTS public.companies (
    cin TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    incorporation_date TEXT NOT NULL,
    authorized_capital DOUBLE PRECISION DEFAULT 1000000.0,
    paid_up_capital DOUBLE PRECISION DEFAULT 100000.0,
    roc_office TEXT,
    directors TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    mca_status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Compliance Tasks Table (Statutory Requirement Matrices)
CREATE TABLE IF NOT EXISTS public.compliance_tasks (
    task_id TEXT PRIMARY KEY,
    company_cin TEXT NOT NULL,
    form_code TEXT NOT NULL,
    title TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    risk_level TEXT DEFAULT 'HIGH',
    max_penalty DOUBLE PRECISION DEFAULT 50000.0,
    category TEXT DEFAULT 'Annual Filing',
    filed_date TEXT,
    srn_number TEXT,
    notes TEXT
);

-- 4. Document Vault Table (AES-256 Encrypted Records)
CREATE TABLE IF NOT EXISTS public.document_vault (
    doc_id TEXT PRIMARY KEY,
    company_cin TEXT NOT NULL,
    doc_name TEXT NOT NULL,
    category TEXT NOT NULL,
    upload_date TEXT NOT NULL,
    file_path TEXT NOT NULL,
    dsc_director TEXT,
    dsc_expiry TEXT,
    encrypted INT DEFAULT 1
);

-- 5. Alert Logs Table (Multi-Channel Dispatch History)
CREATE TABLE IF NOT EXISTS public.alert_logs (
    alert_id TEXT PRIMARY KEY,
    company_cin TEXT NOT NULL,
    form_code TEXT NOT NULL,
    channel TEXT NOT NULL,
    recipient TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    status TEXT DEFAULT 'SENT',
    message TEXT NOT NULL
);

-- Enable Public Table Access for REST API Synchronization
ALTER TABLE public.users DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.companies DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_tasks DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.document_vault DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.alert_logs DISABLE ROW LEVEL SECURITY;
