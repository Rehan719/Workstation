import React from 'react';
import { Card, Button } from '@workstation/ui';
import { QEPDashboard } from '../components/QEPDashboard';
import { Sparkles, ArrowRight, Shield, Globe, Cpu } from 'lucide-react';

export const QEPLanding: React.FC = () => {
  const launchQEP = () => {
    // In a real environment, this might reload with the env flag
    // or just navigate to the dashboard in standalone mode
    window.location.href = '/domains/religion/qep';
  };

  return (
    <div className="min-h-screen bg-sovereign text-white overflow-hidden selection:bg-aura selection:text-sovereign">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_top_right,rgba(100,255,218,0.05)_0%,transparent_50%)] pointer-events-none"></div>

      <nav className="p-10 flex justify-between items-center relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-aura flex items-center justify-center text-sovereign font-black shadow-lg shadow-aura/20">Q</div>
          <span className="font-black text-xl tracking-tighter uppercase">QEP Flagship</span>
        </div>
        <div className="flex gap-8 text-[10px] font-black uppercase tracking-widest text-slate-500">
          <a href="#" className="hover:text-aura transition-all">Engines</a>
          <a href="#" className="hover:text-aura transition-all">Governance</a>
          <a href="#" className="hover:text-aura transition-all">Documentation</a>
        </div>
      </nav>

      <main className="relative z-10 container mx-auto px-10 pt-20 pb-40">
        <div className="max-w-4xl">
          <Badge color="aura" className="mb-6">v0.8 Sovereign Product</Badge>
          <h1 className="text-8xl font-black mb-8 tracking-tighter leading-[0.9]">
            The Quadruple <br />
            <span className="text-aura">Engine Pillar.</span>
          </h1>
          <p className="text-xl text-slate-400 font-bold max-w-2xl leading-relaxed mb-12">
            A premier free offering from the Virtual Sovereign Business. Advanced simulation, resource optimisation, and team orchestration tailored for the Religion Domain.
          </p>

          <div className="flex gap-6">
            <Button onClick={launchQEP} className="bg-aura text-sovereign px-10 py-8 rounded-2xl text-lg font-black uppercase tracking-widest shadow-2xl shadow-aura/30 flex items-center gap-4 group">
              Launch QEP Flagship
              <ArrowRight size={24} className="group-hover:translate-x-2 transition-transform" />
            </Button>
            <Button variant="outline" className="px-10 py-8 rounded-2xl text-lg font-black uppercase tracking-widest">
              View Specs
            </Button>
          </div>
        </div>

        <div className="mt-40 grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="space-y-6">
            <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
              <Cpu size={28} />
            </div>
            <h3 className="text-2xl font-black uppercase tracking-tight">Sovereign AI Core</h3>
            <p className="text-slate-500 font-bold leading-relaxed">Powered by the AI CEO and the Workstation v0.8 infrastructure for unparalleled reasoning depth.</p>
          </div>
          <div className="space-y-6">
            <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
              <Globe size={28} />
            </div>
            <h3 className="text-2xl font-black uppercase tracking-tight">Interfaith Mesh</h3>
            <p className="text-slate-500 font-bold leading-relaxed">Integrated with global spiritual networks and sacred ontologies for cross-domain synthesis.</p>
          </div>
          <div className="space-y-6">
            <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
              <Shield size={28} />
            </div>
            <h3 className="text-2xl font-black uppercase tracking-tight">GaaS Verified</h3>
            <p className="text-slate-500 font-bold leading-relaxed">Strict adherence to the 1127-article Constitution, ensuring ethical alignment in every simulation.</p>
          </div>
        </div>
      </main>

      <footer className="p-20 border-t border-slate-900 text-center relative z-10">
        <p className="text-[10px] font-black text-slate-700 uppercase tracking-[0.5em]">Virtual Sovereign Business • QEP-Religion v0.8</p>
      </footer>
    </div>
  );
};
