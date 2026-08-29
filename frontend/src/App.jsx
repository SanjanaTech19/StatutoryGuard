import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import AuditValidator from './components/AuditValidator';
import LegalAssistant from './components/LegalAssistant';
import AlertsHub from './components/AlertsHub';
import DocumentVault from './components/DocumentVault';
import AdminPanel from './components/AdminPanel';
import AuthModal from './components/AuthModal';
import { 
  BarChart3, ShieldCheck, Bot, Bell, Lock, Crown 
} from 'lucide-react';

export default function App() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [companies, setCompanies] = useState([]);
  const [selectedCin, setSelectedCin] = useState('');
  
  // Feature states
  const [dashboardData, setDashboardData] = useState(null);
  const [assistantPresets, setAssistantPresets] = useState([]);
  const [vaultData, setVaultData] = useState(null);
  const [adminOverview, setAdminOverview] = useState(null);

  // Fetch Companies List
  const fetchCompanies = async () => {
    try {
      const res = await fetch('/api/companies');
      const data = await res.json();
      setCompanies(data.companies || []);
      if (!selectedCin && data.companies?.length > 0) {
        setSelectedCin(data.companies[0].cin);
      }
    } catch (err) {
      console.error('Failed to fetch companies:', err);
    }
  };

  // Fetch Dashboard Data for active CIN
  const fetchDashboard = async (cin) => {
    if (!cin) return;
    try {
      const res = await fetch(`/api/dashboard/${cin}`);
      const data = await res.json();
      setDashboardData(data);
    } catch (err) {
      console.error('Failed to fetch dashboard:', err);
    }
  };

  // Fetch Assistant Presets
  const fetchPresets = async () => {
    try {
      const res = await fetch('/api/assistant/presets');
      const data = await res.json();
      setAssistantPresets(data.presets || []);
    } catch (err) {
      console.error('Failed to fetch presets:', err);
    }
  };

  // Fetch Vault Data
  const fetchVault = async (cin) => {
    if (!cin) return;
    try {
      const res = await fetch(`/api/vault/${cin}`);
      const data = await res.json();
      setVaultData(data);
    } catch (err) {
      console.error('Failed to fetch vault:', err);
    }
  };

  // Fetch Admin Overview
  const fetchAdminOverview = async () => {
    try {
      const res = await fetch('/api/admin/overview');
      const data = await res.json();
      setAdminOverview(data);
    } catch (err) {
      console.error('Failed to fetch admin overview:', err);
    }
  };

  useEffect(() => {
    if (user) {
      fetchCompanies();
      fetchPresets();
    }
  }, [user]);

  useEffect(() => {
    if (selectedCin && user) {
      fetchDashboard(selectedCin);
      fetchVault(selectedCin);
    }
  }, [selectedCin, user]);

  useEffect(() => {
    if (user && user.role === 'admin') {
      fetchAdminOverview();
    }
  }, [user, activeTab]);

  // Auth Action Handlers
  const handleLogin = async (username_or_email, password) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username_or_email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    setUser(data.user);
    if (data.user.company_cin) setSelectedCin(data.user.company_cin);
  };

  const handleAdminLogin = async (admin_username, admin_password, security_pin) => {
    const res = await fetch('/api/auth/admin-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ admin_username, admin_password, security_pin })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Admin login failed');
    setUser(data.user);
    setActiveTab('admin');
  };

  const handleSignup = async (payload) => {
    const res = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Signup failed');
  };

  const handleLogout = () => {
    setUser(null);
    setSelectedCin('');
    setDashboardData(null);
  };

  const handleOnboard = async (cin) => {
    try {
      const res = await fetch('/api/company/onboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cin })
      });
      const data = await res.json();
      await fetchCompanies();
      setSelectedCin(data.company.cin);
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkFiled = async (task_id, srn_number, filed_date) => {
    try {
      await fetch('/api/tasks/mark-filed', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task_id, srn_number, filed_date })
      });
      fetchDashboard(selectedCin);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAuditScan = async (formData) => {
    const res = await fetch('/api/validator/scan', {
      method: 'POST',
      body: formData
    });
    return await res.json();
  };

  const handleTranslate = async (raw_text) => {
    const res = await fetch('/api/assistant/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text })
    });
    return await res.json();
  };

  const handleQuery = async (question) => {
    const res = await fetch('/api/assistant/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    return await res.json();
  };

  const handleDispatchTest = async (payload) => {
    const res = await fetch('/api/alerts/dispatch-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  };

  const handleVaultUpload = async (formData) => {
    await fetch('/api/vault/upload', {
      method: 'POST',
      body: formData
    });
    fetchVault(selectedCin);
  };

  const handleBroadcast = async (payload) => {
    const res = await fetch('/api/admin/broadcast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    fetchAdminOverview();
    return data;
  };

  // If not authenticated, render AuthModal
  if (!user) {
    return (
      <AuthModal
        onLogin={handleLogin}
        onAdminLogin={handleAdminLogin}
        onSignup={handleSignup}
      />
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Sticky Header Navbar */}
      <Navbar
        user={user}
        companies={companies}
        selectedCin={selectedCin}
        setSelectedCin={setSelectedCin}
        onLogout={handleLogout}
        onOnboard={handleOnboard}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">
        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 gap-2 md:gap-4 overflow-x-auto pb-1">
          {user.role === 'admin' && (
            <button
              onClick={() => setActiveTab('admin')}
              className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                activeTab === 'admin'
                  ? 'bg-purple-600/20 text-purple-300 border border-purple-500/40 shadow-lg shadow-purple-500/10'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Crown className="h-4 w-4" />
              <span>👑 Admin Control Center</span>
            </button>
          )}

          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
              activeTab === 'dashboard'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-lg shadow-sky-500/10'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BarChart3 className="h-4 w-4" />
            <span>📊 Centralized Dashboard</span>
          </button>

          <button
            onClick={() => setActiveTab('validator')}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
              activeTab === 'validator'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-lg shadow-sky-500/10'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <ShieldCheck className="h-4 w-4" />
            <span>🛡️ Pre-Submission Audit Engine</span>
          </button>

          <button
            onClick={() => setActiveTab('assistant')}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
              activeTab === 'assistant'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-lg shadow-sky-500/10'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Bot className="h-4 w-4" />
            <span>🤖 Plain-English AI Assistant</span>
          </button>

          <button
            onClick={() => setActiveTab('alerts')}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
              activeTab === 'alerts'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-lg shadow-sky-500/10'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Bell className="h-4 w-4" />
            <span>🔔 Automated Alerts Hub</span>
          </button>

          <button
            onClick={() => setActiveTab('vault')}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-bold transition whitespace-nowrap ${
              activeTab === 'vault'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-lg shadow-sky-500/10'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Lock className="h-4 w-4" />
            <span>🔒 Encrypted Document Vault</span>
          </button>
        </div>

        {/* Tab Content Display */}
        {activeTab === 'admin' && user.role === 'admin' && (
          <AdminPanel overview={adminOverview} onBroadcast={handleBroadcast} />
        )}

        {activeTab === 'dashboard' && (
          <Dashboard data={dashboardData} onMarkFiled={handleMarkFiled} />
        )}

        {activeTab === 'validator' && (
          <AuditValidator onScan={handleAuditScan} />
        )}

        {activeTab === 'assistant' && (
          <LegalAssistant
            presets={assistantPresets}
            onTranslate={handleTranslate}
            onQuery={handleQuery}
          />
        )}

        {activeTab === 'alerts' && dashboardData && (
          <AlertsHub
            company={dashboardData.company}
            tasks={dashboardData.tasks}
            onDispatchTest={handleDispatchTest}
          />
        )}

        {activeTab === 'vault' && selectedCin && (
          <DocumentVault
            cin={selectedCin}
            data={vaultData}
            onUpload={handleVaultUpload}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500">
        StatutoryGuard v2.0.0 &bull; Powered by Python, FastAPI, LangChain & React
      </footer>
    </div>
  );
}
