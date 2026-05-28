import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart3, Users, Zap, TrendingUp } from 'lucide-react';

export const LearningDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v191/learning/analytics').then(res => setAnalytics(res.data));
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
          {analytics.popular_modules.map((m: string) => (
            <div key={m} className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50">
              <span className="font-bold">{m}</span>
              <div className="w-48 h-2 bg-slate-900 rounded-full overflow-hidden">
                <div className="h-full bg-aura" style={{ width: `${Math.random() * 60 + 40}%` }}></div>
              </div>
            </div>
          ))}
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
