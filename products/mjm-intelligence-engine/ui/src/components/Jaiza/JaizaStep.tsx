import React from 'react';

const JaizaStep = ({ evidence, onNext, onBack }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-yellow-600">🟡 Jaiza (Evaluation)</h2>
      <p className="mb-4 text-gray-600">Analyze patterns and assess risk-benefit ratios.</p>

      <div className="bg-gray-50 p-4 rounded mb-6">
        <h3 className="font-semibold mb-2">Evidence Summary</h3>
        <p>Items collected: {evidence?.queries?.length || 0}</p>
      </div>

      <div className="flex space-x-4">
        <button
          onClick={onBack}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 transition"
        >
          Back
        </button>
        <button
          onClick={() => onNext({ patterns: ['sample-pattern-1'] })}
          className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700 transition"
        >
          Analyze Context
        </button>
      </div>
    </div>
  );
};

export default JaizaStep;
