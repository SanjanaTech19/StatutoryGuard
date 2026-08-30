import React, { useState, useEffect } from 'react';
import { Bell, Calendar, MessageSquare, Mail, Download, CheckCircle2, Clock, Send, ShieldAlert, Sparkles, ExternalLink, Edit3, Play, Smartphone, Globe } from 'lucide-react';

export default function AlertsHub({ company, tasks, onDispatchTest }) {
  const [selectedForm, setSelectedForm] = useState(tasks[0]?.form_code || 'AOC-4');
  const [customPhone, setCustomPhone] = useState(company.phone || '+919876543210');
  const [customEmail, setCustomEmail] = useState(company.email || 'founder@startup.in');
  const [dispatchLogs, setDispatchLogs] = useState([]);
  const [dispatchStatus, setDispatchStatus] = useState(null);
  const [previewMsg, setPreviewMsg] = useState('');

  const currentTask = tasks.find((t) => t.form_code === selectedForm) || tasks[0];

  useEffect(() => {
    if (currentTask) {
      setPreviewMsg(
        `[STATUTORYGUARD COMPLIANCE ALERT]\n\n📌 Form: ${currentTask.form_code} (${currentTask.title})\n📅 Due Date: ${currentTask.due_date}\n⚠️ Penalty Exposure: Up to ₹${currentTask.max_penalty?.toLocaleString('en-IN')}\n\nPlease ensure timely filing to maintain 100% audit readiness and avoid penalty risk.`
      );
    }
  }, [selectedForm, currentTask]);

  const handleTestDispatch = async (ch, useWeb = false, customStage = null) => {
    try {
      const recipient = ch === 'Email' ? customEmail.trim() : customPhone.trim();
      if (!recipient) {
        alert('Please enter a valid phone number or email address.');
        return;
      }

      const stagePrefix = customStage ? `[${customStage} CADENCE] ` : '';
      const finalMsg = `${stagePrefix}${previewMsg}`;

      const res = await onDispatchTest({
        company_cin: company.cin,
        form_code: selectedForm,
        channel: ch,
        recipient: recipient,
        message: finalMsg
      });

      // Handle Real Direct Opening of WhatsApp / Gmail Apps
      if (ch === 'WhatsApp') {
        const cleanPhone = recipient.replace(/[^0-9]/g, '');
        const encodedMsg = encodeURIComponent(finalMsg);
        
        if (useWeb) {
          const webUrl = `https://api.whatsapp.com/send?phone=${cleanPhone}&text=${encodedMsg}`;
          window.open(webUrl, '_blank');
          setDispatchStatus(`WhatsApp Web/App link opened for ${recipient}! Click Send in WhatsApp.`);
        } else {
          // Attempt native protocol + open web link as robust fallback
          const webUrl = `https://api.whatsapp.com/send?phone=${cleanPhone}&text=${encodedMsg}`;
          window.open(webUrl, '_blank');
          try {
            window.location.href = `whatsapp://send?phone=${cleanPhone}&text=${encodedMsg}`;
          } catch (e) {}
          setDispatchStatus(`Dispatched WhatsApp alert to ${recipient}! Click Send in WhatsApp window.`);
        }
      } else if (ch === 'Email' && res.mailto_url) {
        window.open(res.mailto_url, '_blank');
        setDispatchStatus(`Gmail Web Compose opened for ${recipient}! Click Send to dispatch email.`);
      } else {
        setDispatchStatus(`Triggered ${customStage || ch} compliance alert simulation!`);
      }

      // Add to local audit log table
      const newLog = {
        alert_id: res.alert_id || `ALT-${Math.floor(Math.random()*1000)}`,
        company_cin: company.cin,
        form_code: selectedForm,
        channel: customStage ? `${ch} (${customStage})` : ch,
        recipient: recipient,
        sent_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        status: 'DELIVERED',
        message: finalMsg
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
              Dispatches automated pre-deadline reminders across WhatsApp, Gmail, and Google / Apple Calendars.
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
              Real-Time Alert Dispatcher
            </h3>
            <span className="text-[10px] font-extrabold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full">
              LIVE DISPATCH READY
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

          {/* Target Recipient Phone & Email Editable Inputs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 bg-slate-950 p-3.5 rounded-xl border border-slate-800">
            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1 flex items-center gap-1">
                <Edit3 className="h-3 w-3 text-emerald-400" />
                Target WhatsApp Mobile No.
              </label>
              <input
                type="text"
                placeholder="+919876543210"
                value={customPhone}
                onChange={(e) => setCustomPhone(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1 flex items-center gap-1">
                <Edit3 className="h-3 w-3 text-sky-400" />
                Target Recipient Email
              </label>
              <input
                type="email"
                placeholder="founder@startup.in"
                value={customEmail}
                onChange={(e) => setCustomEmail(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          {/* Live Message Payload Preview Box */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1.5">
            <div className="flex justify-between items-center text-[11px] font-bold text-slate-400">
              <span>Clean Dispatched Message Payload</span>
              <span className="text-sky-400 font-mono">CIN: {company.cin}</span>
            </div>
            <p className="text-xs text-slate-200 font-mono leading-relaxed bg-slate-900/80 p-3.5 rounded-lg border border-slate-800 whitespace-pre-line">
              {previewMsg}
            </p>
          </div>

          {/* Channel Dispatch Buttons (WhatsApp Web, WhatsApp App & Gmail) */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            <button
              onClick={() => handleTestDispatch('WhatsApp', true)}
              className="p-3 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center gap-1 shadow-lg shadow-emerald-500/5 py-3.5"
            >
              <Globe className="h-5 w-5 text-emerald-400" />
              <span>WhatsApp Web</span>
            </button>

            <button
              onClick={() => handleTestDispatch('WhatsApp', false)}
              className="p-3 bg-teal-500/10 hover:bg-teal-500/20 text-teal-300 border border-teal-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center gap-1 shadow-lg shadow-teal-500/5 py-3.5"
            >
              <Smartphone className="h-5 w-5 text-teal-300" />
              <span>WhatsApp App</span>
            </button>

            <button
              onClick={() => handleTestDispatch('Email')}
              className="p-3 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center gap-1 shadow-lg shadow-sky-500/5 py-3.5"
            >
              <Mail className="h-5 w-5 text-sky-400" />
              <span>Send Gmail</span>
            </button>
          </div>

          {dispatchStatus && (
            <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 font-semibold space-y-1">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                <span>{dispatchStatus}</span>
              </div>
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
              Sync form statutory due dates directly to Google Calendar, Outlook, or Apple iCal with automated 7-day alarms.
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

          {/* Pre-Deadline Cadence Schedule */}
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Clock className="h-5 w-5 text-amber-400" />
                Pre-Deadline Escalation Cadence
              </h3>
              <span className="text-[10px] font-extrabold bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2.5 py-0.5 rounded-full">
                4-STAGE CADENCE
              </span>
            </div>

            <div className="space-y-3">
              {[
                { stage: 'T-30 Days', channel: 'Email', status: 'Email Notification', color: 'text-sky-400 bg-sky-500/10 border-sky-500/30' },
                { stage: 'T-15 Days', channel: 'WhatsApp', status: 'WhatsApp Message', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' },
                { stage: 'T-7 Days', channel: 'Calendar', status: 'Calendar Event Alarm', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' },
                { stage: 'T-1 Day', channel: 'WhatsApp', status: 'Urgent WhatsApp Escalation', color: 'text-rose-400 bg-rose-500/10 border-rose-500/30' }
              ].map((c, idx) => (
                <div key={idx} className="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-0.5 rounded-md font-bold text-[10px] border ${c.color}`}>{c.stage}</span>
                    <span className="font-semibold text-slate-200">{c.status}</span>
                  </div>

                  <button
                    onClick={() => handleTestDispatch(c.channel === 'Email' ? 'Email' : 'WhatsApp', false, c.stage)}
                    className="flex items-center gap-1 text-[11px] font-bold text-sky-400 hover:text-sky-300 transition"
                  >
                    <Play className="h-3 w-3 fill-sky-400" />
                    <span>Test {c.stage}</span>
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Dispatched Alerts Audit Log */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <ShieldAlert className="h-5 w-5 text-indigo-400" />
          Dispatched Alerts Audit Log
        </h3>

        {dispatchLogs.length === 0 ? (
          <div className="text-center text-slate-500 py-6 text-xs">
            No alert dispatches logged in this session yet. Click 'WhatsApp Web', 'WhatsApp App', or 'Send Gmail' above to test dispatching.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                  <th className="py-2.5 px-3">Alert ID</th>
                  <th className="py-2.5 px-3">Form Code</th>
                  <th className="py-2.5 px-3">Channel</th>
                  <th className="py-2.5 px-3">Recipient</th>
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {dispatchLogs.map((log, idx) => (
                  <tr key={idx} className="hover:bg-slate-900/40 font-medium">
                    <td className="py-2.5 px-3 text-sky-400 font-mono text-[11px]">{log.alert_id}</td>
                    <td className="py-2.5 px-3 text-slate-200">{log.form_code}</td>
                    <td className="py-2.5 px-3 text-slate-300">{log.channel}</td>
                    <td className="py-2.5 px-3 text-slate-300 font-mono text-[11px]">{log.recipient}</td>
                    <td className="py-2.5 px-3 text-slate-400">{log.sent_at}</td>
                    <td className="py-2.5 px-3 text-right">
                      <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                        {log.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
