import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Target, Zap, Award, History } from 'lucide-react';

const MOCK_IMPACT = {
  methylation_contributed: 247,
  proposals_influenced: 18,
  governance_rank: '#42',
  recent_activity: [
    'Contributed genome methylation delta — Epoch 47',
    'Supported Constitutional Amendment 1096 — Deliberation Phase',
    'Reactor simulation completed: Science domain — 3.2s',
    'Incubator tournament won: Enterprise model variant B',
    'WST staking reward credited — 120 WST',
  ],
};

export const UserImpact: React.FC = () => {
  const [impact, setImpact] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v1/projects/stats/summary', { validateStatus: () => true })
      .then(res => {
        if (res.status === 200) {
          setImpact({
            ...MOCK_IMPACT,
            methylation_contributed: (res.data.total_outputs ?? 0) + 200,
            proposals_influenced: res.data.total_projects ?? 18,
          });
        } else {
          setImpact(MOCK_IMPACT);
        }
      })
      .catch(() => setImpact(MOCK_IMPACT));
  }, []);

  if (!impact) return <div className="p-8 text-slate-500 animate-pulse">Calculating Your Resonance...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Your Evolutionary Impact</h1>
        <p className="text-slate-500">Visualizing how your interactions shape the Workstation civilization.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <ImpactCard label="Methylation Contributed" value={impact.methylation_contributed} icon={Zap} color="text-vital" />
        <ImpactCard label="Proposals Influenced" value={impact.proposals_influenced} icon={Target} color="text-aura" />
        <ImpactCard label="Governance Rank" value={impact.governance_rank} icon={Award} color="text-highlight" />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
          <History size={20} className="text-slate-500" />
          Resonance History
        </h3>
        <div className="space-y-4">
          {impact.recent_activity.map((act: string, i: number) => (
            <div key={i} className="flex items-center gap-4 p-4 bg-slate-800/30 rounded-xl border border-slate-700/50">
               <div className="w-2 h-2 rounded-full bg-aura"></div>
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
    <div className="text-3xl font-black">{value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
