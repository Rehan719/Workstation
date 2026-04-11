import React, { useState } from 'react';

const MushahidaStep = ({ onNext }) => {
  const [queries, setQueries] = useState('');

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-green-700">🟢 Mushahida (Observation)</h2>
      <p className="mb-4 text-gray-600">Gather raw evidence and document chronological events.</p>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Search Queries</label>
          <textarea
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            rows={4}
            placeholder="Enter queries separated by newlines..."
            value={queries}
            onChange={(e) => setQueries(e.target.value)}
          />
        </div>

        <button
          onClick={() => onNext({ queries: queries.split('\n') })}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
        >
          Acquire Evidence
        </button>
      </div>
    </div>
  );
};

export default MushahidaStep;
