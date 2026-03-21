import React from 'react';
import { Card, RealmSelector } from '@workstation/ui';
import { Building2, Gavel, ShieldCheck, TrendingUp, Handshake, Zap, Globe } from 'lucide-react';

export const EnterpriseRealm: React.FC = () => {
  const treaties = [
    { partner: 'Nexus Corp', did: 'did:vsb:node-nexus', status: 'ACTIVE', throughput: '12Gbps', liability: '100%' },
    { partner: 'Horizon AI', did: 'did:vsb:node-horizon', status: 'NEGOTIATING', throughput: 'N/A', liability: '0%' },
    { partner: 'Eos Foundry', did: 'did:vsb:node-eos', status: 'ACTIVE', throughput: '8Gbps', liability: '100%' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-6xl font-black tracking-tighter mb-4 text-highlight">Forest of Collaboration</h1>
          <p className="text-slate-400 font-bold text-xl max-w-2xl leading-relaxed">
            Enterprise Operations. <span className="text-aura">Anti-fragile supply chains</span> and self-organizing markets for the digital republic.
          </p>
        </div>
        <RealmSelector />
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
           <Card className="p-10">
              <h3 className="text-2xl font-black mb-8 flex items-center gap-3">
                 <Handshake size={28} className="text-highlight" />
                 Symbiotic Treaty Ledger
              </h3>
              <div className="space-y-4">
                 {treaties.map((t) => (
                   <div key={t.partner} className="p-6 rounded-3xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all">
                      <div className="flex items-center gap-6">
                         <div className="p-4 bg-slate-900 rounded-2xl text-highlight">
                            <Building2 size={24} />
                         </div>
                         <div>
                            <p className="font-black text-white text-lg">{t.partner}</p>
                            <p className="text-[10px] font-bold text-slate-600 font-mono tracking-tighter uppercase">{t.did}</p>
                         </div>
                      </div>
                      <div className="flex items-center gap-8">
                         <div className="text-right">
                            <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Throughput</p>
                            <p className="text-sm font-black text-white">{t.throughput}</p>
                         </div>
                         <div className={`w-3 h-3 rounded-full ${t.status === 'ACTIVE' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'bg-amber-500 animate-pulse'}`} />
                         <button className="p-3 bg-slate-900 rounded-xl text-slate-500 hover:text-highlight transition-colors border border-slate-800">
                            <Zap size={20} />
                         </button>
                      </div>
                   </div>
                 ))}
              </div>
           </Card>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-highlight/5 border-highlight/20 overflow-hidden relative group">
                 <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                    <Globe size={120} />
                 </div>
                 <h4 className="text-lg font-black mb-4 flex items-center gap-2">
                    <TrendingUp size={20} className="text-highlight" />
                    Market Pulse
                 </h4>
                 <p className="text-sm text-slate-500 font-bold mb-6">Negotiation streams are optimal. WST circulation: 1.2M/mo.</p>
                 <div className="flex gap-2">
                    <div className="flex-1 h-1 bg-highlight/20 rounded-full overflow-hidden">
                       <div className="h-full bg-highlight w-3/4 animate-pulse" />
                    </div>
                 </div>
              </Card>
              <Card>
                 <h4 className="text-lg font-black mb-4 flex items-center gap-2 text-aura">
                    <ShieldCheck size={20} />
                    Liability Certification
                 </h4>
                 <p className="text-xs text-slate-500 font-bold mb-6 leading-relaxed">
                    Sovereign Liability Fund (SLF) coverage: 100% active. Treaty arbitration governed by IRC (Floor 22).
                 </p>
                 <div className="text-3xl font-black text-white">142,000 WST</div>
              </Card>
           </div>
        </div>

        <aside className="space-y-8">
           <Card className="flex flex-col items-center py-12 text-center bg-slate-900/40">
              <div className="p-6 rounded-3xl bg-highlight/10 text-highlight mb-8 border border-highlight/20">
                 <Gavel size={56} />
              </div>
              <h3 className="text-2xl font-black mb-2">Republic Council</h3>
              <p className="text-sm text-slate-500 font-bold mb-10 px-4 leading-relaxed">
                 Cast your quadratic vote on ecosystem proposals. Next budget allocation: 4d 12h.
              </p>
              <button className="w-full py-5 bg-highlight text-sovereign font-black rounded-2xl text-xs uppercase tracking-[0.2em] hover:scale-105 transition-all shadow-xl shadow-highlight/10">
                 Access Ballot Box
              </button>
           </Card>

           <Card className="border-dashed border-slate-800 bg-transparent">
              <h4 className="text-[10px] font-black uppercase text-slate-700 tracking-widest mb-4">Supply Chain Vitals</h4>
              <div className="space-y-3">
                 {[1, 2].map(i => (
                   <div key={i} className="flex justify-between items-center py-2 border-b border-slate-900 last:border-0">
                      <span className="text-[10px] font-bold text-slate-500">Route-Alpha-{i}</span>
                      <span className="text-[10px] font-black text-emerald-500">Anti-Fragile</span>
                   </div>
                 ))}
              </div>
           </Card>
        </aside>
      </div>
    </div>
  );
};
