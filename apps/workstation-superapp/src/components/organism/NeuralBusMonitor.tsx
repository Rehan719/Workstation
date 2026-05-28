import React, { useState, useEffect } from 'react';

interface NeuralEvent {
    id: string;
    type: string;
    source: string;
    timestamp: number;
    priority: number;
}

const NeuralBusMonitor: React.FC = () => {
    const [events, setEvents] = useState<NeuralEvent[]>([]);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        // Mocking the NeuralBridge WebSocket behavior for visual verification
        const interval = setInterval(() => {
            const newEvent: NeuralEvent = {
                id: Math.random().toString(36).substr(2, 9),
                type: ['IntentGenerated', 'GovernanceValidated', 'ActionExecuted', 'HomeostasisEvent'][Math.floor(Math.random() * 4)],
                source: ['nematron', 'nemoclaw', 'openclaw', 'system'][Math.floor(Math.random() * 4)],
                timestamp: Date.now(),
                priority: Math.floor(Math.random() * 5) + 1
            };
            setEvents(prev => [newEvent, ...prev].slice(0, 50));
            setIsConnected(true);
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    const getPriorityColor = (priority: number) => {
        if (priority === 1) return '#ff4d4d'; // Critical
        if (priority <= 3) return '#ffff4d';  // Normal
        return '#4dff4d';                     // Low
    };

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px', border: '1px solid #333' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2 style={{ margin: 0, borderLeft: '4px solid #00d4ff', paddingLeft: '15px' }}>Neural Bus Monitor</h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: isConnected ? '#00ff00' : '#ff0000', boxShadow: isConnected ? '0 0 8px #00ff00' : 'none' }} />
                    <span style={{ fontSize: '10px', fontWeight: 'bold', textTransform: 'uppercase', color: '#888' }}>
                        {isConnected ? 'libp2p Mesh Active' : 'Connecting...'}
                    </span>
                </div>
            </div>

            <div style={{ maxHeight: '400px', overflowY: 'auto', paddingRight: '10px' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', borderBottom: '1px solid #333', color: '#888' }}>
                            <th style={{ padding: '10px' }}>ID</th>
                            <th style={{ padding: '10px' }}>TYPE</th>
                            <th style={{ padding: '10px' }}>SOURCE</th>
                            <th style={{ padding: '10px' }}>TIME</th>
                            <th style={{ padding: '10px' }}>P</th>
                        </tr>
                    </thead>
                    <tbody>
                        {events.map(event => (
                            <tr key={event.id} style={{ borderBottom: '1px solid #222', transition: 'background 0.2s' }}>
                                <td style={{ padding: '10px', fontFamily: 'monospace', color: '#aaa' }}>{event.id}</td>
                                <td style={{ padding: '10px', fontWeight: 'bold', color: '#00d4ff' }}>{event.type}</td>
                                <td style={{ padding: '10px', color: '#ff00ff' }}>{event.source}</td>
                                <td style={{ padding: '10px', color: '#888' }}>{new Date(event.timestamp).toLocaleTimeString()}</td>
                                <td style={{ padding: '10px' }}>
                                    <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: getPriorityColor(event.priority) }} />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {events.length === 0 && (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#555', fontStyle: 'italic' }}>
                        Awaiting neural signals...
                    </div>
                )}
            </div>
        </div>
    );
};

export default NeuralBusMonitor;
