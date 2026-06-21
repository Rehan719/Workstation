import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Boxes, Cpu, FlaskConical, Factory, Dna, ShieldCheck, Layers,
  Check, Loader2, Sparkles, Recycle, RefreshCw,
} from 'lucide-react';

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

const CLASS_ICON: Record<string, React.ComponentType<any>> = {
  process_intelligence: Cpu, digital_resource: FlaskConical,
  organism_system: Dna, enterprise_org: Factory,
};
const CLASS_LABEL: Record<string, string> = {
  process_intelligence: 'Process Intelligence', digital_resource: 'Digital Resource',
  organism_system: 'Organism System', enterprise_org: 'Enterprise / Org',
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
    setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id]);

  const compose = async () => {
    if (!name.trim() || selected.length === 0) return;
    setComposing(true);
    try {
      await fetch('/api/v1/resources/compose', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, resource_ids: selected, usage_area: usageArea }),
      });
      setName(''); setSelected([]);
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
          <span className="text-highlight"> select, reconfigure, and combine</span> across Synthesis, Design,
          Development, Delivery, Build-to-Order, and the Forge.
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
          return (
            <button key={r.id} type="button" onClick={() => toggle(r.id)}
              className={`text-left p-5 rounded-2xl border transition-all ${sel ? 'bg-highlight/10 border-highlight/50' : 'bg-slate-900 border-slate-800 hover:border-slate-700'}`}>
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
              <p className="text-[8px] font-mono text-slate-600 mt-2">{r.usable_in.join(' · ')}</p>
            </button>
          );
        })}
      </div>

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
          <select value={usageArea} onChange={e => setUsageArea(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-highlight/50">
            {usageAreas.map(a => <option key={a} value={a}>{a.replace(/_/g, ' ')}</option>)}
          </select>
          <Button onClick={compose} disabled={composing || !name.trim() || selected.length === 0} className="flex items-center gap-2 bg-highlight text-sovereign">
            {composing ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            Compose
          </Button>
        </div>
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
                <div className="flex items-center gap-1.5 text-[9px] font-black uppercase text-emerald-400">
                  <RefreshCw size={11} /> rerunnable
                </div>
              </div>
              <div className="flex flex-wrap gap-1.5 mt-3">
                {c.resources.map(r => <Tag key={r.id}>{r.name}</Tag>)}
              </div>
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
