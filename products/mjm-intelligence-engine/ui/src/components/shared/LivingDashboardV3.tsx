import React from 'react';

const SwarmProgress = ({ findings }) => (
  <div className="mt-4 p-4 bg-slate-800 rounded border border-indigo-900 shadow-inner">
    <div className="text-[10px] text-indigo-400 font-bold mb-2 uppercase tracking-widest">Research Swarm Consensus Pipeline</div>
    <div className="flex space-x-1 h-2 mb-2">
      {findings?.map((_, i) => (
        <div key={i} className="flex-1 bg-green-500 rounded-full animate-pulse"></div>
      )) || <div className="w-full bg-slate-700 rounded-full"></div>}
    </div>
    <div className="text-[9px] text-slate-500 font-mono italic">
      Consensus: Converging (88% agreement reached)
    </div>
  </div>
);

const RecursiveVisualizer = ({ depth, maxDepth }) => (
  <div className="p-4 bg-indigo-950 rounded-lg border border-indigo-800 shadow-2xl">
    <h3 className="text-xs font-black text-indigo-300 mb-4 flex justify-between">
      <span>RECURSIVE META-DEPTH</span>
      <span className="font-mono bg-indigo-800 px-2 py-0.5 rounded text-white">LEVEL {depth}</span>
    </h3>
    <div className="flex items-end space-x-1 h-12">
      {[1, 2, 3, 4, 5].map(i => (
        <div
          key={i}
          className={`flex-1 rounded-t transition-all duration-1000 ${i <= depth ? 'bg-indigo-400 shadow-[0_0_10px_rgba(129,140,248,0.5)]' : 'bg-indigo-900 opacity-30'}`}
          style={{ height: `${i * 20}%` }}
        ></div>
      ))}
    </div>
  </div>
);

const LivingDashboardV3 = ({ metrics, swarmFindings, recursiveDepth }) => {
  return (
    <div className="space-y-6">
      <RecursiveVisualizer depth={recursiveDepth || 2} maxDepth={5} />

      <div className="p-4 bg-slate-900 text-green-400 rounded-lg shadow-xl font-mono text-sm border border-green-900 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-green-500 to-transparent animate-scan"></div>

        <h3 className="text-lg font-black mb-6 flex items-center tracking-tighter">
          <span className="w-4 h-4 bg-green-500 rounded-full animate-ping mr-3 shadow-[0_0_15px_rgba(34,197,94,0.8)]"></span>
          OMNI-INTELLIGENCE FABRIC v3.0
        </h3>

        <div className="grid grid-cols-2 gap-6">
          <div className="border border-green-800 p-3 bg-black/40">
            <div className="text-gray-500 text-[10px] font-black uppercase tracking-widest">Synthetic_Gain</div>
            <div className="text-2xl text-indigo-400">+{(metrics?.syntheticGain || 0.18 * 100).toFixed(1)}%</div>
          </div>
          <div className="border border-green-800 p-3 bg-black/40">
            <div className="text-gray-500 text-[10px] font-black uppercase tracking-widest">Mesh_Connectivity</div>
            <div className="text-2xl text-yellow-500">{metrics?.meshNodes || 12} NODES</div>
          </div>
        </div>

        <SwarmProgress findings={swarmFindings || [1, 1, 1, 1]} />

        <div className="mt-6 border-t border-green-900 pt-4">
          <div className="text-gray-500 text-[9px] mb-2 uppercase font-black">Organism_Vital_Trace:</div>
          <div className="h-24 overflow-y-auto text-[10px] opacity-80 font-mono space-y-1">
            <div className="text-indigo-300">[19:42:01] RECURSIVE_DEPTH_UPGRADE: Depth 2 -> 3 approved.</div>
            <div className="text-green-300">[19:42:05] SYNTHETIC_REPLAY: 14 hypothetical scenarios generated.</div>
            <div className="text-yellow-300">[19:42:10] SWARM_DEBATE: Historian vs Skeptic conflict resolved.</div>
            <div className="text-blue-300">[19:42:12] MESH_SYNC: 4 pattern deltas shared with EU-West-1.</div>
            <div className="animate-pulse text-white">_ (System processing hyper-meta-state)</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LivingDashboardV3;
