import React from 'react';
import { motion } from 'framer-motion';
import { FlaskConical, Activity, Database, Users, Cpu, Star } from 'lucide-react';

export const ScienceHub: React.FC = () => {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-vital/20 rounded-2xl text-vital shadow-[0_0_20px_rgba(255,82,82,0.2)]">
            <FlaskConical size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-vital">Science & Research</h1>
            <p className="text-slate-500 font-bold text-lg mt-2">Planetary research, discovery, and experiment simulation.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <HubCard
          title="Science Reactor"
          description="Discovery pipeline integrated with arXiv and research data."
          icon={Cpu}
          action="Launch Engine"
        />
        <HubCard
          title="Experiment Simulator"
          description="Simulate chemical, physical, and neural hypotheses."
          icon={Activity}
          action="Simulate"
        />
        <HubCard
          title="Research Hub"
          description="Global data collaboration and collective hypothesis building."
          icon={Database}
          action="Join Research"
        />
      </div>

      <section className="p-12 glass-card flex items-center justify-between gap-12 border-vital/30 bg-vital/5">
        <div className="flex-1">
          <h3 className="text-2xl font-black mb-4">Planetary Knowledge Synthesis</h3>
          <p className="text-slate-400 font-bold leading-relaxed mb-8">
            The Science Reactor is currently analyzing **32.4 million research papers** across 147 planetary nodes. Join a discovery swarm to contribute.
          </p>
          <button className="px-8 py-3 bg-vital text-white font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-vital/20 uppercase tracking-widest text-sm">Contribute Data</button>
        </div>
        <div className="w-64 h-64 bg-sovereign rounded-full border-4 border-vital/20 border-t-vital animate-spin-slow flex items-center justify-center shadow-[0_0_50px_rgba(255,82,82,0.2)]">
           <FlaskConical size={48} className="text-vital" />
        </div>
      </section>
    </motion.div>
  );
};

const HubCard = ({ title, description, icon: Icon, action }: any) => (
  <div className="p-8 glass-card group border-white/5 hover:border-vital/30">
    <div className="w-12 h-12 rounded-xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-vital group-hover:text-white transition-all">
      <Icon size={24} />
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-xs text-slate-500 font-bold mb-6">{description}</p>
    <button className="text-xs font-black uppercase text-vital tracking-widest hover:underline">{action}</button>
  </div>
);
