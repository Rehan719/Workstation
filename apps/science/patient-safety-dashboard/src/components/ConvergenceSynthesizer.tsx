import React from 'react';

const ConvergenceSynthesizer = ({ assimilationScores, insights }: { assimilationScores: any, insights: any }) => {
  return (
    <div className="convergence-synthesizer" style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>📊 Convergence Synthesis Dashboard (v18.0)</h3>

      <div className="assimilation-card" style={{ marginBottom: '20px' }}>
        <h4>Version Assimilation Completeness</h4>
        <div className="assimilation-bars">
          {Object.entries(assimilationScores).map(([ver, score]) => (
            <div key={ver} className="assimilation-row" style={{ marginBottom: '10px' }}>
              <span style={{ fontSize: '0.8em', display: 'inline-block', width: '60px' }}>{ver}</span>
              <div style={{
                height: '10px',
                backgroundColor: '#eee',
                display: 'inline-block',
                width: 'calc(100% - 70px)',
                borderRadius: '5px',
                overflow: 'hidden'
              }}>
                <div style={{
                  height: '100%',
                  width: `${(score as number) * 100}%`,
                  backgroundColor: '#4caf50'
                }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="meta-insights">
        <h4>Meta-Learning Insights</h4>
        <ul style={{ fontSize: '0.9em' }}>
          {insights.map((insight: string, idx: number) => (
            <li key={idx} style={{ marginBottom: '5px' }}>{insight}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ConvergenceSynthesizer;
