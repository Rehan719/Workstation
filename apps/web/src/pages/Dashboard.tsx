import React, { useState, useEffect } from 'react';
import { Card, RealmSelector, AvatarPlaceholder } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { ShieldCheck, Zap, Cpu, Users, Activity, Globe, Heart, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

export const Dashboard: React.FC = () => {
  const { systemVitals, user } = useStore();

  const stats = [
    { label: 'Status', value: 'v3.0 Sovereign', icon: ShieldCheck, color: 'text-aura' },
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(2)}%`, icon: Zap, color: 'text-yellow-400' },
    { label: 'Latency', value: '28.5ms', icon: Cpu, color: 'text-highlight' },
    { label: 'Mesh Size', value: '50+ Nodes', icon: Users, color: 'text-vital' },
  ];

  return (
    <div className="space-y-12 pb-24">
      {/* Article 1108: Economic Sustainability Badge */}
      <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl flex items-center justify-between">
         <div className="flex items-center gap-4">
            <div className="p-2 bg-emerald-500/20 rounded-lg text-emerald-500">
               <ShieldCheck size={16} />
            </div>
            <p className="text-xs font-bold text-emerald-500 uppercase tracking-wider">Economic Independence Certified: 6 Months Profitability Verified.</p>
         </div>
         <span className="text-[10px] font-black text-emerald-600 bg-emerald-500/5 px-3 py-1 rounded-full uppercase">Quarterly Audit: Passed</span>
      </div>

      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-7xl font-black tracking-tighter mb-4 neon-text">
            Sovereign <span className="text-aura">v3.0</span>
          </h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Welcome back, <span className="text-white">{user?.displayName}</span>. The <span className="text-aura">Civilization Epoch</span> is operational across the planetary mesh.
          </p>
        </div>
        <div className="flex flex-col gap-4 items-end">
          <RealmSelector />
          <div className="flex gap-2">
             <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-500 uppercase tracking-widest">L11-Active</span>
             <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-mono text-emerald-500 uppercase tracking-widest">PQC-Mandatory</span>
          </div>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div key={stat.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <Card className="group cursor-pointer hover:border-aura/50 transition-all">
              <div className="flex justify-between items-start mb-6">
                <div className={`p-3 rounded-xl bg-slate-800/50 ${stat.color}`}>
                  <stat.icon size={24} />
                </div>
                <span className="text-[10px] font-black px-2 py-1 rounded-lg bg-slate-950 text-slate-500 uppercase tracking-widest">Live</span>
              </div>
              <div className="text-3xl font-black mb-1">{stat.value}</div>
              <div className="text-[10px] font-black uppercase tracking-widest text-slate-500">{stat.label}</div>
            </Card>
          </motion.div>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
           <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950/20">
              <div className="absolute top-8 left-8 z-10">
                 <h3 className="text-2xl font-black tracking-tight">Planetary Resonance</h3>
                 <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">libp2p Gossipsub Visualization</p>
              </div>
              <Globe size={240} className="text-aura opacity-20 animate-pulse-slow" />
              <div className="absolute bottom-8 right-8 z-10 flex gap-4">
                 <button className="px-6 py-3 bg-aura/10 border border-aura/30 text-aura rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-aura hover:text-sovereign transition-all">Mesh Explorer</button>
              </div>
           </Card>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card>
                 <h4 className="text-lg font-black mb-6 flex items-center gap-2">
                    <Activity size={18} className="text-vital" />
                    Evolution Stream
                 </h4>
                 <div className="space-y-4">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="flex gap-4 items-start p-4 rounded-2xl bg-slate-950/50 border border-slate-900 group hover:border-aura/30 transition-all">
                         <div className="w-1.5 h-1.5 rounded-full bg-aura mt-2 animate-pulse" />
                         <div>
                            <div className="text-xs font-bold text-slate-300">MergeKit Success</div>
                            <div className="text-[9px] text-slate-500 uppercase tracking-tighter">Layer 8 • {i*2}m ago • TIES</div>
                         </div>
                      </div>
                    ))}
                 </div>
              </Card>
              <Card className="bg-vital/5 border-vital/20">
                 <h4 className="text-lg font-black mb-4 text-vital flex items-center gap-2">
                    <AlertTriangle size={18} />
                    Emergency Protocol
                 </h4>
                 <p className="text-xs text-slate-500 font-bold mb-6 leading-relaxed">
                    Article 1101: 10-minute veto window active for high-risk autonomous workflows. GaaS enforcement status: <span className="text-vital">STRICT</span>.
                 </p>
                 <button className="w-full py-4 border border-vital text-vital font-black rounded-xl text-[10px] uppercase tracking-widest hover:bg-vital hover:text-white transition-all">Open Veto Console</button>
              </Card>
           </div>
        </div>

        <div className="space-y-8">
           <Card className="flex flex-col items-center py-12 text-center">
              <AvatarPlaceholder mood="speaking" />
              <div className="mt-10">
                 <h3 className="text-2xl font-black mb-2 text-white">VSB AI CEO</h3>
                 <p className="text-sm text-slate-500 font-bold max-w-[200px] mx-auto leading-relaxed">"Sovereignty isn't just local—it's <span className="text-aura">federated and anti-fragile</span>."</p>
              </div>
              <button className="mt-10 w-full py-5 rounded-2xl bg-white text-sovereign font-black text-xs uppercase tracking-[0.2em] hover:bg-aura transition-all shadow-2xl">Consult VSB CEO</button>
           </Card>

           <Card>
              <h4 className="text-lg font-black mb-6">Market Vitals</h4>
              <div className="space-y-6">
                 <div className="flex justify-between items-end">
                    <span className="text-[10px] font-black uppercase text-slate-500">WST Circulation</span>
                    <span className="text-xl font-black text-white">1.2M+</span>
                 </div>
                 <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                    <div className="h-full bg-aura w-[85%]" />
                 </div>
              </div>
           </Card>
        </div>
      </div>
    </div>
  );
};
