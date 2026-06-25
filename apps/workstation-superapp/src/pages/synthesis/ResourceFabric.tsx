import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Boxes, Cpu, FlaskConical, Factory, Dna, ShieldCheck, Layers,
  Check, Loader2, Sparkles, Recycle, Play, X,
} from 'lucide-react';
import { DomainTool } from '../../components/DomainTool';

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
}
interface Simulation {
  name: string; usage_area: string; commit_ready: boolean; saved: boolean; note?: string;
  model: {
    pipeline: string[]; combined_capabilities: string[]; resource_classes: Record<string, number>;
    biomimetic_resources: number; shared_usage_areas: string[]; usage_area_supported_by_all: boolean;
    incompatibilities: { id: string; name: string; reason: string }[];
    unset_params: Record<string, string[]>;
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
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean; verdicts?: { framework: string; status: string }[] } } };
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
  const [resources, setResources] = useState<Resource[]>([]);
  const [usageAreas, setUsageAreas] = useState<string[]>([]);
  const [classes, setClasses] = useState<Record<string, number>>({});
  const [filterArea, setFilterArea] = useState<string>('');
  const [filterClass, setFilterClass] = useState<string>('');
  const [selected, setSelected] = useState<string[]>([]);
  const [name, setName] = useState('');
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
    } catch { /* ignore */ }
    setSimulating(false);
  };

  // §7↔§6↔§5 — run a saved configuration end-to-end on Workstation's OWN native swarm
  const runComposition = async (cid: string) => {
    setRunningComp(true); setRunResult(null);
    try {
      const r = await fetch(`/api/v1/resources/compositions/${cid}/run`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objective: runObjective || undefined }),
      });
      setRunResult(await r.json());
    } catch { /* ignore */ }
    setRunningComp(false);
  };

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
    } catch { /* ignore */ }
    setComposing(false);
  };

  return (
    <div className="space-y-10 pb-24">
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
          </div>
          {compositions.slice().reverse().map(c => (
            <Card key={c.id} className="p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-black text-white text-sm">{c.name}</p>
                  <p className="text-[9px] font-black uppercase text-slate-500 mt-0.5">{c.usage_area} · {c.resources.length} resources · {c.id}</p>
                </div>
                <button type="button"
                  onClick={() => { setRunCompId(runCompId === c.id ? null : c.id); setRunResult(null); }}
                  className="flex items-center gap-1.5 text-[9px] font-black uppercase text-highlight border border-highlight/40 px-2.5 py-1 rounded-lg hover:bg-highlight/10 transition-colors">
                  <Play size={11} /> Run
                </button>
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
                  {runResult && runResult.composition_id === c.id && (
                    <div className="space-y-2">
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${!runResult.any_external ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                          {!runResult.any_external ? 'in-house' : 'external used'}
                        </span>
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
