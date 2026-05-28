import React, { useState, useEffect } from 'react';

const NeuralLink: React.FC = () => {
    const [synapseActivity, setSynapseActivity] = useState<number[]>([]);
    const [isLinked, setIsLinked] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            setSynapseActivity(Array.from({ length: 24 }, () => Math.random()));
        }, 100);
        return () => clearInterval(interval);
    }, []);

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px', border: '1px solid #00ff00' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2 style={{ margin: 0, color: '#00ff00', textShadow: '0 0 10px #00ff00' }}>Neural Link Bridge (L13)</h2>
                <button
                    onClick={() => setIsLinked(!isLinked)}
                    style={{ background: isLinked ? '#00ff00' : '#1a1a1a', color: isLinked ? '#000' : '#00ff00', border: '1px solid #00ff00', padding: '5px 15px', borderRadius: '20px', fontWeight: 'bold', cursor: 'pointer' }}
                >
                    {isLinked ? 'SYNAPSE ACTIVE' : 'INITIALIZE LINK'}
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: '10px', height: '100px' }}>
                {synapseActivity.map((val, i) => (
                    <div key={i} style={{
                        background: `rgba(0, 255, 0, ${val * (isLinked ? 1 : 0.2)})`,
                        borderRadius: '2px',
                        boxShadow: isLinked && val > 0.8 ? '0 0 15px #00ff00' : 'none',
                        transition: 'all 0.1s'
                    }} />
                ))}
            </div>

            <div style={{ marginTop: '20px', fontSize: '10px', color: '#008800' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Telemetry Bandwidth: 1.2 GB/s</span>
                    <span>Article 1200 Compliance: VERIFIED</span>
                </div>
                <p style={{ marginTop: '5px' }}>Subjective Qualia Feedback: {isLinked ? 'Intuiting strategic surplus...' : 'Link Idle.'}</p>
            </div>
        </div>
    );
};

export default NeuralLink;
