import React, { useState, useEffect } from 'react';
import { Bell, Calendar, MessageSquare, Mail, Download, CheckCircle2, Clock, Send, ShieldAlert, Sparkles, ExternalLink, Edit3, Play } from 'lucide-react';

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
        const cleanPhone = recipient.replace(/[^0-9+]/g, '');
        const encodedMsg = encodeURIComponent(finalMsg);
        
        if (useWeb) {
          window.open(`https://web.whatsapp.com/send?phone=${cleanPhone}&text=${encodedMsg}`, '_blank');
          setDispatchStatus(`WhatsApp Web opened for ${recipient}! Message logged to audit trail.`);
        } else {
          window.location.href = `whatsapp://send?phone=${cleanPhone}&text=${encodedMsg}`;
          setDispatchStatus(`Launched WhatsApp Desktop/Mobile App directly for ${recipient}!`);
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

  const getOutlookCalendarUrl = () => {
    if (!currentTask) return '#';
    const title = encodeURIComponent(`StatutoryGuard: ${currentTask.form_code} MCA Filing Due`);
    const details = encodeURIComponent(`Mandatory MCA filing due date for ${currentTask.title}.\nAvoid penalty exposure up to ₹${currentTask.max_penalty?.toLocaleString('en-IN')}.`);
    return `https://outlook.office.com/calendar/0/deeplink/compose?subject=${title}&body=${details}&startdt=${currentTask.due_date}T09:00:00Z&enddt=${currentTask.due_date}T10:00:00Z`;
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
              Dispatches automated pre-deadline reminders across WhatsApp, Gmail, and Google/Outlook Calendars.
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

          {/* Channel Dispatch Buttons (WhatsApp & Email) */}
          <div className="grid grid-cols-2 gap-4 pt-1">
            <button
              onClick={() => handleTestDispatch('WhatsApp', false)}
              className="p-3.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center gap-1.5 shadow-lg shadow-emerald-500/5 py-4"
            >
              <MessageSquare className="h-6 w-6 text-emerald-400" />
              <span>Launch WhatsApp</span>
            </button>

            <button
              onClick={() => handleTestDispatch('Email')}
              className="p-3.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center gap-1.5 shadow-lg shadow-sky-500/5 py-4"
            >
              <Mail className="h-6 w-6 text-sky-400" />
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
              Calendar Sync Radar (Google, Outlook & .ics iCal)
            </h3>
            <p className="text-xs text-slate-400">
              Sync form statutory due dates directly to Google Calendar, Outlook Web, or Apple iCal with automated 7-day alarms.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              <a
                href={`/api/alerts/calendar.ics?cin=${company.cin}`}
                download={`${company.name}_mca_deadlines.ics`}
                className="inline-flex items-center justify-center gap-1.5 py-2.5 px-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-bold text-[11px] rounded-xl shadow-lg shadow-indigo-500/20 transition text-center"
              >
                <Download className="h-3.5 w-3.5" />
                <span>Download .ics</span>
              </a>

              <a
                href={getGoogleCalendarUrl()}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-1.5 py-2.5 px-3 bg-slate-800 hover:bg-slate-700 text-sky-300 border border-sky-500/30 font-bold text-[11px] rounded-xl transition text-center"
              >
                <ExternalLink className="h-3.5 w-3.5 text-sky-400" />
                <span>Google Calendar</span>
              </a>

              <a
                href={getOutlookCalendarUrl()}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 py-2.5 px-3 bg-slate-800 hover:bg-slate-700 text-purple-300 border border-purple-500/30 font-bold text-[11px] rounded-xl transition text-center"
              >
                <ExternalLink className="h-3.5 w-3.5 text-purple-400" />
                <span>Outlook Web</span>
              </a>
            </div>

            {/* Upcoming Deadline List Preview Box */}
            <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-2 text-xs">
              <span className="text-[10px] font-extrabold text-slate-400 block uppercase tracking-wider">Upcoming Calendar Events ({tasks.filter(t=>t.status!=='Filed').length})</span>
              <div className="space-y-1.5 max-h-[110px] overflow-y-auto pr-1">
                {tasks.filter(t=>t.status!=='Filed').slice(0, 4).map((t, idx) => (
                  <div key={idx} className="flex justify-between items-center bg-slate-900/90 p-2 rounded-lg border border-slate-800/80 text-[11px]">
                    <span className="font-bold text-sky-400">{t.form_code}: <span className="text-slate-200 font-medium">{t.title}</span></span>
                    <span className="font-mono text-amber-400 font-bold">{t.due_date}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Interactive Automated Pre-Deadline Reminders Cadence Schedule */}
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-extrabold text-sky-400 uppercase tracking-wider flex items-center gap-2">
                <Clock className="h-4 w-4 text-sky-400" />
                Automated Pre-Deadline Alert Cadence Schedule
              </h3>
              <span className="text-[10px] font-extrabold text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                CLICK TO TEST CADENCE
              </span>
            </div>

            <div className="space-y-2 text-xs">
              {/* T-30 Days */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="font-bold text-slate-200 block">T-30 Days Before Due Date</span>
                  <span className="text-[10px] text-slate-400">Email Digest to Co-Founders & CA</span>
                </div>
                <button
                  onClick={() => handleTestDispatch('Email', false, 'T-30')}
                  className="px-2.5 py-1 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-lg text-[10px] font-bold transition flex items-center gap-1 shrink-0"
                >
                  <Play className="h-3 w-3" /> Test T-30 Email
                </button>
              </div>

              {/* T-15 Days */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="font-bold text-slate-200 block">T-15 Days Before Due Date</span>
                  <span className="text-[10px] text-slate-400">WhatsApp Alert to Managing Director</span>
                </div>
                <button
                  onClick={() => handleTestDispatch('WhatsApp', false, 'T-15')}
                  className="px-2.5 py-1 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-lg text-[10px] font-bold transition flex items-center gap-1 shrink-0"
                >
                  <Play className="h-3 w-3" /> Test T-15 WhatsApp
                </button>
              </div>

              {/* T-7 Days */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="font-bold text-slate-200 block">T-7 Days Before Due Date</span>
                  <span className="text-[10px] text-slate-400">Calendar iCal Alarm & Priority Notice</span>
                </div>
                <button
                  onClick={() => handleTestDispatch('Email', false, 'T-7')}
                  className="px-2.5 py-1 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-lg text-[10px] font-bold transition flex items-center gap-1 shrink-0"
                >
                  <Play className="h-3 w-3" /> Test T-7 Alarm
                </button>
              </div>

              {/* T-1 Day */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="font-bold text-slate-200 block">T-1 Day Emergency Alert</span>
                  <span className="text-[10px] text-slate-400">High-Priority Escalation Shield</span>
                </div>
                <button
                  onClick={() => handleTestDispatch('WhatsApp', false, 'T-1 EMERGENCY')}
                  className="px-2.5 py-1 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-lg text-[10px] font-bold transition flex items-center gap-1 shrink-0"
                >
                  <Play className="h-3 w-3" /> Test T-1 Escalation
                </button>
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
            No alert dispatches triggered in current session yet. Select a statutory form above and click Launch WhatsApp or Send Gmail to test!
          </div>
        ) : (
          <div className="space-y-2">
            {dispatchLogs.map((log, idx) => (
              <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between text-xs gap-3">
                <div className="flex items-center gap-3">
                  <div className={`h-9 w-9 rounded-xl flex items-center justify-center shrink-0 ${
                    log.channel.includes('WhatsApp')
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                  }`}>
                    {log.channel.includes('WhatsApp') ? <MessageSquare className="h-4 w-4" /> : <Mail className="h-4 w-4" />}
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
