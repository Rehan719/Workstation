import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Rocket, Target, DollarSign, LineChart, FileText, ChevronRight, CheckCircle2, TrendingUp, Users, ShieldCheck } from 'lucide-react';
import axios from 'axios';

export const BusinessPlanWizard: React.FC = () => {
  const [step, setStep] = useState(1);
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/v310/entrepreneur/generate-plan', {
        creation_id: "Neural-Nexus-v2",
        target_market: "Enterprise AI",
        funding_goal: 50000
      });
      setPlan(res.data);
      setStep(3);
    } catch (err) {
      console.error("Plan generation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-1">Entrepreneurial Hub</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Livelihood & Business Synthesis v151.0</p>
        </div>
        <div className="flex gap-4">
           {[1, 2, 3].map(s => (
             <div key={s} className={`w-8 h-8 rounded-full flex items-center justify-center font-black text-xs border ${step >= s ? 'bg-aura text-sovereign border-aura' : 'border-slate-800 text-slate-700'}`}>
                {s}
             </div>
           ))}
        </div>
      </header>

      <main className="glass-card p-12 bg-highlight/5 border-highlight/20 min-h-[500px] flex flex-col relative overflow-hidden">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="s1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
               <div>
                  <h2 className="text-3xl font-black mb-2 flex items-center gap-3">
                     <Rocket size={28} className="text-highlight" />
                     Launch Your Livelihood
                  </h2>
                  <p className="text-slate-500 font-bold">Select a creation to transform into a sustainable business.</p>
               </div>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-8 bg-sovereign rounded-[2rem] border border-white/10 hover:border-highlight/40 cursor-pointer transition-all group">
                     <p className="text-lg font-black group-hover:text-highlight transition-colors">Neural-Nexus-v2</p>
                     <p className="text-[10px] text-slate-500 font-black uppercase mt-2">Reactor • 1.4k Installs</p>
                  </div>
                  <div className="p-8 bg-slate-900 border border-dashed border-slate-800 rounded-[2rem] flex items-center justify-center text-slate-600 font-bold italic">
                     Select other creation...
                  </div>
               </div>
               <div className="pt-8">
                  <button onClick={() => setStep(2)} className="flex items-center gap-3 px-10 py-4 bg-highlight text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-highlight/20 uppercase tracking-widest text-sm">
                    Configure Strategy
                    <ChevronRight size={18} />
                  </button>
               </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="s2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
               <div>
                  <h2 className="text-3xl font-black mb-2 flex items-center gap-3">
                     <Target size={28} className="text-highlight" />
                     Market Parameters
                  </h2>
                  <p className="text-slate-500 font-bold">Define the scope and goals for the AI CEO's synthesis.</p>
               </div>
               <div className="space-y-6 max-w-xl">
                  <div className="space-y-2">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Target Market</p>
                     <input defaultValue="Enterprise AI Analytics" className="w-full bg-sovereign border border-white/10 rounded-2xl p-5 font-bold outline-none focus:border-highlight transition-all" />
                  </div>
                  <div className="space-y-2">
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Seed Funding Goal (WST)</p>
                     <input defaultValue="50000" className="w-full bg-sovereign border border-white/10 rounded-2xl p-5 font-bold outline-none focus:border-highlight transition-all" />
                  </div>
               </div>
               <div className="pt-8">
                  <button onClick={handleGenerate} disabled={loading} className="flex items-center gap-3 px-10 py-4 bg-highlight text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-highlight/20 uppercase tracking-widest text-sm disabled:opacity-50">
                    {loading ? 'Synthesizing...' : 'Synthesize Business Plan'}
                    <Sparkles size={18} />
                  </button>
               </div>
            </motion.div>
          )}

          {step === 3 && plan && (
            <motion.div key="s3" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
               <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-3xl font-black mb-2">Strategy: Neural-Nexus-v2</h2>
                    <div className="flex items-center gap-2">
                       <CheckCircle2 size={16} className="text-highlight" />
                       <span className="text-xs font-black uppercase text-highlight tracking-widest">AI CEO Validated</span>
                    </div>
                  </div>
                  <button className="p-4 bg-white/10 rounded-2xl text-white hover:bg-white/20 transition-all border border-white/10">
                     <FileText size={24} />
                  </button>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {plan.financial_projections.map((p: any) => (
                    <div key={p.period} className="p-6 bg-sovereign rounded-3xl border border-white/5 space-y-2">
                       <p className="text-[10px] font-black text-slate-500 uppercase">{p.period} Projection</p>
                       <p className="text-2xl font-black text-white">{p.revenue.toLocaleString()} <span className="text-xs text-aura">WST</span></p>
                       <p className="text-xs font-black text-vital">{p.growth} Growth</p>
                    </div>
                  ))}
               </div>

               <div className="p-8 bg-surface rounded-[2rem] border border-white/5">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                     <Target size={18} className="text-highlight" />
                     Strategic Roadmap
                  </h3>
                  <div className="space-y-4">
                     {plan.strategic_steps.map((s: string, i: number) => (
                        <div key={i} className="flex items-center gap-4 text-sm font-bold text-slate-300">
                           <div className="w-6 h-6 rounded-full bg-highlight/20 text-highlight flex items-center justify-center text-[10px]">{i+1}</div>
                           {s}
                        </div>
                     ))}
                  </div>
               </div>

               <button className="w-full py-5 bg-highlight text-sovereign font-black rounded-2xl hover:scale-[1.02] transition-all shadow-xl shadow-highlight/20 uppercase tracking-widest text-sm">
                  Register Business & Open Payouts
               </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
         <div className="p-10 glass-card">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-3">
               <Users size={20} className="text-aura" />
               Expert Mentorship
            </h3>
            <div className="space-y-4">
               {[
                 { name: 'Sovereign-Scale', role: 'Tokenomics Advisor' },
                 { name: 'Growth-Mindset', role: 'Global Strategy' }
               ].map(m => (
                 <div key={m.name} className="flex items-center justify-between p-4 bg-surface rounded-2xl border border-white/5">
                    <div>
                       <p className="font-bold">{m.name}</p>
                       <p className="text-[10px] text-slate-500 uppercase font-black">{m.role}</p>
                    </div>
                    <button className="text-[10px] font-black uppercase text-aura hover:underline">Match</button>
                 </div>
               ))}
            </div>
         </div>

         <div className="p-10 glass-card border-vital/20 bg-vital/5">
            <h3 className="text-xl font-bold mb-4 flex items-center gap-3">
               <ShieldCheck size={20} className="text-vital" />
               Legal Mastery
            </h3>
            <p className="text-xs text-slate-500 font-bold leading-relaxed mb-6">
               Generate AI-assisted Terms of Service and IP Licensing agreements. Verified against the global constitutional floor.
            </p>
            <button className="w-full py-4 bg-white/5 border border-white/10 rounded-xl text-xs font-black uppercase tracking-widest hover:border-vital hover:text-vital transition-all">
               Draft Compliance Pack
            </button>
         </div>
      </section>
    </div>
  );
};
