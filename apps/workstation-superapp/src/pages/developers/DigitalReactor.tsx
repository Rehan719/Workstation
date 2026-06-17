import React, { useState } from 'react';
import { Card, Button, notImplemented} from '@workstation/ui';
import { Play, Shield, Terminal, Zap, Bug, Share2, Info } from 'lucide-react';

export const DigitalReactor: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-aura break-words">Digital Reactor</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Sandboxed Simulation Environment • Layer A5</p>
        </div>
        <Button onClick={() => setIsRunning(!isRunning)} className={isRunning ? 'bg-vital' : 'bg-aura'}>
          {isRunning ? <Zap size={18} className="animate-pulse" /> : <Play size={18} />}
          {isRunning ? 'Stop Simulation' : 'Launch Reactor'}
        </Button>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-12 h-[600px]">
         <aside className="p-8 glass-card bg-sovereign/40 flex flex-col gap-8">
            <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Simulation Parameters</h3>
            <div className="space-y-6">
               <ParamToggle label="Article 1095 Logic" active={true} />
               <ParamToggle label="Latency Stress" active={false} />
               <ParamToggle label="Byzantine Faults" active={false} />
               <ParamToggle label="PQC Enforced" active={true} />
            </div>

            <div className="mt-auto p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center gap-4">
               <Bug size={24} className="text-vital" />
               <p className="text-xs font-bold text-slate-400">Zero active vulnerabilities detected in current configuration.</p>
            </div>
         </aside>

         <main className="@[440px]:col-span-2 glass-card bg-slate-950/50 border-aura/20 relative overflow-hidden flex flex-col">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
            <div className="relative p-10 flex-1 overflow-y-auto custom-scrollbar font-mono text-xs space-y-2">
               {!isRunning ? (
                 <div className="h-full flex flex-col items-center justify-center text-center gap-4 opacity-50">
                    <Terminal size={48} />
                    <p className="font-black uppercase tracking-widest">Waiting for simulation trigger...</p>
                 </div>
               ) : (
                 <>
                   <p className="text-aura">[SYSTEM] Reactor initializing v3.0 Digital Sandbox...</p>
                   <p className="text-slate-500">[INFO] Loading constituent agent: did:vsb:agent-42</p>
                   <p className="text-slate-500">[INFO] Article 1101 validation hook attached.</p>
                   <p className="text-emerald-500">[SUCCESS] Mesh consensus reached in 42ms.</p>
                   <p className="text-slate-500">[INFO] Probing edge-case: latency variance (30ms-50ms).</p>
                   <p className="text-yellow-500">[WARNING] Minor resonance drop detected in Layer 8.</p>
                 </>
               )}
            </div>
            {isRunning && (
              <div className="p-6 bg-slate-900/80 border-t border-aura/20 flex justify-between items-center">
                 <div className="flex gap-4">
                    <div className="px-3 py-1 rounded bg-slate-800 text-[8px] font-black text-slate-400 uppercase">CPU: 42%</div>
                    <div className="px-3 py-1 rounded bg-slate-800 text-[8px] font-black text-slate-400 uppercase">MEM: 1.2GB</div>
                 </div>
                 <Button onClick={() => notImplemented('Export Trace')} variant="outline" className="text-[10px] px-4 py-2"><Share2 size={12} /> Export Trace</Button>
              </div>
            )}
         </main>
      </div>
    </div>
  );
};

const ParamToggle = ({ label, active }: { label: string, active: boolean }) => (
  <div className="flex justify-between items-center group cursor-pointer">
     <span className="text-xs font-bold text-slate-400 group-hover:text-white transition-colors">{label}</span>
     <div className={`w-10 h-5 rounded-full transition-all relative ${active ? 'bg-aura' : 'bg-slate-800'}`}>
        <div className={`absolute top-1 w-3 h-3 rounded-full bg-white transition-all ${active ? 'left-6' : 'left-1'}`} />
     </div>
  </div>
);
