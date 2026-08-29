import React, { useState } from 'react';
import { 
  ShieldCheck, AlertTriangle, CheckCircle2, Clock, Search, 
  ChevronDown, ChevronUp, FileText, CheckCircle, AlertCircle, ArrowUpRight
} from 'lucide-react';

export default function Dashboard({ data, onMarkFiled }) {
  if (!data || !data.company) {
    return (
      <div className="p-8 text-center text-slate-400">
        Loading dashboard metrics...
      </div>
    );
  }

  const { company, tasks, metrics } = data;
  const [statusFilter, setStatusFilter] = useState('All');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [showCompanyDetails, setShowCompanyDetails] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [srnInput, setSrnInput] = useState('');
  const [filedDateInput, setFiledDateInput] = useState(new Date().toISOString().split('T')[0]);

  // Filtering tasks
  let filteredTasks = tasks || [];
  if (statusFilter === 'Pending') {
    filteredTasks = filteredTasks.filter((t) => t.status !== 'Filed');
  } else if (statusFilter === 'Filed') {
    filteredTasks = filteredTasks.filter((t) => t.status === 'Filed');
  } else if (statusFilter === 'Overdue') {
    filteredTasks = filteredTasks.filter((t) => t.status !== 'Filed' && t.days_left < 0);
  }

  if (categoryFilter !== 'All') {
    filteredTasks = filteredTasks.filter((t) => t.category === categoryFilter);
  }

  if (searchQuery) {
    filteredTasks = filteredTasks.filter(
      (t) =>
        t.form_code.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.title.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }

  const handleMarkFiledSubmit = (e) => {
    e.preventDefault();
    if (selectedTask && srnInput) {
      onMarkFiled(selectedTask.task_id, srnInput, filedDateInput);
      setSelectedTask(null);
      setSrnInput('');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Compliance Health Score */}
        <div className="glass-card rounded-2xl p-5 relative overflow-hidden group hover:border-sky-500/50 transition">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-semibold text-slate-400">Compliance Health</p>
              <h3 className="text-2xl font-extrabold text-slate-100 mt-1">
                {metrics.health_score}%
              </h3>
            </div>
            <div className="h-10 w-10 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <ShieldCheck className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
            <span>{metrics.health_score >= 80 ? 'Healthy Audit Score' : 'Attention Required'}</span>
          </div>
        </div>

        {/* Penalty Exposure */}
        <div className="glass-card rounded-2xl p-5 relative overflow-hidden group hover:border-rose-500/50 transition">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-semibold text-slate-400">Statutory Penalty Exposure</p>
              <h3 className="text-2xl font-extrabold text-rose-400 mt-1">
                ₹{metrics.penalty_exposure.toLocaleString('en-IN')}
              </h3>
            </div>
            <div className="h-10 w-10 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
              <AlertTriangle className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-rose-300 font-medium">
            <span>{metrics.penalty_exposure > 0 ? '₹5L Max Penalty Shield Active' : 'Zero Penalty Risk'}</span>
          </div>
        </div>

        {/* Pending Filings */}
        <div className="glass-card rounded-2xl p-5 relative overflow-hidden group hover:border-amber-500/50 transition">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-semibold text-slate-400">Pending Filings</p>
              <h3 className="text-2xl font-extrabold text-amber-400 mt-1">
                {metrics.pending_count}
              </h3>
            </div>
            <div className="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Clock className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-amber-300 font-medium">
            <span>{metrics.overdue_count > 0 ? `${metrics.overdue_count} Overdue` : 'On Track'}</span>
          </div>
        </div>

        {/* Verified Filings */}
        <div className="glass-card rounded-2xl p-5 relative overflow-hidden group hover:border-emerald-500/50 transition">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-semibold text-slate-400">Filed & Verified</p>
              <h3 className="text-2xl font-extrabold text-emerald-400 mt-1">
                {metrics.filed_count}
              </h3>
            </div>
            <div className="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <CheckCircle2 className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-emerald-300 font-medium">
            <span>100% Audit Ready</span>
          </div>
        </div>

        {/* Hours Saved */}
        <div className="glass-card rounded-2xl p-5 relative overflow-hidden group hover:border-indigo-500/50 transition">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-semibold text-slate-400">Hours Saved/Month</p>
              <h3 className="text-2xl font-extrabold text-indigo-400 mt-1">
                {metrics.hours_saved}
              </h3>
            </div>
            <div className="h-10 w-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <ArrowUpRight className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-indigo-300 font-medium">
            <span>+85% Operational Efficiency</span>
          </div>
        </div>
      </div>

      {/* Startup Master Data Details Collapsible */}
      <div className="glass-panel rounded-2xl p-5">
        <button
          onClick={() => setShowCompanyDetails(!showCompanyDetails)}
          className="w-full flex items-center justify-between text-left font-bold text-slate-200 text-sm"
        >
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4 text-sky-400" />
            <span>Active Startup Profile & MCA Master Data</span>
            <span className="text-xs font-semibold text-sky-400 bg-sky-500/10 border border-sky-500/30 px-2 py-0.5 rounded-full">
              {company.cin}
            </span>
          </div>
          {showCompanyDetails ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>

        {showCompanyDetails && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 mt-4 border-t border-slate-800 text-xs">
            <div>
              <p className="text-slate-400">Company Name:</p>
              <p className="font-bold text-slate-200">{company.name}</p>
              <p className="text-slate-400 mt-2">Entity Type:</p>
              <p className="font-bold text-slate-200">{company.entity_type}</p>
            </div>
            <div>
              <p className="text-slate-400">Incorporation Date:</p>
              <p className="font-bold text-slate-200">{company.incorporation_date}</p>
              <p className="text-slate-400 mt-2">ROC Office:</p>
              <p className="font-bold text-slate-200">{company.roc_office}</p>
            </div>
            <div>
              <p className="text-slate-400">Authorized Capital:</p>
              <p className="font-bold text-slate-200">₹{company.authorized_capital?.toLocaleString('en-IN')}</p>
              <p className="text-slate-400 mt-2">Paid-up Capital:</p>
              <p className="font-bold text-slate-200">₹{company.paid_up_capital?.toLocaleString('en-IN')}</p>
            </div>
          </div>
        )}
      </div>

      {/* Statutory Matrix Section */}
      <div className="space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <span>📋 Statutory Requirements Matrix</span>
            <span className="text-xs font-semibold bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full">
              {filteredTasks.length} Forms
            </span>
          </h2>

          {/* Filter Pills & Search */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="h-4 w-4 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                placeholder="Search form code or title..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-sky-500 w-48"
              />
            </div>

            {/* Status Pills */}
            <div className="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs">
              {['All', 'Pending', 'Filed', 'Overdue'].map((s) => (
                <button
                  key={s}
                  onClick={() => setStatusFilter(s)}
                  className={`px-2.5 py-1 rounded-lg font-medium transition ${
                    statusFilter === s
                      ? 'bg-sky-500 text-white font-bold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Statutory Forms List */}
        <div className="space-y-3">
          {filteredTasks.map((t) => {
            const isFiled = t.status === 'Filed';
            const isOverdue = !isFiled && t.days_left < 0;
            const isDueSoon = !isFiled && t.days_left <= 15;

            return (
              <div
                key={t.task_id}
                className="glass-panel rounded-2xl p-5 hover:border-slate-700 transition space-y-3"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-extrabold text-sky-400 bg-sky-500/10 border border-sky-500/30 px-2.5 py-0.5 rounded-lg text-xs">
                        {t.form_code}
                      </span>
                      <h3 className="font-bold text-slate-100 text-sm">{t.title}</h3>

                      {/* Status Badges */}
                      {isFiled ? (
                        <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <CheckCircle className="h-3 w-3" /> FILED
                        </span>
                      ) : isOverdue ? (
                        <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <AlertCircle className="h-3 w-3" /> OVERDUE ({Math.abs(t.days_left)} days ago)
                        </span>
                      ) : isDueSoon ? (
                        <span className="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Clock className="h-3 w-3" /> DUE IN {t.days_left} DAYS
                        </span>
                      ) : (
                        <span className="bg-slate-800 text-slate-400 border border-slate-700 text-[10px] font-bold px-2 py-0.5 rounded-full">
                          DUE {t.due_date}
                        </span>
                      )}
                    </div>

                    <p className="text-xs text-slate-400">{t.description}</p>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <div className="text-right hidden sm:block text-xs">
                      <span className="text-slate-500 block">Penalty Exposure</span>
                      <span className="font-bold text-rose-400">Up to ₹{t.max_penalty?.toLocaleString('en-IN')}</span>
                    </div>

                    {isFiled ? (
                      <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
                        <CheckCircle2 className="h-4 w-4" /> Verified
                      </span>
                    ) : (
                      <button
                        onClick={() => setSelectedTask(t)}
                        className="px-3.5 py-1.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-sky-500/20 transition"
                      >
                        Mark as Filed
                      </button>
                    )}
                  </div>
                </div>

                {/* Key Documents Needed Pills */}
                {t.key_documents && t.key_documents.length > 0 && (
                  <div className="pt-2 border-t border-slate-800/60 flex items-center gap-2 flex-wrap text-[11px]">
                    <span className="text-slate-500 font-medium">Required Documents:</span>
                    {t.key_documents.map((doc, i) => (
                      <span key={i} className="bg-slate-900 text-slate-300 px-2 py-0.5 rounded border border-slate-800">
                        {doc}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Mark Filed Modal */}
      {selectedTask && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-emerald-400" />
              Mark Form `{selectedTask.form_code}` as Filed
            </h3>
            <p className="text-xs text-slate-400">
              Enter official MCA Acknowledgement SRN number to record filing and verify audit compliance.
            </p>

            <form onSubmit={handleMarkFiledSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">MCA SRN Number</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. AA123456789"
                  value={srnInput}
                  onChange={(e) => setSrnInput(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:border-sky-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Filing Date</label>
                <input
                  type="date"
                  required
                  value={filedDateInput}
                  onChange={(e) => setFiledDateInput(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:border-sky-500 focus:outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setSelectedTask(null)}
                  className="px-4 py-2 text-xs font-semibold text-slate-400 hover:text-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-emerald-500/20"
                >
                  Confirm Filing
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
