import React from 'react';
import { Card, Badge } from '@workstation/ui';
import { Binary, GitMerge, Fingerprint } from 'lucide-react';

export const GenomeExplorer: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter italic">Genome Explorer</h1>
        <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Merkle-DAG Integrity • Evolutionary Heritage Tracking</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-6">
               <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <Binary size={24} className="text-highlight" />
                  Sovereign DNA Blocks
               </h3>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[1, 2, 3, 4].map(i => (
                    <div key={i} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 group hover:border-highlight/30 transition-all">
                       <div className="flex justify-between items-start mb-4">
                          <Badge color="highlight">Operon-X{i}</Badge>
                          <Fingerprint size={16} className="text-slate-700" />
                       </div>
                       <p className="text-sm font-black text-white uppercase tracking-widest mb-1">Hash: 0x42e8...{i}</p>
                       <p className="text-[10px] text-slate-500 uppercase font-black">Ratified: 2026-03-21</p>
                    </div>
                  ))}
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
