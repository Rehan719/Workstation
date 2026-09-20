import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { complianceChip } from '../../lib/api';
import { ShieldCheck, Loader2, AlertCircle, CheckCircle2, XCircle, AlertTriangle, Scale, MinusCircle } from 'lucide-react';

interface Verdict { framework: string; status: string; reason: string; coverage?: string; escalate?: string[] }
// W483 — `compliant` is tri-state (null = not established by a screen that cannot clear), and the
// screen states which areas it could and could not assess.
interface Result {
  subject: string; jurisdiction: string; overall: string;
  compliant: boolean | null; verdicts: Verdict[];
  coverage_gaps?: string[]; assessed_by?: string[]; basis?: string;
}

// W455 — two more honest states: not_checked (this row cannot read this kind of subject) and error
// (an engine raised — recorded, never a pass)
const STATUS_ICON: Record<string, React.ComponentType<any>> = { pass: CheckCircle2, review: AlertTriangle, fail: XCircle, not_checked: MinusCircle, error: XCircle };
const STATUS_TONE: Record<string, string> = { pass: 'text-emerald-400', review: 'text-amber-400', fail: 'text-vital', not_checked: 'text-slate-500', error: 'text-vital' };

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
          One federated screen across <span className="text-highlight">Sharia/Halal · UK Legal (London) · Regulatory · EHS · Ethical · Constitutional</span> —
          keyword and vocabulary screens plus engines where one exists. It flags; it does not certify. A pass is a pass of the screen;
          "review — no engine covers this area" means nothing here read the subject. Used by the economy, synthesis, Genesis and the Forge.
        </p>
      </header>

      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-3 flex items-center gap-2"><Scale size={14} /> Frameworks</h3>
        <div className="flex flex-wrap gap-2">
          {/* W455 — each framework says what it actually checks (the card had shown only the names) */}
          {frameworks.map(f => (
            <div key={f.id} className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 max-w-xs" title={f.engine}>
              <p className="text-[10px] font-black uppercase tracking-wider text-slate-400">{f.name}</p>
              <p className="text-[9px] text-slate-500 leading-snug mt-0.5">{f.engine}</p>
            </div>
          ))}
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
          {/* W483 — one rule for every §11 verdict (lib/api.complianceChip). This page kept its own
              colour ternary, so a 'pass' that no framework had assessed rendered full emerald. The
              chip qualifies such a pass and the line below names what could NOT be assessed. */}
          {(() => {
            const _c = complianceChip(result);
            const _assessed = (result.assessed_by ?? []).length > 0;
            return (
              <Card className={`p-5 border ${result.overall === 'fail' ? 'border-vital/40 bg-vital/5' : result.overall === 'review' ? 'border-amber-400/40 bg-amber-400/5' : (result.overall === 'pass' && _assessed) ? 'border-emerald-400/40 bg-emerald-400/5' : 'border-slate-700'}`}>
                <div className="flex items-center gap-3">
                  {result.overall === 'fail' ? <XCircle size={20} className="text-vital" /> : result.overall === 'review' ? <AlertTriangle size={20} className="text-amber-400" /> : (result.overall === 'pass' && _assessed) ? <CheckCircle2 size={20} className="text-emerald-400" /> : <MinusCircle size={20} className="text-slate-500" />}
                  <p className="font-black text-white text-lg uppercase">{result.overall}</p>
                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${_c.cls}`} title={_c.title}>{_c.label}</span>
                  <span className="text-[10px] font-mono text-slate-500 ml-auto">{result.jurisdiction}</span>
                </div>
                <p className="text-[10px] text-slate-400 mt-2 leading-relaxed">
                  {_assessed
                    ? `Assessed by: ${(result.assessed_by ?? []).join(' · ')}.`
                    : 'NOTHING here assessed this subject. A keyword screen can refuse a subject; it cannot clear one.'}
                  {(result.coverage_gaps ?? []).length > 0 &&
                    ` Not assessed: ${(result.coverage_gaps ?? []).join(' · ')}.`}
                </p>
              </Card>
            );
          })()}
          {result.verdicts.map((v, i) => {
            const Icon = STATUS_ICON[v.status] ?? MinusCircle;   // W460 — an unknown status is never a green check
            return (
              <Card key={i} className="p-4">
                <div className="flex items-start gap-3">
                  <Icon size={16} className={`${STATUS_TONE[v.status]} mt-0.5 shrink-0`} />
                  <div>
                    <p className="font-black text-white text-sm uppercase">{v.framework.replace(/_/g, ' ')} <span className={`text-[10px] ${STATUS_TONE[v.status] ?? 'text-slate-500'}`}>· {v.status.replace('_', ' ')}</span>
                      {v.coverage === 'none' && <span className="ml-2 text-[9px] normal-case font-bold text-slate-500">nothing here read this subject</span>}
                    </p>
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
