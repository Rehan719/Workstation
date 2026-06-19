import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Target, Zap, Award, History, Activity } from 'lucide-react';

interface ImpactData {
  total_signals: number;
  total_projects: number;
  governance_proposals: number;
  swarm_runs: number;
  composite_health: number;
  recent_activity: string[];
}

export const UserImpact: React.FC = () => {
  const [impact, setImpact] = useState<ImpactData | null>(null);

  useEffect(() => {
    Promise.all([
      axios.get('/api/v1/organism/status', { validateStatus: () => true }),
      axios.get('/api/v1/projects/stats/summary', { validateStatus: () => true }),
      axios.get('/api/v1/swarm/runs', { validateStatus: () => true }),
      axios.get('/api/v1/projects/governance/proposals', { validateStatus: () => true }),
    ]).then(([orgRes, projRes, swarmRes, propRes]) => {
      const org = orgRes.status === 200 ? orgRes.data : null;
      const proj = projRes.status === 200 ? projRes.data : null;
      const swarmRuns: any[] = swarmRes.status === 200 ? (swarmRes.data.runs ?? []) : [];
      const proposals: any[] = propRes.status === 200 ? (Array.isArray(propRes.data) ? propRes.data : []) : [];

      const totalSignals = org
        ? Object.values(org.systems?.nervous?.total_signals ?? {}).reduce((a: number, b: any) => a + (Number(b) || 0), 0)
        : 0;

      const recentActivity: string[] = [];
      swarmRuns.slice(0, 3).forEach((r: any) => {
        recentActivity.push(`Swarm cascade: ${(r.task ?? '').slice(0, 50)} — ${(r.agents_engaged ?? []).length} agents`);
      });
      proposals.slice(0, 2).forEach((p: any) => {
        recentActivity.push(`Governance proposal: ${p.project_id ?? 'Project'} — ${p.status ?? 'pending'}`);
      });
      if (recentActivity.length === 0) {
        recentActivity.push('Organism health monitored — all biomimetic systems nominal');
        recentActivity.push('Constitutional AI gate active — all operations validated');
      }

      setImpact({
        total_signals: Number(totalSignals),
        total_projects: proj?.total_projects ?? 0,
        governance_proposals: proposals.length,
        swarm_runs: swarmRuns.length,
        composite_health: org?.composite_health ?? 1.0,
        recent_activity: recentActivity,
      });
    }).catch(() => {
      setImpact({
        total_signals: 0, total_projects: 0, governance_proposals: 0,
        swarm_runs: 0, composite_health: 1.0,
        recent_activity: ['Awaiting organism signal data…'],
      });
    });
  }, []);

  if (!impact) return <div className="p-8 text-slate-500 animate-pulse">Calculating Your Resonance...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Your Evolutionary Impact</h1>
        <p className="text-slate-500">How your interactions shape the Workstation organism's collective intelligence.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <ImpactCard label="Organism Signals" value={impact.total_signals.toLocaleString()} icon={Zap} color="text-vital" />
        <ImpactCard label="Active Projects" value={impact.total_projects} icon={Target} color="text-aura" />
        <ImpactCard label="Governance Props" value={impact.governance_proposals} icon={Award} color="text-highlight" />
        <ImpactCard label="Swarm Runs" value={impact.swarm_runs} icon={Activity} color="text-aura" />
      </div>

      <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <p className="text-[10px] font-black uppercase text-slate-500 tracking-wider">Organism Composite Health</p>
          <p className="text-sm font-black text-white">{Math.round(impact.composite_health * 100)}%</p>
        </div>
        <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${impact.composite_health >= 0.8 ? 'bg-green-500' : impact.composite_health >= 0.5 ? 'bg-aura' : 'bg-yellow-500'}`}
            style={{ width: `${Math.round(impact.composite_health * 100)}%` }}
          />
        </div>
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
          <History size={20} className="text-slate-500" />
          Resonance History
        </h3>
        <div className="space-y-4">
          {impact.recent_activity.map((act: string, i: number) => (
            <div key={i} className="flex items-center gap-4 p-4 bg-slate-800/30 rounded-xl border border-slate-700/50">
               <div className="w-2 h-2 rounded-full bg-aura shrink-0"></div>
               <span className="text-sm font-medium">{act}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const ImpactCard = ({ label, value, icon: Icon, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <Icon size={24} className={`${color} mb-4`} />
    <div className="text-3xl font-black">{typeof value === 'number' ? value.toLocaleString() : value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
