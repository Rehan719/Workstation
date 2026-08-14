import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Cpu, Network, Loader2, CheckCircle2, Circle, ShieldCheck, Server, Globe, Plus, Trash2, Play, Save, Activity } from 'lucide-react';

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
interface TreeSignal { input_strength: number; peak_intensity: number; latency_s: number; propagated: boolean; hill: number; method: string }
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
        <div className="mt-2 p-2.5 rounded-xl bg-slate-950 border border-slate-900 flex items-center flex-wrap gap-2">
          <span className="text-[8px] font-black uppercase tracking-widest text-slate-500">Biomimetic signal</span>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${run.signal_response.propagated ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500'}`}>{run.signal_response.propagated ? 'propagated' : 'sub-threshold'}</span>
          <span className="text-[8px] font-bold uppercase text-slate-500">peak {Math.round(run.signal_response.peak_intensity * 100)}% · latency {run.signal_response.latency_s}s · Hill {run.signal_response.hill}</span>
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
      await fetch(`/api/v1/native-ai/lifecycle/${action}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model }),
      });
      loadLifecycle();
    } catch { /* surfaced via reload */ }
    setLcBusy('');
  };

  useEffect(() => {
    fetch('/api/v1/native-ai/status').then(r => r.json()).then(setStatus)
      .catch(() => setError('Failed to load fabric status'))
      .finally(() => setLoading(false));
    fetch('/api/v1/native-ai/capabilities').then(r => r.json()).then(d => setCapabilities(d.capabilities || [])).catch(() => {});
    fetch('/api/v1/native-ai/homeostasis').then(r => r.json()).then(setHomeo).catch(() => {});
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
      const r = await fetch('/api/v1/native-ai/complete', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: cPrompt, agent: 'console', model: cModel }),
      });
      setCRes(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setCompleting(false);
  };

  // §6 — run the prompt across ALL owned models in parallel, then synthesise a consensus
  const [ensRes, setEnsRes] = useState<{ members: { model: string; served_by?: string; output?: string; error?: string }[]; synthesis?: { output: string; served_by?: string } | null } | null>(null);
  const [ensembling, setEnsembling] = useState(false);
  const runEnsemble = async () => {
    if (!cPrompt.trim()) return;
    setEnsembling(true); setEnsRes(null);
    try {
      const r = await fetch('/api/v1/native-ai/ensemble', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: cPrompt, agent: 'console' }),
      });
      setEnsRes(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setEnsembling(false);
  };

  const runSwarm = async () => {
    setRunning(true); setRun(null);
    try {
      const r = await fetch('/api/v1/native-ai/swarm', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: 'demo', context }),
      });
      setRun(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
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

  const saveCascade = async () => {
    setSaving(true);
    try {
      const valid = stages.filter(s => s.role.trim() && s.instruction.trim());
      await fetch('/api/v1/resources/swarm/define', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, context, stages: valid, usage_area: 'synthesis' }),
      });
      await loadCascades();
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setSaving(false);
  };

  const runSaved = async (id: string) => {
    setRunningId(id); setSavedRun(null);
    try {
      const r = await fetch('/api/v1/resources/swarm/run', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ swarm_id: id }),
      });
      setSavedRun({ id, run: await r.json() });
    } catch (e: any) { setError(e?.message ?? String(e)); }
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
                    <Button onClick={() => runSaved(c.id)} disabled={runningId === c.id} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[11px]">
                      {runningId === c.id ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />} Run
                    </Button>
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
