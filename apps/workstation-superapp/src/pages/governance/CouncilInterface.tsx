import React, { useState } from 'react';
import { Card, Button, Badge, notImplemented} from '@workstation/ui';
import { Gavel, ShieldCheck, Users, Activity, Globe, Scale, MessageSquare, AlertCircle, History, Terminal, Fingerprint, TrendingUp, ChevronRight, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, gaas } from '@workstation/shared';

export const CouncilInterface: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('members');

  const members = [
    { id: 'ceo-agent', role: 'AI CEO', status: 'Active', trust: 0.98, type: 'AI' },
    { id: 'cfo-agent', role: 'AI CFO', status: 'Active', trust: 0.95, type: 'AI' },
    { id: 'cto-agent', role: 'AI CTO', status: 'Active', trust: 0.97, type: 'AI' },
    { id: 'guardian-01', role: 'Human Advisor', status: 'Observer', trust: 1.0, type: 'Human' },
  ];

  const proposals = [
    { id: 'GOV-142', title: 'Self-Modification: LEO Latency Optimization', author: 'cto-agent', status: 'Voting', weight: 'Quadratic' },
    { id: 'GOV-143', title: 'Treaty: Open-Sovereign-Federation v3', author: 'ceo-agent', status: 'Ratified', weight: 'MultiSig' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase break-words">Inter-Republic Council</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">AI-Led Eternal Governance • Article 1120 • Self-Healing Rules</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Ballot History')} variant="outline"><History size={18} /> Ballot History</Button>
           <Button onClick={() => notImplemented('Access Ballot Box')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Scale size={18} /> Access Ballot Box
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
               <button onClick={() => setActiveTab('members')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'members' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Members</button>
               <button onClick={() => setActiveTab('proposals')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'proposals' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Proposals</button>
               <button onClick={() => setActiveTab('rules')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'rules' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Self-Healing</button>
            </div>

            <AnimatePresence mode="wait">
               {activeTab === 'members' && (
                 <motion.div key="members" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6">
                    <Card className="p-10">
                       <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4 mb-10">
                          <Users size={24} className="text-aura" />
                          Council Composition
                       </h3>
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {members.map(m => (
                            <div key={m.id} className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                               <div className="flex items-center gap-5">
                                  <div className={`w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all`}>
                                     {m.type === 'AI' ? <Terminal size={20} /> : <Fingerprint size={20} />}
                                  </div>
                                  <div>
                                     <p className="text-sm font-black text-white mb-1 uppercase tracking-widest">{m.id}</p>
                                     <div className="flex items-center gap-3">
                                        <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">{m.role}</span>
                                        <div className={`w-1.5 h-1.5 rounded-full ${m.status === 'Active' ? 'bg-emerald-500' : 'bg-slate-700'}`} />
                                     </div>
                                  </div>
                               </div>
                               <div className="text-right">
                                  <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Trust Score</p>
                                  <span className="text-xs font-black text-white">{m.trust * 100}%</span>
                               </div>
                            </div>
                          ))}
                       </div>
                    </Card>
                 </motion.div>
               )}

               {activeTab === 'proposals' && (
                 <motion.div key="proposals" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-4">
                    {proposals.map(p => (
                      <div key={p.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                         <div className="flex items-center gap-8">
                            <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                               <MessageSquare size={24} />
                            </div>
                            <div>
                               <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{p.title}</p>
                               <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                                  <span>ID: {p.id}</span>
                                  <div className="w-1 h-1 rounded-full bg-slate-800" />
                                  <span>Weight: {p.weight}</span>
                               </div>
                            </div>
                         </div>
                         <Badge color={p.status === 'Ratified' ? 'emerald-500' : 'aura'}>{p.status}</Badge>
                      </div>
                    ))}
                 </motion.div>
               )}

               {activeTab === 'rules' && (
                 <motion.div key="rules" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6">
                    <Card className="p-10 bg-aura/5 border-aura/20">
                       <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4 mb-4">
                          <Activity size={24} className="text-aura" />
                          Self-Healing Rule Feed
                       </h3>
                       <p className="text-sm text-slate-400 font-bold leading-relaxed mb-10 max-w-2xl">
                          The governance engine autonomously evolves rule weights and quorum parameters based on real-time mesh vitals (latency, consensus speed, and Article 1118 thresholds).
                       </p>
                       <div className="space-y-4">
                          {[
                            { rule: 'Quorum-Alpha-Adjustment', trigger: 'latency > 20ms', effect: 'Increase weight of orbital nodes', status: 'ACTIVE' },
                            { rule: 'Vote-Quadratic-Calibration', trigger: 'rep_score_variance > 0.4', effect: 'Cap max individual weighting', status: 'SYNCING' },
                          ].map(rule => (
                            <div key={rule.rule} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex flex-col gap-4">
                               <div className="flex justify-between items-center">
                                  <span className="text-xs font-black text-white uppercase tracking-widest">{rule.rule}</span>
                                  <Badge color="aura">{rule.status}</Badge>
                               </div>
                               <div className="grid grid-cols-2 gap-4 text-[10px] font-black uppercase">
                                  <div className="space-y-1">
                                     <p className="text-slate-700">Trigger</p>
                                     <p className="text-white">{rule.trigger}</p>
                                  </div>
                                  <div className="space-y-1">
                                     <p className="text-slate-700">Effect</p>
                                     <p className="text-aura">{rule.effect}</p>
                                  </div>
                               </div>
                            </div>
                          ))}
                       </div>
                    </Card>
                 </motion.div>
               )}
            </AnimatePresence>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Gavel size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">AI-Led Consensus</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     The Council is 100% AI-led in v3.0, with human advisors providing mandatory oversight for Articles 1101-1127.
                  </p>
               </div>
               <Button onClick={() => notImplemented('Access Governance Log')} className="w-full bg-aura text-sovereign py-5 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-aura/20">Access Governance Log</Button>
            </Card>

            <Card className="p-10 space-y-6">
               <div className="flex justify-between items-center">
                  <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Council Pulse</h4>
                  <TrendingUp size={16} className="text-aura" />
               </div>
               <div className="space-y-4">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase">
                     <span className="text-slate-500">Ratification Rate</span>
                     <span className="text-white">92.4%</span>
                  </div>
                  <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-[92%]" />
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase">
                     <span className="text-slate-500">Veto Frequency</span>
                     <span className="text-vital">0.02 / Day</span>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Article 1120 mandates quadratic voting for all resource allocation decisions.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
