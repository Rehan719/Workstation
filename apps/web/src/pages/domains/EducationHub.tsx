import React from 'react';
import { motion } from 'framer-motion';
import { GraduationCap, BookOpen, Presentation, CheckCircle, Star, Brain, Play } from 'lucide-react';

export const EducationHub: React.FC = () => {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-aura/20 rounded-2xl text-aura shadow-[0_0_20px_rgba(100,255,218,0.2)]">
            <GraduationCap size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-aura">Education & Mastery</h1>
            <p className="text-slate-500 font-bold text-lg mt-2">Personalized learning paths, interactive lessons, and digital reactors.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <HubCard
          title="Education Reactor"
          description="Personalized learning engine with pre-loaded curricula."
          icon={Brain}
          action="Start Lesson"
        />
        <HubCard
          title="Knowledge Ingestion"
          description="Synthesize any data source into a learning object."
          icon={BookOpen}
          action="Ingest Data"
        />
        <HubCard
          title="Mastery Tracking"
          description="Real-time progress and skill certification."
          icon={CheckCircle}
          action="View Stats"
        />
      </div>

      <section className="p-12 glass-card border-aura/30 bg-aura/5 flex items-center justify-between gap-12">
        <div className="flex-1">
          <h3 className="text-2xl font-black mb-4">Your Mastery Pathway</h3>
          <p className="text-slate-400 font-bold leading-relaxed mb-8">
             Based on your interactions, the Education Reactor has prepared a **Recursive Learning Path** on Neural Architectures. 12 lessons ready to launch.
          </p>
          <button className="flex items-center gap-4 px-8 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-aura/20 uppercase tracking-widest text-sm">
            <Play size={18} fill="currentColor" />
            Resume Pathway
          </button>
        </div>
        <div className="w-80 h-48 bg-sovereign rounded-3xl border border-aura/20 overflow-hidden shadow-2xl relative group">
           <div className="absolute inset-0 bg-gradient-to-br from-aura/10 to-transparent"></div>
           <div className="p-8">
              <div className="flex justify-between items-center mb-6">
                 <p className="text-[10px] font-black uppercase text-aura tracking-widest">Progress</p>
                 <p className="text-lg font-black">74%</p>
              </div>
              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                 <div className="h-full bg-aura" style={{ width: '74%' }}></div>
              </div>
           </div>
        </div>
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
