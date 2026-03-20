import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Save, Play, Rocket, Layers, Wand2, ShieldCheck, Terminal, Cpu, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const Forge: React.FC = () => {
  const [models, setModels] = useState<any[]>([]);
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [isRecombining, setIsRecombining] = useState(false);
  const [output, setOutput] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v154/library/models').then(res => setModels(Object.keys(res.data)));
  }, []);

  const handleRecombine = async () => {
    if (selectedModels.length < 2) {
       alert("Select at least 2 models for TIES-Merge.");
       return;
    }
    setIsRecombining(true);
    try {
       const res = await axios.post('/api/v154/forge/recombine', { model_ids: selectedModels, strategy: 'TIES' });
       setOutput(res.data);
    } catch (err) {
       console.error("Forge Recombination Failed.");
    } finally {
       setIsRecombining(false);
    }
  };

  return (
    <div className="space-y-10 animate-in fade-in duration-700">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1 neon-text !text-aura">The Forge</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Developer Realm • Layer 7 Universe</p>
        </div>
        <div className="flex gap-4">
           <div className="px-6 py-3 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-3">
              <Terminal size={18} className="text-aura" />
              <span className="text-xs font-black text-aura uppercase tracking-widest">Sovereign Shell Active</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 h-[600px]">
        <aside className="p-8 glass-card border-white/5 bg-sovereign/40 flex flex-col gap-8 overflow-y-auto custom-scrollbar">
           <div>
              <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] mb-4">Genetic Library</h3>
              <div className="space-y-2">
                 {models.map(m => (
                   <button
                     key={m}
                     onClick={() => setSelectedModels(prev => prev.includes(m) ? prev.filter(x => x !== m) : [...prev, m])}
                     className={`w-full p-4 rounded-2xl border transition-all flex items-center gap-4 group text-left ${
                       selectedModels.includes(m) ? 'bg-aura/10 border-aura text-aura' : 'bg-slate-900/40 border-white/5 text-slate-400'
                     }`}
                   >
                     <div className={`p-2 rounded-lg ${selectedModels.includes(m) ? 'bg-aura text-sovereign' : 'bg-surface text-slate-500'}`}>
                        <Layers size={18} />
                     </div>
                     <span className="text-xs font-bold">{m}</span>
                   </button>
                 ))}
              </div>
           </div>

           <div className="mt-auto pt-6 border-t border-white/5">
              <button
                onClick={handleRecombine}
                disabled={isRecombining}
                className="w-full py-4 bg-aura text-sovereign font-black rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] transition-all shadow-lg shadow-aura/10 uppercase tracking-widest text-xs disabled:opacity-50"
              >
                {isRecombining ? <Plus size={18} className="animate-spin" /> : <Wand2 size={18} />}
                Initiate Recombination
              </button>
           </div>
        </aside>

        <main className="lg:col-span-2 glass-card bg-aura/5 border-aura/20 relative overflow-hidden flex flex-col">
           <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
           <div className="relative p-10 flex-1 overflow-y-auto custom-scrollbar">
              {!output ? (
                <div className="h-full flex flex-col items-center justify-center gap-6 text-center">
                   <div className="w-20 h-20 rounded-full bg-aura/10 flex items-center justify-center text-aura animate-pulse">
                      <Cpu size={40} />
                   </div>
                   <div className="space-y-2">
                      <h3 className="text-2xl font-black">Visual Agent Composer</h3>
                      <p className="text-slate-500 font-bold max-w-xs">Select models from the library to begin the TIES-Merge synthesis.</p>
                   </div>
                </div>
              ) : (
                <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="space-y-10">
                   <div className="flex justify-between items-start">
                      <div>
                        <h2 className="text-3xl font-black mb-2">Synthesis Success</h2>
                        <div className="flex items-center gap-2">
                           <ShieldCheck size={16} className="text-aura" />
                           <span className="text-xs font-black uppercase text-aura tracking-widest">Article 1095 Certified</span>
                        </div>
                      </div>
                   </div>

                   <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="p-8 bg-sovereign rounded-3xl border border-white/5 space-y-4">
                         <p className="text-[10px] font-black text-slate-500 uppercase">Agent DID</p>
                         <p className="font-mono text-xs text-white break-all">{output.agent_did}</p>
                      </div>
                      <div className="p-8 bg-sovereign rounded-3xl border border-white/5 space-y-4">
                         <p className="text-[10px] font-black text-slate-500 uppercase">Fidelity Score</p>
                         <p className="text-4xl font-black text-aura">{output.metadata.fidelity_score * 100}%</p>
                      </div>
                   </div>

                   <div className="p-8 bg-surface rounded-[2rem] border border-white/5">
                      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                         <Terminal size={18} className="text-aura" />
                         Provenance Ledger
                      </h3>
                      <div className="space-y-2 font-mono text-[10px] text-slate-500">
                         <p>MODE: {output.metadata.merge_strategy}</p>
                         <p>ROOT: {output.metadata.hash}</p>
                         <p>TIMESTAMP: {new Date().toISOString()}</p>
                      </div>
                   </div>

                   <button className="w-full py-5 bg-aura text-sovereign font-black rounded-2xl hover:scale-[1.02] transition-all shadow-xl shadow-aura/20 uppercase tracking-widest text-sm">
                      Deploy Agent to User Realm
                   </button>
                </motion.div>
              )}
           </div>
        </main>
      </div>
    </div>
  );
};
