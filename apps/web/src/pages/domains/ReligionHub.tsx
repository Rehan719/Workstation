import React from 'react';
import { motion } from 'framer-motion';
import { Book, Heart, Globe, MessageCircle, Star, ShieldCheck } from 'lucide-react';
import { useGamificationStore } from '../../store/gamificationStore';

export const ReligionHub: React.FC = () => {
  const { completeQuest } = useGamificationStore();

  React.useEffect(() => {
    // Hidden progress for Domain Explorer quest
  }, []);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-highlight/20 rounded-2xl text-highlight shadow-[0_0_20px_rgba(255,215,64,0.2)]">
            <Book size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-highlight">Religion & Ethics</h1>
            <p className="text-slate-500 font-bold text-lg mt-2">Theological study, interfaith dialogue, and ethical reflection.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <HubCard
          title="Scripture Reactor"
          description="AI-assisted deep analysis of sacred texts across traditions."
          icon={ShieldCheck}
          action="Analyze"
        />
        <HubCard
          title="Interfaith Dialogue"
          description="Synthesized perspective rooms for cross-faith understanding."
          icon={Globe}
          action="Join Room"
        />
        <HubCard
          title="Ethical AI Audit"
          description="Evaluate actions against the Workstation's Spiritual Floor."
          icon={Heart}
          action="Run Audit"
        />
      </div>

      <section className="p-8 glass-card">
         <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
           <Star size={20} className="text-highlight" fill="currentColor" />
           Daily Reflection
         </h3>
         <p className="text-slate-400 italic text-lg leading-relaxed">
           "Unity is not uniformity. It is the resonance of unique frequencies into a singular harmonic whole."
         </p>
         <button className="mt-6 px-6 py-2 bg-highlight text-sovereign font-bold rounded-xl hover:scale-105 transition-all">Reflect & Earn 10 XP</button>
      </section>
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
