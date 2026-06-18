import React, { useState } from 'react';

const SwarmIntelligence: React.FC = () => {
    const [swarms] = useState([
        { id: 'swarm-8291', size: 12, fitness: 0.88, status: 'EVOLVING' },
        { id: 'swarm-1024', size: 8, fitness: 0.94, status: 'STABLE' }
    ]);

    const paretoPoints: { x: number; y: number }[] = [
        { x: 10, y: 0.95 }, { x: 25, y: 0.98 }, { x: 50, y: 0.99 }
    ];

    return (
        <div className="p-5 bg-[#050505] text-white rounded-2xl border border-[#1a1a1a]">
            <h2 className="text-fuchsia-500 text-lg font-bold uppercase mb-5">Swarm Intelligence Hub</h2>

            <div className="grid grid-cols-2 gap-5">
                {/* Swarm Leaderboard */}
                <div className="bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
                    <h3 className="text-xs text-[#666] mb-4 uppercase tracking-widest">Active Swarms</h3>
                    {swarms.map(s => (
                        <div
                            key={s.id}
                            className={`flex justify-between p-2.5 bg-[#111] mb-2 rounded-md border-l-[3px] ${
                                s.status === 'STABLE' ? 'border-green-400' : 'border-yellow-400'
                            }`}
                        >
                            <div>
                                <div className="text-xs font-bold">{s.id}</div>
                                <div className="text-[10px] text-[#666]">Size: {s.size} agents</div>
                            </div>
                            <div className="text-right">
                                <div className="text-xs text-[#00d4ff]">{(s.fitness * 100).toFixed(1)}% Fit</div>
                                <div className="text-[9px] text-[#444]">{s.status}</div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Pareto Frontier — SVG avoids inline styles */}
                <div className="bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
                    <h3 className="text-xs text-[#666] mb-4 uppercase tracking-widest">Pareto Frontier: Accuracy vs Latency</h3>
                    <svg viewBox="0 0 100 100" className="w-full h-[120px]" aria-label="Pareto frontier chart">
                        <line x1="0" y1="100" x2="100" y2="100" stroke="#333" strokeWidth="0.5" />
                        <line x1="0" y1="0" x2="0" y2="100" stroke="#333" strokeWidth="0.5" />
                        {paretoPoints.map((p, i) => (
                            <circle
                                key={i}
                                cx={p.x}
                                cy={100 - (p.y - 0.9) * 1000}
                                r="2.5"
                                fill="#ff00ff"
                                filter="url(#glow)"
                            />
                        ))}
                        <defs>
                            <filter id="glow">
                                <feGaussianBlur stdDeviation="1.5" result="blur" />
                                <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                            </filter>
                        </defs>
                        <text x="95" y="99" fontSize="5" fill="#444" textAnchor="end">Latency</text>
                        <text x="4" y="6" fontSize="5" fill="#444">Accuracy</text>
                    </svg>
                </div>
            </div>

            {/* Emergence Feed */}
            <div className="mt-5 bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
                <h3 className="text-xs text-[#666] mb-2.5 uppercase tracking-widest">Emergence Event Stream</h3>
                <div className="font-mono text-[10px] text-green-400 space-y-1">
                    <div>[14:22:01] LEADERSHIP_PATTERN: agent_alpha assumed coordination of swarm_8291.</div>
                    <div>[14:22:15] ALTRUISM_EXCHANGE: agent_beta shared 5.0 WST with agent_gamma.</div>
                    <div>[14:23:40] SPECIALISATION: agent_delta optimized for 'Law' domain tasks.</div>
                </div>
            </div>
        </div>
    );
};

export default SwarmIntelligence;
