import React from 'react';
import { Gauge, Zap, Globe, Activity } from 'lucide-react';

export const FedPerformance: React.FC = () => {
  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-black mb-2">Federation Performance</h1>
        <p className="text-slate-500">Real-time health and throughput metrics for the global Workstation network (1,000+ Nodes).</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <PerfCard label="Total Nodes" value="1,024" icon={Globe} color="text-aura" />
        <PerfCard label="Avg Latency" value="142ms" icon={Zap} color="text-highlight" />
        <PerfCard label="Treaty Velocity" value="42/min" icon={Activity} color="text-vital" />
        <PerfCard label="Ecosystem Uptime" value="99.99%" icon={Gauge} color="text-emerald-400" />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex flex-col items-center justify-center text-center">
         <div className="w-32 h-32 rounded-full border-8 border-aura/20 border-t-aura animate-spin-slow mb-8"></div>
         <h3 className="text-xl font-bold mb-2">Global Gossipsub Convergence</h3>
         <p className="text-slate-500 max-w-sm">Visualizing real-time propagation of cytokine signals across 1,024 federated nodes.</p>
      </div>
    </div>
  );
};

const PerfCard = ({ label, value, icon: Icon, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <Icon size={24} className={`${color} mb-4`} />
    <div className="text-3xl font-black">{value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
