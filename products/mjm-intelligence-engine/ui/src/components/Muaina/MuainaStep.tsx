import React from 'react';

const MuainaStep = ({ previousData, onBack }) => {
  const bundle = previousData?.result;
  const proposal = bundle?.proposal_package;
  const litigation = proposal?.litigation_bundle;

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-red-600">🔴 Muaina (Inspection)</h2>

      {proposal ? (
        <div className="space-y-6">
          <div className="border-l-4 border-red-500 pl-4">
            <h3 className="font-bold text-lg">{proposal.title}</h3>
            <p className="text-gray-600">{proposal.description}</p>
          </div>

          <div className="bg-blue-50 p-4 rounded border border-blue-200">
            <h4 className="font-bold text-blue-800 mb-2">⚖️ UK Litigation Readiness (Specialized)</h4>
            <div className="text-sm space-y-2">
              <p><strong>Guidance:</strong> {litigation?.et1_guidance}</p>
              <div className="p-2 bg-white rounded border whitespace-pre-wrap font-mono text-xs">
                {litigation?.witness_statement_draft}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {proposal.roadmap.map((step, i) => (
              <div key={i} className="p-3 bg-gray-100 rounded text-sm">
                <span className="font-bold text-red-600">{step.phase}:</span> {step.action}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-gray-400">No proposal data available.</div>
      )}

      <div className="mt-8 flex space-x-4">
        <button onClick={onBack} className="bg-gray-200 px-4 py-2 rounded">Back</button>
        <button
          onClick={() => console.log('Final Bundle:', bundle)}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Download Submission Package
        </button>
      </div>
    </div>
  );
};

export default MuainaStep;
