import React, { useState } from 'react';
import { BrainCircuit, Fingerprint, Network, ShieldCheck, Activity, BarChart3, Lock, Cpu } from 'lucide-react';

export const QEPAIPortal: React.FC = () => {
  const [activeModel, setActiveModel] = useState<string | null>('Theological NLP');

  const aiModels = [
    { id: 'NLP-01', name: 'Theological NLP', type: 'Natural Language Processing', status: 'Optimal', performance: '99.2%', color: 'bg-indigo-500' },
    { id: 'CV-01', name: 'Arabic OCR & Sanad', type: 'Computer Vision', status: 'Stable', performance: '96.5%', color: 'bg-emerald-500' },
    { id: 'PRED-01', name: 'Student Success', type: 'Predictive Analytics', status: 'Learning', performance: '92.1%', color: 'bg-amber-500' },
    { id: 'FED-01', name: 'Federated Global', type: 'Federated Learning', status: 'Syncing', performance: '98.8%', color: 'bg-blue-500' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <BrainCircuit className="w-8 h-8 text-indigo-600" />
          Sovereign AI Portal
        </h2>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1 text-[10px] font-black text-slate-500 uppercase">
             <ShieldCheck className="w-4 h-4 text-emerald-500" />
             AI Ethics: Compliant
          </div>
          <div className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase tracking-widest">
            v8.7 Sovereign Signature
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {aiModels.map((model) => (
              <div
                key={model.id}
                className={`p-5 rounded-2xl border-2 transition-all cursor-pointer shadow-sm ${activeModel === model.name ? 'border-indigo-500 bg-indigo-50/30' : 'border-slate-100 bg-white hover:border-indigo-200'}`}
                onClick={() => setActiveModel(model.name)}
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{model.id} • {model.type}</div>
                  <div className={`w-2 h-2 rounded-full ${model.color}`}></div>
                </div>
                <div className="text-xl font-black text-slate-800 uppercase tracking-tighter">{model.name}</div>
                <div className="flex justify-between items-center mt-4">
                  <div className="flex items-center gap-1 text-[10px] font-bold text-slate-500 uppercase">
                    <Activity className="w-3 h-3" /> Status: {model.status}
                  </div>
                  <div className="text-xs font-black text-indigo-600">{model.performance} Accuracy</div>
                </div>
              </div>
            ))}
          </div>

          <div className="p-8 bg-slate-900 rounded-3xl border-2 border-slate-800 relative overflow-hidden">
            <div className="relative z-10 space-y-6">
              <div className="flex items-center gap-2 text-indigo-400 mb-2">
                <Network className="w-6 h-6" />
                <h3 className="text-sm font-black uppercase tracking-widest text-white">Federated Learning Hub</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { realm: 'Forge', status: 'Syncing Updates', epsilon: '0.012' },
                  { realm: 'Genome', status: 'Local Training', epsilon: '0.008' },
                  { realm: 'Learner', status: 'Aggregated', epsilon: '0.015' }
                ].map((realm) => (
                  <div key={realm.realm} className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                    <div className="text-[10px] font-black text-indigo-400 uppercase mb-1">{realm.realm} Realm</div>
                    <div className="text-xs font-bold text-white mb-3">{realm.status}</div>
                    <div className="flex justify-between items-center text-[10px] text-slate-400 font-bold uppercase">
                       <span>ε (Privacy):</span>
                       <span className="text-emerald-400">{realm.epsilon}</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-6 bg-indigo-500/10 rounded-2xl border border-indigo-500/20">
                 <div className="flex items-center gap-2 mb-4">
                    <Lock className="w-4 h-4 text-indigo-400" />
                    <span className="text-xs font-black text-white uppercase tracking-widest">Privacy-Preserving Aggregation</span>
                 </div>
                 <p className="text-xs text-slate-300 font-medium leading-relaxed italic">
                    "Global model updated with weighted Laplacian noise to ensure zero individual student data leak across regional federated nodes."
                 </p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="p-6 bg-white border-2 border-slate-100 rounded-2xl shadow-sm">
            <h3 className="text-xs font-black text-slate-800 uppercase mb-4 tracking-widest border-b border-slate-100 pb-2 flex items-center gap-2">
               <Fingerprint className="w-4 h-4 text-indigo-600" /> Computer Vision Engine
            </h3>
            <div className="aspect-video bg-slate-100 rounded-xl mb-4 flex items-center justify-center border-2 border-dashed border-slate-200">
               <div className="text-center">
                  <Cpu className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <div className="text-[10px] font-black text-slate-400 uppercase">Awaiting Manuscript Input</div>
               </div>
            </div>
            <div className="space-y-3">
               <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="text-[10px] font-black text-slate-400 uppercase mb-1">OCR Status</div>
                  <div className="text-xs font-bold text-slate-700">Detected: Uthmani Script</div>
               </div>
               <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Authenticity Score</div>
                  <div className="text-xs font-bold text-emerald-600">0.985 (High Confidence)</div>
               </div>
            </div>
          </div>

          <div className="p-6 bg-white border-2 border-slate-100 rounded-2xl shadow-sm">
            <h3 className="text-xs font-black text-slate-800 uppercase mb-4 tracking-widest border-b border-slate-100 pb-2 flex items-center gap-2">
               <BarChart3 className="w-4 h-4 text-indigo-600" /> Global Recommendation
            </h3>
            <div className="space-y-2">
               {[
                 { label: 'Tajweed Mastery', fit: 98, cls: 'w-[98%]' },
                 { label: 'Hifz Accelerator', fit: 85, cls: 'w-[85%]' },
                 { label: 'Arabic Foundation', fit: 92, cls: 'w-[92%]' }
               ].map((item) => (
                 <div key={item.label} className="space-y-1">
                    <div className="flex justify-between text-[10px] font-bold uppercase text-slate-500">
                       <span>{item.label}</span>
                       <span className="text-indigo-600">{item.fit}% Match</span>
                    </div>
                    <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                       <div className={`h-full bg-indigo-500 ${item.cls}`}></div>
                    </div>
                 </div>
               ))}
            </div>
            <button className="w-full mt-4 py-2 bg-indigo-600 text-white rounded-lg text-[10px] font-black uppercase hover:bg-indigo-700 transition-colors">
              Update Recommendation Model
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
