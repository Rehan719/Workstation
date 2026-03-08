import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Onboarding = ({ onComplete }) => {
  const [step, setStep] = useState(0);

  const steps = [
    {
      title: "Welcome to Jules AI",
      content: "Your Digital Sanctuary for Quranic learning and sovereign business development. Let's take a quick tour.",
      target: "welcome"
    },
    {
      title: "Your Spiritual Dashboard",
      content: "Track your Tazkiyah (purification) score and Hifz progress in real-time. Every recitation counts.",
      target: "dashboard"
    },
    {
      title: "The Digital Reactor",
      content: "Incubate projects across Science, Law, and Faith. AI-driven insights vetted by scholars.",
      target: "reactors"
    },
    {
      title: "Scholar Governance",
      content: "Rest assured that all religious content is audited by a qualified Scholar Board with veto power.",
      target: "scholar"
    }
  ];

  const nextStep = () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      onComplete();
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      >
        <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl border border-amber-500/20">
          <div className="flex justify-between items-center mb-6">
            <span className="text-[10px] font-black uppercase tracking-widest text-amber-600 bg-amber-100 px-3 py-1 rounded-full">
              Tutorial: Step {step + 1} of {steps.length}
            </span>
            <button onClick={onComplete} className="text-slate-400 hover:text-slate-600">
              Skip
            </button>
          </div>
          <h2 className="text-3xl font-black text-slate-900 mb-4 leading-tight">{steps[step].title}</h2>
          <p className="text-slate-600 mb-8 text-lg leading-relaxed">{steps[step].content}</p>
          <div className="flex gap-4">
            <button
              onClick={nextStep}
              className="flex-1 bg-amber-500 text-white font-black py-4 rounded-xl shadow-lg shadow-amber-500/20 hover:bg-amber-600 transition-all"
            >
              {step === steps.length - 1 ? "Finish" : "Next"}
            </button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default Onboarding;
