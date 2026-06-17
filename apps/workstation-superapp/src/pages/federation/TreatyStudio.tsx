import React, { useState } from 'react';
import axios from 'axios';
import { ScrollText, PenLine, Check, Users } from 'lucide-react';

export const TreatyStudio: React.FC = () => {
  const [nodeA, setNodeA] = useState('');
  const [nodeB, setNodeB] = useState('');
  const [terms, setTerms] = useState('');
  const [draft, setDraft] = useState<any>(null);

  const handleDraft = async () => {
    const res = await axios.post(`/api/v250/treaties/draft?node_a=${nodeA}&node_b=${nodeB}&terms=${terms}`);
    setDraft(res.data);
  };

  const handleSign = () => {
    setDraft((prev: any) => prev ? { ...prev, status: 'Signed' } : prev);
  };

  return (
    <div className="space-y-10 max-w-5xl mx-auto">
      <header>
        <h1 className="text-4xl font-black mb-2">Treaty Studio</h1>
        <p className="text-slate-500">Draft and auto-negotiate standard data sharing and compute exchange treaties.</p>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-12">
        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-8">
           <h3 className="text-xl font-bold flex items-center gap-2">
             <PenLine size={20} className="text-aura" />
             Drafting Table
           </h3>
           <div className="grid grid-cols-2 gap-4">
              <input value={nodeA} onChange={e => setNodeA(e.target.value)} placeholder="Node A ID" className="w-full bg-sovereign border border-slate-700 rounded-xl px-4 py-3" />
              <input value={nodeB} onChange={e => setNodeB(e.target.value)} placeholder="Node B ID" className="w-full bg-sovereign border border-slate-700 rounded-xl px-4 py-3" />
           </div>
           <textarea value={terms} onChange={e => setTerms(e.target.value)} placeholder="Define Treaty Terms..." className="w-full h-40 bg-sovereign border border-slate-700 rounded-2xl p-6" />
           <button onClick={handleDraft} className="w-full py-4 bg-aura text-sovereign font-black rounded-xl">Propose Treaty</button>
        </section>

        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 flex flex-col items-center justify-center text-center">
           {!draft ? (
             <div className="space-y-4">
                <ScrollText size={64} className="text-slate-800 mx-auto" />
                <p className="text-slate-600 font-bold uppercase tracking-widest text-xs">Awaiting Proposal...</p>
             </div>
           ) : (
             <div className="w-full animate-in zoom-in-95 duration-500">
                <div className="p-6 bg-slate-800/30 rounded-2xl border border-aura/20 text-left">
                   <div className="flex justify-between items-center mb-4">
                      <span className="text-[10px] font-black uppercase bg-aura text-sovereign px-2 py-0.5 rounded">{draft.status}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{draft.id}</span>
                   </div>
                   <h4 className="font-bold mb-2">Protocol: {draft.nodes.join(' ↔ ')}</h4>
                   <p className="text-sm text-slate-400 italic mb-6">"{draft.terms}"</p>
                   <button type="button" onClick={handleSign} className="w-full flex items-center justify-center gap-2 py-3 bg-vital/20 text-vital border border-vital/30 rounded-xl font-bold">
                      <Check size={18} />
                      Sign Treaty
                   </button>
                </div>
             </div>
           )}
        </section>
      </div>
    </div>
  );
};
