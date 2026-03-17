import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Shield, Vote, AlertTriangle, ScrollText } from 'lucide-react';

export const FederationGovernance: React.FC = () => {
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [voters, setVoters] = useState(142);

  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-black mb-2">Federation Governance</h1>
        <p className="text-slate-500">Cross-node treaty management and constitutional amendment voting.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
             <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
               <ScrollText size={20} className="text-aura" />
               Active Treaties
             </h3>
             <div className="space-y-4">
                <TreatyItem nodeA="Alpha" nodeB="Beta" type="Data Sharing" status="enforced" />
                <TreatyItem nodeA="Gamma" nodeB="Alpha" type="Compute Exchange" status="negotiating" />
             </div>
          </section>

          <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
             <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
               <Vote size={20} className="text-highlight" />
               Pending Federation Votes
             </h3>
             <div className="p-6 bg-slate-800/30 rounded-2xl border border-slate-700">
                <p className="font-bold mb-2">AMD-142: Post-Quantum Migration Protocol</p>
                <p className="text-xs text-slate-500 mb-6">Proposal to mandate Kyber-768 for all cross-node heartbeat signatures.</p>
                <div className="flex justify-between items-center">
                   <span className="text-xs font-black text-aura uppercase">{voters} Guardians Voted</span>
                   <button className="px-6 py-2 bg-aura text-sovereign font-bold rounded-lg hover:scale-105 transition-all">Cast Resonance</button>
                </div>
             </div>
          </section>
        </div>

        <div className="space-y-8">
          <section className="p-8 rounded-3xl bg-rose-500/5 border border-rose-500/20">
             <h3 className="text-xl font-bold mb-6 flex items-center gap-2 text-rose-400">
               <AlertTriangle size={20} />
               Ecosystem Alerts
             </h3>
             <div className="space-y-4">
                <div className="p-4 bg-rose-500/10 rounded-xl border border-rose-500/20">
                   <p className="text-xs font-bold text-rose-200 uppercase">Node-Gamma Offline</p>
                   <p className="text-[10px] text-rose-400/70 mt-1">Connectivity lost 14m ago. Treaty sync suspended.</p>
                </div>
             </div>
          </section>
        </div>
      </div>
    </div>
  );
};

const TreatyItem = ({ nodeA, nodeB, type, status }: any) => (
  <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50">
    <div className="flex items-center gap-3">
       <span className="text-xs font-bold text-white">{nodeA} <span className="text-slate-600 px-1">↔</span> {nodeB}</span>
       <span className="text-[10px] font-black uppercase text-slate-500 bg-slate-900 px-2 py-0.5 rounded border border-slate-700">{type}</span>
    </div>
    <span className={`text-[10px] font-black uppercase ${status === 'enforced' ? 'text-vital' : 'text-amber-500'}`}>{status}</span>
  </div>
);
