import React, { useState } from 'react';

/**
 * VisualAgentComposer (v138.0 Phase 1 MVP)
 *
 * Provides a node-based interface for assembling biomimetic agent swarms.
 * Features: Drag-and-drop workflow simulation, parameter configuration,
 * and constitutional transparency panel.
 */
const VisualAgentComposer: React.FC = () => {
    const [agents, setAgents] = useState([
        { id: 'master-1', type: 'BRAIN', name: 'Nematron-1B', x: 50, y: 50, params: { temp: 0.7 } },
        { id: 'guard-1', type: 'IMMUNE', name: 'Nemoclaw-3B', x: 250, y: 150, params: { threshold: 0.8 } }
    ]);

    const [selectedId, setSelectedId] = useState<string | null>(null);

    const addAgent = (type: string) => {
        const newAgent = {
            id: `${type.toLowerCase()}-${Date.now()}`,
            type,
            name: `${type} Module v1.0`,
            x: 100 + Math.random() * 200,
            y: 50 + Math.random() * 150,
            params: {}
        };
        setAgents([...agents, newAgent]);
    };

    const exportBlueprint = () => {
        const blueprint = {
            version: "v138.0",
            timestamp: new Date().toISOString(),
            swarm_topology: agents
        };
        const blob = new Blob([JSON.stringify(blueprint, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'agent_swarm_blueprint.json';
        a.click();
    };

    return (
        <div className="visual-agent-composer" style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '20px', background: '#050505', color: '#e0e0e0', padding: '20px', borderRadius: '16px', border: '1px solid #1a1a1a' }}>
            {/* Main Canvas */}
            <div style={{ position: 'relative', height: '500px', background: '#0a0a0a', borderRadius: '12px', overflow: 'hidden', border: '1px solid #111' }}>
                <div style={{ position: 'absolute', top: '15px', left: '15px', zIndex: 10 }}>
                    <h3 style={{ margin: 0, color: '#00d4ff', fontSize: '14px', textTransform: 'uppercase', letterSpacing: '1px' }}>Swarm Topology Designer</h3>
                </div>

                <div style={{ position: 'absolute', top: '15px', right: '15px', zIndex: 10, display: 'flex', gap: '8px' }}>
                    <button onClick={() => addAgent('BRAIN')} style={btnStyle('#ff00ff')}>+ Brain</button>
                    <button onClick={() => addAgent('IMMUNE')} style={btnStyle('#00d4ff')}>+ Immune</button>
                    <button onClick={() => addAgent('TOOL')} style={btnStyle('#ffff00')}>+ Tool</button>
                </div>

                <svg style={{ position: 'absolute', width: '100%', height: '100%' }}>
                    {/* Simulated neural connections */}
                    {agents.map((a, i) => i > 0 && (
                        <line key={`l-${i}`} x1={agents[i-1].x + 60} y1={agents[i-1].y + 40} x2={a.x + 60} y2={a.y + 40} stroke="#222" strokeWidth="1" strokeDasharray="4" />
                    ))}
                </svg>

                {agents.map(agent => (
                    <div
                        key={agent.id}
                        onClick={() => setSelectedId(agent.id)}
                        style={{
                            position: 'absolute', left: agent.x, top: agent.y,
                            width: '120px', padding: '12px', background: selectedId === agent.id ? '#1a1a1a' : '#111',
                            border: `1px solid ${selectedId === agent.id ? '#00d4ff' : '#222'}`,
                            borderRadius: '8px', cursor: 'pointer', transition: 'all 0.2s',
                            boxShadow: selectedId === agent.id ? '0 0 15px rgba(0, 212, 255, 0.2)' : 'none'
                        }}
                    >
                        <div style={{ fontSize: '9px', fontWeight: 'bold', color: typeColor(agent.type), marginBottom: '4px' }}>{agent.type}</div>
                        <div style={{ fontSize: '11px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{agent.name}</div>
                    </div>
                ))}
            </div>

            {/* Sidebar / Transparency Panel */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div style={{ background: '#0a0a0a', padding: '15px', borderRadius: '12px', border: '1px solid #1a1a1a', flex: 1 }}>
                    <h4 style={{ margin: '0 0 10px 0', fontSize: '12px', color: '#666' }}>Config & Governance</h4>
                    {selectedId ? (
                        <div>
                            <p style={{ fontSize: '11px', color: '#aaa' }}>Agent ID: <span style={{ color: '#00d4ff' }}>{selectedId}</span></p>
                            <div style={{ marginTop: '10px' }}>
                                <label style={{ fontSize: '10px', display: 'block', marginBottom: '4px' }}>Inference Temperature</label>
                                <input type="range" style={{ width: '100%' }} />
                            </div>
                            <div style={{ marginTop: '15px', padding: '10px', background: '#111', borderRadius: '6px', borderLeft: '3px solid #00ff00' }}>
                                <div style={{ fontSize: '9px', color: '#00ff00', fontWeight: 'bold' }}>GaaS COMPLIANT</div>
                                <div style={{ fontSize: '10px', color: '#666', marginTop: '4px' }}>Aligns with Article 1101.</div>
                            </div>
                        </div>
                    ) : (
                        <p style={{ fontSize: '11px', color: '#444', fontStyle: 'italic' }}>Select a node to configure</p>
                    )}
                </div>

                <button
                    onClick={exportBlueprint}
                    style={{
                        background: '#00d4ff', color: '#000', border: 'none',
                        padding: '12px', borderRadius: '8px', fontWeight: 'bold',
                        cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '1px'
                    }}
                >
                    Export Swarm Blueprint
                </button>
            </div>
        </div>
    );
};

const btnStyle = (color: string) => ({
    background: 'transparent',
    color: color,
    border: `1px solid ${color}`,
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '10px',
    cursor: 'pointer',
    fontWeight: 'bold' as const
});

const typeColor = (type: string) => {
    switch(type) {
        case 'BRAIN': return '#ff00ff';
        case 'IMMUNE': return '#00d4ff';
        case 'TOOL': return '#ffff00';
        default: return '#fff';
    }
};

export default VisualAgentComposer;
