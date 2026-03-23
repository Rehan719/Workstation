import React from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Database, Plus, Settings, Archive } from 'lucide-react';

export const Factory: React.FC = () => {
  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black text-white uppercase tracking-tighter italic">The Factory</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Mass Production • Automated Deployment • QA Convergence</p>
        </div>
        <Button className="bg-aura text-sovereign"><Plus size={18} /> New Production Line</Button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-6">
               <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <Database size={24} className="text-aura" />
                  Active Production Lines
               </h3>
               <div className="space-y-4">
                  <div className="p-8 rounded-3xl bg-slate-950 border border-slate-900 flex items-center justify-between">
                     <div className="flex items-center gap-6">
                        <div className="w-12 h-12 rounded-xl bg-aura/20 flex items-center justify-center text-aura"><Settings size={24} /></div>
                        <div>
                           <p className="text-lg font-black text-white uppercase tracking-widest">Autonomous-BTO-Core-01</p>
                           <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Target: Mainnet-V1</p>
                        </div>
                     </div>
                     <Badge color="aura">In Production</Badge>
                  </div>
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
