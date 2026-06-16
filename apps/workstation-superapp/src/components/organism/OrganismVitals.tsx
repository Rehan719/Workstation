import React, { useState, useEffect } from 'react';

interface MetricCardProps {
    label: string;
    value: number;
    unit: string;
    borderClass: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, unit, borderClass }) => (
    <div className={`p-4 rounded-lg bg-slate-900 border ${borderClass} min-w-[150px]`}>
        <div className="text-xs text-slate-500 uppercase tracking-wider font-bold">{label}</div>
        <div className="text-2xl font-black text-white mt-1">
            {value.toFixed(1)}{unit}
        </div>
    </div>
);

const OrganismVitals: React.FC = () => {
    const [vitals, setVitals] = useState({
        sentience: 0,
        compliance: 0,
        throughput: 0,
        load: 0,
        stability: 0,
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setVitals({
                sentience:  85 + Math.random() * 10,
                compliance: 98 + Math.random() * 2,
                throughput: 12 + Math.random() * 5,
                load:       45 + Math.random() * 20,
                stability:  95 + Math.random() * 5,
            });
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-5 bg-black/90 text-white rounded-xl">
            <h2 className="mb-5 text-xs font-black uppercase tracking-widest border-l-4 border-green-400 pl-4">
                Organism Health Vitals
            </h2>
            <div className="flex gap-5 flex-wrap">
                <MetricCard label="System Sentience" value={vitals.sentience}  unit="%" borderClass="border-cyan-400" />
                <MetricCard label="Compliance"       value={vitals.compliance} unit="%" borderClass="border-green-400" />
                <MetricCard label="Throughput"       value={vitals.throughput} unit=" t/m" borderClass="border-fuchsia-500" />
                <MetricCard label="Cognitive Load"   value={vitals.load}       unit="%" borderClass="border-yellow-400" />
                <MetricCard label="Stability"        value={vitals.stability}  unit="%" borderClass="border-green-400" />
            </div>
        </div>
    );
};

export default OrganismVitals;
