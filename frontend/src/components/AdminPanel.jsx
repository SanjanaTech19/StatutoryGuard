import React, { useState } from 'react';
import { Crown, Building2, Users, AlertOctagon, Send, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function AdminPanel({ overview, onBroadcast }) {
  if (!overview) {
    return <div className="p-8 text-center text-slate-400">Loading Administrator Portal...</div>;
  }

  const { metrics, companies, users, logs } = overview;
  const [broadcastMsg, setBroadcastMsg] = useState(
    '🚨 MCA V3 Portal Maintenance Alert: Extended timeline for DIR-3 KYC filing. Please upload docs to StatutoryGuard for audit verification.'
  );
  const [sendWA, setSendWA] = useState(true);
  const [sendEM, setSendEM] = useState(true);
  const [broadcastStatus, setBroadcastStatus] = useState(null);

  const handleBroadcastSubmit = async (e) => {
    e.preventDefault();
    if (!broadcastMsg) return;
    try {
      const res = await onBroadcast({
        message: broadcastMsg,
        send_whatsapp: sendWA,
        send_email: sendEM
      });
      setBroadcastStatus(`Broadcast dispatched to ${res.target_companies} startups (${res.total_messages_sent} messages sent)!`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="glass-card rounded-2xl p-6 relative overflow-hidden border border-purple-500/30">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <Crown className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">System Administrator Command & Control Center</h2>
            <p className="text-xs text-slate-400 mt-1">
              Restricted Administrator Portal & Global Regulatory Compliance Monitor
            </p>
          </div>
        </div>
      </div>

      {/* Global Stat Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs font-semibold text-slate-400">Total Registered Startups</p>
          <h3 className="text-2xl font-extrabold text-slate-100 mt-1">{metrics.total_startups}</h3>
        </div>

        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs font-semibold text-slate-400">Guarded Penalty Risk</p>
          <h3 className="text-2xl font-extrabold text-rose-400 mt-1">₹{metrics.total_penalty_guarded?.toLocaleString('en-IN')}</h3>
        </div>

        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs font-semibold text-slate-400">Critical Overdue Filings</p>
          <h3 className="text-2xl font-extrabold text-amber-400 mt-1">{metrics.total_overdue_filings}</h3>
        </div>

        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs font-semibold text-slate-400">Total System Users</p>
          <h3 className="text-2xl font-extrabold text-sky-400 mt-1">{metrics.total_users}</h3>
        </div>
      </div>

      {/* Companies Oversight Table */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <Building2 className="h-5 w-5 text-sky-400" />
          Multi-Startup Compliance Oversight
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">CIN</th>
                <th className="p-3">Company Name</th>
                <th className="p-3">Entity Type</th>
                <th className="p-3">ROC Office</th>
                <th className="p-3">Health</th>
                <th className="p-3">Penalty Exposure</th>
                <th className="p-3">Overdue</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {companies?.map((c) => (
                <tr key={c.cin} className="hover:bg-slate-900/50 transition">
                  <td className="p-3 font-mono font-bold text-sky-400">{c.cin}</td>
                  <td className="p-3 font-bold text-slate-200">{c.name}</td>
                  <td className="p-3 text-slate-400">{c.entity_type}</td>
                  <td className="p-3 text-slate-400">{c.roc_office}</td>
                  <td className="p-3 font-bold text-emerald-400">{c.health_score}%</td>
                  <td className="p-3 font-bold text-rose-400">₹{c.penalty_exposure?.toLocaleString('en-IN')}</td>
                  <td className="p-3 font-bold text-amber-400">{c.overdue_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Emergency Broadcast Center */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <Send className="h-5 w-5 text-purple-400" />
          System-Wide Emergency Broadcast Hub
        </h3>
        <p className="text-xs text-slate-400">
          Send critical regulatory updates, circular alerts, or portal outage notifications to ALL startup founders simultaneously.
        </p>

        <form onSubmit={handleBroadcastSubmit} className="space-y-4">
          <textarea
            rows={3}
            value={broadcastMsg}
            onChange={(e) => setBroadcastMsg(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
          />

          <div className="flex gap-4 text-xs font-semibold text-slate-300">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={sendWA}
                onChange={(e) => setSendWA(e.target.checked)}
                className="rounded bg-slate-950 border-slate-800 text-purple-500"
              />
              <span>Dispatch via WhatsApp</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={sendEM}
                onChange={(e) => setSendEM(e.target.checked)}
                className="rounded bg-slate-950 border-slate-800 text-purple-500"
              />
              <span>Dispatch via Email</span>
            </label>
          </div>

          <button
            type="submit"
            className="py-3 px-6 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-purple-500/20 transition flex items-center gap-2"
          >
            <Send className="h-4 w-4" />
            <span>Dispatch System-Wide Broadcast</span>
          </button>
        </form>

        {broadcastStatus && (
          <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-xl text-xs text-purple-300 font-semibold flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4" /> {broadcastStatus}
          </div>
        )}
      </div>
    </div>
  );
}
