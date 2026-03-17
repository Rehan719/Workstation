import React from 'react';
import { Layers } from 'lucide-react';

export const QEPEngine: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Quad Engine Platform</h1>
        <p className="text-slate-500">Monitoring orchestration: Discovery, Ingestion, Synthesis, Deployment.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {['Discovery', 'Ingestion', 'Synthesis', 'Deployment'].map(engine => (
          <div key={engine} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 flex flex-col items-center">
            <div className="w-16 h-16 rounded-full border-4 border-aura/20 border-t-aura animate-spin-slow mb-4 flex items-center justify-center">
              <Layers size={24} className="text-aura" />
            </div>
            <h3 className="font-bold">{engine}</h3>
            <span className="text-[10px] text-vital font-black uppercase mt-1">Operational</span>
          </div>
        ))}
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
         <div className="flex justify-between items-center mb-8">
           <h3 className="text-xl font-bold">Active Pipeline Visualization</h3>
           <div className="flex gap-4">
             <div className="flex items-center gap-2">
               <div className="w-3 h-3 rounded-full bg-aura"></div>
               <span className="text-[10px] font-bold uppercase text-slate-500">Data Stream</span>
             </div>
             <div className="flex items-center gap-2">
               <div className="w-3 h-3 rounded-full bg-vital"></div>
               <span className="text-[10px] font-bold uppercase text-slate-500">Synthesis Node</span>
             </div>
           </div>
         </div>
         <div className="h-64 bg-sovereign rounded-2xl border border-slate-800 flex items-center justify-center">
            <p className="text-slate-700 font-bold uppercase tracking-widest text-xs">Pipeline Graph Integration...</p>
         </div>
      </div>
    </div>
  );
};
