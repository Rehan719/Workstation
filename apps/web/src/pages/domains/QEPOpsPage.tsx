import React from 'react';
import {
  Server,
  Terminal,
  AlertTriangle,
  Cpu,
  Zap,
  Database,
  CloudLightning,
  CheckCircle2
} from 'lucide-react';

const QEPOpsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0A0B10] text-white p-8">
      <header className="mb-12 flex justify-between items-center">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Server className="text-[#00FF85]" size={24} />
            <span className="text-[#00FF85] font-mono tracking-widest text-sm uppercase">Production Operations Center</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight">System Infrastructure & SLA Status</h1>
          <p className="text-slate-400 mt-2">Sovereign State Monitoring v8.6 — Real-time Infrastructure & Auto-Remediation Logs</p>
        </div>
        <div className="bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-lg flex items-center gap-3">
          <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-emerald-500 font-mono text-sm">SYSTEMS: OPERATIONAL</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {[
          { icon: <Cpu />, label: 'CPU Usage', value: '42%', color: 'text-blue-400' },
          { icon: <Database />, label: 'Storage', value: '1.2TB', color: 'text-purple-400' },
          { icon: <CloudLightning />, label: 'Latency', value: '152ms', color: 'text-[#00FF85]' },
          { icon: <Zap />, label: 'Throughput', value: '1.4k rps', color: 'text-amber-400' },
        ].map((stat, idx) => (
          <div key={idx} className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
            <div className="flex items-center gap-3 mb-2 text-slate-500">
              {React.cloneElement(stat.icon as React.ReactElement, { size: 16 })}
              <span className="text-sm font-medium">{stat.label}</span>
            </div>
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl h-96 relative overflow-hidden">
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <Terminal size={20} className="text-[#00FF85]" />
              Real-time Sovereign Audit Trail
            </h3>
            <div className="font-mono text-xs space-y-3 overflow-y-auto h-64 p-4 bg-black/50 rounded-lg">
              <p className="text-emerald-500">[2026-04-03 21:05:12] INFO: AI Path Optimizer deployed successfully (v8.6.0)</p>
              <p className="text-blue-400">[2026-04-03 21:05:45] METRIC: Throughput reached 1.2k rps. Scaled +2 nodes.</p>
              <p className="text-amber-400">[2026-04-03 21:06:01] WARN: Latency spike detected (245ms). Clearing CDN edge cache.</p>
              <p className="text-emerald-400">[2026-04-03 21:06:15] AUTO_REMEDIATION: Cache clear complete. Latency normalized to 152ms.</p>
              <p className="text-slate-500">[2026-04-03 21:07:00] INFO: Privacy preserving noise injected into analytics stream.</p>
              <p className="text-emerald-500">[2026-04-03 21:07:30] AUDIT: Differential privacy budget updated (ε=0.42).</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <AlertTriangle size={20} className="text-amber-500" />
              Recent Incident Log
            </h3>
            <div className="space-y-4">
              {[
                { type: 'Latency Spike', time: '5m ago', status: 'Resolved' },
                { type: 'Storage Alert', time: '1h ago', status: 'Healthy' },
                { type: 'SLA Breach (Error Rate)', time: '3h ago', status: 'Resolved' },
              ].map((incident, idx) => (
                <div key={idx} className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg border border-slate-800">
                  <div>
                    <div className="font-medium text-sm">{incident.type}</div>
                    <div className="text-[10px] text-slate-500 uppercase font-mono">{incident.time}</div>
                  </div>
                  <div className="flex items-center gap-1.5 text-emerald-500 text-xs font-mono uppercase">
                    <CheckCircle2 size={12} />
                    {incident.status}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-4 text-emerald-500">Auto-Scaling Events</h3>
            <p className="text-xs text-slate-400 mb-6 font-mono tracking-wider italic">
              AI-driven infrastructure optimization active.
            </p>
            <div className="space-y-6 relative ml-4 border-l border-slate-800 pl-6 py-2">
              {[
                { time: '12:45', action: '+2 nodes added', reason: 'High throughput (1.5k rps)' },
                { time: '14:20', action: 'CDN Edge Refresh', reason: 'Latency spike > 250ms' },
                { time: '16:05', action: 'DB Instance Scaled', reason: 'Storage query latency detected' },
              ].map((evt, idx) => (
                <div key={idx} className="relative">
                   <div className="absolute -left-[30px] top-1 h-2 w-2 rounded-full bg-emerald-500 ring-4 ring-[#15171E]"></div>
                   <div className="font-bold text-xs font-mono">{evt.time}</div>
                   <div className="text-sm font-semibold">{evt.action}</div>
                   <div className="text-[10px] text-slate-500 italic mt-0.5">{evt.reason}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QEPOpsPage;
