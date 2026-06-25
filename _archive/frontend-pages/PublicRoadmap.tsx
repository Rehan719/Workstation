import React from 'react';
import { Map, Zap, Calendar, ArrowRight } from 'lucide-react';
import { useTheme } from '../theme/ThemeContext';
import { notImplemented } from '@workstation/ui';

export const PublicRoadmap: React.FC = () => {
  const { theme } = useTheme();

  return (
    <div className={`space-y-12 ${theme === 'advanced' ? 'animate-in fade-in slide-in-from-bottom-4 duration-1000' : ''}`} role="main" aria-label="Public Evolution Roadmap">
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
          theme={theme}
        />
        <PhaseCard
          phase="Phase 2: Symbiosis"
          status="In Progress"
          items={["Epigenetic Voting", "Digital Twins", "L0 Homeostasis"]}
          color="text-aura"
          theme={theme}
        />
        <PhaseCard
          phase="Phase 3: Civilization"
          status="Planned"
          items={["Real-world Federation", "Economic Integration", "PQC Migration"]}
          color="text-highlight"
          theme={theme}
        />
      </div>

      <div className={`p-8 rounded-3xl border transition-all duration-700 ${
        theme === 'advanced' ? 'bg-sovereign border-aura/30 shadow-[0_0_30px_rgba(100,255,218,0.05)]' : 'bg-slate-900/40 border-slate-800'
      }`}>
         <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
           <Zap size={20} className="text-aura" />
           Top Community Priorities
         </h3>
         <div className="space-y-4">
            <PriorityItem title="Mobile Biometric Auth" votes={1240} theme={theme} />
            <PriorityItem title="Stripe/Crypto Checkout" votes={850} theme={theme} />
            <PriorityItem title="Kyber-768 Integration" votes={420} theme={theme} />
         </div>
      </div>
    </div>
  );
};

const PhaseCard = ({ phase, status, items, color, theme }: any) => (
  <div className={`p-8 rounded-3xl border transition-all duration-700 backdrop-blur-sm ${
    theme === 'advanced' ? 'bg-sovereign border-aura/30 shadow-[0_0_20px_rgba(100,255,218,0.05)]' : 'bg-slate-900/40 border-slate-800'
  }`}>
    <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded border mb-4 inline-block ${color} ${
      theme === 'advanced' ? 'bg-sovereign border-aura/20 shadow-[0_0_10px_rgba(100,255,218,0.1)]' : 'bg-slate-800 border-slate-700'
    }`}>{status}</span>
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

const PriorityItem = ({ title, votes, theme }: any) => (
  <div className={`flex items-center justify-between p-4 rounded-xl border transition-all ${
    theme === 'advanced' ? 'bg-sovereign border-aura/20 hover:border-aura/50' : 'bg-slate-800/30 border-slate-700/50'
  }`}>
    <span className="font-bold text-sm">{title}</span>
    <div className="flex items-center gap-4">
       <span className="text-xs font-black text-aura uppercase tracking-widest">{votes} Resonance</span>
       <button type="button" onClick={() => notImplemented('This action')}
         className={`p-2 rounded-lg transition-all ${
           theme === 'advanced' ? 'bg-aura/10 text-aura hover:bg-aura hover:text-sovereign' : 'bg-slate-700 text-white hover:bg-aura hover:text-sovereign'
         }`}
         aria-label={`Vote for ${title}`}
       >
         <ArrowRight size={16} />
       </button>
    </div>
  </div>
);
