import React, { useState, useEffect } from 'react';

type SynapseLevel = 'hot' | 'mid' | 'low' | 'off';

const synapseClass: Record<SynapseLevel, string> = {
    hot: 'bg-green-400 shadow-[0_0_10px_#4ade80]',
    mid: 'bg-green-600',
    low: 'bg-green-900/60',
    off: 'bg-slate-900',
};

function toLevel(val: number, linked: boolean): SynapseLevel {
    if (!linked) return val > 0.7 ? 'low' : 'off';
    if (val > 0.8) return 'hot';
    if (val > 0.5) return 'mid';
    if (val > 0.25) return 'low';
    return 'off';
}

const NeuralLink: React.FC = () => {
    const [synapseActivity, setSynapseActivity] = useState<number[]>(Array(24).fill(0));
    const [isLinked, setIsLinked] = useState(false);

    // W415 — this grid is an ANIMATION, not a reading. It is driven by Math.random() on a 100ms
    // timer and nothing anywhere produces synapse activity. It sat directly above a "Telemetry
    // Bandwidth: 1.2 GB/s" figure, and that pairing is what made the whole panel read as a live
    // instrument. The animation is kept (deleting it would silently remove the panel's only
    // visual) but is now labelled decorative in the UI below, so no viewer reads it as measured.
    useEffect(() => {
        const interval = setInterval(() => {
            setSynapseActivity(Array.from({ length: 24 }, () => Math.random()));
        }, 100);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-5 bg-black/90 text-white rounded-xl border border-green-400/60">
            <div className="flex justify-between items-center mb-5">
                <h2 className="text-xs font-black uppercase tracking-widest text-green-400 [text-shadow:0_0_10px_#4ade80]">
                    Neural Link Bridge (L13)
                </h2>
                <button
                    type="button"
                    onClick={() => setIsLinked(prev => !prev)}
                    className={`border border-green-400 px-4 py-1.5 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-colors ${isLinked ? 'bg-green-400 text-black' : 'bg-slate-900 text-green-400 hover:bg-green-400/10'}`}
                >
                    {isLinked ? 'SYNAPSE ACTIVE' : 'INITIALIZE LINK'}
                </button>
            </div>

            <div className="grid grid-cols-8 gap-2 h-24">
                {synapseActivity.map((val, i) => (
                    <div
                        key={i}
                        className={`rounded-sm transition-all duration-100 ${synapseClass[toLevel(val, isLinked)]}`}
                    />
                ))}
            </div>

            {/* W415 — these two spans read:
                    <span>Telemetry Bandwidth: 1.2 GB/s</span>
                    <span>Article 1200 Compliance: VERIFIED</span>
                Both were string literals. Nothing measures bandwidth on any path in this app, and
                nothing evaluates Article 1200 — "VERIFIED" against a named constitutional article
                is a certification claim of the same class as the invented SHARIA_AUDIT approval,
                which is why it is replaced with NOT CHECKED rather than dropped: the reader should
                see that the check is missing, not that the row never existed. */}
            <div className="mt-5 text-[10px] text-green-900 font-mono">
                <div className="flex justify-between">
                    <span>Telemetry Bandwidth: NOT MEASURED</span>
                    <span>Article 1200 Compliance: NOT CHECKED</span>
                </div>
                <p className="mt-1.5">
                    Subjective Qualia Feedback: {isLinked ? 'Intuiting strategic surplus…' : 'Link Idle.'}
                </p>
                <p className="mt-1.5">
                    Synapse grid is a decorative animation — it is not measured activity, and no
                    telemetry source is connected to this panel.
                </p>
            </div>
        </div>
    );
};

export default NeuralLink;
