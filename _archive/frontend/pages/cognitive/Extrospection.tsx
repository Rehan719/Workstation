import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Globe, Search, ArrowUpRight, TrendingUp } from 'lucide-react';

export const Extrospection: React.FC = () => {
  const [signals, setSignals] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v190/extrospection/signals').then(res => setSignals(res.data));
  }, []);

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">World Mind</h1>
        <p className="text-slate-500">Synthesized global signals and research trends via active extrospection engines.</p>
      </header>

      <div className="relative max-w-2xl">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Direct extrospection query..."
          className="w-full bg-slate-900 border border-slate-700 rounded-2xl py-4 pl-12 pr-6 text-lg focus:outline-none focus:border-aura transition-all"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Globe size={20} className="text-aura" />
            Global Signal Feed
          </h3>
          <div className="space-y-4">
            {signals.map(s => (
              <div key={s.id} className="p-5 rounded-2xl bg-slate-800/30 border border-slate-700/50 hover:border-aura transition-all cursor-pointer group">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-700">
                    {s.source}
                  </span>
                  <ArrowUpRight size={14} className="text-slate-600 group-hover:text-aura transition-colors" />
                </div>
                <p className="font-bold text-sm mb-2">{s.title}</p>
                <div className="flex items-center gap-2">
                  <progress value={s.relevance} max={1} aria-label={`Relevance ${(s.relevance * 100).toFixed(0)}%`}
                    className="flex-1 h-1 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
                  <span className="text-[10px] font-black text-slate-500">Relevance: {(s.relevance * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 flex flex-col">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <TrendingUp size={20} className="text-highlight" />
            Emergent Patterns
          </h3>
          <div className="flex-1 flex items-center justify-center italic text-slate-600">
            [Pattern Resonance Visualization]
          </div>
        </div>
      </div>
    </div>
  );
};
