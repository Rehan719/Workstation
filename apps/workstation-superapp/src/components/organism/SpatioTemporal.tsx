import React, { useState, useEffect } from 'react';

// §L14 (W496, FU-112) — THIS PANEL IS A DRAWING, AND IT USED TO CLAIM OTHERWISE. It is reached from
// every page (Shell → FourthColumn → CommandCenter tiled), and under an "illustrative" header it
// printed two statements as though they were readings: a fixed offset presented as a relative clock
// for another planet, and a consensus status asserting that a cross-planetary sync was ACTIVE. There
// is no such sync, no second site, and nothing here reads any data — the only live value on the panel
// is this browser's own clock, advanced by the time-scale slider. The curve is a static SVG path.
// What is drawn is now labelled as drawn, and the two claims are gone rather than dressed in a
// caveat: a header saying "illustrative" does not make a sentence below it true.
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
                <h2 className="text-xs font-black uppercase tracking-widest text-cyan-400">
                    4D Spatio-Temporal Dashboard (L14) — a drawing: nothing here reads any data
                </h2>
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
                <svg width="100%" height="100%" aria-label="An illustrative curve. It is a fixed path, not a plot of any measurement.">
                    <path d="M0 75 Q 100 20, 200 75 T 400 75" fill="none" stroke="#00d4ff" strokeWidth="2" strokeDasharray="10,5" />
                    <circle cx="200" cy="75" r="5" fill="#fff" />
                    <text x="210" y="70" fill="#fff" fontSize="8">Illustrative curve — not plotted from data</text>
                </svg>
            </div>

            <div className="mt-5 text-xs font-mono">
                <div className="flex justify-between text-slate-600">
                    <span>Browser clock, scaled ×{timeScale}: {new Date(currentTime).toISOString()}</span>
                    <span data-testid="spatio-clock-basis">the only live value on this panel</span>
                </div>
                <div className="mt-2.5 text-slate-500 font-black text-[10px] uppercase tracking-widest"
                     data-testid="spatio-basis">
                    No distributed sync exists and no second site is connected — this panel reports nothing
                </div>
            </div>
        </div>
    );
};

export default SpatioTemporal;
