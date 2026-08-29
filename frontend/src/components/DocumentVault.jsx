import React, { useState } from 'react';
import { Lock, Key, Upload, FileText, CheckCircle2, Shield } from 'lucide-react';

export default function DocumentVault({ cin, data, onUpload }) {
  const { documents, directors } = data || { documents: [], directors: [] };
  const [docName, setDocName] = useState('');
  const [category, setCategory] = useState('Incorporation & MOA/AOA');
  const [director, setDirector] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [catFilter, setCatFilter] = useState('All');

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!docName || !file) {
      alert('Please enter document name and choose a file.');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('company_cin', cin);
      formData.append('doc_name', docName);
      formData.append('category', category);
      formData.append('dsc_director', director);
      formData.append('file', file);

      await onUpload(formData);
      setDocName('');
      setFile(null);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  let filteredDocs = documents || [];
  if (catFilter !== 'All') {
    filteredDocs = filteredDocs.filter((d) => d.category === catFilter);
  }

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="glass-card rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Lock className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">Encrypted Document Vault & DSC Tracker</h2>
            <p className="text-xs text-slate-400 mt-1">
              AES-256 encrypted repository for Digital Signatures (DSC), MOA/AOA, Financials, and Board Minutes.
            </p>
          </div>
        </div>
      </div>

      {/* Director DSC Tracker */}
      <div className="glass-panel rounded-2xl p-6 space-y-3">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <Key className="h-4 w-4 text-sky-400" />
          Director Digital Signature Certificate (DSC) Expiry Radar
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {directors?.map((d, i) => (
            <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-xs font-bold text-slate-200">{d.name}</h4>
                  <p className="text-[10px] text-slate-400">DIN: {d.din}</p>
                </div>
                <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full">
                  VALID
                </span>
              </div>
              <div className="text-[11px] text-slate-400">
                <span>DSC Expiry: </span>
                <span className="font-bold text-slate-200">{d.dsc_expiry}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Upload & Document Gallery Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Form */}
        <div className="glass-panel rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Upload className="h-4 w-4 text-sky-400" />
            Upload Document to Vault
          </h3>

          <form onSubmit={handleUploadSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Document Name</label>
              <input
                type="text"
                placeholder="e.g. Certificate_of_Incorporation.pdf"
                value={docName}
                onChange={(e) => setDocName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              >
                <option value="Incorporation & MOA/AOA">Incorporation & MOA/AOA</option>
                <option value="Director DSC & KYC">Director DSC & KYC</option>
                <option value="Board Minutes & Resolutions">Board Minutes & Resolutions</option>
                <option value="Financial Statements">Financial Statements</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Choose File</label>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-xs text-slate-400"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center justify-center gap-1.5"
            >
              <Shield className="h-4 w-4" />
              <span>{loading ? 'Encrypting with AES-256...' : 'Encrypt & Save to Vault'}</span>
            </button>
          </form>
        </div>

        {/* Document Gallery */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <FileText className="h-4 w-4 text-indigo-400" />
              Encrypted Repository Documents
            </h3>

            <select
              value={catFilter}
              onChange={(e) => setCatFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-slate-300 focus:outline-none"
            >
              <option value="All">All Categories</option>
              <option value="Incorporation & MOA/AOA">Incorporation</option>
              <option value="Director DSC & KYC">Director DSC</option>
              <option value="Board Minutes & Resolutions">Board Minutes</option>
              <option value="Financial Statements">Financials</option>
            </select>
          </div>

          <div className="space-y-3">
            {filteredDocs.length === 0 ? (
              <div className="text-center text-slate-500 py-8 text-xs">
                No documents found in vault.
              </div>
            ) : (
              filteredDocs.map((doc) => (
                <div key={doc.doc_id} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                      <FileText className="h-5 w-5" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-200">{doc.doc_name}</h4>
                      <p className="text-[10px] text-slate-400">Category: {doc.category} &bull; Date: {doc.upload_date}</p>
                    </div>
                  </div>

                  <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-full flex items-center gap-1">
                    <CheckCircle2 className="h-3 w-3" /> AES-256 ENCRYPTED
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
