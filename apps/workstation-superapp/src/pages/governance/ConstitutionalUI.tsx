import React, { useState, useEffect } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Shield, Sparkles, FileText, Send, History, CheckCircle2, AlertTriangle, Search, Activity, Zap, TrendingUp, Clock, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const ConstitutionalUI: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'articles' | 'timeline' | 'history'>('articles');
  const [search, setSearch] = useState('');
  const [articles, setArticles] = useState<any[]>([]);

  useEffect(() => {
    // v0.2: Constitution Explorer - Fetch all 1127 articles
    fetch('/api/v154/constitution/articles')
      .then(res => res.json())
      .then(data => setArticles(Array.isArray(data) ? data : []))
      .catch(() => setArticles([]));
  }, []);

  const timeline = [
    { id: 'ev-1', title: 'Self-Ratified: Article 1148', type: 'AUTONOMOUS', rationale: 'LEO latency variance recovery.', time: '2h ago' },
    { id: 'ev-2', title: 'Proposed: Article 1151', type: 'AI-PROPOSAL', rationale: 'Martian regolith harvesting rights.', time: '14h ago' },
  ];

  const filtered = articles.filter(a =>
    a?.title?.toLowerCase().includes(search.toLowerCase()) ||
    a?.category?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Constitutional Core</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Self-Modification Engine • Universal Governance • Phase 4</p>
        </div>
        <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
           {['articles', 'timeline', 'history'].map((tab) => (
             <button
               key={tab}
               onClick={() => setActiveTab(tab as any)}
               className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === tab ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
             >
               {tab}
             </button>
           ))}
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-4 text-aura">
                  <Shield size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Adaptation Engine</h4>
               </div>
               <p className="text-sm text-slate-400 font-bold leading-relaxed">
                  Autonomous self-healing is active. Constitutional AI generates and ratifies low-impact amendments.
               </p>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Trust Score</span>
                     <span className="text-aura">0.96 (SOVEREIGN)</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-[96%]" />
                  </div>
               </div>
               <Button className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-aura/20">
                  <Sparkles size={18} /> Propose Amendment
               </Button>
            </Card>

            <Card className="p-10 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Filter Codex</h4>
               <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                  <Search size={18} className="text-slate-700" />
                  <input
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    placeholder="Search by Title, Category..."
                    className="bg-transparent border-none outline-none text-xs text-white font-bold w-full"
                  />
               </div>
               <div className="flex flex-wrap gap-2">
                  {['CORE', 'ETERNAL', 'COSMIC', 'CARE'].map(cat => (
                    <button key={cat} onClick={() => setSearch(cat)} className="px-3 py-1 rounded-lg bg-slate-900 text-[8px] font-black text-slate-500 hover:text-aura transition-all">{cat}</button>
                  ))}
               </div>
            </Card>
         </aside>

         <main className="lg:col-span-8">
            <AnimatePresence mode="wait">
               {activeTab === 'articles' && (
                 <motion.div key="articles" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
                    {filtered.map((art, i) => (
                      <div key={art.id} className="p-10 rounded-[2.5rem] bg-slate-950/80 border border-slate-900 group hover:border-aura/30 transition-all">
                         <div className="flex justify-between items-center mb-6">
                            <div className="flex items-center gap-4">
                               <div className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-black text-aura uppercase">Article {art.id}</div>
                               <Badge color={art.category === 'COSMIC' ? 'highlight' : 'aura'}>{art.category}</Badge>
                            </div>
                            <CheckCircle2 size={20} className="text-emerald-500 opacity-20 group-hover:opacity-100 transition-opacity" />
                         </div>
                         <h3 className="text-3xl font-black mb-4 text-white uppercase tracking-tight">{art.title}</h3>
                         <p className="text-lg text-slate-400 font-bold leading-relaxed">{art.content}</p>
                      </div>
                    ))}
                 </motion.div>
               )}

               {activeTab === 'timeline' && (
                 <motion.div key="timeline" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
                    <Card className="p-10">
                       <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4 mb-10">
                          <Clock size={24} className="text-aura" />
                          Evolution Timeline
                       </h3>
                       <div className="space-y-8 relative before:absolute before:left-7 before:top-2 before:bottom-2 before:w-px before:bg-slate-800">
                          {timeline.map((ev, i) => (
                            <div key={ev.id} className="relative pl-20">
                               <div className="absolute left-4 top-1 w-6 h-6 rounded-full bg-slate-950 border-2 border-aura flex items-center justify-center z-10">
                                  <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                               </div>
                               <div className="p-8 rounded-[2.5rem] bg-slate-900/50 border border-slate-800 group hover:border-aura/30 transition-all">
                                  <div className="flex justify-between items-start mb-4">
                                     <div>
                                        <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{ev.title}</p>
                                        <Badge color="aura">{ev.type}</Badge>
                                     </div>
                                     <span className="text-[10px] font-black text-slate-600 uppercase">{ev.time}</span>
                                  </div>
                                  <p className="text-sm text-slate-400 font-bold leading-relaxed">{ev.rationale}</p>
                               </div>
                            </div>
                          ))}
                       </div>
                    </Card>
                 </motion.div>
               )}
            </AnimatePresence>
         </main>
      </div>
    </div>
  );
};
