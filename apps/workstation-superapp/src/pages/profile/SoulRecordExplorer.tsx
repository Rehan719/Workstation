import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Fingerprint, Globe, GitCommit, Layers, ChevronRight, ShieldCheck, Award } from 'lucide-react';
import { motion } from 'framer-motion';

export const SoulRecordExplorer: React.FC = () => {
  const [record, setRecord] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v340/soul-record/guardian-did').then(res => setRecord(res.data));
  }, []);

  if (!record) return <div className="p-8 text-slate-500 animate-pulse">Synchronizing Multi-Verse Identity...</div>;

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div className="flex items-center gap-6">
           <div className="p-5 bg-vital/20 rounded-full text-vital shadow-[0_0_30px_rgba(255,82,82,0.2)]">
              <Fingerprint size={40} />
           </div>
           <div>
             <h1 className="text-4xl font-black mb-1">Soul-Record</h1>
             <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Multi-Dimensional Identity Explorer v153.0</p>
           </div>
        </div>
        <div className="text-right">
           <p className="text-[10px] font-black text-slate-500 uppercase">Unified Reputation</p>
           <p className="text-4xl font-black text-white">{record.unified_reputation.toLocaleString()}</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {record.dimensions.map((dim: any) => (
          <div key={dim.name} className="p-8 glass-card border-white/5 group hover:border-aura/30 transition-all">
             <div className="flex justify-between items-start mb-6">
                <div className="p-4 bg-surface rounded-2xl text-slate-500 group-hover:text-aura transition-colors">
                   <Globe size={24} />
                </div>
                <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 uppercase tracking-widest">
                   RC: {record.reality_coefficient}
                </span>
             </div>
             <h3 className="text-xl font-bold mb-1">{dim.name}</h3>
             <p className="text-xs text-slate-500 font-black uppercase tracking-widest mb-6">{dim.contributions} Contributions</p>

             <div className="flex gap-2 mb-8">
                {dim.badges.map((b: string) => (
                   <div key={b} className="p-2 bg-aura/10 rounded-lg text-aura border border-aura/20">
                      <Award size={14} />
                   </div>
                ))}
             </div>

             <div className="flex justify-between items-end pt-6 border-t border-white/5">
                <div>
                   <p className="text-[10px] font-black text-slate-500 uppercase">Reputation</p>
                   <p className="text-xl font-black text-white">{dim.reputation}</p>
                </div>
                <button type="button" aria-label={`Explore ${dim.name}`} title={`Explore ${dim.name}`} className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all">
                   <ChevronRight size={18} />
                </button>
             </div>
          </div>
        ))}
      </div>

      <section className="p-12 glass-card bg-vital/5 border-vital/20 flex flex-col items-center justify-center text-center gap-6 min-h-[400px]">
         <Layers size={48} className="text-vital animate-pulse" />
         <h3 className="text-2xl font-black uppercase tracking-tight">Identity Graph Integration</h3>
         <p className="text-slate-400 font-bold max-w-2xl leading-relaxed">
            Visualizing the cross-dimensional links of your Soul-Record. Every contribution is cryptographically linked to the UEG Merkle-DAG root.
         </p>
         <div className="text-[10px] font-mono text-slate-600 break-all max-w-xl">
            ROOT_HASH: {record.merkle_root}
         </div>
      </section>
    </div>
  );
};
