import React from 'react';

const MuainaStep = ({ analysis, onBack }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-red-600">🔴 Muaina (Inspection)</h2>
      <p className="mb-4 text-gray-600">Develop actionable proposals and litigation-ready packages.</p>

      <div className="border-l-4 border-red-500 pl-4 mb-6">
        <h3 className="font-semibold">Strategic Option: Regulatory Realignment</h3>
        <p className="text-sm text-gray-500">Confidence: 94% | Impact: High</p>
      </div>

      <div className="flex space-x-4">
        <button
          onClick={onBack}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 transition"
        >
          Back
        </button>
        <button
          onClick={() => alert('Exporting to UK Employment Tribunal format...')}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Export Litigation Bundle
        </button>
      </div>
    </div>
  );
};

export default MuainaStep;
