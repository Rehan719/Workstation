/**
 * W444 — the QEP intelligence layer's first surface.
 *
 * The four ops here were rebuilt honestly in W439 (real SM-2 XAI, parsed-or-null fidelity,
 * tri-state compliance verdict, sum-to-1 weight gate) — and then never rendered anywhere, so
 * the class-kills had no witness. This panel shows them verbatim:
 *   • XAI: the REAL MemorizationEngine's next-review computation with display-weight
 *     attribution, the basis lines shown prominently (they are the honesty).
 *   • Recommendation weights: owner-tunable, live sum readout, the 422 contract shown verbatim.
 *   • Adaptation registry + execute: blueprints recorded, never "installed"; fidelity is the
 *     model's self-declared figure or "unmeasured" — never a flattering constant.
 *   • Compliance audit: green only on true, red on false, amber "NOT ESTABLISHED" on null —
 *     never a green badge over controls that did not run.
 */
import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Brain, Loader2, AlertCircle, ShieldCheck, GitBranch, Scale } from 'lucide-react';

const Chip: React.FC<{ tone: 'ok' | 'warn' | 'bad' | 'dim'; children: React.ReactNode; title?: string }> = ({ tone, children, title }) => (
  <span title={title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${
    tone === 'ok' ? 'bg-emerald-500/15 text-emerald-400'
    : tone === 'warn' ? 'bg-amber-500/20 text-amber-400'
    : tone === 'bad' ? 'bg-vital/15 text-vital' : 'bg-slate-800 text-slate-400'}`}>{children}</span>
);

const QEPIntelligence: React.FC = () => {
  const [xaiIn, setXaiIn] = useState({ ease_factor: 2.5, interval_days: 6, repetition: 3, last_quality: 4 });
  const [xai, setXai] = useState<any>(null);
  const [weights, setWeights] = useState({ ease_weight: 0.4, interval_weight: 0.35, quality_weight: 0.25 });
  const [reg, setReg] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [adapt, setAdapt] = useState({ pattern: '', source_domain: 'religion', target_domain: 'science' });
  const [blueprint, setBlueprint] = useState<any>(null);
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');
  const [loadErr, setLoadErr] = useState('');

  const jget = (url: string) => fetch(url).then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); });
  const loadAll = () => {
    setLoadErr('');
    jget('/api/v1/qep/adaptation/registry').then(setReg).catch(() => setLoadErr('registry unavailable'));
    jget('/api/v1/qep/compliance/audit').then(setAudit).catch(() => setLoadErr(e => e ? `${e} · audit unavailable` : 'audit unavailable'));
  };
  useEffect(() => { loadAll(); }, []);

  const explain = async () => {
    setBusy('xai'); setErr('');
    try {
      const q = new URLSearchParams(Object.entries(xaiIn).map(([k, v]) => [k, String(v)]));
      const r = await fetch(`/api/v1/qep/xai/explanations?${q}`);
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : JSON.stringify(d.detail).slice(0, 200)); setBusy(''); return; }
      setXai(d);
      setWeights({ ease_weight: d.model_weights.ease_weight, interval_weight: d.model_weights.interval_weight, quality_weight: d.model_weights.quality_weight });
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy('');
  };

  const saveWeights = async () => {
    setBusy('weights'); setErr(''); setMsg('');
    try {
      const r = await fetch('/api/v1/qep/recommendation/update', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(weights),
      });
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setBusy(''); return; }
      setMsg('Weights persisted — they feed the XAI attributions and the compliance audit\'s normalisation check.');
      loadAll();
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy('');
  };

  const runAdapt = async () => {
    setBusy('adapt'); setErr(''); setBlueprint(null);
    try {
      const r = await fetch('/api/v1/qep/adaptation/execute', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(adapt),
      });
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setBusy(''); return; }
      setBlueprint(d);
      loadAll();
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy('');
  };

  const wSum = weights.ease_weight + weights.interval_weight + weights.quality_weight;

  return (
    <div className="space-y-6">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-1">QEP · Intelligence layer</p>
        <h2 className="text-2xl font-black tracking-tight text-white uppercase italic">Explainability · Adaptation · Compliance</h2>
        {loadErr && <p role="alert" className="text-[10px] font-bold text-vital mt-2">{loadErr} — showing nothing rather than stale figures</p>}
      </header>

      {/* XAI */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-1"><Brain size={13} /> Explain SM-2 scheduling (XAI)</h3>
        <p className="text-[9px] text-slate-600 mb-3">Why would the hifz engine schedule a review this way? Computed by the REAL MemorizationEngine over the inputs below.</p>
        <div className="flex flex-wrap items-end gap-2 mb-3">
          {([['ease_factor', 'ease (1.3–3.0)'], ['interval_days', 'interval (days)'], ['repetition', 'repetitions'], ['last_quality', 'quality (0–5)']] as const).map(([k, label]) => (
            <div key={k}>
              <label className="text-[8px] font-black uppercase tracking-widest text-slate-600 block mb-1">{label}</label>
              <input type="number" step={k === 'ease_factor' ? 0.1 : 1} value={(xaiIn as any)[k]}
                onChange={e => setXaiIn({ ...xaiIn, [k]: Number(e.target.value) })}
                aria-label={k}
                className="w-24 bg-slate-900 border border-slate-800 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-highlight/50" />
            </div>
          ))}
          <Button onClick={explain} disabled={busy === 'xai'} className="flex items-center gap-1.5 bg-highlight text-sovereign text-[10px]">
            {busy === 'xai' ? <Loader2 size={12} className="animate-spin" /> : <Brain size={12} />} Explain
          </Button>
        </div>
        {xai && (
          <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
            <p className="text-sm font-black text-white">
              {xai.decision === 'advance' ? 'ADVANCE' : 'RESET'} → next review in {xai.next_interval_days} day(s)
              <span className="text-[9px] text-slate-500"> · new efactor {xai.new_efactor}</span>
            </p>
            <p className="text-[9px] text-emerald-400 mt-0.5">{xai.interval_basis}</p>
            <div className="space-y-1 mt-2">
              {(xai.explanations || []).map((c: any) => (
                <div key={c.feature} className="flex items-center justify-between gap-2 text-[10px]">
                  <span className="font-mono text-slate-400">{c.feature} = {c.value}</span>
                  <span className="text-slate-500 flex-1 px-2 truncate" title={c.rationale}>{c.rationale}</span>
                  <span className="font-mono text-slate-300">+{c.contribution}</span>
                </div>
              ))}
            </div>
            <p className="text-[9px] text-amber-400/80 italic mt-2">{xai.explanations_basis}</p>
          </div>
        )}
      </Card>

      {/* Recommendation weights */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-1"><Scale size={13} /> Recommendation model weights</h3>
        <p className="text-[9px] text-slate-600 mb-3">The persisted display-attribution weights. They must sum to ~1.0 — the compliance audit grades exactly this contract.</p>
        <div className="flex flex-wrap items-end gap-2">
          {(['ease_weight', 'interval_weight', 'quality_weight'] as const).map(k => (
            <div key={k}>
              <label className="text-[8px] font-black uppercase tracking-widest text-slate-600 block mb-1">{k.replace('_', ' ')}</label>
              <input type="number" step={0.05} min={0} max={1} value={(weights as any)[k]}
                onChange={e => setWeights({ ...weights, [k]: Number(e.target.value) })}
                aria-label={k}
                className="w-24 bg-slate-900 border border-slate-800 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-highlight/50" />
            </div>
          ))}
          <span className={`text-[10px] font-black uppercase tracking-widest ${Math.abs(wSum - 1.0) < 0.05 ? 'text-emerald-400' : 'text-amber-400'}`}>sum {wSum.toFixed(2)}</span>
          <Button onClick={saveWeights} disabled={busy === 'weights'} className="flex items-center gap-1.5 bg-slate-800 text-white text-[10px]">
            {busy === 'weights' ? <Loader2 size={12} className="animate-spin" /> : <ShieldCheck size={12} />} Save weights
          </Button>
        </div>
        {msg && <p className="text-emerald-400 text-[10px] font-bold mt-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {msg}</p>}
      </Card>

      {/* Adaptation registry + execute */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-1"><GitBranch size={13} /> Cross-domain adaptation registry</h3>
        <p className="text-[9px] text-slate-600 mb-3">Pedagogical patterns adapted between domains. A registered adaptation is a recorded BLUEPRINT — nothing is installed or activated; fidelity is the model's self-declared figure, or unmeasured.</p>
        <div className="space-y-1.5 mb-4">
          {(reg?.adaptations ?? []).map((a: any) => (
            <div key={a.id} className="flex items-center justify-between gap-2 p-2 rounded-lg bg-slate-950 border border-slate-900 text-[10px]">
              <span className="text-slate-300 font-bold truncate">{a.pattern}<span className="text-slate-600 font-mono"> · {a.from} → {a.to}</span></span>
              <div className="flex items-center gap-1.5 shrink-0">
                <Chip tone="dim">{a.status}</Chip>
                {a.served_by != null && <Chip tone={a.served_by === 'native' ? 'warn' : 'ok'}>{a.served_by === 'native' ? 'floor-served' : `served by ${a.served_by}`}</Chip>}
                {typeof a.fidelity === 'number' && a.served_by != null && a.served_by !== 'native'
                  ? <span className="font-mono text-slate-400" title="model self-declared — not independently measured">fidelity {a.fidelity}</span>
                  : <Chip tone="dim" title={a.fidelity_note || 'no measured fidelity exists'}>unmeasured</Chip>}
              </div>
            </div>
          ))}
          {reg && (reg.adaptations?.length ?? 0) === 0 && <p className="text-[10px] text-slate-600 italic">no adaptations recorded</p>}
        </div>
        <div className="flex flex-wrap items-end gap-2">
          <div className="flex-1 min-w-[180px]">
            <label className="text-[8px] font-black uppercase tracking-widest text-slate-600 block mb-1">pattern to adapt</label>
            <input value={adapt.pattern} onChange={e => setAdapt({ ...adapt, pattern: e.target.value })}
              aria-label="adaptation pattern" placeholder="e.g. spaced repetition with mastery gates"
              className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-highlight/50" />
          </div>
          {(['source_domain', 'target_domain'] as const).map(k => (
            <div key={k}>
              <label className="text-[8px] font-black uppercase tracking-widest text-slate-600 block mb-1">{k.replace('_', ' ')}</label>
              <select value={(adapt as any)[k]} onChange={e => setAdapt({ ...adapt, [k]: e.target.value })}
                aria-label={k}
                className="text-xs bg-slate-900 border border-slate-800 rounded-lg px-2 py-2 text-white focus:outline-none focus:border-highlight/50">
                {['religion', 'science', 'care', 'education', 'law', 'enterprise'].map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
          ))}
          <Button onClick={runAdapt} disabled={busy === 'adapt' || !adapt.pattern.trim()} className="flex items-center gap-1.5 bg-highlight text-sovereign text-[10px]">
            {busy === 'adapt' ? <Loader2 size={12} className="animate-spin" /> : <GitBranch size={12} />} Generate blueprint
          </Button>
        </div>
        {blueprint && (
          <div className="mt-3 p-3 rounded-xl bg-slate-950 border border-slate-900">
            <div className="flex items-center gap-1.5 mb-1.5">
              <Chip tone="dim">{blueprint.status}</Chip>
              {blueprint.adaptation?.served_by && (
                <Chip tone={blueprint.adaptation.served_by === 'native' ? 'warn' : 'ok'}>
                  {blueprint.adaptation.served_by === 'native' ? 'outline-grade — floor-served, not model analysis' : `served by ${blueprint.adaptation.served_by}`}
                </Chip>
              )}
              <span className="text-[9px] text-slate-500">fidelity: {typeof blueprint.adaptation?.fidelity === 'number' ? `${blueprint.adaptation.fidelity} (model self-declared)` : 'none parsed → unmeasured'}</span>
            </div>
            <pre className="text-[10px] text-slate-300 whitespace-pre-wrap max-h-56 overflow-y-auto">{blueprint.blueprint}</pre>
            <p className="text-[9px] text-amber-400/80 italic mt-1.5">{blueprint.status_note}</p>
          </div>
        )}
      </Card>

      {/* Compliance audit */}
      <Card className="p-5">
        <div className="flex items-center justify-between gap-3 flex-wrap mb-2">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><ShieldCheck size={13} /> Compliance audit</h3>
          {audit && (
            <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${
              audit.compliant === true ? 'bg-emerald-500/15 text-emerald-400'
              : audit.compliant === false ? 'bg-vital/15 text-vital'
              : 'bg-amber-500/20 text-amber-400'}`}>
              {audit.compliant === true ? 'compliant' : audit.compliant === false ? 'NOT compliant' : 'NOT ESTABLISHED — controls could not run'}
            </span>
          )}
        </div>
        <div className="space-y-1.5">
          {(audit?.checks ?? []).map((c: any) => (
            <div key={c.control} className="flex items-start justify-between gap-2 p-2 rounded-lg bg-slate-950 border border-slate-900 text-[10px]">
              <span className="text-slate-300 font-bold">{c.control}</span>
              <div className="text-right shrink-0 max-w-[55%]">
                <Chip tone={c.status === 'pass' ? 'ok' : c.status === 'review' ? 'bad' : 'warn'}>{c.status}</Chip>
                {c.reason && <p className="text-[9px] text-slate-500 mt-0.5">{c.reason}</p>}
              </div>
            </div>
          ))}
        </div>
        {audit?.note && <p className="text-[9px] text-amber-400/80 italic mt-2">{audit.note}</p>}
      </Card>

      {err && <p role="alert" className="text-vital text-[10px] font-bold flex items-center gap-1.5"><AlertCircle size={12} /> {err}</p>}
    </div>
  );
};

export default QEPIntelligence;
