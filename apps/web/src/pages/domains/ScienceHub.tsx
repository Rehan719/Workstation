import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Microscope, Activity, Cpu, Settings, Search, History, Info, ChevronRight, Zap, Globe, Binary, FlaskConical, Network, Globe2, AlertCircle, Plus, BookOpen, Database, TestTube2, RefreshCcw } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const ScienceHub: React.FC = () => {
  const { genomicMetadata, systemVitals } = useStore();
  const [activeTab, setActiveTab] = useState('research');

  const papers = [
    { id: 'p-142', title: 'Planetary Mesh Resonance Analysis v3.0', author: 'Scholar-Agent-42', date: '2026-03-20', citations: 124, reproducibility: 0.99 },
    { id: 'p-219', title: 'TIES-Merge Genetic Crossover Optimization', author: 'Recombination-CoE', date: '2026-03-21', citations: 42, reproducibility: 0.98 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">Nexus of Proof</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Empirical Discovery • Federated Knowledge Graph • Science Hub</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Lab Notes</Button>
           <Button className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Microscope size={18} /> Initiate Analysis
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-highlight/5 border-highlight/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,204,100,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Knowledge Synthesis Mesh
                     <Badge color="highlight">Empirical-Core</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">GraphRAG Analysis • Article 1121 Secure Citations</p>
               </div>

               <div className="relative z-10 flex items-center justify-center">
                  <Network size={220} className="text-highlight opacity-20 animate-pulse-slow" />
                  <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 4 }} className="absolute">
                     <RefreshCcw size={60} className="text-highlight opacity-40 animate-spin-slow" />
                  </motion.div>
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10">
                  <div className="text-right">
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Experiments Verified</p>
                     <p className="text-2xl font-black text-highlight">1,242</p>
                  </div>
                  <div className="text-right">
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Global P-Value</p>
                     <p className="text-2xl font-black text-highlight">0.001</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <TestTube2 size={24} className="text-highlight" />
                     Research & Reproducibility
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('research')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'research' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Research</button>
                     <button onClick={() => setActiveTab('sims')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'sims' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Simulations</button>
                  </div>
               </div>

               <div className="space-y-4">
                  {papers.map((p, i) => (
                    <motion.div
                      key={p.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight group-hover:bg-highlight group-hover:text-sovereign transition-all">
                             <BookOpen size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{p.title}</p>
                             <div className="flex items-center gap-4">
                                <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{p.author}</span>
                                <Badge color="highlight">{p.citations} Citations</Badge>
                                <Badge color="emerald-500">{p.reproducibility * 100}% Repro</Badge>
                             </div>
                          </div>
                       </div>
                       <Button variant="outline" className="px-6 py-3">View Trace</Button>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-highlight/5 border-highlight/20">
               <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign shadow-xl shadow-highlight/20">
                  <Database size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Digital Reactor Lab</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Run sandboxed simulations for agents, genomes, or experimental models with full reproducibility logs.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-highlight/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Queue Status</span>
                     <span className="text-white">Active</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Sim Duration</span>
                     <span className="text-highlight">&lt;200ms</span>
                  </div>
               </div>
               <Button className="w-full bg-highlight text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs">Launch Experiment</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Genomic Research View</h4>
               <div className="space-y-3 text-[10px] font-mono text-slate-500">
                  <div className="flex justify-between">
                     <span>Active Regulons</span>
                     <span className="text-highlight">142</span>
                  </div>
                  <div className="flex justify-between">
                     <span>T Fa Clusters</span>
                     <span className="text-highlight">12</span>
                  </div>
                  <div className="flex justify-between">
                     <span>Reproducibility Score</span>
                     <span className="text-emerald-500">0.994</span>
                  </div>
               </div>
               <Button variant="outline" className="w-full text-[9px] py-2">Open GRN Visualiser</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight">
                     <Binary size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Open Data</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Article 1121 Compliant</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
