import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, Brain, ShieldCheck, Zap } from 'lucide-react';
import { useWebSocket } from '../../hooks/useWebSocket';

export const Introspection: React.FC = () => {
  const liveVitals = useWebSocket('/api/v200/resonance/ws/vitals');
  const [vitals, setVitals] = useState<any>(null);

  useEffect(() => {
    if (liveVitals) setVitals(liveVitals);
  }, [liveVitals]);

  useEffect(() => {
    if (!vitals) {
      axios.get('/api/v190/introspection/vitals').then(res => setVitals(res.data));
    }
  }, []);

  if (!vitals) return <div className="p-8 text-slate-500 animate-pulse">Initializing Introspection...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Self Vision</h1>
        <p className="text-slate-500">Real-time introspection of the Workstation's vital signs and biochemical resonance.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <VitalCard label="Oxytocin" value={vitals.oxytocin} color="text-emerald-400" />
        <VitalCard label="Serotonin" value={vitals.serotonin} color="text-amber-400" />
        <VitalCard label="Dopamine" value={vitals.dopamine} color="text-aura" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 flex flex-col justify-center items-center h-80">
          <Activity size={64} className="text-vital mb-6 animate-pulse" />
          <h3 className="text-2xl font-black">System Health: {(vitals.system_health * 100).toFixed(2)}%</h3>
          <p className="text-slate-500 mt-2 font-bold uppercase tracking-widest text-xs">Apotheosis v139.0 Active</p>
        </div>

        <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-80">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Brain size={20} className="text-aura" />
            Cognitive Load
          </h3>
          <div className="space-y-6">
             <LoadBar label="Synthesis Engine" value={42} />
             <LoadBar label="Genomic Reconfiguration" value={18} />
             <LoadBar label="Passive Sensory Monitoring" value={85} />
          </div>
        </div>
      </div>
    </div>
  );
};

const VitalCard = ({ label, value, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2">{label} Resonance</p>
    <div className={`text-5xl font-black ${color}`}>{(value * 100).toFixed(1)}%</div>
    <div className="mt-4 h-1 w-full bg-slate-800 rounded-full overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${value * 100}%` }}
        className={`h-full ${color.replace('text', 'bg')}`}
      />
    </div>
  </div>
);

const LoadBar = ({ label, value }: any) => (
  <div>
    <div className="flex justify-between text-[10px] font-black uppercase text-slate-500 mb-2">
      <span>{label}</span>
      <span>{value}%</span>
    </div>
    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full bg-aura" style={{ width: `${value}%` }}></div>
    </div>
  </div>
);
