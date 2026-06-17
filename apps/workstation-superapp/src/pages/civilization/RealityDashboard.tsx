import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { GitBranch, TrendingUp, Zap, Activity, ChevronRight, Play, Star, Map, Users } from 'lucide-react';
import { motion } from 'framer-motion';
import { notImplemented } from '@workstation/ui';

export const RealityDashboard: React.FC = () => {
  const [timelines, setTimelines] = useState<any[]>([]);

  useEffect(() => {
    // Simulated branching futures
    setTimelines([
      { id: 'T-Main', title: "Current Trajectory", probability: 0.85, status: "Active", prosperity: "+12%" },
      { id: 'T-Alpha', title: "Empathy Peak (Sanctum-Meta-01)", probability: 0.12, status: "Simulated", prosperity: "+28%" },
      { id: 'T-Omega', title: "Resource Scarcity Crisis", probability: 0.03, status: "Simulated", prosperity: "-42%" }
    ]);
  }, []);

  return (
    <div className="space-y-12">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black mb-1 break-words">Reality Dashboard</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Branching Civilizational Futures v153.0</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <div className="px-6 py-3 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-3 shadow-[0_0_20px_rgba(100,255,218,0.1)]">
              <GitBranch size={18} className="text-aura" />
              <span className="text-xs font-black text-aura uppercase tracking-widest">Reality Engine Online</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-12">
        <div className="@[440px]:col-span-2 space-y-8">
           <section className="p-10 glass-card bg-sovereign/40 border-white/5 min-h-[500px] flex flex-col items-center justify-center relative overflow-hidden group">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.05)_0%,transparent_70%)]"></div>
              {/* Timeline Visualization Placeholder */}
              <div className="relative w-full h-full flex items-center justify-center">
                 <div className="w-[1px] h-full bg-aura/20 absolute left-1/2"></div>
                 <div className="space-y-32 relative z-10">
                    {timelines.map((t, i) => (
                      <motion.div
                        key={t.id}
                        initial={{ opacity: 0, x: i % 2 === 0 ? -50 : 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.2 }}
                        className={`p-6 glass-card border-aura/30 w-64 cursor-pointer hover:border-aura transition-all ${t.status === 'Active' ? 'bg-aura/10' : 'bg-surface'}`}
                      >
                         <div className="flex justify-between items-start mb-4">
                            <span className="text-[10px] font-black uppercase text-aura border border-aura/20 px-2 py-0.5 rounded">{t.id}</span>
                            <span className={`text-[10px] font-black uppercase ${t.status === 'Active' ? 'text-aura' : 'text-slate-500'}`}>{t.status}</span>
                         </div>
                         <h4 className="font-bold text-sm mb-2">{t.title}</h4>
                         <div className="flex justify-between items-end">
                            <p className="text-[10px] font-black text-slate-500 uppercase">Prosperity</p>
                            <p className={`text-lg font-black ${t.prosperity.startsWith('+') ? 'text-aura' : 'text-vital'}`}>{t.prosperity}</p>
                         </div>
                      </motion.div>
                    ))}
                 </div>
              </div>
           </section>
        </div>

        <aside className="space-y-8">
           <section className="p-8 glass-card border-aura/20 bg-aura/5">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-3">
                 <Zap size={20} className="text-aura" />
                 Cosmic Treasury
              </h3>
              <div className="space-y-6">
                 <div>
                    <p className="text-[10px] font-black text-slate-500 uppercase">Unified Balance</p>
                    <p className="text-4xl font-black text-white">1,542,420 <span className="text-xs text-aura">WST</span></p>
                 </div>
                 <div className="p-4 bg-sovereign rounded-xl border border-white/5 space-y-2">
                    <p className="text-[10px] font-black text-slate-500 uppercase">Simulated Yield (T-Alpha)</p>
                    <p className="text-xl font-black text-aura">+142,000 WST</p>
                 </div>
                 <button onClick={() => notImplemented('Allocate Multi-Verse Grant')} className="w-full py-4 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest hover:scale-105 transition-all">Allocate Multi-Verse Grant</button>
              </div>
           </section>

           <section className="p-8 glass-card">
              <h3 className="text-xl font-bold mb-6">Reality Voting</h3>
              <p className="text-xs text-slate-500 font-bold leading-relaxed mb-6">
                 Citizens can vote to steer the civilization toward preferred simulated futures. Resource allocation shifts based on collective preference.
              </p>
              <div className="space-y-4">
                 <div className="flex justify-between items-center p-3 bg-surface rounded-xl border border-white/5">
                    <span className="text-xs font-bold">T-Alpha Influence</span>
                    <span className="text-sm font-black text-aura">14.2%</span>
                 </div>
              </div>
           </section>
        </aside>
      </div>
    </div>
  );
};
