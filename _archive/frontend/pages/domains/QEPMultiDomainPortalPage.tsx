import React, { useState } from 'react';
import { Network, Globe, Layers, BookOpen, Scale, Briefcase, HeartPulse, Microscope, ChevronRight, Activity, Share2, ShieldCheck } from 'lucide-react';

export const QEPMultiDomainPortal: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState<string | null>('Science');

  const domainIntegrations = [
    { name: 'Science', icon: <Microscope className="w-5 h-5" />, status: 'Federated', activeMechanisms: 12, compatibility: '98.5%', color: 'border-blue-200 text-blue-600 bg-blue-50' },
    { name: 'Law', icon: <Scale className="w-5 h-5" />, status: 'Federated', activeMechanisms: 8, compatibility: '99.1%', color: 'border-slate-200 text-slate-600 bg-slate-50' },
    { name: 'Employment', icon: <Briefcase className="w-5 h-5" />, status: 'Syncing', activeMechanisms: 15, compatibility: '95.8%', color: 'border-emerald-200 text-emerald-600 bg-emerald-50' },
    { name: 'Care', icon: <HeartPulse className="w-5 h-5" />, status: 'Federated', activeMechanisms: 5, compatibility: '97.2%', color: 'border-rose-200 text-rose-600 bg-rose-50' }
  ];

  const mechanisms = [
    { name: 'Ontology Engine v1.2', type: 'Knowledge', status: 'Approved', pipeline: 'Genome' },
    { name: 'Audit Trail Manager v2.1', type: 'Governance', status: 'Approved', pipeline: 'Introspection' },
    { name: 'Adaptive Learning Core v3.0', type: 'Pedagogy', status: 'Review', pipeline: 'Learner' }
  ];

  const exportMechanisms = () => {
    const blob = new Blob([JSON.stringify({ target_domain: selectedDomain, mechanisms }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mechanisms-to-${selectedDomain || 'domain'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <Network className="w-8 h-8 text-indigo-600" />
          Multi-Domain Federation
        </h2>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1 text-[10px] font-black text-slate-500 uppercase">
             <Activity className="w-4 h-4 text-emerald-500" />
             Federation Health: Stable
          </div>
          <div className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase tracking-widest">
            v8.7 Sovereign Signature
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-4 gap-4">
        {domainIntegrations.map((domain) => (
          <div
            key={domain.name}
            className={`p-5 rounded-2xl border-2 transition-all cursor-pointer shadow-sm ${selectedDomain === domain.name ? 'border-indigo-500 bg-white ring-4 ring-indigo-50' : 'border-slate-100 bg-white hover:border-indigo-200'}`}
            onClick={() => setSelectedDomain(domain.name)}
          >
            <div className="flex justify-between items-start mb-4">
               <div className={`p-2 rounded-lg ${domain.color}`}>
                  {domain.icon}
               </div>
               <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  {domain.status}
               </div>
            </div>
            <div className="text-xl font-black text-slate-800 uppercase tracking-tighter">{domain.name} Domain</div>
            <div className="grid grid-cols-2 gap-2 mt-4 pt-4 border-t border-slate-100">
               <div>
                  <div className="text-[10px] font-bold text-slate-400 uppercase">Mechanisms</div>
                  <div className="text-sm font-black text-slate-700">{domain.activeMechanisms} Active</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-slate-400 uppercase">Compatibility</div>
                  <div className="text-sm font-black text-slate-700">{domain.compatibility}</div>
               </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-6">
        <div className="@[440px]:col-span-2 space-y-6">
          <div className="p-8 bg-white border-2 border-slate-100 rounded-3xl shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
               <div className="flex items-center gap-2">
                  <Share2 className="w-6 h-6 text-indigo-600" />
                  <h3 className="text-sm font-black uppercase tracking-widest text-slate-800">Shared Mechanism Exchange ({selectedDomain})</h3>
               </div>
               <button type="button" onClick={exportMechanisms} className="text-[10px] font-black text-indigo-600 uppercase hover:text-indigo-800 transition-colors">
                  Export Mechanism to {selectedDomain}
               </button>
            </div>

            <div className="space-y-4">
               {mechanisms.map((mechanism) => (
                 <div key={mechanism.name} className="p-4 bg-slate-50 border border-slate-200 rounded-2xl flex items-center justify-between hover:border-indigo-400 group cursor-pointer transition-all">
                    <div className="flex items-center gap-4">
                       <div className="p-3 bg-white border border-slate-200 rounded-xl">
                          <Layers className="w-5 h-5 text-slate-400 group-hover:text-indigo-600" />
                       </div>
                       <div>
                          <div className="text-sm font-black text-slate-800 group-hover:text-indigo-600">{mechanism.name}</div>
                          <div className="text-[10px] font-bold text-slate-400 uppercase">{mechanism.type} • Source: {mechanism.pipeline} Realm</div>
                       </div>
                    </div>
                    <div className="flex items-center gap-4">
                       <div className="px-3 py-1 bg-indigo-100 text-indigo-700 text-[10px] font-black rounded-full uppercase tracking-widest">
                          {mechanism.status}
                       </div>
                       <ChevronRight className="w-5 h-5 text-slate-300" />
                    </div>
                 </div>
               ))}
            </div>

            <div className="p-6 bg-indigo-50 border-2 border-indigo-100 rounded-2xl">
               <div className="flex items-center gap-2 mb-3">
                  <ShieldCheck className="w-5 h-5 text-indigo-600" />
                  <span className="text-xs font-black text-indigo-900 uppercase">AI-Powered Adaptation Blueprint</span>
               </div>
               <p className="text-xs text-indigo-700 font-medium leading-relaxed">
                  "The 'Ontology Engine' is currently undergoing automated mapping to the {selectedDomain} domain concept hierarchy. Compatibility validation score predicted at 98.2% after regional norm adjustments."
               </p>
            </div>
          </div>
        </div>

        <div className="p-6 bg-slate-900 rounded-2xl border-2 border-slate-800 space-y-6">
          <div className="flex items-center gap-2 text-indigo-400">
             <Globe className="w-6 h-6" />
             <h3 className="text-xs font-black uppercase tracking-widest text-white">Federation Registry</h3>
          </div>
          <div className="space-y-4">
             {[
               { domain: 'Science', node: 'SCI-FED-01', health: '99.9%', latency: '12ms' },
               { domain: 'Law', node: 'LAW-FED-01', health: '100%', latency: '8ms' },
               { domain: 'Employment', node: 'EMP-FED-01', health: '98.5%', latency: '25ms' },
               { domain: 'Care', node: 'CARE-FED-01', health: '99.7%', latency: '15ms' }
             ].map((node) => (
               <div key={node.domain} className="p-3 bg-slate-800/50 border border-slate-700 rounded-xl">
                  <div className="flex justify-between items-center mb-2">
                     <div className="text-xs font-black text-white uppercase">{node.domain} Node</div>
                     <div className="text-[10px] font-black text-emerald-400 uppercase tracking-widest">{node.health} Up</div>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-bold text-slate-500 uppercase">
                     <span>ID: {node.node}</span>
                     <span>Latency: {node.latency}</span>
                  </div>
               </div>
             ))}
          </div>
          <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
             <div className="text-[10px] font-black text-indigo-300 uppercase mb-2 flex items-center gap-1">
                <BookOpen className="w-3 h-3" /> Cross-Domain Pattern
             </div>
             <p className="text-[10px] text-slate-400 font-medium leading-relaxed italic">
                Pattern-first reusability confirmed: 82% of QEP v8.7 core mechanisms are successfully federated across all 4 target domains.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
};
