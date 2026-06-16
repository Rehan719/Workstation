import React, { useState, useEffect } from 'react';

const AGENT_COUNT = 5;
const TWO_PI = Math.PI * 2;

const HolographicForge: React.FC = () => {
    const [tick, setTick] = useState(0);

    useEffect(() => {
        const id = setInterval(() => setTick(t => (t + 1) % 360), 50);
        return () => clearInterval(id);
    }, []);

    const cx = 140;
    const cy = 130;
    const orbitR = 80;

    const agents = Array.from({ length: AGENT_COUNT }, (_, i) => {
        const angle = (TWO_PI * i) / AGENT_COUNT + (tick * Math.PI) / 180;
        return { x: cx + Math.cos(angle) * orbitR, y: cy + Math.sin(angle) * orbitR * 0.45 };
    });

    const meshPoints = Array.from({ length: 6 }, (_, i) => {
        const a = (TWO_PI * i) / 6;
        return { x: cx + Math.cos(a) * 50, y: cy + Math.sin(a) * 25 };
    });

    return (
        <div className="p-5 bg-black/90 text-white rounded-xl border border-fuchsia-500/60">
            <div className="mb-4">
                <h2 className="text-xs font-black uppercase tracking-widest text-fuchsia-400 [text-shadow:0_0_10px_#d946ef]">
                    Holographic Agent Forge (L13)
                </h2>
                <p className="text-[10px] text-slate-500 mt-1 font-bold">3D Immersive Swarm Composition Active</p>
            </div>

            <div className="w-full h-64 bg-black rounded-lg overflow-hidden flex items-center justify-center border border-slate-900">
                <svg width="280" height="260">
                    {/* Icosahedron wireframe approximation */}
                    {meshPoints.map((p, i) => {
                        const next = meshPoints[(i + 1) % meshPoints.length];
                        const opp = meshPoints[(i + 3) % meshPoints.length];
                        return (
                            <g key={i} opacity="0.4">
                                <line x1={p.x} y1={p.y} x2={next.x} y2={next.y} stroke="#00ff00" strokeWidth="0.8" />
                                <line x1={p.x} y1={p.y} x2={cx} y2={cy} stroke="#00ff00" strokeWidth="0.5" />
                                <line x1={p.x} y1={p.y} x2={opp.x} y2={opp.y} stroke="#00ff00" strokeWidth="0.4" />
                            </g>
                        );
                    })}

                    {/* Orbiting agent nodes */}
                    {agents.map((a, i) => (
                        <g key={i}>
                            <circle cx={a.x} cy={a.y} r="5" fill="#22d3ee" opacity="0.9" />
                            <circle cx={a.x} cy={a.y} r="9" fill="none" stroke="#22d3ee" strokeWidth="0.5" opacity="0.3" />
                        </g>
                    ))}

                    {/* Core nucleus */}
                    <circle cx={cx} cy={cy} r="8" fill="#00ff00" opacity="0.7" />
                    <circle cx={cx} cy={cy} r="14" fill="none" stroke="#00ff00" strokeWidth="1" opacity="0.3" />
                    <circle cx={cx} cy={cy} r="22" fill="none" stroke="#00ff00" strokeWidth="0.5" opacity="0.15" />

                    <text x={cx} y={cy + 40} textAnchor="middle" fill="#94a3b8" fontSize="8" fontFamily="monospace">
                        SOVEREIGN MESH CORE
                    </text>
                </svg>
            </div>

            <div className="mt-4 flex gap-2.5">
                <button
                    type="button"
                    className="bg-slate-900 text-fuchsia-400 border border-fuchsia-500 px-4 py-1.5 rounded text-[10px] font-black uppercase tracking-widest hover:bg-fuchsia-500/10 transition-colors"
                >
                    INFUSE QUALIA
                </button>
                <button
                    type="button"
                    className="bg-fuchsia-500 text-white px-4 py-1.5 rounded text-[10px] font-black uppercase tracking-widest hover:bg-fuchsia-400 transition-colors"
                >
                    PROJECT SWARM
                </button>
            </div>
        </div>
    );
};

export default HolographicForge;
