import React, { useState } from 'react';
import { Bot, FileText, Send, Sparkles, AlertCircle, Clock, CheckCircle } from 'lucide-react';

export default function LegalAssistant({ presets, onTranslate, onQuery }) {
  const [activeTab, setActiveTab] = useState('decoder');
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
          onClick={() => setActiveTab('decoder')}
          className={`pb-3 text-xs font-bold transition border-b-2 ${
            activeTab === 'decoder'
              ? 'border-sky-500 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          📄 Legal Circular & Notice Decoder
        </button>
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
      </div>

      {/* Tab 1: Decoder */}
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

      {/* Tab 2: Q&A Chat */}
      {activeTab === 'chat' && (
        <div className="space-y-4">
          <div className="glass-panel rounded-2xl p-6 min-h-[350px] flex flex-col justify-between space-y-4">
            <div className="space-y-3 overflow-y-auto max-h-[400px] pr-2">
              {chatHistory.length === 0 ? (
                <div className="text-center text-slate-500 py-12 text-xs">
                  <Bot className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                  Ask any question about Companies Act 2013, INC-20A rules, DIR-3 KYC deadlines, or board meeting counts.
                </div>
              ) : (
                chatHistory.map((m, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-2xl text-xs ${
                      m.role === 'user'
                        ? 'bg-sky-500/10 border border-sky-500/30 text-slate-100 ml-12'
                        : 'bg-slate-900 border border-slate-800 text-slate-200 mr-12'
                    }`}
                  >
                    <span className="text-[10px] font-bold block mb-1 text-slate-400">
                      {m.role === 'user' ? 'You' : 'StatutoryGuard AI'}
                    </span>
                    <div className="whitespace-pre-line font-medium">{m.content}</div>
                  </div>
                ))
              )}
            </div>

            <form onSubmit={handleQuerySubmit} className="flex gap-2 pt-2 border-t border-slate-800">
              <input
                type="text"
                placeholder="Ask compliance question (e.g. 'What is the penalty for missing INC-20A?')"
                value={questionInput}
                onChange={(e) => setQuestionInput(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
              <button
                type="submit"
                disabled={loadingQuery}
                className="px-5 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center gap-1.5 shrink-0"
              >
                <Send className="h-4 w-4" />
                <span>Send</span>
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
