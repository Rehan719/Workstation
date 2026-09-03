import React, { useState, useEffect } from 'react';
import { provenanceBadge } from '../../lib/api';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import {
  Boxes, Cpu, FlaskConical, Factory, Dna, ShieldCheck, Layers,
  Check, Loader2, Sparkles, Recycle, Play, X,
  Hammer, Zap, BarChart3, Brain, BookOpen, Code2, Rocket, Package, ArrowRight, Wand2,
} from 'lucide-react';
import { DomainTool } from '../../components/DomainTool';

// ── Process-intelligence studios ────────────────────────────────────────────────
// The Resource Fabric is the single hub for every engine. Each standalone studio below
// is a real §7 surface (its own page/route); launching from here keeps the nav lean while
// nothing is orphaned — the engines remain first-class, reachable in one click from the Fabric.
const STUDIOS: { name: string; desc: string; route: string; icon: React.ComponentType<any> }[] = [
  { name: 'Synthesis Studio',  desc: 'Ingest & synthesise knowledge',      route: '/synthesis',     icon: Sparkles },
  { name: 'Synthesis Nexus',   desc: 'Four-layer engine orchestration',     route: '/nexus',         icon: Sparkles },
  { name: 'Forge Pipeline',    desc: 'Forge digital resources',             route: '/forge-pipeline',icon: Hammer },
  { name: 'Digital Reactor',   desc: 'Mutate & iterate variants',           route: '/reactor',       icon: Zap },
  { name: 'Incubator',         desc: 'Evolve fitness over generations',     route: '/incubator',     icon: FlaskConical },
  { name: 'Reactor Studio',    desc: '2D/3D visual analytics',              route: '/reactor-studio',icon: BarChart3 },
  { name: 'Factory',           desc: 'Produce deliverables at scale',       route: '/factory',       icon: Factory },
  { name: 'Generator',         desc: 'Generate one artefact (code/schema/…)', route: '/generator',    icon: Wand2 },
  { name: 'Intelligence Lab',  desc: '8-stage BDP / SPI methodology',       route: '/intelligence',  icon: Brain },
  { name: 'Authorship Engine', desc: '9-stage scholarship & authorship',    route: '/authorship',    icon: BookOpen },
  { name: 'Design & Dev',      desc: '9-stage design & development',        route: '/design-dev',    icon: Code2 },
  { name: 'Solutions',         desc: 'Design · Build · Launch a solution',  route: '/solutions',     icon: Rocket },
  { name: 'Build to Order',    desc: 'Bespoke build-to-order pipeline',     route: '/bto',           icon: Package },
];

// ── Types ─────────────────────────────────────────────────────────────────────

interface Resource {
  id: string; name: string; resource_class: string; type: string; description: string;
  capabilities: string[]; reconfigurable_params: Record<string, string>; endpoint: string;
  methods: string[]; reusable: boolean; rerunnable: boolean; biomimetic: boolean; usable_in: string[];
}
interface Composition {
  id: string; name: string; usage_area: string;
  resources: { id: string; name: string; resource_class: string }[];
  reusable: boolean; rerunnable: boolean; created_at: string;
  // W273/W284 — living-design lifecycle + the params still unset (for per-run entry)
  version?: number;
  model?: { unset_params?: Record<string, string[]> };
}
// W274/W284 — a persisted composition run (GET /resources/compositions/runs)
interface HistoryRun {
  run_id: string; composition_id: string; name: string; version?: number; objective: string;
  qms_gate_passed?: boolean | null; any_external?: boolean;
  real_resources?: { resource: string; ran?: string; duration_ms?: number }[];
  plan_binding?: { result?: string; advanced?: boolean; objective_id?: string } | null;
  created_at: string;
}
interface Simulation {
  name: string; usage_area: string; commit_ready: boolean; saved: boolean; note?: string;
  model: {
    pipeline: string[]; combined_capabilities: string[]; resource_classes: Record<string, number>;
    biomimetic_resources: number; shared_usage_areas: string[]; usage_area_supported_by_all: boolean;
    incompatibilities: { id: string; name: string; reason: string }[];
    unset_params: Record<string, string[]>;
    // §7→§8 — projected living-organism capacity for this config's cognitive load (read-only, pre-commit).
    organism_capacity?: {
      projected_posture?: string; admitted_max_parallel?: number; demand_nodes?: number;
      fits_current_capacity?: boolean; organism?: { mode?: string; circadian?: string; atp_ratio?: number };
    } | null;
  };
  simulation: {
    quality?: { qms_gate_passed?: boolean; delivery_coverage?: number; bar?: string[]; document_controlled?: boolean;
      compliance?: { overall?: string; compliant?: boolean; verdicts?: { framework: string; status: string }[] } };
    biomimetic?: { immune?: { health?: number }; circadian?: string };
  };
}
interface CompositionRun {
  composition_id: string; name: string; objective: string; posture: string;
  trace: { step: number; role: string; served_by: string; output: string }[];
  final: string; any_external: boolean;
  // W273/W274/W284 — run-time honesty + plan binding surfaced to the Owner
  run_id?: string; commit_ready?: boolean; usage_area_supported?: boolean;
  quality_warning?: string | null; run_params_applied?: string[];
  plan_binding?: { result?: string; advanced?: boolean; objective_id?: string; status?: string } | null;
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean; verdicts?: { framework: string; status: string }[] } } };
  // §7→§5→§6→§8 — when the config includes the org resource, the real Chief→Build-to-Order cascade also runs.
  org_cascade?: {
    ran?: string; csuite_engaged?: string[]; management_systems?: string[]; appraisals?: string[];
    homeostasis?: { posture?: string }; governance?: string; ueg_hash?: string;
  } | null;
  // §7 deep integration — resources with a real endpoint also execute their genuine engine logic.
  real_resource_runs?: {
    resource: string; ran?: string; output?: string; error?: string;
    viable?: boolean; passages?: number; cognitive_primed?: boolean; engines_used?: string[];
    scenarios_run?: number; generations_run?: number; winner?: string;
    served_by?: string; is_external?: boolean; stages_run?: number;   // §6 — owned-resource provenance
  }[];
}

