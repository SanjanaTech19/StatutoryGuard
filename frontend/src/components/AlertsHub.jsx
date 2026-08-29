import React, { useState, useEffect } from 'react';
import { Bell, Calendar, MessageSquare, Mail, Smartphone, Download, CheckCircle2, Clock, Send, ShieldAlert, Sparkles, ExternalLink } from 'lucide-react';

export default function AlertsHub({ company, tasks, onDispatchTest }) {
  const [selectedForm, setSelectedForm] = useState(tasks[0]?.form_code || 'AOC-4');
  const [dispatchLogs, setDispatchLogs] = useState([]);
  const [dispatchStatus, setDispatchStatus] = useState(null);
  const [lastDispatchedChannel, setLastDispatchedChannel] = useState(null);
  const [previewMsg, setPreviewMsg] = useState('');

  const currentTask = tasks.find((t) => t.form_code === selectedForm) || tasks[0];

  useEffect(() => {
    if (currentTask) {
      setPreviewMsg(
        `🟢 StatutoryGuard Alert: Filing for ${currentTask.form_code} (${currentTask.title}) is due on ${currentTask.due_date}. Avoid statutory penalty risk up to ₹${currentTask.max_penalty?.toLocaleString('en-IN')}. Verify compliance: https://statutoryguard.in`
      );
    }
  }, [selectedForm, currentTask]);

  const handleTestDispatch = async (ch) => {
    try {
      const recipient = ch === 'Email' ? company.email || 'founder@startup.in' : company.phone || '+919876543210';
      const res = await onDispatchTest({
        company_cin: company.cin,
        form_code: selectedForm,
        channel: ch,
        recipient: recipient,
        message: previewMsg
      });

      setLastDispatchedChannel(ch);
      setDispatchStatus(`Successfully dispatched ${ch} reminder for ${selectedForm} to ${recipient}!`);

      // Add to local audit log table
      const newLog = {
        alert_id: res.alert_id || `ALT-${Math.floor(Math.random()*1000)}`,
        company_cin: company.cin,
        form_code: selectedForm,
        channel: ch,
        recipient: recipient,
        sent_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        status: 'DELIVERED',
        message: previewMsg
      };

      setDispatchLogs((prev) => [newLog, ...prev]);
    } catch (err) {
      console.error(err);
    }
  };

  const getGoogleCalendarUrl = () => {
    if (!currentTask) return '#';
    const title = encodeURIComponent(`StatutoryGuard: ${currentTask.form_code} MCA Filing Due`);
    const details = encodeURIComponent(`Mandatory MCA filing due date for ${currentTask.title}.\nAvoid penalty exposure up to ₹${currentTask.max_penalty?.toLocaleString('en-IN')}.\nVerify compliance on StatutoryGuard.`);
    const dates = `${currentTask.due_date.replace(/-/g, '')}/${currentTask.due_date.replace(/-/g, '')}`;
    return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${details}&dates=${dates}`;
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
            <h2 className="text-xl font-bold text-slate-100">Automated Multi-Channel Alerts Hub & Cadence Radar</h2>
            <p className="text-xs text-slate-400 mt-1">
              Dispatches automated pre-deadline reminders across WhatsApp, SMS, and Email to safeguard against ₹5 Lakh statutory penalties.
            </p>
          </div>
        </div>
      </div>

      {/* Main 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Real-time Dispatch Tester */}
        <div className="glass-panel rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-sky-400" />
              Test Real-Time Alert Dispatch
            </h3>
            <span className="text-[10px] font-extrabold bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2.5 py-0.5 rounded-full">
              LIVE SIMULATOR
            </span>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Select Statutory Form</label>
            <select
              value={selectedForm}
              onChange={(e) => setSelectedForm(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500 font-medium"
            >
              {tasks.map((t) => (
                <option key={t.task_id} value={t.form_code}>
                  {t.form_code}: {t.title} (Due {t.due_date})
                </option>
              ))}
            </select>
          </div>

          {/* Live Message Payload Preview Box */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1.5">
            <div className="flex justify-between items-center text-[11px] font-bold text-slate-400">
              <span>Dispatched Message Payload Preview</span>
              <span className="text-sky-400 font-mono">CIN: {company.cin}</span>
            </div>
            <p className="text-xs text-slate-200 font-mono leading-relaxed bg-slate-900/80 p-3 rounded-lg border border-slate-800">
              {previewMsg}
            </p>
          </div>

          {/* Channel Dispatch Buttons */}
          <div className="grid grid-cols-3 gap-3 pt-1">
            <button
              onClick={() => handleTestDispatch('WhatsApp')}
              className="p-3.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5 shadow-lg shadow-emerald-500/5"
            >
              <MessageSquare className="h-5 w-5 text-emerald-400" />
              <span>WhatsApp Alert</span>
            </button>

            <button
              onClick={() => handleTestDispatch('Email')}
              className="p-3.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5 shadow-lg shadow-sky-500/5"
            >
              <Mail className="h-5 w-5 text-sky-400" />
              <span>Email Digest</span>
            </button>

            <button
              onClick={() => handleTestDispatch('SMS')}
              className="p-3.5 bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center gap-1.5 shadow-lg shadow-purple-500/5"
            >
              <Smartphone className="h-5 w-5 text-purple-400" />
              <span>SMS Alert</span>
            </button>
          </div>

          {dispatchStatus && (
            <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 font-semibold flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
              <span>{dispatchStatus}</span>
            </div>
          )}
        </div>

        {/* Right Column: Calendar Sync & Pre-Deadline Cadence Timeline */}
        <div className="space-y-6">
          {/* Calendar Sync Radar */}
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Calendar className="h-5 w-5 text-indigo-400" />
              Calendar Sync Radar (.ics & Google Calendar)
            </h3>
            <p className="text-xs text-slate-400">
              Sync all statutory due dates directly to Google Calendar, Outlook, or Apple iCal with automated 7-day alarms.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <a
                href={`/api/alerts/calendar.ics?cin=${company.cin}`}
                download={`${company.name}_mca_deadlines.ics`}
                className="inline-flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-500/20 transition text-center"
              >
                <Download className="h-4 w-4" />
                <span>Download .ics File</span>
              </a>

              <a
                href={getGoogleCalendarUrl()}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 py-3 px-4 bg-slate-800 hover:bg-slate-700 text-sky-300 border border-sky-500/30 font-bold text-xs rounded-xl transition text-center"
              >
                <ExternalLink className="h-4 w-4 text-sky-400" />
                <span>Add to Google Calendar</span>
              </a>
            </div>
          </div>

          {/* Automated Pre-Deadline Reminders Cadence Timeline */}
          <div className="glass-panel rounded-2xl p-6 space-y-3">
            <h3 className="text-xs font-extrabold text-sky-400 uppercase tracking-wider flex items-center gap-2">
              <Clock className="h-4 w-4 text-sky-400" />
              Automated Pre-Deadline Alert Cadence Schedule
            </h3>

            <div className="space-y-2 text-xs">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                <span className="font-bold text-slate-200">T-30 Days Before Due Date</span>
                <span className="text-[11px] font-bold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-full">Email Digest to Co-Founders & CA</span>
              </div>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                <span className="font-bold text-slate-200">T-15 Days Before Due Date</span>
                <span className="text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full">WhatsApp Alert to Managing Director</span>
              </div>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                <span className="font-bold text-slate-200">T-7 Days Before Due Date</span>
                <span className="text-[11px] font-bold text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded-full">Urgent SMS & iCal Alarm</span>
              </div>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                <span className="font-bold text-slate-200">T-1 Day Emergency Alert</span>
                <span className="text-[11px] font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded-full">High-Priority Escalation Shield</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Dispatch Audit Logs Table */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-sky-400" />
          Alert Dispatch Audit Log History ({dispatchLogs.length})
        </h3>

        {dispatchLogs.length === 0 ? (
          <div className="text-center text-slate-500 py-8 text-xs border border-dashed border-slate-800 rounded-xl">
            No alert dispatches triggered in current session yet. Select a statutory form above and click WhatsApp, Email, or SMS Alert to test!
          </div>
        ) : (
          <div className="space-y-2">
            {dispatchLogs.map((log, idx) => (
              <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between text-xs gap-3">
                <div className="flex items-center gap-3">
                  <div className={`h-9 w-9 rounded-xl flex items-center justify-center shrink-0 ${
                    log.channel === 'WhatsApp'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : log.channel === 'Email'
                      ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                      : 'bg-purple-500/10 text-purple-400 border border-purple-500/30'
                  }`}>
                    {log.channel === 'WhatsApp' ? <MessageSquare className="h-4 w-4" /> : log.channel === 'Email' ? <Mail className="h-4 w-4" /> : <Smartphone className="h-4 w-4" />}
                  </div>

                  <div>
                    <span className="font-bold text-slate-100">{log.form_code} ({log.channel})</span>
                    <p className="text-[10px] text-slate-400 font-mono">Recipient: {log.recipient} &bull; Time: {log.sent_at}</p>
                  </div>
                </div>

                <span className="text-[10px] font-extrabold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-full flex items-center gap-1 shrink-0">
                  <CheckCircle2 className="h-3 w-3" /> {log.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
