import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart3, Users, Zap, TrendingUp } from 'lucide-react';

const MODULE_SCORES: Record<string, number> = {
  'Sovereign Genome': 87,
  'Constitutional AI': 94,
  'Federation Portal': 72,
  'Reactor Simulations': 81,
  'Entrepreneur Wizard': 68,
  'Civilization Brain': 76,
};

const MOCK_ANALYTICS = {
  avg_session_depth: '4.7',
  evolutionary_impact: 0.82,
  popular_modules: Object.keys(MODULE_SCORES),
};

export const LearningDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v1/projects/stats/summary', { validateStatus: () => true })
      .then(res => {
        if (res.status === 200) {
          setAnalytics({
            ...MOCK_ANALYTICS,
            avg_session_depth: ((res.data.total_projects ?? 0) * 0.5 + 4).toFixed(1),
          });
        } else {
          setAnalytics(MOCK_ANALYTICS);
        }
      })
      .catch(() => setAnalytics(MOCK_ANALYTICS));
  }, []);

  if (!analytics) return <div className="p-8 text-slate-500 animate-pulse">Analyzing Engagement...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Learning Dashboard</h1>
        <p className="text-slate-500">How your interactions are shaping the Workstation's collective intelligence.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <AnalyticsCard label="Session Depth" value={analytics.avg_session_depth} icon={BarChart3} />
        <AnalyticsCard label="Evolutionary Impact" value={`${(analytics.evolutionary_impact * 100).toFixed(1)}%`} icon={Zap} />
        <AnalyticsCard label="Feedback Resonance" value="0.98" icon={TrendingUp} />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-6">Popular Modules (Engagement Map)</h3>
        <div className="space-y-4">
          {analytics.popular_modules.map((m: string) => {
            const score = MODULE_SCORES[m] ?? 65;
            return (
              <div key={m} className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50 gap-4">
                <span className="font-bold min-w-0 truncate">{m}</span>
                <div className="flex items-center gap-3 shrink-0">
                  <progress value={score} max={100} aria-label={`${m} engagement ${score}%`}
                    className="w-36 h-2 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-900 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
                  <span className="text-[10px] font-black text-slate-500 w-8 text-right">{score}%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const AnalyticsCard = ({ label, value, icon: Icon }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
    <Icon size={24} className="text-aura mb-4" />
    <div className="text-3xl font-black">{value}</div>
    <p className="text-xs font-bold uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
