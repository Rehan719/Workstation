import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Shield, BarChart3, FileText, Leaf, Calendar, AlertTriangle,
  Loader2, CheckCircle2, ChevronDown, ChevronUp, Plus, Download,
  type LucideIcon
} from 'lucide-react';

// ── Types ────────────────────────────────────────────────────────────────────

interface Standard { id: string; name: string; type: string; description: string }

type Tab = 'qms' | 'bms' | 'dcs' | 'ems' | 'audit' | 'risk';

const TABS: { id: Tab; label: string; icon: LucideIcon; color: string; endpoint: string }[] = [
  { id: 'qms',   label: 'QMS (ISO 9001)',   icon: Shield,        color: 'text-blue-400',   endpoint: '/api/v1/mgmt/qms/generate'    },
  { id: 'bms',   label: 'BMS / OKRs',       icon: BarChart3,     color: 'text-green-400',  endpoint: '/api/v1/mgmt/bms/generate'    },
  { id: 'dcs',   label: 'Document Control',  icon: FileText,      color: 'text-purple-400', endpoint: '/api/v1/mgmt/dcs/generate'    },
  { id: 'ems',   label: 'EMS (ISO 14001)',   icon: Leaf,          color: 'text-emerald-400',endpoint: '/api/v1/mgmt/ems/generate'    },
  { id: 'audit', label: 'Audit Schedule',    icon: Calendar,      color: 'text-yellow-400', endpoint: '/api/v1/mgmt/audit/schedule'  },
  { id: 'risk',  label: 'Risk Register',     icon: AlertTriangle, color: 'text-red-400',    endpoint: '/api/v1/mgmt/risk-register'   },
];

// ── Shared form field component ───────────────────────────────────────────────

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs text-white/50 font-mono uppercase tracking-wider">{label}</label>
      {children}
    </div>
  );
}

function Input({ value, onChange, placeholder }: { value: string; onChange: (v: string) => void; placeholder?: string }) {
  return (
    <input
      value={value} onChange={e => onChange(e.target.value)}
      placeholder={placeholder}
      className="bg-white/5 border border-white/15 rounded-lg px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-white/30"
    />
  );
}

function Select({ value, onChange, options }: { value: string; onChange: (v: string) => void; options: {value:string;label:string}[] }) {
  return (
    <select
      value={value} onChange={e => onChange(e.target.value)}
      className="bg-white/5 border border-white/15 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-white/30"
    >
      {options.map(o => <option key={o.value} value={o.value} className="bg-slate-900">{o.label}</option>)}
    </select>
  );
}

// ── Result display ────────────────────────────────────────────────────────────

function ResultPanel({ result, expanded, onToggle }: { result: string; expanded: boolean; onToggle: () => void }) {
  const download = () => {
    const blob = new Blob([result], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'management_framework.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white/3 border border-white/10 rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-white/5" onClick={onToggle}>
        <div className="flex items-center gap-2 text-sm text-green-400 font-semibold">
          <CheckCircle2 size={15} />
          Framework Generated
        </div>
        <div className="flex items-center gap-2">
          <button onClick={e => { e.stopPropagation(); download(); }} className="p-1.5 rounded hover:bg-white/10 text-white/40 hover:text-white/70">
            <Download size={13} />
          </button>
          {expanded ? <ChevronUp size={15} className="text-white/40" /> : <ChevronDown size={15} className="text-white/40" />}
        </div>
      </div>
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0 }} animate={{ height: 'auto' }} exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 max-h-96 overflow-y-auto">
              <pre className="text-xs text-white/70 font-mono whitespace-pre-wrap leading-relaxed">{result}</pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// ── Tab panels ────────────────────────────────────────────────────────────────

const DOMAIN_OPTIONS = [
  { value: 'general', label: 'General' },
  { value: 'technology', label: 'Technology' },
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'finance', label: 'Finance' },
  { value: 'education', label: 'Education' },
  { value: 'legal', label: 'Legal' },
  { value: 'manufacturing', label: 'Manufacturing' },
];

function QMSPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [domain, setDomain] = useState('general');
  const [size, setSize] = useState('small');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/qms/generate', { organisation_name: org, domain, size });
      onResult(res.data.framework);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate an ISO 9001:2015-aligned Quality Management System with policies, objectives, process maps, audit programme, and certification checklist.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="Acme Ltd" /></Field>
        <Field label="Domain"><Select value={domain} onChange={setDomain} options={DOMAIN_OPTIONS} /></Field>
        <Field label="Size"><Select value={size} onChange={setSize} options={[{value:'micro',label:'Micro'},{value:'small',label:'Small'},{value:'medium',label:'Medium'},{value:'large',label:'Large'}]} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600/30 hover:bg-blue-600/50 text-blue-300 border border-blue-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate QMS Framework
      </button>
    </div>
  );
}

function BMSPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [mission, setMission] = useState('');
  const [domain, setDomain] = useState('general');
  const [horizon, setHorizon] = useState('annual');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim() || !mission.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/bms/generate', { organisation_name: org, mission, domain, planning_horizon: horizon });
      onResult(res.data.framework);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate a Balanced Scorecard and OKR framework with strategic map, performance review cadence, and decision rights matrix.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="Acme Ltd" /></Field>
        <Field label="Mission Statement"><Input value={mission} onChange={setMission} placeholder="To transform X by Y..." /></Field>
        <Field label="Domain"><Select value={domain} onChange={setDomain} options={DOMAIN_OPTIONS} /></Field>
        <Field label="Planning Horizon"><Select value={horizon} onChange={setHorizon} options={[{value:'quarterly',label:'Quarterly'},{value:'annual',label:'Annual'},{value:'3-year',label:'3 Year'}]} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim() || !mission.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-green-600/30 hover:bg-green-600/50 text-green-300 border border-green-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate BMS / OKRs
      </button>
    </div>
  );
}

function DCSPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [domain, setDomain] = useState('general');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/dcs/generate', { organisation_name: org, domain });
      onResult(res.data.framework);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate a Document Control System with taxonomy, naming conventions, version control protocol, approval workflow, and retention schedule.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="Acme Ltd" /></Field>
        <Field label="Domain"><Select value={domain} onChange={setDomain} options={DOMAIN_OPTIONS} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600/30 hover:bg-purple-600/50 text-purple-300 border border-purple-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate DCS Framework
      </button>
    </div>
  );
}

function EMSPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [domain, setDomain] = useState('general');
  const [sector, setSector] = useState('services');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/ems/generate', { organisation_name: org, domain, sector });
      onResult(res.data.framework);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate an ISO 14001:2015-aligned Environmental Management System with aspects register, legal register, objectives, energy plan, and carbon methodology.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="GreenTech Ltd" /></Field>
        <Field label="Domain"><Select value={domain} onChange={setDomain} options={DOMAIN_OPTIONS} /></Field>
        <Field label="Sector"><Select value={sector} onChange={setSector} options={[{value:'services',label:'Services'},{value:'technology',label:'Technology'},{value:'manufacturing',label:'Manufacturing'},{value:'healthcare',label:'Healthcare'}]} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 border border-emerald-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate EMS Framework
      </button>
    </div>
  );
}

function AuditPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [standard, setStandard] = useState('ISO 9001');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/audit/schedule', { organisation_name: org, audit_standard: standard, year: new Date().getFullYear() });
      onResult(res.data.schedule);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate a risk-based internal audit programme with risk assessment matrix, annual schedule, audit methodology, and NC tracking process.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="Acme Ltd" /></Field>
        <Field label="Standard"><Select value={standard} onChange={setStandard} options={[{value:'ISO 9001',label:'ISO 9001'},{value:'ISO 14001',label:'ISO 14001'},{value:'ISO 27001',label:'ISO 27001'},{value:'ISO 45001',label:'ISO 45001'}]} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-yellow-600/30 hover:bg-yellow-600/50 text-yellow-300 border border-yellow-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate Audit Schedule
      </button>
    </div>
  );
}

