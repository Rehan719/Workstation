import React from 'react';
import { motion } from 'framer-motion';
import { Card, RealmSelector } from '@workstation/ui';
import { BookOpen, Search, Network, FileText, Share2, Globe } from 'lucide-react';

export const ScholarRealm: React.FC = () => {
  const papers = [
    { title: 'Merkle-DAG Integrity in Bio-Neural Architectures', author: 'Dr. Nexus', cites: 142 },
    { title: 'TIES-Merging: Performance Bounds on INT4 Models', author: 'CoE-Research', cites: 89 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-white">Observatory of Understanding</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Global knowledge organism. <span className="text-aura">Federated GraphRAG</span> and automated meta-analysis.
          </p>
        </div>
        <RealmSelector />
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
         <aside className="space-y-8">
            <Card>
               <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-6">Mesh Discovery</h4>
               <div className="space-y-4">
                  <div className="flex items-center gap-3">
                     <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                     <span className="text-[10px] font-bold text-slate-400">Node-Alpha: Synced</span>
                  </div>
                  <div className="flex items-center gap-3">
                     <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                     <span className="text-[10px] font-bold text-slate-400">Node-Omega: Synced</span>
                  </div>
               </div>
            </Card>

            <button className="w-full py-4 bg-white text-sovereign font-black rounded-xl text-xs uppercase tracking-widest flex items-center justify-center gap-2 hover:scale-105 transition-all">
               <Search size={16} /> Search Repository
            </button>
         </aside>

         <main className="lg:col-span-3 space-y-8">
            <Card>
               <h3 className="text-2xl font-black mb-8 flex items-center gap-3">
                  <FileText size={28} className="text-aura" />
                  Recent Publications
               </h3>
               <div className="space-y-6">
                  {papers.map((p) => (
                    <div key={p.title} className="p-8 rounded-[2rem] bg-slate-950/50 border border-slate-900 group hover:border-aura/30 transition-all cursor-pointer">
                       <div className="flex justify-between items-start mb-4">
                          <h4 className="text-lg font-bold text-white group-hover:text-aura transition-colors">{p.title}</h4>
                          <span className="text-[10px] font-black px-3 py-1 rounded-lg bg-slate-900 text-slate-500">Peer Reviewed</span>
                       </div>
                       <div className="flex items-center gap-6 text-[10px] font-black uppercase text-slate-600">
                          <span>{p.author}</span>
                          <span className="flex items-center gap-1"><Share2 size={12} /> {p.cites} Citations</span>
                          <span className="text-aura">v154.0 Verified</span>
                       </div>
                    </div>
                  ))}
               </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
               <Card className="bg-aura/5 border-aura/20">
                  <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                     <Network size={20} className="text-aura" />
                     Federated GraphRAG
                  </h4>
                  <p className="text-xs text-slate-500 font-bold mb-6">Multi-hop reasoning active across 12 distributed knowledge nodes.</p>
                  <div className="flex gap-2">
                     {['Llama', 'Phi', 'Mistral'].map(tag => (
                       <span key={tag} className="px-2 py-1 rounded bg-slate-900 text-[8px] font-black text-slate-400 uppercase tracking-tighter">Engine: {tag}</span>
                     ))}
                  </div>
               </Card>
               <Card>
                  <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                     <Globe size={20} className="text-slate-500" />
                     ORCID Integration
                  </h4>
                  <p className="text-xs text-slate-500 font-bold mb-6">Account linked: did:vsb:scholar-42-alpha. Reputation: 99.9%.</p>
                  <button className="text-[10px] font-black text-aura uppercase tracking-widest hover:underline">View Scholar Profile</button>
               </Card>
            </div>
         </main>
      </div>
    </div>
  );
};
