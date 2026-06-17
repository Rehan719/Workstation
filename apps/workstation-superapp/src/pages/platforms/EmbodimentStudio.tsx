import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { User, Cpu, Zap, Activity, ShieldCheck, History, Info, ChevronRight, MousePointer2, Smartphone, Terminal, Radio, Brain, Eye } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, gaas } from '@workstation/shared';

export const EmbodimentStudio: React.FC = () => {
  const { currentRealm } = useStore();
  const [activeAvatar, setActiveAvatar] = useState(0);

  const platforms = [
    { id: 'plat-1', name: 'Synthetic-Humanoid-v4', type: 'Physical', status: 'Ready', battery: '92%' },
    { id: 'plat-2', name: 'Lunar-Rover-Relay', type: 'Robotic', status: 'Connected', battery: '84%' },
    { id: 'plat-3', name: 'Neural-Link-A1', type: 'BCI', status: 'Calibrating', battery: 'N/A' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Embodiment Studio</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Avatar-to-Physical Body Streaming • BCI Mapping • Phase 4</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Calibrate BCI')} variant="outline"><Brain size={18} /> Calibrate BCI</Button>
           <Button onClick={() => notImplemented('Inhabit Avatar')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Eye size={18} /> Inhabit Avatar
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <main className="@[440px]:col-span-8 space-y-10">
            <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Neural Interface Feed
                     <Badge color="aura">Sync-Active</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Real-time Kinesthetic Data • &lt;500ms Latency</p>
               </div>

               {/* 3D Humanoid Model Stub */}
               <div className="relative z-10">
                  <User size={240} className="text-aura opacity-20 animate-pulse-slow" />
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 10, ease: "linear" }} className="absolute -inset-10 border border-aura/10 border-dashed rounded-full" />
               </div>

               <div className="absolute bottom-10 flex gap-6 z-10">
                  <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 rounded-xl">
                     <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                     <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Soma-Sync Locked</span>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <Cpu size={24} className="text-aura" />
                  Available Embodiments
               </h3>
               <div className="space-y-4">
                  {platforms.map((plat, i) => (
                    <motion.div
                      key={plat.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all`}>
                             {plat.type === 'BCI' ? <Brain size={24} /> : plat.type === 'Robotic' ? <Activity size={24} /> : <User size={24} />}
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{plat.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{plat.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-emerald-500">{plat.battery}</span>
                             </div>
                          </div>
                       </div>
                       <Badge color={plat.status === 'Ready' ? 'emerald-500' : 'aura'}>{plat.status}</Badge>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </main>

         <aside className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Zap size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Kinesthetic Mapping</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Map your digital intent to physical degrees of freedom. Article 1148 governs safe robotic embodiment.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10 text-[10px] font-black uppercase text-slate-500">
                  <div className="flex justify-between items-center">
                     <span>DOFs Active</span>
                     <span className="text-white">142</span>
                  </div>
                  <div className="flex justify-between items-center">
                     <span>Haptic Feedback</span>
                     <span className="text-emerald-500">CONNECTED</span>
                  </div>
               </div>
               <Button onClick={() => notImplemented('Calibrate Mapping')} className="w-full bg-aura text-sovereign py-5 rounded-2xl font-black text-[10px] uppercase tracking-widest">Calibrate Mapping</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Neural Signal Vitals</h4>
               <div className="h-40 flex items-end gap-1 px-4">
                  {[40, 65, 35, 80, 50, 90, 70, 45, 85, 60, 35, 75].map((h, i) => (
                    <motion.div
                      key={i}
                      animate={{ height: [`${h}%`, `${h+10}%`, `${h}%`] }}
                      transition={{ duration: 1, repeat: Infinity, delay: i * 0.1 }}
                      className="flex-1 bg-aura/40 rounded-t-sm"
                    />
                  ))}
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Synthetic bodies are equipped with local GaaS-Edge for instantaneous rule enforcement.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
