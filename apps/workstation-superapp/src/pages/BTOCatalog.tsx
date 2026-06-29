import React, { useState } from 'react';
import {
  Settings2, Fingerprint, Dna, Building2, Users, Award, Globe,
  ShoppingBag, Wrench, Box, Cpu, CheckSquare, Square,
  ChevronDown, ChevronUp, MessageSquare, Loader2, ExternalLink,
  Sparkles, Layers, Package,
} from 'lucide-react';
import { Card } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useNavigate } from 'react-router-dom';
import { FabricLink } from '../components/FabricLink';
import axios from 'axios';

// ── BTO component registry ────────────────────────────────────────────────────

const BTO_COMPONENTS = [
  { id: 'entity',   label: 'Entity',                    icon: Fingerprint, desc: 'Sovereign Digital Identity · L1 Core' },
  { id: 'organism', label: 'Organism',                   icon: Dna,         desc: 'Full L1–L12 Multi-Layer Fabric' },
  { id: 'vsb',      label: 'Virtual Sovereign Business', icon: Building2,   desc: 'AI CEO + Autonomous Operations' },
  { id: 'csuite',   label: 'C-Suite',                    icon: Users,       desc: 'CFO · CTO · CMO · COO Agents' },
  { id: 'coe',      label: 'Centers of Excellence',      icon: Award,       desc: 'Security · Ethics · QA · Compliance' },
  { id: 'domains',  label: 'Domains',                    icon: Globe,       desc: 'Religion · Science · Law · Care · Education' },
  { id: 'realms',   label: 'Realms',                     icon: Layers,      desc: 'Learner · Developer · Enterprise · Scholar' },
  { id: 'products', label: 'Products',                   icon: ShoppingBag, desc: 'Full BTO Product Catalog access' },
  { id: 'services', label: 'Services',                   icon: Wrench,      desc: 'Synthesis Studio · Capital · Marketplace' },
] as const;

type ComponentId = typeof BTO_COMPONENTS[number]['id'];

// ── Component ─────────────────────────────────────────────────────────────────

