import React from 'react';
import { Card, RealmSelector, Button } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { Shield, Settings, Activity, Database, Cpu, Globe, Key, AlertTriangle } from 'lucide-react';

export const AdminPanel: React.FC = () => {
  const { systemVitals } = useStore();

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1">Entity Control</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Homeostatic Orchestrator • Layer 5 Hardening</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline">Export UEG Logs</Button>
           <Button className="bg-vital text-white">Emergency 888_HOLD</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         <Card className="p-10 lg:col-span-2">
            <h3 className="text-2xl font-black mb-10 flex items-center gap-3">
               <Shield size={28} className="text-aura" />
               Security Posture (OWASP ASI)
            </h3>
            <div className="space-y-6">
               {[
                 { id: 'ASI-01', name: 'Goal Hijacking', status: 'Mitigated', color: 'text-emerald-500' },
                 { id: 'ASI-02', name: 'Tool Misuse', status: 'Mitigated', color: 'text-emerald-500' },
                 { id: 'ASI-04', name: 'Supply Chain', status: 'Hardened', color: 'text-aura' },
                 { id: 'ASI-06', name: 'Adversarial Negotiation', status: 'Active Monitoring', color: 'text-yellow-500' },
               ].map((asi) => (
                 <div key={asi.id} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between">
                    <div className="flex items-center gap-6">
                       <span className="text-xs font-black text-slate-700">{asi.id}</span>
                       <span className="font-bold text-white">{asi.name}</span>
                    </div>
                    <span className={`text-[10px] font-black uppercase ${asi.color}`}>{asi.status}</span>
                 </div>
               ))}
            </div>
         </Card>

         <aside className="space-y-8">
            <Card>
               <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-8">CL1 Efficiency</h4>
               <div className="flex flex-col items-center gap-6">
                  <div className="w-32 h-32 rounded-full border-8 border-slate-900 border-t-aura flex items-center justify-center relative">
                     <span className="text-2xl font-black text-white">12.5x</span>
                     <p className="absolute -bottom-6 text-[8px] font-black text-slate-500 uppercase">vs GPU baseline</p>
                  </div>
                  <p className="text-[10px] font-bold text-slate-600 text-center uppercase leading-relaxed">20% of total inference offloaded to parallel biological units.</p>
               </div>
            </Card>

            <Card className="bg-aura/5 border-aura/20">
               <h4 className="text-xs font-black uppercase text-aura tracking-widest mb-6 flex items-center gap-2">
                  <Key size={14} /> PQC Finality
               </h4>
               <div className="space-y-4">
                  <div className="flex justify-between text-[10px] font-bold">
                     <span className="text-slate-500 uppercase">Algorithm</span>
                     <span className="text-white">Kyber-1024</span>
                  </div>
                  <div className="flex justify-between text-[10px] font-bold">
                     <span className="text-slate-500 uppercase">Signature</span>
                     <span className="text-white">Dilithium-5</span>
                  </div>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
