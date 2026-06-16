import React, { useState } from 'react';
import { Search, Book, FileText, Globe, Shield, Activity, Brain } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { notImplemented } from '@workstation/ui';

const coeData = [
  { name: 'AI Ethics', icon: Shield, articles: 124, scholars: 12, description: 'Alignment and constitutional safety protocols.' },
  { name: 'Data Science', icon: Activity, articles: 256, scholars: 18, description: 'Neural synthesis and graph analytics.' },
  { name: 'Security', icon: Globe, articles: 89, scholars: 8, description: 'Post-quantum cryptography and node defense.' },
  { name: 'UX Design', icon: Brain, articles: 42, scholars: 5, description: 'Biomimetic interfaces and cognitive load optimization.' }
];

export const KnowledgeHub: React.FC = () => {
  const [search, setSearch] = useState('');
  const filtered = coeData.filter(coe => coe.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      <header>
        <h1 className="text-5xl font-black mb-3 tracking-tight neon-text">Centers of Excellence</h1>
        <p className="text-slate-500 font-bold text-lg">Federated knowledge hubs driving the evolution of sovereign intelligence.</p>
      </header>

      <div className="relative max-w-2xl">
        <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-aura" size={20} />
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search CoE knowledge base..."
          className="w-full bg-surface/50 border border-white/10 rounded-2xl py-5 pl-14 pr-8 text-xl focus:outline-none focus:border-aura transition-all shadow-2xl backdrop-blur-xl font-bold"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <AnimatePresence>
          {filtered.map(coe => (
            <motion.div
              layout
              key={coe.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="p-8 glass-card group cursor-pointer"
            >
              <div className="w-14 h-14 rounded-2xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-aura group-hover:text-sovereign transition-all duration-500 shadow-lg">
                <coe.icon size={28} />
              </div>
              <h3 className="text-2xl font-black mb-2 tracking-tight">{coe.name}</h3>
              <p className="text-sm text-slate-500 mb-6 font-bold leading-relaxed">{coe.description}</p>
              <div className="flex items-center gap-4 border-t border-white/5 pt-6">
                 <div>
                    <p className="text-[10px] font-black text-slate-500 uppercase">Articles</p>
                    <p className="text-lg font-black text-aura">{coe.articles}</p>
                 </div>
                 <div>
                    <p className="text-[10px] font-black text-slate-500 uppercase">Scholars</p>
                    <p className="text-lg font-black text-white">{coe.scholars}</p>
                 </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-bold">Latest Insights</h3>
        {[1, 2, 3].map(i => (
          <div key={i} className="flex items-center justify-between p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
            <div className="flex items-center gap-4">
              <FileText className="text-aura" />
              <div>
                <p className="font-bold">Constitutional Governance in Agentic Swarms</p>
                <p className="text-[10px] text-slate-500 font-bold uppercase">AI Ethics • 2 hours ago</p>
              </div>
            </div>
            <button onClick={() => notImplemented('Read Article')} className="text-xs font-bold text-aura hover:underline">Read Article</button>
          </div>
        ))}
      </div>
    </div>
  );
};
