import React from 'react';
import { motion } from 'framer-motion';
import { Package, ChevronRight, Settings2, Box, Cpu, Network } from 'lucide-react';
import { Card } from '@workstation/ui';
import { useStore } from '@workstation/shared';

export const BTOCatalog: React.FC = () => {
  const { products, setCurrentTab } = useStore();

  const getIcon = (category: string) => {
    switch (category) {
      case 'AGENT': return <Box size={32} />;
      case 'REACTOR': return <Cpu size={32} />;
      case 'REALM': return <Network size={32} />;
      default: return <Package size={32} />;
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
                <button className="flex items-center gap-2 px-6 py-3 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all text-xs uppercase tracking-widest shadow-lg shadow-aura/10">
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
          onClick={() => setCurrentTab('ceo')}
          className="px-10 py-5 bg-white text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-xl uppercase tracking-widest text-sm">
            Consult VSB AI CEO
          </button>
      </div>
    </div>
  );
};
