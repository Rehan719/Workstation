import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Globe, TrendingUp, Cpu, ShieldCheck, Activity, Zap, Users, ArrowUpRight, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Insight {
  id: string;
  type: string;
  title: string;
  detail: string;
  score: number;
}

interface ForecastData {
  forecast: string;
  generated_at: number;
  portfolio_size: number;
  valid_until: number;
}

interface StatsData {
  total_projects: number;
  total_outputs: number;
  complete: number;
  cpu_percent: number;
  memory_percent: number;
  swarm_health: number;
}

export const CivilizationDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [insights,  setInsights]  = useState<Insight[]>([]);
  const [forecast,  setForecast]  = useState<ForecastData | null>(null);
  const [stats,     setStats]     = useState<StatsData | null>(null);
  const [loading,   setLoading]   = useState(true);

  useEffect(() => {
    Promise.allSettled([
      axios.get('/api/v1/intelligence/insights'),
      axios.get('/api/v1/intelligence/forecasts'),
      axios.get('/api/v1/projects/stats/summary'),
    ]).then(([insRes, fcRes, stRes]) => {
      if (insRes.status === 'fulfilled') setInsights(insRes.value.data.insights ?? []);
      if (fcRes.status  === 'fulfilled') setForecast(fcRes.value.data);
      if (stRes.status  === 'fulfilled') setStats(stRes.value.data);
    }).finally(() => setLoading(false));
  }, []);

  const swarmPct = stats ? Math.round((stats.swarm_health ?? 0.98) * 100) : 98;

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-aura break-words uppercase tracking-tighter">Civilization Brain</h1>
          <p className="text-slate-500 font-bold text-sm mt-2">Real-time portfolio intelligence and collective decision mapping.</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
          <div className="px-5 py-2.5 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-2">
            <Activity size={14} className="text-aura animate-pulse" />
            <span className="text-[9px] font-black text-aura uppercase tracking-widest">Co-Conscious Mode Active</span>
          </div>
        </div>
      </header>

      {/* Stat cards */}
      <div className="grid grid-cols-2 @[440px]:grid-cols-4 gap-6">
        <StatCard label="Total Projects"   value={stats ? String(stats.total_projects) : '—'} icon={Globe}      color="text-aura" />
        <StatCard label="Deliverables"     value={stats ? String(stats.total_outputs)  : '—'} icon={TrendingUp}  color="text-highlight" />
        <StatCard label="Commercialised"   value={stats ? String(stats.complete)       : '—'} icon={Cpu}         color="text-vital" />
        <StatCard label="Swarm Health"     value={`${swarmPct}%`}                             icon={ShieldCheck} color="text-emerald-400" />
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-10">
        {/* Insights column */}
        <div className="@[440px]:col-span-2 space-y-6">
          <h3 className="text-lg font-black flex items-center gap-3 uppercase tracking-tight">
            <Zap size={18} className="text-aura" /> Collective Insights
          </h3>

          {loading ? (
            <div className="flex items-center gap-3 py-10 text-slate-500">
              <Loader2 size={18} className="animate-spin" />
              <span className="text-xs font-bold uppercase tracking-widest">Loading intelligence…</span>
            </div>
          ) : insights.length === 0 ? (
            <div className="p-8 rounded-2xl bg-slate-900/40 border border-slate-800 text-center">
              <Globe size={28} className="text-slate-700 mx-auto mb-3" />
              <p className="text-xs font-bold text-slate-500">No insights yet — create projects to unlock portfolio intelligence.</p>
              <button type="button" onClick={() => navigate('/projects')}
                className="mt-4 px-4 py-2 bg-aura text-sovereign rounded-xl text-[9px] font-black uppercase tracking-widest hover:opacity-90">
                Go to Projects
              </button>
            </div>
          ) : (
            insights.map((ins, i) => (
              <div key={ins.id} className="p-8 rounded-2xl border border-aura/20 bg-aura/5 hover:bg-aura/10 transition-all">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-slate-900 rounded-xl text-aura">
                      <Globe size={20} />
                    </div>
                    <span className="text-[9px] font-black text-aura uppercase tracking-widest">{ins.type}</span>
                  </div>
                  <div className="px-3 py-1 bg-slate-900 rounded-full border border-slate-800 text-[9px] font-black text-slate-400 uppercase">
                    Score: {(ins.score * 100).toFixed(0)}%
                  </div>
                </div>
                <h4 className="text-lg font-black text-white mb-2">{ins.title}</h4>
                <p className="text-slate-400 text-sm leading-relaxed mb-5">{ins.detail}</p>
                <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 flex items-center justify-between gap-4">
                  <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Navigate to Projects to take action</p>
                  <button type="button" onClick={() => navigate('/projects')}
                    className="flex items-center gap-1.5 text-[9px] font-black uppercase text-aura hover:underline shrink-0">
                    Open Projects <ArrowUpRight size={11} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Sidebar */}
        <aside className="space-y-6">
          {/* Forecast */}
          <section className="p-6 rounded-2xl border border-slate-800 bg-slate-950/40">
            <h3 className="text-sm font-black text-white mb-4 flex items-center gap-2 uppercase tracking-tight">
              <TrendingUp size={14} className="text-aura" /> 90-Day Forecast
            </h3>
            {loading ? (
              <div className="py-6 flex items-center gap-2 text-slate-500">
                <Loader2 size={14} className="animate-spin" />
                <span className="text-[9px] font-bold uppercase">Generating…</span>
              </div>
            ) : forecast ? (
              <div className="space-y-3">
                <pre className="text-[9px] text-slate-400 leading-relaxed whitespace-pre-wrap font-sans">{forecast.forecast}</pre>
                {forecast.valid_until && (
                  <p className="text-[8px] text-slate-600 font-bold">
                    Cached · refreshes {new Date(forecast.valid_until * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                )}
              </div>
            ) : (
              <p className="text-[9px] text-slate-500">Forecast unavailable — check API server.</p>
            )}
          </section>

          {/* Live vitals */}
          <section className="p-6 rounded-2xl border border-slate-800 bg-slate-950/40">
            <h3 className="text-sm font-black text-white mb-4 flex items-center gap-2 uppercase tracking-tight">
              <Activity size={14} className="text-vital" /> System Vitals
            </h3>
            <div className="space-y-4">
              {[
                { label: 'CPU', value: stats?.cpu_percent ?? 0, color: 'text-aura', bar: 'bg-aura' },
                { label: 'Memory', value: stats?.memory_percent ?? 0, color: 'text-highlight', bar: 'bg-highlight' },
              ].map(v => (
                <div key={v.label} className="space-y-1.5">
                  <div className="flex justify-between text-[9px] font-black uppercase tracking-widest">
                    <span className="text-slate-500">{v.label}</span>
                    <span className={v.color}>{stats ? `${v.value.toFixed(1)}%` : '—'}</span>
                  </div>
                  <progress value={v.value} max={100} aria-label={`${v.label} usage`}
                    className={`w-full h-1 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:${v.bar} [&::-moz-progress-bar]:${v.bar}`} />
                </div>
              ))}
            </div>
          </section>

          {/* Project activity */}
          <section className="p-6 rounded-2xl border border-vital/20 bg-vital/5">
            <h3 className="text-sm font-black text-vital mb-4 flex items-center gap-2 uppercase tracking-tight">
              <Activity size={14} /> Portfolio Stream
            </h3>
            <div className="space-y-3">
              {insights.slice(0, 3).map((ins, i) => (
                <div key={ins.id} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                  <p className="text-[9px] text-slate-500 font-black uppercase mb-1">{ins.type}</p>
                  <p className="text-[10px] font-bold text-slate-300 leading-snug">{ins.title}</p>
                </div>
              ))}
              {insights.length === 0 && !loading && (
                <p className="text-[9px] text-slate-600 font-bold">No activity yet.</p>
              )}
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color }: { label: string; value: string; icon: React.ElementType; color: string }) => (
  <div className="p-6 rounded-2xl border border-slate-800 bg-slate-950/40">
    <div className={`p-3 rounded-xl bg-slate-900 mb-4 ${color} w-fit`}>
      <Icon size={18} />
    </div>
    <p className="text-2xl font-black text-white mb-1">{value}</p>
    <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
  </div>
);
