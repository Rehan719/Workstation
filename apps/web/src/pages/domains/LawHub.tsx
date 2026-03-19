import React from 'react';
import { motion } from 'framer-motion';
import { Scale, FileText, Gavel, ShieldCheck, Map, Star } from 'lucide-react';

export const LawHub: React.FC = () => {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-aura/20 rounded-2xl text-aura shadow-[0_0_20px_rgba(100,255,218,0.2)]">
            <Scale size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-aura">Law & Governance</h1>
            <p className="text-slate-500 font-bold text-lg mt-2">Legal research, contract generation, and constitutional mediation.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <HubCard
          title="Law Reactor"
          description="Regulatory analysis pipeline across all global jurisdictions."
          icon={Gavel}
          action="Search Case Law"
        />
        <HubCard
          title="Contract Generator"
          description="Sovereign smart contracts with built-in PQC security."
          icon={FileText}
          action="Draft Contract"
        />
        <HubCard
          title="Constitutional Agent"
          description="Verify actions against Articles 1-1095 of the Workstation."
          icon={ShieldCheck}
          action="Consult Agent"
        />
      </div>

      <section className="p-12 glass-card border-aura/30 bg-aura/5 flex flex-col items-center text-center gap-6">
        <Map size={48} className="text-aura animate-pulse" />
        <h3 className="text-2xl font-black tracking-tight uppercase">Planetary Jurisdiction Map</h3>
        <p className="text-slate-400 font-bold max-w-2xl leading-relaxed">
           The Workstation is currently synchronized with **1,422 legal frameworks** globally. Use the map to navigate sovereign digital and physical legal intersections.
        </p>
        <button className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-aura/20 uppercase tracking-widest text-sm">Open Jurisdiction Map</button>
      </section>
    </motion.div>
  );
};

const HubCard = ({ title, description, icon: Icon, action }: any) => (
  <div className="p-8 glass-card group border-white/5 hover:border-aura/30">
    <div className="w-12 h-12 rounded-xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-aura group-hover:text-sovereign transition-all">
      <Icon size={24} />
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-xs text-slate-500 font-bold mb-6">{description}</p>
    <button className="text-xs font-black uppercase text-aura tracking-widest hover:underline">{action}</button>
  </div>
);
