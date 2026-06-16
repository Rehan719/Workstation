import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Fingerprint, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus } from 'lucide-react';

export const MethylationEditor: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Methylation Editor</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Epigenetic Configuration • Trait Inheritance Suppression</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Rollback Marks')} variant="outline"><History size={18} /> Rollback Marks</Button>
           <Button onClick={() => notImplemented('Add Epigenetic Mark')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Plus size={18} /> Add Epigenetic Mark
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Fingerprint size={24} className="text-highlight" />
                     Methylation Marks
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="highlight">Epigenetic Inheritance</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight group-hover:bg-highlight group-hover:text-sovereign transition-all`}>
                             <Fingerprint size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">Mark-CH3-{i}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>Gene: RECT-EN-0{i}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-highlight">Status: Active</span>
                             </div>
                          </div>
                       </div>
                       <Badge color="aura">Suppressed</Badge>
                    </div>
                  ))}
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
