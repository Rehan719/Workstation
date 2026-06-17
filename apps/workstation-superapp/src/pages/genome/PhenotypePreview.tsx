import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Eye, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus } from 'lucide-react';

export const PhenotypePreview: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Phenotype Preview</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Phenotypic Expression Mapping • Behavioral Outcomes</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Reality Preview')} variant="outline"><Eye size={18} /> Reality Preview</Button>
           <Button onClick={() => notImplemented('Update Phenotype')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Plus size={18} /> Update Phenotype
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <main className="@[440px]:col-span-8 space-y-10">
            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-highlight/5 border-highlight/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,204,100,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     Phenotypic State
                     <Badge color="highlight">Article 1132 Compliant</Badge>
                  </h3>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Morphological & Behavioral Simulation Output</p>
               </div>

               <div className="relative z-10 flex flex-col items-center gap-6">
                  <div className="w-48 h-48 rounded-full border-2 border-highlight/20 flex items-center justify-center">
                     <Eye size={80} className="text-highlight opacity-40 animate-pulse" />
                  </div>
                  <p className="font-mono text-xs text-highlight animate-pulse text-center uppercase tracking-widest">... RENDERING PHENOTYPE ...<br/>FIDELITY: 99.98%</p>
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
