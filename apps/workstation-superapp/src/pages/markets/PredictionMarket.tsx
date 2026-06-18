import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Target, TrendingUp, BarChart3, ChevronRight, Activity, Users, ShieldCheck, DollarSign } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from '@workstation/ui';

const SEED_MARKETS = [
  { id: 'm1', title: 'Will the Workstation reach 1,000 active users by Q4 2026?', probability: 0.74, volume: 48200, ends_at: '2026-12-31' },
  { id: 'm2', title: 'Will sovereign AI surpass 95% constitutional compliance this epoch?', probability: 0.91, volume: 32100, ends_at: '2026-09-30' },
  { id: 'm3', title: 'Will the Federation Network exceed 50 registered nodes?', probability: 0.62, volume: 19800, ends_at: '2026-10-15' },
  { id: 'm4', title: 'Will WST token velocity increase by 3× vs previous epoch?', probability: 0.45, volume: 27600, ends_at: '2026-11-01' },
];

export const PredictionMarket: React.FC = () => {
  const [markets, setMarkets] = useState<any[]>(SEED_MARKETS);
  const [stakes, setStakes] = useState<Record<string, 'YES' | 'NO'>>({});

  useEffect(() => {
    axios.get('/api/v1/intelligence/forecasts', { validateStatus: () => true })
      .catch(() => {});
    // Seeds already set; live markets endpoint can be added when backend supports it
  }, []);

  const handleStake = (id: string, side: 'YES' | 'NO') => {
    setStakes(prev => ({ ...prev, [id]: side }));
    toast(`Stake placed: ${side} on market ${id}`);
  };

  return (
    <div className="space-y-12">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black mb-1 break-words">Wisdom Hub</h1>
          <p className="text-highlight font-bold uppercase text-[10px] tracking-widest">Civilizational Prediction Markets v152.0</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <div className="px-6 py-3 bg-highlight/10 border border-highlight/30 rounded-xl flex items-center gap-3">
              <TrendingUp size={18} className="text-highlight" />
              <span className="text-xs font-black text-highlight uppercase tracking-widest">Crowd Signal: Bullish</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-8">
        {markets.map(m => (
          <div key={m.id} className="p-8 glass-card border-white/5 hover:border-highlight/30 transition-all flex flex-col gap-6">
             <div className="flex justify-between items-start">
                <div className="p-4 bg-surface rounded-2xl text-highlight">
                   <Target size={24} />
                </div>
                <div className="text-right">
                   <p className="text-[10px] font-black text-slate-500 uppercase">Current Probability</p>
                   <p className="text-3xl font-black text-white">{(m.probability * 100).toFixed(0)}%</p>
                </div>
             </div>

             <h3 className="text-xl font-bold leading-relaxed">{m.title}</h3>

             <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-black uppercase tracking-widest">
                   <span className="text-highlight">YES: {(m.probability * 100).toFixed(0)}%</span>
                   <span className="text-slate-600">NO: {((1 - m.probability) * 100).toFixed(0)}%</span>
                </div>
                <progress value={m.probability} max={1} aria-label={`YES probability ${(m.probability * 100).toFixed(0)}%`}
                  className="w-full h-2 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-highlight [&::-moz-progress-bar]:bg-highlight" />
             </div>

             <div className="grid grid-cols-2 gap-4">
                <button type="button"
                  onClick={() => handleStake(m.id, 'YES')}
                  className={`py-4 font-black rounded-xl transition-all uppercase tracking-widest text-xs ${stakes[m.id] === 'YES' ? 'bg-highlight text-sovereign ring-2 ring-highlight/50' : 'bg-highlight/20 text-highlight border border-highlight/30 hover:bg-highlight hover:text-sovereign'}`}>
                  {stakes[m.id] === 'YES' ? '✓ Staked YES' : 'Buy YES'}
                </button>
                <button type="button"
                  onClick={() => handleStake(m.id, 'NO')}
                  className={`py-4 font-black rounded-xl transition-all uppercase tracking-widest text-xs ${stakes[m.id] === 'NO' ? 'bg-slate-600 text-white ring-2 ring-slate-500/50' : 'bg-white/5 border border-white/10 text-white hover:bg-white/10'}`}>
                  {stakes[m.id] === 'NO' ? '✓ Staked NO' : 'Buy NO'}
                </button>
             </div>

             <div className="flex justify-between items-center pt-4 border-t border-white/5">
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Volume: {m.volume.toLocaleString()} WST</p>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Resolution: {new Date(m.ends_at).toLocaleDateString()}</p>
             </div>
          </div>
        ))}
      </div>
    </div>
  );
};
