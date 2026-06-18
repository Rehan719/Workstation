import React from 'react';
import { motion } from 'framer-motion';
import { Card, RealmSelector, notImplemented} from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { Book, Compass, Star, Users, ArrowRight, Flower2, Activity } from 'lucide-react';

import { MessageSquare, Bell, Zap, FileText, Layout, BarChart, ShieldCheck } from 'lucide-react';

export const LearnerRealm: React.FC = () => {
  const { user } = useStore();

  const channels = [
    { id: 'avatar', icon: <MessageSquare size={16} />, label: 'Avatar', status: 'streaming' },
    { id: 'notification', icon: <Bell size={16} />, label: 'Notify', status: 'online' },
    { id: 'signal', icon: <Zap size={16} />, label: 'Signal', status: 'low-latency' },
    { id: 'summary', icon: <FileText size={16} />, label: 'Summary', status: 'daily' },
    { id: 'dashboard', icon: <Layout size={16} />, label: 'Console', status: 'active' },
    { id: 'predictive', icon: <BarChart size={16} />, label: 'Predict', status: 'forecasting' },
    { id: 'ethical', icon: <ShieldCheck size={16} />, label: 'Ethical', status: 'transparent' },
  ];

  const gardens = [
    { name: 'Quantum Mechanics', progress: 88, flowers: 3, level: 'Advanced' },
    { name: 'Systems Biology', progress: 45, flowers: 1, level: 'Intermediate' },
    { name: 'Agentic Ethics', progress: 95, flowers: 4, level: 'Master' },
    { name: 'PQC Foundations', progress: 12, flowers: 0, level: 'Beginner' },
  ];

  return (
    <div className="space-y-12 pb-24">
      {/* 7-Channel Communication Bar */}
      <div className="flex justify-center -mt-6">
        <div className="bg-slate-950/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-2 flex gap-4 shadow-2xl">
          {channels.map(ch => (
            <div key={ch.id} className="flex flex-col items-center gap-1 group cursor-pointer hover:bg-slate-900 p-2 rounded-xl transition-all">
              <div className="text-slate-500 group-hover:text-aura transition-colors">{ch.icon}</div>
              <span className="text-[8px] font-black uppercase text-slate-600 group-hover:text-slate-400">{ch.label}</span>
            </div>
          ))}
        </div>
      </div>

      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-aura">Garden of Curiosity</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Nurture your intellect. <span className="text-white">{user?.displayName}</span>, your knowledge gardens are bloom-synchronized with <span className="text-vital">Layer 12 adaptivity</span>.
          </p>
        </div>
        <RealmSelector />
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-4 gap-6">
        {gardens.map((garden) => (
          <Card key={garden.name} className="group hover:border-aura/50 transition-all cursor-pointer overflow-hidden flex flex-col h-full">
             <div className="flex justify-between items-start mb-6">
                <div className="p-4 rounded-2xl bg-slate-800/50 text-vital group-hover:scale-110 transition-transform border border-slate-800">
                   <Book size={28} />
                </div>
                <div className="flex gap-1 bg-slate-900/80 px-2 py-1 rounded-lg">
                   {garden.flowers > 0 ? (
                     Array.from({ length: garden.flowers }).map((_, i) => (
                       <Flower2 key={i} size={14} className="text-vital animate-pulse" />
                     ))
                   ) : (
                     <div className="w-14 h-3.5 bg-slate-800 rounded-full animate-pulse" />
                   )}
                </div>
             </div>

             <h3 className="text-xl font-black mb-1 text-white">{garden.name}</h3>
             <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-6">{garden.level}</p>

             <div className="space-y-2 mt-auto">
                <div className="flex justify-between text-[10px] font-black uppercase text-slate-500">
                   <span>Synergy</span>
                   <span>{garden.progress}%</span>
                </div>
                <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                   <motion.div
                     initial={{ width: 0 }}
                     animate={{ width: `${garden.progress}%` }}
                     className="h-full bg-vital shadow-[0_0_10px_rgba(255,82,82,0.5)]"
                   />
                </div>
             </div>
          </Card>
        ))}
      </section>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8">
         <div className="@[440px]:col-span-2 space-y-8">
            <Card className="p-10 bg-aura/5 border-aura/20 overflow-hidden relative">
               <div className="absolute -bottom-10 -right-10 opacity-5 rotate-12">
                  <Activity size={300} className="text-aura" />
               </div>
               <h4 className="text-2xl font-black mb-6 flex items-center gap-3">
                  <Compass size={32} className="text-aura" />
                  Peer Discovery Mesh
               </h4>
               <p className="text-lg text-slate-400 font-bold mb-10 max-w-xl leading-relaxed">
                  The Mycelial layer has identified a cluster of 8 learners exploring 'TIES-Merging Architecture'. Synergy potential: <span className="text-aura">92%</span>.
               </p>
               <div className="flex items-center gap-6">
                  <div className="flex -space-x-4">
                     {[1, 2, 3, 4].map(i => (
                       <div key={i} className="w-14 h-14 rounded-full bg-slate-800 border-4 border-sovereign flex items-center justify-center font-black text-sm text-aura shadow-xl">
                          S{i}
                       </div>
                     ))}
                  </div>
                  <button type="button" onClick={() => notImplemented('Join Sync Session')} className="px-8 py-3 bg-white text-sovereign font-black rounded-xl text-xs uppercase tracking-widest hover:scale-105 transition-all">Join Sync Session</button>
               </div>
            </Card>
         </div>

         <Card className="bg-vital/5 border-vital/20 py-12 flex flex-col items-center text-center">
            <div className="w-20 h-20 rounded-full bg-vital/10 text-vital flex items-center justify-center mb-8 border border-vital/20 animate-pulse-slow">
               <Star size={40} />
            </div>
            <h4 className="text-xl font-black mb-4">Mastery Progression</h4>
            <p className="text-sm text-slate-500 font-bold mb-10 px-6">
               Neural sensors confirm mastery of 'Phase 1 Recombination'. Your garden has bloomed with a new <span className="text-vital">Sovereign Flower</span>.
            </p>
            <div className="px-6 py-2 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-black text-slate-400 uppercase tracking-widest">
               Rank: Guardian Initiate
            </div>
         </Card>
      </div>
    </div>
  );
};