function RiskPanel({ onResult }: { onResult: (r: string) => void }) {
  const [org, setOrg] = useState('');
  const [domain, setDomain] = useState('general');
  const [context, setContext] = useState('');
  const [numRisks, setNumRisks] = useState('10');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!org.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/v1/mgmt/risk-register', { organisation_name: org, domain, context, num_risks: parseInt(numRisks) });
      onResult(res.data.register);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">Generate a comprehensive risk register covering strategic, operational, financial, legal, reputational, technology, people, and environmental risks.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Field label="Organisation Name"><Input value={org} onChange={setOrg} placeholder="Acme Ltd" /></Field>
        <Field label="Domain"><Select value={domain} onChange={setDomain} options={DOMAIN_OPTIONS} /></Field>
        <Field label="Context (optional)"><Input value={context} onChange={setContext} placeholder="Key business context..." /></Field>
        <Field label="Number of Risks"><Select value={numRisks} onChange={setNumRisks} options={['5','8','10','15','20'].map(v=>({value:v,label:`${v} risks`}))} /></Field>
      </div>
      <button onClick={generate} disabled={loading || !org.trim()} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-600/30 hover:bg-red-600/50 text-red-300 border border-red-500/30 font-semibold text-sm disabled:opacity-50">
        {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
        Generate Risk Register
      </button>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export const ManagementSystemsHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('qms');
  const [standards, setStandards] = useState<Standard[]>([]);
  const [result, setResult] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    axios.get('/api/v1/mgmt/standards').then(r => setStandards(r.data.standards ?? [])).catch(() => {});
  }, []);

  const handleResult = (r: string) => {
    setResult(r);
    setExpanded(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const current = TABS.find(t => t.id === activeTab)!;

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
          <Shield size={22} className="text-blue-400" />
          Management Systems Hub
        </h1>
        <p className="text-sm text-white/40 mt-1">ISO 9001 · ISO 14001 · Balanced Scorecard · OKRs · Audit · Risk — AI-generated, immediately usable</p>
      </div>

      {/* Standards chips */}
      {standards.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {standards.map(s => (
            <span key={s.id} className="px-2 py-0.5 rounded text-xs font-mono bg-white/5 border border-white/10 text-white/50">
              {s.name}
            </span>
          ))}
        </div>
      )}

      {/* Result panel */}
      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
            <ResultPanel result={result} expanded={expanded} onToggle={() => setExpanded(e => !e)} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Tab bar */}
      <div className="flex flex-wrap gap-2">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => { setActiveTab(tab.id); setResult(null); }}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold border transition-all ${
              activeTab === tab.id
                ? 'bg-white/10 border-white/20 text-white'
                : 'bg-white/3 border-white/8 text-white/40 hover:text-white/70 hover:bg-white/5'
            }`}
          >
            <tab.icon size={14} className={activeTab === tab.id ? tab.color : ''} />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Active panel */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/5 border border-white/10 rounded-2xl p-6"
      >
        <div className="flex items-center gap-2 mb-5">
          <current.icon size={18} className={current.color} />
          <h2 className="text-white font-bold">{current.label}</h2>
        </div>
        {activeTab === 'qms'   && <QMSPanel   onResult={handleResult} />}
        {activeTab === 'bms'   && <BMSPanel   onResult={handleResult} />}
        {activeTab === 'dcs'   && <DCSPanel   onResult={handleResult} />}
        {activeTab === 'ems'   && <EMSPanel   onResult={handleResult} />}
        {activeTab === 'audit' && <AuditPanel onResult={handleResult} />}
        {activeTab === 'risk'  && <RiskPanel  onResult={handleResult} />}
      </motion.div>
    </div>
  );
};

export default ManagementSystemsHub;
