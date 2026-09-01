import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { HeartPulse, Loader2, Play, Square, Activity, Sun, Moon, ShieldCheck, Zap } from 'lucide-react';

interface Beat { beat: number; phase: string; intensity: number; realisation: number | null; health: number | null; actions: string[]; at: string; self_recovery?: string | null }
interface Status {
  running: boolean; beats: number; circadian_phase: string; phase_intensity: number;
  last_beat: string | null; last_realisation: number | null; interval_seconds: number;
  auto_evolve: boolean; auto_economy: boolean; auto_align: boolean; auto_compliance: boolean;
  auto_ship: boolean; autonomy_persisted?: boolean; autonomy_restored_at?: string | null;
  evolution_auto_apply?: { enabled: boolean | null; readable: boolean; governed_by: string;
    consumer?: string; how_to_change?: string; why_not_a_toggle?: string; effect_when_off?: string };
  recent: Beat[]; integrations: string[];
}

/**
 * §3 · §4.10 · §12 (W420) — the five autonomy flags, with plain copy for what each DOES on the next
 * beat. Four of these had no control anywhere: auto_economy was declared in this file's interface
 * but never rendered, and auto_align / auto_compliance / auto_ship appeared nowhere in the frontend
 * at all. "Once established it runs, maintains, defends, improves and grows itself" is the product's
 * headline promise, and until now a user could switch on exactly one fifth of it.
 */
const AUTONOMY: { key: keyof Status; label: string; does: string }[] = [
  { key: 'auto_evolve', label: 'Self-improve',
    does: 'Runs an AI evolution cycle on maintenance-phase beats, paced — proposals go to governance, never straight to production.' },
  { key: 'auto_economy', label: 'Self-run',
    does: 'Operates each living VSB on the beat: metabolic cycle, profit waterfall, virtual WST only.' },
  { key: 'auto_compliance', label: 'Self-defend',
    does: 'Re-screens every living VSB against §11 compliance each beat, so a verdict is not frozen at establishment.' },
  { key: 'auto_align', label: 'Self-align',
    does: 'Routes vision gaps to delivery tiers each beat. Plan-only and cheap — it writes no code.' },
  { key: 'auto_ship', label: 'Self-ship',
    does: 'Re-ships ONE stale repo per beat, oldest first.' },
];

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
            <div className="mt-5 pt-4 border-t border-slate-800">
              <div className="flex items-baseline justify-between gap-3 mb-1">
                <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest">Autonomy — what the organism does on its own</p>
                <span className="text-[9px] font-bold text-slate-500">
                  {[...AUTONOMY].filter(a => s[a.key]).length} of {AUTONOMY.length} on
                </span>
              </div>
              <p className="text-[10px] text-slate-500 font-semibold mb-3 leading-relaxed">
                All five are OFF by default and take effect on the NEXT beat. Money moved by
                self-run is virtual WST.
                {s.autonomy_persisted === false
                  ? ' ⚠ These settings could NOT be saved — they will revert when the backend restarts.'
                  : ' Your choices are saved and survive a restart.'}
                {s.autonomy_restored_at ? ` Restored from ${s.autonomy_restored_at}.` : ''}
              </p>
              <div className="space-y-2">
                {AUTONOMY.map(a => (
                  <label key={a.key} className="flex items-start gap-3 cursor-pointer p-2.5 rounded-xl bg-slate-950 border border-slate-900 hover:border-slate-800">
                    <input type="checkbox" checked={!!s[a.key]}
                      aria-label={`${a.label} — ${a.does}`}
                      onChange={e => act('configure', { [a.key]: e.target.checked })}
                      className="accent-highlight w-4 h-4 mt-0.5 shrink-0" />
                    <span className="min-w-0">
                      <span className="block text-[11px] font-black text-slate-200">
                        {a.label} <span className="text-slate-600 font-bold">· {a.key}</span>
                        <span className={`ml-2 text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${s[a.key] ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500'}`}>{s[a.key] ? 'on' : 'off'}</span>
                      </span>
                      <span className="block text-[10px] text-slate-500 font-semibold leading-relaxed mt-0.5">{a.does}</span>
                    </span>
                  </label>
                ))}
              </div>
              {/* §8 (W424) — the CCA-governed post-approval APPLY lever. It has a real consumer
                  on this beat and had no UI anywhere, so a user could not tell whether approved
                  evolution work would ever land. Shown READ-ONLY: routing a switch here would
                  bypass the arms-length approval it exists behind. */}
              {s.evolution_auto_apply && (
                <div className="mt-3 p-2.5 rounded-xl bg-slate-950 border border-slate-900">
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-[11px] font-black text-slate-200">
                      Apply approved evolution <span className="text-slate-600 font-bold">· evolution_auto_apply</span>
                    </span>
                    <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${s.evolution_auto_apply.enabled ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500'}`}>
                      {s.evolution_auto_apply.readable ? (s.evolution_auto_apply.enabled ? 'on' : 'off') : 'unreadable'}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-500 font-semibold leading-relaxed mt-1">
                    {s.evolution_auto_apply.enabled
                      ? s.evolution_auto_apply.consumer
                      : s.evolution_auto_apply.effect_when_off}{' '}
                    Governed by the {s.evolution_auto_apply.governed_by} — {s.evolution_auto_apply.how_to_change}.
                  </p>
                </div>
              )}
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
