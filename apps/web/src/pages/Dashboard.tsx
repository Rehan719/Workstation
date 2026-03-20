import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '@workstation/shared';
import { TrendingUp, Users, Cpu, Zap, ArrowUpRight, ShieldCheck, Activity, Globe, LayoutGrid, GraduationCap, Code, Building2, BookOpen } from 'lucide-react';
import { Card, RealmSelector, AvatarPlaceholder } from '@workstation/ui';

export const Dashboard: React.FC = () => {
  const { currentRealm, systemVitals, user } = useStore();

  const stats = [
    { label: 'Entity Status', value: 'v3.0 Sovereign', delta: 'Unified', icon: ShieldCheck, color: 'text-aura' },
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(2)}%`, delta: 'Optimal', icon: Zap, color: 'text-aura' },
    { label: 'CPU Load', value: `${systemVitals.cpu.toFixed(1)}%`, delta: 'Stable', icon: Cpu, color: 'text-highlight' },
    { label: 'Active Agents', value: systemVitals.activeAgents.toString(), delta: '+3/hr', icon: Users, color: 'text-vital' },
  ];

  const realms = [
    { id: 'LEARNER', name: 'Learner Realm', icon: GraduationCap, desc: 'Garden of Curiosity' },
    { id: 'DEVELOPER', name: 'Developer Realm', icon: Code, desc: 'Forge of Creation' },
    { id: 'ENTERPRISE', name: 'Enterprise Realm', icon: Building2, desc: 'Forest of Collaboration' },
    { id: 'SCHOLAR', name: 'Scholar Realm', icon: BookOpen, desc: 'Observatory of Understanding' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-7xl font-black tracking-tighter mb-4">
            Sovereign <span className="text-aura">v3.0</span>
          </h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Welcome, <span className="text-white">{user?.displayName}</span>. The Workstation ecosystem is resonating across <span className="text-aura">7 layers</span> of distributed intelligence.
          </p>
        </div>
        <div className="flex flex-col gap-4 items-end">
          <RealmSelector />
          <div className="flex gap-2">
            <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-500 uppercase tracking-widest">
              Epoch: Genesis
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-mono text-emerald-500 uppercase tracking-widest">
              Online
            </span>
          </div>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card className="group cursor-pointer hover:border-aura/50 transition-all">
              <div className="flex justify-between items-start mb-6">
                <div className={`p-3 rounded-xl bg-slate-800/50 ${stat.color}`}>
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
          <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden">
            <div className="absolute top-8 left-8">
              <h3 className="text-2xl font-black tracking-tight">Unified Interface</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Active Realm: {currentRealm}</p>
            </div>

            <div className="grid grid-cols-2 gap-4 w-full max-w-lg mt-12">
              {realms.map((realm) => (
                <button
                  key={realm.id}
                  className={`p-6 rounded-2xl border transition-all text-left group ${
                    currentRealm === realm.id
                      ? 'bg-aura/10 border-aura shadow-lg shadow-aura/5'
                      : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <realm.icon size={32} className={`mb-4 ${currentRealm === realm.id ? 'text-aura' : 'text-slate-500 group-hover:text-slate-300'}`} />
                  <div className={`font-black text-sm ${currentRealm === realm.id ? 'text-white' : 'text-slate-400'}`}>{realm.name}</div>
                  <div className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{realm.desc}</div>
                </button>
              ))}
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card>
              <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                <Activity size={18} className="text-vital" />
                Evolution Stream
              </h4>
              <div className="space-y-4">
                {[1, 2, 3].map((_, i) => (
                  <div key={i} className="flex gap-4 items-start p-3 rounded-xl bg-slate-950/50 border border-slate-900">
                    <div className="w-1.5 h-1.5 rounded-full bg-aura mt-2 animate-pulse" />
                    <div>
                      <div className="text-xs font-bold">Model Recombination Proposed</div>
                      <div className="text-[9px] text-slate-500 uppercase tracking-tighter">Layer 5 • TIES Merging • 2m ago</div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
            <Card>
              <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                <Globe size={18} className="text-highlight" />
                Mycelial Mesh
              </h4>
              <div className="h-32 flex items-center justify-center border border-dashed border-slate-800 rounded-xl">
                 <span className="text-[10px] font-mono text-slate-600 uppercase tracking-[0.3em]">Visualizing Pheromones...</span>
              </div>
            </Card>
          </div>
        </div>

        <div className="space-y-8">
          <Card className="flex flex-col items-center py-12">
            <AvatarPlaceholder mood={currentRealm === 'UNIFIED' ? 'thinking' : 'speaking'} />
            <div className="mt-8 text-center">
              <h3 className="text-xl font-black mb-2">VSB AI CEO</h3>
              <p className="text-sm text-slate-400 font-bold max-w-[200px]">"Sovereignty is not given, it is computed at the edge."</p>
            </div>
            <button className="mt-8 w-full py-4 rounded-xl bg-slate-800 font-black text-xs uppercase tracking-widest hover:bg-aura hover:text-sovereign transition-all">
              Initiate Executive Consultation
            </button>
          </Card>

          <Card>
            <h4 className="text-lg font-black mb-6">Recent Activity</h4>
            <div className="space-y-4">
               {['PQC Handshake', 'UEG Sync', 'Article 1095 Validated'].map((item, i) => (
                 <div key={i} className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest py-2 border-b border-slate-800/50 last:border-0">
                    <span className="text-slate-500">{item}</span>
                    <span className="text-aura">Success</span>
                 </div>
               ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
