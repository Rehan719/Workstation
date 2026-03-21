import React from 'react';
import { motion } from 'framer-motion';
import { Card, RealmSelector } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { Book, Compass, Star, Users, ArrowRight, Flower2 } from 'lucide-react';

export const LearnerRealm: React.FC = () => {
  const { user } = useStore();

  const gardens = [
    { name: 'Quantum Mechanics', progress: 85, flowers: 3 },
    { name: 'Systems Biology', progress: 42, flowers: 1 },
    { name: 'Agentic Ethics', progress: 95, flowers: 4 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-aura">Garden of Curiosity</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Welcome back, <span className="text-white">{user?.displayName}</span>. Your knowledge gardens are blooming with <span className="text-vital">neuro-adaptive pacing</span>.
          </p>
        </div>
        <RealmSelector />
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {gardens.map((garden) => (
          <Card key={garden.name} className="group hover:border-aura/50 transition-all cursor-pointer overflow-hidden">
             <div className="flex justify-between items-start mb-6">
                <div className="p-4 rounded-2xl bg-slate-800/50 text-vital group-hover:scale-110 transition-transform">
                   <Book size={32} />
                </div>
                <div className="flex gap-1">
                   {Array.from({ length: garden.flowers }).map((_, i) => (
                     <Flower2 key={i} size={16} className="text-vital animate-pulse" />
                   ))}
                </div>
             </div>

             <h3 className="text-2xl font-black mb-4">{garden.name}</h3>

             <div className="space-y-2 mb-8">
                <div className="flex justify-between text-[10px] font-black uppercase text-slate-500">
                   <span>Mastery</span>
                   <span>{garden.progress}%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                   <motion.div
                     initial={{ width: 0 }}
                     animate={{ width: `${garden.progress}%` }}
                     className="h-full bg-vital shadow-[0_0_10px_rgba(255,82,82,0.5)]"
                   />
                </div>
             </div>

             <button className="w-full py-4 rounded-xl bg-slate-800 font-black text-xs uppercase tracking-widest hover:bg-vital hover:text-white transition-all flex items-center justify-center gap-2">
                Continue Exploration <ArrowRight size={14} />
             </button>
          </Card>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
         <Card className="bg-aura/5 border-aura/20">
            <h4 className="text-xl font-black mb-4 flex items-center gap-3">
               <Compass size={24} className="text-aura" />
               Peer Discovery
            </h4>
            <p className="text-sm text-slate-400 font-bold mb-8">Flocking algorithms have identified 3 learners with complementary interests in 'Biomimetic Systems'.</p>
            <div className="flex -space-x-4">
               {[1, 2, 3].map(i => (
                 <div key={i} className="w-12 h-12 rounded-full bg-slate-800 border-2 border-sovereign flex items-center justify-center font-bold text-xs text-aura">
                    P{i}
                 </div>
               ))}
            </div>
         </Card>

         <Card className="bg-vital/5 border-vital/20">
            <h4 className="text-xl font-black mb-4 flex items-center gap-3">
               <Star size={24} className="text-vital" />
               Adaptive Difficulty
            </h4>
            <p className="text-sm text-slate-400 font-bold mb-4">Neural sensors indicate optimal engagement. Increasing abstraction level for next module.</p>
            <div className="flex items-center gap-2">
               <div className="px-3 py-1 rounded-lg bg-slate-900 text-[10px] font-black text-vital uppercase">Lvl: Expert</div>
               <div className="w-32 h-1 bg-slate-900 rounded-full overflow-hidden">
                  <div className="h-full bg-vital w-4/5" />
               </div>
            </div>
         </Card>
      </div>
    </div>
  );
};
