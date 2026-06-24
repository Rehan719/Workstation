import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { Card, Badge } from '@workstation/ui';
import { Cpu, HardDrive, MemoryStick, Server, Activity, Loader2, AlertTriangle, Layers, CheckCircle2 } from 'lucide-react';

interface CtoMetrics {
  cpu_percent: number;
  memory_percent: number;
  memory_used_gb: number;
  disk_percent: number;
  active_projects: number;
  total_projects: number;
  total_outputs: number;
  uptime: string;
}

function GaugeBar({ pct, color }: { pct: number; color: string }) {
  return (
    <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
      <div className={`h-full rounded-full transition-all duration-700 ${color}`} style={{ width: `${Math.min(pct, 100)}%` }} />
    </div>
  );
}

function healthColor(pct: number): string {
  if (pct > 85) return 'bg-vital';
  if (pct > 65) return 'bg-amber-500';
  return 'bg-emerald-500';
}

export const CTO: React.FC = () => {
  const { data: metrics, isLoading, isError } = useQuery<CtoMetrics>({
    queryKey: ['cto-infra'],
    queryFn:  () => axios.get<CtoMetrics>('/api/csuite/cto/infrastructure').then(r => r.data),
    refetchInterval: 15_000,
    staleTime: 10_000,
    retry: 1,
    refetchOnWindowFocus: false,
  });

  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 15_000);
    return () => clearInterval(id);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center gap-3 py-20 text-slate-500">
        <Loader2 className="animate-spin" size={20} />
        Loading infrastructure metrics…
      </div>
    );
  }

  if (isError || !metrics) {
    return (
      <div className="flex items-center gap-3 py-20 text-slate-500">
        <AlertTriangle size={20} className="text-amber-500" />
        Backend offline — start the API server to see live infrastructure data.
      </div>
    );
  }

  const gauges = [
    { icon: Cpu,        label: 'CPU Usage',      pct: metrics.cpu_percent,    suffix: '%', detail: `${(100 - metrics.cpu_percent).toFixed(1)}% headroom` },
    { icon: MemoryStick,label: 'Memory',         pct: metrics.memory_percent, suffix: '%', detail: `${metrics.memory_used_gb} GB used` },
    { icon: HardDrive,  label: 'Disk',           pct: metrics.disk_percent,   suffix: '%', detail: `${(100 - metrics.disk_percent).toFixed(1)}% free` },
  ];

  const portfolio = [
    { label: 'Total Projects',   value: metrics.total_projects,  icon: Layers },
    { label: 'Active Workflows', value: metrics.active_projects,  icon: Activity },
    { label: 'AI Outputs',       value: metrics.total_outputs,    icon: CheckCircle2 },
  ];

  return (
    <div className="space-y-10">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-4">
        <div>
          <h1 className="text-4xl @[680px]:text-6xl font-black text-white tracking-tighter uppercase">CTO Infrastructure</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em] mt-1">
            Live System Vitals · Refreshes every 15 s
          </p>
        </div>
        <Badge color="emerald-500" className="self-start @[480px]:self-auto">
          Uptime {metrics.uptime}
        </Badge>
      </header>

      {/* System Resource Gauges */}
      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-6">
        {gauges.map(({ icon: Icon, label, pct, suffix, detail }) => (
          <Card key={label} className="p-8 space-y-6 bg-slate-950 border-slate-800">
            <div className="flex justify-between items-start">
              <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                <Icon size={24} />
              </div>
              <span className={`text-3xl font-black ${pct > 85 ? 'text-vital' : pct > 65 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {pct.toFixed(1)}{suffix}
              </span>
            </div>
            <div>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3">{label}</p>
              <GaugeBar pct={pct} color={healthColor(pct)} />
              <p className="text-xs text-slate-600 mt-2 font-bold">{detail}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* Portfolio Stats */}
      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-6">
        {portfolio.map(({ label, value, icon: Icon }) => (
          <Card key={label} className="p-8 flex items-center gap-6 bg-slate-950 border-slate-800">
            <div className="w-14 h-14 rounded-2xl bg-aura/10 flex items-center justify-center text-aura flex-shrink-0">
              <Icon size={28} />
            </div>
            <div>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">{label}</p>
              <p className="text-4xl font-black text-white">{value}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* System services */}
      <Card className="p-8 bg-slate-950 border-slate-800">
        <h3 className="text-lg font-black text-white uppercase tracking-tight mb-6 flex items-center gap-3">
          <Server size={20} className="text-aura" /> Services
        </h3>
        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-4">
          {[
            { name: 'FastAPI (app_mvp)',   status: 'RUNNING',  note: 'Spine: 11 routers' },
            { name: 'AI Gateway (Claude)', status: 'ONLINE',   note: 'Anthropic → OpenAI → Ollama' },
            { name: 'Synthesis Pipeline',  status: 'RUNNING',  note: 'SSE streaming enabled' },
            { name: 'Project Store',       status: 'RUNNING',  note: `${metrics.total_projects} projects persisted` },
            { name: 'Realms Registry',     status: 'RUNNING',  note: 'Discover + create endpoints live' },
            { name: 'Vitals WebSocket',    status: 'RUNNING',  note: 'Real psutil broadcasts @ 5 s' },
          ].map(svc => (
            <div key={svc.name} className="flex items-center justify-between p-4 rounded-2xl bg-slate-900 border border-slate-800">
              <div>
                <p className="font-black text-white text-sm">{svc.name}</p>
                <p className="text-[10px] text-slate-500 font-bold">{svc.note}</p>
              </div>
              <span className="text-[10px] font-black text-emerald-400 uppercase">{svc.status}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
