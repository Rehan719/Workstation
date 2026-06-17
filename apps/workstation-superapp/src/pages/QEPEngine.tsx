import React from 'react';
import { Layers, Search, Database, Cpu, Send, LayoutGrid, CheckCircle2, AlertCircle } from 'lucide-react';
import { Card, Button, notImplemented} from '@workstation/ui';
import { useStore } from '@workstation/shared';

export const QEPEngine: React.FC = () => {
  const engines = [
    { name: 'Discovery', icon: Search, color: 'text-aura', status: 'Scanning Mesh', progress: 92 },
    { name: 'Ingestion', icon: Database, color: 'text-highlight', status: 'Syncing DIDs', progress: 45 },
    { name: 'Synthesis', icon: Cpu, color: 'text-vital', status: 'Recombining', progress: 78 },
    { name: 'Deployment', icon: Send, color: 'text-aura', status: 'Broadcasting', progress: 10 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header>
        <h1 className="text-5xl font-black mb-3 tracking-tight">Quad Engine Reactor</h1>
        <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
          The <span className="text-aura">DISD Pipeline</span>: Governing the lifecycle of sovereign AI components.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-4 gap-6">
        {engines.map((engine) => (
          <Card key={engine.name} className="flex flex-col group hover:border-aura/50 transition-all">
            <div className="flex justify-between items-start mb-6">
               <div className={`w-14 h-14 rounded-2xl bg-slate-800/50 flex items-center justify-center ${engine.color}`}>
                  <engine.icon size={28} />
               </div>
               <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{engine.progress}%</span>
            </div>
            <h3 className="text-xl font-black mb-1">{engine.name}</h3>
            <p className="text-[10px] text-slate-600 font-bold uppercase tracking-widest mb-6">{engine.status}</p>
            <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
               <div className={`h-full bg-aura transition-all duration-1000`} style={{ width: `${engine.progress}%` }} />
            </div>
          </Card>
        ))}
      </div>

      <Card className="p-10">
         <div className="flex justify-between items-center mb-10">
            <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
               <LayoutGrid size={24} className="text-aura" />
               DISD Pipeline Control Panel
            </h3>
            <Button onClick={() => notImplemented('Initiate Synthesis')} variant="secondary">Initiate Synthesis</Button>
         </div>

         <div className="space-y-4">
            {[
              { id: '1', name: 'Llama-3-Graft', stage: 'Synthesis', health: 'Healthy' },
              { id: '2', name: 'Search-Optimizer-v2', stage: 'Discovery', health: 'Healthy' },
              { id: '3', name: 'Ethics-Guardrail-v3', stage: 'Deployment', health: 'Critical' },
            ].map((node) => (
              <div key={node.id} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                 <div className="flex items-center gap-6">
                    <div className="w-10 h-10 rounded-full bg-slate-900 flex items-center justify-center font-bold text-xs text-slate-500">#{node.id}</div>
                    <div>
                       <p className="font-black text-white">{node.name}</p>
                       <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">Stage: {node.stage}</p>
                    </div>
                 </div>
                 <div className="flex items-center gap-4">
                    <div className={`flex items-center gap-2 px-3 py-1 rounded-lg text-[10px] font-black uppercase ${node.health === 'Healthy' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-vital/10 text-vital'}`}>
                       {node.health === 'Healthy' ? <CheckCircle2 size={12} /> : <AlertCircle size={12} />}
                       {node.health}
                    </div>
                    <Button onClick={() => notImplemented('Manage')} variant="outline" className="px-4 py-2 text-[10px]">Manage</Button>
                 </div>
              </div>
            ))}
         </div>
      </Card>
    </div>
  );
};
