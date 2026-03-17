import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Rocket, Zap, History, Globe } from 'lucide-react';

export const EvolutionDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v240/evolution/metrics').then(res => setMetrics(res.data));
  }, []);

  if (!metrics) return <div className="p-8 text-slate-500 animate-pulse">Synchronizing Evolution Data...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Continuous Evolution Dashboard</h1>
        <p className="text-slate-500">Real-time metrics on how the Workstation platform is evolving autonomously.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard label="Proposals Generated" value={metrics.proposals_generated} icon={Zap} />
        <MetricCard label="Autonomous Deploys" value={metrics.autonomous_deploys} icon={Rocket} />
        <MetricCard label="Velocity" value={metrics.implementation_velocity} icon={History} />
        <MetricCard label="Impact Score" value={metrics.user_impact_score} icon={Globe} />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
         <h3 className="text-xl font-bold mb-6">Autonomous Trajectory</h3>
         <div className="h-64 bg-sovereign rounded-2xl border border-slate-800 flex items-center justify-center italic text-slate-700">
           Real-time Evolution Graph Integration...
         </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, icon: Icon }: any) => (
  <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
    <Icon size={20} className="text-aura mb-4" />
    <div className="text-2xl font-black">{value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
