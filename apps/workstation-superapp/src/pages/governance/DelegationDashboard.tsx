import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Cpu, ShieldCheck, ChevronRight, Activity, TrendingUp, AlertCircle, Play, UserCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const DelegationDashboard: React.FC = () => {
  const [delegations, setDelegations] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v320/governance/autonomous/delegations').then(res => setDelegations(res.data));
    axios.get('/api/v320/governance/autonomous/performance').then(res => setStats(res.data));
  }, []);

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-1">Autonomous Governance</h1>
          <p className="font-bold uppercase text-[10px] tracking-widest text-aura">AI Executor Delegation v152.0</p>
        </div>
        {stats && (
           <div className="flex gap-4">
              <div className="px-6 py-3 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-3">
                 <UserCheck size={18} className="text-aura" />
                 <span className="text-xs font-black text-aura uppercase tracking-widest">{stats.human_satisfaction_rate * 100}% Satisfaction</span>
              </div>
           </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         {stats && (
           <>
             <StatCard title="Decisions Processed" value={stats.decisions_processed.toLocaleString()} icon={Cpu} color="text-aura" />
             <StatCard title="Efficiency Gain" value={stats.efficiency_gain} icon={TrendingUp} color="text-vital" />
             <StatCard title="Active Overrides" value={stats.active_overrides} icon={AlertCircle} color="text-highlight" />
           </>
         )}
      </div>

      <div className="space-y-8">
         <h3 className="text-2xl font-black flex items-center gap-3">
            <ShieldCheck size={24} className="text-aura" />
            Active AI Authorities
         </h3>

         <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {delegations.map(del => (
              <div key={del.id} className="p-8 glass-card border-white/5 hover:border-aura/30 transition-all flex flex-col">
                 <div className="flex justify-between items-start mb-6">
                    <div className="p-4 bg-surface rounded-2xl text-aura">
                       <Cpu size={24} />
                    </div>
                    <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-aura/10 text-aura border border-aura/20 uppercase tracking-widest">
                       {del.status}
                    </span>
                 </div>
                 <h4 className="text-xl font-bold mb-1">{del.ai_executor}</h4>
                 <p className="text-xs text-slate-500 font-black uppercase tracking-widest mb-6">Domain: {del.category}</p>

                 <div className="p-6 bg-sovereign rounded-2xl border border-white/5 space-y-4 mb-8">
                    <div className="flex justify-between items-center">
                       <span className="text-[10px] font-bold text-slate-500 uppercase">Resonance Threshold</span>
                       <span className="text-sm font-black">{del.threshold.toLocaleString()} WST</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                       <div className="h-full w-full bg-aura"></div>
                    </div>
                 </div>

                 <button className="w-full py-4 bg-white/5 border border-white/10 rounded-xl font-bold text-xs uppercase tracking-widest hover:border-aura hover:text-aura transition-all mt-auto flex items-center justify-center gap-2">
                    <Play size={14} />
                    Audit Decision Log
                 </button>
              </div>
            ))}
         </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon: Icon, color }: any) => (
  <div className="p-8 glass-card border-white/5">
    <div className={`p-4 rounded-2xl bg-surface mb-6 ${color} w-fit`}>
       <Icon size={24} />
    </div>
    <p className="text-3xl font-black mb-1">{value}</p>
    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{title}</p>
  </div>
);
