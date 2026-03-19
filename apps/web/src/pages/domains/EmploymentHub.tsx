import React from 'react';
import { motion } from 'framer-motion';
import { Briefcase, BriefcaseIcon, Search, Rocket, Star, TrendingUp, Users } from 'lucide-react';

export const EmploymentHub: React.FC = () => {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-highlight/20 rounded-2xl text-highlight shadow-[0_0_20px_rgba(255,215,64,0.2)]">
            <Briefcase size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-highlight">Employment & Enterprise</h1>
            <p className="text-slate-500 font-bold text-lg mt-2">Career assessment, skill-building, and VSB business simulation.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <HubCard
          title="Employment Reactor"
          description="Career matching and skill-building pathways."
          icon={Search}
          action="Find Matches"
        />
        <HubCard
          title="VSB Simulator"
          description="Launch a micro-business with the AI CEO's strategy."
          icon={Rocket}
          action="Start Business"
        />
        <HubCard
          title="Enterprise Network"
          description="Global marketplace for VSB trade and alliances."
          icon={Users}
          action="Browse Network"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="p-10 glass-card">
          <h3 className="text-2xl font-black mb-6">Market Trends</h3>
          <div className="space-y-6">
            {[
              { label: 'Neural Engineering', trend: '+42%', color: 'text-aura' },
              { label: 'Sovereign Law', trend: '+18%', color: 'text-vital' },
              { label: 'Bio-Computing', trend: '+35%', color: 'text-highlight' }
            ].map(t => (
               <div key={t.label} className="flex items-center justify-between p-4 bg-surface rounded-2xl border border-white/5">
                 <span className="font-bold">{t.label}</span>
                 <span className={`font-black ${t.color}`}>{t.trend}</span>
               </div>
            ))}
          </div>
        </section>

        <section className="p-10 glass-card bg-highlight/5 border-highlight/20">
          <TrendingUp size={32} className="text-highlight mb-4" />
          <h3 className="text-2xl font-black mb-4">Launch Your VSB</h3>
          <p className="text-slate-400 font-bold leading-relaxed mb-8">
             Generate a fully autonomous business model in 5 minutes. Includes strategy, financial projections, and C-Suite support.
          </p>
          <button className="w-full px-8 py-4 bg-highlight text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-highlight/20 uppercase tracking-widest text-sm">Create New VSB</button>
        </section>
      </div>
    </motion.div>
  );
};

const HubCard = ({ title, description, icon: Icon, action }: any) => (
  <div className="p-8 glass-card group border-white/5 hover:border-highlight/30">
    <div className="w-12 h-12 rounded-xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-highlight group-hover:text-sovereign transition-all">
      <Icon size={24} />
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-xs text-slate-500 font-bold mb-6">{description}</p>
    <button className="text-xs font-black uppercase text-highlight tracking-widest hover:underline">{action}</button>
  </div>
);
