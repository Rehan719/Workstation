import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layers, Activity, TrendingUp, CheckCircle2 } from 'lucide-react';
import { notImplemented } from '@workstation/ui';

const SEED_TESTS = [
  { test_id: 'reactor-prompt-v2', active: true,  variants: ['control', 'variant-A', 'variant-B'], scores: [42, 67, 81] },
  { test_id: 'incubator-fitness', active: true,  variants: ['baseline', 'enhanced'],              scores: [55, 78] },
  { test_id: 'ceo-tone-tuning',   active: false, variants: ['formal', 'conversational'],          scores: [88, 93] },
  { test_id: 'genome-mutation-v3',active: true,  variants: ['conservative', 'aggressive'],        scores: [61, 74] },
];

export const ABTestingPanel: React.FC = () => {
  const [tests, setTests] = useState<any[]>(SEED_TESTS);

  useEffect(() => {
    axios.get('/api/v1/projects/', { validateStatus: () => true })
      .catch(() => {});
    // Live A/B endpoint can be wired when backend exposes it
  }, []);

  return (
    <div className="space-y-8">
      <h3 className="text-xl font-bold flex items-center gap-2">
        <Layers size={20} className="text-aura" />
        Active A/B Experiments
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {tests.map(test => (
          <div key={test.test_id} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-xl">
             <div className="flex justify-between items-start mb-6">
                <div>
                   <h4 className="font-bold text-sm uppercase tracking-widest text-slate-400">{test.test_id.replace('-', ' ')}</h4>
                   <p className="text-[10px] text-slate-500 mt-1">Status: {test.active ? 'Running' : 'Complete'}</p>
                </div>
                <div className="p-2 bg-aura/10 rounded-lg text-aura">
                   <Activity size={16} />
                </div>
             </div>

             <div className="space-y-4">
                {test.variants.map((v: string, vi: number) => {
                   const score = test.scores?.[vi] ?? 50;
                   return (
                   <div key={v} className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-slate-700/50 group">
                      <span className="text-xs font-bold capitalize">{v}</span>
                      <div className="flex items-center gap-3">
                         <progress value={score} max={100} aria-label={`${v} score ${score}%`}
                            className="w-24 h-1.5 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
                         <span className="text-[10px] font-bold text-slate-500 w-8 text-right">{score}%</span>
                      </div>
                   </div>
                   );
                })}
             </div>

             <div className="mt-6 pt-6 border-t border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2 text-highlight">
                   <TrendingUp size={14} />
                   <span className="text-[10px] font-black uppercase tracking-widest">Confidence: 94%</span>
                </div>
                <button type="button" onClick={() => notImplemented('View Analytics')} className="text-[10px] font-black uppercase text-aura hover:underline">View Analytics</button>
             </div>
          </div>
        ))}
      </div>
    </div>
  );
};
