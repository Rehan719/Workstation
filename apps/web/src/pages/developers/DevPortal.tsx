import React from 'react';
import { Terminal, Key, BookOpen, Download, ShoppingBag, ShieldCheck } from 'lucide-react';

export const DevPortal: React.FC = () => {
  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-black mb-2">Unified Developer Portal</h1>
        <p className="text-slate-500">Build reactors, deploy nodes, and list products in the global marketplace.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         <section className="lg:col-span-2 p-8 rounded-[2.5rem] bg-gradient-to-br from-aura/10 to-transparent border border-white/10 space-y-6">
            <h3 className="text-xl font-bold flex items-center gap-2 italic">
               <ShieldCheck size={20} className="text-aura" />
               Quantum Security Enforced (PQC-MANDATORY)
            </h3>
            <p className="text-sm text-slate-400">All third-party reactors must implement CRYSTALS-Dilithium for instruction signing. Classical fallbacks are disabled federation-wide.</p>
         </section>
         <div className="p-8 rounded-[2.5rem] bg-slate-900 border border-slate-800 flex flex-col items-center justify-center text-center group cursor-pointer hover:border-aura transition-all">
            <ShoppingBag size={32} className="text-highlight mb-4 group-hover:scale-110 transition-transform" />
            <h4 className="font-bold">Marketplace Console</h4>
            <p className="text-[10px] text-slate-500 mt-2">Manage your BTO listings and resonance revenue.</p>
         </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-8">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Key size={20} className="text-aura" />
            API Keys
          </h3>
          <div className="p-6 bg-slate-800/30 rounded-2xl border border-slate-700">
             <p className="text-xs text-slate-500 mb-4">Production Key: ws_live_0x42f...88</p>
             <button className="text-xs font-black text-aura uppercase hover:underline">Regenerate Key</button>
          </div>
        </section>

        <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-8">
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
          </div>
        </section>
      </div>

      <section className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-64 flex flex-col items-center justify-center text-center">
         <BookOpen size={48} className="text-slate-700 mb-4" />
         <h3 className="text-xl font-bold mb-2">SDK Documentation & Tutorials</h3>
         <p className="text-slate-500 max-w-md">Learn how to build custom reactors and BTO products using our comprehensive guides.</p>
      </section>
    </div>
  );
};
