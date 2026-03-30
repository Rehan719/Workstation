import React, { useEffect, useState } from 'react';

interface LegalEvent {
  id: string;
  date: string;
  description: string;
  source_document: string;
  legal_tags: string[];
  confidence: number;
}

export const EvidenceGraphView: React.FC = () => {
  const [events, setEvents] = useState<LegalEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const response = await fetch('/api/v1/evidence/graph');
        const data = await response.json();
        setEvents(data);
      } catch (e) {
        console.error('Failed to fetch evidence graph', e);
      } finally {
        setLoading(false);
      }
    };
    fetchGraph();
  }, []);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-2xl shadow-2xl border border-slate-800 h-[600px] flex flex-col">
      <h2 className="text-2xl font-extrabold mb-6 flex items-center">
        <span className="mr-3 text-purple-500">⚖️</span> Forensic Evidence Graph
      </h2>

      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
          {events.map((event) => (
            <div key={event.id} className="bg-slate-800/50 p-4 rounded-xl border border-slate-700 hover:border-purple-500/50 transition-all">
              <div className="flex justify-between items-start mb-2">
                <span className="text-purple-400 font-mono text-sm">{event.date}</span>
                <span className="text-[10px] px-2 py-0.5 bg-slate-700 rounded text-slate-300">
                  CONFIDENCE: {Math.round(event.confidence * 100)}%
                </span>
              </div>
              <p className="text-sm text-slate-200 mb-3">{event.description}</p>
              <div className="flex flex-wrap gap-2">
                {event.legal_tags.map(tag => (
                  <span key={tag} className="text-[10px] px-2 py-0.5 bg-purple-900/30 text-purple-300 rounded-full border border-purple-800/50">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="mt-3 text-[10px] text-slate-500 flex items-center">
                <span className="mr-2">📄 Source:</span>
                <span className="italic truncate">{event.source_document}</span>
              </div>
            </div>
          ))}
          {events.length === 0 && <div className="text-center text-slate-500 mt-20 italic">No evidence ingested yet.</div>}
        </div>
      )}
    </div>
  );
};
