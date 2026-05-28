import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Globe, Map, Activity, ShieldCheck, History, Info, ChevronRight, Zap, Globe2, AlertCircle, Plus, Send, Network, Server, Satellite, Rocket, Moon, Sun, Radio } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const CosmicMeshDashboard: React.FC = () => {
  const { systemVitals } = useStore();
  const [activeView, setActiveView] = useState('solar');

  const cosmicNodes = [
    { id: 'lun-1', name: 'Lunar-South-Pole', region: 'Moon', latency: '1.2s', status: 'Healthy', type: 'Relay' },
    { id: 'mar-1', name: 'Mars-Olympus-Hub', region: 'Mars', latency: '4m 20s', status: 'Normal', type: 'Gateway' },
    { id: 'ast-42', name: 'Ceres-Mining-Alpha', region: 'Asteroid Belt', latency: '24m', status: 'Syncing', type: 'Seed' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Cosmic Command</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Interstellar Mesh Visualisation • Phase 4 Cosmic Embodiment</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><Rocket size={18} /> Missions</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Spawn Off-World Node
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="h-[600px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.02)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Interstellar Mesh Map
                     <Badge color="aura">DTN-Active</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Delay-Tolerant Network • LEO-to-Lunar Laser Links</p>
               </div>

               {/* Solar System Simulation Stub */}
               <div className="relative w-full h-full flex items-center justify-center">
                  <div className="w-10 h-10 rounded-full bg-yellow-500 shadow-[0_0_50px_rgba(234,179,8,0.5)] animate-pulse" />

                  {/* Planetary Orbits */}
                  <div className="absolute w-40 h-40 rounded-full border border-white/5" />
                  <div className="absolute w-80 h-80 rounded-full border border-white/5" />
                  <div className="absolute w-[500px] h-[500px] rounded-full border border-white/5" />

                  {/* Nodes */}
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 40, ease: "linear" }} className="absolute w-80 h-80">
                     <div className="w-4 h-4 rounded-full bg-blue-500 shadow-lg absolute -top-2 left-1/2 -translate-x-1/2">
                        <div className="absolute -inset-2 border border-aura/20 rounded-full animate-ping" />
                     </div>
                  </motion.div>

                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 80, ease: "linear" }} className="absolute w-[500px] h-[500px]">
                     <div className="w-4 h-4 rounded-full bg-red-500 shadow-lg absolute -top-2 left-1/2 -translate-x-1/2">
                        <div className="absolute -inset-2 border border-vital/20 rounded-full animate-ping" />
                     </div>
                  </motion.div>
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10 text-right">
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Cislunar Nodes</p>
                     <p className="text-2xl font-black text-aura">12</p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Deep Space</p>
                     <p className="text-2xl font-black text-highlight">4</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <Satellite size={24} className="text-aura" />
                  Off-World Node Registry
               </h3>
               <div className="space-y-4">
                  {cosmicNodes.map((node, i) => (
                    <motion.div
                      key={node.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all`}>
                             {node.region === 'Moon' ? <Moon size={24} /> : node.region === 'Mars' ? <Rocket size={24} /> : <Zap size={24} />}
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{node.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{node.region}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-aura">{node.latency} RTT</span>
                             </div>
                          </div>
                       </div>
                       <Badge color={node.status === 'Healthy' ? 'emerald-500' : 'aura'}>{node.status}</Badge>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-4 text-aura">
                  <Radio size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">DTN Protocol</h4>
               </div>
               <div className="space-y-8">
                  <div className="space-y-3">
                     <div className="flex justify-between items-end">
                        <span className="text-[10px] font-black uppercase text-slate-500">Buffer Utilization</span>
                        <span className="text-xl font-black text-white">42%</span>
                     </div>
                     <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-aura w-[42%]" />
                     </div>
                  </div>
                  <div className="p-6 rounded-2xl bg-slate-950 border border-slate-900 space-y-3">
                     <div className="flex justify-between items-center text-[9px] font-black uppercase">
                        <span className="text-slate-500">Comm Window</span>
                        <span className="text-emerald-500">OPEN</span>
                     </div>
                     <p className="text-xs font-bold text-white">Next Mars alignment in 4h 12m.</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Cislunar Vitals</h4>
               <div className="space-y-4">
                  {[
                    { label: 'Earth-Moon Laser', value: '1.2 Gbps', color: 'emerald-500' },
                    { label: 'Relay Uptime', value: '99.99%', color: 'aura' },
                  ].map(stat => (
                    <div key={stat.label} className="flex justify-between items-center">
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{stat.label}</span>
                       <span className={`text-xs font-black text-${stat.color}`}>{stat.value}</span>
                    </div>
                  ))}
               </div>
            </Card>

            <Card className="p-8 border-slate-800 flex items-center gap-6">
               <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura shadow-xl shadow-aura/10 animate-pulse">
                  <Satellite size={28} />
               </div>
               <div>
                  <h4 className="text-lg font-black text-white mb-1 uppercase tracking-tight">Orbital Sync</h4>
                  <p className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Block #14242 COSMIC</p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
