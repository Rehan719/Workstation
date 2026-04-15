import React, { useState } from 'react';

const MushahidaStep = ({ onNext, domainId }) => {
  const [queries, setQueries] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAcquire = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/pipeline/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          domain_id: domainId,
          queries: queries.split('\n').filter(q => q.trim()),
          contributor: 'user'
        })
      });
      const data = await response.json();
      onNext({ jobId: data.job_id });
    } catch (error) {
      console.error('Failed to start pipeline:', error);
      alert('Failed to connect to MJM Engine. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

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
          onClick={handleAcquire}
          disabled={loading || !queries.trim()}
          className={`bg-green-600 text-white px-4 py-2 rounded transition ${loading ? 'opacity-50' : 'hover:bg-green-700'}`}
        >
          {loading ? 'Initializing Engine...' : 'Acquire Evidence'}
        </button>
      </div>
    </div>
  );
};

export default MushahidaStep;
