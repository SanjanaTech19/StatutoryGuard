import React, { useState } from 'react';
import { Shield, Building2, Plus, LogOut, User, Lock } from 'lucide-react';

export default function Navbar({ user, companies, selectedCin, setSelectedCin, onLogout, onOnboard }) {
  const [showOnboardModal, setShowOnboardModal] = useState(false);
  const [cinInput, setCinInput] = useState('U72900KA2023PTC174821');

  const handleOnboardSubmit = (e) => {
    e.preventDefault();
    if (cinInput) {
      onOnboard(cinInput);
      setShowOnboardModal(false);
    }
  };

  const displayName = user?.full_name || user?.username || 'Founder';

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800 px-6 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Shield className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-gradient">
              StatutoryGuard
            </h1>
            <p className="text-xs text-slate-400 font-medium">
              Zero Penalty Risk &bull; 100% Audit-Ready
            </p>
          </div>
        </div>

        {/* Controls & Active Company */}
        <div className="flex items-center gap-3 w-full md:w-auto overflow-x-auto">
          {/* Active Company Selector */}
          <div className="flex items-center gap-2 bg-slate-900/80 border border-slate-800 rounded-xl px-3 py-1.5 text-sm">
            <Building2 className="h-4 w-4 text-sky-400 shrink-0" />
            <select
              value={selectedCin}
              onChange={(e) => setSelectedCin(e.target.value)}
              className="bg-transparent text-slate-200 font-semibold focus:outline-none cursor-pointer pr-2"
            >
              {companies.map((c) => (
                <option key={c.cin} value={c.cin} className="bg-slate-900 text-slate-100">
                  {c.name} ({c.entity_type})
                </option>
              ))}
            </select>
          </div>

          {/* Onboard Startup Button */}
          <button
            onClick={() => setShowOnboardModal(true)}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-2 rounded-xl transition border border-slate-700"
          >
            <Plus className="h-4 w-4 text-sky-400" />
            <span>Add Startup</span>
          </button>

          {/* User Badge */}
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
            <div className="h-6 w-6 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/40">
              {user.role === 'admin' ? (
                <Lock className="h-3.5 w-3.5 text-indigo-400" />
              ) : (
                <User className="h-3.5 w-3.5 text-sky-400" />
              )}
            </div>
            <div className="text-xs">
              <span className="font-bold text-slate-200 block">{displayName}</span>
              <span className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.2 rounded ${
                user.role === 'admin' ? 'bg-purple-500/20 text-purple-300' : 'bg-sky-500/20 text-sky-300'
              }`}>
                {user.role} ({user.username})
              </span>
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={onLogout}
            title="Logout"
            className="p-2 rounded-xl bg-slate-900 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 border border-slate-800 transition"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Onboard Startup Modal */}
      {showOnboardModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-2">
              <Building2 className="h-5 w-5 text-sky-400" />
              Onboard New Startup via MCA CIN
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Enter official 21-digit CIN number to fetch Master Data & generate compliance matrix.
            </p>
            <form onSubmit={handleOnboardSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">CIN Number</label>
                <input
                  type="text"
                  value={cinInput}
                  onChange={(e) => setCinInput(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-sky-500 focus:outline-none"
                  placeholder="U72900KA2023PTC174821"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowOnboardModal(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-400 hover:text-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-sky-500/20"
                >
                  Fetch & Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </header>
  );
}