const CLASS_ICON: Record<string, React.ComponentType<any>> = {
  process_intelligence: Cpu, digital_resource: FlaskConical,
  organism_system: Dna, enterprise_org: Factory,
};
const CLASS_LABEL: Record<string, string> = {
  process_intelligence: 'Process Intelligence', digital_resource: 'Digital Resource',
  organism_system: 'Organism System', enterprise_org: 'Enterprise / Org',
};

// Surfaced resources that can be RUN inline from the fabric (on Workstation's OWN in-house engines).
// Each maps to a <DomainTool> config. Resources needing richer inputs (e.g. truth_consensus' list of
// claim objects) are intentionally absent until DomainTool can express them.
const RUN_CONFIGS: Record<string, React.ComponentProps<typeof DomainTool>> = {
  mega_project: {
    title: 'Mega-Project Synthesis',
    description: <>Synthesise a mega-project concept into a structured deliverable — in-house, with no fabricated figures.</>,
    endpoint: '/api/v1/mega-project/synthesise',
    resultKey: 'deliverable',
    submitLabel: 'Synthesise',
    fields: [
      { name: 'concept', label: 'Concept', type: 'textarea', placeholder: 'e.g. a carbon-negative shipping network' },
      { name: 'domain', label: 'Domain', type: 'text', default: 'enterprise' },
    ],
  },
  resource_optimizer: {
    title: 'Resource Allocation',
    description: <>Verify → schedule → assemble → allocate a resource request. Capacity is a single-node simulated baseline.</>,
    endpoint: '/api/v1/optimizer/allocate',
    resultKey: '_full',   // no such key → DomainTool shows the full JSON allocation result
    submitLabel: 'Allocate',
    fields: [
      { name: 'domain', label: 'Domain', type: 'text', default: 'science' },
      { name: 'requirements', label: 'Requirements (key: value per line)', type: 'keyvalue', default: 'CPU: 4\nRAM: 1024' },
      { name: 'tier', label: 'Tier', type: 'text', default: 'standard' },
    ],
  },
  experimentation: {
    title: 'Reactor · Experimentation (what-if)',
    description: <>Project and compare the outcomes of what-if scenarios against a subject — in-house, ranked, QMS-gated.</>,
    endpoint: '/api/v1/reactor/experiment',
    resultKey: 'comparison',
    submitLabel: 'Run experiment',
    fields: [
      { name: 'subject', label: 'Subject', type: 'textarea', placeholder: 'e.g. our halal meal-service pricing model' },
      { name: 'scenarios', label: 'What-if scenarios (one per line)', type: 'list', default: 'What if we cut price 20%?\nWhat if we add a subscription tier?\nWhat if we expand to a second city?' },
      { name: 'domain', label: 'Domain', type: 'text', default: 'enterprise' },
    ],
  },
  truth_consensus: {
    title: 'Truth Consensus',
    description: <>Reputation-weighted consensus over a set of claims — accepts a claim when its weighted confidence clears the threshold.</>,
    endpoint: '/api/v1/collective/consensus',
    resultKey: '_full',   // no such key → DomainTool shows the full JSON consensus result
    submitLabel: 'Reach consensus',
    fields: [
      { name: 'claims', label: 'Claims (claim | confidence | reputation, one per line)', type: 'claims', default: 'halal supply is verified | 0.95 | 2\nprice is optimal | 0.4 | 1' },
      { name: 'threshold', label: 'Threshold', type: 'text', default: '0.85' },
    ],
  },
};

// ── Component ─────────────────────────────────────────────────────────────────

