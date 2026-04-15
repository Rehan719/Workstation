import React, { useState, useEffect } from 'react';

const JaizaStep = ({ previousData, onNext, onBack }) => {
  const [status, setStatus] = useState('processing');
  const [result, setResult] = useState(null);

  useEffect(() => {
    let interval;
    if (previousData?.jobId) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`http://localhost:8000/pipeline/status/${previousData.jobId}`);
          const data = await res.json();
          setStatus(data.status);
          if (data.status === 'completed') {
            setResult(data.result);
            clearInterval(interval);
          }
        } catch (e) {
          console.error(e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [previousData?.jobId]);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-yellow-600">🟡 Jaiza (Evaluation)</h2>

      <div className="bg-gray-50 p-4 rounded mb-6">
        <h3 className="font-semibold mb-2">Engine Status: {status.toUpperCase()}</h3>
        {status === 'processing' && (
          <div className="animate-pulse text-blue-600">Mushahida acquisition and Jaiza evaluation in progress...</div>
        )}
        {result && (
          <div className="mt-4">
            <h4 className="font-bold text-green-700">Evidence Collected: {result.evidence_graph.items.length}</h4>
            <div className="mt-2 text-sm max-h-40 overflow-y-auto">
              {result.analysis_dossier.patterns.map((p, i) => (
                <div key={i} className="p-2 border-b">{p.pattern_id || p.description}</div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="flex space-x-4">
        <button onClick={onBack} className="bg-gray-200 px-4 py-2 rounded">Back</button>
        <button
          disabled={status !== 'completed'}
          onClick={() => onNext({ result })}
          className={`bg-yellow-600 text-white px-4 py-2 rounded ${status !== 'completed' ? 'opacity-50' : ''}`}
        >
          View Proposals
        </button>
      </div>
    </div>
  );
};

export default JaizaStep;
