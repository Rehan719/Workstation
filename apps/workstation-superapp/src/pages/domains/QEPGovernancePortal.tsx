import React from 'react';
import { DAOGovernanceInterface } from '../../components/qep/dao/DAOGovernanceInterface';
import { AIEthicsDashboard } from '../../components/qep/ethics/AIEthicsDashboard';
import { toast } from '@workstation/ui';

export const QEPGovernancePortal: React.FC = () => {
  const exportReusabilityKit = () => {
    const payload = {
      framework: 'Sovereign State v99.0',
      exported_at: new Date().toISOString(),
      note: 'Decentralized governance + AI ethics auditing reusability kit',
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'reusability-kit.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-10 space-y-12 bg-white min-h-screen">
      <div className="max-w-7xl mx-auto space-y-16">
        <section>
          <DAOGovernanceInterface />
        </section>

        <section className="pt-12 border-t-2 border-slate-100">
          <AIEthicsDashboard />
        </section>

        <section className="p-8 bg-indigo-50 border-2 border-indigo-100 rounded-3xl text-center space-y-4">
           <div className="inline-block p-3 bg-indigo-100 rounded-full mb-2">
             <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white font-black text-xl">v8.5</div>
           </div>
           <h3 className="text-2xl font-black text-indigo-900 uppercase tracking-tighter">Sovereign Signature Compliance</h3>
           <p className="text-indigo-700 text-sm font-medium max-w-2xl mx-auto leading-relaxed">
             This portal demonstrates the integration of decentralized governance and automated AI ethics auditing. Every proposal, vote, and ethics assessment is verified against the Sovereign State v99.0 framework and logged to the immutable VSB signature trail.
           </p>
           <div className="flex gap-4 justify-center pt-4">
             <button type="button" onClick={async () => { try { const r = await fetch('/api/v1/qep/compliance/audit'); const d = await r.json(); toast(`Compliance: ${d.compliant ? 'PASS' : 'REVIEW'} · ${d.checks?.length ?? 0} controls`); } catch { toast('Audit failed'); } }} className="px-6 py-2 bg-indigo-600 text-white text-xs font-black uppercase rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200">
               View Compliance Audit
             </button>
             <button type="button" onClick={exportReusabilityKit} className="px-6 py-2 bg-white text-indigo-600 border-2 border-indigo-200 text-xs font-black uppercase rounded-xl hover:border-indigo-400 transition-colors">
               Export Reusability Kit
             </button>
           </div>
        </section>
      </div>
    </div>
  );
};
