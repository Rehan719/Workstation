import React, { useState } from 'react';
import { Terminal, Key, BookOpen, Download, ShoppingBag, ShieldCheck, Cpu, Database, Server } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';
import { notImplemented } from '@workstation/ui';

export const DevPortal: React.FC = () => {
  const { theme } = useTheme();
  const isAdvanced = theme === 'advanced';
  const [apiKey, setApiKey] = useState('ws_live_0x42f...88');

  const regenerateKey = () => {
    setApiKey(`ws_live_0x${Math.random().toString(16).slice(2, 8)}...${Math.random().toString(16).slice(2, 4)}`);
  };

  return (
    <div className={`space-y-12 ${isAdvanced ? 'animate-in fade-in slide-in-from-bottom-4 duration-1000' : ''}`}>
      <header>
        <h1 className="text-4xl font-black mb-2">Unified Developer Portal</h1>
        <p className="text-slate-500">Build reactors, deploy nodes, and list products in the global marketplace.</p>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8">
         <section className={`@[440px]:col-span-2 p-8 rounded-[2.5rem] space-y-6 border transition-all duration-700 ${
           isAdvanced ? 'bg-sovereign border-aura/30 shadow-[0_0_30px_rgba(100,255,218,0.1)]' : 'bg-gradient-to-br from-aura/10 to-transparent border-white/10'
         }`}>
            <h3 className="text-xl font-bold flex items-center gap-2 italic">
               <ShieldCheck size={20} className="text-aura" />
               Quantum Security Enforced (PQC-MANDATORY)
            </h3>
            <p className="text-sm text-slate-400">All third-party reactors must implement CRYSTALS-Dilithium for instruction signing. Classical fallbacks are disabled federation-wide.</p>
         </section>
         <div className={`p-8 rounded-[2.5rem] border flex flex-col items-center justify-center text-center group cursor-pointer transition-all ${
           isAdvanced ? 'bg-sovereign border-aura/30 hover:border-aura' : 'bg-slate-900 border-slate-800 hover:border-aura'
         }`}>
            <ShoppingBag size={32} className="text-highlight mb-4 group-hover:scale-110 transition-transform" />
            <h4 className="font-bold">Marketplace Console</h4>
            <p className="text-[10px] text-slate-500 mt-2">Manage your BTO listings and resonance revenue.</p>
         </div>
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-12">
        <section className={`p-8 rounded-3xl border space-y-8 transition-all duration-700 ${
          isAdvanced ? 'bg-sovereign border-aura/30' : 'bg-slate-900/40 border-slate-800'
        }`}>
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Key size={20} className="text-aura" />
            API Keys
          </h3>
          <div className={`p-6 rounded-2xl border transition-all ${
            isAdvanced ? 'bg-sovereign border-aura/20' : 'bg-slate-800/30 border-slate-700'
          }`}>
             <p className="text-xs text-slate-500 mb-4">Production Key: {apiKey}</p>
             <button type="button" onClick={regenerateKey} className="text-xs font-black text-aura uppercase hover:underline">Regenerate Key</button>
          </div>
        </section>

        <section className={`p-8 rounded-3xl border space-y-8 transition-all duration-700 ${
          isAdvanced ? 'bg-sovereign border-aura/30' : 'bg-slate-900/40 border-slate-800'
        }`}>
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Download size={20} className="text-highlight" />
            Ecosystem SDKs
          </h3>
          <div className="space-y-4">
             <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl">
                <span className="font-bold">Workstation JS SDK</span>
                <span className="text-[10px] font-black text-slate-500 bg-slate-900 px-2 py-0.5 rounded border border-slate-700">v1.0.4</span>
             </div>
             <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl">
                <span className="font-bold">Workstation Python SDK</span>
                <span className="text-[10px] font-black text-slate-500 bg-slate-900 px-2 py-0.5 rounded border border-slate-700">v0.8.2</span>
             </div>
             <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl">
                <div className="flex flex-col gap-1">
                  <span className="font-bold">Workstation Go SDK</span>
                  <span className="text-[10px] text-slate-500">Edge Node & Telemetry Ingestion</span>
                </div>
                <span className="text-[10px] font-black text-aura bg-aura/10 px-2 py-0.5 rounded border border-aura/20">ALPHA</span>
             </div>
             <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl">
                <div className="flex flex-col gap-1">
                  <span className="font-bold">Workstation Rust SDK</span>
                  <span className="text-[10px] text-slate-500">PQC Handshakes & Sovereign Runtimes</span>
                </div>
                <span className="text-[10px] font-black text-aura bg-aura/10 px-2 py-0.5 rounded border border-aura/20">ALPHA</span>
             </div>
             <div className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl">
                <div className="flex flex-col gap-1">
                  <span className="font-bold">Workstation Java SDK</span>
                  <span className="text-[10px] text-slate-500">Enterprise Integration (Spring/Kafka)</span>
                </div>
                <span className="text-[10px] font-black text-aura bg-aura/10 px-2 py-0.5 rounded border border-aura/20">ALPHA</span>
             </div>
          </div>
        </section>
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-8">
        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-64 flex flex-col items-center justify-center text-center">
          <BookOpen size={48} className="text-slate-700 mb-4" />
          <h3 className="text-xl font-bold mb-2">SDK Documentation & Tutorials</h3>
          <p className="text-slate-500 max-w-md">Learn how to build custom reactors and BTO products using our comprehensive guides.</p>
        </section>
        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-64 flex flex-col items-center justify-center text-center border-dashed border-aura/30 group hover:border-aura transition-all">
          <Terminal size={48} className="text-aura/50 group-hover:text-aura mb-4 transition-colors" />
          <h3 className="text-xl font-bold mb-2">Enterprise Developer Program</h3>
          <p className="text-slate-500 max-w-md">Apply for dedicated support, custom deployment blueprints, and higher marketplace visibility.</p>
          <button type="button" onClick={() => notImplemented('Apply Now')} className="mt-4 text-[10px] font-black text-aura uppercase tracking-widest border border-aura/30 px-4 py-2 rounded-lg hover:bg-aura/10">Apply Now</button>
        </section>
      </div>
    </div>
  );
};
