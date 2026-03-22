import React, { useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Shield, Sparkles, FileText, Send, History, CheckCircle2, AlertTriangle, Search } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const ConstitutionalUI: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'articles' | 'proposals' | 'history'>('articles');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1">Constitutional Explorer</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Self-Modification Engine • Article 1118 Compliance</p>
        </div>
        <div className="flex gap-4 p-1 rounded-xl bg-slate-900 border border-slate-800">
           {['articles', 'proposals', 'history'].map((tab) => (
             <button
               key={tab}
               onClick={() => setActiveTab(tab as any)}
               className={`px-4 py-2 rounded-lg text-[10px] font-black uppercase transition-all ${activeTab === tab ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
             >
               {tab}
             </button>
           ))}
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
         <aside className="space-y-8">
            <Card className="bg-aura/5 border-aura/20">
               <h4 className="text-xs font-black uppercase text-aura tracking-widest mb-4 flex items-center gap-2">
                  <Shield size={14} /> Trust Threshold
               </h4>
               <p className="text-xs text-slate-400 font-bold leading-relaxed mb-6">Autonomous amendments require a Trust Factor (T Fa) score of ≥0.9. Current node status: <span className="text-aura">Sovereign High-Trust</span>.</p>
               <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                  <div className="h-full bg-aura w-[92%]" />
               </div>
            </Card>

            <Button className="w-full bg-aura text-sovereign">
               <Sparkles size={16} /> Propose Amendment
            </Button>

            <Card className="bg-slate-950/60">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Search Articles</h4>
               <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900 border border-slate-800">
                  <Search size={14} className="text-slate-600" />
                  <input placeholder="e.g. 1095" className="bg-transparent border-none outline-none text-xs text-white font-bold w-full" />
               </div>
            </Card>
         </aside>

         <main className="lg:col-span-3">
            <AnimatePresence mode="wait">
               {activeTab === 'articles' && (
                 <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-4">
                    {[
                      { id: 1, title: 'Sovereignty', content: 'Every Workstation node is a sovereign digital organism.' },
                      { id: 1095, title: 'Recombination', content: 'All agents and actions must pass GaaS validation.' },
                      { id: 1118, title: 'Infinite Adaptation', content: 'The Constitution shall be capable of autonomous amendment.' },
                    ].map((art) => (
                      <div key={art.id} className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 group hover:border-aura/30 transition-all">
                         <div className="flex justify-between items-start mb-4">
                            <span className="text-[10px] font-black text-aura uppercase tracking-widest">Article {art.id}</span>
                            <CheckCircle2 size={16} className="text-emerald-500 opacity-50" />
                         </div>
                         <h3 className="text-xl font-black mb-2">{art.title}</h3>
                         <p className="text-slate-400 font-bold leading-relaxed">{art.content}</p>
                      </div>
                    ))}
                 </motion.div>
               )}
               {activeTab === 'proposals' && (
                 <div className="h-64 flex flex-col items-center justify-center text-center gap-4 opacity-50">
                    <Send size={48} className="text-aura" />
                    <p className="text-sm font-black uppercase tracking-widest">No active amendment proposals for current epoch.</p>
                 </div>
               )}
            </AnimatePresence>
         </main>
      </div>
    </div>
  );
};
