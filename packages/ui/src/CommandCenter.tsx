import React, { useState } from 'react';
import { useStore, gaas } from '@workstation/shared';
import { User, Bell, Radio, FileText, BarChart3, Sparkles, ShieldCheck, X, Activity, MessageCircle, Heart, Brain, Zap, Clock, TrendingUp, Cpu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button, Badge } from './index';
import AgentForge from '../../../apps/web/src/components/organism/AgentForge';
import OrganismVitals from '../../../apps/web/src/components/organism/OrganismVitals';
import NeuralLink from '../../../apps/web/src/components/organism/NeuralLink';
import SpatioTemporal from '../../../apps/web/src/components/organism/SpatioTemporal';

export const CommandCenter = () => {
  const { currentRealm, currentMode } = useStore();
  const [activeChannel, setActiveChannel] = useState<string | null>(null);

  const channels = [
    { id: 'avatar', name: 'Avatar', icon: User, color: 'text-aura', description: 'Real-time Interaction' },
    { id: 'notification', name: 'Notification', icon: Bell, color: 'text-highlight', description: 'System Alerts' },
    { id: 'signal', name: 'Signal', icon: Radio, color: 'text-vital', description: 'Agent Pheromones' },
    { id: 'summary', name: 'Summary', icon: FileText, color: 'text-aura', description: 'AI Reports' },
    { id: 'dashboard', name: 'Dashboard', icon: BarChart3, color: 'text-highlight', description: 'Live Metrics' },
    { id: 'predictive', name: 'Predictive', icon: Sparkles, color: 'text-vital', description: 'Forecasting' },
    { id: 'neural', name: 'Neural Link', icon: Zap, color: 'text-vital', description: 'L13 Interface' },
    { id: 'spatio', name: 'Spatio-Temporal', icon: Clock, color: 'text-aura', description: 'L14 Mapping' },
    { id: 'forge', name: 'Agent Forge', icon: Cpu, color: 'text-aura', description: 'Visual Composer' },
    { id: 'ethical', name: 'Ethical', icon: ShieldCheck, color: 'text-aura', description: 'Constitutional AI' },
  ];

  return (
    <>
    <div className="fixed left-6 top-1/2 -translate-y-1/2 flex flex-col gap-4 z-[100]">
      <div className={`p-4 rounded-[2rem] bg-slate-950/80 border border-slate-900 backdrop-blur-3xl flex flex-col gap-5 shadow-2xl transition-all ${currentMode === 'REST' ? 'grayscale-[50%] opacity-80' : ''}`}>
        {channels.map((channel) => (
          <button
            key={channel.id}
            onClick={() => setActiveChannel(channel.id)}
            className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all group relative ${activeChannel === channel.id ? 'bg-aura text-sovereign shadow-xl shadow-aura/20' : 'bg-slate-900 text-slate-500 hover:bg-slate-800 hover:text-white hover:scale-110'}`}
          >
            <channel.icon size={22} />

            {/* Tooltip */}
            <div className="absolute left-16 px-4 py-2 bg-slate-950 border border-slate-900 rounded-xl opacity-0 group-hover:opacity-100 transition-all whitespace-nowrap pointer-events-none text-[10px] font-black uppercase tracking-widest text-aura shadow-2xl z-[110] -translate-x-2 group-hover:translate-x-0">
               {channel.name}
               <div className="text-slate-500 font-bold mt-1 text-[8px]">{channel.description}</div>
            </div>
          </button>
        ))}

        <div className="h-px bg-slate-900 mx-2" />

        <div className="flex flex-col gap-2 items-center">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
          <span className="text-[8px] font-black text-slate-700 uppercase tracking-widest vertical-rl">Live</span>
        </div>
      </div>
    </div>

    <AnimatePresence>
       {activeChannel && (
         <div className="fixed inset-0 z-[200] flex items-center justify-center p-8 pointer-events-none">
            <motion.div
               initial={{ opacity: 0, scale: 0.9, x: -50 }}
               animate={{ opacity: 1, scale: 1, x: 0 }}
               exit={{ opacity: 0, scale: 0.9, x: -50 }}
               className="w-[480px] bg-slate-950/90 border border-aura/20 rounded-[3rem] shadow-2xl pointer-events-auto overflow-hidden backdrop-blur-3xl ml-24"
            >
               <div className="p-8 border-b border-white/5 bg-aura/5 flex justify-between items-center">
                  <div className="flex items-center gap-4">
                     <div className="w-12 h-12 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                        {channels.find(c => c.id === activeChannel)?.icon({ size: 24 })}
                     </div>
                     <div>
                        <h3 className="text-xl font-black text-white uppercase tracking-tight">{activeChannel} Channel</h3>
                        <p className="text-[10px] font-black text-aura uppercase tracking-widest">Multi-Modal Fabric v3.0</p>
                     </div>
                  </div>
                  <button onClick={() => setActiveChannel(null)} className="p-3 text-slate-500 hover:text-white hover:bg-white/5 rounded-2xl transition-all">
                     <X size={20} />
                  </button>
               </div>

               <div className="p-8 max-h-[600px] overflow-y-auto custom-scrollbar space-y-6">
                  <ChannelContent id={activeChannel} />
               </div>

               <div className="p-6 border-t border-white/5 bg-slate-950/50 flex gap-3">
                  <input placeholder={`Query ${activeChannel} channel...`} className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl px-5 py-3 text-xs text-white focus:outline-none focus:border-aura/30" />
                  <button className="p-3 bg-aura text-sovereign rounded-2xl shadow-xl shadow-aura/20 hover:scale-110 transition-all">
                     <MessageCircle size={20} />
                  </button>
               </div>
            </motion.div>
         </div>
       )}
    </AnimatePresence>
    </>
  );
};

const ChannelContent = ({ id }: { id: string }) => {
   const { currentRealm, currentMode } = useStore();

   const contents: Record<string, any> = {
      avatar: (
         <div className="space-y-6 text-center">
            <div className="relative mx-auto w-40 h-40">
               <div className="absolute inset-0 rounded-full border-4 border-aura/20 animate-pulse-slow" />
               <div className="w-full h-full rounded-full bg-slate-900 border-2 border-aura flex items-center justify-center overflow-hidden">
                  <User size={80} className="text-aura opacity-30" />
               </div>
               <div className="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-emerald-500 border-4 border-slate-950 flex items-center justify-center">
                  <Activity size={14} className="text-white" />
               </div>
            </div>
            <div className="space-y-2">
               <h4 className="text-lg font-black text-white">Sovereign Avatar Active</h4>
               <p className="text-xs text-slate-400 font-bold leading-relaxed px-6">
                  WebRTC stream synchronized. Current Persona: <span className="text-aura uppercase tracking-widest">{currentRealm}</span>.
                  <br/>Latency: <span className="text-emerald-500">18ms</span>
               </p>
            </div>
            <div className="grid grid-cols-2 gap-3">
               <Button variant="outline" className="text-[9px]">Switch Persona</Button>
               <Button variant="outline" className="text-[9px]">Calibrate Voice</Button>
            </div>
         </div>
      ),
      neural: (
         <div className="space-y-6">
            <NeuralLink />
         </div>
      ),
      spatio: (
         <div className="space-y-6">
            <SpatioTemporal />
         </div>
      ),
      predictive: (
         <div className="space-y-6">
            <div className="p-6 rounded-3xl bg-slate-900/50 border border-white/5 space-y-6">
               <div className="flex justify-between items-center">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Time-Series Forecast</p>
                  <TrendingUp size={16} className="text-aura" />
               </div>
               <div className="h-24 flex items-end gap-1 px-2">
                  {[40, 65, 35, 80, 50, 90, 70, 45, 85, 60, 35, 75].map((h, i) => (
                    <div key={i} className="flex-1 bg-aura/20 rounded-t-sm" style={{ height: `${h}%` }} />
                  ))}
               </div>
               <div className="space-y-4">
                  <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                     <Activity size={18} className="text-vital" />
                     <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">Resonance drop predicted at 14:00Z.</p>
                  </div>
                  <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                     <Zap size={18} className="text-aura" />
                     <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">Energy surplus detected in L2 CL1 nodes.</p>
                  </div>
               </div>
            </div>

            {/* Proactive Suggestions Section */}
            <div className="space-y-4">
               <div className="flex items-center gap-3">
                  <Brain size={18} className="text-aura" />
                  <h4 className="text-sm font-black text-white uppercase tracking-widest">RL-Powered Suggestions</h4>
               </div>
               <div className="p-6 rounded-3xl bg-aura/5 border border-aura/10 border-dashed space-y-4">
                  <p className="text-xs text-slate-400 font-bold leading-relaxed italic">
                     "You've been in WORK mode for 4 hours. Suggesting a transition to REST to optimize cognitive durability."
                  </p>
                  <div className="flex gap-3">
                     <Button className="flex-1 text-[9px] py-2">Apply REST Mode</Button>
                     <Button variant="ghost" className="text-[9px] py-2">Dismiss</Button>
                  </div>
               </div>
            </div>
         </div>
      ),
      forge: (
         <div className="space-y-6">
            <AgentForge />
         </div>
      ),
      dashboard: (
         <div className="space-y-6">
            <OrganismVitals />
         </div>
      ),
      ethical: (
         <div className="space-y-6">
            <div className="p-8 rounded-3xl bg-aura/5 border border-aura/20 relative overflow-hidden">
               <div className="absolute top-0 right-0 p-4 opacity-10">
                  <ShieldCheck size={60} className="text-aura" />
               </div>
               <p className="text-[10px] font-black text-aura uppercase tracking-widest mb-4">Constitutional Alignment</p>
               <p className="text-sm text-white font-bold leading-relaxed relative z-10">
                  Current session conforms to <span className="text-aura">Floor 24</span> mandates. Article 1126 (Care Ethics) is actively enforcing compassionate guardrails.
               </p>
            </div>

            <div className="space-y-3">
               <div className="flex justify-between items-center p-4 rounded-2xl bg-slate-900 border border-slate-800">
                  <div className="flex items-center gap-3">
                     <Clock size={16} className="text-slate-500" />
                     <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest">Veto Window Status</span>
                  </div>
                  <Badge color="emerald-500">IDLE</Badge>
               </div>
               <div className="flex justify-between items-center p-4 rounded-2xl bg-slate-900 border border-slate-800">
                  <div className="flex items-center gap-3">
                     <Activity size={16} className="text-slate-500" />
                     <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest">Privacy ε Budget</span>
                  </div>
                  <span className="text-xs font-black text-white">0.08 / 0.1</span>
               </div>
            </div>

            <Button variant="outline" className="w-full">View Full Ethical Audit</Button>
         </div>
      )
   };

   return contents[id] || (
      <div className="p-20 text-center space-y-6">
         <div className="w-16 h-16 rounded-2xl bg-slate-900 mx-auto flex items-center justify-center text-slate-700 animate-pulse">
            <Radio size={32} />
         </div>
         <p className="text-[10px] text-slate-600 font-black uppercase tracking-widest">
            Real-time stream initializing via libp2p...
         </p>
      </div>
   );
};
