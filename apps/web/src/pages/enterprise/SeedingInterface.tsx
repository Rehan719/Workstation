import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Rocket, Sparkles, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, LayoutGrid, Terminal, Database, Send, Network, Activity } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const SeedingInterface: React.FC = () => {
  const { user } = useStore();
  const [seedingStep, setSeedingStep] = useState(0);

  const targetEnvironments = [
    { id: 'env-1', name: 'Lunar-Lava-Tube', resources: 'Medium', constraint: 'Low-Gravity' },
    { id: 'env-2', name: 'Martian-Regolith', resources: 'High', constraint: 'Atmospheric-Shield' },
    { id: 'env-3', name: 'Europan-Subsurface', resources: 'Extreme', constraint: 'Pressure-Hardened' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Civilisation Seeding</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Autonomous Offspring Spawning • Deep Space NANITE Propagation</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Seed Records</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Sparkles size={18} /> Define New Seed
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Rocket size={24} className="text-aura" />
                     Seeding Wizard
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="aura">Phase 4 Active</Badge>
                     <Badge color="emerald-500">UEG Lineage Strict</Badge>
                  </div>
               </div>

               <div className="space-y-8">
                  <div className="flex justify-between px-10">
                     {['Target', 'Config', 'Genome', 'Launch'].map((step, i) => (
                        <div key={step} className="flex flex-col items-center gap-2">
                           <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center font-black text-xs transition-all ${seedingStep >= i ? 'bg-aura text-sovereign border-aura' : 'border-slate-800 text-slate-700'}`}>
                              {i + 1}
                           </div>
                           <span className={`text-[9px] font-black uppercase tracking-widest ${seedingStep >= i ? 'text-aura' : 'text-slate-700'}`}>{step}</span>
                        </div>
                     ))}
                  </div>

                  <AnimatePresence mode="wait">
                     <motion.div
                        key={seedingStep}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="p-10 rounded-[3rem] bg-slate-950 border border-slate-900"
                     >
                        {seedingStep === 0 && (
                           <div className="space-y-6">
                              <h4 className="text-lg font-black text-white uppercase tracking-widest">Select Target Environment</h4>
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                 {targetEnvironments.map(env => (
                                    <button key={env.id} onClick={() => setSeedingStep(1)} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-aura/50 transition-all text-left group">
                                       <p className="text-sm font-black text-white mb-2 uppercase">{env.name}</p>
                                       <Badge color="aura">{env.resources} Res</Badge>
                                    </button>
                                 ))}
                              </div>
                           </div>
                        )}
                        {seedingStep === 1 && (
                           <div className="space-y-6 text-center py-10">
                              <Zap size={48} className="text-aura mx-auto animate-pulse" />
                              <h4 className="text-xl font-black text-white uppercase">Synthesizing Offspring Genome...</h4>
                              <p className="text-sm text-slate-500 font-bold max-w-md mx-auto">Adapting L1-L12 layers for deep space autonomous governance.</p>
                              <Button onClick={() => setSeedingStep(2)} className="bg-white text-sovereign mt-6">Continue Configuration</Button>
                           </div>
                        )}
                     </motion.div>
                  </AnimatePresence>
               </div>
            </Card>

            <Card className="p-10 bg-aura/5 border-aura/20 flex flex-col items-center text-center gap-6">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign">
                  <Database size={32} />
               </div>
               <div className="space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight">Collective Knowledge Graph</h3>
                  <p className="text-sm text-slate-400 font-bold max-w-xl">
                     All autonomous offspring synchronize discoveries to the universal mesh via DTN. Even with latency, constitutional integrity is maintained.
                  </p>
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-slate-950 border-slate-900">
               <h4 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                  <Activity size={20} className="text-aura" />
                  Seed Vitals
               </h4>
               <div className="space-y-6">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Autonomous Units</span>
                     <span className="text-white">5</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Mesh Alignment</span>
                     <span className="text-emerald-500">99.4%</span>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Seeding requires MultiSigCouncil approval for resource allocation on celestial bodies.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
