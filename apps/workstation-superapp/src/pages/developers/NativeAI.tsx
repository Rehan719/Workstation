import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Cpu, Network, Loader2, CheckCircle2, Circle, ShieldCheck, Server, Globe, Plus, Trash2, Play, Save, Activity } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

interface ModelResource {
  name: string; kind: string; available: boolean; is_external: boolean; model?: string; note?: string;
}
interface Status {
  posture: string; external_allowed: boolean; owned_resources_available: string[];
  selection_order: string[]; guarantee: string; resources: ModelResource[];
  active_model?: string; active_model_label?: string; is_real_model?: boolean;
  mode?: string; floor_active?: boolean; floor_note?: string | null;
}
interface Capability { name: string; endpoint: string; kind: string; source: string; in_house: boolean; description: string }
interface SwarmStep { step: number; role: string; served_by: string; output: string }
interface SwarmRun { agent: string; stages: number; trace: SwarmStep[]; final: string; any_external: boolean }
interface Stage { role: string; instruction: string }
interface TreeNodeDef { id: string; role: string; depends_on: string[] }
interface TreeNodeResult extends TreeNodeDef { served_by: string; is_external: boolean; output: string }
interface TreeGovernance { governed_by: string; qms_passed: boolean; qms_coverage_proxy: number; dcms_hash: string; dcms_algo: string; dcms_version: number }
interface TreeDecision { recommendation: string; consistency: number; worst_case_utility: number; method: string; stressors: string[] }
interface TreeValidation { max_branch_overlap: number; integrated: boolean; branches_checked: number; method: string }
interface TreeConsensus { reached: boolean; choice: string | null; threshold: number; votes: Record<string, string>; proceed_fraction: number; method: string }
interface TreeSignal { input_strength: number; activation: number; supra_threshold: boolean; k50: number; hill: number; basis: string; method: string }
interface TreeRun {
  goal: string; posture: string; tree: TreeNodeDef[]; levels: string[][];
  node_count: number; parallel_levels: number; max_parallel: number; immune_threat: string;
  governance?: TreeGovernance | null; decision?: TreeDecision | null;
  validation?: TreeValidation | null; consensus?: TreeConsensus | null; signal_response?: TreeSignal | null;
  ueg_hash?: string | null; ueg_ledger?: string | null;
  nodes: TreeNodeResult[]; final: string; any_external: boolean;
}
interface SavedCascade { id: string; name: string; stages: Stage[]; usage_area: string; created_at: string }

function kindIcon(kind: string) {
  if (kind === 'native') return Cpu;
  if (kind === 'local') return Server;
  return Globe;
}

