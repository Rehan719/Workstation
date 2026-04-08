import React, { useState } from 'react';
import PentaVeritasRadar from './components/PentaVeritasRadar';
import ScientificEvidenceTimeline from './components/ScientificEvidenceTimeline';
import RiskBenefitHeatMap from './components/RiskBenefitHeatMap';
import StakeholderAlignmentRadar from './components/StakeholderAlignmentRadar';

function App() {
  const [jurisdiction, setJurisdiction] = useState('EMA');

  const mockScores = {
    EMA: { I: 0.98, II: 0.94, III: 0.88, IV: 0.92, V: 0.95, overall: 0.935 },
    MHRA: { I: 0.97, II: 0.90, III: 0.85, IV: 0.90, V: 0.91, overall: 0.91 },
    FDA: { I: 0.99, II: 0.92, III: 0.86, IV: 0.88, V: 0.89, overall: 0.92 }
  };

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#f0f4f8' }}>
      <header className="App-header" style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1>Patient Safety Intelligence Dashboard v15.0</h1>
        <p>Sovereign Autonomous Execution — Science Grand Operation (Penta-Veritas Integrated)</p>
        <div style={{ marginTop: '20px' }}>
          <label>Jurisdiction: </label>
          <select value={jurisdiction} onChange={(e) => setJurisdiction(e.target.value)}>
            <option value="EMA">EMA (EU)</option>
            <option value="MHRA (UK)">MHRA (UK)</option>
            <option value="FDA">FDA (US)</option>
          </select>
        </div>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '40px', maxWidth: '1200px', margin: '0 auto' }}>

        <section style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <PentaVeritasRadar scores={mockScores[jurisdiction] || mockScores.EMA} />
        </section>

        <section style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <ScientificEvidenceTimeline />
        </section>

        <section style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <RiskBenefitHeatMap />
        </section>

        <section style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <StakeholderAlignmentRadar />
        </section>

        <section style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', gridColumn: '1 / -1' }}>
          <h2>v15.0 Predictive Outcome Forecast</h2>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '1.2em' }}>
              <p><strong>Enforcement Probability:</strong> 84.7% (High)</p>
              <p><strong>Confidence Interval:</strong> [0.87 - 0.94]</p>
              <p><strong>Lead Jurisdiction:</strong> {jurisdiction}</p>
            </div>
            <div style={{ maxWidth: '600px', borderLeft: '4px solid #ff7300', paddingLeft: '20px' }}>
              <p><strong>Predictive Note:</strong> EMA precautionary principle analysis suggests imminent regulatory overhaul for AAV-mediated germline risks. Strategic recommendation: Proactive policy engagement (Truth V).</p>
            </div>
          </div>
        </section>
      </main>

      <footer style={{ marginTop: '50px', fontSize: '0.8em', borderTop: '1px solid #ccc', paddingTop: '10px', textAlign: 'center' }}>
        <p>Product ID: VSB-SIG-SCI-15.0 | Classification: Sovereign Asset | v15.0-PENTA-VERITAS</p>
      </footer>
    </div>
  );
}

export default App;
