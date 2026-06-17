import React, { useState } from 'react';
import { Card, Button, Badge, notImplemented } from '@workstation/ui';
import { Workflow, Play, History, Activity, Terminal, ArrowRight, CheckCircle2, AlertCircle, Info, Settings, LayoutGrid, Users, Zap, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, gaas } from '@workstation/shared';

export const Pipelines: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('pipelines');
  const [activePipeline, setActivePipeline] = useState(0);

  const [swarms, setSwarms] = useState([
    { id: 's-42', name: 'Alpha-Knowledge-Swarm', status: 'Active', agents: 5, tasks: 12, health: 'Healthy' },
    { id: 's-107', name: 'Market-Analysis-Swarm', status: 'Thinking', agents: 3, tasks: 4, health: 'Normal' },
  ]);

  const removeSwarm = (id: string) => setSwarms(prev => prev.filter(s => s.id !== id));

  const pipelines = [
    { id: 'p-1', name: 'Knowledge-Synthesis-Main', type: 'QEP Reactor', steps: 4, status: 'Running', health: 'Healthy' },
    { id: 'p-2', name: 'Agent-Evolution-L10', type: 'Evolution Engine', steps: 8, status: 'Paused', health: 'Normal' },
    { id: 'p-3', name: 'Mesh-Heartbeat-L11', type: 'Civilization Mesh', steps: 3, status: 'Idle', health: 'Healthy' },
  ];

  const steps = [
    { name: 'Discovery', status: 'Completed', time: '12ms' },
    { name: 'Ingestion', status: 'Completed', time: '42ms' },
    { name: 'Synthesis', status: 'Running', time: 'Currently Active' },
    { name: 'Deployment', status: 'Pending', time: '---' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Orchestration</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Workflow Pipelines & Swarm Management • Layer 9 Orchestrator</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('History')} variant="outline"><History size={18} /> History</Button>
           <Button onClick={() => notImplemented('New Workflow')} className="bg-aura text-sovereign shadow-xl shadow-aura/20"><Play size={18} /> New Workflow</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <div className="@[440px]:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('pipelines')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'pipelines' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Pipelines</button>
                     <button onClick={() => setActiveTab('swarms')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'swarms' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Active Swarms</button>
                  </div>
                  <div className="flex gap-4">
                     <Badge color="aura">L9 Orchestrator Active</Badge>
                     <Badge color="emerald-500">UEG Tracking Strict</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     {activeTab === 'pipelines' ? (
                        <motion.div key="pipelines" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                           {pipelines.map((p, i) => (
                              <div key={p.id} onClick={() => setActivePipeline(i)} className={`p-8 rounded-[2.5rem] border-2 transition-all cursor-pointer flex items-center justify-between group ${activePipeline === i ? 'bg-aura/10 border-aura shadow-2xl shadow-aura/10' : 'bg-slate-950/80 border-slate-900 hover:border-slate-800'}`}>
                                 <div className="flex items-center gap-8">
                                    <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-sovereign transition-all ${activePipeline === i ? 'bg-aura' : 'bg-slate-900 text-aura border border-slate-800'}`}>
                                       <Workflow size={24} />
                                    </div>
                                    <div>
                                       <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{p.name}</p>
                                       <div className="flex items-center gap-4">
                                          <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{p.type}</span>
                                          <Badge color="aura">{p.steps} Steps</Badge>
                                       </div>
                                    </div>
                                 </div>
                                 <ArrowRight size={24} className={activePipeline === i ? 'text-aura' : 'text-slate-800'} />
                              </div>
                           ))}
                        </motion.div>
                     ) : (
                        <motion.div key="swarms" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                           {swarms.map((s, i) => (
                              <div key={s.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                                 <div className="flex items-center gap-8">
                                    <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                                       <Users size={24} />
                                    </div>
                                    <div>
                                       <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{s.name}</p>
                                       <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                          <span>{s.agents} Agents</span>
                                          <div className="w-1 h-1 rounded-full bg-slate-800" />
                                          <span>{s.tasks} Tasks Pending</span>
                                       </div>
                                    </div>
                                 </div>
                                 <div className="flex items-center gap-6">
                                    <Badge color={s.status === 'Active' ? 'emerald-500' : 'aura'}>{s.status}</Badge>
                                    <button type="button" onClick={() => removeSwarm(s.id)} aria-label={`Remove ${s.name}`} title={`Remove ${s.name}`} className="p-3 bg-slate-900 border border-slate-800 rounded-xl text-vital hover:bg-vital/10 transition-all"><Trash2 size={20} /></button>
                                 </div>
                              </div>
                           ))}
                        </motion.div>
                     )}
                  </AnimatePresence>
               </div>
            </Card>

            {activeTab === 'pipelines' && (
              <Card className="p-10 space-y-10 relative overflow-hidden">
                 <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
                 <div className="flex justify-between items-center relative z-10">
                    <h3 className="text-2xl font-black text-white uppercase tracking-widest">Active Execution View</h3>
                    <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest">PID: 14242 • Article 1112 Compliant</div>
                 </div>

                 <div className="relative z-10 flex justify-between px-10">
                    {steps.map((step, i) => (
                      <React.Fragment key={step.name}>
                        <div className="flex flex-col items-center gap-4 group">
                           <div className={`w-16 h-16 rounded-3xl border-2 flex items-center justify-center transition-all ${step.status === 'Completed' ? 'bg-aura text-sovereign border-aura' : step.status === 'Running' ? 'bg-aura/10 border-aura shadow-2xl shadow-aura/10 animate-pulse' : 'bg-slate-900 border-slate-800'}`}>
                              {step.status === 'Completed' ? <CheckCircle2 size={24} /> : step.status === 'Running' ? <Activity size={24} className="text-aura" /> : <LayoutGrid size={24} className="text-slate-700" />}
                           </div>
                           <div className="text-center">
                              <p className={`text-[10px] font-black uppercase tracking-widest mb-1 ${step.status === 'Completed' ? 'text-aura' : 'text-slate-500'}`}>{step.name}</p>
                              <p className="text-[8px] font-bold text-slate-600 uppercase tracking-widest">{step.time}</p>
                           </div>
                        </div>
                        {i < steps.length - 1 && (
                          <div className="flex-1 h-0.5 bg-slate-900 mt-8 mx-4 relative">
                             <motion.div
                                animate={{ x: [0, 40], opacity: [0, 1, 0] }}
                                transition={{ repeat: Infinity, duration: 1.5 }}
                                className="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-aura/20 rounded-full blur-md"
                             />
                          </div>
                        )}
                      </React.Fragment>
                    ))}
                 </div>
              </Card>
            )}
         </div>

         <div className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Terminal size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Swarm Command</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Manually scale swarm capacity or reconfigure task decomposition logic for the L9 Orchestrator.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Throughput</span>
                     <span className="text-white">1.2M req/s</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Latency</span>
                     <span className="text-emerald-500">18ms</span>
                  </div>
               </div>
               <Button onClick={() => notImplemented('Scale Swarm')} className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs">Scale Swarm</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                     <Settings size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Auto-Healing</h4>
                     <p className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Article 1120 Active</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
