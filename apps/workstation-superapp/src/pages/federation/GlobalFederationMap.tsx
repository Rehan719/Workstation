import React, { useState, useEffect } from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Globe, Map, Activity, ShieldCheck, History, Info, ChevronRight, Zap, Globe2, AlertCircle, Plus, Send, Network, Server, Satellite } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const GlobalFederationMap: React.FC = () => {
  const { systemVitals } = useStore();
  const [activeLayer, setActiveLayer] = useState('mesh');

  const nodes = [
    { id: 'n-1', name: 'North-America-Primary', type: 'Terrestrial', latency: '12ms', status: 'Healthy' },
    { id: 'n-2', name: 'Europe-Hub', type: 'Terrestrial', latency: '28ms', status: 'Healthy' },
    { id: 'n-3', name: 'Orbital-Alpha-LEO', type: 'Orbital', latency: '42ms', status: 'Normal' },
    { id: 'n-4', name: 'Undersea-Atlantic', type: 'Undersea', latency: '18ms', status: 'Healthy' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Global Federation</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Planetary Mesh Visualisation • Layer 11 Civilisation</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Mesh Log')} variant="outline"><History size={18} /> Mesh Log</Button>
           <Button onClick={() => notImplemented('Register Node')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Register Node
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <div className="@[440px]:col-span-8 space-y-10">
            <Card className="h-[600px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Planetary Resonance Map
                     <Badge color="aura">libp2p DHT</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Real-time Node Discovery & Latency Heatmap</p>
               </div>

               {/* 3D Globe Visualisation Stub */}
               <div className="relative w-full h-full flex items-center justify-center">
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 60, ease: "linear" }}>
                     <Globe2 size={400} className="text-aura opacity-20" />
                  </motion.div>

                  {/* Floating Node Markers */}
                  {[...Array(12)].map((_, i) => (
                    <motion.div
                      key={i}
                      animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.3, 0.7, 0.3]
                      }}
                      transition={{ duration: 2 + Math.random() * 2, repeat: Infinity, delay: i * 0.5 }}
                      className="absolute w-4 h-4 rounded-full bg-aura shadow-2xl shadow-aura/50"
                      style={{
                        left: `${20 + Math.random() * 60}%`,
                        top: `${20 + Math.random() * 60}%`,
                      }}
                    />
                  ))}
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10 text-right">
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Total Peers</p>
                     <p className="text-2xl font-black text-aura">{systemVitals.node_count || 100}+</p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Global P99</p>
                     <p className="text-2xl font-black text-aura">18.4ms</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Server size={24} className="text-aura" />
                     Sovereign Node Registry
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveLayer('mesh')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeLayer === 'mesh' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Terrestrial</button>
                     <button onClick={() => setActiveLayer('orbital')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeLayer === 'orbital' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Orbital</button>
                  </div>
               </div>

               <div className="space-y-4">
                  {nodes.map((node, i) => (
                    <motion.div
                      key={node.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all`}>
                             {node.type === 'Orbital' ? <Satellite size={24} /> : <Server size={24} />}
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{node.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{node.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-aura">{node.latency} Latency</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-6">
                          <Badge color={node.status === 'Healthy' ? 'emerald-500' : 'highlight'}>{node.status}</Badge>
                          <Button onClick={() => notImplemented('View Vitals')} variant="outline" className="px-6 py-3">View Vitals</Button>
                       </div>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </div>

         <div className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Activity size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Mesh Capacity</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Total federation compute resources currently at 84% utilization. Scaling LEO routing...
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Throughput</span>
                     <span className="text-white">12.4 PFLOPS</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-[84%]" />
                  </div>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Network Protocols</h4>
               <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">QUIC_TRANSPORT</span>
                     <Badge color="emerald-500">ACTIVE</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">GOSSIPSUB_V1</span>
                     <Badge color="aura">ROUTING</Badge>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                     <ShieldCheck size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">PQC Enforced</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Article 1107 Compliant</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
