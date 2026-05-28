import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layers, Activity, TrendingUp, CheckCircle2 } from 'lucide-react';

export const ABTestingPanel: React.FC = () => {
  const [tests, setTests] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v260/ab-tests').then(res => setTests(res.data));
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
                {test.variants.map((v: string) => (
                   <div key={v} className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-slate-700/50 group">
                      <span className="text-xs font-bold capitalize">{v}</span>
                      <div className="flex items-center gap-3">
                         <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-aura" style={{ width: `${Math.random() * 100}%` }}></div>
                         </div>
                         <span className="text-[10px] font-bold text-slate-500">{(Math.random() * 100).toFixed(0)}%</span>
                      </div>
                   </div>
                ))}
             </div>

             <div className="mt-6 pt-6 border-t border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2 text-highlight">
                   <TrendingUp size={14} />
                   <span className="text-[10px] font-black uppercase tracking-widest">Confidence: 94%</span>
                </div>
                <button className="text-[10px] font-black uppercase text-aura hover:underline">View Analytics</button>
             </div>
          </div>
        ))}
      </div>
    </div>
  );
};
