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
        <div className="p-5 bg-black/90 text-white rounded-xl border border-cyan-400/60">
            <div className="flex justify-between items-center mb-5">
                <h2 className="text-xs font-black uppercase tracking-widest text-cyan-400">4D Spatio-Temporal Dashboard (L14)</h2>
                <div className="flex items-center gap-3">
                    <label htmlFor="time-scale" className="text-[10px] uppercase tracking-widest text-slate-500 font-black">
                        Time Scale
                    </label>
                    <input
                        id="time-scale"
                        type="range"
                        min="1"
                        max="100"
                        value={timeScale}
                        onChange={(e) => setTimeScale(parseInt(e.target.value))}
                        className="accent-cyan-400 w-24"
                    />
                </div>
            </div>

            <div className="relative h-36 border border-slate-900 bg-gradient-to-b from-black to-slate-950 rounded-lg overflow-hidden">
                <svg width="100%" height="100%">
                    <path d="M0 75 Q 100 20, 200 75 T 400 75" fill="none" stroke="#00d4ff" strokeWidth="2" strokeDasharray="10,5" />
                    <circle cx="200" cy="75" r="5" fill="#fff" />
                    <text x="210" y="70" fill="#fff" fontSize="8">Current Reality</text>
                </svg>
            </div>

            <div className="mt-5 text-xs font-mono">
                <div className="flex justify-between text-slate-600">
                    <span>Earth Baseline: {new Date(currentTime).toISOString()}</span>
                    <span>Mars Relative: T + 842s</span>
                </div>
                <div className="mt-2.5 text-cyan-400 font-black text-[10px] uppercase tracking-widest">
                    Sovereign Consensus Status: CROSS-PLANETARY SYNC ACTIVE
                </div>
            </div>
        </div>
    );
};

export default SpatioTemporal;
