import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { GitBranch, History, Layers, Zap } from 'lucide-react';
import fallbackData from '../../data/fallbackData.json';

export const Evolution: React.FC = () => {
  const [data, setData] = useState<any>(fallbackData.evolution);

  useEffect(() => {
    axios.get('/api/v190/evolution/trajectories')
      .then(res => setData(res.data))
      .catch(() => console.warn("Using fallback evolution data."));
  }, []);

  if (!data) return <div className="p-8 text-slate-500 animate-pulse">Mapping Evolution...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Mind Forge</h1>
        <p className="text-slate-500">Visualization of the Workstation's learning trajectories and recursive self-evolution.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard label="Evolutionary Step" value={data.evolutionary_step} icon={Zap} />
        <StatCard label="Graph Depth" value="1.42M" icon={Layers} />
        <StatCard label="Active Operons" value={data.active_operons} icon={GitBranch} />
        <StatCard label="Mutation Rate" value="0.04%" icon={History} />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8">Recursive Self-Improvement Log</h3>
        <div className="space-y-4">
          {data.recent_mutations.map((m: string, i: number) => (
            <div key={i} className="flex gap-4 p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
               <div className="w-10 h-10 rounded-xl bg-vital/20 text-vital flex items-center justify-center flex-shrink-0">
                 <ShieldCheck size={20} />
               </div>
               <div>
                 <p className="font-bold">{m}</p>
                 <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest mt-1">Successfully Converged • Floor 20 Compliant</p>
               </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon }: any) => (
  <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
    <div className="flex justify-between items-start mb-4">
      <div className="p-2 bg-slate-800 rounded-lg text-aura">
        <Icon size={18} />
      </div>
    </div>
    <div className="text-2xl font-black">{value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);

const ShieldCheck = ({ size }: any) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>
  </svg>
);
