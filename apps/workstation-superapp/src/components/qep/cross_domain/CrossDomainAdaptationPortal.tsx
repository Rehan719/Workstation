import React from 'react';

const CrossDomainAdaptationPortal: React.FC = () => {
  const [targetDomains, setTargetDomains] = React.useState([
    { id: "science", name: "Science", status: "ADAPTED", mechanisms: 12, validation: "PASSED" },
    { id: "law", name: "Law", status: "ADAPTED", mechanisms: 8, validation: "PASSED" },
    { id: "employment", name: "Employment", status: "ADAPTED", mechanisms: 15, validation: "PASSED" },
    { id: "care", name: "Care", status: "ADAPTED", mechanisms: 10, validation: "PASSED" }
  ]);

  return (
    <div className="cross-domain-adaptation p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-bold text-emerald-400">Cross-Domain Adaptation</h2>
          <p className="text-xs text-slate-500 font-mono mt-1">v8.4 Sovereign Signature Mechanism Exchange</p>
        </div>
        <div className="status-indicator flex items-center gap-2 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
          <span className="text-lg">🌐</span>
          <span className="text-[10px] font-bold text-emerald-400 uppercase">Interoperable</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {targetDomains.map(domain => (
          <div key={domain.id} className="domain-card p-5 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-emerald-500/50 transition-all cursor-pointer group">
            <div className="flex justify-between items-start mb-6">
              <h3 className="text-lg font-bold group-hover:text-emerald-400 transition-colors">VSB::{domain.name}</h3>
              <span className={`text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded border border-emerald-500/20`}>{domain.status}</span>
            </div>
            <div className="space-y-3 mb-6">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500 uppercase font-bold tracking-wider">Adapted Mechanisms</span>
                <span className="text-emerald-400 font-mono">{domain.mechanisms}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500 uppercase font-bold tracking-wider">Validation Status</span>
                <span className="text-emerald-400 font-mono">{domain.validation}</span>
              </div>
            </div>
            <button className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded transition-colors text-xs border border-slate-700">
              Explore Adapted Plugins
            </button>
          </div>
        ))}
      </div>

      <div className="adaptation-workflow p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-lg">
        <h4 className="text-emerald-400 font-bold mb-4 text-sm flex items-center gap-2">
          <span>⚙️</span> Adaptation Workflow
        </h4>
        <ol className="space-y-3">
          {[
            "Analyze QEP v8.4 mechanisms",
            "Identify target domain constraints",
            "Execute automated adaptation scripts",
            "Validate compatibility & publish"
          ].map((step, i) => (
            <li key={i} className="flex items-center gap-3 text-xs text-slate-400">
              <span className="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center text-emerald-500 font-bold font-mono border border-slate-700">{i+1}</span>
              {step}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default CrossDomainAdaptationPortal;
