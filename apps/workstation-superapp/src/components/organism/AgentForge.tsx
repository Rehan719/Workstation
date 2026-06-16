import React, { useState } from 'react';
import { notImplemented } from '@workstation/ui';

type AgentNode = { id: string; type: string; name: string; x: number; y: number };

const NODE_COLOR: Record<string, string> = {
    COGNITIVE: '#d946ef',
    GOVERNANCE: '#22d3ee',
    REASONING: '#d946ef',
    ACTION: '#22d3ee',
    EXECUTION: '#22d3ee',
};

const AgentForge: React.FC = () => {
    const [nodes, setNodes] = useState<AgentNode[]>([
        { id: 'brain',  type: 'COGNITIVE',  name: 'Nematron v1.0', x: 30,  y: 70 },
        { id: 'immune', type: 'GOVERNANCE', name: 'Nemoclaw v1.0', x: 190, y: 70 },
        { id: 'limbs',  type: 'EXECUTION',  name: 'OpenClaw v1.0', x: 350, y: 70 },
    ]);

    const addNode = (type: string) => {
        setNodes(prev => [...prev, {
            id: `node-${prev.length}`,
            type,
            name: `${type.charAt(0) + type.slice(1).toLowerCase()} Agent`,
            x: 30 + (prev.length % 4) * 140,
            y: 70 + Math.floor(prev.length / 4) * 80,
        }]);
    };

    return (
        <div className="p-5 bg-black/90 text-white rounded-xl min-h-[400px]">
            <div className="flex justify-between items-center mb-5">
                <h2 className="text-xs font-black uppercase tracking-widest border-l-4 border-fuchsia-500 pl-4">
                    Developer Forge: Agent Composer
                </h2>
                <div className="flex gap-2">
                    <button
                        type="button"
                        onClick={() => addNode('REASONING')}
                        className="bg-slate-900 text-white border border-fuchsia-500 px-4 py-1.5 rounded text-[10px] font-black uppercase tracking-widest hover:bg-fuchsia-500/10 transition-colors"
                    >
                        + Reasoning
                    </button>
                    <button
                        type="button"
                        onClick={() => addNode('ACTION')}
                        className="bg-slate-900 text-white border border-cyan-400 px-4 py-1.5 rounded text-[10px] font-black uppercase tracking-widest hover:bg-cyan-400/10 transition-colors"
                    >
                        + Action
                    </button>
                    <button onClick={() => notImplemented('Deploy Swarm')}
                        type="button"
                        className="bg-fuchsia-500 text-white px-5 py-1.5 rounded text-[10px] font-black uppercase tracking-widest hover:bg-fuchsia-400 transition-colors"
                    >
                        Deploy Swarm
                    </button>
                </div>
            </div>

            {/* SVG canvas — node x/y are SVG attributes, not CSS inline styles */}
            <div className="relative w-full h-72 bg-slate-950 rounded-lg border border-dashed border-slate-800 overflow-hidden">
                <svg width="100%" height="100%">
                    {/* Edges */}
                    {nodes.map((node, i) =>
                        i < nodes.length - 1 && (
                            <line
                                key={`edge-${i}`}
                                x1={node.x + 60} y1={node.y + 25}
                                x2={nodes[i + 1].x} y2={nodes[i + 1].y + 25}
                                stroke="#334155" strokeWidth="2" strokeDasharray="5,5"
                            />
                        )
                    )}
                    {/* Nodes */}
                    {nodes.map(node => {
                        const color = NODE_COLOR[node.type] ?? '#22d3ee';
                        return (
                            <g key={node.id}>
                                <rect
                                    x={node.x} y={node.y}
                                    width="120" height="50" rx="6"
                                    fill="#111827" stroke={color} strokeWidth="1"
                                />
                                <text
                                    x={node.x + 60} y={node.y + 17}
                                    textAnchor="middle"
                                    fill={color}
                                    fontSize="8"
                                    fontWeight="bold"
                                    fontFamily="monospace"
                                >
                                    {node.type}
                                </text>
                                <text
                                    x={node.x + 60} y={node.y + 33}
                                    textAnchor="middle"
                                    fill="#94a3b8"
                                    fontSize="8"
                                    fontFamily="monospace"
                                >
                                    {node.name}
                                </text>
                            </g>
                        );
                    })}
                </svg>
            </div>

            <p className="mt-4 text-[10px] text-slate-600 italic font-bold">
                Node-based composition active. Genetic inheritance: 98.4%. Swarm stability: NOMINAL.
            </p>
        </div>
    );
};

export default AgentForge;
