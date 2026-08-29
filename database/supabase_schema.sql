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

-- Enable RLS and add public permissive policies for seamless REST API sync
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.document_vault ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alert_logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public Users Access" ON public.users;
CREATE POLICY "Public Users Access" ON public.users FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public Companies Access" ON public.companies;
CREATE POLICY "Public Companies Access" ON public.companies FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public Tasks Access" ON public.compliance_tasks;
CREATE POLICY "Public Tasks Access" ON public.compliance_tasks FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public Vault Access" ON public.document_vault;
CREATE POLICY "Public Vault Access" ON public.document_vault FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public Logs Access" ON public.alert_logs;
CREATE POLICY "Public Logs Access" ON public.alert_logs FOR ALL USING (true) WITH CHECK (true);
