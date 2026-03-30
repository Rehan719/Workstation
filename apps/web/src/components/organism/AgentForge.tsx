import React, { useState } from 'react';

const AgentForge: React.FC = () => {
    const [nodes, setNodes] = useState([
        { id: 'brain', type: 'COGNITIVE', name: 'Nematron v1.0', x: 100, y: 100 },
        { id: 'immune', type: 'GOVERNANCE', name: 'Nemoclaw v1.0', x: 300, y: 100 },
        { id: 'limbs', type: 'EXECUTION', name: 'OpenClaw v1.0', x: 500, y: 100 }
    ]);

    const addNode = (type: string) => {
        const newNode = {
            id: `node-${Date.now()}`,
            type,
            name: `${type.charAt(0) + type.slice(1).toLowerCase()} Agent`,
            x: Math.random() * 400 + 50,
            y: Math.random() * 200 + 50
        };
        setNodes([...nodes, newNode]);
    };

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px', minHeight: '400px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2 style={{ margin: 0, borderLeft: '4px solid #ff00ff', paddingLeft: '15px' }}>Developer Forge: Agent Composer</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button onClick={() => addNode('REASONING')} style={{ background: '#1a1a1a', color: '#fff', border: '1px solid #ff00ff', padding: '5px 15px', borderRadius: '4px', cursor: 'pointer' }}>+ Reasoning</button>
                    <button onClick={() => addNode('ACTION')} style={{ background: '#1a1a1a', color: '#fff', border: '1px solid #00d4ff', padding: '5px 15px', borderRadius: '4px', cursor: 'pointer' }}>+ Action</button>
                    <button style={{ background: '#ff00ff', color: '#fff', border: 'none', padding: '5px 20px', borderRadius: '4px', fontWeight: 'bold' }}>Deploy Swarm</button>
                </div>
            </div>

            <div style={{ position: 'relative', width: '100%', height: '300px', background: '#111', borderRadius: '8px', border: '1px dashed #333', overflow: 'hidden' }}>
                <svg style={{ position: 'absolute', width: '100%', height: '100%', pointerEvents: 'none' }}>
                    {nodes.map((node, i) => i < nodes.length - 1 && (
                        <line key={i} x1={node.x + 50} y1={node.y + 25} x2={nodes[i+1].x} y2={nodes[i+1].y + 25} stroke="#333" strokeWidth="2" strokeDasharray="5,5" />
                    ))}
                </svg>
                {nodes.map(node => (
                    <div key={node.id} style={{
                        position: 'absolute', left: node.x, top: node.y,
                        width: '120px', padding: '10px', background: '#1a1a1a',
                        border: `1px solid ${node.type === 'COGNITIVE' ? '#ff00ff' : '#00d4ff'}`,
                        borderRadius: '6px', fontSize: '10px', textAlign: 'center',
                        boxShadow: '0 4px 10px rgba(0,0,0,0.5)'
                    }}>
                        <div style={{ fontWeight: 'black', marginBottom: '5px', color: node.type === 'COGNITIVE' ? '#ff00ff' : '#00d4ff' }}>{node.type}</div>
                        <div>{node.name}</div>
                    </div>
                ))}
            </div>

            <p style={{ marginTop: '15px', fontSize: '10px', color: '#555', fontStyle: 'italic' }}>
                Node-based composition active. Genetic inheritance: 98.4%. Swarm stability: NOMINAL.
            </p>
        </div>
    );
};

export default AgentForge;
