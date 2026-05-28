import React from 'react';
import { Card, Badge } from '@workstation/ui';
import { Network, Zap, Cpu, Activity } from 'lucide-react';

export const GRNDashboard: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter italic">GRN Dashboard</h1>
        <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Gene Regulatory Network • Allostatic Regulation</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-highlight/5 border-highlight/10">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,204,100,0.05)_0%,transparent_70%)]"></div>
               <div className="relative z-10 flex flex-col items-center gap-6">
                  <div className="w-32 h-32 rounded-full border-2 border-highlight/20 flex items-center justify-center">
                     <Network size={64} className="text-highlight opacity-40 animate-pulse" />
                  </div>
                  <p className="font-mono text-xs text-highlight animate-pulse text-center uppercase tracking-widest">Constructing Regulation Mesh...<br/>Nodes: 142 | Edges: 850</p>
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
