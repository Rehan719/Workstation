import React, { useState } from 'react';
import { Card, Button, Badge, notImplemented } from '@workstation/ui';
import { Beaker, Trophy, Activity, Target, Zap, Rocket, Layers, ChevronRight, Info, Plus, TrendingUp, FlaskConical, History, Star, ThumbsUp, ThumbsDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useStore, gaas } from '@workstation/shared';

export const Incubator: React.FC = () => {
  const { user } = useStore();
  const navigate = useNavigate();
  const [activeTournament, setActiveTournament] = useState(0);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);

  const tournaments = [
    { id: 't-1', name: 'Alpha-Summarizer v3', agents: 12, top_fitness: 0.94, time_left: '2h 14m', stage: 'Round 3' },
    { id: 't-2', name: 'Reasoning-Optimizer', agents: 32, top_fitness: 0.88, time_left: '14h 52m', stage: 'Initial' },
    { id: 't-3', name: 'Ethics-Guard-Gen-4', agents: 8, top_fitness: 0.99, time_left: 'Completed', stage: 'Finalized' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter break-words">Evolution Engine</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Agent Evolution Arena • Layer 10 Fitness Selection</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Brackets')} variant="outline"><Target size={18} /> Brackets</Button>
           <Button onClick={() => notImplemented('Seed Tournament')} className="bg-aura text-sovereign"><Plus size={18} /> Seed Tournament</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4">
                     <Trophy size={24} className="text-aura" />
                     Live Tournaments
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="aura">Tournament Mode Active</Badge>
                     <Badge color="emerald-500">PQC Verified</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  {tournaments.map((t, i) => (
                    <motion.div
                      key={t.id}
                      onClick={() => setActiveTournament(i)}
                      className={`p-8 rounded-[2.5rem] border-2 transition-all cursor-pointer flex items-center justify-between group ${activeTournament === i ? 'bg-aura/10 border-aura shadow-2xl shadow-aura/10' : 'bg-slate-950/80 border-slate-900 hover:border-slate-800'}`}
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-sovereign transition-all ${activeTournament === i ? 'bg-aura' : 'bg-slate-900 text-aura border border-slate-800 group-hover:scale-110'}`}>
                             <Activity size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{t.name}</p>
                             <div className="flex items-center gap-4">
                                <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Stage: {t.stage}</span>
                                <span className="text-[10px] font-black text-aura uppercase tracking-widest bg-aura/10 px-2 py-0.5 rounded-lg">{t.agents} Active Agents</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-8">
                          <div className="text-right">
                             <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Max Fitness</p>
                             <p className="text-xl font-black text-white">{t.top_fitness * 100}%</p>
                          </div>
                          <ChevronRight size={24} className={activeTournament === i ? 'text-aura' : 'text-slate-800'} />
                       </div>
                    </motion.div>
                  ))}
               </div>
            </Card>

            <Card className="p-10 space-y-8">
               <h3 className="text-2xl font-black text-white uppercase tracking-widest">User Feedback Loop</h3>
               <div className="p-8 rounded-[2rem] bg-slate-950 border border-slate-900 flex items-center justify-between">
                  <div className="flex items-center gap-6">
                     <div className="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-aura">
                        <Star size={24} />
                     </div>
                     <div>
                        <p className="text-sm font-bold text-white">Rate Leader Performance</p>
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Affects Gen-15 Fitness Weights</p>
                     </div>
                  </div>
                  <div className="flex gap-4">
                     <button type="button" onClick={() => setFeedback('up')} aria-label="Rate leader positively" title="Rate leader positively" className={`p-4 rounded-2xl bg-slate-900 border transition-all ${feedback === 'up' ? 'border-emerald-500 text-emerald-500' : 'border-slate-800 text-slate-500 hover:text-emerald-500'}`}><ThumbsUp size={24} /></button>
                     <button type="button" onClick={() => setFeedback('down')} aria-label="Rate leader negatively" title="Rate leader negatively" className={`p-4 rounded-2xl bg-slate-900 border transition-all ${feedback === 'down' ? 'border-vital text-vital' : 'border-slate-800 text-slate-500 hover:text-vital'}`}><ThumbsDown size={24} /></button>
                  </div>
               </div>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10">
               <h4 className="text-xl font-black flex items-center gap-3">
                  <Activity size={20} className="text-aura" />
                  Fitness Vitals
               </h4>
               <div className="space-y-6">
                  <div className="flex justify-between items-end">
                     <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Mean Fitness</span>
                     <span className="text-xl font-black text-white">0.742</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-950 rounded-full overflow-hidden p-[2px] border border-slate-900">
                     <div className="h-full bg-aura w-[74%] rounded-full" />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                     <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                        <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Generations</p>
                        <p className="text-xl font-black text-white">1,424</p>
                     </div>
                     <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                        <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Diversity</p>
                        <p className="text-xl font-black text-aura">0.88</p>
                     </div>
                  </div>
               </div>
            </Card>

            <Card className="p-10 bg-aura/5 border-aura/20 space-y-8">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Rocket size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Promote Agent</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed mb-6">
                     Move high-fitness agents from the Incubator into production or the Living Marketplace.
                  </p>
               </div>
               <Button onClick={() => navigate('/factory')} className="w-full py-5 rounded-2xl text-[10px] font-black uppercase tracking-widest">Open Factory</Button>
            </Card>
         </div>
      </div>
    </div>
  );
};