export const ResourceFabric: React.FC = () => {
  const navigate = useNavigate();
  const [resources, setResources] = useState<Resource[]>([]);
  const [usageAreas, setUsageAreas] = useState<string[]>([]);
  const [classes, setClasses] = useState<Record<string, number>>({});
  const [filterArea, setFilterArea] = useState<string>('');
  const [filterClass, setFilterClass] = useState<string>('');
  const [selected, setSelected] = useState<string[]>([]);
  const [name, setName] = useState('');
  const [actErr, setActErr] = useState('');   // W344 — actions never fail silently
  const [usageArea, setUsageArea] = useState('synthesis');
  const [composing, setComposing] = useState(false);
  const [compositions, setCompositions] = useState<Composition[]>([]);
  const [runningId, setRunningId] = useState<string | null>(null);
  const [sim, setSim] = useState<Simulation | null>(null);   // §7 — model & simulate before commit
  const [simulating, setSimulating] = useState(false);
  // §7 — user design control over each resource's reconfigurable parameters: {resourceId: {param: value}}
  const [paramConfig, setParamConfig] = useState<Record<string, Record<string, string>>>({});
  // §7↔§6↔§5 — run a saved composition on the native swarm
  const [runCompId, setRunCompId] = useState<string | null>(null);
  const [runObjective, setRunObjective] = useState('');
  const [runResult, setRunResult] = useState<CompositionRun | null>(null);
  const [runningComp, setRunningComp] = useState(false);
  // W284 — per-RUN params (previously shown as "Params to set on run" but silently dropped),
  // living-design lifecycle (save-to-design PUT / DELETE), and the persisted runs history.
  const [runParams, setRunParams] = useState<Record<string, Record<string, string>>>({});
  const [savingParams, setSavingParams] = useState(false);
  const [histOpen, setHistOpen] = useState(false);
  const [histRuns, setHistRuns] = useState<HistoryRun[]>([]);

  const load = () => {
    const qs = new URLSearchParams();
    if (filterClass) qs.set('resource_class', filterClass);
    if (filterArea) qs.set('usable_in', filterArea);
    fetch(`/api/v1/resources?${qs.toString()}`).then(r => r.json()).then(d => {
      setResources(d.resources ?? []);
      setUsageAreas(d.usage_areas ?? []);
      setClasses(d.classes ?? {});
    }).catch(() => {});
  };
  const loadCompositions = () =>
    fetch('/api/v1/resources/compositions').then(r => r.json())
      .then(d => setCompositions(d.compositions ?? [])).catch(() => {});

  useEffect(() => { load(); }, [filterArea, filterClass]);
  useEffect(() => { loadCompositions(); }, []);

  const toggle = (id: string) =>
    setSelected(s => { setSim(null); return s.includes(id) ? s.filter(x => x !== id) : [...s, id]; });

  // set a reconfigurable parameter value for a resource (user design control); invalidates the preview
  const setParam = (rid: string, key: string, val: string) => {
    setSim(null);
    setParamConfig(pc => ({ ...pc, [rid]: { ...(pc[rid] || {}), [key]: val } }));
  };
  // only send params the user actually set (non-empty) so `unset_params` stays honest
  const buildConfig = (): Record<string, Record<string, string>> => {
    const out: Record<string, Record<string, string>> = {};
    selected.forEach(rid => {
      const entries = Object.entries(paramConfig[rid] || {}).filter(([, v]) => String(v).trim() !== '');
      if (entries.length) out[rid] = Object.fromEntries(entries);
    });
    return out;
  };

  // §7 — model & SIMULATE the configuration before commit (gated by the living QMS)
  const simulate = async () => {
    if (selected.length === 0) return;
    setSimulating(true); setSim(null);
    try {
      const r = await fetch('/api/v1/resources/compose/simulate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name || '(unnamed)', resource_ids: selected, usage_area: usageArea, config: buildConfig() }),
      });
      setSim(await r.json());
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setSimulating(false);
  };

  // W284 — only params the user actually typed reach the request (empty strings dropped)
  const cleanRunParams = () => {
    const out: Record<string, Record<string, string>> = {};
    for (const [rid, ps] of Object.entries(runParams)) {
      const kept = Object.fromEntries(Object.entries(ps).filter(([, v]) => v.trim() !== ''));
      if (Object.keys(kept).length) out[rid] = kept;
    }
    return Object.keys(out).length ? out : undefined;
  };

  // §7↔§6↔§5 — run a saved configuration end-to-end on Workstation's OWN native swarm.
  // W284 FIX: the per-run params the UI collects are now genuinely SENT (they were dropped).
  const runComposition = async (cid: string) => {
    setRunningComp(true); setRunResult(null);
    try {
      const r = await fetch(`/api/v1/resources/compositions/${cid}/run`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objective: runObjective || undefined, params: cleanRunParams() }),
      });
      setRunResult(await r.json());
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setRunningComp(false);
  };

  // W273/W284 — the saved design is LIVING: persist the entered params onto it (re-simulated,
  // version bumps server-side), or retire it entirely.
  const saveParamsToDesign = async (cid: string) => {
    const cfg = cleanRunParams();
    if (!cfg) return;
    setSavingParams(true);
    try {
      await fetch(`/api/v1/resources/compositions/${cid}`, {
        method: 'PUT', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config: cfg }),
      });
      loadCompositions();
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setSavingParams(false);
  };

  const deleteComposition = async (cid: string) => {
    try {
      await fetch(`/api/v1/resources/compositions/${cid}`, { method: 'DELETE' });
      if (runCompId === cid) setRunCompId(null);
      loadCompositions();
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
  };

  const loadRunsHistory = () =>
    fetch('/api/v1/resources/compositions/runs?limit=10').then(r => r.json())
      .then(d => setHistRuns(d.runs ?? [])).catch(() => {});

  const compose = async () => {
    if (!name.trim() || selected.length === 0) return;
    setComposing(true);
    try {
      await fetch('/api/v1/resources/compose', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, resource_ids: selected, usage_area: usageArea, config: buildConfig() }),
      });
      setName(''); setSelected([]); setSim(null); setParamConfig({});
      loadCompositions();
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setComposing(false);
  };

  return (
    <div className="space-y-10 pb-24">
      {actErr && <p className="text-vital text-xs font-bold">{actErr}</p>}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Resource Fabric</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Resource Fabric</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Every resource of the organism — process-intelligence engines, reactors, factories, incubators,
          labs, twins, organism systems, and the enterprise org — in one place to
          <span className="text-highlight"> select, reconfigure, combine, and model &amp; simulate before commit</span> across
          Synthesis, Design, Development, Delivery, Build-to-Order, and the Forge.
        </p>
      </header>

      {/* Process-intelligence studios — every engine, one click from the hub (keeps the nav lean) */}
      <div>
        <div className="flex items-center gap-3 mb-3">
          <Cpu size={16} className="text-highlight" />
          <h3 className="text-[10px] font-black uppercase tracking-[0.25em] text-slate-400">Process-Intelligence Studios</h3>
          <span className="text-[9px] font-mono text-slate-600">{STUDIOS.length} engines</span>
        </div>
        <div className="grid grid-cols-2 @[560px]:grid-cols-3 @[900px]:grid-cols-4 gap-3">
          {STUDIOS.map(s => (
            <button key={s.route} type="button" onClick={() => navigate(s.route)}
              className="group text-left p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-highlight/50 transition-all">
              <div className="flex items-center justify-between mb-2">
                <div className="w-8 h-8 rounded-xl bg-highlight/10 flex items-center justify-center"><s.icon size={14} className="text-highlight" /></div>
                <ArrowRight size={13} className="text-slate-600 group-hover:text-highlight transition-colors" />
              </div>
              <p className="font-black text-white text-xs">{s.name}</p>
              <p className="text-[10px] text-slate-500 leading-snug mt-0.5">{s.desc}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Filters */}
      <Card className="p-6 space-y-4">
        <div>
          <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2">Usage Area</p>
          <div className="flex flex-wrap gap-2">
            <FilterChip active={filterArea === ''} onClick={() => setFilterArea('')} label="All" />
            {usageAreas.map(a => <FilterChip key={a} active={filterArea === a} onClick={() => setFilterArea(a)} label={a.replace(/_/g, ' ')} />)}
          </div>
        </div>
        <div>
          <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2">Class</p>
          <div className="flex flex-wrap gap-2">
            <FilterChip active={filterClass === ''} onClick={() => setFilterClass('')} label="All" />
            {Object.keys(classes).map(k => <FilterChip key={k} active={filterClass === k} onClick={() => setFilterClass(k)} label={`${CLASS_LABEL[k] ?? k} (${classes[k]})`} />)}
          </div>
        </div>
      </Card>

      {/* Resource grid */}
      <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-4">
        {resources.map(r => {
          const Icon = CLASS_ICON[r.resource_class] ?? Boxes;
          const sel = selected.includes(r.id);
          const runnable = !!RUN_CONFIGS[r.id];
          return (
            <div key={r.id} className="relative">
              <button type="button" onClick={() => toggle(r.id)}
                className={`w-full h-full text-left p-5 rounded-2xl border transition-all ${sel ? 'bg-highlight/10 border-highlight/50' : 'bg-slate-900 border-slate-800 hover:border-slate-700'}`}>
                <div className="flex items-start justify-between mb-2">
                  <div className="w-9 h-9 rounded-xl bg-highlight/10 flex items-center justify-center"><Icon size={15} className="text-highlight" /></div>
                  <div className={`w-5 h-5 rounded-md border flex items-center justify-center ${sel ? 'bg-highlight border-highlight' : 'border-slate-700'}`}>
                    {sel && <Check size={12} className="text-sovereign" />}
                  </div>
                </div>
                <p className="font-black text-white text-sm">{r.name}</p>
                <p className="text-[9px] font-black uppercase tracking-wider text-slate-500 mt-0.5">{CLASS_LABEL[r.resource_class] ?? r.resource_class} · {r.type}</p>
                <p className="text-[11px] text-slate-500 leading-relaxed mt-2">{r.description}</p>
                <div className="flex flex-wrap gap-1 mt-3">
                  {r.biomimetic && <Tag tone="aura">biomimetic</Tag>}
                  {r.reusable && <Tag>reusable</Tag>}
                  {r.rerunnable && <Tag>rerunnable</Tag>}
                </div>
                <p className="text-[8px] font-mono text-slate-600 mt-2 mb-6">{r.usable_in.join(' · ')}</p>
              </button>
              {runnable && (
                <button type="button" onClick={() => setRunningId(r.id)}
                  className="absolute bottom-3 right-3 px-2.5 py-1 rounded-lg bg-aura/20 text-aura text-[9px] font-black uppercase tracking-widest flex items-center gap-1 hover:bg-aura/30 transition-all">
                  <Play size={10} /> Run
                </button>
              )}
            </div>
          );
        })}
      </div>

      {/* Inline run panel — run a surfaced resource on Workstation's OWN in-house engines */}
      {runningId && RUN_CONFIGS[runningId] && (
        <Card className="p-6 border-aura/30 bg-aura/5">
          <div className="flex items-center justify-between mb-5">
            <h3 className="font-black text-aura uppercase tracking-widest text-sm flex items-center gap-2">
              <Play size={14} /> Run · {resources.find(r => r.id === runningId)?.name ?? runningId}
            </h3>
            <button type="button" onClick={() => setRunningId(null)} className="text-slate-500 hover:text-white"><X size={16} /></button>
          </div>
          <DomainTool {...RUN_CONFIGS[runningId]} />
        </Card>
      )}

      {/* Compose tray */}
      <Card className="p-6 border-highlight/30 bg-highlight/5 sticky bottom-4">
        <div className="flex items-center gap-3 mb-4">
          <Layers size={16} className="text-highlight" />
          <h3 className="font-black text-highlight uppercase tracking-widest text-sm">Compose Combination</h3>
          <span className="text-[10px] font-mono text-slate-500 ml-auto">{selected.length} selected</span>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <input value={name} onChange={e => setName(e.target.value)} placeholder="Composition name…"
            className="flex-1 min-w-[200px] bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
          <select value={usageArea} onChange={e => { setUsageArea(e.target.value); setSim(null); }}
            className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-highlight/50">
            {usageAreas.map(a => <option key={a} value={a}>{a.replace(/_/g, ' ')}</option>)}
          </select>
          <Button onClick={simulate} disabled={simulating || selected.length === 0} className="flex items-center gap-2 bg-slate-800 text-highlight">
            {simulating ? <Loader2 size={16} className="animate-spin" /> : <FlaskConical size={16} />}
            Model &amp; Simulate
          </Button>
          <Button onClick={compose} disabled={composing || !name.trim() || selected.length === 0} className="flex items-center gap-2 bg-highlight text-sovereign">
            {composing ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            Compose
          </Button>
        </div>

        {/* §7 — user design control: reconfigure each selected resource's parameters before commit */}
        {selected.length > 0 && (
          <details className="mt-4 bg-slate-950/60 rounded-2xl border border-slate-800">
            <summary className="cursor-pointer px-4 py-2 text-[9px] font-black uppercase tracking-widest text-slate-400">
              Configure parameters ({selected.length} selected) — user design control
            </summary>
            <div className="px-4 pb-4 space-y-3">
              {selected.map(id => {
                const r = resources.find(x => x.id === id);
                if (!r) return null;
                const params = Object.entries(r.reconfigurable_params || {});
                return (
                  <div key={id} className="border-t border-slate-800/60 pt-2 first:border-t-0">
                    <p className="text-[10px] font-black text-white mb-1.5">{r.name}</p>
                    {params.length === 0 ? (
                      <p className="text-[9px] text-slate-600 italic">No reconfigurable parameters.</p>
                    ) : (
                      <div className="flex flex-wrap gap-2">
                        {params.map(([key, type]) => (
                          <input key={key} value={(paramConfig[id] || {})[key] ?? ''}
                            onChange={e => setParam(id, key, e.target.value)}
                            placeholder={`${key} (${type})`}
                            className="text-[10px] bg-slate-900 border border-slate-800 rounded-lg px-2 py-1 text-white placeholder:text-slate-600 min-w-[150px] focus:outline-none focus:border-highlight/50" />
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
              <p className="text-[8px] text-slate-600 italic">Set values, then Model &amp; Simulate — the model shows which parameters remain unset.</p>
            </div>
          </details>
        )}

        {/* §7 — the platform models + simulates the configuration BEFORE commit (gated by the living QMS) */}
        {sim && sim.model && (
          <div className="mt-4 p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[9px] font-black uppercase tracking-widest text-highlight">Modelled &amp; simulated before commit</span>
              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${sim.commit_ready ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                {sim.commit_ready ? 'commit-ready' : 'not commit-ready'}
              </span>
              {typeof sim.simulation?.quality?.qms_gate_passed === 'boolean' && (
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${sim.simulation.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                  title={`§10 quality bar: ${(sim.simulation.quality.bar || []).join(' · ')}`}>
                  QMS gate: {sim.simulation.quality.qms_gate_passed ? 'pass' : 'fail'} · cov {Math.round((sim.simulation.quality.delivery_coverage || 0) * 100)}%{sim.simulation.quality.document_controlled ? ' · doc-controlled' : ''}
                </span>
              )}
              {sim.simulation?.biomimetic?.immune && (
                <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-violet-500/15 text-violet-300">
                  organism: immune {Math.round((sim.simulation.biomimetic.immune.health ?? 0) * 100)}% · {sim.simulation.biomimetic.circadian}
                </span>
              )}
              {sim.simulation?.quality?.compliance && (
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${sim.simulation.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                  title={`§11 live compliance — ${(sim.simulation.quality.compliance.verdicts || []).map(v => `${v.framework}:${v.status}`).join(' · ')}`}>
                  compliance: {sim.simulation.quality.compliance.overall}
                </span>
              )}
              {sim.model.organism_capacity && (
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${sim.model.organism_capacity.fits_current_capacity ? 'bg-violet-500/15 text-violet-300' : 'bg-amber-500/15 text-amber-400'}`}
                  title={`§8 living-organism capacity now — mode ${sim.model.organism_capacity.organism?.mode}, ATP ${Math.round((sim.model.organism_capacity.organism?.atp_ratio ?? 0) * 100)}%, ${sim.model.organism_capacity.organism?.circadian}. The run will be homeostatically governed at execution time.`}>
                  §8 capacity: {sim.model.organism_capacity.projected_posture} · admits {sim.model.organism_capacity.admitted_max_parallel} {sim.model.organism_capacity.fits_current_capacity ? '· fits' : '· over capacity'}
                </span>
              )}
            </div>
            <p className="text-[10px] text-slate-400"><span className="text-slate-600 font-black uppercase">Pipeline:</span> {sim.model.pipeline.join(' → ')}</p>
            <p className="text-[10px] text-slate-400"><span className="text-slate-600 font-black uppercase">Combined capabilities ({sim.model.combined_capabilities.length}):</span> {sim.model.combined_capabilities.slice(0, 12).join(' · ')}{sim.model.combined_capabilities.length > 12 ? ' …' : ''}</p>
            {sim.model.incompatibilities.length > 0 && (
              <p className="text-[10px] text-vital"><span className="font-black uppercase">Incompatible with “{sim.usage_area}”:</span> {sim.model.incompatibilities.map(i => i.name).join(', ')} — change the usage area or remove these.</p>
            )}
            {Object.keys(sim.model.unset_params).length > 0 && (
              <p className="text-[9px] text-slate-500"><span className="text-slate-600 font-black uppercase">Params to set on run:</span> {Object.entries(sim.model.unset_params).map(([rid, ps]) => `${rid}: ${ps.join(', ')}`).join(' · ')}</p>
            )}
            {sim.note && <p className="text-[9px] text-slate-600 italic">{sim.note}</p>}
          </div>
        )}
      </Card>

      {/* Saved compositions */}
      {compositions.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <Recycle size={16} className="text-highlight" />
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Reusable Compositions</h3>
            {/* W274/W284 — 'rerunnable, reusable' includes the EVIDENCE of past runs */}
            <button type="button"
              onClick={() => { const o = !histOpen; setHistOpen(o); if (o) loadRunsHistory(); }}
              className="text-[9px] font-black uppercase text-slate-500 border border-slate-700 px-2 py-0.5 rounded-lg hover:text-highlight hover:border-highlight/40 transition-colors">
              {histOpen ? 'Hide run history' : 'Run history'}
            </button>
          </div>
          {histOpen && (
            <Card className="p-4 space-y-2">
              <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">Persisted composition runs (newest first)</p>
              {histRuns.length === 0 && <p className="text-[10px] text-slate-600 italic">No persisted runs yet — run a composition below.</p>}
              {histRuns.map(h => (
                <div key={h.run_id} className="flex flex-wrap items-center gap-1.5 border-t border-slate-800 first:border-t-0 pt-1.5 first:pt-0">
                  <span className="text-[9px] font-mono text-slate-500">{h.run_id}</span>
                  <span className="text-[10px] font-black text-white">{h.name}</span>
                  {typeof h.qms_gate_passed === 'boolean' && (
                    <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${h.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>QMS {h.qms_gate_passed ? 'pass' : 'fail'}</span>
                  )}
                  {(h.real_resources ?? []).map(rr => (
                    <span key={rr.resource} className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/10 text-aura">{rr.resource}</span>
                  ))}
                  {h.plan_binding?.result && (
                    <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${h.plan_binding.advanced ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>plan: {h.plan_binding.result}</span>
                  )}
                  <span className="text-[8px] text-slate-600 ml-auto">{h.created_at}</span>
                </div>
              ))}
            </Card>
          )}
          {compositions.slice().reverse().map(c => (
            <Card key={c.id} className="p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-black text-white text-sm">{c.name}</p>
                  <p className="text-[9px] font-black uppercase text-slate-500 mt-0.5">{c.usage_area} · {c.resources.length} resources · {c.id}{c.version ? ` · v${c.version}` : ''}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button type="button"
                    onClick={() => { setRunCompId(runCompId === c.id ? null : c.id); setRunResult(null); setRunParams({}); }}
                    className="flex items-center gap-1.5 text-[9px] font-black uppercase text-highlight border border-highlight/40 px-2.5 py-1 rounded-lg hover:bg-highlight/10 transition-colors">
                    <Play size={11} /> Run
                  </button>
                  {/* W273/W284 — retire a design (the lifecycle is complete: compose · reconfigure · run · retire) */}
                  <button type="button" onClick={() => deleteComposition(c.id)} title="Retire this design"
                    className="text-[9px] font-black uppercase text-slate-500 border border-slate-700 px-2 py-1 rounded-lg hover:text-vital hover:border-vital/40 transition-colors">
                    ✕
                  </button>
                </div>
              </div>
              <div className="flex flex-wrap gap-1.5 mt-3">
                {c.resources.map(r => <Tag key={r.id}>{r.name}</Tag>)}
              </div>

              {/* §7↔§6↔§5 — run this configuration end-to-end on Workstation's OWN native swarm */}
              {runCompId === c.id && (
                <div className="mt-4 p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
                  <p className="text-[9px] font-black uppercase tracking-widest text-highlight">Run on the native swarm (§6)</p>
                  <div className="flex flex-wrap items-center gap-2">
                    <input value={runObjective} onChange={e => setRunObjective(e.target.value)}
                      placeholder="Objective for this run (blank = default)…"
                      className="flex-1 min-w-[200px] text-[11px] bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
                    <Button onClick={() => runComposition(c.id)} disabled={runningComp} className="flex items-center gap-1.5 bg-highlight text-sovereign text-[11px]">
                      {runningComp ? <Loader2 size={13} className="animate-spin" /> : <Play size={13} />} Run pipeline
                    </Button>
                  </div>
                  {/* W284 FIX — the unset params are ENTERABLE and genuinely sent with the run
                      (previously the UI listed them but the request dropped them) */}
                  {c.model?.unset_params && Object.keys(c.model.unset_params).length > 0 && (
                    <div className="space-y-1.5">
                      <p className="text-[8px] font-black uppercase tracking-widest text-slate-500">Per-run parameters (blank = the design's defaults)</p>
                      {Object.entries(c.model.unset_params).map(([rid, ps]) => (
                        <div key={rid} className="flex flex-wrap items-center gap-1.5">
                          <span className="text-[9px] font-black uppercase text-slate-400 w-24 shrink-0">{rid}</span>
                          {ps.map(p => (
                            <input key={p} value={runParams[rid]?.[p] ?? ''}
                              onChange={e => setRunParams(rp => ({ ...rp, [rid]: { ...(rp[rid] ?? {}), [p]: e.target.value } }))}
                              placeholder={p}
                              className="w-28 text-[10px] bg-slate-900 border border-slate-800 rounded px-2 py-1 text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
                          ))}
                        </div>
                      ))}
                      <button type="button" onClick={() => saveParamsToDesign(c.id)} disabled={savingParams}
                        className="text-[8px] font-black uppercase text-aura border border-aura/40 px-2 py-0.5 rounded hover:bg-aura/10 transition-colors">
                        {savingParams ? 'Saving…' : 'Save params to the design (re-simulates · version bumps)'}
                      </button>
                    </div>
                  )}
                  {runResult && runResult.composition_id === c.id && (
                    <div className="space-y-2">
                      {/* W273/W284 — run-time honesty surfaced: a failed pre-run simulation warns, never silently */}
                      {runResult.quality_warning && (
                        <p className="text-[9px] text-amber-400 border border-amber-500/30 bg-amber-500/5 rounded-lg px-2.5 py-1.5">{runResult.quality_warning}</p>
                      )}
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${!runResult.any_external ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                          {!runResult.any_external ? 'in-house' : 'external used'}
                        </span>
                        {(runResult.run_params_applied ?? []).length > 0 && (
                          <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/15 text-aura">per-run params: {runResult.run_params_applied!.join(' · ')}</span>
                        )}
                        {runResult.plan_binding && (
                          <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${runResult.plan_binding.advanced ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>
                            plan: {runResult.plan_binding.result}
                          </span>
                        )}
                        {typeof runResult.quality_assurance?.quality?.qms_gate_passed === 'boolean' && (
                          <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${runResult.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                            QMS gate: {runResult.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'}{runResult.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                          </span>
                        )}
                        {runResult.quality_assurance?.quality?.compliance && (
                          <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${runResult.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                            title={`§11 live compliance — ${(runResult.quality_assurance.quality.compliance.verdicts || []).map(v => `${v.framework}:${v.status}`).join(' · ')}`}>
                            compliance: {runResult.quality_assurance.quality.compliance.overall}
                          </span>
                        )}
                      </div>
                      {/* §7→§5→§6→§8 — the real Chief→Build-to-Order cascade also ran (org resource present) */}
                      {runResult.org_cascade && (
                        <div className="border border-highlight/30 bg-highlight/5 rounded-lg p-2.5 space-y-1">
                          <p className="text-[9px] font-black uppercase tracking-widest text-highlight">§5 Living Organisation · real Chief→Build-to-Order cascade ran</p>
                          {runResult.org_cascade.csuite_engaged && (
                            <p className="text-[9px] text-slate-400">C-Suite engaged (your design): <span className="text-white">{runResult.org_cascade.csuite_engaged.join(' · ')}</span> — each drives a CoE</p>
                          )}
                          <div className="flex flex-wrap items-center gap-1.5">
                            {(runResult.org_cascade.management_systems || []).map(m => (
                              <span key={m} className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{m}</span>
                            ))}
                            {runResult.org_cascade.homeostasis?.posture && (
                              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-violet-500/15 text-violet-300">§8 {runResult.org_cascade.homeostasis.posture}</span>
                            )}
                            {runResult.org_cascade.governance && (
                              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400">gov: {runResult.org_cascade.governance}</span>
                            )}
                            {runResult.org_cascade.ueg_hash && (
                              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300" title={runResult.org_cascade.ueg_hash}>§6 provenance sealed</span>
                            )}
                          </div>
                          {runResult.org_cascade.appraisals && (
                            <p className="text-[8px] text-slate-600">arms-length appraisals: {runResult.org_cascade.appraisals.length} tiers</p>
                          )}
                        </div>
                      )}
                      {(runResult.real_resource_runs || []).length > 0 && (
                        <div className="border border-aura/30 bg-aura/5 rounded-lg p-2.5 space-y-2">
                          <p className="text-[9px] font-black uppercase tracking-widest text-aura">§7 real engines ran · the composed resources executed their genuine logic</p>
                          {(runResult.real_resource_runs || []).map((rr, i) => (
                            <div key={i} className="border-t border-aura/10 first:border-t-0 pt-1.5 first:pt-0">
                              <div className="flex flex-wrap items-center gap-1.5">
                                <span className="text-[9px] font-black uppercase text-white">{rr.resource}</span>
                                {rr.ran && <span className="text-[8px] font-mono text-slate-600">{rr.ran}</span>}
                                {rr.error
                                  ? <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-vital/15 text-vital">error</span>
                                  : <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400">ran</span>}
                                {typeof rr.viable === 'boolean' && (
                                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${rr.viable ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>{rr.viable ? 'viable' : 'not viable'}{rr.passages ? ` · ${rr.passages}p` : ''}</span>
                                )}
                                {typeof rr.cognitive_primed === 'boolean' && (
                                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{rr.cognitive_primed ? 'cognitive-primed' : 'context-fed'}</span>
                                )}
                                {typeof rr.scenarios_run === 'number' && (
                                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{rr.scenarios_run} scenarios</span>
                                )}
                                {typeof rr.generations_run === 'number' && (
                                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{rr.generations_run} generations</span>
                                )}
                                {typeof rr.stages_run === 'number' && (
                                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{rr.stages_run} stages</span>
                                )}
                                {rr.served_by && (
                                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${rr.is_external ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}
                                    title="Which OWNED resource served (native floor · local Ollama model · opt-in external)">
                                    {provenanceBadge(rr.served_by, rr.is_external).label}
                                  </span>
                                )}
                              </div>
                              {(rr.output || rr.error) && (
                                <p className="text-[10px] text-slate-400 whitespace-pre-wrap leading-relaxed max-h-24 overflow-y-auto mt-1">{rr.error || rr.output}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                      {runResult.trace.map(t => (
                        <div key={t.step} className="border-t border-slate-800/60 pt-2">
                          <p className="text-[9px] font-black uppercase tracking-widest text-slate-400">{t.step}. {t.role} <span className="text-slate-600 font-mono normal-case">· {t.served_by}</span></p>
                          <p className="text-[10px] text-slate-400 whitespace-pre-wrap leading-relaxed max-h-24 overflow-y-auto">{t.output.slice(0, 360)}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const FilterChip: React.FC<{ active: boolean; onClick: () => void; label: string }> = ({ active, onClick, label }) => (
  <button type="button" onClick={onClick}
    className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${active ? 'bg-highlight/20 text-highlight border border-highlight/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}>
    {label}
  </button>
);

const Tag: React.FC<{ children: React.ReactNode; tone?: 'aura' }> = ({ children, tone }) => (
  <span className={`px-2 py-0.5 rounded-md text-[8px] font-black uppercase tracking-wider ${tone === 'aura' ? 'bg-aura/10 text-aura' : 'bg-slate-800 text-slate-400'}`}>
    {children}
  </span>
);
