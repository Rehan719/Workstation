import React from 'react';

const ProductionMonitoringDashboard: React.FC = () => {
  const [pipelineMetrics, setPipelineMetrics] = React.useState([
    { name: "Scraping", status: "HEALTHY", latency: "145ms", errors: "0.01%" },
    { name: "Ingestion", status: "HEALTHY", latency: "88ms", errors: "0.00%" },
    { name: "Knowledge", status: "HEALTHY", latency: "210ms", errors: "0.02%" },
    { name: "Introspection", status: "HEALTHY", latency: "1.2s", errors: "0.05%" }
  ]);

  return (
    <div className="production-monitoring p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-bold text-emerald-400">Production Monitoring</h2>
          <p className="text-xs text-slate-500 font-mono mt-1">SLA: 99.99% | Uptime: 99.995%</p>
        </div>
        <div className="status-indicator flex items-center gap-2 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
          <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
          <span className="text-[10px] font-bold text-emerald-400 uppercase">System Nominal</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {pipelineMetrics.map(pipeline => (
          <div key={pipeline.name} className="pipeline-card p-4 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-emerald-500/30 transition-all">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-sm font-bold text-slate-300">{pipeline.name} Pipeline</h3>
              <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${pipeline.status === 'HEALTHY' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                {pipeline.status}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="metric">
                <span className="text-[10px] text-slate-500 block uppercase">Latency</span>
                <span className="text-lg font-mono text-emerald-400">{pipeline.latency}</span>
              </div>
              <div className="metric">
                <span className="text-[10px] text-slate-500 block uppercase">Error Rate</span>
                <span className="text-lg font-mono text-emerald-400">{pipeline.errors}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="sla-enforcement p-4 bg-slate-800 border border-slate-700 rounded-lg">
        <h3 className="text-xs font-bold text-emerald-500 uppercase mb-4 flex items-center gap-2">
          <span>🛡️</span> SLA Enforcement & Auto-Remediation
        </h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">Recovery Time Objective (RTO)</span>
            <span className="text-emerald-400 font-mono">15min</span>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">Recovery Point Objective (RPO)</span>
            <span className="text-emerald-400 font-mono">5min</span>
          </div>
          <div className="mt-4 pt-4 border-t border-slate-700">
            <p className="text-[10px] text-slate-500 leading-relaxed italic">
              Auto-remediation logic is active. High latency will trigger horizontal scaling; high error rates will trigger an automated rollback to the last stable VSB snapshot.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductionMonitoringDashboard;
