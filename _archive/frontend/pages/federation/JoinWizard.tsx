import React, { useState } from 'react';
import { toast } from '@workstation/ui';
import { Network, Terminal, ShieldCheck, Cpu } from 'lucide-react';

export const JoinFederationWizard: React.FC = () => {
  const [step, setStep] = useState(0);

  const steps = [
    { title: "Select Node Architecture", content: "Choose between standard cloud instances or local sovereign Docker nodes." },
    { title: "Configure Reactors", content: "Select which CoE knowledge bases and agents your node will host." },
    { title: "Treaty Synchronization", content: "Auto-negotiate standard data sharing treaties with existing federation nodes." },
    { title: "Spawn & Register", content: "Generate your PQC-ready node identity and register with the global federation." }
  ];

  return (
    <div className="space-y-10 max-w-4xl mx-auto">
      <header>
        <h1 className="text-4xl font-black mb-2">Join the Federation</h1>
        <p className="text-slate-500">Contribute compute and storage to the Workstation civilization.</p>
      </header>

      <div className="p-12 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-8 relative overflow-hidden">
        <progress value={step + 1} max={steps.length} aria-label={`Step ${step + 1} of ${steps.length}`}
          className="absolute top-0 left-0 w-full h-1 appearance-none rounded-none overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-aura [&::-webkit-progress-value]:transition-all [&::-moz-progress-bar]:bg-aura" />

        <div className="flex gap-8 items-start">
           <div className="p-4 bg-aura/10 text-aura rounded-2xl">
              {step === 0 && <Cpu size={32} />}
              {step === 1 && <Terminal size={32} />}
              {step === 2 && <ShieldCheck size={32} />}
              {step === 3 && <Network size={32} />}
           </div>
           <div className="flex-1">
              <h2 className="text-2xl font-black mb-2">{steps[step].title}</h2>
              <p className="text-slate-400 leading-relaxed">{steps[step].content}</p>
           </div>
        </div>

        <div className="pt-8 border-t border-slate-800 flex justify-between items-center">
           <button
             disabled={step === 0}
             onClick={() => setStep(step - 1)}
             className={`px-8 py-3 rounded-xl font-bold ${step === 0 ? 'text-slate-700 cursor-not-allowed' : 'text-slate-400 hover:bg-slate-800'}`}
           >
             Back
           </button>
           <button
             onClick={() => step < steps.length - 1 ? setStep(step + 1) : toast("Node Registration Queued — PQC signature pending.")}
             className="px-8 py-3 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all"
           >
             {step === steps.length - 1 ? "Initialize Node" : "Continue"}
           </button>
        </div>
      </div>
    </div>
  );
};
