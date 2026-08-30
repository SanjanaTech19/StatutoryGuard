import React, { useState } from 'react';
import { Bot, FileText, Send, Sparkles, AlertCircle, Clock, CheckCircle, ShieldAlert, Scale, AlertTriangle, CheckCircle2, ArrowRightCircle } from 'lucide-react';

function FormattedLegalResponse({ text }) {
  if (!text) return null;

  const lines = text.split('\n');
  const elements = [];

  lines.forEach((line, idx) => {
    const trimmed = line.strip ? line.strip() : line.trim();
    if (!trimmed) return;

    // Actionable Rectification Steps Section Header (e.g. ### 📝 3. Actionable Rectification Steps:)
    if (trimmed.includes('Actionable Rectification Steps') || trimmed.includes('Actionable Compliance Steps')) {
      elements.push(
        <div key={idx} className="flex items-center gap-2 font-extrabold text-sm text-emerald-400 border-b border-emerald-500/30 pb-2 mt-4 mb-3">
          <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
          <span className="uppercase tracking-wider">ACTIONABLE RECTIFICATION STEPS</span>
        </div>
      );
      return;
    }

    // Headings (e.g. ### or **Header**)
    if (trimmed.startsWith('###') || (trimmed.startsWith('**') && trimmed.endsWith('**') && trimmed.length < 80)) {
      const cleanHeading = trimmed.replace(/^[#*\s]+|[*\s]+$/g, '');
      const isPenalty = cleanHeading.toLowerCase().includes('penalty') || cleanHeading.toLowerCase().includes('consequence');
      
      elements.push(
        <div key={idx} className={`flex items-center gap-2 font-extrabold text-sm border-b pb-1.5 mt-4 mb-2 ${
          isPenalty ? 'text-amber-400 border-amber-500/30' : 'text-sky-400 border-slate-800'
        }`}>
          {isPenalty ? <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0" /> : <Scale className="h-4 w-4 text-sky-400 shrink-0" />}
          <span>{cleanHeading}</span>
        </div>
      );
      return;
    }

    // Individual Action Steps (e.g. 1. Pass Board Resolution... or 2. File Form...)
    if (/^\d+\./.test(trimmed)) {
      const match = trimmed.match(/^(\d+)\.\s*(.*)/);
      const stepNum = match ? match[1] : '';
      const stepContent = match ? match[2] : trimmed;

      const parts = stepContent.split(/(\*\*.*?\*\*)/g);

      elements.push(
        <div key={idx} className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-200 text-xs my-2 flex items-start gap-3 shadow-sm hover:border-emerald-500/50 transition">
          <div className="h-6 w-6 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 font-extrabold flex items-center justify-center text-[11px] shrink-0 mt-0.5">
            {stepNum}
          </div>
          <div className="flex-1 text-slate-100 font-medium leading-relaxed">
            {parts.map((part, pIdx) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={pIdx} className="font-extrabold text-emerald-300">{part.slice(2, -2)}</strong>;
              }
              return part;
            })}
          </div>
        </div>
      );
      return;
    }

    // Standard Bullet Points (e.g. - Private Limited Company...)
    if (trimmed.startsWith('-') || trimmed.startsWith('*')) {
      const cleanBullet = trimmed.replace(/^[*\-\s]+/, '');
      const parts = cleanBullet.split(/(\*\*.*?\*\*)/g);

      elements.push(
        <div key={idx} className="flex items-start gap-2.5 my-1.5 pl-1 text-xs text-slate-200 leading-relaxed">
          <ArrowRightCircle className="h-3.5 w-3.5 text-sky-400 shrink-0 mt-0.5" />
          <p className="flex-1">
            {parts.map((part, pIdx) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={pIdx} className="font-extrabold text-slate-100">{part.slice(2, -2)}</strong>;
              }
              return part;
            })}
          </p>
        </div>
      );
      return;
    }

    // Standard Text Line
    const parts = trimmed.split(/(\*\*.*?\*\*)/g);
    elements.push(
      <p key={idx} className="text-xs text-slate-200 leading-relaxed my-1">
        {parts.map((part, pIdx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={pIdx} className="font-extrabold text-slate-100">{part.slice(2, -2)}</strong>;
          }
          return part;
        })}
      </p>
    );
  });

  return <div className="space-y-1">{elements}</div>;
}

