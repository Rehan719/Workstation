import React from 'react';
import { Map, Zap, Calendar, ArrowRight } from 'lucide-react';

export const PublicRoadmap: React.FC = () => {
  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-black mb-2">Public Evolution Roadmap</h1>
        <p className="text-slate-500">Autonomous trajectory of the Workstation civilization, shaped by Guardian resonance.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <PhaseCard
          phase="Phase 1: Convergence"
          status="Completed"
          items={["Cognitive Dashboards", "BTO Wizard", "Live Vitals"]}
          color="text-vital"
        />
        <PhaseCard
          phase="Phase 2: Symbiosis"
          status="In Progress"
          items={["Epigenetic Voting", "Digital Twins", "L0 Homeostasis"]}
          color="text-aura"
        />
        <PhaseCard
          phase="Phase 3: Civilization"
          status="Planned"
          items={["Real-world Federation", "Economic Integration", "PQC Migration"]}
          color="text-highlight"
        />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
         <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
           <Zap size={20} className="text-aura" />
           Top Community Priorities
         </h3>
         <div className="space-y-4">
            <PriorityItem title="Mobile Biometric Auth" votes={1240} />
            <PriorityItem title="Stripe/Crypto Checkout" votes={850} />
            <PriorityItem title="Kyber-768 Integration" votes={420} />
         </div>
      </div>
    </div>
  );
};

const PhaseCard = ({ phase, status, items, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded bg-slate-800 border border-slate-700 mb-4 inline-block ${color}`}>{status}</span>
    <h3 className="text-xl font-bold mb-4">{phase}</h3>
    <ul className="space-y-2">
      {items.map((item: string) => (
        <li key={item} className="text-xs text-slate-400 flex items-center gap-2">
           <div className="w-1 h-1 rounded-full bg-slate-600"></div>
           {item}
        </li>
      ))}
    </ul>
  </div>
);

const PriorityItem = ({ title, votes }: any) => (
  <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50">
    <span className="font-bold text-sm">{title}</span>
    <div className="flex items-center gap-4">
       <span className="text-xs font-black text-aura uppercase">{votes} Resonance</span>
       <button className="p-2 bg-slate-700 rounded-lg hover:bg-aura hover:text-sovereign transition-all">
         <ArrowRight size={16} />
       </button>
    </div>
  </div>
);
