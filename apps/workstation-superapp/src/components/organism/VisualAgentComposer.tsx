import React, { useState } from 'react';

/**
 * VisualAgentComposer (v138.0 Phase 1 MVP)
 *
 * Provides a node-based interface for assembling biomimetic agent swarms.
 * Features: Drag-and-drop workflow simulation, parameter configuration,
 * and constitutional transparency panel.
 */
const VisualAgentComposer: React.FC = () => {
    interface Agent {
        id: string;
        type: string;
        name: string;
        x: number;
        y: number;
        params: Record<string, number>;
    }

    const [agents, setAgents] = useState<Agent[]>([
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

    const selectedAgent = agents.find(a => a.id === selectedId);

    return (
        <div className="visual-agent-composer grid grid-cols-[1fr_300px] gap-5 bg-[#050505] text-[#e0e0e0] p-5 rounded-2xl border border-[#1a1a1a]">
            {/* Main Canvas */}
            <div className="relative h-[500px] bg-[#0a0a0a] rounded-xl overflow-hidden border border-[#111]">
                <div className="absolute top-[15px] left-[15px] z-10">
                    <h3 className="m-0 text-[#00d4ff] text-sm uppercase tracking-wider">Swarm Topology Designer</h3>
                </div>

                <div className="absolute top-[15px] right-[15px] z-10 flex gap-2">
                    <button type="button" onClick={() => addAgent('BRAIN')} className={btnClass('#ff00ff')}>+ Brain</button>
                    <button type="button" onClick={() => addAgent('IMMUNE')} className={btnClass('#00d4ff')}>+ Immune</button>
                    <button type="button" onClick={() => addAgent('TOOL')} className={btnClass('#ffff00')}>+ Tool</button>
                </div>

                <svg className="absolute inset-0 w-full h-full">
                    {/* Simulated neural connections */}
                    {agents.map((a, i) => i > 0 && (
                        <line key={`l-${i}`} x1={agents[i-1].x + 60} y1={agents[i-1].y + 40} x2={a.x + 60} y2={a.y + 40} stroke="#222" strokeWidth="1" strokeDasharray="4" />
                    ))}
                </svg>

                {agents.map(agent => {
                    const isSelected = selectedId === agent.id;
                    return (
                        <div
                            key={agent.id}
                            onClick={() => setSelectedId(agent.id)}
                            // left/top are genuinely free-form 2D canvas coordinates (drag-and-drop
                            // positioning), not a bounded set of values that could be pre-enumerated
                            // as Tailwind classes — set directly via the DOM through a ref callback
                            // instead of a JSX `style` attribute.
                            ref={(el) => {
                                if (el) {
                                    el.style.left = `${agent.x}px`;
                                    el.style.top = `${agent.y}px`;
                                }
                            }}
                            className={`absolute w-[120px] p-3 rounded-lg cursor-pointer transition-all border ${
                                isSelected ? 'bg-[#1a1a1a] border-[#00d4ff] shadow-[0_0_15px_rgba(0,212,255,0.2)]' : 'bg-[#111] border-[#222] shadow-none'
                            }`}
                        >
                            <div className={`text-[9px] font-bold mb-1 ${typeClass(agent.type)}`}>{agent.type}</div>
                            <div className="text-[11px] whitespace-nowrap overflow-hidden text-ellipsis">{agent.name}</div>
                        </div>
                    );
                })}
            </div>

            {/* Sidebar / Transparency Panel */}
            <div className="flex flex-col gap-[15px]">
                <div className="bg-[#0a0a0a] p-[15px] rounded-xl border border-[#1a1a1a] flex-1">
                    <h4 className="m-0 mb-2.5 text-xs text-[#666]">Config & Governance</h4>
                    {selectedAgent ? (
                        <div>
                            <p className="text-[11px] text-[#aaa]">Agent ID: <span className="text-[#00d4ff]">{selectedAgent.id}</span></p>
                            <div className="mt-2.5">
                                <label htmlFor="agent-inference-temp" className="text-[10px] block mb-1">Inference Temperature</label>
                                {/* Ledger cluster 3 — this slider was completely unbound (no value,
                                    no onChange): dragging it changed nothing anywhere. It now edits
                                    the selected agent's real params.temp. */}
                                <input
                                    id="agent-inference-temp"
                                    type="range"
                                    min={0}
                                    max={1}
                                    step={0.05}
                                    aria-label="Inference Temperature"
                                    title="Inference Temperature"
                                    className="w-full"
                                    value={selectedAgent.params?.temp ?? 0.7}
                                    onChange={e => {
                                        const temp = Number(e.target.value);
                                        setAgents(prev => prev.map(a =>
                                            a.id === selectedAgent.id
                                                ? { ...a, params: { ...a.params, temp } }
                                                : a));
                                    }}
                                />
                                <p className="text-[10px] text-[#aaa] mt-1">temp: {(selectedAgent.params?.temp ?? 0.7).toFixed(2)}</p>
                            </div>
                            <div className="mt-[15px] p-2.5 bg-[#111] rounded-md border-l-[3px] border-[#00ff00]">
                                <div className="text-[9px] text-[#00ff00] font-bold">GaaS COMPLIANT</div>
                                
                            </div>
                        </div>
                    ) : (
                        <p className="text-[11px] text-[#444] italic">Select a node to configure</p>
                    )}
                </div>

                <button
                    type="button"
                    onClick={exportBlueprint}
                    className="bg-[#00d4ff] text-black border-none p-3 rounded-lg font-bold cursor-pointer uppercase tracking-wider"
                >
                    Export Swarm Blueprint
                </button>
            </div>
        </div>
    );
};

const btnClass = (color: string) => {
    const colorClasses: Record<string, string> = {
        '#ff00ff': 'text-[#ff00ff] border-[#ff00ff]',
        '#00d4ff': 'text-[#00d4ff] border-[#00d4ff]',
        '#ffff00': 'text-[#ffff00] border-[#ffff00]',
    };
    return `bg-transparent border ${colorClasses[color] ?? 'text-white border-white'} px-2.5 py-1 rounded text-[10px] cursor-pointer font-bold`;
};

const typeClass = (type: string) => {
    switch (type) {
        case 'BRAIN': return 'text-[#ff00ff]';
        case 'IMMUNE': return 'text-[#00d4ff]';
        case 'TOOL': return 'text-[#ffff00]';
        default: return 'text-white';
    }
};

export default VisualAgentComposer;
