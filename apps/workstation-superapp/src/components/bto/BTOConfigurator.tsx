import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, ChevronLeft, CheckCircle2, Shield } from 'lucide-react';

interface BTOConfiguratorProps {
  product: any;
  onClose: () => void;
}

export const BTOConfigurator: React.FC<BTOConfiguratorProps> = ({ product, onClose }) => {
  const [step, setStep] = useState(0);
  const [selections, setSelections] = useState<Record<string, string>>({});
  const [isOrdered, setIsOrdered] = useState(false);

  const currentOption = product.options[step];

  const handleSelect = (choiceId: string) => {
    setSelections({ ...selections, [currentOption.id]: choiceId });
  };

  const handleNext = () => {
    if (step < product.options.length - 1) {
      setStep(step + 1);
    } else {
      setIsOrdered(true);
    }
  };

  const calculateTotal = () => {
    let total = product.basePrice;
    Object.entries(selections).forEach(([optionId, choiceId]) => {
      const option = product.options.find((o: any) => o.id === optionId);
      const choice = option?.choices.find((c: any) => c.id === choiceId);
      if (choice) total += choice.price;
    });
    return total;
  };

  if (isOrdered) {
    return (
      <div className="text-center p-12 space-y-6">
        <div className="w-20 h-20 bg-vital/20 text-vital rounded-full mx-auto flex items-center justify-center">
          <CheckCircle2 size={48} />
        </div>
        <h2 className="text-3xl font-black">Order Synchronized</h2>
        <p className="text-slate-500 max-w-sm mx-auto">
          Your custom <span className="text-white font-bold">{product.name}</span> has been queued for compilation.
        </p>
        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-left space-y-2">
          <p className="text-[10px] font-black uppercase text-slate-500">Order ID: SOV-{Math.random().toString(36).substr(2, 9).toUpperCase()}</p>
          <p className="text-[10px] font-black uppercase text-slate-500">Estimated Delivery: 4h 12m</p>
        </div>
        <button type="button" onClick={onClose} className="w-full py-4 bg-aura text-sovereign font-bold rounded-xl">Return to Catalog</button>
      </div>
    );
  }

  return (
    <div className="p-8 h-full flex flex-col">
      <header className="mb-8 flex justify-between items-start">
        <div>
          <h2 className="text-2xl font-black mb-1">Configuring {product.name}</h2>
          <div className="flex gap-2">
            {product.options.map((_: any, i: number) => (
              <div key={i} className={`h-1 w-8 rounded-full ${i <= step ? 'bg-aura' : 'bg-slate-800'}`}></div>
            ))}
          </div>
        </div>
        <button type="button" onClick={onClose} className="text-slate-500 hover:text-white">&times;</button>
      </header>

      <div className="flex-1">
        <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Step {step + 1}: {currentOption.name}</p>
        <div className="space-y-4">
          {currentOption.choices.map((choice: any) => (
            <button
              key={choice.id}
              onClick={() => handleSelect(choice.id)}
              className={`w-full p-6 rounded-2xl border text-left transition-all ${
                selections[currentOption.id] === choice.id
                  ? 'bg-aura/10 border-aura shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                  : 'bg-slate-900/50 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex justify-between items-center">
                <span className="font-bold">{choice.name}</span>
                <span className="text-xs font-black text-slate-400">+{choice.price} WST</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      <footer className="mt-8 pt-6 border-t border-slate-800 flex justify-between items-center">
        <div>
          <p className="text-[10px] font-black text-slate-500 uppercase">Configuration Total</p>
          <p className="text-2xl font-black">{calculateTotal().toLocaleString()} WST</p>
        </div>
        <div className="flex gap-4">
          {step > 0 && (
            <button type="button" onClick={() => setStep(step - 1)} aria-label="Previous step" className="p-4 bg-slate-800 rounded-xl text-white">
              <ChevronLeft size={24} />
            </button>
          )}
          <button
            onClick={handleNext}
            disabled={!selections[currentOption.id]}
            className={`flex items-center gap-2 px-8 py-4 rounded-xl font-bold transition-all ${
              selections[currentOption.id] ? 'bg-aura text-sovereign' : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
          >
            {step === product.options.length - 1 ? 'Deploy Infrastructure' : 'Next Step'}
            <ChevronRight size={20} />
          </button>
        </div>
      </footer>
    </div>
  );
};
