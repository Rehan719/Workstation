import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Shield, Users, Globe, ChevronRight, CheckCircle2, Gavel, UserPlus, MessageSquare } from 'lucide-react';

export const RealmEditor: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isCreated, setIsCreated] = useState(false);

  const steps = [
    { id: 1, title: "Identity", icon: Globe },
    { id: 2, title: "Governance", icon: Shield },
    { id: 3, title: "Intelligence", icon: MessageSquare }
  ];

  if (isCreated) {
    return (
      <div className="flex flex-col items-center justify-center h-[500px] text-center gap-6">
        <div className="w-24 h-24 rounded-full bg-aura/20 text-aura flex items-center justify-center shadow-[0_0_40px_rgba(100,255,218,0.3)]">
           <CheckCircle2 size={48} />
        </div>
        <div>
           <h2 className="text-3xl font-black mb-2">Realm Instantiated</h2>
           <p className="text-slate-500 font-bold max-w-sm mx-auto">Your sovereign domain is now active in the global federation.</p>
        </div>
        <button type="button" onClick={() => navigate('/')} className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl">Enter Your Realm</button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-12">
      <header className="flex justify-between items-center border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-1">Realm Foundry</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Construct Sovereign Intelligence Domains</p>
        </div>
        <div className="flex gap-4">
           {steps.map(s => (
             <div key={s.id} className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${step === s.id ? 'bg-aura/10 border-aura text-aura' : 'bg-slate-900 border-white/5 text-slate-500'}`}>
                <s.icon size={16} />
                <span className="text-xs font-black uppercase">{s.title}</span>
             </div>
           ))}
        </div>
      </header>

      <main className="glass-card p-12 bg-aura/5 border-aura/20 min-h-[400px] flex flex-col">
        {step === 1 && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
             <div>
                <h3 className="text-2xl font-black mb-2">Define Your Identity</h3>
                <p className="text-slate-500 font-bold">The name and vision that will unite your community.</p>
             </div>
             <div className="space-y-4">
                <input placeholder="Realm Name (e.g., Quantum Garden)" className="w-full bg-sovereign border border-white/10 rounded-2xl p-6 text-xl font-bold focus:border-aura outline-none transition-all" />
                <textarea placeholder="Describe the realm's core mission..." className="w-full bg-sovereign border border-white/10 rounded-2xl p-6 h-32 font-bold focus:border-aura outline-none transition-all"></textarea>
             </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
             <div>
                <h3 className="text-2xl font-black mb-2">Governance Protocols</h3>
                <p className="text-slate-500 font-bold">Establish roles, permissions, and decision-making logic.</p>
             </div>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <GovOption icon={UserPlus} label="Membership" desc="Approval Required" />
                <GovOption icon={Gavel} label="Voting" desc="Quadratic Weighting" />
                <GovOption icon={Shield} label="Privacy" desc="Federated Access" />
                <GovOption icon={Users} label="Roles" desc="Admin, Mentor, Citizen" />
             </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
             <div>
                <h3 className="text-2xl font-black mb-2">Sovereign Intelligence</h3>
                <p className="text-slate-500 font-bold">Select the AI agents that will support your realm.</p>
             </div>
             <div className="p-8 bg-sovereign rounded-3xl border border-white/5 flex items-center justify-between group cursor-pointer hover:border-aura/30 transition-all">
                <div className="flex items-center gap-6">
                   <div className="p-4 bg-aura/20 text-aura rounded-2xl">
                      <Shield size={32} />
                   </div>
                   <div>
                      <p className="text-lg font-black">AI CEO Governance Proxy</p>
                      <p className="text-sm text-slate-500 font-bold">Continuous constitutional validation and strategic oversight.</p>
                   </div>
                </div>
                <div className="w-6 h-6 rounded-full border-2 border-aura flex items-center justify-center">
                   <div className="w-3 h-3 bg-aura rounded-full"></div>
                </div>
             </div>
          </div>
        )}

        <div className="mt-auto pt-10 flex justify-between">
           <button
             onClick={() => setStep(Math.max(1, step - 1))}
             disabled={step === 1}
             className="px-8 py-4 text-slate-500 font-black uppercase text-sm hover:text-white disabled:opacity-0 transition-all"
           >
             Back
           </button>
           <button
             onClick={() => {
               if (step < 3) setStep(step + 1);
               else setIsCreated(true);
             }}
             className="flex items-center gap-3 px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-aura/20 uppercase tracking-widest text-sm"
           >
             {step === 3 ? "Initialize Realm" : "Next Protocol"}
             <ChevronRight size={18} />
           </button>
        </div>
      </main>
    </div>
  );
};

const GovOption = ({ icon: Icon, label, desc }: any) => (
  <div className="p-6 bg-sovereign rounded-2xl border border-white/5 hover:border-aura/30 transition-all cursor-pointer group">
     <div className="flex items-center gap-4 mb-2">
        <Icon size={18} className="text-slate-500 group-hover:text-aura transition-colors" />
        <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">{label}</span>
     </div>
     <p className="text-sm font-bold">{desc}</p>
  </div>
);
