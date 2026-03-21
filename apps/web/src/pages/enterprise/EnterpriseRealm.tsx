import React from 'react';
import { motion } from 'framer-motion';
import { Card, RealmSelector } from '@workstation/ui';
import { Building2, Gavel, ShieldCheck, TrendingUp, Handshake, Zap } from 'lucide-react';

export const EnterpriseRealm: React.FC = () => {
  const treaties = [
    { partner: 'Nexus Corp', did: 'did:vsb:node-nexus', status: 'ACTIVE', throughput: '12Gbps' },
    { partner: 'Horizon AI', did: 'did:vsb:node-horizon', status: 'NEGOTIATING', throughput: 'N/A' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-highlight">Forest of Collaboration</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Enterprise Scale. <span className="text-aura">Self-organizing markets</span> and anti-fragile supply chains at the edge.
          </p>
        </div>
        <RealmSelector />
      </header>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
           <Card>
              <h3 className="text-2xl font-black mb-8 flex items-center gap-3">
                 <Handshake size={28} className="text-highlight" />
                 Active Treaties
              </h3>
              <div className="space-y-4">
                 {treaties.map((t) => (
                   <div key={t.partner} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all">
                      <div className="flex items-center gap-6">
                         <div className="p-3 bg-slate-900 rounded-xl text-highlight">
                            <Building2 size={24} />
                         </div>
                         <div>
                            <p className="font-black text-white">{t.partner}</p>
                            <p className="text-[10px] font-bold text-slate-500 font-mono">{t.did}</p>
                         </div>
                      </div>
                      <div className="flex items-center gap-8">
                         <div className="text-right">
                            <p className="text-[10px] font-black text-slate-600 uppercase mb-1">Status</p>
                            <span className={`px-2 py-1 rounded-lg text-[10px] font-black uppercase ${t.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'}`}>
                               {t.status}
                            </span>
                         </div>
                         <button className="p-3 bg-slate-900 rounded-xl text-slate-500 hover:text-highlight transition-colors">
                            <Zap size={20} />
                         </button>
                      </div>
                   </div>
                 ))}
              </div>
           </Card>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-highlight/5 border-highlight/20">
                 <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                    <TrendingUp size={20} className="text-highlight" />
                    Market Pulse
                 </h4>
                 <div className="h-32 flex items-center justify-center border border-dashed border-highlight/20 rounded-xl">
                    <span className="text-[10px] font-mono text-highlight/50 uppercase tracking-[0.3em]">Negotiation Stream...</span>
                 </div>
              </Card>
              <Card>
                 <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                    <ShieldCheck size={20} className="text-aura" />
                    Liability Status
                 </h4>
                 <p className="text-xs text-slate-500 font-bold mb-4">Sovereign Liability Fund coverage: 100% active on Polygon Mainnet.</p>
                 <div className="text-2xl font-black text-white">142,000 WST</div>
              </Card>
           </div>
        </div>

        <aside className="space-y-8">
           <Card className="flex flex-col items-center py-10 text-center">
              <div className="p-6 rounded-3xl bg-highlight/10 text-highlight mb-6">
                 <Gavel size={48} />
              </div>
              <h3 className="text-xl font-black mb-2">Republic Council</h3>
              <p className="text-sm text-slate-500 font-bold mb-8 px-4">Cast your quadratic vote on current ecosystem proposals.</p>
              <button className="w-full py-4 bg-highlight text-sovereign font-black rounded-xl text-xs uppercase tracking-widest hover:scale-105 transition-all">Open Ballot</button>
           </Card>
        </aside>
      </section>
    </div>
  );
};