function Trace({ run }: { run: SwarmRun }) {
  return (
    <div className="mt-4">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-[9px] font-black uppercase text-slate-400">{run.stages} stages</span>
        <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${run.any_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
          {run.any_external ? 'used external accelerant' : 'fully in-house'}
        </span>
      </div>
      <div className="space-y-2">
        {run.trace.map(s => (
          <div key={s.step} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
            <div className="flex items-center justify-between mb-1">
              <p className="text-xs font-black text-white flex items-center gap-1.5">
                {s.served_by === 'native' ? <CheckCircle2 size={11} className="text-aura" /> : <Circle size={11} className="text-emerald-400" />}
                {s.step}. {s.role}
              </p>
              <span className="text-[8px] font-bold uppercase text-slate-600">served by {s.served_by}</span>
            </div>
            <p className="text-[10px] text-slate-500 whitespace-pre-wrap line-clamp-4">{s.output}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function TreeView({ run }: { run: TreeRun }) {
  const nodes = run.nodes || [];
  const levels = run.levels || [];
  const byId: Record<string, TreeNodeResult> = Object.fromEntries(nodes.map(n => [n.id, n]));
  return (
    <div className="mt-4">
      <div className="flex items-center flex-wrap gap-2 mb-3">
        <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-aura/15 text-aura">{run.node_count ?? nodes.length} nodes</span>
        <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400">{levels.length} levels</span>
        <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400">{run.parallel_levels} parallel · ≤{run.max_parallel}/level</span>
        <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${run.immune_threat === 'NOMINAL' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>immune: {run.immune_threat}</span>
        <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${run.any_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>{run.any_external ? 'used external accelerant' : 'fully in-house'}</span>
      </div>
      {/* dependency levels — nodes in the same level ran in PARALLEL */}
      <div className="space-y-2">
        {levels.map((level, li) => (
          <div key={li} className="flex items-stretch gap-2">
            <span className="text-[8px] font-black uppercase text-slate-600 w-12 shrink-0 pt-2">L{li + 1}{level.length > 1 ? ' ∥' : ''}</span>
            <div className="flex-1 grid gap-2" style={{ gridTemplateColumns: `repeat(${Math.min(level.length, 4)}, minmax(0, 1fr))` }}>
              {level.map(nid => {
                const n = byId[nid];
                if (!n) return null;
                return (
                  <div key={nid} className="p-2.5 rounded-xl bg-slate-950 border border-slate-900">
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <p className="text-[11px] font-black text-white flex items-center gap-1 truncate">
                        {n.served_by === 'native' ? <CheckCircle2 size={10} className="text-aura shrink-0" /> : <Circle size={10} className="text-emerald-400 shrink-0" />}
                        {n.id}
                      </p>
                      <span className="text-[7px] font-bold uppercase text-slate-600 shrink-0">{n.served_by}</span>
                    </div>
                    <p className="text-[8px] font-bold uppercase text-slate-500 mb-1 truncate">{n.role}</p>
                    {n.depends_on.length > 0 && <p className="text-[8px] text-slate-700 mb-1">← {n.depends_on.join(', ')}</p>}
                    <p className="text-[9px] text-slate-500 whitespace-pre-wrap line-clamp-3">{n.output}</p>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      {run.governance && (
        <div className="mt-3 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">VBS governance</span>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${run.governance.qms_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>QMS {run.governance.qms_passed ? 'passed' : 'flagged'}</span>
          <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400">DCMS {run.governance.dcms_algo} v{run.governance.dcms_version}</span>
          <span className="text-[8px] font-mono text-slate-600" title={run.governance.dcms_hash}>{run.governance.dcms_hash.slice(0, 16)}…</span>
        </div>
      )}
      {run.validation && (
        <div className="mt-2 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">Validation</span>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${run.validation.integrated ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>{run.validation.integrated ? 'integrated' : 'near-copy'}</span>
          <span className="text-[8px] font-bold uppercase text-slate-500">max branch overlap {Math.round(run.validation.max_branch_overlap * 100)}% · {run.validation.branches_checked} branches</span>
          <span className="text-[8px] text-slate-600">difflib</span>
        </div>
      )}
      {run.consensus && (
        <div className="mt-2 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">Swarm consensus</span>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${run.consensus.reached && run.consensus.choice === 'proceed' ? 'bg-emerald-500/15 text-emerald-400' : run.consensus.reached ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-500'}`}>{run.consensus.reached ? (run.consensus.choice || 'reached') : 'no consensus'}</span>
          <span className="text-[8px] font-bold uppercase text-slate-500">{Math.round(run.consensus.proceed_fraction * 100)}% proceed · {Object.keys(run.consensus.votes).length} voters · ≥{Math.round(run.consensus.threshold * 100)}%</span>
        </div>
      )}
      {run.decision && (
        <div className="mt-2 p-2.5 rounded-xl bg-highlight/5 border border-highlight/20 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-highlight">Minimax decision</span>
          <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-highlight/15 text-highlight">{run.decision.recommendation}</span>
          <span className="text-[8px] font-bold uppercase text-slate-500">consistency {Math.round(run.decision.consistency * 100)}% · worst-case {run.decision.worst_case_utility}</span>
          <span className="text-[8px] text-slate-600">vs {run.decision.stressors.join(' · ')}</span>
        </div>
      )}
      {run.signal_response && (
        <div className="mt-2 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2" title={run.signal_response.basis}>
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">Biomimetic signal</span>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${run.signal_response.supra_threshold ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500'}`}>{run.signal_response.supra_threshold ? 'supra-threshold' : 'sub-threshold'}</span>
          <span className="text-[8px] font-bold uppercase text-slate-500">activation {Math.round(run.signal_response.activation * 100)}% · K50 {run.signal_response.k50} · Hill {run.signal_response.hill}</span>
          <span className="text-[8px] text-slate-600">Hill transform of consensus strength — nothing timed</span>
        </div>
      )}
      {run.ueg_hash && (
        <div className="mt-2 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">UEG provenance</span>
          <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400">chain-logged</span>
          <span className="text-[8px] text-slate-600">{run.ueg_ledger}</span>
          <span className="text-[8px] font-mono text-slate-600" title={run.ueg_hash}>{run.ueg_hash.slice(0, 16)}…</span>
        </div>
      )}
      {run.final && (
        <div className="mt-3 p-3 rounded-xl bg-aura/5 border border-aura/20">
          <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1">Synthesised result</p>
          <p className="text-[11px] text-slate-300 whitespace-pre-wrap line-clamp-6">{run.final}</p>
        </div>
      )}
    </div>
  );
}

// ── W437 — the Primitive Console: every owned primitive RUNNABLE, honest payload rendered whole ──
// The catalog above this described 10 primitives no page could reach; each was audited (and five
// were FIXED) before this console shipped — see docs/NATIVE_PRIMITIVE_DEFECT_LEDGER.md. The
// renderer is deliberately generic: it shows the FULL response, because the honesty fields
// (basis · tied · population_source · nulls-with-reasons) are the product, not decoration.
interface PrimField { key: string; label: string; kind: 'text' | 'number' | 'select' | 'check'; def: string | number | boolean; options?: string[]; wide?: boolean }
interface PrimDef { id: string; label: string; hint: string; fields: PrimField[]; build: (v: Record<string, string | number | boolean>) => Record<string, unknown> }

const parsePairs = (s: string) => String(s).split(',').map(x => x.trim()).filter(Boolean);
// W437 refuter catches on this console's own parsers: a vote without a colon used to be silently
// DEFAULTED to choice "go" (dissent converted to assent by a constant); a mis-typed population
// silently became NaN → null → the server default. Malformed input is now REFUSED with the entry
// named — the backend's honesty is worthless if the frontend fabricates the request.
const parseVotes = (s: string) => parsePairs(s).map(p => {
  const i = p.indexOf(':');
  const voter = i < 0 ? p.trim() : p.slice(0, i).trim();
  const choice = i < 0 ? '' : p.slice(i + 1).trim();
  if (!voter || !choice) throw new Error(`vote "${p}" is not voter:choice — refusing to guess a ballot`);
  return { voter, choice };
});
const parseCount = (s: string, what: string) => {
  const n = Number(String(s).trim());
  if (!Number.isInteger(n) || n < 0) throw new Error(`${what} "${s}" is not a whole number ≥ 0 — refusing to substitute a default`);
  return n;
};
const parseUtilities = (s: string) => Object.fromEntries(parsePairs(s).map(p => {
  const i = p.indexOf(':');
  const action = i < 0 ? '' : p.slice(0, i).trim();
  const u = Number(p.slice(i + 1).trim());
  if (!action || !Number.isFinite(u)) throw new Error(`utility "${p}" is not action:number`);
  return [action, u];
}));

const PRIMITIVES: PrimDef[] = [
  { id: 'consensus', label: 'Consensus', hint: 'Threshold vote-tally — the strongest clearing choice wins; ties are disclosed, never resolved by input order.',
    fields: [{ key: 'votes', label: 'votes (voter:choice, …)', kind: 'text', def: 'ceo:go, cfo:go, cto:go, cmo:hold', wide: true },
             { key: 'threshold', label: 'threshold (0–1]', kind: 'number', def: 0.66 }],
    build: v => ({ threshold: Number(v.threshold), votes: parseVotes(String(v.votes)) }) },
  { id: 'quorum', label: 'Quorum', hint: 'Density × threshold over the platform\'s defined agent catalog by default (a static definition, not a live observation) — the payload says which population was used.',
    fields: [{ key: 'agents', label: 'population (blank = agent catalog)', kind: 'text', def: '' },
             { key: 'secretion', label: 'secretion / agent', kind: 'number', def: 10 },
             { key: 'threshold', label: 'threshold', kind: 'number', def: 50 }],
    build: v => ({ ...(String(v.agents).trim() === '' ? {} : { agents: parseCount(String(v.agents), 'population') }), secretion: Number(v.secretion), threshold: Number(v.threshold) }) },
  { id: 'decide', label: 'Decide', hint: 'Maximin over per-action utilities you supply. Leave utilities blank and every action ties — NO winner is invented (the default utility cannot tell actions apart).',
    fields: [{ key: 'actions', label: 'actions (comma-separated)', kind: 'text', def: 'proceed, refine, hold', wide: true },
             { key: 'utilities', label: 'per-action utilities (action:u, … — blank = all tie)', kind: 'text', def: 'proceed:0.9, refine:0.8, hold:0.6', wide: true },
             { key: 'base_stability', label: 'base stability', kind: 'number', def: 0.9 }],
    build: v => ({ actions: parsePairs(String(v.actions)), state: { base_stability: Number(v.base_stability) },
                   ...(String(v.utilities).trim() === '' ? {} : { action_utilities: parseUtilities(String(v.utilities)) }) }) },
  { id: 'intent', label: 'Intent', hint: 'Deterministic regex intent classification — all per-intent scores returned.',
    fields: [{ key: 'text', label: 'text', kind: 'text', def: 'build and deploy a halal marketplace app', wide: true }],
    build: v => ({ text: v.text }) },
  { id: 'entailment', label: 'Entailment', hint: 'LEXICAL overlap with the deciding ratio in the payload — a one-sided negation marker with high overlap yields CONTRADICTION (a heuristic; the limits field says what it cannot tell).',
    fields: [{ key: 'premise', label: 'premise', kind: 'text', def: 'the sky is not blue', wide: true },
             { key: 'hypothesis', label: 'hypothesis', kind: 'text', def: 'the sky is blue', wide: true }],
    build: v => ({ premise: v.premise, hypothesis: v.hypothesis }) },
  { id: 'validate', label: 'Validate', hint: 'Reference comparison (difflib / numerical tolerance) — not LLM self-grading.',
    fields: [{ key: 'prediction', label: 'prediction', kind: 'text', def: 'the quick brown fox', wide: true },
             { key: 'actual', label: 'reference', kind: 'text', def: 'the quick brown fox jumps', wide: true },
             { key: 'task_type', label: 'task type', kind: 'select', def: 'SEMANTIC', options: ['SEMANTIC', 'NUMERICAL', 'APP_CODE', 'GENERIC'] }],
    build: v => ({ prediction: v.prediction, actual: v.actual, task_type: v.task_type }) },
  { id: 'rigor', label: 'Rigor', hint: 'Real scipy CI + t-test over the accumulated series — unmeasured stays null with the reason (no fabricated p-values).',
    fields: [{ key: 'metric_name', label: 'metric name', kind: 'text', def: 'console_rate' },
             { key: 'value', label: 'observation', kind: 'number', def: 0.83 },
             { key: 'baseline', label: 'baseline', kind: 'number', def: 0.6 }],
    build: v => ({ metric_name: v.metric_name, value: Number(v.value), baseline: Number(v.baseline) }) },
  { id: 'transduce', label: 'Transduce', hint: 'Hill saturation transform — where the signal sits on the dose-response curve. Nothing is timed.',
    fields: [{ key: 'input_signal', label: 'input signal (≥0)', kind: 'number', def: 0.7 },
             { key: 'hill', label: 'Hill coefficient', kind: 'number', def: 4.5 }],
    build: v => ({ input_signal: Number(v.input_signal), hill: Number(v.hill) }) },
  // edges split on '>' — the first version used '-', which MANGLED any hyphenated node name
  // ('web-server' became a dangling ['web','server'] the backend then honestly discarded: a wrong
  // measurement of the graph the user described, manufactured by the console itself)
  { id: 'topology', label: 'Topology', hint: 'Betti numbers over APPLIED edges — malformed/dangling edges are discarded AND disclosed, never counted as cycles.',
    fields: [{ key: 'nodes', label: 'nodes (comma-separated)', kind: 'text', def: 'a, b, c', wide: true },
             { key: 'edges', label: 'edges (u>v, …)', kind: 'text', def: 'a>b, b>c, c>a', wide: true }],
    build: v => ({ nodes: parsePairs(String(v.nodes)), edges: parsePairs(String(v.edges)).map(e => {
      const i = e.indexOf('>');
      if (i < 0) throw new Error(`edge "${e}" is not u>v`);
      return [e.slice(0, i).trim(), e.slice(i + 1).trim()];
    }) }) },
  { id: 'entropy', label: 'Seed', hint: 'Deterministic SHA3-512 seed derivation over your source labels — reproducible, reads NO system entropy, never for keys.',
    fields: [{ key: 'sources', label: 'source labels (comma-separated)', kind: 'text', def: 'alpha, beta', wide: true }],
    build: v => ({ sources: parsePairs(String(v.sources)).map((s, i) => ({ source: s, timestamp: i + 1, size: 0, content_hash: s })) }) },
];

function PrimValue({ k, v }: { k: string; v: unknown }) {
  // W437 refuter catch: one constant label cannot carry the null's meaning — consensus.choice null
  // means "measured, nothing cleared", rigor.p_value null means "not measured". The basis line says
  // which; the chip only points there.
  if (v === null) return <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-500">null — see basis</span>;
  if (typeof v === 'boolean') return <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${v ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>{String(v)}</span>;
  if (Array.isArray(v) && v.length > 12) return <span className="text-[9px] font-mono text-slate-400">[{v.length} points]</span>;
  if (typeof v === 'object') return <span className="text-[9px] font-mono text-slate-400 break-all">{JSON.stringify(v)}</span>;
  return <span className={`text-[10px] font-bold ${k === 'seed' ? 'font-mono' : ''} text-slate-300 break-all`}>{String(v)}</span>;
}

function PrimitiveConsole() {
  const [sel, setSel] = useState<string>('consensus');
  const [vals, setVals] = useState<Record<string, Record<string, string | number | boolean>>>(
    () => Object.fromEntries(PRIMITIVES.map(p => [p.id, Object.fromEntries(p.fields.map(f => [f.key, f.def]))])));
  const [res, setRes] = useState<Record<string, unknown> | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const prim = PRIMITIVES.find(p => p.id === sel)!;

  const run = async () => {
    setBusy(true); setRes(null); setErr('');
    try {
      setRes(await apiJson(`/api/v1/native-ai/${prim.id}`, { method: 'POST', body: prim.build(vals[prim.id]) }));
    } catch (e) { setErr(errorMessage(e)); }   // a 422 here is the honesty working (bad input REFUSED)
    setBusy(false);
  };

  const basis = res && typeof res.basis === 'string' ? res.basis : null;
  const method = res && typeof res.method === 'string' ? res.method : null;
  const rows = res ? Object.entries(res).filter(([k]) => k !== 'basis' && k !== 'method') : [];

  return (
    <Card className="p-6 border-aura/30">
      <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-1 flex items-center gap-2"><Play size={14} /> Primitive console — run every owned capability live</h3>
      <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">
        Each primitive below runs the REAL integrated module and renders its <span className="text-aura">whole</span> payload —
        including the parts that say what was <span className="text-aura">not</span> measured. Every one was audited (five fixed, W437)
        before this console made them reachable.
      </p>
      <div className="flex gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 flex-wrap mb-3">
        {PRIMITIVES.map(p => (
          <button key={p.id} type="button" onClick={() => { setSel(p.id); setRes(null); setErr(''); }}
            className={`px-2.5 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${sel === p.id ? 'bg-aura text-sovereign' : 'text-slate-500 hover:text-white'}`}>{p.label}</button>
        ))}
      </div>
      <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">{prim.hint}</p>
      <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-2 mb-3">
        {prim.fields.map(f => (
          <label key={f.key} className={`block ${f.wide ? '@[640px]:col-span-2' : ''}`}>
            <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">{f.label}</span>
            {f.kind === 'select' ? (
              <select value={String(vals[prim.id][f.key])}
                onChange={e => setVals(s => ({ ...s, [prim.id]: { ...s[prim.id], [f.key]: e.target.value } }))}
                className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300 mt-0.5">
                {f.options!.map(o => <option key={o} value={o}>{o}</option>)}
              </select>
            ) : (
              <input value={String(vals[prim.id][f.key])} type={f.kind === 'number' ? 'number' : 'text'} step="any"
                onChange={e => setVals(s => ({ ...s, [prim.id]: { ...s[prim.id], [f.key]: e.target.value } }))}
                className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300 mt-0.5" />
            )}
          </label>
        ))}
      </div>
      <Button onClick={run} disabled={busy} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
        {busy ? <Loader2 size={13} className="animate-spin" /> : <Play size={13} />} Run {prim.label.toLowerCase()}
      </Button>
      {err && <p className="text-vital text-[11px] font-bold mt-3">{err}</p>}
      {res && (
        <div className="mt-3 p-3 rounded-xl bg-slate-950 border border-slate-900">
          <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-x-4 gap-y-1.5">
            {rows.map(([k, v]) => (
              <div key={k} className="flex items-baseline justify-between gap-2 min-w-0">
                <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 shrink-0">{k}</span>
                <PrimValue k={k} v={v} />
              </div>
            ))}
          </div>
          {basis && (
            <p className="text-[10px] text-amber-200/80 italic leading-relaxed mt-2 pt-2 border-t border-slate-900">
              <span className="not-italic font-black uppercase text-[8px] tracking-widest text-amber-400/80 mr-1.5">basis</span>{basis}
            </p>
          )}
          {method && <p className="text-[8px] font-mono text-slate-600 mt-1.5">{method}</p>}
        </div>
      )}
    </Card>
  );
}

export const NativeAI: React.FC = () => {
  const [status, setStatus] = useState<Status | null>(null);
  const [capabilities, setCapabilities] = useState<Capability[]>([]);
  const [context, setContext] = useState('a halal, zero-waste community meal service for elderly Londoners');
  const [run, setRun] = useState<SwarmRun | null>(null);
  const [running, setRunning] = useState(false);
  const [goal, setGoal] = useState('Build and launch a halal compliance review service for SME food businesses');
  const [tree, setTree] = useState<TreeRun | null>(null);
  const [treeRunning, setTreeRunning] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [homeo, setHomeo] = useState<any>(null);   // §8→§6 live homeostatic posture
  // W437 — fabric integrity: a REAL import probe of every capability's backing module, plus the
  // live resource selection order (both were server-side only; no page ever called them)
  const [selfcheck, setSelfcheck] = useState<{ total: number; live: number; all_live: boolean; modules: { source: string; live: boolean; error?: string }[] } | null>(null);
  const [fabricRes, setFabricRes] = useState<{ resources: string[]; selection_order: string[] } | null>(null);

  // ── bespoke cascade design (user design control) ──
  const [name, setName] = useState('Concept Validator');
  const [stages, setStages] = useState<Stage[]>([
    { role: 'analyst', instruction: 'Analyse the objective and list the top risks.' },
    { role: 'designer', instruction: 'Design the approach addressing those risks.' },
    { role: 'synthesiser', instruction: 'Synthesise the single best recommendation.' },
  ]);
  const [cascades, setCascades] = useState<SavedCascade[]>([]);
  const [saving, setSaving] = useState(false);
  const [savedRun, setSavedRun] = useState<{ id: string; run: SwarmRun } | null>(null);
  const [runningId, setRunningId] = useState('');

  const loadCascades = () =>
    fetch('/api/v1/resources/swarm').then(r => r.json()).then(d => setCascades(d.cascades || [])).catch(() => {});

  // W276/W284 — the owned-model estate's LIFECYCLE (evaluate · promote · retire · reinstate)
  const [lifecycle, setLifecycle] = useState<{
    promoted_default?: string | null; effective_default?: string; retired?: string[];
    discovered?: string[]; active_estate?: string[];
    evaluations?: { model: string; can_serve: boolean; score: number | null; at: string }[];
  } | null>(null);
  const [lcBusy, setLcBusy] = useState('');
  const loadLifecycle = () =>
    fetch('/api/v1/native-ai/lifecycle').then(r => r.json()).then(setLifecycle).catch(() => {});
  const lifecycleAction = async (action: 'evaluate' | 'promote' | 'retire' | 'reinstate', model: string) => {
    setLcBusy(`${action}:${model}`);
    try {
      // Ledger cluster 2 — a failed retire/promote must be visible, never a silent reload
      await apiJson(`/api/v1/native-ai/lifecycle/${action}`, { method: 'POST', body: { model } });
      loadLifecycle();
    } catch (e) { setError(errorMessage(e)); }
    setLcBusy('');
  };

  useEffect(() => {
    fetch('/api/v1/native-ai/status').then(r => r.json()).then(setStatus)
      .catch(() => setError('Failed to load fabric status'))
      .finally(() => setLoading(false));
    fetch('/api/v1/native-ai/capabilities').then(r => r.json()).then(d => setCapabilities(d.capabilities || [])).catch(() => {});
    fetch('/api/v1/native-ai/homeostasis').then(r => r.json()).then(setHomeo).catch(() => {});
    fetch('/api/v1/native-ai/selfcheck').then(r => r.json()).then(setSelfcheck).catch(() => {});
    fetch('/api/v1/native-ai/resources').then(r => r.json()).then(setFabricRes).catch(() => {});
    fetch('/api/v1/native-ai/models').then(r => r.json())
      .then(d => setModelTiers(d.tiers || [])).catch(() => {});
    loadCascades();
    loadLifecycle();
  }, []);

  // §6/§7 — native completion with user-selected model tier (auto · native floor · local model(s))
  const [cPrompt, setCPrompt] = useState('Outline a halal, zero-waste weekly meal plan for an elderly resident');
  const [cModel, setCModel] = useState<string>('auto');
  const [modelTiers, setModelTiers] = useState<{ id: string; label: string; kind: string }[]>([]);
  const [cRes, setCRes] = useState<{ output: string; served_by: string; is_external: boolean; resources_tried?: string[] } | null>(null);
  const [completing, setCompleting] = useState(false);
  const runComplete = async () => {
    if (!cPrompt.trim()) return;
    setCompleting(true); setCRes(null);
    try {
      setCRes(await apiJson('/api/v1/native-ai/complete', {
        method: 'POST', body: { prompt: cPrompt, agent: 'console', model: cModel } }));
    } catch (e) { setError(errorMessage(e)); }
    setCompleting(false);
  };

  // §6 — run the prompt across ALL owned models in parallel, then synthesise a consensus
  const [ensRes, setEnsRes] = useState<{ members: { model: string; served_by?: string; output?: string; error?: string }[]; synthesis?: { output: string; served_by?: string } | null } | null>(null);
  const [ensembling, setEnsembling] = useState(false);
  const runEnsemble = async () => {
    if (!cPrompt.trim()) return;
    setEnsembling(true); setEnsRes(null);
    try {
      setEnsRes(await apiJson('/api/v1/native-ai/ensemble', {
        method: 'POST', body: { prompt: cPrompt, agent: 'console' } }));
    } catch (e) { setError(errorMessage(e)); }
    setEnsembling(false);
  };

  const runSwarm = async () => {
    setRunning(true); setRun(null);
    try {
      setRun(await apiJson('/api/v1/native-ai/swarm', {
        method: 'POST', body: { agent: 'demo', context } }));
    } catch (e) { setError(errorMessage(e)); }
    setRunning(false);
  };

  const runTree = async () => {
    if (!goal.trim()) return;
    setTreeRunning(true); setTree(null); setError('');
    try {
      const r = await fetch('/api/v1/native-ai/tree', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal }),
      });
      const data = await r.json();
      // only render a well-formed tree run; surface anything else (404/500/error) as a message
      if (r.ok && Array.isArray(data?.levels) && Array.isArray(data?.nodes)) {
        setTree(data);
      } else {
        setError(data?.detail || `Workflow-tree run failed (HTTP ${r.status}).`);
      }
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setTreeRunning(false);
  };

  const setStage = (i: number, k: keyof Stage, v: string) =>
    setStages(s => s.map((st, idx) => (idx === i ? { ...st, [k]: v } : st)));
  const addStage = () => setStages(s => [...s, { role: '', instruction: '' }]);
  const removeStage = (i: number) => setStages(s => s.filter((_, idx) => idx !== i));

  // §7 (W344) — RECONFIGURE from the UI: the PUT reconfigure path (W267) was fully functional
  // but reachable by curl only — no page offered an Edit. editingId switches the designer between
  // define (POST) and reconfigure (PUT) of the loaded cascade.
  const [editingId, setEditingId] = useState<string | null>(null);
  const startEdit = (c: SavedCascade) => {
    setEditingId(c.id);
    setName(c.name);
    setStages(c.stages.map(s => ({ role: s.role, instruction: s.instruction })));
  };

  const saveCascade = async () => {
    setSaving(true);
    try {
      const valid = stages.filter(s => s.role.trim() && s.instruction.trim());
      const url = editingId ? `/api/v1/resources/swarm/${editingId}` : '/api/v1/resources/swarm/define';
      const r = await fetch(url, {
        method: editingId ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editingId ? { name, stages: valid }
                                       : { name, context, stages: valid, usage_area: 'synthesis' }),
      });
      if (!r.ok) setError(`Save failed (HTTP ${r.status}).`);   // W344 — never a silent click
      setEditingId(null);
      await loadCascades();
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setSaving(false);
  };

  const runSaved = async (id: string) => {
    setRunningId(id); setSavedRun(null);
    try {
      setSavedRun({ id, run: await apiJson('/api/v1/resources/swarm/run', {
        method: 'POST', body: { swarm_id: id } }) });
    } catch (e) { setError(errorMessage(e)); }
    setRunningId('');
  };

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Native AI Fabric</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">In-House AI Resources</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Workstation's <span className="text-highlight">own</span> AI Swarm · Models · Orchestration — not a façade over external
          API calls. The platform produces a real result from its <span className="text-highlight">owned</span> resources with no
          external dependency; external providers are optional accelerants only.
        </p>
      </header>

      {error && <p className="text-vital text-xs font-bold">{error}</p>}

      {loading && !status && !error && (
        <div className="flex items-center gap-2 text-[11px] font-bold text-slate-500"><Loader2 size={14} className="animate-spin" /> Loading the native AI fabric…</div>
      )}

      {status && (
        <>
          {/* HONEST active-model resolution — is your AI a REAL model right now, or the deterministic floor? */}
          <Card className={`p-4 ${status.floor_active ? 'border-amber-500/40 bg-amber-500/5' : 'border-emerald-500/40 bg-emerald-500/5'}`}>
            <div className="flex items-center gap-3 flex-wrap">
              <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded ${status.floor_active ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                {status.floor_active ? 'Deterministic floor active' : `Real model: ${status.active_model_label || status.active_model}`}
              </span>
              <span className="text-[9px] font-bold uppercase text-slate-500">serving: {status.active_model} · {status.mode}</span>
            </div>
            {status.floor_active && status.floor_note && (
              <p className="text-[11px] text-slate-400 leading-relaxed mt-2">{status.floor_note}</p>
            )}
          </Card>

          {/* Posture */}
          <Card className="p-6 border-emerald-500/30 bg-emerald-500/5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-black text-white uppercase tracking-wide flex items-center gap-2"><ShieldCheck size={16} className="text-emerald-400" /> Posture</h3>
              <span className="text-[10px] font-black uppercase px-2 py-1 rounded bg-emerald-500/20 text-emerald-400">{status.posture}</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">{status.guarantee}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">external allowed: {String(status.external_allowed)}</span>
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">selection: {status.selection_order.join(' → ')}</span>
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-aura/10 text-aura">owned available: {status.owned_resources_available.join(', ')}</span>
            </div>
          </Card>

          {/* §8 → §6 — the living organism's homeostasis governs how much cognition the fabric admits;
              cognitive work expends ATP (closed loop). Real organism state, never fabricated. */}
          {homeo?.organism && (
            <Card className="p-6 border-violet-500/30 bg-violet-500/5">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-black text-white uppercase tracking-wide flex items-center gap-2">
                  <Activity size={16} className="text-violet-300" /> Biomimetic Homeostasis · cognition control
                </h3>
                <span className={`text-[10px] font-black uppercase px-2 py-1 rounded ${
                  homeo.posture === 'full' ? 'bg-emerald-500/20 text-emerald-400'
                  : homeo.posture === 'reduced' ? 'bg-amber-500/20 text-amber-400'
                  : 'bg-vital/20 text-vital'}`}>{homeo.posture}</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                The living organism (§8) modulates the native AI fabric (§6): immune, circadian rhythm and metabolic ATP
                set how many swarm agents run in parallel — and each run expends ATP, which recovers on the circadian cycle.
              </p>
              <div className="flex flex-wrap gap-2 mt-3">
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-violet-500/10 text-violet-300">max parallel: {homeo.max_parallel}</span>
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">mode: {homeo.organism.mode}</span>
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">circadian: {homeo.organism.circadian}{homeo.organism.is_peak_focus ? ' · peak' : ''}</span>
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">ATP: {Math.round((homeo.organism.atp_ratio ?? 0) * 100)}%</span>
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">immune: {homeo.organism.immune_threat}</span>
                <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">composite: {Math.round((homeo.organism.composite_health ?? 0) * 100)}%</span>
              </div>
            </Card>
          )}

          {/* Owned AI capabilities catalogue */}
          {capabilities.length > 0 && (
            <div>
              <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Cpu size={14} /> Owned AI capabilities ({capabilities.length})</h3>
              <p className="text-[10px] text-slate-600 mb-3">Each is backed by a real, integrated <span className="text-aura">agentic_core</span> module — no external dependency.</p>
              <div className="grid grid-cols-1 @[640px]:grid-cols-2 @[960px]:grid-cols-3 gap-2">
                {capabilities.map(cap => (
                  <Card key={cap.endpoint + cap.name} className="p-3">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <p className="text-[11px] font-black text-white truncate">{cap.name}</p>
                      <span className="text-[7px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 shrink-0">{cap.kind}</span>
                    </div>
                    <p className="text-[9px] text-slate-500 leading-snug line-clamp-3 mb-1.5">{cap.description}</p>
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-[8px] font-mono text-slate-600 truncate">{cap.endpoint}</span>
                      {cap.in_house && <span className="text-[7px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/10 text-aura shrink-0">in-house</span>}
                    </div>
                    <p className="text-[8px] font-mono text-slate-700 mt-1 truncate">↳ {cap.source}</p>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* W437 — fabric integrity: the real import probe + live selection order, finally on a page */}
          {selfcheck && (
            <Card className={`p-4 ${selfcheck.all_live ? 'border-emerald-500/30' : 'border-amber-500/40 bg-amber-500/5'}`}>
              <div className="flex items-center gap-2 flex-wrap mb-2">
                <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-2"><ShieldCheck size={14} className={selfcheck.all_live ? 'text-emerald-400' : 'text-amber-400'} /> Fabric integrity</h3>
                <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${selfcheck.all_live ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                  {selfcheck.live}/{selfcheck.total} backing modules import live
                </span>
                {fabricRes && <span className="text-[9px] font-bold uppercase text-slate-500">selection: {fabricRes.selection_order.join(' → ')}</span>}
              </div>
              <div className="flex flex-wrap gap-1">
                {selfcheck.modules.map(m => (
                  <span key={m.source} title={m.error || 'imports cleanly'}
                    className={`text-[8px] font-mono px-1.5 py-0.5 rounded ${m.live ? 'bg-slate-900 text-slate-500' : 'bg-vital/15 text-vital'}`}>{m.source}{m.live ? '' : ' ✗'}</span>
                ))}
              </div>
            </Card>
          )}

          {/* W437 — the 10 primitives were catalogued above but NO page could run them */}
          <PrimitiveConsole />

          {/* Resources */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Cpu size={14} /> Model Resources</h3>
            <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-3">
              {status.resources.map(r => {
                const Icon = kindIcon(r.kind);
                return (
                  <Card key={r.name} className="p-4">
                    <div className="flex items-center justify-between mb-1">
                      <p className="font-black text-white text-sm flex items-center gap-2"><Icon size={14} className={r.is_external ? 'text-slate-500' : 'text-aura'} /> {r.name} {r.model && <span className="text-[9px] text-slate-600 font-bold">({r.model})</span>}</p>
                      <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${r.available ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-600'}`}>{r.available ? 'available' : 'off'}</span>
                    </div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${r.is_external ? 'bg-amber-500/10 text-amber-400' : 'bg-aura/10 text-aura'}`}>{r.is_external ? 'external (opt-in)' : 'owned'}</span>
                      <span className="text-[8px] font-bold uppercase text-slate-600">{r.kind}</span>
                    </div>
                    <p className="text-[10px] text-slate-600 leading-relaxed">{r.note}</p>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* §6/§7 — native completion with a user-selected model tier */}
          <Card className="p-6 border-aura/30">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-1 flex items-center gap-2"><Cpu size={14} /> Native completion · choose the owned model tier</h3>
            <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">Run a completion on Workstation's OWN AI and pick which owned tier serves — the result reports the resource that actually served (honest provenance).</p>
            <textarea value={cPrompt} onChange={e => setCPrompt(e.target.value)} rows={2}
              className="w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300 mb-3"
              placeholder="Prompt for the native AI…" />
            <div className="flex items-center gap-3 flex-wrap mb-3">
              <div className="flex gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 flex-wrap">
                {(modelTiers.length ? modelTiers : [{ id: 'auto', label: 'Auto', kind: 'policy' }, { id: 'native', label: 'Native floor', kind: 'native' }]).map(t => (
                  <button key={t.id} type="button" onClick={() => setCModel(t.id)}
                    title={t.kind === 'local' ? 'an owned local model (Ollama) — floor fallback' : t.id === 'native' ? 'force the deterministic native floor (fast · free · reproducible)' : 'in-house-first: local model → native floor → opt-in external'}
                    className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${cModel === t.id ? 'bg-aura text-sovereign' : 'text-slate-500 hover:text-white'}`}>{t.label}</button>
                ))}
              </div>
              <Button onClick={runComplete} disabled={completing || !cPrompt.trim()} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
                {completing ? <Loader2 size={13} className="animate-spin" /> : <Cpu size={13} />} Run completion
              </Button>
              <button type="button" onClick={runEnsemble} disabled={ensembling || !cPrompt.trim()}
                title="Run across ALL owned models in parallel, then synthesise a consensus"
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-aura/40 text-aura text-[10px] font-black uppercase tracking-widest hover:bg-aura/10 disabled:opacity-50">
                {ensembling ? <Loader2 size={12} className="animate-spin" /> : <Network size={12} />} Ensemble (all owned models)
              </button>
            </div>
            {ensRes && (
              <div className="p-3 rounded-xl bg-slate-950 border border-aura/20 mb-3">
                <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Ensemble · {ensRes.members.length} owned models in parallel → consensus</p>
                <div className="flex flex-wrap gap-1.5 mb-2">
                  {ensRes.members.map((m, i) => (
                    <span key={i} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${m.error ? 'bg-vital/15 text-vital' : 'bg-slate-900 text-slate-400'}`} title={m.output ? m.output.slice(0, 200) : m.error}>
                      {m.model} {m.served_by ? `· ${m.served_by}` : ''}{m.error ? ' · failed' : ''}
                    </span>
                  ))}
                </div>
                {ensRes.synthesis?.output && (
                  <div className="border-t border-aura/10 pt-2">
                    <p className="text-[8px] font-black uppercase tracking-widest text-aura mb-1">Consensus <span className="text-slate-600 normal-case">· synthesised by {ensRes.synthesis.served_by}</span></p>
                    <p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">{ensRes.synthesis.output}</p>
                  </div>
                )}
              </div>
            )}
            {cRes && (
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${cRes.is_external ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                    {cRes.is_external ? `via ${cRes.served_by}` : `in-house · ${cRes.served_by}`}
                  </span>
                  {cRes.resources_tried && <span className="text-[8px] font-mono text-slate-600">tried: {cRes.resources_tried.join(' → ')}</span>}
                </div>
                <p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">{cRes.output}</p>
              </div>
            )}
          </Card>

          {/* W276/W284 — the owned-model estate is MANAGED: evaluate · promote · retire · reinstate */}
          {lifecycle && (
            <Card className="p-6 border-sky-500/30">
              <h3 className="text-[10px] font-black uppercase tracking-widest text-sky-300 mb-1">Owned-model lifecycle (§6 — the estate is managed, not enumerated)</h3>
              <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">
                Serving default: <span className="text-white font-black">{lifecycle.effective_default ?? '—'}</span>
                {lifecycle.promoted_default ? <span className="text-sky-300"> (promoted)</span> : <span> (env default)</span>}
                {(lifecycle.retired ?? []).length > 0 && <span> · retired: {lifecycle.retired!.join(', ')}</span>}
              </p>
              {(lifecycle.discovered ?? []).length === 0 && (
                <p className="text-[10px] text-slate-600 italic mb-2">No local models discovered right now — evaluation reports honestly (can_serve: false) rather than inventing scores; pull a model into the local server to manage the estate.</p>
              )}
              <div className="space-y-1.5">
                {(lifecycle.discovered ?? []).map(m => (
                  <div key={m} className="flex flex-wrap items-center gap-1.5">
                    <span className="text-[11px] font-black text-white">{m}</span>
                    {lifecycle.effective_default === m && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300">serving</span>}
                    {(lifecycle.retired ?? []).includes(m) && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-500">retired</span>}
                    {(['evaluate', 'promote'] as const).map(a => (
                      <button key={a} type="button" onClick={() => lifecycleAction(a, m)} disabled={!!lcBusy}
                        className="text-[8px] font-black uppercase text-slate-400 border border-slate-700 px-1.5 py-0.5 rounded hover:text-sky-300 hover:border-sky-500/40 transition-colors">
                        {lcBusy === `${a}:${m}` ? '…' : a}
                      </button>
                    ))}
                    <button type="button"
                      onClick={() => lifecycleAction((lifecycle.retired ?? []).includes(m) ? 'reinstate' : 'retire', m)}
                      disabled={!!lcBusy}
                      className="text-[8px] font-black uppercase text-slate-400 border border-slate-700 px-1.5 py-0.5 rounded hover:text-amber-400 hover:border-amber-500/40 transition-colors">
                      {(lifecycle.retired ?? []).includes(m) ? 'reinstate' : 'retire'}
                    </button>
                  </div>
                ))}
              </div>
              {(lifecycle.evaluations ?? []).length > 0 && (
                <div className="mt-3 space-y-1">
                  <p className="text-[8px] font-black uppercase tracking-widest text-slate-500">Recent evaluations (honest — no score when the target could not serve)</p>
                  {lifecycle.evaluations!.slice(-3).reverse().map((ev, i) => (
                    <p key={i} className="text-[9px] text-slate-400">
                      {ev.model} · {ev.can_serve ? `score ${ev.score}` : 'could not serve — no score'} · {ev.at}
                    </p>
                  ))}
                </div>
              )}
            </Card>
          )}

          {/* Quick swarm runner */}
          <Card className="p-6">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Network size={14} /> Quick swarm (default cascade, owned resources)</h3>
            <textarea value={context} onChange={e => setContext(e.target.value)} rows={2}
              className="w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300 mb-3"
              placeholder="Context / objective for the swarm…" />
            <Button onClick={runSwarm} disabled={running} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
              {running ? <Loader2 size={13} className="animate-spin" /> : <Network size={13} />} Run quick swarm
            </Button>
            {run && <Trace run={run} />}
          </Card>

          {/* Autonomous workflow-TREE orchestration (the living-organism cascade) */}
          <Card className="p-6 border-highlight/30">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-1 flex items-center gap-2"><Network size={14} /> Autonomous workflow tree</h3>
            <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">
              Give a goal — the native swarm <span className="text-highlight">autonomously decomposes</span> it into a dependency
              <span className="text-highlight"> tree</span> and runs it in-house-first with <span className="text-highlight">parallel branches</span>,
              biomimetically mediated (immune-throttled parallelism · nervous-system signals · the learning loop). Every node reports the owned resource that served it.
            </p>
            <textarea value={goal} onChange={e => setGoal(e.target.value)} rows={2}
              className="w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300 mb-3"
              placeholder="Goal for the swarm to plan + execute as a workflow tree…" />
            <Button onClick={runTree} disabled={treeRunning || !goal.trim()} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
              {treeRunning ? <Loader2 size={13} className="animate-spin" /> : <Network size={13} />} Plan + run workflow tree
            </Button>
            {tree && <TreeView run={tree} />}
          </Card>

          {/* Design a bespoke cascade (user design control) */}
          <Card className="p-6 border-aura/30">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-1 flex items-center gap-2"><Cpu size={14} /> Design a bespoke swarm cascade</h3>
            <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">Reconfigure the agent stages, name it, and save it as a reusable, re-runnable resource that runs on Workstation's <span className="text-aura">owned</span> resources. This is a first-class Resource-Fabric resource.</p>
            <input value={name} onChange={e => setName(e.target.value)}
              className="w-full text-xs font-bold bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-white mb-3"
              placeholder="Cascade name…" />
            <div className="space-y-2 mb-3">
              {stages.map((s, i) => (
                <div key={i} className="flex items-center gap-2">
                  <input value={s.role} onChange={e => setStage(i, 'role', e.target.value)}
                    className="w-32 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-aura font-bold"
                    placeholder="role" />
                  <input value={s.instruction} onChange={e => setStage(i, 'instruction', e.target.value)}
                    className="flex-1 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300"
                    placeholder="instruction for this agent…" />
                  <button onClick={() => removeStage(i)} aria-label={`Remove stage ${i + 1}`} title="Remove stage" className="text-slate-600 hover:text-vital p-1"><Trash2 size={13} /></button>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-2">
              <Button onClick={addStage} className="flex items-center gap-1.5 bg-slate-900 text-slate-300 text-[11px]"><Plus size={12} /> Add stage</Button>
              <Button onClick={saveCascade} disabled={saving || !name.trim()} className="flex items-center gap-1.5 bg-aura text-sovereign text-[11px]">
                {saving ? <Loader2 size={12} className="animate-spin" /> : <Save size={12} />} Save cascade
              </Button>
            </div>
          </Card>

          {/* Saved cascades */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Server size={14} /> Saved cascades ({cascades.length})</h3>
            {cascades.length === 0 && <p className="text-[11px] text-slate-600">No saved cascades yet — design one above.</p>}
            <div className="space-y-3">
              {cascades.slice().reverse().map(c => (
                <Card key={c.id} className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-black text-white text-sm">{c.name}</p>
                      <p className="text-[9px] text-slate-600 font-bold uppercase mt-0.5">{c.stages.length} stages · {c.stages.map(s => s.role).join(' → ')}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {/* §7 (W344) — the reconfigure path, finally reachable from the page */}
                      <Button onClick={() => startEdit(c)} className="bg-slate-900 text-slate-300 text-[11px]">
                        {editingId === c.id ? 'Editing…' : 'Edit'}
                      </Button>
                      <Button onClick={() => runSaved(c.id)} disabled={runningId === c.id} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[11px]">
                        {runningId === c.id ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />} Run
                      </Button>
                    </div>
                  </div>
                  {savedRun?.id === c.id && <Trace run={savedRun.run} />}
                </Card>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
