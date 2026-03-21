import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '@workstation/shared';
import { ShieldCheck, Zap, Cpu, Users, Activity, Globe, LayoutGrid, GraduationCap, Code, Building2, BookOpen, Heart } from 'lucide-react';
import { Card, RealmSelector, AvatarPlaceholder } from '@workstation/ui';

export const Dashboard: React.FC = () => {
  const { currentRealm, systemVitals, user } = useStore();

  const stats = [
    { label: 'Entity Status', value: 'v3.0 Sovereign', delta: 'Unified', icon: ShieldCheck, color: 'text-aura' },
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(2)}%`, delta: 'Optimal', icon: Zap, color: '#ffd740' },
    { label: 'CPU Load', value: `${systemVitals.cpu.toFixed(1)}%`, delta: 'Steady', icon: Cpu, color: '#38bdf8' },
    { label: 'Agents', value: systemVitals.activeAgents.toString(), delta: '+12/hr', icon: Users, color: '#ff5252' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <div className="p-4 bg-aura/10 border border-aura/30 rounded-2xl flex items-center justify-between">
         <div className="flex items-center gap-4">
            <div className="p-2 bg-aura/20 rounded-lg text-aura">
               <Heart size={16} fill="currentColor" />
            </div>
            <p className="text-xs font-bold text-aura uppercase tracking-wider">Civilization v3.0 Phase 2: Core Validation & Scaling Active.</p>
         </div>
         <button className="px-4 py-1.5 bg-aura text-sovereign font-black rounded-lg text-[10px] uppercase hover:scale-105 transition-all">Mesh Status: Healthy</button>
      </div>

      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-7xl font-black tracking-tighter mb-4 neon-text">
            Sovereign <span className="text-aura">v3.0</span>
          </h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Welcome, <span className="text-white">{user?.displayName}</span>. The Workstation ecosystem has entered the <span className="text-aura">Civilization Epoch</span>.
          </p>
        </div>
        <div className="flex flex-col gap-4 items-end">
          <RealmSelector />
          <div className="flex gap-2">
            <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-500 uppercase tracking-widest">
              Epoch: Civilization
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-mono text-emerald-500 uppercase tracking-widest">
              Mesh Active
            </span>
          </div>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div key={stat.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <Card className="group cursor-pointer hover:border-aura/50 transition-all">
              <div className="flex justify-between items-start mb-6">
                <div className={`p-3 rounded-xl bg-slate-800/50`} style={{ color: stat.color }}>
                  <stat.icon size={24} />
                </div>
                <span className="text-[10px] font-black px-2 py-1 rounded-lg bg-slate-950 text-slate-500 uppercase tracking-widest">
                  {stat.delta}
                </span>
              </div>
              <div className="text-3xl font-black mb-1">{stat.value}</div>
              <div className="text-[10px] font-black uppercase tracking-widest text-slate-500">{stat.label}</div>
            </Card>
          </motion.div>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950/20">
            <div className="absolute top-8 left-8 z-10">
              <h3 className="text-2xl font-black tracking-tight">Ecosystem Resonance</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Planetary Mesh Visualization (libp2p DHT)</p>
            </div>

            <div className="w-full h-full opacity-30 flex items-center justify-center">
               <Globe size={300} className="text-aura animate-pulse-slow" />
            </div>

            <div className="absolute bottom-8 right-8 z-10">
               <button className="px-6 py-3 bg-aura/10 border border-aura/30 text-aura rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-aura hover:text-sovereign transition-all">Open Mesh Explorer</button>
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
             <Card>
                <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                   <Activity size={18} className="text-vital" />
                   Evolution Stream
                </h4>
                <div className="space-y-4">
                   {[1, 2, 3].map(i => (
                     <div key={i} className="flex gap-4 items-start p-4 rounded-2xl bg-slate-950/50 border border-slate-900 group hover:border-aura/30 transition-all">
                        <div className="w-1.5 h-1.5 rounded-full bg-aura mt-2 animate-pulse" />
                        <div>
                           <div className="text-xs font-bold">MergeKit Success</div>
                           <div className="text-[9px] text-slate-500 uppercase tracking-tighter">Layer 8 • TIES-Merge • {i*2}m ago</div>
                        </div>
                     </div>
                   ))}
                </div>
             </Card>
             <Card>
                <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                   <LayoutGrid size={18} className="text-highlight" />
                   Ecosystem Audits
                </h4>
                <div className="space-y-4">
                   <div className="flex justify-between items-center p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                      <span className="text-[10px] font-black text-emerald-500 uppercase">OWASP ASI-01</span>
                      <span className="text-[10px] font-bold text-slate-400">Verified</span>
                   </div>
                   <div className="flex justify-between items-center p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                      <span className="text-[10px] font-black text-emerald-500 uppercase">PQC Compliance</span>
                      <span className="text-[10px] font-bold text-slate-400">Mandatory</span>
                   </div>
                   <div className="flex justify-between items-center p-3 rounded-xl bg-amber-500/5 border border-amber-500/20">
                      <span className="text-[10px] font-black text-amber-500 uppercase">SLF Reserve</span>
                      <span className="text-[10px] font-bold text-slate-400">142K WST</span>
                   </div>
                </div>
             </Card>
          </div>
        </div>

        <div className="space-y-8">
          <Card className="flex flex-col items-center py-12">
            <AvatarPlaceholder mood="thinking" />
            <div className="mt-10 text-center">
              <h3 className="text-2xl font-black mb-2 text-white">VSB AI CEO</h3>
              <p className="text-sm text-slate-500 font-bold max-w-[240px] leading-relaxed">"The civilization epoch demands a new standard of <span className="text-aura">autonomous integrity</span>."</p>
            </div>
            <button className="mt-10 w-full py-5 rounded-2xl bg-white text-sovereign font-black text-xs uppercase tracking-[0.2em] hover:bg-aura transition-all shadow-2xl">
              Initiate Consultation
            </button>
          </Card>

          <Card className="bg-vital/5 border-vital/20">
             <h4 className="text-lg font-black mb-6 text-vital">Emergency Protocol</h4>
             <p className="text-xs text-slate-500 font-bold mb-8 leading-relaxed">Article 1081: 888_HOLD logic is active. 10-minute veto window required for all high-risk autonomous workflows.</p>
             <button className="w-full py-4 border border-vital text-vital font-black rounded-xl text-[10px] uppercase tracking-widest hover:bg-vital hover:text-white transition-all">Manual Veto System</button>
          </Card>
        </div>
      </div>
    </div>
  );
};
