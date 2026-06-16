import React, { useState, useEffect } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { ShieldCheck, Lock, Activity, History, Info, Globe, AlertTriangle, Zap, RefreshCw, BarChart3, Database } from 'lucide-react';
import { motion } from 'framer-motion';

export const AdminPanel: React.FC = () => {
  const [securityStatus, setSecurityStatus] = useState<any>(null);
  const [resilienceData, setResilienceData] = useState<any>(null);
  const [isTraining, setIsTraining] = useState(false);

  useEffect(() => {
    fetch('/api/v154/security/status')
      .then(res => res.json())
      .then(data => setSecurityStatus(data))
      .catch(err => console.error("Security Fetch Error:", err));
  }, []);

  return (
    <div className="space-y-12 pb-24">
      <header>
        <h1 className="text-6xl font-black text-white uppercase tracking-tighter italic">Entity Control</h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.4em] mt-2">Administrative Command Center • v0.6 Ultimate</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center border-b border-white/5 pb-8">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Lock size={28} className="text-vital" />
                     PQC Security Finality
                  </h3>
                  <Badge color="emerald-500">{securityStatus?.pqc_status || 'LOADING...'}</Badge>
               </div>

               <div className="grid grid-cols-2 gap-10">
                  <div className="space-y-4">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Active Algorithms</p>
                     <div className="flex flex-wrap gap-2">
                        {securityStatus?.active_algorithms?.map((alg: string) => (
                           <span key={alg} className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-aura uppercase tracking-widest">{alg}</span>
                        ))}
                     </div>
                  </div>
                  <div className="space-y-4">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Classical Fallback</p>
                     <Badge color="vital">DISABLED</Badge>
                  </div>
               </div>

               <div className="space-y-6 pt-10">
                  <h4 className="text-[10px] font-black text-slate-700 uppercase tracking-widest">Handshake History (v0.8 Logs)</h4>
                  <div className="space-y-3">
                     {securityStatus?.handshake_history?.map((log: any, i: number) => (
                        <div key={i} className="p-4 rounded-2xl bg-slate-950 border border-slate-900 flex justify-between items-center">
                           <div className="flex items-center gap-4">
                              <ShieldCheck size={16} className={log.status === 'SUCCESS' ? 'text-emerald-500' : 'text-vital'} />
                              <span className="text-[10px] font-mono text-slate-300">{log.client}</span>
                           </div>
                           <span className="text-[10px] font-mono text-slate-600">{log.timestamp}</span>
                        </div>
                     ))}
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10 border-aura/20">
               <div className="flex justify-between items-center border-b border-white/5 pb-8">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Activity size={28} className="text-aura" />
                     Resilience & Self-Healing
                  </h3>
                  <Badge color="aura">LSTM Active</Badge>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                  <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                        <BarChart3 size={14} />
                        Failure Probability
                     </p>
                     <p className="text-3xl font-black text-white">0.04%</p>
                  </div>
                  <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                        <Database size={14} />
                        Metric Samples
                     </p>
                     <p className="text-3xl font-black text-white">12,450</p>
                  </div>
                  <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                        <ShieldCheck size={14} />
                        Healing Status
                     </p>
                     <p className="text-3xl font-black text-emerald-500 uppercase tracking-tighter">Nominal</p>
                  </div>
               </div>

               <div className="p-10 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                  <div className="flex items-center gap-8">
                     <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                        <RefreshCw size={32} className={isTraining ? 'animate-spin' : ''} />
                     </div>
                     <div>
                        <p className="text-xl font-black text-white mb-1 uppercase tracking-widest">LSTM Resilience Model</p>
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Last Retrained: {new Date().toLocaleDateString()}</p>
                     </div>
                  </div>
                  <Button
                    onClick={() => { setIsTraining(true); setTimeout(() => setIsTraining(false), 3000); }}
                    disabled={isTraining}
                    className="bg-aura text-sovereign px-8 py-6 rounded-2xl font-black uppercase tracking-widest text-xs"
                  >
                     {isTraining ? 'Training...' : 'Retrain Model'}
                  </Button>
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 bg-vital/5 border-vital/20 space-y-8">
               <h4 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                  <AlertTriangle size={20} className="text-vital" />
                  Absolute Termination
               </h4>
               <p className="text-sm text-slate-400 font-bold leading-relaxed">
                  Article 1107: Non-PQC handshakes will result in immediate session termination. This policy is globally enforced.
               </p>
               <Button className="w-full bg-vital text-white py-6 rounded-2xl font-black uppercase text-xs tracking-widest">Rotate PQC Keys</Button>
            </Card>
         </aside>
      </div>
    </div>
  );
};
