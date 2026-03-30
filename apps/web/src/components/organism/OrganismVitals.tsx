import React, { useState, useEffect } from 'react';

const OrganismVitals: React.FC = () => {
    const [vitals, setVitals] = useState({
        sentience: 0,
        compliance: 0,
        throughput: 0,
        load: 0,
        stability: 0
    });

    useEffect(() => {
        // Mock socket connection for visual verification
        const interval = setInterval(() => {
            setVitals({
                sentience: 85 + Math.random() * 10,
                compliance: 98 + Math.random() * 2,
                throughput: 12 + Math.random() * 5,
                load: 45 + Math.random() * 20,
                stability: 95 + Math.random() * 5
            });
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const MetricCard = ({ label, value, unit, color }: any) => (
        <div style={{ padding: '15px', borderRadius: '8px', background: '#1a1a1a', border: `1px solid ${color}`, minWidth: '150px' }}>
            <div style={{ fontSize: '12px', color: '#888', textTransform: 'uppercase' }}>{label}</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#fff', marginTop: '5px' }}>
                {typeof value === 'number' ? value.toFixed(1) : value}{unit}
            </div>
        </div>
    );

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px' }}>
            <h2 style={{ marginBottom: '20px', borderLeft: '4px solid #00ff00', paddingLeft: '15px' }}>Organism Health Vitals</h2>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
                <MetricCard label="System Sentience" value={vitals.sentience} unit="%" color="#00d4ff" />
                <MetricCard label="Compliance" value={vitals.compliance} unit="%" color="#00ff00" />
                <MetricCard label="Throughput" value={vitals.throughput} unit=" t/m" color="#ff00ff" />
                <MetricCard label="Cognitive Load" value={vitals.load} unit="%" color="#ffff00" />
                <MetricCard label="Stability" value={vitals.stability} unit="%" color="#00ff00" />
            </div>
        </div>
    );
};

export default OrganismVitals;
