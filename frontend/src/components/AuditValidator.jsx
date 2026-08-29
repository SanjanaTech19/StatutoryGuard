import React, { useState } from 'react';
import { ShieldCheck, FileCheck, Upload, AlertOctagon, CheckCircle2, AlertTriangle, FileText, Scale, Coins, Wallet } from 'lucide-react';

const SAMPLE_BALANCE_SHEET_TEXT = `
BALANCE SHEET OF INNOVATETECH SOLUTIONS PRIVATE LIMITED
AS ON 31ST MARCH 2024

I. EQUITY AND LIABILITIES
1. Shareholders' Funds
   (a) Share Capital: Rs. 500,000
   (b) Reserves and Surplus: Rs. 1,200,000
   Total Equity: Rs. 1,700,000

2. Non-Current & Current Liabilities
   (a) Trade Payables: Rs. 300,000
   (b) Short Term Provisions: Rs. 150,000
   Total Liabilities: Rs. 450,000

TOTAL EQUITY AND LIABILITIES: Rs. 2,150,000

II. ASSETS
1. Non-Current Assets
   (a) Property, Plant & Equipment: Rs. 800,000
2. Current Assets
   (a) Trade Receivables: Rs. 500,000
   (b) Cash and Bank Balances: Rs. 750,000
   
TOTAL ASSETS: Rs. 2,050,000

ATTESTATION & SIGNATURE:
Director DIN: 08123456
Director DIN: 09876543
Place: Bengaluru
Date: 05-09-2024
Sd/- Rajesh Kumar (Managing Director)
`;

