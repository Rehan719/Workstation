import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Star, ChevronRight, CheckCircle2, Lock } from 'lucide-react';
import { useGamificationStore } from '../../store/gamificationStore';

export const QuestLog: React.FC = () => {
  const { quests, stats } = useGamificationStore();

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-end border-b border-white/5 pb-6">
        <div>
          <h2 className="text-3xl font-black mb-2">Evolution Quests</h2>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-[0.2em]">Guided Pathways to Sovereignty</p>
        </div>
        <div className="flex gap-2">
           <div className="px-4 py-2 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-2">
              <Star size={14} className="text-aura" fill="currentColor" />
              <span className="text-xs font-black text-aura">{quests.filter(q => stats.completed_quests.includes(q.id)).length}/{quests.length}</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {quests.map((quest) => {
          const isCompleted = stats.completed_quests.includes(quest.id);
          return (
            <motion.div
              key={quest.id}
              whileHover={{ scale: 1.02 }}
              className={`p-6 rounded-[2rem] border transition-all ${
                isCompleted
                  ? 'bg-aura/5 border-aura/20'
                  : 'bg-slate-900/40 border-white/5 hover:border-white/10'
              }`}
            >
              <div className="flex justify-between items-start mb-6">
                 <div className={`p-4 rounded-2xl ${isCompleted ? 'bg-aura/10 text-aura' : 'bg-surface text-slate-500'}`}>
                    <Trophy size={24} />
                 </div>
                 <div className="text-right">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{quest.category}</p>
                    <p className="text-lg font-black text-white">+{quest.xp_reward} XP</p>
                 </div>
              </div>

              <h3 className={`text-xl font-bold mb-2 ${isCompleted ? 'text-aura' : 'text-white'}`}>{quest.title}</h3>
              <p className="text-xs text-slate-500 font-bold mb-8 leading-relaxed">{quest.description}</p>

              {isCompleted ? (
                <div className="flex items-center gap-2 text-aura font-black uppercase text-[10px] tracking-widest">
                   <CheckCircle2 size={14} />
                   Quest Synchronized
                </div>
              ) : (
                <button className="w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl font-bold text-xs uppercase tracking-widest transition-all">
                  Launch Quest
                </button>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
