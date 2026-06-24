import React, { useState } from 'react';
import { Card, Button, notImplemented, toast } from '@workstation/ui';
import { GitBranch, UserPlus, ShieldCheck, History, Rocket, ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

export const OffspringManagement: React.FC = () => {
  const [offspring, setOffspring] = useState([
    { id: 'did:vsb:offspring-001', parent: 'did:vsb:sovereign-v3', status: 'Sovereign', age: '12d', health: 0.98 },
    { id: 'did:vsb:offspring-002', parent: 'did:vsb:sovereign-v3', status: 'Federated', age: '4d', health: 0.95 },
  ]);

  const spawnInstance = () => {
    const n = offspring.length + 1;
    setOffspring(prev => [...prev, {
      id: `did:vsb:offspring-${String(n).padStart(3, '0')}`,
      parent: 'did:vsb:sovereign-v3',
      status: 'Federated',
      age: '0d',
      health: 1.0,
    }]);
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-highlight break-words">Offspring Management</h1>
          <p className="font-bold uppercase text-[10px] tracking-widest text-highlight">NANITE Propagation • Autonomous Replication (Article 1115)</p>
        </div>
        <Button onClick={spawnInstance} className="bg-highlight text-sovereign">
           <Rocket size={18} /> Spawn New Instance
        </Button>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-4 gap-8">
         <aside className="space-y-8">
            <Card>
               <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-6">Replication Vitals</h4>
               <div className="space-y-6">
                  <VitalsRow label="Offspring Count" value="12" />
                  <VitalsRow label="Success Rate" value="99.9%" />
                  <VitalsRow label="Lineage Depth" value="L4" />
               </div>
            </Card>

            <Card className="bg-highlight/5 border-highlight/20">
               <h4 className="text-xs font-black uppercase text-highlight tracking-widest mb-4">Self-Certification</h4>
               <p className="text-[10px] text-slate-400 font-bold leading-relaxed mb-6">All offspring undergo mandatory v3.0 certification before achieving sovereign status.</p>
               <Button onClick={() => notImplemented('View Certification Specs')} variant="outline" className="w-full text-[8px]">View Certification Specs</Button>
            </Card>
         </aside>

         <main className="@[440px]:col-span-3 space-y-8">
            <Card className="p-10 min-h-[400px]">
               <div className="flex justify-between items-center mb-10">
                  <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
                     <GitBranch size={28} className="text-highlight" />
                     Lineage Visualiser
                  </h3>
                  <div className="flex gap-2">
                     <span className="px-3 py-1 rounded-full bg-slate-900 text-[10px] font-black uppercase text-slate-500">Root: v3.0-Genesis</span>
                  </div>
               </div>

               <div className="space-y-4">
                  {offspring.map((item) => (
                    <div key={item.id} className="p-6 rounded-3xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all">
                       <div className="flex items-center gap-6">
                          <div className="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-highlight border border-slate-800 group-hover:scale-110 transition-transform">
                             <UserPlus size={24} />
                          </div>
                          <div>
                             <p className="font-black text-white text-sm">{item.id}</p>
                             <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">Parent: {item.parent}</p>
                          </div>
                       </div>
                       <div className="flex items-center gap-8">
                          <div className="text-right">
                             <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Status</p>
                             <span className="px-2 py-1 rounded bg-emerald-500/10 text-emerald-500 text-[8px] font-black uppercase">{item.status}</span>
                          </div>
                          <div className="w-px h-8 bg-slate-900" />
                          <button type="button" onClick={() => toast(`${item.id} · ${item.status} · Age ${item.age} · Health ${(item.health * 100).toFixed(0)}%`)} aria-label="Open instance" title="Open instance" className="p-2 text-slate-500 hover:text-highlight transition-colors">
                             <ExternalLink size={18} />
                          </button>
                       </div>
                    </div>
                  ))}
               </div>
            </Card>

            <Card className="h-48 border-dashed border-slate-800 bg-transparent flex flex-col items-center justify-center text-center gap-4">
               <History size={32} className="text-slate-700" />
               <p className="text-xs font-bold text-slate-600 uppercase tracking-[0.2em]">Archived Lineage Records (Phase 1-2)</p>
            </Card>
         </main>
      </div>
    </div>
  );
};

const VitalsRow = ({ label, value }: { label: string, value: string }) => (
  <div className="flex justify-between items-end">
     <span className="text-[10px] font-black uppercase text-slate-500">{label}</span>
     <span className="text-lg font-black text-white">{value}</span>
  </div>
);
