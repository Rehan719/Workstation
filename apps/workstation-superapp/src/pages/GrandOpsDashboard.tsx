import React, { useState, useEffect } from 'react';

const GrandOpsDashboard: React.FC = () => {
    const [view, setView] = useState<'effectiveness' | 'constitutional' | 'workstation' | 'biomimetic'>('effectiveness');
    const [metrics, setMetrics] = useState<any>(null);

    useEffect(() => {
        setMetrics({
            injection_success: 99.95,
            compliance_rate: 100,
            learning_convergence: 0.98,
            p0_violations: 0,
            active_resilience_fallback: 2,
            parallel_speedup: '3.4x',
            immune_memory_size: 14,
            ceo_alignment: '95%'
        });
    }, []);

    const tabs = [
        { id: 'effectiveness',  label: 'Effectiveness' },
        { id: 'constitutional', label: 'Constitutional Health' },
        { id: 'workstation',    label: 'Workstation Orchestration' },
        { id: 'biomimetic',     label: 'Biomimetic Metrics' },
    ] as const;

    return (
        <div className="p-5 font-sans bg-gray-100 min-h-screen">
            <h1 className="text-[#1a3353] text-2xl font-black mb-5">
                Veritas v4.0 – Constitutional Octo-Veritas Command Center
            </h1>

            <div className="flex gap-2.5 mb-5">
                {tabs.map(t => (
                    <button
                        key={t.id}
                        type="button"
                        onClick={() => setView(t.id)}
                        className={`px-5 py-2.5 rounded border border-[#1a3353] font-bold transition-colors ${
                            view === t.id
                                ? 'bg-[#1a3353] text-white'
                                : 'bg-white text-[#1a3353] hover:bg-gray-50'
                        }`}
                    >
                        {t.label}
                    </button>
                ))}
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm">
                {view === 'effectiveness'  && <EffectivenessView  m={metrics} />}
                {view === 'constitutional' && <ConstitutionalView m={metrics} />}
                {view === 'workstation'    && <WorkstationView    m={metrics} />}
                {view === 'biomimetic'     && <BiometricView      m={metrics} />}
            </div>
        </div>
    );
};

const EffectivenessView = ({ m }: { m: any }) => (
    <div>
        <h2 className="text-xl font-black mb-4">Operational Effectiveness (Truth IX)</h2>
        <div className="flex gap-5">
            <StatCard label="Injection Success"       value={`${m?.injection_success}%`} color="text-green-600" />
            <StatCard label="Learning Convergence"    value={m?.learning_convergence}     color="text-purple-600" />
            <StatCard label="CEO Strategic Alignment" value={m?.ceo_alignment}            color="text-[#1a3353]" />
        </div>
    </div>
);

const ConstitutionalView = ({ m }: { m: any }) => (
    <div>
        <h2 className="text-xl font-black mb-4">Constitutional Health (Articles 1–1095)</h2>
        <div className="flex gap-5 mb-6">
            <StatCard label="P0 Compliance"    value="100%"              color="text-blue-600" />
            <StatCard label="Active Violations" value={m?.p0_violations} color={m?.p0_violations > 0 ? 'text-red-600' : 'text-green-600'} />
            <StatCard label="Escalation Events" value="0"                color="text-green-600" />
        </div>
        <h3 className="font-black text-lg mb-2">Priority Article Enforcement</h3>
        <ul className="space-y-1 text-sm text-gray-700 list-disc pl-5">
            <li>Article 42 (Data Sovereignty): ACTIVE - 100% Pass</li>
            <li>Article 78 (Accessibility): ACTIVE - 100% Pass</li>
            <li>Article 101 (Audit Logging): ACTIVE - 100% Pass</li>
            <li>Article 1095 (Sovereign Synthesis): ACTIVE - CEO Approved</li>
        </ul>
    </div>
);

const WorkstationView = ({ m: _m }: { m: any }) => (
    <div>
        <h2 className="text-xl font-black mb-4">Workstation Orchestration (C-Suite &amp; CoEs)</h2>
        <div className="grid grid-cols-2 gap-8">
            <div>
                <h3 className="font-black text-lg mb-2">C-Suite Preference Weights</h3>
                <ul className="space-y-1 text-sm text-gray-700 list-disc pl-5">
                    <li>CFO (Cost): 0.8</li>
                    <li>CMO (Engagement): 1.0</li>
                    <li>CTO (Reliability): 0.7</li>
                    <li>CHO (Ethics): 0.95</li>
                </ul>
            </div>
            <div>
                <h3 className="font-black text-lg mb-2">CoE Gatekeeping Status</h3>
                <ul className="space-y-1 text-sm list-disc pl-5">
                    <li>AI Ethics CoE: <span className="text-green-600 font-bold">APPROVED</span></li>
                    <li>Security CoE: <span className="text-green-600 font-bold">APPROVED</span></li>
                    <li>UX CoE: <span className="text-green-600 font-bold">APPROVED</span></li>
                    <li>DevOps CoE: <span className="text-green-600 font-bold">MONITORING</span></li>
                </ul>
            </div>
        </div>
    </div>
);

const BiometricView = ({ m }: { m: any }) => (
    <div>
        <h2 className="text-xl font-black mb-4">Biomimetic Resilience &amp; Efficiency</h2>
        <div className="flex gap-5 mb-4">
            <StatCard label="Mycelial Fallbacks"   value={m?.active_resilience_fallback} color="text-orange-600" />
            <StatCard label="Ant Parallelization"  value={m?.parallel_speedup}           color="text-blue-600" />
            <StatCard label="Immune Pathogens"     value={m?.immune_memory_size}         color="text-amber-800" />
        </div>
        <p className="text-sm text-gray-600 italic">
            System is self-healing. Proactive fallback enabled for known PDF failure signatures.
        </p>
    </div>
);

const StatCard = ({ label, value, color }: { label: string; value: any; color: string }) => (
    <div className="border border-gray-200 rounded-lg p-5 flex-1 text-center">
        <h4 className="text-sm font-bold text-gray-500 mb-2">{label}</h4>
        <p className={`text-3xl font-black ${color}`}>{value}</p>
    </div>
);

export default GrandOpsDashboard;
