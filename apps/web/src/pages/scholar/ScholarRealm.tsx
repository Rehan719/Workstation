import React from 'react';
import { Card, Button, RealmSelector } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Search, Network, FileText, Share2, Globe, Brain } from 'lucide-react';

export const ScholarRealm: React.FC = () => {
  const { user } = useStore();

  const mockCitations = [
    { name: 'Jan', count: 12 }, { name: 'Feb', count: 18 }, { name: 'Mar', count: 42 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-white">Observatory of Understanding</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Welcome, Researcher <span className="text-white">{user?.displayName}</span>. Federated GraphRAG and automated meta-analysis are <span className="text-aura">v3.0 Operational</span>.
          </p>
        </div>
        <RealmSelector />
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
         <aside className="space-y-8">
            <Card className="bg-slate-900/60">
               <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-6">Mesh Synapse Discovery</h4>
               <div className="space-y-4">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="flex items-center gap-3">
                       <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                       <span className="text-[10px] font-bold text-slate-400 uppercase">Node-Alpha-{i}: Active</span>
                    </div>
                  ))}
               </div>
            </Card>

            <Button variant="secondary" className="w-full">
               <Search size={16} /> Advanced Query
            </Button>
         </aside>

         <main className="lg:col-span-3 space-y-8">
            <Card className="p-10">
               <div className="flex justify-between items-center mb-10">
                  <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
                     <FileText size={28} className="text-aura" />
                     Publication Pipeline
                  </h3>
                  <span className="text-[10px] font-black px-3 py-1 rounded-lg bg-slate-900 text-slate-500 uppercase">12 Pending Peer Reviews</span>
               </div>

               <div className="space-y-6">
                  {['TIES-Merging Performance Analysis', 'Mycelial Mesh Latency Study'].map((title, i) => (
                    <div key={title} className="p-8 rounded-[2rem] bg-slate-950 border border-slate-900 group hover:border-aura/30 transition-all cursor-pointer">
                       <div className="flex justify-between items-start mb-4">
                          <h4 className="text-lg font-bold text-white group-hover:text-aura transition-colors">{title}</h4>
                          <div className="flex gap-2">
                             <div className="px-2 py-1 rounded bg-aura/10 text-aura text-[8px] font-black uppercase">Verified</div>
                             <div className="px-2 py-1 rounded bg-slate-800 text-slate-500 text-[8px] font-black uppercase">Open Access</div>
                          </div>
                       </div>
                       <p className="text-sm text-slate-500 font-bold mb-6">Automated synthesis of cross-node research datasets (ε=0.1 compliant).</p>
                       <div className="flex items-center gap-6 text-[10px] font-black uppercase text-slate-600">
                          <span className="flex items-center gap-1"><Share2 size={12} /> {80 + (i*12)} Citations</span>
                          <span className="flex items-center gap-1"><Brain size={12} /> Graph Depth: 1.4M</span>
                       </div>
                    </div>
                  ))}
               </div>
            </Card>

            <Card className="h-64">
               <h4 className="text-lg font-black mb-6 flex items-center gap-2">
                  <Network size={20} className="text-aura" />
                  Citation Ecosystem Growth
               </h4>
               <div className="h-40 w-full opacity-50 flex items-center justify-center border border-dashed border-slate-800 rounded-2xl">
                  <span className="text-[10px] font-mono text-slate-600 uppercase tracking-widest">Growth Visualization Stream...</span>
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
