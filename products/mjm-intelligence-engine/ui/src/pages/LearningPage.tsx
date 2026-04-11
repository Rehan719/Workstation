import React from 'react';

const LearningPage = () => {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6">Cognitive Cortex Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold mb-4">Learned Patterns</h3>
          <ul className="space-y-3">
            <li className="flex justify-between items-center p-3 bg-slate-50 rounded">
              <span>procedural_fairness_gap</span>
              <span className="text-green-600 font-bold">95.2% Confidence</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-slate-50 rounded">
              <span>whistleblower_risk_signal</span>
              <span className="text-green-600 font-bold">91.8% Confidence</span>
            </li>
          </ul>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold mb-4">Evolution Queue</h3>
          <div className="p-4 border-l-4 border-yellow-400 bg-yellow-50 text-sm">
            <p className="font-bold">EVO-1712850132</p>
            <p>Recommended: Update whistleblower weighting in patient_safety</p>
            <div className="mt-3 flex space-x-2">
              <button className="bg-green-600 text-white px-3 py-1 rounded">Approve</button>
              <button className="bg-slate-200 px-3 py-1 rounded">Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningPage;
