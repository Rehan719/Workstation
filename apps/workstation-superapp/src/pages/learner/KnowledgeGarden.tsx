import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Flower, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, GraduationCap } from 'lucide-react';

export const KnowledgeGarden: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Knowledge Garden</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Mastery Blooms • Neuro-Adaptive Learning Pacing</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Mastery Map')} variant="outline"><GraduationCap size={18} /> Mastery Map</Button>
           <Button onClick={() => notImplemented('Plant Seed')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Plus size={18} /> Plant Seed
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Flower size={24} className="text-highlight" />
                     Blooming Knowledge
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="highlight">Mastery Achieved</Badge>
                  </div>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { name: 'Sovereign Architecture', level: 100, cls: 'w-full', icon: Flower },
                    { name: 'PQC Protocol', level: 85, cls: 'w-[85%]', icon: Flower },
                    { name: 'Mycelial Mesh', level: 42, cls: 'w-[42%]', icon: Flower },
                    { name: 'GaaS Validation', level: 100, cls: 'w-full', icon: Flower }
                  ].map((f, i) => (
                    <div
                      key={i}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex flex-col items-center justify-center group hover:border-highlight/30 transition-all cursor-pointer text-center"
                    >
                       <div className={`w-20 h-20 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight group-hover:bg-highlight group-hover:text-sovereign transition-all mb-4`}>
                          <f.icon size={40} className={f.level === 100 ? "animate-pulse" : ""} />
                       </div>
                       <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{f.name}</p>
                       <div className="w-32 h-1 bg-slate-900 rounded-full mt-2 overflow-hidden">
                          <div className={`h-full bg-highlight ${f.cls}`} />
                       </div>
                       <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mt-2">Mastery: {f.level}%</p>
                    </div>
                  ))}
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