export default function LegalAssistant({ presets, onTranslate, onQuery }) {
  const [activeTab, setActiveTab] = useState('chat');
  const [selectedPreset, setSelectedPreset] = useState('');
  const [customText, setCustomText] = useState('');
  const [translationResult, setTranslationResult] = useState(null);
  const [loadingTranslate, setLoadingTranslate] = useState(false);

  const [questionInput, setQuestionInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loadingQuery, setLoadingQuery] = useState(false);

  const handleTranslateSubmit = async (e) => {
    e.preventDefault();
    setLoadingTranslate(true);
    try {
      let rawText = customText;
      if (selectedPreset) {
        const p = presets.find((item) => item.title === selectedPreset);
        if (p) rawText = p.raw_text;
      }
      if (!rawText) {
        alert('Please select a preset or paste circular text.');
        setLoadingTranslate(false);
        return;
      }
      const res = await onTranslate(rawText);
      setTranslationResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingTranslate(false);
    }
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!questionInput) return;
    const userQ = questionInput;
    setQuestionInput('');
    setLoadingQuery(true);

    try {
      const res = await onQuery(userQ);
      setChatHistory((prev) => [
        ...prev,
        { role: 'user', content: userQ },
        { role: 'assistant', content: res.answer }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingQuery(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="glass-card rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Bot className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">Plain-English MCA Legal Assistant</h2>
            <p className="text-xs text-slate-400 mt-1">
              Translates dense MCA circulars into actionable step-by-step task lists with clear status indicators.
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-4">
        <button
          onClick={() => setActiveTab('chat')}
          className={`pb-3 text-xs font-bold transition border-b-2 ${
            activeTab === 'chat'
              ? 'border-sky-500 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          💬 Compliance Q&A Assistant
        </button>
        <button
          onClick={() => setActiveTab('decoder')}
          className={`pb-3 text-xs font-bold transition border-b-2 ${
            activeTab === 'decoder'
              ? 'border-sky-500 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          📄 Legal Circular & Notice Decoder
        </button>
      </div>

      {/* Tab 1: Q&A Chat */}
      {activeTab === 'chat' && (
        <div className="space-y-4">
          <div className="glass-panel rounded-2xl p-6 min-h-[400px] flex flex-col justify-between space-y-4">
            <div className="space-y-4 overflow-y-auto max-h-[500px] pr-2">
              {chatHistory.length === 0 ? (
                <div className="text-center text-slate-500 py-16 text-xs">
                  <Bot className="h-10 w-10 mx-auto mb-2 text-sky-400" />
                  <p className="font-bold text-slate-300 text-sm">Ask StatutoryGuard AI Any Compliance Question</p>
                  <p className="mt-1 text-slate-500">Ask about Companies Act 2013, Section 128 Audit Trail, INC-20A rules, DIR-3 KYC, or AOC-4 deadlines.</p>
                </div>
              ) : (
                chatHistory.map((m, idx) => (
                  <div
                    key={idx}
                    className={`p-5 rounded-2xl text-xs ${
                      m.role === 'user'
                        ? 'bg-sky-500/10 border border-sky-500/30 text-slate-100 ml-8 font-semibold'
                        : 'bg-slate-900 border border-slate-800 text-slate-200 mr-4 space-y-2'
                    }`}
                  >
                    <div className="flex items-center justify-between border-b border-slate-800/80 pb-2 mb-2">
                      <span className="text-[11px] font-bold text-sky-400 flex items-center gap-1.5">
                        {m.role === 'user' ? '👤 You' : '🛡️ StatutoryGuard AI Response'}
                      </span>
                    </div>

                    {m.role === 'user' ? (
                      <p className="text-xs text-slate-100 leading-relaxed font-medium">{m.content}</p>
                    ) : (
                      <FormattedLegalResponse text={m.content} />
                    )}
                  </div>
                ))
              )}
            </div>

            <form onSubmit={handleQuerySubmit} className="flex gap-2 pt-3 border-t border-slate-800">
              <input
                type="text"
                placeholder="Ask compliance question (e.g. 'What are the rules for electronic books of account under Section 128?')"
                value={questionInput}
                onChange={(e) => setQuestionInput(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
              <button
                type="submit"
                disabled={loadingQuery}
                className="px-6 py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center gap-1.5 shrink-0"
              >
                <Send className="h-4 w-4" />
                <span>{loadingQuery ? 'Analyzing...' : 'Send'}</span>
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Tab 2: Decoder */}
      {activeTab === 'decoder' && (
        <div className="space-y-6">
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <form onSubmit={handleTranslateSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1">
                  Select Preset MCA Circular
                </label>
                <select
                  value={selectedPreset}
                  onChange={(e) => setSelectedPreset(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                >
                  <option value="">Select Preset Circular...</option>
                  {presets?.map((p) => (
                    <option key={p.id} value={p.title}>
                      {p.title}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1">
                  Or Paste Custom MCA Legal Circular Text
                </label>
                <textarea
                  rows={4}
                  value={customText}
                  onChange={(e) => setCustomText(e.target.value)}
                  placeholder="Paste dense legal text here..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <button
                type="submit"
                disabled={loadingTranslate}
                className="w-full py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center justify-center gap-2"
              >
                <Sparkles className="h-4 w-4" />
                <span>{loadingTranslate ? 'Translating via LangChain AI...' : 'Translate to Plain-English'}</span>
              </button>
            </form>
          </div>

          {/* Translation Result Card */}
          {translationResult && (
            <div className="glass-card rounded-2xl p-6 space-y-5">
              <div>
                <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider">Plain-English Summary</h4>
                <p className="text-sm font-semibold text-slate-100 mt-1">{translationResult.summary}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold">Compliance Due Date</span>
                  <span className="text-xs font-bold text-amber-400 mt-0.5 block">{translationResult.deadline}</span>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold">Penalty Risk Exposure</span>
                  <span className="text-xs font-bold text-rose-400 mt-0.5 block">{translationResult.penalty_risk}</span>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300">Actionable Task Breakdown</h4>
                {translationResult.actionable_tasks?.map((t, idx) => (
                  <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-100">{t.task}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        t.status === 'Filed'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                          : t.status === 'Review'
                          ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                          : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                      }`}>
                        [{t.status.toUpperCase()}]
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">Action: {t.action}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
