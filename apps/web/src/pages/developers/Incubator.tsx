import React from 'react';
import { Card, Button } from '@workstation/ui';
import { Beaker, FlaskConical, TrendingUp, Zap, Filter, Share2, Rocket } from 'lucide-react';

export const Incubator: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1 text-aura">The Incubator</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Agent Evolution & Genetic Tournaments • Layer A6</p>
        </div>
        <Button className="bg-aura text-sovereign">
           <Beaker size={18} /> Seed New Agent
        </Button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
           <Card className="p-10">
              <div className="flex justify-between items-center mb-10">
                 <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
                    <TrendingUp size={28} className="text-aura" />
                    Evolutionary Tournaments
                 </h3>
                 <span className="text-[10px] font-black text-slate-500 uppercase">Throughput: 500 agents/hr</span>
              </div>

              <div className="space-y-4">
                 {[1, 2, 3].map(i => (
                   <div key={i} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                      <div className="flex items-center gap-4">
                         <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-aura border border-slate-800">
                            <Zap size={20} />
                         </div>
                         <div>
                            <p className="font-black text-white">Gen-{i*10} Tournament</p>
                            <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">Active Candidates: 142</p>
                         </div>
                      </div>
                      <div className="text-right">
                         <p className="text-[10px] font-black text-aura uppercase mb-1">Peak Fitness</p>
                         <p className="text-lg font-black text-white">0.962</p>
                      </div>
                   </div>
                 ))}
              </div>
           </Card>

           <Card className="bg-slate-900/40 p-10 border-dashed border-slate-800">
              <div className="flex flex-col items-center text-center gap-6">
                 <FlaskConical size={48} className="text-slate-700" />
                 <div className="space-y-2">
                    <h3 className="text-xl font-black text-slate-400">Petri Dish Explorer</h3>
                    <p className="text-sm text-slate-600 font-bold max-w-md">Create isolated cultures to test experimental model merges or high-risk agent behaviors without mesh interference.</p>
                 </div>
                 <Button variant="outline">Initialize Petri Dish</Button>
              </div>
           </Card>
        </div>

        <aside className="space-y-8">
           <Card className="p-8">
              <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-6">Incubator Vitals</h4>
              <div className="space-y-6">
                 <VitalsRow label="Success Rate" value="85%" />
                 <VitalsRow label="Mutation Rate" value="0.02" />
                 <VitalsRow label="Generations" value="1,420" />
              </div>
           </Card>

           <Card className="bg-aura/10 border-aura/30 flex flex-col items-center py-8 text-center">
              <Rocket size={32} className="text-aura mb-4" />
              <h4 className="text-lg font-black mb-2">Factory Deployment</h4>
              <p className="text-xs text-slate-400 font-bold mb-6 px-4">Compile and publish high-fitness agents to your workspace with one click.</p>
              <Button className="w-full">Open Factory</Button>
           </Card>
        </aside>
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
