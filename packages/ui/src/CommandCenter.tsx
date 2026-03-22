import React, { useState } from 'react';
import { useStore, gaas } from '@workstation/shared';
import { User, Bell, Radio, FileText, BarChart3, Sparkles, ShieldCheck, X, Activity, MessageCircle, Heart } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

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
               className="w-[420px] bg-slate-950/90 border border-aura/20 rounded-[3rem] shadow-2xl pointer-events-auto overflow-hidden backdrop-blur-3xl ml-24"
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

               <div className="p-8 max-h-[500px] overflow-y-auto custom-scrollbar space-y-6">
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
   const { currentRealm } = useStore();

   const contents: Record<string, any> = {
      avatar: (
         <div className="space-y-4 text-center">
            <div className="w-32 h-32 rounded-full bg-slate-900 border-2 border-aura mx-auto flex items-center justify-center">
               <User size={64} className="text-aura opacity-20" />
            </div>
            <p className="text-sm text-slate-400 font-bold leading-relaxed px-4">
               Avatar streaming is active for the <span className="text-aura">{currentRealm}</span> persona. Latency &lt;200ms verified.
            </p>
            <div className="flex gap-2 justify-center">
               <Badge color="emerald-500">LiveKit Connected</Badge>
               <Badge color="aura">High Fidelity</Badge>
            </div>
         </div>
      ),
      predictive: (
         <div className="space-y-6">
            <div className="p-6 rounded-2xl bg-slate-900/50 border border-white/5">
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Domain Insights</p>
               <div className="space-y-4">
                  <div className="flex items-center gap-4">
                     <Activity size={18} className="text-vital" />
                     <p className="text-xs font-bold text-slate-300">Predicted system resonance drop in 2h.</p>
                  </div>
                  <div className="flex items-center gap-4">
                     <Heart size={18} className="text-emerald-500" />
                     <p className="text-xs font-bold text-slate-300">Learner mastery bloom expected for "Genomics".</p>
                  </div>
               </div>
            </div>
            <Button variant="outline" className="w-full">Export Forecast Trace</Button>
         </div>
      ),
      ethical: (
         <div className="space-y-6">
            <div className="p-6 rounded-2xl bg-aura/5 border border-aura/20 border-dashed">
               <p className="text-[10px] font-black text-aura uppercase tracking-widest mb-2">Article 1126 Compliance</p>
               <p className="text-xs text-slate-400 font-bold leading-relaxed">
                  "AI agents in Care realm trained on care ethics... provide empathetic responses."
               </p>
            </div>
            <div className="space-y-3">
               <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[10px] font-black text-slate-300">Audit Status</span>
                  <Badge color="emerald-500">PASSING</Badge>
               </div>
               <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[10px] font-black text-slate-300">Risk Mitigation</span>
                  <span className="text-[10px] font-black text-white">ACTIVE</span>
               </div>
            </div>
         </div>
      )
   };

   return contents[id] || (
      <div className="p-10 text-center text-slate-600 font-black uppercase tracking-widest text-xs">
         Real-time stream initializing...
      </div>
   );
};

export const RealmSelector = () => {
  const { currentRealm, setCurrentRealm } = useStore();

  const realms = ['UNIFIED', 'LEARNER', 'DEVELOPER', 'ENTERPRISE', 'SCHOLAR'] as const;

  return (
    <div className="flex gap-4 p-2 rounded-2xl bg-slate-950/80 border border-slate-900 w-fit backdrop-blur-xl">
      {realms.map((realm) => (
        <button
          key={realm}
          onClick={() => setCurrentRealm(realm)}
          className={`px-5 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
            currentRealm === realm
              ? 'bg-aura text-sovereign shadow-xl shadow-aura/20'
              : 'text-slate-500 hover:text-slate-300 hover:bg-slate-900'
          }`}
        >
          {realm}
        </button>
      ))}
    </div>
  );
};
