import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { GraduationCap, BookOpen, HeartPulse, Trophy, Activity, Rocket, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, Network, Binary, Sparkles } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const EducationHub: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('curriculum');

  const subjects = [
    { id: 's-1', title: 'Sovereign Genomics v3', mastery: 0.94, status: 'Mastered', flowers: 42 },
    { id: 's-2', title: 'L11 Mesh Orchestration', mastery: 0.82, status: 'In-Progress', flowers: 12 },
    { id: 's-3', title: 'Ethical Recombination', mastery: 0.45, status: 'Active', flowers: 0 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">Academy of Becoming</h1>
          <p className="text-emerald-500 font-black uppercase text-[10px] tracking-[0.3em]">Garden of Curiosity • Personal Growth & Knowledge Transfer • Education Hub</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Transcript</Button>
           <Button className="bg-emerald-500 text-sovereign shadow-xl shadow-emerald-500/20">
              <Plus size={18} /> Start New Lesson
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-emerald-500/5 border-emerald-500/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Knowledge Garden Visualiser
                     <Badge color="emerald-500">GraphRAG</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Neuro-Adaptive Pacing • 1.4M Knowledge Nodes</p>
               </div>

               <div className="relative z-10 scale-125">
                  <Network size={200} className="text-emerald-500 opacity-20 animate-pulse-slow" />
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10 text-right">
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Flowers Mastered</p>
                     <p className="text-2xl font-black text-emerald-500">142</p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Knowledge Density</p>
                     <p className="text-2xl font-black text-emerald-500">0.88</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <GraduationCap size={24} className="text-emerald-500" />
                     Mastery Curriculum
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('curriculum')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'curriculum' ? 'bg-slate-800 text-emerald-500 shadow-lg' : 'text-slate-500 hover:text-white'}`}>Active</button>
                     <button onClick={() => setActiveTab('mastery')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'mastery' ? 'bg-slate-800 text-emerald-500 shadow-lg' : 'text-slate-500 hover:text-white'}`}>Mastery</button>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                        {subjects.map((subject, i) => (
                          <div key={subject.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-emerald-500/30 transition-all cursor-pointer">
                             <div className="flex items-center gap-8">
                                <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-emerald-500 group-hover:bg-emerald-500 group-hover:text-sovereign transition-all">
                                   <Binary size={24} />
                                </div>
                                <div>
                                   <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{subject.title}</p>
                                   <div className="flex items-center gap-4">
                                      <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Mastery: {subject.mastery * 100}%</span>
                                      <Badge color={subject.status === 'Mastered' ? 'emerald-500' : 'aura'}>{subject.status}</Badge>
                                   </div>
                                </div>
                             </div>
                             <div className="flex items-center gap-8">
                                <div className="text-right">
                                   <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Flowers</p>
                                   <p className="text-xl font-black text-emerald-500">{subject.flowers}</p>
                                </div>
                                <button className="p-4 bg-slate-900 border border-slate-800 rounded-2xl text-slate-500 hover:text-emerald-500 transition-all"><ChevronRight size={20} /></button>
                             </div>
                          </div>
                        ))}
                     </motion.div>
                  </AnimatePresence>
               </div>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-emerald-500/5 border-emerald-500/20">
               <div className="w-16 h-16 rounded-2xl bg-emerald-500 flex items-center justify-center text-sovereign shadow-xl shadow-emerald-500/20">
                  <Activity size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Neuro-Adaptive Pacing</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     L4 regulation loops optimize learning intensity based on your cognitive resonance.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-emerald-500/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Focus Level</span>
                     <span className="text-white">High</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Retention Rate</span>
                     <span className="text-emerald-500">94.2%</span>
                  </div>
               </div>
               <Button className="w-full bg-emerald-500 text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-emerald-500/20">Enter Focus Mode</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <div className="flex items-center gap-4 text-emerald-500">
                  <Sparkles size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Curriculum Composer</h4>
               </div>
               <p className="text-xs text-slate-400 font-bold leading-relaxed">
                  Synthesize a personalized curriculum using the Quad Engine Discovery phase.
               </p>
               <Button variant="outline" className="w-full text-[9px] py-2">Launch Composer</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-emerald-500">
                     <Trophy size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Mastery Rewards</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">142 WST Earned</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
