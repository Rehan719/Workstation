import React from 'react';

const QuantumLabs = () => (
  <div className="p-8 bg-indigo-950 text-white rounded-3xl shadow-2xl border border-indigo-500/30">
    <h2 className="text-3xl font-black text-indigo-300 mb-8 flex items-center gap-3">
      Quantum Product Demos
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {['Quantum Bio Forge', 'Evolutionary AI', 'Universe Simulator'].map(product => (
        <div key={product} className="p-8 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-md group hover:bg-white/10 transition-all cursor-pointer">
           <div className="w-12 h-12 bg-indigo-500/20 rounded-lg mb-6 flex items-center justify-center group-hover:scale-110 transition-transform">✨</div>
           <h4 className="font-bold text-xl mb-2">{product}</h4>
           <p className="text-xs text-indigo-200/60 leading-relaxed mb-6">Interactive high-fidelity demonstration of quantum-enhanced simulation.</p>
           <button className="text-[10px] font-black uppercase tracking-widest text-indigo-400 group-hover:text-white">Launch Demo →</button>
        </div>
      ))}
    </div>
  </div>
);

export default QuantumLabs;
