import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Cpu, Network, Loader2, CheckCircle2, Circle, ShieldCheck, Server, Globe, Plus, Trash2, Play, Save } from 'lucide-react';

interface ModelResource {
  name: string; kind: string; available: boolean; is_external: boolean; model?: string; note?: string;
}
interface Status {
  posture: string; external_allowed: boolean; owned_resources_available: string[];
  selection_order: string[]; guarantee: string; resources: ModelResource[];
}
interface SwarmStep { step: number; role: string; served_by: string; output: string }
interface SwarmRun { agent: string; stages: number; trace: SwarmStep[]; final: string; any_external: boolean }
interface Stage { role: string; instruction: string }
interface TreeNodeDef { id: string; role: string; depends_on: string[] }
interface TreeNodeResult extends TreeNodeDef { served_by: string; is_external: boolean; output: string }
interface TreeGovernance { governed_by: string; qms_passed: boolean; qms_coverage_proxy: number; dcms_hash: string; dcms_algo: string; dcms_version: number }
interface TreeRun {
  goal: string; posture: string; tree: TreeNodeDef[]; levels: string[][];
  node_count: number; parallel_levels: number; max_parallel: number; immune_threat: string;
  governance?: TreeGovernance | null;
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
  const [context, setContext] = useState('a halal, zero-waste community meal service for elderly Londoners');
  const [run, setRun] = useState<SwarmRun | null>(null);
  const [running, setRunning] = useState(false);
  const [goal, setGoal] = useState('Build and launch a halal compliance review service for SME food businesses');
  const [tree, setTree] = useState<TreeRun | null>(null);
  const [treeRunning, setTreeRunning] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

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

  useEffect(() => {
    fetch('/api/v1/native-ai/status').then(r => r.json()).then(setStatus)
      .catch(() => setError('Failed to load fabric status'))
      .finally(() => setLoading(false));
    loadCascades();
  }, []);

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
