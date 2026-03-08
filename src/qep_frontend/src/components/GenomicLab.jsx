import React from 'react';

const GenomicLab = () => (
  <div className="p-8 bg-slate-900 text-white rounded-3xl shadow-2xl border border-white/10">
    <h2 className="text-3xl font-black text-amber-500 mb-8">Genomic Evolution Lab</h2>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 p-12 bg-black/40 rounded-3xl border border-white/5 relative overflow-hidden">
         <div className="absolute inset-0 opacity-10" style={{backgroundImage: 'radial-gradient(circle, #f59e0b 1px, transparent 1px)', backgroundSize: '20px 20px'}}></div>
         <p className="font-mono text-amber-500/50 mb-4 tracking-tighter">SIMULATION_ACTIVE [GEN_142]</p>
         <div className="flex items-end gap-2 h-40">
           {[40, 60, 45, 80, 50, 95, 70, 85].map((h, i) => (
             <div key={i} className="flex-1 bg-amber-500/20 border-t border-amber-500" style={{height: `${h}%`}}></div>
           ))}
         </div>
         <p className="mt-6 text-sm italic text-white/60">Population fitness increasing via controlled mutation (Article 163).</p>
      </div>
      <div className="space-y-6">
        <button className="w-full py-4 bg-amber-500 text-slate-900 font-black rounded-xl">INITIATE MUTATION</button>
        <button className="w-full py-4 bg-white/5 border border-white/10 rounded-xl font-bold">EXPORT GENOTYPE</button>
      </div>
    </div>
  </div>
);

export default GenomicLab;
