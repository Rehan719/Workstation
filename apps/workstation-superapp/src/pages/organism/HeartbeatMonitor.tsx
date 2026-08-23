import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { HeartPulse, Loader2, Play, Square, Activity, Sun, Moon, ShieldCheck, Zap } from 'lucide-react';

interface Beat { beat: number; phase: string; intensity: number; realisation: number | null; health: number | null; actions: string[]; at: string; self_recovery?: string | null }
interface Status {
  running: boolean; beats: number; circadian_phase: string; phase_intensity: number;
  last_beat: string | null; last_realisation: number | null; interval_seconds: number;
  auto_evolve: boolean; auto_economy: boolean; recent: Beat[]; integrations: string[];
}

const PHASE_ICON: Record<string, React.ComponentType<any>> = {
  ACTIVE_FOCUS: Sun, ACTIVE_REST: Sun, MAINTENANCE_FOCUS: Moon, MAINTENANCE_REST: Moon,
};

export const HeartbeatMonitor: React.FC = () => {
  const [s, setS] = useState<Status | null>(null);
  const [busy, setBusy] = useState(false);
  const [actErr, setActErr] = useState('');   // W329 — actions never fail silently

  const load = () => fetch('/api/v1/heartbeat/status').then(r => r.json()).then(setS).catch(() => {});
  useEffect(() => { load(); const t = setInterval(load, 8000); return () => clearInterval(t); }, []);

  const act = async (path: string, body?: object) => {
    setBusy(true);
    setActErr('');
    try {
      const r = await fetch(`/api/v1/heartbeat/${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
      if (!r.ok) setActErr(`Action failed (HTTP ${r.status}) — nothing changed`);
      await load();
    } catch {
      setActErr('Backend unreachable — nothing changed');
    }
    setBusy(false);
  };

  const Phase = s ? (PHASE_ICON[s.circadian_phase] ?? Activity) : Activity;

  return (
    <div className="space-y-10 pb-24">
      {actErr && <p className="text-vital text-xs font-bold">{actErr}</p>}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Continuous Autonomy</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Organism Heartbeat</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The circadian rhythm that makes Workstation <span className="text-highlight">run itself continuously</span> — pulsing the
          nervous system, checking homeostasis, ticking vision-realisation, and logging every beat to the constitutional UEG.
          Cheap by default; expensive AI cognition is opt-in and paced.
        </p>
      </header>

      {s && (
        <>
          <Card className="p-8">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${s.running ? 'bg-vital/20' : 'bg-slate-800'}`}>
                  <HeartPulse size={22} className={s.running ? 'text-vital animate-pulse' : 'text-slate-500'} />
                </div>
                <div>
                  <p className="font-black text-white text-lg">{s.running ? 'Beating' : 'Stopped'}</p>
                  <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">{s.beats} beats · every ~{s.interval_seconds}s</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button onClick={() => act('beat')} disabled={busy} className="flex items-center gap-1.5 bg-highlight text-sovereign text-xs"><Zap size={13} /> Beat</Button>
                {s.running
                  ? <Button onClick={() => act('stop')} disabled={busy} className="flex items-center gap-1.5 bg-slate-800 text-white text-xs"><Square size={13} /> Stop</Button>
                  : <Button onClick={() => act('start')} disabled={busy} className="flex items-center gap-1.5 bg-emerald-600 text-white text-xs"><Play size={13} /> Start</Button>}
              </div>
            </div>
            <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3 text-center">
              <Metric icon={Phase} label="Circadian Phase" value={s.circadian_phase.replace('_', ' ')} />
              <Metric icon={Activity} label="Intensity" value={`${Math.round(s.phase_intensity * 100)}%`} />
              <Metric icon={Activity} label="Realisation" value={s.last_realisation != null ? `${Math.round(s.last_realisation * 100)}%` : '—'} tone="good" />
              <Metric icon={ShieldCheck} label="Auto-evolve" value={s.auto_evolve ? 'ON' : 'OFF'} tone={s.auto_evolve ? 'good' : undefined} />
            </div>
            <div className="flex items-center justify-between mt-5 pt-4 border-t border-slate-800">
              <p className="text-[10px] text-slate-500 font-bold">Autonomous AI evolution cycles (opt-in, paced):</p>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={s.auto_evolve} onChange={e => act('configure', { auto_evolve: e.target.checked })} className="accent-highlight w-4 h-4" />
                <span className="text-[11px] font-black text-slate-300">{s.auto_evolve ? 'Enabled' : 'Disabled'}</span>
              </label>
            </div>
            <div className="flex flex-wrap gap-1.5 mt-3">
              {s.integrations.map(i => <span key={i} className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-400 text-[8px] font-black uppercase tracking-wider">{i.replace(/_/g, ' ')}</span>)}
            </div>
          </Card>

          {s.recent.length > 0 && (
            <Card className="p-6">
              <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4">Recent Beats</h3>
              <div className="space-y-2">
                {s.recent.slice().reverse().map(b => (
                  <div key={b.beat} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-900 text-xs">
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-slate-600">#{b.beat}</span>
                      <span className="text-highlight font-black uppercase text-[9px]">{b.phase.replace('_', ' ')}</span>
                    </div>
                    <div className="flex items-center gap-3 text-[9px] font-mono">
                      <span className="text-slate-500">{b.actions.join(' · ')}</span>
                      {b.self_recovery && (
                        <span className="text-amber-400 font-black uppercase" title="§8 survival instinct — the organism autonomously rested and restored its own energy on this beat">
                          self-healed ATP {b.self_recovery}
                        </span>
                      )}
                      {b.realisation != null && <span className="text-emerald-400">{Math.round(b.realisation * 100)}%</span>}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  );
};

const Metric: React.FC<{ icon: React.ComponentType<any>; label: string; value: any; tone?: 'good' }> = ({ icon: Icon, label, value, tone }) => (
  <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
    <Icon size={13} className="text-slate-500 mx-auto mb-1" />
    <p className={`text-sm font-black ${tone === 'good' ? 'text-emerald-400' : 'text-white'}`}>{value}</p>
    <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mt-1">{label}</p>
  </div>
);
