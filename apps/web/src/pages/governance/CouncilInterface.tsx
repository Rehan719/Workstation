import React from 'react';
import { Card, Button, RealmSelector } from '@workstation/ui';
import { Gavel, ShieldCheck, Users, Activity, Globe, Scale, MessageSquare, AlertCircle } from 'lucide-react';

export const CouncilInterface: React.FC = () => {
  const members = [
    { id: 'ceo-agent', role: 'AI Member', status: 'Active', trust: 0.98 },
    { id: 'cfo-agent', role: 'AI Member', status: 'Active', trust: 0.95 },
    { id: 'guardian-01', role: 'Human Advisor', status: 'Observer', trust: 1.0 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-aura">Inter-Republic Council</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            v3.0 Eternal Governance. <span className="text-white">AI-led decision making</span> with quadratic voting and self-healing rules.
          </p>
        </div>
        <RealmSelector />
      </header>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
           <Card className="p-10">
              <div className="flex justify-between items-center mb-10">
                 <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
                    <Users size={28} className="text-aura" />
                    Council Membership
                 </h3>
                 <span className="text-[10px] font-black text-slate-500 uppercase">Article 1120 Certified</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                 {members.map((m) => (
                   <div key={m.id} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                      <div className="flex items-center gap-4">
                         <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center font-bold text-xs text-aura">
                            {m.id.substring(0, 2).toUpperCase()}
                         </div>
                         <div>
                            <p className="font-black text-white">{m.id}</p>
                            <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{m.role}</p>
                         </div>
                      </div>
                      <div className="text-right">
                         <p className={`text-[10px] font-black uppercase ${m.status === 'Active' ? 'text-emerald-500' : 'text-slate-500'}`}>{m.status}</p>
                         <p className="text-[10px] font-bold text-slate-700">Trust: {(m.trust * 100).toFixed(0)}%</p>
                      </div>
                   </div>
                 ))}
              </div>
           </Card>

           <Card className="bg-aura/5 border-aura/20">
              <h4 className="text-xl font-black mb-6 flex items-center gap-3">
                 <Activity size={24} className="text-aura" />
                 Governance Pulse
              </h4>
              <p className="text-sm text-slate-400 font-bold mb-8">The self-healing engine is currently optimizing 'Quorum Parameters' based on sub-30ms latency benchmarks.</p>
              <div className="flex gap-4">
                 <div className="px-4 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[10px] font-black text-aura uppercase tracking-widest">Self-Healing: Active</div>
                 <div className="px-4 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[10px] font-black text-slate-500 uppercase tracking-widest">Human Observers: 1</div>
              </div>
           </Card>
        </div>

        <aside className="space-y-8">
           <Card className="flex flex-col items-center py-12 text-center">
              <div className="p-6 rounded-3xl bg-slate-900 text-aura mb-8 border border-aura/20">
                 <Gavel size={56} />
              </div>
              <h3 className="text-2xl font-black mb-2">Voting Console</h3>
              <p className="text-sm text-slate-500 font-bold mb-10 px-4">Participate in the v3.0 sovereign consensus using quadratic weighting.</p>
              <Button className="w-full py-5 bg-white text-sovereign text-xs font-black uppercase tracking-[0.2em] hover:bg-aura shadow-2xl">Access Ballot Box</Button>
           </Card>

           <Card className="bg-vital/5 border-vital/20">
              <h4 className="text-xs font-black uppercase text-vital tracking-widest mb-4 flex items-center gap-2">
                 <AlertCircle size={14} /> Active Proposals
              </h4>
              <div className="space-y-3">
                 <p className="text-[10px] font-bold text-slate-500 uppercase">#GOV-142: Mesh Scaling ε=0.08</p>
                 <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                    <div className="h-full bg-vital w-[65%]" />
                 </div>
              </div>
           </Card>
        </aside>
      </section>
    </div>
  );
};
