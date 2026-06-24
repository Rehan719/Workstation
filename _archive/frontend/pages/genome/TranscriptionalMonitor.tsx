import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Radio, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, Activity } from 'lucide-react';

export const TranscriptionalMonitor: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Transcriptional Monitor</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">mRNA Synthesis • Expression Dynamics • Allostatic Load Monitoring</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Expression Plot')} variant="outline"><Activity size={18} /> Expression Plot</Button>
           <Button onClick={() => notImplemented('Add Expression Logic')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Plus size={18} /> Add Expression Logic
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <main className="@[440px]:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Radio size={24} className="text-highlight" />
                     Transcriptional Output
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="highlight">Real-time Expression</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight group-hover:bg-highlight group-hover:text-sovereign transition-all`}>
                             <Radio size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">mRNA-Operon-{i}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>Copy Count: 1.4K</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-highlight">Status: Synthesising</span>
                             </div>
                          </div>
                       </div>
                       <Badge color="aura">High</Badge>
                    </div>
                  ))}
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
