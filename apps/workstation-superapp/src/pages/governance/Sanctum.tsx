import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Shield, Gavel, Landmark, ChevronRight, Lock, Eye, Sparkles, Award, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from '@workstation/ui';
import { progressWidthClass } from '../../lib/progressWidth';

export const Sanctum: React.FC = () => {
  const [accessGranted, setAccessGranted] = useState(false);
  const [proposals, setProposals] = useState<any[]>([]);
  const [detailProposal, setDetailProposal] = useState<any | null>(null);

  useEffect(() => {
    // Simulated authentication check: Min reputation 1000
    setTimeout(() => setAccessGranted(true), 1500);
    setProposals([
      { id: 'meta-01', title: "Evolve Article 1096: Post-Quantum Autonomy", status: "Deliberation", support: "84%" },
      { id: 'meta-02', title: "Modify Amendment Threshold to 75% Supermajority", status: "Voting", support: "92%" }
    ]);
  }, []);

  const castSovereignVote = (id: string) => {
    setProposals(prev => prev.map(p => {
      if (p.id !== id) return p;
      const next = Math.min(100, parseFloat(p.support) + 1);
      return { ...p, support: `${next}%` };
    }));
  };

  if (!accessGranted) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center gap-6">
        <Lock size={64} className="text-slate-700" />
        <h2 className="text-2xl font-black text-slate-500 uppercase tracking-[0.4em]">The Sanctum</h2>
        <p className="text-slate-600 font-bold max-w-xs">Verification of multi-dimensional resonance in progress. Minimum reputation threshold: 1,000.</p>
        <div className="w-48 h-1 bg-slate-900 rounded-full overflow-hidden mt-4">
           <div className={`h-full bg-aura animate-pulse ${progressWidthClass(65)}`}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-12 max-w-6xl mx-auto">
      <header className="flex flex-col items-center text-center gap-4 py-12 border-b border-white/5 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.05)_0%,transparent_70%)]"></div>
        <div className="p-5 bg-aura/20 rounded-full text-aura shadow-[0_0_50px_rgba(100,255,218,0.2)] relative z-10">
          <Shield size={48} />
        </div>
        <div className="relative z-10">
           <h1 className="text-6xl font-black tracking-tighter neon-text">THE SANCTUM</h1>
           <p className="text-slate-500 font-bold text-xl mt-3 uppercase tracking-widest">The Seat of Constitutional Sovereignty</p>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-12">
        <div className="@[440px]:col-span-2 space-y-8">
           <div className="flex items-center justify-between">
              <h3 className="text-2xl font-black uppercase tracking-tight flex items-center gap-3">
                 <Sparkles size={24} className="text-aura" />
                 Meta-Amendments
              </h3>
              <button type="button" onClick={() => toast('Meta-Proposal drafting opens in the next governance epoch')} className="px-6 py-2 border border-aura/30 text-aura font-black rounded-xl text-xs uppercase tracking-widest hover:bg-aura/10 transition-all">New Meta-Proposal</button>
           </div>

           <div className="space-y-6">
              {proposals.map(p => (
                <div key={p.id} className="p-8 glass-card border-aura/20 bg-aura/5 hover:bg-aura/10 transition-all group">
                   <div className="flex justify-between items-start mb-6">
                      <div className="text-[10px] font-black text-aura uppercase tracking-[0.2em] border border-aura/30 px-3 py-1 rounded-full">
                         {p.status}
                      </div>
                      <span className="text-sm font-black text-white">{p.support} Consensus</span>
                   </div>
                   <h4 className="text-2xl font-black mb-4 leading-tight">{p.title}</h4>
                   <div className="flex gap-4">
                      <button type="button" onClick={() => castSovereignVote(p.id)} className="flex-1 py-4 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest">Cast Sovereign Vote</button>
                      <button type="button" onClick={() => setDetailProposal(p)} aria-label="View proposal details" title="View proposal details" className="p-4 bg-white/5 border border-white/10 rounded-xl text-slate-400 hover:text-white transition-all"><Eye size={20} /></button>
                   </div>
                </div>
              ))}
           </div>
        </div>

        <aside className="space-y-8">
           <section className="p-8 glass-card border-white/5 bg-sovereign/40">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-3">
                 <Award size={20} className="text-highlight" />
                 Resonance Authority
              </h3>
              <div className="space-y-6">
                 <div>
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Sovereign Reputation</p>
                    <p className="text-4xl font-black text-white">1,420</p>
                 </div>
                 <div>
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Meta-Voting Weight</p>
                    <p className="text-xl font-black text-aura">2.42x</p>
                 </div>
                 <div className="pt-4 border-t border-white/5 text-[10px] text-slate-500 font-bold leading-relaxed">
                    Authority derived from 142 cross-realm contributions and 12 passed constitutional amendments.
                 </div>
              </div>
           </section>
        </aside>
      </div>

      <AnimatePresence>
        {detailProposal && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-6"
            onClick={() => setDetailProposal(null)}>
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }}
              onClick={e => e.stopPropagation()}
              className="bg-slate-950 border border-aura/30 rounded-[2rem] p-8 w-full max-w-lg space-y-6">
              <div className="flex items-start justify-between gap-4">
                <div className="p-3 bg-aura/10 rounded-xl text-aura shrink-0"><Shield size={20} /></div>
                <button type="button" aria-label="Close" onClick={() => setDetailProposal(null)} className="text-slate-500 hover:text-white shrink-0"><X size={18} /></button>
              </div>
              <div>
                <span className="text-[9px] font-black text-aura uppercase tracking-widest border border-aura/30 px-2 py-0.5 rounded-full">{detailProposal.status}</span>
                <h3 className="text-xl font-black text-white mt-3 leading-snug">{detailProposal.title}</h3>
              </div>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="p-4 bg-slate-900 rounded-xl">
                  <p className="text-[9px] text-slate-500 font-black uppercase tracking-widest mb-1">Consensus</p>
                  <p className="text-2xl font-black text-aura">{detailProposal.support}</p>
                </div>
                <div className="p-4 bg-slate-900 rounded-xl">
                  <p className="text-[9px] text-slate-500 font-black uppercase tracking-widest mb-1">Status</p>
                  <p className="text-sm font-black text-white uppercase">{detailProposal.status}</p>
                </div>
              </div>
              <button type="button" onClick={() => { castSovereignVote(detailProposal.id); setDetailProposal(null); }}
                className="w-full py-3 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest hover:opacity-90">
                Cast Sovereign Vote
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
