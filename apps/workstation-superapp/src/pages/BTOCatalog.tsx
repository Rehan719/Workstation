import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Package, ChevronRight, Settings2, Box, Cpu, Network, CheckSquare, Square, Loader2,
  Fingerprint, Dna, Building2, Users, Award, Globe, Layers, ShoppingBag, Wrench, ExternalLink
} from 'lucide-react';
import { Card, Button } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const CONFIGURE_ROUTES: Record<string, string> = {
  AGENT: '/visual-composer',
  REACTOR: '/reactor',
  REALM: '/realm-editor',
};

const BTO_COMPONENTS = [
  { id: 'entity', label: 'Entity', icon: Fingerprint },
  { id: 'organism', label: 'Organism', icon: Dna },
  { id: 'vsb', label: 'Virtual Sovereign Business', icon: Building2 },
  { id: 'csuite', label: 'C-Suite', icon: Users },
  { id: 'coe', label: 'Centers of Excellence', icon: Award },
  { id: 'domains', label: 'Domains', icon: Globe },
  { id: 'realms', label: 'Realms', icon: Layers },
  { id: 'products', label: 'Products', icon: ShoppingBag },
  { id: 'services', label: 'Services', icon: Wrench },
];

export const BTOCatalog: React.FC = () => {
  const { products, setCurrentTab } = useStore();
  const navigate = useNavigate();

  const [entityName, setEntityName] = useState('');
  const [selectedComponents, setSelectedComponents] = useState<string[]>([]);
  const [building, setBuilding] = useState(false);
  const [blueprint, setBlueprint] = useState<any>(null);

  const getIcon = (category: string) => {
    switch (category) {
      case 'AGENT': return <Box size={32} />;
      case 'REACTOR': return <Cpu size={32} />;
      case 'REALM': return <Network size={32} />;
      default: return <Package size={32} />;
    }
  };

  const handleConfigure = (productId: string, category: string) => {
    const route = CONFIGURE_ROUTES[category] || '/forge';
    navigate(`${route}?product=${productId}`);
  };

  const toggleComponent = (id: string) => {
    setSelectedComponents(prev => prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]);
  };

  const allSelected = selectedComponents.length === BTO_COMPONENTS.length;
  const toggleSelectAll = () => {
    setSelectedComponents(allSelected ? [] : BTO_COMPONENTS.map(c => c.id));
  };

  const handleBuild = async () => {
    if (selectedComponents.length === 0) return alert('Select at least one component to build.');
    setBuilding(true);
    setBlueprint(null);
    try {
      const resp = await axios.post('/api/v1/bto/configure', {
        entity_name: entityName || 'Unnamed Entity',
        components: selectedComponents,
      });
      setBlueprint(resp.data);
    } catch (e) {
      alert('Build failed.');
    } finally {
      setBuilding(false);
    }
  };

  return (
    <div className="space-y-12 pb-24">
      <header>
        <h1 className="text-5xl font-black mb-3 tracking-tight">Build-to-Order Catalog</h1>
        <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
          Configure and deploy custom agentic infrastructure across the <span className="text-aura">Sovereign Mesh</span>.
        </p>
      </header>

      <Card className="p-8 border-slate-900 bg-slate-950/40 space-y-6">
        <h3 className="text-sm font-black text-white uppercase tracking-widest">BTO Configurator</h3>
        <div className="space-y-2">
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Entity Name</label>
          <input
            value={entityName}
            onChange={(e) => setEntityName(e.target.value)}
            placeholder="Name your Sovereign Digital Entity..."
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura"
          />
        </div>
        <div className="flex items-center justify-between">
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Components ({selectedComponents.length} selected)</label>
          <button
            type="button"
            onClick={toggleSelectAll}
            className="flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest text-aura hover:text-white transition-colors"
          >
            {allSelected ? <CheckSquare size={12} /> : <Square size={12} />}
            {allSelected ? 'Clear All' : 'Select All'}
          </button>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
          {BTO_COMPONENTS.map(c => {
            const active = selectedComponents.includes(c.id);
            const activeClass = 'p-3 rounded-2xl border flex flex-col items-center gap-2 transition-all bg-aura text-sovereign border-aura';
            const inactiveClass = 'p-3 rounded-2xl border flex flex-col items-center gap-2 transition-all bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700';
            return active ? (
              <button type="button" key={c.id} onClick={() => toggleComponent(c.id)} aria-pressed="true" className={activeClass}>
                <c.icon size={18} />
                <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{c.label}</span>
              </button>
            ) : (
              <button type="button" key={c.id} onClick={() => toggleComponent(c.id)} aria-pressed="false" className={inactiveClass}>
                <c.icon size={18} />
                <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{c.label}</span>
              </button>
            );
          })}
        </div>
        <Button
          onClick={handleBuild}
          disabled={building || selectedComponents.length === 0}
          className="w-full bg-white text-sovereign py-6 shadow-2xl shadow-white/5"
        >
          {building ? <Loader2 className="animate-spin mr-2" /> : <Settings2 className="mr-2" size={18} />}
          {building ? 'Provisioning...' : `Build Entity${selectedComponents.length > 1 ? ` (${selectedComponents.length} components)` : ''}`}
        </Button>

        {blueprint && (
          <div className="pt-6 border-t border-slate-800 space-y-4">
            <p className="text-[10px] font-black text-aura uppercase tracking-widest">Blueprint: {blueprint.entity_name} ({blueprint.blueprint_id.slice(0, 8)})</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(blueprint.components).map(([key, data]: [string, any]) => {
                const meta = BTO_COMPONENTS.find(c => c.id === key);
                return (
                  <div key={key} className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-start justify-between gap-4">
                    <div>
                      <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">{meta?.label || key}</p>
                      <p className="text-xs text-slate-300 font-bold">
                        {data.status || data.type || data.name || (Array.isArray(data.available) ? data.available.join(', ') : 'Configured')}
                      </p>
                    </div>
                    {data.route && (
                      <button
                        type="button"
                        onClick={() => navigate(data.route)}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-aura text-sovereign rounded-lg text-[9px] font-black uppercase tracking-widest shrink-0"
                      >
                        Launch <ExternalLink size={10} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {products.map((product) => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="h-full flex flex-col group hover:border-aura/50 transition-all">
              <div className="flex justify-between items-start mb-8">
                <div className="p-4 rounded-2xl bg-slate-800/50 text-aura group-hover:scale-110 transition-transform">
                  {getIcon(product.category)}
                </div>
                <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-slate-950 text-slate-500 border border-slate-900 uppercase tracking-widest">
                  {product.category}
                </span>
              </div>

              <h3 className="text-2xl font-black mb-3 text-white">{product.name}</h3>
              <p className="text-slate-500 font-bold text-sm mb-8 flex-1 leading-relaxed">
                {product.description}
              </p>

              <div className="space-y-4 mb-8">
                 {Object.entries(product.specs).map(([k, v]) => (
                   <div key={k} className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-slate-600">
                      <span>{k}</span>
                      <span className="text-slate-400">{v}</span>
                   </div>
                 ))}
              </div>

              <div className="flex items-end justify-between mt-auto pt-6 border-t border-slate-800/50">
                <div>
                  <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-1">Cost</p>
                  <p className="text-2xl font-black text-white">{product.price}</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleConfigure(product.id, product.category)}
                  className="flex items-center gap-2 px-6 py-3 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all text-xs uppercase tracking-widest shadow-lg shadow-aura/10"
                >
                  <Settings2 size={16} />
                  Configure
                  <ChevronRight size={16} />
                </button>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="p-12 rounded-3xl bg-aura/5 border border-aura/20 backdrop-blur-sm text-center">
         <h3 className="text-2xl font-black mb-4">Need a custom solution?</h3>
         <p className="text-slate-400 font-bold mb-8 max-w-xl mx-auto">Our C-Suite agents can assist in architecting specialized reactors for high-throughput enterprise swarm coordination.</p>
         <button
          type="button"
          onClick={() => { setCurrentTab('ceo'); navigate('/ceo'); }}
          className="px-10 py-5 bg-white text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-xl uppercase tracking-widest text-sm">
            Consult VSB AI CEO
          </button>
      </div>
    </div>
  );
};
