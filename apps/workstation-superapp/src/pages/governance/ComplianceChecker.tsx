import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { ShieldCheck, Loader2, AlertCircle, CheckCircle2, XCircle, AlertTriangle, Scale } from 'lucide-react';

interface Verdict { framework: string; status: string; reason: string }
interface Result { subject: string; jurisdiction: string; overall: string; compliant: boolean; verdicts: Verdict[] }

const STATUS_ICON: Record<string, React.ComponentType<any>> = { pass: CheckCircle2, review: AlertTriangle, fail: XCircle };
const STATUS_TONE: Record<string, string> = { pass: 'text-emerald-400', review: 'text-amber-400', fail: 'text-vital' };

export const ComplianceChecker: React.FC = () => {
  const [frameworks, setFrameworks] = useState<any[]>([]);
  const [subject, setSubject] = useState('');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<Result | null>(null);

  useEffect(() => { fetch('/api/v1/compliance/frameworks').then(r => r.json()).then(d => setFrameworks(d.frameworks ?? [])).catch(() => {}); }, []);

  const check = async () => {
    if (!subject.trim()) return;
    setRunning(true); setError(''); setResult(null);
    try {
      const r = await fetch('/api/v1/compliance/check', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ subject }) });
      if (!r.ok) { setError(`HTTP ${r.status}`); setRunning(false); return; }
      setResult(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Governance</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Compliance</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          One federated check across <span className="text-highlight">Sharia/Halal · UK Legal (London) · Regulatory · EHS · Ethical · Constitutional</span>.
          Used by the economy, synthesis, Genesis, and the Forge to keep every output halal, lawful, and ethical.
        </p>
      </header>

      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-3 flex items-center gap-2"><Scale size={14} /> Frameworks</h3>
        <div className="flex flex-wrap gap-2">
          {frameworks.map(f => <span key={f.id} className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-[10px] font-black uppercase tracking-wider text-slate-400">{f.name}</span>)}
        </div>
      </Card>

      <Card className="p-8 space-y-5">
        <textarea value={subject} onChange={e => setSubject(e.target.value)} rows={3} placeholder="Describe a product, intent, or content to check — e.g. 'A halal meal-prep subscription'" className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none" />
        <div className="flex items-center gap-4">
          <Button onClick={check} disabled={running || !subject.trim()} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <ShieldCheck size={16} />}
            {running ? 'Checking…' : 'Run Compliance Check'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {result && (
        <div className="space-y-3">
          <Card className={`p-5 border ${result.overall === 'fail' ? 'border-vital/40 bg-vital/5' : result.overall === 'review' ? 'border-amber-400/40 bg-amber-400/5' : 'border-emerald-400/40 bg-emerald-400/5'}`}>
            <div className="flex items-center gap-3">
              {result.overall === 'fail' ? <XCircle size={20} className="text-vital" /> : result.overall === 'review' ? <AlertTriangle size={20} className="text-amber-400" /> : <CheckCircle2 size={20} className="text-emerald-400" />}
              <p className="font-black text-white text-lg uppercase">{result.overall}</p>
              <span className="text-[10px] font-mono text-slate-500 ml-auto">{result.jurisdiction}</span>
            </div>
          </Card>
          {result.verdicts.map((v, i) => {
            const Icon = STATUS_ICON[v.status] ?? CheckCircle2;
            return (
              <Card key={i} className="p-4">
                <div className="flex items-start gap-3">
                  <Icon size={16} className={`${STATUS_TONE[v.status]} mt-0.5 shrink-0`} />
                  <div>
                    <p className="font-black text-white text-sm uppercase">{v.framework.replace(/_/g, ' ')} <span className={`text-[10px] ${STATUS_TONE[v.status]}`}>· {v.status}</span></p>
                    <p className="text-[11px] text-slate-500 mt-0.5">{v.reason}</p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
