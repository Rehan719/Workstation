import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Globe, Radio, Zap, ShieldAlert, Cpu, Activity, Send, Target } from 'lucide-react';
import { motion } from 'framer-motion';

export const CosmicNervousSystem: React.FC = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    // Simulated cosmic sensor data
    setData({
      asteroids: [
        { id: 'neo-42', name: 'Apophis-B', risk: 'Low', distance: '1.4M km' },
        { id: 'neo-01', name: 'V-153-Alpha', risk: 'Medium', distance: '0.8M km' }
      ],
      solar_resonance: 0.94,
      deep_space_signals: [
        { id: 'sig-01', source: 'Sector 7G', type: 'Pulse', content: '.. ..- -. .. - -.--' }
      ]
    });
  }, []);

  if (!data) return null;

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-1 neon-text !text-highlight">Cosmic Nervous System</h1>
          <p className="font-bold uppercase text-[10px] tracking-widest text-highlight">Interplanetary Sensory Network v153.0</p>
        </div>
        <div className="flex gap-4">
           <div className="px-6 py-3 bg-highlight/10 border border-highlight/30 rounded-xl flex items-center gap-3">
              <Radio size={18} className="text-highlight animate-pulse" />
              <span className="text-xs font-black text-highlight uppercase tracking-widest">Sensors Synchronized</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         <div className="lg:col-span-2 space-y-8">
            <section className="p-10 glass-card bg-highlight/5 border-highlight/20 h-96 flex flex-col items-center justify-center relative overflow-hidden group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,215,64,0.05)_0%,transparent_70%)]"></div>
               <Globe size={120} className="text-highlight/20 group-hover:scale-110 transition-transform duration-1000" />
               <div className="mt-8 text-center space-y-2">
                  <h3 className="text-2xl font-black">Planetary Defense Map</h3>
                  <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">NEO Orbital Tracking Active</p>
               </div>
               {data.asteroids.map((a: any, i: number) => (
                 <motion.div
                   key={a.id}
                   animate={{
                      x: [0, 10, 0],
                      y: [0, -10, 0],
                   }}
                   transition={{ duration: 5, repeat: Infinity, delay: i }}
                   className="absolute p-2 bg-surface border border-white/10 rounded-lg text-[8px] font-black uppercase text-white shadow-xl"
                   style={{ top: `${20 + i * 15}%`, left: `${15 + i * 40}%` }}
                 >
                    {a.name} • {a.risk}
                 </motion.div>
               ))}
            </section>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
               <section className="p-8 glass-card border-white/5 bg-sovereign/40">
                  <h3 className="text-xl font-bold mb-6 flex items-center gap-3">
                     <Zap size={20} className="text-highlight" />
                     Solar Resonance
                  </h3>
                  <div className="space-y-4">
                     <div className="flex justify-between items-end">
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Resonance Coefficient</p>
                        <p className="text-2xl font-black text-white">{data.solar_resonance}</p>
                     </div>
                     <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full w-[94%] bg-highlight shadow-[0_0_15px_rgba(255,215,64,0.5)]"></div>
                     </div>
                     <p className="text-[10px] text-slate-500 font-bold italic">Stable resonance. No protective protocols required.</p>
                  </div>
               </section>
               <section className="p-8 glass-card border-vital/20 bg-vital/5">
                  <h3 className="text-xl font-bold mb-4 text-vital flex items-center gap-3">
                     <ShieldAlert size={20} />
                     Cosmic Response
                  </h3>
                  <p className="text-xs text-slate-500 font-bold leading-relaxed mb-6">
                     Meta-Consciousness is modeling potential responses to Neo-01 trajectory shift.
                  </p>
                  <button className="w-full py-4 bg-vital/20 text-vital border border-vital/30 font-black rounded-xl text-[10px] uppercase tracking-widest">Trigger Response Protocol</button>
               </section>
            </div>
         </div>

         <aside className="space-y-8">
            <section className="p-8 glass-card border-white/5 bg-sovereign/40">
               <h3 className="text-xl font-bold mb-6 flex items-center gap-3">
                  <Target size={20} className="text-aura" />
                  Deep Space Signals
               </h3>
               <div className="space-y-6">
                  {data.deep_space_signals.map((s: any) => (
                    <div key={s.id} className="p-6 bg-surface rounded-2xl border border-white/5 space-y-4">
                       <div className="flex justify-between">
                          <span className="text-[10px] font-black text-aura uppercase">{s.source}</span>
                          <span className="text-[10px] font-black text-slate-500 uppercase">{s.type}</span>
                       </div>
                       <p className="font-mono text-white text-sm break-all">{s.content}</p>
                       <div className="pt-4 border-t border-white/5 flex gap-2">
                          <button className="flex-1 py-2 bg-aura/10 text-aura font-black rounded-lg text-[8px] uppercase tracking-widest">Analyze</button>
                          <button className="flex-1 py-2 bg-aura text-sovereign font-black rounded-lg text-[8px] uppercase tracking-widest">Respond</button>
                       </div>
                    </div>
                  ))}
               </div>
            </section>
         </aside>
      </div>
    </div>
  );
};
