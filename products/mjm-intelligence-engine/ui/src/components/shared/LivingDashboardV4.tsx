import React from 'react';

const HyperdimensionalVisualizer = () => (
  <div className="h-64 bg-black rounded-lg border border-indigo-900 relative overflow-hidden flex items-center justify-center shadow-[0_0_50px_rgba(79,70,229,0.3)]">
    <div className="absolute inset-0 opacity-30">
      <div className="grid grid-cols-10 grid-rows-10 h-full w-full">
        {[...Array(100)].map((_, i) => (
          <div key={i} className="border-[0.5px] border-indigo-500/20 animate-pulse" style={{ animationDelay: `${i * 10}ms` }}></div>
        ))}
      </div>
    </div>
    <div className="z-10 text-center">
      <div className="text-4xl font-black text-white tracking-[1em] opacity-20 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 select-none">
        10,000 DIMENSIONS
      </div>
      <div className="text-indigo-400 font-mono text-sm animate-bounce">
        HYPERDIMENSIONAL_FABRIC_SYNC_ACTIVE
      </div>
    </div>
  </div>
);

const Swarmv4Monitor = ({ swarmStatus }) => (
  <div className="p-4 bg-slate-900 border border-indigo-900 rounded-lg shadow-2xl">
    <h4 className="text-[10px] font-black text-indigo-300 uppercase tracking-widest mb-4">Autonomous_Research_Swarm_v4</h4>
    <div className="space-y-3">
      {['Skeptic', 'Innovator', 'Synthesizer', 'Historian'].map((role, i) => (
        <div key={i} className="flex items-center justify-between group">
          <div className="flex items-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-red-500' : 'bg-green-500'} group-hover:animate-ping`}></span>
            <span className="text-xs text-slate-400 font-bold">{role}</span>
          </div>
          <div className="text-[10px] text-slate-600 font-mono italic">
            {i === 0 ? 'Critiquing_Hypothesis_3...' : 'Searching_Repositories...'}
          </div>
        </div>
      ))}
    </div>
    <div className="mt-4 pt-4 border-t border-indigo-900/50 text-center">
      <div className="text-xs text-green-400 font-black animate-pulse">CONSENSUS: 94.2% (CALIBRATED)</div>
    </div>
  </div>
);

const LivingDashboardV4 = ({ metrics, swarmStatus, recursiveDepth }) => {
  return (
    <div className="space-y-8 max-w-6xl mx-auto p-4">
      <header className="flex justify-between items-end border-b border-indigo-900/30 pb-4">
        <div>
          <h2 className="text-2xl font-black text-indigo-400 tracking-tighter">HYPER-META-COGNITIVE ORGANISM</h2>
          <p className="text-[10px] text-slate-500 font-mono uppercase tracking-[0.3em]">Version 4.0.0.RECURSIVE_HYPER_META</p>
        </div>
        <div className="text-right">
          <div className="text-[10px] text-indigo-300 font-black mb-1">RECURSION_DEPTH_GAUGE</div>
          <div className="flex space-x-1 h-4">
            {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
              <div key={i} className={`w-2 rounded-sm ${i <= (recursiveDepth || 4) ? 'bg-indigo-500' : 'bg-indigo-950 opacity-20'}`}></div>
            ))}
          </div>
        </div>
      </header>

      <HyperdimensionalVisualizer />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Swarmv4Monitor swarmStatus={swarmStatus} />

        <div className="md:col-span-2 p-6 bg-indigo-950/20 border border-indigo-900/50 rounded-lg relative overflow-hidden backdrop-blur-sm">
          <div className="absolute top-0 right-0 p-2 text-[8px] text-indigo-500/50 font-mono">SOVEREIGN_AMYGDALA_PULSE: 0.22ms</div>
          <h4 className="text-[10px] font-black text-indigo-300 uppercase mb-4">Recursive_Intelligence_Fabric_Metrics</h4>
          <div className="grid grid-cols-2 gap-8">
            <div className="space-y-1">
              <div className="text-[9px] text-slate-500 uppercase font-black">Meta_Recursive_Gain</div>
              <div className="text-3xl font-black text-white">+28.5% <span className="text-xs text-indigo-400 font-normal">Δ/depth</span></div>
            </div>
            <div className="space-y-1">
              <div className="text-[9px] text-slate-500 uppercase font-black">Blueprint_Reusability</div>
              <div className="text-3xl font-black text-white">92.1% <span className="text-xs text-green-400 font-normal">INSTANT</span></div>
            </div>
          </div>
          <div className="mt-8 h-20 border-t border-indigo-900/30 pt-4 flex space-x-4 overflow-x-auto">
             {['PATIENT_SAFETY', 'LEGAL_TRIBUNAL', 'GENOME_SYNTH', 'ENV_IMPACT'].map(project => (
               <div key={project} className="px-3 py-1 bg-indigo-900/40 rounded text-[9px] text-indigo-300 font-black border border-indigo-800/50 flex-shrink-0 flex items-center">
                 <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full mr-2"></span>
                 {project}
               </div>
             ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LivingDashboardV4;
