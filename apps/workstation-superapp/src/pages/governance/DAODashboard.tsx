import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import { Gavel, Landmark, TrendingUp, ChevronRight, Check, X, ShieldAlert, Vote, Users } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const VoteBar = ({ votesFor, votesAgainst }: { votesFor: number; votesAgainst: number }) => {
  const forRef = useRef<HTMLDivElement>(null);
  const againstRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const total = votesFor + votesAgainst;
    if (!total) return;
    if (forRef.current) forRef.current.style.width = `${(votesFor / total) * 100}%`;
    if (againstRef.current) againstRef.current.style.width = `${(votesAgainst / total) * 100}%`;
  }, [votesFor, votesAgainst]);
  return (
    <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden flex">
      <div ref={forRef} className="h-full bg-aura" />
      <div ref={againstRef} className="h-full bg-rose-500" />
    </div>
  );
};

export const DAODashboard: React.FC = () => {
  const [proposals, setProposals] = useState<any[]>([]);
  const [treasury, setTreasury] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v310/governance/proposals').then(res => setProposals(res.data));
    axios.get('/api/v310/governance/treasury').then(res => setTreasury(res.data));
  }, []);

  const handleVote = async (id: string, support: boolean) => {
    await axios.post(`/api/v310/governance/vote?proposal_id=${id}&user_id=guardian&weight=100&support=${support}`);
    alert(`Vote recorded: ${support ? 'FOR' : 'AGAINST'}. System resonance updated.`);
  };

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1">Creator DAO</h1>
          <p className="text-slate-500 font-bold text-lg mt-2">Decentralized platform governance and treasury oversight.</p>
        </div>
        {treasury && (
           <div className="flex items-center gap-6">
              <div className="text-right">
                 <p className="text-[10px] font-black text-slate-500 uppercase">Public Treasury</p>
                 <p className="text-3xl font-black text-white">{treasury.balance_wst.toLocaleString()} WST</p>
              </div>
              <div className="p-4 bg-aura/20 text-aura rounded-2xl">
                 <Landmark size={28} />
              </div>
           </div>
        )}
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
         <div className="lg:col-span-2 space-y-8">
            <h3 className="text-2xl font-black flex items-center gap-3">
               <Vote size={24} className="text-aura" />
               Active Proposals
            </h3>

            <div className="space-y-6">
               {proposals.map(p => (
                 <div key={p.id} className="p-8 glass-card border-white/5 hover:border-aura/20 transition-all space-y-6">
                    <div className="flex justify-between items-start">
                       <div>
                          <div className="flex items-center gap-2 mb-2">
                             <span className="text-[10px] font-black uppercase px-3 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                                {p.category}
                             </span>
                             <span className="text-[10px] font-black uppercase text-aura">Ends in 6 days</span>
                          </div>
                          <h4 className="text-xl font-bold">{p.title}</h4>
                       </div>
                       <div className="text-right">
                          <p className="text-[10px] font-black text-slate-500 uppercase">Proposer</p>
                          <p className="text-xs font-bold text-white">@{p.proposer}</p>
                       </div>
                    </div>

                    <div className="space-y-2">
                       <div className="flex justify-between text-[10px] font-black uppercase tracking-widest">
                          <span className="text-aura">FOR: {p.votes_for.toLocaleString()}</span>
                          <span className="text-rose-500">AGAINST: {p.votes_against.toLocaleString()}</span>
                       </div>
                       <VoteBar votesFor={p.votes_for} votesAgainst={p.votes_against} />
                    </div>

                    <div className="flex gap-4">
                       <button
                         onClick={() => handleVote(p.id, true)}
                         className="flex-1 py-4 bg-aura text-sovereign font-black rounded-xl hover:scale-[1.02] transition-all flex items-center justify-center gap-2 uppercase tracking-widest text-xs"
                       >
                         <Check size={18} />
                         Support
                       </button>
                       <button
                         onClick={() => handleVote(p.id, false)}
                         className="flex-1 py-4 bg-rose-500/20 text-rose-500 border border-rose-500/30 font-black rounded-xl hover:bg-rose-500/30 transition-all flex items-center justify-center gap-2 uppercase tracking-widest text-xs"
                       >
                         <X size={18} />
                         Reject
                       </button>
                    </div>
                 </div>
               ))}
            </div>
         </div>

         <aside className="space-y-8">
            <section className="p-8 glass-card border-aura/20 bg-aura/5">
               <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <ShieldAlert size={20} className="text-aura" />
                  Voting Power
               </h3>
               <div className="space-y-6">
                  <div>
                     <p className="text-[10px] font-black text-slate-500 uppercase">Your Balance</p>
                     <p className="text-3xl font-black text-white">14,205 <span className="text-xs text-aura">WST</span></p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-500 uppercase">Delegated Power</p>
                     <p className="text-xl font-black text-slate-400">0.0</p>
                  </div>
                  <button className="w-full py-4 bg-white/5 border border-white/10 rounded-xl font-bold text-xs uppercase tracking-widest hover:border-aura hover:text-aura transition-all">
                     Delegate Votes
                  </button>
               </div>
            </section>

            <section className="p-8 glass-card">
               <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Users size={20} className="text-highlight" />
                  Active Guilds
               </h3>
               <div className="space-y-4">
                  {['Education-Foundry', 'Legal-Engineers', 'Ethical-Scholars'].map(g => (
                    <div key={g} className="flex items-center justify-between p-4 bg-surface rounded-2xl border border-white/5">
                       <span className="text-sm font-bold">{g}</span>
                       <ChevronRight size={14} className="text-slate-600" />
                    </div>
                  ))}
               </div>
            </section>
         </aside>
      </div>
    </div>
  );
};
