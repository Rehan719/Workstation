import React from 'react';

const LivingDashboard = ({ metrics }) => {
  return (
    <div className="p-4 bg-slate-900 text-green-400 rounded-lg shadow-xl font-mono text-sm border border-green-900">
      <h3 className="text-lg font-bold mb-4 flex items-center">
        <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse mr-2"></span>
        SYSTEM HEALTH & ADAPTATION METRICS
      </h3>

      <div className="grid grid-cols-2 gap-4">
        <div className="border border-green-800 p-2">
          <div className="text-gray-500">SENSORY_INPUT_RATE</div>
          <div className="text-xl">{metrics?.ingestionRate || '14.2'} items/sec</div>
        </div>
        <div className="border border-green-800 p-2">
          <div className="text-gray-500">COGNITIVE_CONFIDENCE</div>
          <div className="text-xl">{(metrics?.confidence || 0.94 * 100).toFixed(1)}%</div>
        </div>
        <div className="border border-green-800 p-2">
          <div className="text-gray-500">LEARNING_VELOCITY</div>
          <div className="text-xl">{metrics?.learningVelocity || '0.82'} Δ/cycle</div>
        </div>
        <div className="border border-green-800 p-2">
          <div className="text-gray-500">EVOLUTION_STATUS</div>
          <div className="text-xl text-yellow-500">STABLE</div>
        </div>
      </div>

      <div className="mt-4 border-t border-green-900 pt-2">
        <div className="text-gray-500 mb-1">PROVENANCE_LOG:</div>
        <div className="h-20 overflow-y-auto text-xs opacity-70">
          [15:42:01] INGESTED: clinical_trial_data_v4<br/>
          [15:42:05] PATTERN_MATCH: autoimmune_risk_signal (0.91)<br/>
          [15:42:10] EVOLUTION_TRIGGER: weighting_adjustment_whistleblower<br/>
          [15:42:12] STATE_CHECKPOINT: CHK-MUA-1712850132
        </div>
      </div>
    </div>
  );
};

export default LivingDashboard;