export default function AuditValidator({ onScan }) {
  const [docType, setDocType] = useState('Financial Statement / Balance Sheet (AOC-4)');
  const [file, setFile] = useState(null);
  const [useSample, setUseSample] = useState(false);
  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState(null);

  const handleScanSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('doc_type', docType);

      if (file) {
        formData.append('file', file);
      } else if (useSample) {
        formData.append('text_content', SAMPLE_BALANCE_SHEET_TEXT);
      } else {
        alert('Please upload a file or check the sample text box.');
        setLoading(false);
        return;
      }

      const res = await onScan(formData);
      setAuditResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatFieldValue = (val) => {
    if (val === null || val === undefined) {
      return <span className="text-slate-500 font-semibold italic text-xs">Not Specified</span>;
    }
    if (typeof val === 'number') {
      return <span className="text-sky-300 font-extrabold text-sm">₹{val.toLocaleString('en-IN')}</span>;
    }
    return <span className="text-slate-200 font-bold text-xs">{val}</span>;
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="glass-card rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">Audit-Ready Pre-Submission Rules Engine</h2>
            <p className="text-xs text-slate-400 mt-1">
              Upload draft financial statements or board resolutions prior to MCA portal filing to catch balance sheet discrepancies, missing director signatures, and SS-1 errors.
            </p>
          </div>
        </div>
      </div>

      {/* Form & Upload */}
      <div className="glass-panel rounded-2xl p-6">
        <form onSubmit={handleScanSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-2">Select Document Type</label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                'Financial Statement / Balance Sheet (AOC-4)',
                'Board Resolution (SS-1 Compliance)',
                'Annual Return (MGT-7)'
              ].map((t) => (
                <button
                  type="button"
                  key={t}
                  onClick={() => setDocType(t)}
                  className={`p-3 rounded-xl text-xs font-semibold text-left transition border ${
                    docType === t
                      ? 'bg-sky-500/20 border-sky-500 text-sky-300'
                      : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* File Upload Box */}
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-2">Upload Document File (PDF / Text)</label>
            <div className="border-2 border-dashed border-slate-800 hover:border-sky-500/50 rounded-2xl p-8 text-center bg-slate-950/50 transition">
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => {
                  setFile(e.target.files[0]);
                  setUseSample(false);
                }}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center gap-2">
                <Upload className="h-8 w-8 text-sky-400" />
                <span className="text-xs font-semibold text-slate-200">
                  {file ? file.name : 'Click to upload PDF or text document'}
                </span>
                <span className="text-[10px] text-slate-500">Supports PDF, TXT (Max 10MB)</span>
              </label>
            </div>
          </div>

          {/* Sample Checkbox */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="sample-check"
              checked={useSample}
              onChange={(e) => {
                setUseSample(e.target.checked);
                if (e.target.checked) setFile(null);
              }}
              className="rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0 cursor-pointer"
            />
            <label htmlFor="sample-check" className="text-xs font-medium text-slate-300 cursor-pointer">
              Or test with sample Balance Sheet containing intentional math discrepancy
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center justify-center gap-2"
          >
            {loading ? (
              <span>Scanning Document Rules Engine...</span>
            ) : (
              <>
                <FileCheck className="h-4 w-4" />
                <span>Run Pre-Submission Audit Scan</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Audit Scan Results */}
      {auditResult && (
        <div className="space-y-6">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <FileText className="h-5 w-5 text-sky-400" />
            Audit Scan Verification Report
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-card rounded-2xl p-5 text-center">
              <p className="text-xs font-semibold text-slate-400">Audit Readiness Score</p>
              <h4 className={`text-3xl font-extrabold mt-2 ${
                auditResult.score >= 80 ? 'text-emerald-400' : 'text-rose-400'
              }`}>
                {auditResult.score}/100
              </h4>
            </div>

            <div className="glass-card rounded-2xl p-5 text-center">
              <p className="text-xs font-semibold text-slate-400">Validation Status</p>
              <div className="mt-2">
                {auditResult.is_valid ? (
                  <span className="inline-flex items-center gap-1.5 px-3.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-extrabold text-xs rounded-full">
                    <CheckCircle2 className="h-4 w-4" /> AUDIT READY
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5 px-3.5 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/30 font-extrabold text-xs rounded-full">
                    <AlertOctagon className="h-4 w-4" /> REJECTION RISK
                  </span>
                )}
              </div>
            </div>

            <div className="glass-card rounded-2xl p-5 text-center">
              <p className="text-xs font-semibold text-slate-400">Issues Detected</p>
              <h4 className="text-3xl font-extrabold text-slate-100 mt-2">
                {auditResult.discrepancies?.length || 0}
              </h4>
            </div>
          </div>

          {/* Premium Extracted Financial & Governance Grid */}
          {auditResult.extracted_data && (
            <div className="glass-panel rounded-2xl p-6 space-y-4 border border-slate-800">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-extrabold text-sky-400 uppercase tracking-wider flex items-center gap-2">
                  <Scale className="h-4 w-4 text-sky-400" />
                  Extracted Financial & Governance Indicators
                </h4>
                <span className="text-[11px] font-semibold text-slate-400 bg-slate-900 border border-slate-800 px-2.5 py-0.5 rounded-full">
                  Schedule III Audit Parse
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.entries(auditResult.extracted_data).map(([key, val]) => (
                  <div key={key} className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-1.5 transition hover:border-slate-700">
                    <div className="flex items-center gap-2">
                      {key.includes('Assets') ? (
                        <Coins className="h-4 w-4 text-emerald-400 shrink-0" />
                      ) : key.includes('Liabilities') ? (
                        <Wallet className="h-4 w-4 text-rose-400 shrink-0" />
                      ) : (
                        <FileText className="h-4 w-4 text-indigo-400 shrink-0" />
                      )}
                      <span className="text-xs font-bold text-slate-300 truncate">{key}</span>
                    </div>
                    <div>
                      {formatFieldValue(val)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Discrepancies Breakdown */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-300">Detailed Rule Discrepancy Breakdown</h4>
            {auditResult.discrepancies?.length === 0 ? (
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" /> Zero discrepancies detected! Document is 100% Audit-Ready for MCA submission.
              </div>
            ) : (
              auditResult.discrepancies?.map((d, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-xl border text-xs space-y-1.5 ${
                    d.severity === 'CRITICAL'
                      ? 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                      : d.severity === 'HIGH'
                      ? 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                      : 'bg-sky-500/10 border-sky-500/30 text-sky-300'
                  }`}
                >
                  <div className="flex items-center gap-2 font-extrabold uppercase tracking-wider text-[10px]">
                    <AlertTriangle className="h-4 w-4 shrink-0" />
                    <span>[{d.severity}] {d.rule}</span>
                  </div>
                  <p className="font-semibold text-slate-100">{d.description}</p>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
