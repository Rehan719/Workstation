import React, { useState } from 'react';

export const OnboardingTour: React.FC = () => {
  const [step, setStep] = useState(0);
  const [visible, setVisible] = useState(true);

  const steps = [
    { title: "Welcome, Guardian", content: "You are now at the heart of the Workstation federation. This tour will guide you through your new sovereign command console." },
    { title: "Cognitive Dashboards", content: "Explore 'Self Vision' for system vitals and 'World Mind' for global research synthesis." },
    { title: "Sovereign Wallet", content: "Manage your WST resonance and stake in the global federation's liability fund." },
    { title: "Recursive Evolution", content: "Use the 'Enhancement Proposer' to vote on and approve autonomous system improvements." }
  ];

  if (!visible) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-sovereign/90 backdrop-blur-md">
      <div className="max-w-md w-full p-8 bg-slate-900 border border-aura/30 rounded-3xl shadow-2xl text-center">
        <h2 className="text-3xl font-black mb-4">{steps[step].title}</h2>
        <p className="text-slate-400 mb-8 leading-relaxed">{steps[step].content}</p>

        <div className="flex gap-4">
           {step > 0 && (
             <button
               onClick={() => setStep(step - 1)}
               className="flex-1 py-4 border border-slate-700 rounded-xl font-bold hover:bg-slate-800 transition-all"
             >
               Previous
             </button>
           )}
           <button
             onClick={() => step < steps.length - 1 ? setStep(step + 1) : setVisible(false)}
             className="flex-2 py-4 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all"
           >
             {step === steps.length - 1 ? "Start Command" : "Next Step"}
           </button>
        </div>
      </div>
    </div>
  );
};
