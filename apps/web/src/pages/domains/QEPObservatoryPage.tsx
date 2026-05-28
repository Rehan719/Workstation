import React, { useState } from 'react';
import { Microscope, Layers, BookOpen, BrainCircuit, Activity, ChevronRight, HelpCircle } from 'lucide-react';

export const SovereignXAIObservatory: React.FC = () => {
  const [selectedExplanations, setSelectedExplanations] = useState<string | null>(null);

  const modelMetrics = [
    { name: 'Source Quality', precision: 0.98, recall: 0.96, f1: 0.97, status: 'Healthy', color: 'bg-emerald-500' },
    { name: 'Theological Consistency', precision: 0.99, recall: 0.99, f1: 0.99, status: 'Healthy', color: 'bg-indigo-500' },
    { name: 'Concept Relationship', precision: 0.94, recall: 0.92, f1: 0.93, status: 'Fair', color: 'bg-amber-500' },
    { name: 'Adaptive Learning', precision: 0.88, recall: 0.86, f1: 0.87, status: 'Active', color: 'bg-blue-500' }
  ];

  const recentExplanations = [
    { id: 'EXPL-01', model: 'Source Quality', decision: 'Approve Source', method: 'SHAP', timestamp: '2 mins ago' },
    { id: 'EXPL-02', model: 'Personalization', decision: 'Recommend Lesson 5', method: 'LIME', timestamp: '15 mins ago' },
    { id: 'EXPL-03', model: 'Consistency', decision: 'Pass Theological Audit', method: 'Counterfactual', timestamp: '1 hour ago' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <Microscope className="w-8 h-8 text-indigo-600" />
          Sovereign XAI Observatory
        </h2>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1 text-[10px] font-black text-slate-500 uppercase">
             <Activity className="w-4 h-4 text-emerald-500" />
             System Status: Healthy
          </div>
          <div className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full uppercase">
            QEP v8.5 Signature Product
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {modelMetrics.map((metric) => (
          <div key={metric.name} className="p-5 bg-white border-2 border-slate-100 rounded-2xl hover:border-indigo-200 transition-colors shadow-sm">
             <div className="flex justify-between items-start mb-3">
               <div className="text-xs font-black text-slate-400 uppercase tracking-widest">{metric.name}</div>
               <div className={`w-2 h-2 rounded-full ${metric.color}`}></div>
             </div>
             <div className="text-2xl font-black text-slate-800">F1: {(metric.f1 * 100).toFixed(0)}%</div>
             <div className="grid grid-cols-2 gap-2 mt-3">
                <div className="text-[10px] font-bold text-slate-400 uppercase">P: {metric.precision}</div>
                <div className="text-[10px] font-bold text-slate-400 uppercase">R: {metric.recall}</div>
             </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-8 bg-slate-900 rounded-3xl border-2 border-slate-800 relative overflow-hidden">
          <div className="relative z-10 space-y-6">
            <div className="flex items-center gap-2 text-indigo-400 mb-2">
              <BrainCircuit className="w-6 h-6" />
              <h3 className="text-sm font-black uppercase tracking-widest text-white">Interactive Decision Explainer</h3>
            </div>

            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700 space-y-4">
               <div className="flex justify-between items-center">
                  <div className="text-xs font-black text-indigo-400 uppercase">Feature Importance (SHAP)</div>
                  <HelpCircle className="w-4 h-4 text-slate-600" />
               </div>
               <div className="space-y-3">
                  {[
                    { feature: 'Theological Authenticity', weight: 0.85, color: 'bg-emerald-400' },
                    { feature: 'Citation Count', weight: 0.65, color: 'bg-blue-400' },
                    { feature: 'Sanad Verification', weight: 0.92, color: 'bg-indigo-400' },
                    { feature: 'Community Reputation', weight: 0.45, color: 'bg-amber-400' }
                  ].map((f) => (
                    <div key={f.feature} className="space-y-1">
                       <div className="flex justify-between text-[10px] font-bold uppercase text-slate-400">
                         <span>{f.feature}</span>
                         <span className="text-white">{(f.weight * 100).toFixed(0)}%</span>
                       </div>
                       <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                          <div className={`h-full ${f.color}`} style={{ width: `${f.weight * 100}%` }}></div>
                       </div>
                    </div>
                  ))}
               </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
               <div className="p-5 bg-indigo-900/30 rounded-xl border border-indigo-500/20 space-y-2">
                  <div className="text-[10px] font-black text-indigo-300 uppercase flex items-center gap-1">
                    <Layers className="w-3 h-3" /> Counterfactual Analysis
                  </div>
                  <p className="text-xs text-indigo-100 font-medium leading-relaxed">
                    "If Sanad Verification was below 0.8, the Source Quality prediction would have changed from 'Approve' to 'Pending'."
                  </p>
               </div>
               <div className="p-5 bg-emerald-900/30 rounded-xl border border-emerald-500/20 space-y-2">
                  <div className="text-[10px] font-black text-emerald-300 uppercase flex items-center gap-1">
                    <BookOpen className="w-3 h-3" /> Theological Context
                  </div>
                  <p className="text-xs text-emerald-100 font-medium leading-relaxed">
                    "This decision aligns with the 1127 Constitutional Articles regarding source integrity and scholarly consensus."
                  </p>
               </div>
            </div>
          </div>
          <div className="absolute top-[-20px] right-[-20px] w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl"></div>
        </div>

        <div className="p-6 bg-white border-2 border-slate-100 rounded-2xl shadow-sm">
          <h3 className="text-xs font-black text-slate-800 uppercase mb-4 tracking-widest border-b border-slate-100 pb-2 flex items-center gap-2">
             Recent Explanations
          </h3>
          <div className="space-y-3">
             {recentExplanations.map((expl) => (
               <div
                 key={expl.id}
                 className="p-3 bg-slate-50 border border-slate-200 rounded-lg hover:border-indigo-400 hover:bg-white transition-all group cursor-pointer"
                 onClick={() => setSelectedExplanations(expl.id)}
               >
                  <div className="flex justify-between items-start mb-1">
                    <div className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">{expl.id} • {expl.method}</div>
                    <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 transition-colors" />
                  </div>
                  <div className="text-xs font-black text-slate-800 group-hover:text-indigo-600">{expl.model}</div>
                  <div className="text-[10px] font-bold text-slate-500 uppercase mt-1">{expl.decision} • {expl.timestamp}</div>
               </div>
             ))}
          </div>
          <button className="w-full mt-4 py-2 border-2 border-dashed border-slate-200 rounded-lg text-[10px] font-black text-slate-400 uppercase hover:border-indigo-400 hover:text-indigo-600 transition-all">
            View All Explanations
          </button>
        </div>
      </div>
    </div>
  );
};