export const BTOCatalog: React.FC = () => {
  const { setCurrentTab } = useStore();
  const navigate = useNavigate();

  const [entityName, setEntityName]             = useState('');
  const [selectedComponents, setSelectedComponents] = useState<ComponentId[]>([]);
  const [building, setBuilding]                 = useState(false);
  const [blueprint, setBlueprint]               = useState<any>(null);
  const [expandedKeys, setExpandedKeys]         = useState<Set<string>>(new Set());
  const [errorMsg, setErrorMsg]                 = useState<string | null>(null);
  // §13 real Build-to-Order: produce genuine deliverables for the blueprint's catalog products
  const [btoBuilding, setBtoBuilding]           = useState(false);
  const [btoResult, setBtoResult]               = useState<any>(null);

  // ── Helpers ───────────────────────────────────────────────────────────────

  const toggleComponent = (id: ComponentId) =>
    setSelectedComponents(prev =>
      prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
    );

  const allSelected = selectedComponents.length === BTO_COMPONENTS.length;
  const toggleAll   = () =>
    setSelectedComponents(allSelected ? [] : BTO_COMPONENTS.map(c => c.id) as ComponentId[]);

  const toggleExpand = (key: string) =>
    setExpandedKeys(prev => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  const handleBuild = async () => {
    if (selectedComponents.length === 0) {
      setErrorMsg('Select at least one infrastructure component to build.');
      return;
    }
    setErrorMsg(null);
    setBuilding(true);
    setBlueprint(null);
    setExpandedKeys(new Set());
    try {
      const resp = await axios.post('/api/v1/bto/configure', {
        entity_name: entityName.trim() || 'Sovereign Entity',
        components: selectedComponents,
        product_resources: [],
      });
      setBlueprint(resp.data);
      setExpandedKeys(new Set(Object.keys(resp.data.components || {})));
    } catch {
      setErrorMsg('Build failed — check the API server is running.');
    } finally {
      setBuilding(false);
    }
  };

  const handleBuildToOrder = async () => {
    const catalog = blueprint?.components?.products?.catalog;
    const list = Array.isArray(catalog) ? catalog : (catalog?.products || []);
    const slugs = list.map((p: any) => p.slug).filter(Boolean).slice(0, 3);   // bounded: build the first few
    if (slugs.length === 0) return;
    setBtoBuilding(true);
    setBtoResult(null);
    try {
      const resp = await axios.post('/api/v1/bto/build', {
        entity_name: blueprint.entity_name || 'Sovereign Entity',
        product_resources: slugs,
        objective: `Build-to-order delivery for ${blueprint.entity_name || 'Sovereign Entity'}`,
      });
      setBtoResult(resp.data);
    } catch {
      setErrorMsg('Build-to-Order failed — check the API server is running.');
    } finally {
      setBtoBuilding(false);
    }
  };

  const componentSummary = (data: any): string => {
    if (data.status && typeof data.status === 'string') return data.status;
    if (data.type)    return data.type;
    if (data.name)    return data.name;
    if (Array.isArray(data.layers))   return `${data.layers.length} layers`;
    if (Array.isArray(data.members))  return data.members.map((m: any) => m.role).join(', ');
    if (Array.isArray(data.centers))  return data.centers.slice(0, 3).join(', ');
    if (Array.isArray(data.available)) return data.available.slice(0, 3).join(', ') + (data.available.length > 3 ? '…' : '');
    return 'Configured';
  };

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-8 pb-10">

      {/* Header */}
      <header>
        <h1 className="text-3xl @[440px]:text-4xl @[900px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">
          Build-to-<span className="text-aura">Order</span>
        </h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">
          Sovereign Entity Configurator · Select components · Provision your blueprint
        </p>
        <div className="mt-3"><FabricLink /></div>
      </header>

      {/* Blueprint result card */}
      <Card className="p-8 border-slate-800 bg-slate-950/20 flex flex-col min-h-[260px]">
        {!blueprint && !building && (
          <div className="flex-1 flex flex-col items-center justify-center text-center gap-4">
            <div className="w-14 h-14 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
              <Box size={28} />
            </div>
            <div>
              <p className="text-base font-black text-slate-700 uppercase tracking-tighter italic">No Blueprint Active</p>
              <p className="text-xs text-slate-500 font-bold max-w-xs mx-auto mt-1">
                Select infrastructure components below, name your entity, then hit Build.
              </p>
            </div>
          </div>
        )}

        {building && (
          <div className="flex-1 flex flex-col items-center justify-center text-center gap-8">
            <div className="relative w-20 h-20">
              <div className="absolute inset-0 rounded-full border-2 border-aura/20 animate-ping" />
              <div className="w-20 h-20 rounded-full border-2 border-aura animate-spin border-t-transparent" />
            </div>
            <div>
              <p className="text-aura font-black uppercase tracking-[0.3em] text-xs">Provisioning Sovereign Infrastructure</p>
              <p className="text-slate-500 text-[10px] mt-1 font-bold uppercase tracking-widest italic animate-pulse">
                Bootstrapping L1–L12 fabric...
              </p>
            </div>
          </div>
        )}

        {blueprint && !building && (
          <div className="flex-1 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Blueprint header */}
            <div className="flex items-start gap-4 mb-6">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
                <Cpu size={18} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Blueprint Provisioned</p>
                <h3 className="text-xl font-black text-white uppercase tracking-tight">{blueprint.entity_name}</h3>
                <p className="text-[9px] text-aura font-mono mt-0.5">{blueprint.blueprint_id}</p>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-2xl font-black text-white">{blueprint.component_count}</p>
                <p className="text-[8px] text-slate-500 uppercase tracking-widest">Components</p>
              </div>
            </div>

            {/* Components grid */}
            <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-3">
              {Object.entries(blueprint.components || {}).map(([key, data]: [string, any]) => {
                const meta      = BTO_COMPONENTS.find(c => c.id === key);
                const Icon      = meta?.icon || Package;
                const isExpanded = expandedKeys.has(key);
                const summary   = componentSummary(data);
                return (
                  <div key={key} className="border border-slate-800 rounded-2xl overflow-hidden">
                    <div
                      className="flex items-center gap-3 p-4 cursor-pointer hover:bg-slate-900/40 transition-colors"
                      onClick={() => toggleExpand(key)}
                    >
                      <div className="w-8 h-8 rounded-lg bg-aura/10 flex items-center justify-center shrink-0">
                        <Icon size={14} className="text-aura" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-[9px] font-black text-aura uppercase tracking-widest">{meta?.label || key}</p>
                        <p className="text-xs text-slate-300 font-bold truncate">{summary}</p>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        {data.route && (
                          <button
                            type="button"
                            onClick={e => { e.stopPropagation(); navigate(data.route); }}
                            className="flex items-center gap-1 px-2.5 py-1.5 bg-aura text-sovereign rounded-lg text-[9px] font-black uppercase tracking-widest"
                          >
                            Launch <ExternalLink size={9} />
                          </button>
                        )}
                        {data.routes && (
                          <button
                            type="button"
                            onClick={e => { e.stopPropagation(); navigate(Object.values(data.routes as Record<string, string>)[0]); }}
                            className="flex items-center gap-1 px-2.5 py-1.5 bg-aura text-sovereign rounded-lg text-[9px] font-black uppercase tracking-widest"
                          >
                            Explore <ExternalLink size={9} />
                          </button>
                        )}
                        {isExpanded ? <ChevronUp size={13} className="text-slate-600" /> : <ChevronDown size={13} className="text-slate-600" />}
                      </div>
                    </div>
                    {isExpanded && (
                      <div className="border-t border-slate-800 px-4 py-3 bg-slate-950/40">
                        <pre className="text-[9px] text-slate-400 font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap break-words">
                          {JSON.stringify(data, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* §13 Build-to-Order — turn the catalog products in this blueprint into REAL deliverables */}
            {blueprint.components?.products && (
              <div className="mt-6 border border-aura/30 bg-aura/5 rounded-2xl p-4">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <div className="min-w-0">
                    <p className="text-[9px] font-black uppercase tracking-widest text-aura flex items-center gap-1.5"><Package size={12} /> Build-to-Order · real §13 delivery</p>
                    <p className="text-[10px] text-slate-500 font-bold mt-0.5">Produce genuine, QMS-gated deliverables for this blueprint's catalog products (first 3) on Workstation's own engines.</p>
                  </div>
                  <button
                    type="button"
                    onClick={handleBuildToOrder}
                    disabled={btoBuilding}
                    className={`flex items-center gap-2 px-4 py-2 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shrink-0 ${
                      btoBuilding ? 'bg-slate-800 text-slate-600 cursor-not-allowed' : 'bg-aura text-sovereign hover:scale-105 active:scale-95'}`}
                  >
                    {btoBuilding ? <Loader2 size={13} className="animate-spin" /> : <Wrench size={13} />}
                    {btoBuilding ? 'Building…' : 'Build to Order'}
                  </button>
                </div>
                {btoResult && (
                  <div className="mt-3 space-y-2">
                    <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">
                      Delivered <span className="text-emerald-400">{btoResult.delivered_count}</span> · {btoResult.posture}
                    </p>
                    {(btoResult.built || []).map((b: any, i: number) => (
                      <div key={i} className="flex items-center gap-2 p-2.5 rounded-lg bg-slate-950 border border-slate-900">
                        <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.status === 'BUILT' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>{b.status}</span>
                        <span className="text-xs font-bold text-white truncate flex-1">{b.name}</span>
                        {typeof b.qms_gate_passed === 'boolean' && (
                          <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>QMS {b.qms_gate_passed ? 'pass' : 'fail'}</span>
                        )}
                        {b.deliverable_id && (
                          <span className="text-[8px] font-mono text-aura shrink-0" title="Produced via the §13 living-deliverables engine">{b.deliverable_id}</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Reset */}
            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => { setBlueprint(null); setSelectedComponents([]); setEntityName(''); setExpandedKeys(new Set()); setErrorMsg(null); setBtoResult(null); }}
                className="text-[9px] font-black text-slate-600 hover:text-white uppercase tracking-widest transition-colors"
              >
                Reset Builder
              </button>
            </div>
          </div>
        )}
      </Card>

      {/* Error banner */}
      {errorMsg && (
        <div role="alert" className="flex items-center gap-3 px-4 py-3 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-400">
          <span className="text-xs font-bold flex-1">{errorMsg}</span>
          <button type="button" onClick={() => setErrorMsg(null)} aria-label="Dismiss error" title="Dismiss" className="text-red-400/60 hover:text-red-400 transition-colors shrink-0">✕</button>
        </div>
      )}

      {/* ── Composer ──────────────────────────────────────────────────────── */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">

        {/* Entity name */}
        <div className="px-5 py-4">
          <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em] mb-2">Entity Name</p>
          <input
            value={entityName}
            onChange={e => setEntityName(e.target.value)}
            placeholder="Name your Sovereign Digital Entity..."
            aria-label="Entity Name"
            className="w-full bg-transparent text-sm text-white placeholder-slate-600 outline-none font-medium leading-relaxed"
          />
        </div>

        <div className="border-t border-slate-800" />

        {/* Component grid */}
        <div className="px-5 py-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">
              Infrastructure Components
              {selectedComponents.length > 0 && (
                <span className="ml-2 text-aura">· {selectedComponents.length} of {BTO_COMPONENTS.length} selected</span>
              )}
            </span>
            <button
              type="button"
              onClick={toggleAll}
              {...({ 'aria-pressed': allSelected ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
              className="flex items-center gap-1 text-[9px] font-black text-slate-500 hover:text-white uppercase tracking-widest transition-colors"
            >
              {allSelected ? <CheckSquare size={11} className="text-aura" /> : <Square size={11} />}
              {allSelected ? 'Deselect All' : 'Select All'}
            </button>
          </div>

          <div className="grid grid-cols-3 @[420px]:grid-cols-5 gap-2">
            {BTO_COMPONENTS.map(c => {
              const active = selectedComponents.includes(c.id);
              return (
                <button
                  key={c.id}
                  type="button"
                  onClick={() => toggleComponent(c.id)}
                  title={c.desc}
                  {...({ 'aria-pressed': active ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
                  className={`flex flex-col items-center gap-1.5 p-3 rounded-2xl border text-center transition-all ${
                    active
                      ? 'bg-aura text-sovereign border-aura shadow-lg shadow-aura/10'
                      : 'bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'
                  }`}
                >
                  <c.icon size={15} />
                  <span className="text-[8px] font-black uppercase tracking-wide leading-tight">{c.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="border-t border-slate-800" />

        {/* Toolbar */}
        <div className="px-5 py-3 flex items-center gap-3 flex-wrap">
          <button
            type="button"
            onClick={() => { setCurrentTab('ceo'); navigate('/ceo'); }}
            className="flex items-center gap-1.5 px-3 py-2 rounded-2xl border bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600 text-[10px] font-black uppercase tracking-wider transition-all"
          >
            <MessageSquare size={12} /> Consult AI CEO
          </button>
          <button
            type="button"
            onClick={() => navigate('/marketplace?tab=products')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-2xl border bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600 text-[10px] font-black uppercase tracking-wider transition-all"
          >
            <ShoppingBag size={12} /> Browse Products
          </button>

          <div className="flex-1" />

          <button
            type="button"
            onClick={handleBuild}
            disabled={building || selectedComponents.length === 0}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all duration-150 ${
              !building && selectedComponents.length > 0
                ? 'bg-white text-sovereign shadow-lg shadow-white/10 hover:scale-105 active:scale-95'
                : 'bg-slate-800 text-slate-600 cursor-not-allowed'
            }`}
          >
            {building ? <Loader2 size={14} className="animate-spin" /> : <Settings2 size={14} />}
            {building
              ? 'Provisioning...'
              : `Build Entity${selectedComponents.length > 0 ? ` (${selectedComponents.length})` : ''}`
            }
          </button>
        </div>
      </div>

      {/* Info strip */}
      <div className="flex flex-wrap gap-4 text-[9px] font-black text-slate-700 uppercase tracking-widest">
        <span className="flex items-center gap-1.5"><Sparkles size={10} className="text-aura" /> AI-Mediated Provisioning</span>
        <span className="flex items-center gap-1.5"><Cpu size={10} className="text-aura" /> L1–L12 Sovereign Fabric</span>
        <span className="flex items-center gap-1.5"><Settings2 size={10} className="text-aura" /> {BTO_COMPONENTS.length} Infrastructure Modules</span>
      </div>
    </div>
  );
};
