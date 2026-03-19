import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Target, TrendingUp, BarChart3, ChevronRight, Activity, Users, ShieldCheck, DollarSign } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const PredictionMarket: React.FC = () => {
  const [markets, setMarkets] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v320/markets/').then(res => setMarkets(res.data));
  }, []);

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-1">Wisdom Hub</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-highlight">Civilizational Prediction Markets v152.0</p>
        </div>
        <div className="flex gap-4">
           <div className="px-6 py-3 bg-highlight/10 border border-highlight/30 rounded-xl flex items-center gap-3">
              <TrendingUp size={18} className="text-highlight" />
              <span className="text-xs font-black text-highlight uppercase tracking-widest">Crowd Signal: Bullish</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
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
                   <span className="text-highlight">YES: {m.probability * 100}%</span>
                   <span className="text-slate-600">NO: {(1 - m.probability) * 100}%</span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                   <div className="h-full bg-highlight" style={{ width: `${m.probability * 100}%` }}></div>
                </div>
             </div>

             <div className="grid grid-cols-2 gap-4">
                <button className="py-4 bg-highlight text-sovereign font-black rounded-xl hover:scale-[1.02] transition-all uppercase tracking-widest text-xs">Buy YES</button>
                <button className="py-4 bg-white/5 border border-white/10 text-white font-black rounded-xl hover:bg-white/10 transition-all uppercase tracking-widest text-xs">Buy NO</button>
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
