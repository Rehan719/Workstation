import React, { useState, useEffect } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Activity, Zap, Shield, ShieldAlert, RefreshCw, Cpu, Globe, HeartPulse, Terminal, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const HomeostaticOrchestrator: React.FC = () => {
  const [vitals, setVitals] = useState({
    efficiency: 92.4,
    latency: 18,
    swarmHealth: 99.8,
    activeNodes: 1024,
    energySaving: '20%'
  });
  const [events, setEvents] = useState<any[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setVitals(prev => ({
        ...prev,
        efficiency: Math.min(100, Math.max(80, prev.efficiency + (Math.random() - 0.5))),
        latency: Math.max(5, prev.latency + (Math.random() - 0.5) * 2)
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const triggerFailure = () => {
    setIsSimulating(true);
    const newEvent = {
      id: Date.now(),
      type: 'FAILURE',
      target: 'L11-ORBITAL-NODE-04',
      message: 'Simulated failure: Sub-system unresponsive.',
      timestamp: new Date().toLocaleTimeString()
    };
    setEvents(prev => [newEvent, ...prev]);
    setVitals(prev => ({ ...prev, swarmHealth: 85.2, efficiency: 72.1 }));

    setTimeout(() => {
       const healEvent = {
         id: Date.now() + 1,
         type: 'HEAL',
         target: 'L11-ORBITAL-NODE-04',
         message: 'Resilience Manager: Node redirected and rebooted. Stability restored.',
         timestamp: new Date().toLocaleTimeString()
       };
       setEvents(prev => [healEvent, ...prev]);
       setVitals(prev => ({ ...prev, swarmHealth: 99.8, efficiency: 92.4 }));
       setIsSimulating(false);
    }, 4000);
  };

  return (
    <div className="space-y-10 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black text-white uppercase tracking-tighter italic break-words">Homeostatic Orchestrator</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.4em] mt-2">v138.0 Galactic Era • Autonomous Self-Healing Mesh</p>
        </div>
        <Button
          variant="outline"
          onClick={triggerFailure}
          disabled={isSimulating}
          className="bg-vital/10 border-vital/30 text-vital hover:bg-vital hover:text-sovereign"
        >
          <ShieldAlert size={18} /> Trigger Failure Simulation
        </Button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
         <Card className="p-8 space-y-4">
            <div className="flex justify-between items-start">
               <Activity size={24} className="text-aura" />
               <Badge color="aura">LIVE</Badge>
            </div>
            <div>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Efficiency</p>
               <p className="text-3xl font-black text-white">{vitals.efficiency.toFixed(1)}%</p>
            </div>
            <div className="h-1 w-full bg-slate-900 rounded-full overflow-hidden">
               <motion.div animate={{ width: `${vitals.efficiency}%` }} className="h-full bg-aura" />
            </div>
         </Card>
         <Card className="p-8 space-y-4">
            <div className="flex justify-between items-start">
               <Zap size={24} className="text-highlight" />
               <Badge color="highlight">OPTIMAL</Badge>
            </div>
            <div>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Avg Latency</p>
               <p className="text-3xl font-black text-white">{vitals.latency.toFixed(0)}ms</p>
            </div>
            <div className="h-1 w-full bg-slate-900 rounded-full overflow-hidden">
               <motion.div animate={{ width: `${(100 - vitals.latency) / 100 * 100}%` }} className="h-full bg-highlight" />
            </div>
         </Card>
         <Card className="p-8 space-y-4">
            <div className="flex justify-between items-start">
               <HeartPulse size={24} className="text-emerald-500" />
               <Badge color="emerald-500">HEALTHY</Badge>
            </div>
            <div>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Swarm Integrity</p>
               <p className="text-3xl font-black text-white">{vitals.swarmHealth}%</p>
            </div>
            <div className="h-1 w-full bg-slate-900 rounded-full overflow-hidden">
               <motion.div animate={{ width: `${vitals.swarmHealth}%` }} className="h-full bg-emerald-500" />
            </div>
         </Card>
         <Card className="p-8 space-y-4">
            <div className="flex justify-between items-start">
               <Shield size={24} className="text-vital" />
               <Badge color="vital">PQC ACTIVE</Badge>
            </div>
            <div>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">CL1 Energy Saving</p>
               <p className="text-3xl font-black text-white">{vitals.energySaving}</p>
            </div>
            <div className="flex gap-1">
               {[1, 2, 3, 4, 5].map(i => <div key={i} className="flex-1 h-1 bg-vital rounded-full" />)}
            </div>
         </Card>
      </div>

      <div className="grid grid-cols-12 gap-8">
         <div className="col-span-12 @[440px]:col-span-8">
            <Card className="p-10">
               <h3 className="text-2xl font-black text-white uppercase tracking-tight mb-8 flex items-center gap-4">
                  <Terminal size={24} className="text-slate-500" />
                  Orchestration Event Stream
               </h3>
               <div className="space-y-4 h-[400px] overflow-y-auto pr-4 custom-scrollbar">
                  <AnimatePresence initial={false}>
                     {events.length === 0 && (
                       <div className="h-full flex flex-col items-center justify-center text-slate-600">
                          <Globe size={48} className="mb-4 opacity-20" />
                          <p className="text-xs font-black uppercase tracking-[0.2em]">Awaiting Mesh Signals...</p>
                       </div>
                     )}
                     {events.map((e) => (
                       <motion.div
                         key={e.id}
                         initial={{ opacity: 0, x: -20 }}
                         animate={{ opacity: 1, x: 0 }}
                         className={`p-6 rounded-2xl border ${e.type === 'FAILURE' ? 'bg-vital/5 border-vital/20' : 'bg-aura/5 border-aura/20'} flex gap-6 items-start`}
                       >
                          <div className={`p-3 rounded-xl ${e.type === 'FAILURE' ? 'bg-vital/20 text-vital' : 'bg-aura/20 text-aura'}`}>
                             {e.type === 'FAILURE' ? <AlertTriangle size={20} /> : <RefreshCw size={20} className={e.type === 'HEAL' ? 'animate-spin' : ''} />}
                          </div>
                          <div className="flex-1">
                             <div className="flex justify-between mb-1">
                                <span className={`text-[10px] font-black uppercase tracking-widest ${e.type === 'FAILURE' ? 'text-vital' : 'text-aura'}`}>{e.type} EVENT</span>
                                <span className="text-[10px] font-mono text-slate-600">{e.timestamp}</span>
                             </div>
                             <p className="text-sm font-bold text-white mb-1">{e.target}</p>
                             <p className="text-xs text-slate-400 font-medium leading-relaxed">{e.message}</p>
                          </div>
                       </motion.div>
                     ))}
                  </AnimatePresence>
               </div>
            </Card>
         </div>

         <div className="col-span-12 @[440px]:col-span-4 space-y-8">
            <Card className="p-8 bg-aura/5 border-aura/20">
               <h4 className="text-xs font-black text-aura uppercase tracking-widest mb-6">Multi-Modal Fabric</h4>
               <div className="space-y-6">
                  <div className="flex items-center gap-4">
                     <div className="w-12 h-12 rounded-full bg-slate-900 border border-aura/30 flex items-center justify-center">
                        <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 2 }} className="w-3 h-3 bg-aura rounded-full" />
                     </div>
                     <div>
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Sentiment Stream</p>
                        <p className="text-xs font-black text-white">ANALYTICAL / CALM</p>
                     </div>
                  </div>
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-900">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Ethical Justification</p>
                     <p className="text-[10px] font-medium text-slate-300 leading-relaxed italic">
                        "Mesh actions prioritized for systemic stability over localized throughput, aligning with Article 1112."
                     </p>
                  </div>
               </div>
            </Card>

            <Card className="p-8">
               <h4 className="text-xs font-black text-white uppercase tracking-widest mb-6">Historical Resilience</h4>
               <div className="h-48 flex items-end gap-2">
                  {[40, 70, 45, 90, 65, 85, 30, 95, 80, 100].map((h, i) => (
                    <div key={i} className="flex-1 bg-slate-900 rounded-t-lg overflow-hidden relative group">
                       <motion.div initial={{ height: 0 }} animate={{ height: `${h}%` }} className={`absolute bottom-0 w-full transition-all group-hover:bg-aura ${h > 80 ? 'bg-aura/40' : h > 50 ? 'bg-highlight/40' : 'bg-vital/40'}`} />
                    </div>
                  ))}
               </div>
               <div className="flex justify-between mt-4">
                  <span className="text-[8px] font-black text-slate-700 uppercase">T-10 Epochs</span>
                  <span className="text-[8px] font-black text-slate-700 uppercase">Current</span>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
