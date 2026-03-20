import React from 'react';
import { Layers, Search, Database, Cpu, Send, LayoutGrid } from 'lucide-react';
import { Card } from '@workstation/ui';
import { useStore } from '@workstation/shared';

export const QEPEngine: React.FC = () => {
  const { systemVitals } = useStore();

  const engines = [
    { name: 'Discovery', icon: Search, color: 'text-aura' },
    { name: 'Ingestion', icon: Database, color: 'text-highlight' },
    { name: 'Synthesis', icon: Cpu, color: 'text-vital' },
    { name: 'Deployment', icon: Send, color: 'text-aura' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header>
        <h1 className="text-5xl font-black mb-3 tracking-tight">Quad Engine Platform (QEP)</h1>
        <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
          The underlying orchestration engine managing the <span className="text-aura">Autonomous Knowledge Pipeline</span>.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {engines.map((engine) => (
          <Card key={engine.name} className="flex flex-col items-center group hover:border-aura/50 transition-all">
            <div className={`w-20 h-20 rounded-full border-4 border-slate-800 border-t-aura animate-spin-slow mb-6 flex items-center justify-center relative`}>
              <engine.icon size={32} className={`${engine.color} absolute`} />
            </div>
            <h3 className="text-xl font-black mb-2">{engine.name}</h3>
            <div className="flex items-center gap-2">
               <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/20" />
               <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Operational</span>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="h-full">
            <div className="flex justify-between items-center mb-10">
              <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
                 <LayoutGrid size={24} className="text-aura" />
                 Active Pipeline Visualization
              </h3>
              <div className="flex gap-6">
                 {['Inlet', 'Refining', 'Outlet'].map(label => (
                   <div key={label} className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-slate-700" />
                      <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">{label}</span>
                   </div>
                 ))}
              </div>
            </div>

            <div className="h-80 bg-sovereign/40 rounded-3xl border border-slate-900 flex flex-col items-center justify-center relative overflow-hidden group">
               <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-aura via-transparent to-transparent group-hover:opacity-20 transition-opacity duration-1000" />
               <p className="text-slate-700 font-black uppercase tracking-[0.4em] text-xs mb-4 z-10">Pipeline Graph Stream</p>
               <div className="flex gap-4 z-10">
                  <div className="w-32 h-1 bg-slate-800 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-2/3 animate-pulse" />
                  </div>
               </div>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <h4 className="text-lg font-black mb-6 uppercase tracking-widest text-slate-500">Live Vitals</h4>
            <div className="space-y-6">
               <div className="flex justify-between items-end">
                  <span className="text-[10px] font-black uppercase text-slate-500">Throughput</span>
                  <span className="text-xl font-black">128 MB/s</span>
               </div>
               <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-highlight w-[65%]" />
               </div>
               <div className="flex justify-between items-end">
                  <span className="text-[10px] font-black uppercase text-slate-500">Synthesis Latency</span>
                  <span className="text-xl font-black">42ms</span>
               </div>
               <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-vital w-[40%]" />
               </div>
            </div>
          </Card>

          <Card className="bg-aura/10 border-aura/30">
             <h4 className="text-lg font-black mb-2">Platform Health</h4>
             <p className="text-xs text-slate-400 font-bold mb-6">All engines resonating at optimal frequencies (99.98% Fidelity).</p>
             <button className="w-full py-4 bg-aura text-sovereign font-black rounded-xl text-[10px] uppercase tracking-widest hover:scale-105 transition-all">Re-Sync Mesh</button>
          </Card>
        </div>
      </div>
    </div>
  );
};
