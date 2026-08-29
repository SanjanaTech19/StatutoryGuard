import React, { useState } from 'react';
import { Shield, User, Building2, Lock, ArrowRight, AlertTriangle } from 'lucide-react';

export default function AuthModal({ onLogin, onAdminLogin, onSignup }) {
  const [tab, setTab] = useState('login');
  
  // Login State
  const [loginInput, setLoginInput] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginError, setLoginError] = useState('');

  // Admin Login State
  const [adminUser, setAdminUser] = useState('admin');
  const [adminPass, setAdminPass] = useState('AdminStrictSecret123!');
  const [adminPin, setAdminPin] = useState('998877');
  const [adminError, setAdminError] = useState('');

  // Signup State
  const [cin, setCin] = useState('U72900KA2023PTC174821');
  const [compName, setCompName] = useState('InnovateTech Solutions Private Limited');
  const [entityType, setEntityType] = useState('Private Limited');
  const [incDate, setIncDate] = useState('2023-05-10');
  const [fullName, setFullName] = useState('Rajesh Kumar');
  const [username, setUsername] = useState('rajesh_founder');
  const [email, setEmail] = useState('rajesh@innovatetech.in');
  const [pass1, setPass1] = useState('');
  const [signupMsg, setSignupMsg] = useState('');

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoginError('');
    try {
      await onLogin(loginInput, loginPass);
    } catch (err) {
      setLoginError(err.message || 'Login failed');
    }
  };

  const handleAdminLoginSubmit = async (e) => {
    e.preventDefault();
    setAdminError('');
    try {
      await onAdminLogin(adminUser, adminPass, adminPin);
    } catch (err) {
      setAdminError(err.message || 'Strict Admin Authentication Failed');
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    setSignupMsg('');
    try {
      await onSignup({
        cin,
        company_name: compName,
        entity_type: entityType,
        incorporation_date: incDate,
        full_name: fullName,
        username,
        email,
        password: pass1
      });
      setSignupMsg('Account created successfully! Please sign in.');
      setTab('login');
    } catch (err) {
      setSignupMsg(err.message || 'Sign up failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950 relative overflow-hidden">
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-md w-full glass-card rounded-3xl p-8 space-y-6 relative z-10 border border-slate-800">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="h-14 w-14 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-xl shadow-sky-500/20 mx-auto">
            <Shield className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-gradient">
            StatutoryGuard
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            AI-Driven MCA/ROC Compliance Armour for Indian Startups
          </p>
        </div>

        {/* Tab Selector */}
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
          <button
            onClick={() => setTab('login')}
            className={`flex-1 py-2 rounded-lg transition ${
              tab === 'login' ? 'bg-sky-500 text-white shadow font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Founder Login
          </button>
          <button
            onClick={() => setTab('signup')}
            className={`flex-1 py-2 rounded-lg transition ${
              tab === 'signup' ? 'bg-sky-500 text-white shadow font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Sign-Up
          </button>
          <button
            onClick={() => setTab('admin')}
            className={`flex-1 py-2 rounded-lg transition ${
              tab === 'admin' ? 'bg-purple-600 text-white shadow font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Admin Auth
          </button>
        </div>

        {/* 1. Founder Login */}
        {tab === 'login' && (
          <form onSubmit={handleLoginSubmit} className="space-y-4">
            {signupMsg && (
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-xl text-xs">
                {signupMsg}
              </div>
            )}
            {loginError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-xl text-xs font-semibold">
                {loginError}
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Username or Work Email</label>
              <input
                type="text"
                required
                placeholder="founder@startup.in"
                value={loginInput}
                onChange={(e) => setLoginInput(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                required
                placeholder="••••••••"
                value={loginPass}
                onChange={(e) => setLoginPass(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center justify-center gap-2"
            >
              <span>Sign In as Founder</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>
        )}

        {/* 2. Sign Up */}
        {tab === 'signup' && (
          <form onSubmit={handleSignupSubmit} className="space-y-3">
            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Company CIN</label>
              <input
                type="text"
                required
                value={cin}
                onChange={(e) => setCin(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Company Name</label>
                <input
                  type="text"
                  required
                  value={compName}
                  onChange={(e) => setCompName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Entity Type</label>
                <select
                  value={entityType}
                  onChange={(e) => setEntityType(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                >
                  <option value="Private Limited">Private Limited</option>
                  <option value="One Person Company">One Person Company</option>
                  <option value="LLP">LLP</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Username</label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Work Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                required
                placeholder="••••••••"
                value={pass1}
                onChange={(e) => setPass1(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition"
            >
              Register Startup & Create Founder Account
            </button>
          </form>
        )}

        {/* 3. Strict Admin Login */}
        {tab === 'admin' && (
          <form onSubmit={handleAdminLoginSubmit} className="space-y-4">
            <div className="p-3 bg-purple-500/10 border border-purple-500/30 text-purple-300 rounded-xl text-xs flex items-center gap-2">
              <Lock className="h-4 w-4 shrink-0" />
              <span>Strict 2FA Administrative Security Portal</span>
            </div>

            {adminError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-xl text-xs font-semibold">
                {adminError}
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Admin Username</label>
              <input
                type="text"
                required
                value={adminUser}
                onChange={(e) => setAdminUser(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Admin Password</label>
              <input
                type="password"
                required
                value={adminPass}
                onChange={(e) => setAdminPass(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">2FA Security PIN</label>
              <input
                type="password"
                required
                value={adminPin}
                onChange={(e) => setAdminPin(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-purple-500/20 transition flex items-center justify-center gap-2"
            >
              <span>Authenticate as System Admin</span>
              <Lock className="h-4 w-4" />
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
