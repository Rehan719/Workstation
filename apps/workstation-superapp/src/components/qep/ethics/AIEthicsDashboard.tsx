import React from 'react';
import { Info, AlertTriangle, ShieldCheck, Activity } from 'lucide-react';

export const AIEthicsDashboard: React.FC = () => {
  const biasMetrics = [
    { type: 'Sectarian', score: 0.12, status: 'Healthy', color: 'text-emerald-400' },
    { type: 'Regional Dialect', score: 0.35, status: 'Fair', color: 'text-blue-400' },
    { type: 'Gender Representation', score: 0.08, status: 'Healthy', color: 'text-emerald-400' },
    { type: 'Accessibility (WCAG)', score: 0.05, status: 'Healthy', color: 'text-emerald-400' }
  ];

  const recentAudits = [
    { id: 'AU-001', model: 'Forge-8.5', action: 'Content Generation', status: 'Passed', timestamp: '2 mins ago' },
    { id: 'AU-002', model: 'Genome-8.5', action: 'Ontology Sync', status: 'Passed', timestamp: '15 mins ago' },
    { id: 'AU-003', model: 'Learner-8.5', action: 'Path Personalization', status: 'Passed', timestamp: '1 hour ago' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <ShieldCheck className="w-8 h-8 text-indigo-600" />
          AI Ethics & Governance
        </h2>
        <div className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase">
          Ethics Level: Sovereign
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {biasMetrics.map((metric) => (
          <div key={metric.type} className="p-4 bg-slate-50 border-2 border-slate-200 rounded-xl">
            <div className="text-xs font-bold text-slate-500 uppercase mb-1">{metric.type}</div>
            <div className={`text-2xl font-black ${metric.color}`}>{(metric.score * 100).toFixed(0)}%</div>
            <div className="flex items-center gap-1 mt-2">
               <Activity className={`w-3 h-3 ${metric.color}`} />
               <span className="text-[10px] font-bold text-slate-400 uppercase">{metric.status}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="p-6 bg-slate-900 rounded-2xl border-2 border-slate-800">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-widest">Recent Ethics Audits</h3>
        </div>
        <div className="space-y-3">
          {recentAudits.map((audit) => (
            <div key={audit.id} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700">
               <div>
                 <div className="text-xs font-bold text-slate-400 uppercase">{audit.id} • {audit.model}</div>
                 <div className="text-sm font-bold text-white">{audit.action}</div>
               </div>
               <div className="text-right">
                 <div className="text-xs font-black text-emerald-400 uppercase">{audit.status}</div>
                 <div className="text-[10px] font-bold text-slate-500">{audit.timestamp}</div>
               </div>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 bg-blue-50 border-2 border-blue-100 rounded-xl flex gap-3">
        <Info className="w-5 h-5 text-blue-600 shrink-0" />
        <p className="text-xs text-blue-800 leading-relaxed font-medium">
          The QEP v8.5 Ethics Framework automatically audits all generative and predictive models for theological, sectarian, and dialect bias. Every assessment is logged to the sovereign audit trail and available for scholar review.
        </p>
      </div>
    </div>
  );
};
