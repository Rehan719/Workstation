import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Search, Database, Cpu, Send, LayoutGrid, CheckCircle2, AlertCircle, Loader2, RefreshCw, Activity } from 'lucide-react';
import { Card, Button } from '@workstation/ui';

interface OrganismMetrics {
  composite_health: number;
  mode: string;
  systems: {
    immune:       { health: number; threat_level: string; errors_in_window: number };
    nervous:      { signals_last_60s: number; arousal_state: string; signal_rate_per_second: number };
    self_healing: { overall_health: number; open_circuits: number };
    metabolic:    { atp_ratio: number };
    reconfiguration: { rpm_limit: number; preferred_provider: string };
  };
}

function engineStatus(name: string, value: number): string {
  if (name === 'Discovery') return value > 50 ? 'Scanning Signal Mesh' : value > 0 ? 'Low Signal Flow' : 'Idle';
  if (name === 'Ingestion') return value > 80 ? 'Healthy Intake' : value > 50 ? 'Degraded Intake' : 'High Threat';
  if (name === 'Synthesis') return value > 80 ? 'ATP Peak' : value > 50 ? 'Nominal Synthesis' : 'Low Energy';
  if (name === 'Deployment') return value > 80 ? 'All Circuits Closed' : value > 50 ? 'Partial Healing' : 'Circuits Open';
  return 'Unknown';
}

