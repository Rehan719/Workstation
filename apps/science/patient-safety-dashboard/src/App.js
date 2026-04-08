import React from 'react';
import QuadraVeritasRadar from './components/QuadraVeritasRadar';

function App() {
  const mockScores = {
    I: 0.98,
    II: 0.94,
    III: 0.88,
    IV: 0.92,
    overall: 0.935
  };

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <header className="App-header">
        <h1>Patient Safety Intelligence Dashboard v13.0</h1>
        <p>Sovereign Autonomous Execution — Science Grand Operation</p>
      </header>
      <main>
        <section style={{ maxWidth: '800px', margin: '40px auto' }}>
          <QuadraVeritasRadar scores={mockScores} />
        </section>
        <section style={{ maxWidth: '800px', margin: '40px auto' }}>
          <h2>Strategic Risk Forecast</h2>
          <ul>
            <li><strong>Liability Probability:</strong> 92% (90% Confidence)</li>
            <li><strong>Regulatory Action Probability:</strong> 85% (85% Confidence)</li>
            <li><strong>Current Convergence Status:</strong> Adaptive Inevitability</li>
          </ul>
        </section>
      </main>
      <footer style={{ marginTop: '50px', fontSize: '0.8em', borderTop: '1px solid #ccc', paddingTop: '10px' }}>
        <p>Product ID: VSB-SIG-SCI-13.0 | Status: QUADRA-VERITAS-COMPLETE</p>
      </footer>
    </div>
  );
}

export default App;
