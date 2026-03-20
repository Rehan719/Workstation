import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useGamificationStore } from '../store/gamificationStore';
import { TrendingUp, Users, Cpu, Zap, ArrowUpRight, ShieldCheck, Activity, Globe } from 'lucide-react';
import { ResonanceMap } from '../components/federation/ResonanceMap';

const stats = [
  { label: 'Entity Status', value: 'v3.0 Sovereign', delta: 'Unified', icon: ShieldCheck, color: 'text-aura' },
  { label: 'Resonance', value: '99.98%', delta: 'Optimal', icon: Zap, color: 'text-aura' },
  { label: 'Mesh Depth', value: '1.42M', delta: '+142k/hr', icon: Globe, color: 'text-highlight' },
  { label: 'Autopoiesis', value: 'Active', delta: 'Self-Evolving', icon: Activity, color: 'text-vital' },
];

export const Dashboard: React.FC = () => {
  const { completeQuest } = useGamificationStore();

  const { fetchQuests } = useGamificationStore();

  useEffect(() => {
    fetchQuests('guardian');
    completeQuest('guardian', 'q-001');
  }, []);

  return (
    <div className="space-y-6">
      <div className="p-4 bg-highlight/10 border border-highlight/30 rounded-2xl flex items-center justify-between">
         <div className="flex items-center gap-4">
            <div className="p-2 bg-highlight/20 rounded-lg text-highlight">
               <Heart size={16} fill="currentColor" />
            </div>
            <p className="text-xs font-bold text-highlight uppercase tracking-wider">Playful Sovereignty Manifesto: The Workstation is now free for all humanity.</p>
         </div>
         <button className="px-4 py-1.5 bg-highlight text-sovereign font-black rounded-lg text-[10px] uppercase hover:scale-105 transition-all">Support on Open Collective</button>
      </div>
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="space-y-12"
      role="main"
      aria-label="Workstation Dashboard"
    >
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
           <h1 className="text-6xl font-black tracking-tighter mb-3 neon-text">
             Welcome back, <span className="text-white">Guardian</span>
           </h1>
           <p className="text-slate-500 font-bold text-lg max-w-2xl leading-relaxed">
             The Workstation ecosystem is resonating at <span className="text-aura font-black">optimal frequencies</span> across the planetary network.
           </p>
        </div>
        <div className="flex gap-4">
           <button className="interactive-button py-4 px-8 text-xs">Synchronize Vitals</button>
        </div>
      </header>

      <section aria-label="System Overview Stats" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className="p-8 glass-card group cursor-pointer"
            tabIndex={0}
            role="article"
          >
            <div className="flex justify-between items-start mb-8">
              <div className={`p-4 rounded-2xl bg-surface/80 border border-white/5 ${stat.color} shadow-inner group-hover:scale-110 transition-transform duration-500`} aria-hidden="true">
                <stat.icon size={28} />
              </div>
              <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-surface border border-white/5 text-slate-400 uppercase tracking-widest" aria-label={`Change: ${stat.delta}`}>
                {stat.delta}
              </span>
            </div>
            <div className="text-4xl font-black mb-1 tracking-tight" aria-label={`${stat.label} value is ${stat.value}`}>{stat.value}</div>
            <div className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">{stat.label}</div>
          </motion.div>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <section aria-label="UEG Resonance Map" className="lg:col-span-2 glass-card h-[550px] overflow-hidden relative group">
           <div className="absolute top-8 left-8 z-10">
              <h3 className="text-2xl font-black tracking-tight mb-1">Planetary Resonance</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">UEG Unified State Graph</p>
           </div>
           <ResonanceMap />
           <div className="absolute top-8 right-8 z-10">
              <button className="p-3 bg-surface/80 border border-white/10 rounded-xl hover:border-aura/50 transition-colors">
                 <ArrowUpRight size={20} className="text-aura" />
              </button>
           </div>
        </section>

        <section aria-label="Recent Activity Log" className="p-12 glass-card h-[550px] flex flex-col">
          <h3 className="text-2xl font-black mb-8 tracking-tight">Recent Activity</h3>
          <div className="space-y-6 overflow-y-auto custom-scrollbar pr-2 flex-1" aria-live="polite">
            {[
              { t: 'Protocol v148.0 Synchronized', m: 'Planetary', c: 'aura' },
              { t: 'PQC Handshake Successful', m: 'Security', c: 'vital' },
              { t: 'Marketplace Deployment', m: 'Economy', c: 'highlight' },
              { t: 'Guardian Vote Recorded', m: 'Governance', c: 'aura' },
              { t: 'Neural Operon Mutation', m: 'Evolution', c: 'vital' }
            ].map((act, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + (i * 0.1) }}
                className="flex gap-5 p-5 rounded-[1.5rem] bg-surface/30 border border-white/5 hover:bg-surface/50 transition-colors cursor-pointer group"
                tabIndex={0}
              >
                <div className={`w-2 h-2 rounded-full bg-${act.c} mt-2 shadow-[0_0_12px_rgba(100,255,218,0.5)] group-hover:scale-125 transition-transform`}></div>
                <div>
                  <p className="text-sm font-black group-hover:text-aura transition-colors">{act.t}</p>
                  <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest mt-1">{act.m} • JUST NOW</p>
                </div>
              </motion.div>
            ))}
          </div>
        </section>
      </div>
    </motion.div>
    </div>
  );
};
