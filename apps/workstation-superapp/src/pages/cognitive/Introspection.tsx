import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, Brain, Zap, Heart, Wind, Shield, Cpu, FlaskConical, Radio } from 'lucide-react';

interface Biometrics {
  circadian:      { cycle: string };
  cardiovascular: { resource_flow: number; peristaltic_delay: number };
  cognition:      { state: string; primary_drive: string };
  immune:         { health: number; threat_level: string; error_rate: number };
  metabolic:      { efficiency: number; atp_ratio: number; total_projects: number };
  nervous:        { arousal_state: string; signal_rate: number };
  communication:  { neurotransmitter: string; is_active: boolean };
}

const SEED: Biometrics = {
  circadian:      { cycle: 'ACTIVE_FOCUS' },
  cardiovascular: { resource_flow: 75, peristaltic_delay: 1.5 },
  cognition:      { state: 'STABLE', primary_drive: 'DISCOVERY' },
  immune:         { health: 0.98, threat_level: 'NONE', error_rate: 0 },
  metabolic:      { efficiency: 0.92, atp_ratio: 0.88, total_projects: 0 },
  nervous:        { arousal_state: 'RESTING', signal_rate: 0.0 },
  communication:  { neurotransmitter: 'Oxytocin', is_active: false },
};

export const Introspection: React.FC = () => {
  const [bio, setBio] = useState<Biometrics>(SEED);

  useEffect(() => {
    const load = () => {
      axios.get<Biometrics>('/api/v1/biometrics/status', { validateStatus: () => true })
        .then(res => { if (res.status === 200 && res.data) setBio(res.data); })
        .catch(() => {});
    };
    load();
    const t = setInterval(load, 10000);
    return () => clearInterval(t);
  }, []);

  // Map real biometrics to display values
  const vitals = {
    oxytocin:      bio.communication.neurotransmitter === 'Oxytocin'  ? 0.85 : 0.5,
    serotonin:     bio.communication.neurotransmitter === 'Serotonin' ? 0.88 : 0.55,
    dopamine:      bio.communication.neurotransmitter === 'Dopamine'  ? 0.82 : 0.6,
    system_health: bio.immune.health,
  };

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

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-12">
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
            Live Biometrics
          </h3>
          <div className="space-y-6">
             <LoadVisual label={`Metabolic (ATP ${(bio.metabolic.atp_ratio * 100).toFixed(0)}%)`} value={Math.round(bio.metabolic.efficiency * 100)} color="bg-aura" />
             <LoadVisual label={`Cardiovascular (Flow)`} value={Math.round(bio.cardiovascular.resource_flow)} color="bg-highlight" />
             <LoadVisual label={`Immune Health`} value={Math.round(bio.immune.health * 100)} color="bg-vital" />
          </div>
          <div className="grid grid-cols-2 gap-3 mt-4">
            {[
              { icon: Radio, label: 'Circadian', val: bio.circadian.cycle.replace('_', ' ') },
              { icon: Brain, label: 'Cognition', val: bio.cognition.state },
              { icon: Shield, label: 'Immune', val: bio.immune.threat_level },
              { icon: Cpu, label: 'Nervous', val: bio.nervous.arousal_state },
            ].map(({ icon: Icon, label, val }) => (
              <div key={label} className="flex items-center gap-2 bg-slate-900/40 rounded-xl px-3 py-2">
                <Icon size={12} className="text-slate-500 shrink-0" />
                <div>
                  <p className="text-[8px] font-black uppercase tracking-widest text-slate-600">{label}</p>
                  <p className="text-[10px] font-black text-white">{val}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const RESONANCE_COLORS: Record<string, { border: string; bg: string; text: string; solid: string }> = {
  '#64ffda': { border: 'border-aura',      bg: 'bg-aura/10',      text: 'text-aura',      solid: 'bg-aura' },
  '#ffd740': { border: 'border-highlight', bg: 'bg-highlight/10', text: 'text-highlight', solid: 'bg-highlight' },
  '#ff5252': { border: 'border-vital',     bg: 'bg-vital/10',     text: 'text-vital',     solid: 'bg-vital' },
};

const ResonanceBall = ({ label, value, color, icon: Icon }: any) => {
  const c = RESONANCE_COLORS[color] ?? RESONANCE_COLORS['#64ffda'];
  return (
    <div className="glass-card p-10 flex flex-col items-center group cursor-pointer overflow-hidden relative">
       <motion.div
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
          className={`w-20 h-20 rounded-full border-2 flex items-center justify-center mb-6 shadow-2xl relative z-10 ${c.border} ${c.bg}`}
       >
          <Icon size={32} className={c.text} />
       </motion.div>
       <p className="text-[10px] font-black uppercase text-slate-500 tracking-[0.3em] mb-2 z-10">{label} Resonance</p>
       <div className={`text-5xl font-black z-10 ${c.text}`}>{(value * 100).toFixed(1)}%</div>
       <div className="absolute inset-x-0 bottom-0 h-1 bg-white/5 overflow-hidden">
          <motion.div
             initial={{ width: 0 }}
             animate={{ width: `${value * 100}%` }}
             transition={{ duration: 2, ease: "easeOut" }}
             className={`h-full ${c.solid}`}
          />
       </div>
    </div>
  );
};

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