export const QEPEngine: React.FC = () => {
  const [metrics, setMetrics] = useState<OrganismMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [triggerMsg, setTriggerMsg] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await axios.get('/api/v1/organism/status');
      setMetrics(res.data);
    } catch { /* keep previous */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, [load]);

  const triggerSynthesis = async () => {
    setTriggering(true); setTriggerMsg(null);
    try {
      const res = await axios.post('/api/v1/organism/homeostasis');
      setTriggerMsg(res.data.summary ?? 'Homeostasis cycle triggered.');
      await load();
    } catch (e: any) {
      setTriggerMsg(e?.response?.data?.detail ?? 'Trigger failed.');
    } finally { setTriggering(false); }
  };

  const engines = metrics ? [
    {
      name: 'Discovery',
      icon: Search,
      color: 'text-aura',
      progress: Math.min(Math.round((metrics.systems.nervous.signals_last_60s / 60) * 100), 100),
      status: engineStatus('Discovery', Math.min((metrics.systems.nervous.signals_last_60s / 60) * 100, 100)),
    },
    {
      name: 'Ingestion',
      icon: Database,
      color: 'text-highlight',
      progress: Math.round(metrics.systems.immune.health * 100),
      status: engineStatus('Ingestion', metrics.systems.immune.health * 100),
    },
    {
      name: 'Synthesis',
      icon: Cpu,
      color: 'text-vital',
      progress: Math.round(metrics.systems.metabolic.atp_ratio * 100),
      status: engineStatus('Synthesis', metrics.systems.metabolic.atp_ratio * 100),
    },
    {
      name: 'Deployment',
      icon: Send,
      color: 'text-aura',
      progress: Math.round(metrics.systems.self_healing.overall_health * 100),
      status: engineStatus('Deployment', metrics.systems.self_healing.overall_health * 100),
    },
  ] : [
    { name: 'Discovery', icon: Search,   color: 'text-aura',      progress: 0, status: 'Loading…' },
    { name: 'Ingestion', icon: Database, color: 'text-highlight',  progress: 0, status: 'Loading…' },
    { name: 'Synthesis', icon: Cpu,      color: 'text-vital',      progress: 0, status: 'Loading…' },
    { name: 'Deployment', icon: Send,    color: 'text-aura',       progress: 0, status: 'Loading…' },
  ];

  const nodes = metrics ? [
    {
      id: '1',
      name: 'Nervous Mesh',
      stage: 'Discovery',
      health: metrics.systems.nervous.arousal_state === 'ALERT' || metrics.systems.nervous.arousal_state === 'HYPERVIGILANT' ? 'Warning' : 'Healthy',
      detail: `${metrics.systems.nervous.signal_rate_per_second.toFixed(2)} sig/s · ${metrics.systems.nervous.arousal_state}`,
    },
    {
      id: '2',
      name: 'Immune Gate',
      stage: 'Ingestion',
      health: metrics.systems.immune.errors_in_window > 5 ? 'Warning' : 'Healthy',
      detail: `${metrics.systems.immune.threat_level} · ${metrics.systems.immune.errors_in_window} errors/window`,
    },
    {
      id: '3',
      name: 'Metabolic Core',
      stage: 'Synthesis',
      health: metrics.systems.metabolic.atp_ratio < 0.3 ? 'Critical' : metrics.systems.metabolic.atp_ratio < 0.5 ? 'Warning' : 'Healthy',
      detail: `ATP ratio: ${(metrics.systems.metabolic.atp_ratio * 100).toFixed(0)}% · RPM ${metrics.systems.reconfiguration.rpm_limit}`,
    },
  ] : [
    { id: '1', name: 'Nervous Mesh',   stage: 'Discovery', health: 'Healthy', detail: 'Initialising…' },
    { id: '2', name: 'Immune Gate',    stage: 'Ingestion',  health: 'Healthy', detail: 'Initialising…' },
    { id: '3', name: 'Metabolic Core', stage: 'Synthesis',  health: 'Healthy', detail: 'Initialising…' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-5xl font-black mb-3 tracking-tight">Quad Engine Reactor</h1>
          <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
            The <span className="text-aura">DISD Pipeline</span>: Live organism intelligence driving the sovereign AI lifecycle.
          </p>
          {metrics && (
            <div className="mt-3 flex items-center gap-3">
              <span className={`text-xs font-black uppercase px-3 py-1 rounded-full border ${
                metrics.mode === 'FULL_POWER' ? 'border-green-500/40 text-green-400 bg-green-500/10' :
                metrics.mode === 'NOMINAL'    ? 'border-aura/40 text-aura bg-aura/10' :
                metrics.mode === 'DEGRADED'   ? 'border-yellow-500/40 text-yellow-400 bg-yellow-500/10' :
                'border-red-500/40 text-red-400 bg-red-500/10'
              }`}>{metrics.mode}</span>
              <span className="text-sm text-slate-500">
                Composite health: <span className="text-white font-bold">{Math.round(metrics.composite_health * 100)}%</span>
              </span>
            </div>
          )}
        </div>
        <button onClick={load} disabled={loading} className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-500 hover:text-white disabled:opacity-50">
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-4 gap-6">
        {engines.map((engine) => (
          <Card key={engine.name} className="flex flex-col group hover:border-aura/50 transition-all">
            <div className="flex justify-between items-start mb-6">
               <div className={`w-14 h-14 rounded-2xl bg-slate-800/50 flex items-center justify-center ${engine.color}`}>
                  <engine.icon size={28} />
               </div>
               <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{engine.progress}%</span>
            </div>
            <h3 className="text-xl font-black mb-1">{engine.name}</h3>
            <p className="text-[10px] text-slate-600 font-bold uppercase tracking-widest mb-6">{engine.status}</p>
            <progress value={engine.progress} max={100} aria-label={`${engine.name} progress ${engine.progress}%`}
               className="w-full h-1 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-900 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
          </Card>
        ))}
      </div>

      <Card className="p-10">
         <div className="flex justify-between items-center mb-10">
            <h3 className="text-2xl font-black tracking-tight flex items-center gap-3">
               <LayoutGrid size={24} className="text-aura" />
               DISD Pipeline Control Panel
            </h3>
            <Button
              onClick={triggerSynthesis}
              disabled={triggering}
              variant="secondary"
              className="flex items-center gap-2"
            >
              {triggering ? <Loader2 size={14} className="animate-spin" /> : <Activity size={14} />}
              {triggering ? 'Synthesising…' : 'Initiate Synthesis'}
            </Button>
         </div>

         {triggerMsg && (
           <div className="mb-6 p-4 rounded-xl bg-aura/5 border border-aura/20 text-sm text-aura/80 font-mono">{triggerMsg}</div>
         )}

         <div className="space-y-4">
            {nodes.map((node) => (
              <div key={node.id} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                 <div className="flex items-center gap-6">
                    <div className="w-10 h-10 rounded-full bg-slate-900 flex items-center justify-center font-bold text-xs text-slate-500">#{node.id}</div>
                    <div>
                       <p className="font-black text-white">{node.name}</p>
                       <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">Stage: {node.stage}</p>
                       <p className="text-[9px] text-slate-700 mt-0.5 font-mono">{node.detail}</p>
                    </div>
                 </div>
                 <div className={`flex items-center gap-2 px-3 py-1 rounded-lg text-[10px] font-black uppercase ${
                   node.health === 'Healthy'  ? 'bg-emerald-500/10 text-emerald-500' :
                   node.health === 'Warning'  ? 'bg-yellow-500/10 text-yellow-500' :
                   'bg-red-500/10 text-red-500'
                 }`}>
                    {node.health === 'Healthy' ? <CheckCircle2 size={12} /> : <AlertCircle size={12} />}
                    {node.health}
                 </div>
              </div>
            ))}
         </div>
      </Card>
    </div>
  );
};
