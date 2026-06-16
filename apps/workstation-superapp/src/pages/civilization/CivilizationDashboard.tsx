import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Globe, TrendingUp, Cpu, ShieldCheck, Activity, Zap, Users, ArrowUpRight } from 'lucide-react';
import { motion } from 'framer-motion';

export const CivilizationDashboard: React.FC = () => {
  const [insights, setInsights] = useState<any[]>([]);
  const [forecasts, setForecasts] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v320/intelligence/insights').then(res => setInsights(res.data));
    axios.get('/api/v320/intelligence/forecasts').then(res => setForecasts(res.data));
  }, []);

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1 neon-text !text-aura">Civilization Brain</h1>
          <p className="text-slate-500 font-bold text-lg mt-2">Real-time planetary intelligence and collective decision mapping.</p>
        </div>
        <div className="flex gap-4">
           <div className="px-6 py-3 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-3 shadow-[0_0_20px_rgba(100,255,218,0.1)]">
              <Activity size={18} className="text-aura animate-pulse" />
              <span className="text-xs font-black text-aura uppercase tracking-widest">Co-Conscious Mode Active</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
         <StatCard label="WST Liquidity" value={forecasts?.wst_liquidity.projection} delta="+12%" icon={Zap} color="text-aura" />
         <StatCard label="Voter Participation" value={forecasts?.voter_turnout.current} delta="+8%" icon={Users} color="text-vital" />
         <StatCard label="Autonomous Decisions" value="1,420" delta="100% Valid" icon={Cpu} color="text-highlight" />
         <StatCard label="System Integrity" value="99.98%" delta="Optimal" icon={ShieldCheck} color="text-aura" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2 space-y-8">
           <h3 className="text-2xl font-black flex items-center gap-3">
              <Zap size={24} className="text-aura" />
              Collective Insights
           </h3>
           <div className="space-y-6">
              {insights.map(i => (
                <div key={i.id} className="p-10 glass-card bg-aura/5 border-aura/20 group hover:bg-aura/10 transition-all">
                   <div className="flex justify-between items-start mb-6">
                      <div className="p-4 bg-surface rounded-2xl text-aura">
                         <Globe size={32} />
                      </div>
                      <div className="flex items-center gap-2 bg-sovereign px-4 py-2 rounded-full border border-white/5 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                         Confidence: {i.confidence * 100}%
                      </div>
                   </div>
                   <h4 className="text-2xl font-black mb-2">{i.title}</h4>
                   <p className="text-slate-400 font-bold leading-relaxed mb-8">{i.observation}</p>

                   <div className="p-6 bg-sovereign/60 rounded-2xl border border-white/5 space-y-4">
                      <p className="text-[10px] font-black text-aura uppercase tracking-widest">System Recommendation</p>
                      <p className="text-sm font-bold text-white leading-relaxed">{i.recommendation}</p>
                      <button className="flex items-center gap-2 text-xs font-black uppercase text-aura hover:underline">
                         Trigger Strategic Initiative
                         <ArrowUpRight size={14} />
                      </button>
                   </div>
                </div>
              ))}
           </div>
        </div>

        <aside className="space-y-8">
           <section className="p-8 glass-card">
              <h3 className="text-xl font-bold mb-8">Trend Forecasting</h3>
              <div className="space-y-10">
                 {forecasts && Object.entries(forecasts).map(([key, val]: [string, any]) => (
                   <div key={key} className="space-y-3">
                      <div className="flex justify-between items-end">
                         <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{key.replace('_', ' ')}</p>
                         <p className="text-lg font-black text-white">{val.projection}</p>
                      </div>
                      <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                         <div className="h-full w-[70%] bg-aura shadow-[0_0_10px_rgba(100,255,218,0.5)]"></div>
                      </div>
                      <p className="text-[10px] text-slate-500 font-bold italic">{val.driver || val.catalyst || 'Natural Growth'}</p>
                   </div>
                 ))}
              </div>
           </section>

           <section className="p-8 glass-card border-vital/20 bg-vital/5">
              <h3 className="text-xl font-bold mb-6 text-vital flex items-center gap-2">
                 <Activity size={20} />
                 Anomaly Stream
              </h3>
              <div className="space-y-4">
                 {[1, 2].map(x => (
                   <div key={x} className="p-4 bg-sovereign/40 rounded-xl border border-white/5">
                      <p className="text-[10px] text-slate-500 font-black uppercase mb-1">Economic • 8m ago</p>
                      <p className="text-xs font-bold text-slate-300">Micro-transaction spike in Region: Swarm-North.</p>
                   </div>
                 ))}
              </div>
           </section>
        </aside>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color }: any) => (
  <div className="p-8 glass-card">
    <div className={`p-4 rounded-2xl bg-surface mb-6 ${color} w-fit`}>
       <Icon size={24} />
    </div>
    <p className="text-3xl font-black mb-1">{value}</p>
    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
  </div>
);
