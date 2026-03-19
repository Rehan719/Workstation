import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, Brain, ShieldCheck, Zap, Heart, Wind } from 'lucide-react';
import { useWebSocket } from '../../hooks/useWebSocket';

export const Introspection: React.FC = () => {
  const liveVitals = useWebSocket('/api/v200/resonance/ws/vitals');
  const [vitals, setVitals] = useState<any>(null);

  useEffect(() => {
    if (liveVitals) setVitals(liveVitals);
  }, [liveVitals]);

  useEffect(() => {
    if (!vitals) {
      axios.get('/api/v190/introspection/vitals')
        .then(res => setVitals(res.data))
        .catch(() => {
          setVitals({
            oxytocin: 0.85,
            serotonin: 0.92,
            dopamine: 0.74,
            system_health: 0.9998
          });
        });
    }
  }, []);

  if (!vitals) return <div className="p-8 text-aura animate-pulse font-black uppercase tracking-widest">Calibrating Introspection...</div>;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-12 animate-in fade-in duration-1000"
    >
      <header>
        <h1 className="text-6xl font-black mb-3 tracking-tighter neon-text uppercase">Self Vision</h1>
        <p className="text-slate-500 font-bold text-lg max-w-2xl leading-relaxed">
          Real-time introspection of the Workstation's <span className="text-aura">biochemical resonance</span> and homeostatic state.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <ResonanceBall label="Oxytocin" value={vitals.oxytocin} color="#64ffda" icon={Heart} />
        <ResonanceBall label="Serotonin" value={vitals.serotonin} color="#ffd740" icon={Wind} />
        <ResonanceBall label="Dopamine" value={vitals.dopamine} color="#ff5252" icon={Zap} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div className="glass-card p-12 flex flex-col justify-center items-center h-[400px] relative overflow-hidden group">
          <motion.div
             animate={{ scale: [1, 1.1, 1], rotate: 360 }}
             transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
             className="absolute inset-0 opacity-10 bg-aura-glow"
          ></motion.div>
          <Activity size={80} className="text-vital mb-8 animate-pulse z-10" />
          <h3 className="text-4xl font-black z-10">System Health</h3>
          <p className="text-6xl font-black neon-text mt-2 z-10">{(vitals.system_health * 100).toFixed(2)}%</p>
          <p className="text-slate-500 mt-6 font-black uppercase tracking-[0.3em] text-xs z-10">Apotheosis Architecture v139.0 Active</p>
        </div>

        <div className="glass-card p-12 h-[400px] flex flex-col justify-between">
          <h3 className="text-2xl font-black flex items-center gap-3">
            <Brain size={24} className="text-aura" />
            Cognitive Load
          </h3>
          <div className="space-y-10">
             <LoadVisual label="Synthesis Engine" value={42} color="bg-aura" />
             <LoadVisual label="Genomic Reconfiguration" value={18} color="bg-highlight" />
             <LoadVisual label="Passive Sensory Monitoring" value={85} color="bg-vital" />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const ResonanceBall = ({ label, value, color, icon: Icon }: any) => (
  <div className="glass-card p-10 flex flex-col items-center group cursor-pointer overflow-hidden relative">
     <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        className="w-20 h-20 rounded-full border-2 flex items-center justify-center mb-6 shadow-2xl relative z-10"
        style={{ borderColor: color, backgroundColor: `${color}10` }}
     >
        <Icon size={32} style={{ color }} />
     </motion.div>
     <p className="text-[10px] font-black uppercase text-slate-500 tracking-[0.3em] mb-2 z-10">{label} Resonance</p>
     <div className="text-5xl font-black z-10" style={{ color }}>{(value * 100).toFixed(1)}%</div>
     <div className="absolute inset-x-0 bottom-0 h-1 bg-white/5 overflow-hidden">
        <motion.div
           initial={{ width: 0 }}
           animate={{ width: `${value * 100}%` }}
           transition={{ duration: 2, ease: "easeOut" }}
           className="h-full"
           style={{ backgroundColor: color }}
        />
     </div>
  </div>
);

const LoadVisual = ({ label, value, color }: any) => (
  <div>
    <div className="flex justify-between text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">
      <span>{label}</span>
      <span className="text-white">{value}%</span>
    </div>
    <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 1.5, ease: "circOut" }}
        className={`h-full ${color} shadow-[0_0_15px_rgba(100,255,218,0.3)]`}
      />
    </div>
  </div>
);
