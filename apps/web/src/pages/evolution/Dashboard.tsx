import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Rocket, Zap, History, Globe, Accessibility, Layers, Target, ShieldCheck, TrendingUp } from 'lucide-react';
import { ABTestingPanel } from './ABTesting';

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

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6">
        <MetricCard label="Proposals Generated" value={metrics.proposals_generated} icon={Zap} />
        <MetricCard label="Autonomous Deploys" value={metrics.autonomous_deploys} icon={Rocket} />
        <MetricCard label="Accessibility Fidelity" value="99.9%" icon={Accessibility} />
        <MetricCard label="PQC Enforcement" value="100%" icon={ShieldCheck} />
        <MetricCard label="Velocity" value={metrics.implementation_velocity} icon={History} />
        <MetricCard label="Impact Score" value={metrics.user_impact_score} icon={Globe} />
      </div>

      <div className="space-y-12">
        <ABTestingPanel />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
               <Target size={20} className="text-highlight" />
               Autonomous Trajectory
            </h3>
            <div className="h-80 bg-sovereign rounded-2xl border border-slate-800 flex flex-col items-center justify-center italic text-slate-700 p-10 text-center">
              <div className="w-16 h-16 rounded-full border-4 border-aura/10 border-t-aura animate-spin mb-6"></div>
              <p className="text-sm font-bold uppercase tracking-widest text-slate-500">Synthesizing Future Mind-States...</p>
              <p className="text-[10px] text-slate-600 mt-2 max-w-xs">Integrating A/B test deltas and accessibility fidelity into the L1 Evolution Graph.</p>
            </div>
          </div>
          <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
               <TrendingUp size={20} className="text-vital" />
               Historical Impact Delays
            </h3>
            <div className="space-y-4">
              <ABTestResult label="Smart Sidebar Order" variantA="Static" variantB="Predictive" winner="Predictive (+18% CTR)" />
              <ABTestResult label="PQC Status Badge" variantA="Text Only" variantB="Iconic" winner="Iconic (+5% engagement)" />
              <ABTestResult label="Onboarding Flow" variantA="Sequential" variantB="Adaptive" winner="Adaptive (+32% completion)" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ABTestResult = ({ label, variantA, variantB, winner }: any) => (
  <div className="p-4 rounded-xl bg-slate-800/30 border border-slate-700/50">
    <div className="flex justify-between items-center mb-2">
      <span className="text-xs font-bold text-slate-400">{label}</span>
      <span className="text-[10px] font-black px-2 py-0.5 rounded bg-aura/20 text-aura uppercase tracking-widest">Complete</span>
    </div>
    <div className="grid grid-cols-2 gap-4 text-[10px] font-bold uppercase tracking-wider mb-2 text-slate-500">
      <div>A: {variantA}</div>
      <div>B: {variantB}</div>
    </div>
    <div className="text-xs font-bold text-highlight">{winner}</div>
  </div>
);

const MetricCard = ({ label, value, icon: Icon }: any) => (
  <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
    <Icon size={20} className="text-aura mb-4" />
    <div className="text-2xl font-black">{value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
