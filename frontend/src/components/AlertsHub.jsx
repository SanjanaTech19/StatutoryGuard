import React, { useState } from 'react';
import { Bell, Calendar, MessageSquare, Mail, Smartphone, Download, CheckCircle2 } from 'lucide-react';

export default function AlertsHub({ company, tasks, onDispatchTest }) {
  const [selectedForm, setSelectedForm] = useState(tasks[0]?.form_code || 'DIR-3 KYC');
  const [channel, setChannel] = useState('WhatsApp');
  const [dispatchStatus, setDispatchStatus] = useState(null);

  const handleTestDispatch = async (ch) => {
    try {
      const recipient = ch === 'Email' ? company.email || 'founder@startup.in' : company.phone || '+919876543210';
      const msg = `🟢 StatutoryGuard Alert: Filing for ${selectedForm} is due soon. Avoid penalty risk. Log in: https://statutoryguard.in`;
      
      const res = await onDispatchTest({
        company_cin: company.cin,
        form_code: selectedForm,
        channel: ch,
        recipient: recipient,
        message: msg
      });
      setDispatchStatus(`Success: ${res.message}`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="glass-card rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Bell className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">Automated Multi-Channel Alerts Hub</h2>
            <p className="text-xs text-slate-400 mt-1">
              Dispatches automated reminders before statutory deadlines across WhatsApp, SMS, and Email.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time Dispatch Tester */}
        <div className="glass-panel rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-sky-400" />
            Test Real-Time Alert Dispatch
          </h3>
          <p className="text-xs text-slate-400">
            Select an upcoming form and trigger an instant simulated dispatch payload.
          </p>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Select Statutory Form</label>
            <select
              value={selectedForm}
              onChange={(e) => setSelectedForm(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              {tasks.map((t) => (
                <option key={t.task_id} value={t.form_code}>
                  {t.form_code}: {t.title} (Due {t.due_date})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-3 gap-3 pt-2">
            <button
              onClick={() => handleTestDispatch('WhatsApp')}
              className="p-3 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5"
            >
              <MessageSquare className="h-5 w-5" />
              <span>WhatsApp</span>
            </button>

            <button
              onClick={() => handleTestDispatch('Email')}
              className="p-3 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5"
            >
              <Mail className="h-5 w-5" />
              <span>Email</span>
            </button>

            <button
              onClick={() => handleTestDispatch('SMS')}
              className="p-3 bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5"
            >
              <Smartphone className="h-5 w-5" />
              <span>SMS Alert</span>
            </button>
          </div>

          {dispatchStatus && (
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 font-medium flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4" /> {dispatchStatus}
            </div>
          )}
        </div>

        {/* Calendar Sync Exporter */}
        <div className="glass-panel rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Calendar className="h-5 w-5 text-indigo-400" />
            Calendar Sync Radar (.ics Export)
          </h3>
          <p className="text-xs text-slate-400">
            Export all statutory due dates directly to Google Calendar, Outlook, or Apple Calendar with automated 7-day pre-deadline alarms.
          </p>

          <a
            href={`/api/alerts/calendar.ics?cin=${company.cin}`}
            download={`${company.name}_deadlines.ics`}
            className="inline-flex items-center justify-center gap-2 w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-500/20 transition"
          >
            <Download className="h-4 w-4" />
            <span>Download .ics Calendar File</span>
          </a>
        </div>
      </div>
    </div>
  );
}
