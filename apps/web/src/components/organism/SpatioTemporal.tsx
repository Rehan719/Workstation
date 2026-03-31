import React, { useState, useEffect } from 'react';

const SpatioTemporal: React.FC = () => {
    const [currentTime, setCurrentTime] = useState(Date.now());
    const [timeScale, setTimeScale] = useState(1);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentTime(prev => prev + (100 * timeScale));
        }, 100);
        return () => clearInterval(interval);
    }, [timeScale]);

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px', border: '1px solid #00d4ff' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2 style={{ margin: 0, color: '#00d4ff' }}>4D Spatio-Temporal Dashboard (L14)</h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '10px' }}>Time Scale:</span>
                    <input type="range" min="1" max="100" value={timeScale} onChange={(e) => setTimeScale(parseInt(e.target.value))} />
                </div>
            </div>

            <div style={{ position: 'relative', height: '150px', border: '1px solid #111', background: 'linear-gradient(180deg, #050505 0%, #111 100%)', borderRadius: '8px' }}>
                {/* Simulated temporal trails */}
                <svg width="100%" height="100%">
                    <path d="M0 75 Q 100 20, 200 75 T 400 75" fill="none" stroke="#00d4ff" strokeWidth="2" strokeDasharray="10,5" />
                    <circle cx="200" cy="75" r="5" fill="#fff" />
                    <text x="210" y="70" fill="#fff" fontSize="8">Current Reality</text>
                </svg>
            </div>

            <div style={{ marginTop: '20px', fontSize: '12px', fontFamily: 'monospace' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#888' }}>
                    <span>Earth Baseline: {new Date(currentTime).toISOString()}</span>
                    <span>Mars Relative: T + 842s</span>
                </div>
                <div style={{ marginTop: '10px', color: '#00d4ff' }}>
                    Sovereign Consensus Status: CROSS-PLANETARY SYNC ACTIVE
                </div>
            </div>
        </div>
    );
};

export default SpatioTemporal;
