import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Globe, Map, Activity, ShieldCheck, History, Info, ChevronRight, Zap, Globe2, AlertCircle, Plus, Send, Network, Server, Satellite, Anchor, Wind } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const OrbitalDashboard: React.FC = () => {
  const { systemVitals } = useStore();
  const [activeTab, setActiveTab] = useState('mesh');

  const orbitalNodes = [
    { id: 'sat-1', name: 'LEO-Primary-Alpha', altitude: '550km', latency: '42ms', health: 'Healthy' },
    { id: 'sat-2', name: 'LEO-Bridge-Beta', altitude: '542km', latency: '48ms', health: 'Healthy' },
    { id: 'sat-3', name: 'Orbital-Relay-Gamma', altitude: '1200km', latency: '84ms', health: 'Normal' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase">Orbital Command</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Planetary Mesh Visualisation • LEO & Undersea Node Tracking</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><Satellite size={18} /> Telemetry</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Deploy Satellite Node
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="h-[600px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Planetary Resonance Map
                     <Badge color="aura">v3.0 Sovereign</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Real-time Orbital Telemetry & Undersea Handshakes</p>
               </div>

               {/* 3D Global Visualisation */}
               <div className="relative w-full h-full flex items-center justify-center">
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 60, ease: "linear" }}>
                     <Globe2 size={420} className="text-aura opacity-20" />
                  </motion.div>

                  {/* Orbital Rings */}
                  <motion.div animate={{ rotate: -360 }} transition={{ repeat: Infinity, duration: 40, ease: "linear" }} className="absolute w-[500px] h-[500px] rounded-full border border-aura/10 border-dashed" />
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 30, ease: "linear" }} className="absolute w-[600px] h-[600px] rounded-full border border-highlight/5 border-dashed" />

                  {/* Node markers */}
                  <motion.div animate={{ scale: [1, 1.2, 1], opacity: [0.4, 0.8, 0.4] }} transition={{ repeat: Infinity, duration: 2 }} className="absolute w-2 h-2 rounded-full bg-aura shadow-[0_0_15px_rgba(100,255,218,0.8)]" style={{ top: '30%', left: '45%' }} />
                  <motion.div animate={{ scale: [1, 1.2, 1], opacity: [0.4, 0.8, 0.4] }} transition={{ repeat: Infinity, duration: 2.5 }} className="absolute w-2 h-2 rounded-full bg-highlight shadow-[0_0_15px_rgba(255,204,100,0.8)]" style={{ top: '60%', left: '70%' }} />
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10 text-right">
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Orbital Active</p>
                     <p className="text-2xl font-black text-aura">14</p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Undersea Active</p>
                     <p className="text-2xl font-black text-highlight">42</p>
                  </div>
               </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
               <Card className="p-10 space-y-6">
                  <h3 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                     <Satellite size={24} className="text-aura" />
                     LEO Node Registry
                  </h3>
                  <div className="space-y-4">
                     {orbitalNodes.map(node => (
                       <div key={node.id} className="p-5 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                          <div>
                             <p className="text-sm font-black text-white mb-1 uppercase">{node.name}</p>
                             <p className="text-[9px] font-black text-slate-600 uppercase tracking-widest">{node.altitude} • {node.latency}</p>
                          </div>
                          <Badge color="emerald-500">{node.health}</Badge>
                       </div>
                     ))}
                  </div>
               </Card>

               <Card className="p-10 space-y-6">
                  <h3 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                     <Anchor size={24} className="text-highlight" />
                     Undersea Cables
                  </h3>
                  <div className="space-y-4">
                     {[
                       { id: 'c-1', name: 'Trans-Atlantic-V3', speed: '400 Tbps', health: 'Optimal' },
                       { id: 'c-2', name: 'Pacific-Relay-Sovereign', speed: '1.2 Pbps', health: 'Optimal' },
                     ].map(cable => (
                       <div key={cable.id} className="p-5 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all">
                          <div>
                             <p className="text-sm font-black text-white mb-1 uppercase">{cable.name}</p>
                             <p className="text-[9px] font-black text-slate-600 uppercase tracking-widest">{cable.speed}</p>
                          </div>
                          <Badge color="emerald-500">{cable.health}</Badge>
                       </div>
                     ))}
                  </div>
               </Card>
            </div>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-4 text-aura">
                  <Wind size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Mesh Dynamics</h4>
               </div>
               <div className="space-y-8">
                  <div className="space-y-3">
                     <div className="flex justify-between items-end">
                        <span className="text-[10px] font-black uppercase text-slate-500">Global Coverage</span>
                        <span className="text-xl font-black text-white">99.4%</span>
                     </div>
                     <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-aura w-[99%]" />
                     </div>
                  </div>
                  <div className="space-y-3">
                     <div className="flex justify-between items-end">
                        <span className="text-[10px] font-black uppercase text-slate-500">Inter-Node Sync</span>
                        <span className="text-xl font-black text-white">14ms</span>
                     </div>
                     <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-highlight w-[88%]" />
                     </div>
                  </div>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">P99 Latency Distribution</h4>
               <div className="h-40 flex items-end gap-1 px-4">
                  {[20, 35, 45, 30, 25, 60, 50, 40, 70, 55, 30, 20].map((h, i) => (
                    <motion.div
                      key={i}
                      initial={{ height: 0 }}
                      animate={{ height: `${h}%` }}
                      className="flex-1 bg-aura/40 rounded-t-sm"
                    />
                  ))}
               </div>
               <div className="flex justify-between items-center text-[9px] font-black uppercase text-slate-600">
                  <span>Americas</span>
                  <span>Europe</span>
                  <span>APAC</span>
               </div>
            </Card>

            <Card className="p-8 border-slate-800 flex items-center gap-6">
               <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura shadow-xl shadow-aura/10 animate-pulse">
                  <Satellite size={28} />
               </div>
               <div>
                  <h4 className="text-lg font-black text-white mb-1 uppercase">Orbital Sync</h4>
                  <p className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Locked: LEO-Block #142</p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
