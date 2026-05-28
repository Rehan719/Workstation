import React from 'react';
import { Globe, Shield, Zap, Users, ArrowRight } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';

export const LandingPage: React.FC = () => {
  const { theme } = useTheme();
  const isAdvanced = theme === 'advanced';

  return (
    <div className={`min-h-screen bg-sovereign text-white ${isAdvanced ? 'font-mono' : 'font-sans'}`}>
      {/* Hero Section */}
      <section className="relative h-screen flex flex-col items-center justify-center text-center p-6 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-aura/5 to-transparent"></div>
        <div className="relative z-10 space-y-8 max-w-4xl">
           <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-none animate-in fade-in slide-in-from-top-10 duration-1000">
             THE GLOBAL <span className="text-aura">CIVILIZATION</span> INTERFACE
           </h1>
           <p className="text-xl md:text-2xl text-slate-400 font-bold max-w-2xl mx-auto">
             Scale your digital sovereignty. Connect to millions of nodes. Build your own realms.
           </p>
           <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="px-10 py-5 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all text-xl shadow-[0_0_50px_rgba(100,255,218,0.3)]">
                Launch My Node
              </button>
              <button className="px-10 py-5 bg-white/5 border border-white/10 backdrop-blur-xl font-black rounded-2xl hover:bg-white/10 transition-all text-xl">
                Explore the Federation
              </button>
           </div>
        </div>

        {/* Scalability Badge */}
        <div className="absolute bottom-10 flex items-center gap-4 px-6 py-3 bg-slate-900/50 border border-white/10 rounded-full backdrop-blur-2xl">
           <Users size={20} className="text-aura" />
           <span className="text-sm font-bold tracking-widest uppercase">1,042,000 Concurrent Guardians</span>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-32 px-6 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
         <FeatureCard
            icon={Globe}
            title="Massive Federation"
            desc="Optimized for 10,000+ sovereign nodes and millions of users."
         />
         <FeatureCard
            icon={Shield}
            title="Quantum-Safe"
            desc="PQC-mandatory security protocols protect your digital civilization."
         />
         <FeatureCard
            icon={Zap}
            title="M7 Integrated"
            desc="Native AI synthesis from OpenAI, Google, Meta, and NVIDIA."
         />
      </section>
    </div>
  );
};

const FeatureCard = ({ icon: Icon, title, desc }: any) => (
  <div className="p-10 rounded-[3rem] bg-slate-900/40 border border-white/5 hover:border-aura/30 transition-all group">
     <div className="w-16 h-16 rounded-2xl bg-aura/10 flex items-center justify-center text-aura mb-8 group-hover:scale-110 transition-transform">
        <Icon size={32} />
     </div>
     <h3 className="text-2xl font-black mb-4">{title}</h3>
     <p className="text-slate-500 font-bold leading-relaxed">{desc}</p>
  </div>
);
