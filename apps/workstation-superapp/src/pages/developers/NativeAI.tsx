import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Cpu, Network, Loader2, CheckCircle2, Circle, ShieldCheck, Server, Globe } from 'lucide-react';

interface ModelResource {
  name: string; kind: string; available: boolean; is_external: boolean; model?: string; note?: string;
}
interface Status {
  posture: string; external_allowed: boolean; owned_resources_available: string[];
  selection_order: string[]; guarantee: string; resources: ModelResource[];
}
interface SwarmStep { step: number; role: string; served_by: string; output: string }
interface SwarmRun { agent: string; stages: number; trace: SwarmStep[]; final: string; any_external: boolean }

function kindIcon(kind: string) {
  if (kind === 'native') return Cpu;
  if (kind === 'local') return Server;
  return Globe;
}

export const NativeAI: React.FC = () => {
  const [status, setStatus] = useState<Status | null>(null);
  const [context, setContext] = useState('a halal, zero-waste community meal service for elderly Londoners');
  const [run, setRun] = useState<SwarmRun | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/v1/native-ai/status').then(r => r.json()).then(setStatus).catch(() => setError('Failed to load fabric status'));
  }, []);

  const runSwarm = async () => {
    setRunning(true); setRun(null);
    try {
      const r = await fetch('/api/v1/native-ai/swarm', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: 'demo', context }),
      });
      setRun(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Native AI Fabric</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">In-House AI Resources</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Workstation's <span className="text-highlight">own</span> AI Swarm · Models · Orchestration — not a façade over external
          API calls. The platform produces a real result from its <span className="text-highlight">owned</span> resources with no
          external dependency; external providers are optional accelerants only.
        </p>
      </header>

      {error && <p className="text-vital text-xs font-bold">{error}</p>}

      {status && (
        <>
          {/* Posture */}
          <Card className="p-6 border-emerald-500/30 bg-emerald-500/5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-black text-white uppercase tracking-wide flex items-center gap-2"><ShieldCheck size={16} className="text-emerald-400" /> Posture</h3>
              <span className="text-[10px] font-black uppercase px-2 py-1 rounded bg-emerald-500/20 text-emerald-400">{status.posture}</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">{status.guarantee}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">external allowed: {String(status.external_allowed)}</span>
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-slate-900 text-slate-400">selection: {status.selection_order.join(' → ')}</span>
              <span className="text-[9px] font-bold uppercase px-2 py-1 rounded bg-aura/10 text-aura">owned available: {status.owned_resources_available.join(', ')}</span>
            </div>
          </Card>

          {/* Resources */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Cpu size={14} /> Model Resources</h3>
            <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-3">
              {status.resources.map(r => {
                const Icon = kindIcon(r.kind);
                return (
                  <Card key={r.name} className="p-4">
                    <div className="flex items-center justify-between mb-1">
                      <p className="font-black text-white text-sm flex items-center gap-2"><Icon size={14} className={r.is_external ? 'text-slate-500' : 'text-aura'} /> {r.name} {r.model && <span className="text-[9px] text-slate-600 font-bold">({r.model})</span>}</p>
                      <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${r.available ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-600'}`}>{r.available ? 'available' : 'off'}</span>
                    </div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${r.is_external ? 'bg-amber-500/10 text-amber-400' : 'bg-aura/10 text-aura'}`}>{r.is_external ? 'external (opt-in)' : 'owned'}</span>
                      <span className="text-[8px] font-bold uppercase text-slate-600">{r.kind}</span>
                    </div>
                    <p className="text-[10px] text-slate-600 leading-relaxed">{r.note}</p>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Swarm runner */}
          <Card className="p-6">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Network size={14} /> Native Swarm (bespoke agent cascade, owned resources)</h3>
            <textarea value={context} onChange={e => setContext(e.target.value)} rows={2}
              className="w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300 mb-3"
              placeholder="Context / objective for the swarm…" />
            <Button onClick={runSwarm} disabled={running} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
              {running ? <Loader2 size={13} className="animate-spin" /> : <Network size={13} />} Run native swarm
            </Button>
            {run && (
              <div className="mt-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-[9px] font-black uppercase text-slate-400">{run.stages} stages</span>
                  <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${run.any_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                    {run.any_external ? 'used external accelerant' : 'fully in-house'}
                  </span>
                </div>
                <div className="space-y-2">
                  {run.trace.map(s => (
                    <div key={s.step} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <div className="flex items-center justify-between mb-1">
                        <p className="text-xs font-black text-white flex items-center gap-1.5">
                          {s.served_by === 'native' ? <CheckCircle2 size={11} className="text-aura" /> : <Circle size={11} className="text-emerald-400" />}
                          {s.step}. {s.role}
                        </p>
                        <span className="text-[8px] font-bold uppercase text-slate-600">served by {s.served_by}</span>
                      </div>
                      <p className="text-[10px] text-slate-500 whitespace-pre-wrap line-clamp-4">{s.output}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  );
};
