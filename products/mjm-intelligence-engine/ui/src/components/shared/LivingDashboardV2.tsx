import React from 'react';

const MetaCognitivePanel = ({ report }) => {
  if (!report) return <div className="p-4 text-gray-500 italic">No introspection data yet...</div>;

  return (
    <div className="p-4 bg-indigo-900 text-indigo-100 rounded-lg shadow-xl border border-indigo-700">
      <h3 className="text-sm font-black mb-3 flex items-center">
        <span className="w-2 h-2 bg-indigo-400 rounded-full animate-ping mr-2"></span>
        META-COGNITIVE INTROSPECTION
      </h3>

      <div className="space-y-3">
        <div className="bg-indigo-950 p-2 rounded">
          <div className="text-[10px] text-indigo-400 uppercase">Chosen Strategy</div>
          <div className="font-bold text-lg">{report.chosen_strategy.name}</div>
        </div>

        <div className="text-xs italic opacity-80">
          "{report.reasoning}"
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div className="border border-indigo-700 p-1 text-center">
            <div className="text-[8px] uppercase">Confidence</div>
            <div className="font-mono">{(report.confidence * 100).toFixed(1)}%</div>
          </div>
          <div className="border border-indigo-700 p-1 text-center">
            <div className="text-[8px] uppercase">Improvement</div>
            <div className="font-mono text-green-400">+{report.expected_improvement.toFixed(2)}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const EpistemicVisualizer = ({ summary }) => {
  return (
    <div className="mt-4 p-3 bg-slate-900 border border-slate-700 rounded text-xs font-mono">
      <div className="text-indigo-400 mb-2">EPISTEMIC_STATE_SUMMARY:</div>
      <div className="grid grid-cols-2 gap-2 text-[10px]">
        <div>FACTS: {summary?.total_facts || 0}</div>
        <div>UNCERTAINTY: {summary?.total_uncertainties || 0}</div>
      </div>
      <div className="mt-2 pt-2 border-t border-slate-800">
        <div className="text-yellow-500 uppercase text-[8px]">Recommended Research:</div>
        <ul className="list-disc list-inside opacity-70">
          {summary?.recommended_research?.map((r, i) => <li key={i}>{r}</li>)}
        </ul>
      </div>
    </div>
  );
};

const LivingDashboardV2 = ({ metrics, metaReport, epistemicSummary }) => {
  return (
    <div className="space-y-4">
      <MetaCognitivePanel report={metaReport} />
      <div className="p-4 bg-slate-900 text-green-400 rounded-lg shadow-xl font-mono text-sm border border-green-900">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse mr-2"></span>
          ORGANISM HEALTH v2.0
        </h3>

        <div className="grid grid-cols-2 gap-4">
          <div className="border border-green-800 p-2">
            <div className="text-gray-500">INGESTION_RATE</div>
            <div className="text-xl">{metrics?.ingestionRate || '18.5'} s/m</div>
          </div>
          <div className="border border-green-800 p-2">
            <div className="text-gray-500">LEARNING_VELOCITY</div>
            <div className="text-xl text-indigo-400">{(metrics?.learningVelocity || 0.95).toFixed(2)} Δ</div>
          </div>
        </div>

        <EpistemicVisualizer summary={epistemicSummary} />
      </div>
    </div>
  );
};

export default LivingDashboardV2;
