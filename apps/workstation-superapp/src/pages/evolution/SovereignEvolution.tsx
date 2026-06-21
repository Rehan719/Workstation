import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Dna, Loader2, AlertCircle, Crown, Briefcase, Award, GitBranch,
  Wrench, Sparkles, Rocket, Bug, ShieldCheck, Activity,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Directive {
  id: string; function: string; owner: string; priority: string;
  title: string; rationale: string; verdict?: string; effort?: string; execution_note?: string;
}
interface Roadmap {
  cycle_id: string; created_at: string; duration_ms: number;
  introspection: any; ceo_directives: Directive[]; bto_roadmap: string;
  curated_by: string[]; items_proceeding: number; change_control_submissions: any[];
}

const FN_ICON: Record<string, React.ComponentType<any>> = {
  improvement: Sparkles, maintenance: Wrench, development: Rocket, correction: Bug,
};
const FN_LABEL: Record<string, string> = {
  improvement: 'Self-Improvement', maintenance: 'Self-Maintenance',
  development: 'Self-Development', correction: 'Self-Correction',
};
const ORG_TIERS = [
  { icon: Crown, label: 'AI CEO', desc: 'Triages organism state → directives' },
  { icon: Briefcase, label: 'C-Suite', desc: 'CTO/COO/CFO/CLO evaluate & verdict' },
  { icon: Award, label: 'CoE', desc: 'Quality-gate to standards' },
  { icon: GitBranch, label: 'BTO', desc: 'Sequence into roadmap + governance' },
];

function verdictTone(v?: string) {
  if (v === 'reject') return 'text-vital';
  if (v === 'defer') return 'text-amber-400';
  return 'text-emerald-400';
}

// ── Component ─────────────────────────────────────────────────────────────────

export const SovereignEvolution: React.FC = () => {
  const [focus, setFocus] = useState('');
  const [submitCC, setSubmitCC] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);

  useEffect(() => {
    fetch('/api/v1/sovereign-evolution/roadmap')
      .then(r => r.json())
      .then(d => { if (d && d.ceo_directives) setRoadmap(d); })
      .catch(() => {});
  }, []);

  const runCycle = async () => {
    setRunning(true);
    setError('');
    try {
      const res = await fetch('/api/v1/sovereign-evolution/cycle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ focus, submit_to_change_control: submitCC }),
      });
      if (!res.ok) { setError(`HTTP ${res.status}`); setRunning(false); return; }
      setRoadmap(await res.json());
    } catch (e: any) {
      setError(e?.message ?? String(e));
    }
    setRunning(false);
  };

  const imm = roadmap?.introspection?.immune;
  const res = roadmap?.introspection?.resources;

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Self-Evolution</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Sovereign Evolution Office</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The organism evolves itself — autonomously, and curated by its own Virtual Sovereign Business.
          It observes its state, then the <span className="text-highlight">AI CEO → C-Suite → CoE → BTO</span> curate
          self-improvement, maintenance, development and correction into a governed transformation roadmap.
        </p>
      </header>

      {/* Org curation pipeline */}
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-5">VSB Curation Pipeline</h3>
        <div className="grid grid-cols-2 @[640px]:grid-cols-4 gap-3">
          {ORG_TIERS.map(({ icon: Icon, label, desc }, i) => (
            <div key={label} className="p-4 rounded-2xl border bg-slate-900 border-slate-800">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-7 h-7 rounded-lg bg-highlight/10 flex items-center justify-center"><Icon size={12} className="text-highlight" /></div>
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Tier {i + 1}</span>
              </div>
              <p className="text-[11px] font-black text-white mb-1">{label}</p>
              <p className="text-[9px] text-slate-600 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
        <div className="flex flex-wrap gap-2 mt-4">
          {Object.entries(FN_LABEL).map(([k, label]) => {
            const Icon = FN_ICON[k];
            return (
              <span key={k} className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-[9px] font-black uppercase tracking-wider text-slate-400">
                <Icon size={11} className="text-highlight" /> {label}
              </span>
            );
          })}
        </div>
      </Card>

      {/* Controls */}
      <Card className="p-8 space-y-6">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">CEO Focus (optional)</label>
          <input
            value={focus}
            onChange={e => setFocus(e.target.value)}
            placeholder="Steer this cycle, e.g. 'frontend latency' or 'test coverage' — or leave blank for full autonomy"
            className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50"
          />
        </div>
        <label className="flex items-center gap-3 cursor-pointer">
          <input type="checkbox" checked={submitCC} onChange={e => setSubmitCC(e.target.checked)} className="accent-highlight w-4 h-4" />
          <span className="text-[11px] font-bold text-slate-400">Submit P1 &amp; correction items to the Change Control Agency for governance</span>
        </label>
        <div className="flex items-center gap-4 pt-1">
          <Button onClick={runCycle} disabled={running} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <Dna size={16} />}
            {running ? 'Curating Evolution Cycle…' : 'Run Autonomous Cycle'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {roadmap && (
        <div className="space-y-6">
          {/* Introspection snapshot */}
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Activity size={16} className="text-highlight" />
              <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Organism Introspection</h3>
              <span className="text-[9px] font-mono text-slate-600 ml-auto">cycle {roadmap.cycle_id} · {roadmap.duration_ms}ms</span>
            </div>
            <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3 text-center">
              <Metric label="Projects" value={roadmap.introspection?.projects?.total ?? 0} />
              <Metric label="Immune Health" value={imm?.health ?? '—'} tone={imm?.threat_level === 'NONE' || imm?.threat_level === 'LOW' ? 'good' : 'warn'} />
              <Metric label="CPU" value={res ? `${res.cpu_percent}%` : '—'} />
              <Metric label="Items Proceeding" value={roadmap.items_proceeding} tone="good" />
            </div>
          </Card>

          {/* CEO directives curated by C-Suite */}
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-5">
              <Crown size={16} className="text-highlight" />
              <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">CEO Directives · Curated by C-Suite</h3>
              <span className="text-[9px] font-mono text-slate-600 ml-auto">{roadmap.curated_by?.join(' → ')}</span>
            </div>
            <div className="space-y-3">
              {roadmap.ceo_directives.map(d => {
                const Icon = FN_ICON[d.function] ?? Sparkles;
                return (
                  <div key={d.id} className="p-4 rounded-2xl bg-slate-950 border border-slate-900">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3 min-w-0">
                        <div className="w-8 h-8 rounded-xl bg-highlight/10 flex items-center justify-center shrink-0"><Icon size={14} className="text-highlight" /></div>
                        <div className="min-w-0">
                          <p className="font-black text-white text-sm">{d.title}</p>
                          <p className="text-[10px] text-slate-500 font-bold mt-0.5">{d.rationale}</p>
                          {d.execution_note && <p className="text-[10px] text-slate-400 italic mt-1">↳ {d.execution_note}</p>}
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-1 shrink-0">
                        <span className="text-[9px] font-black uppercase tracking-wider text-highlight">{d.owner}</span>
                        <span className="text-[8px] font-black uppercase text-slate-600">{FN_LABEL[d.function] ?? d.function} · {d.priority}</span>
                        <span className={`text-[9px] font-black uppercase ${verdictTone(d.verdict)}`}>{d.verdict ?? 'proceed'} · {d.effort ?? 'M'}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>

          {/* BTO transformation roadmap */}
          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <div className="flex items-center gap-3 mb-3">
              <GitBranch size={16} className="text-highlight" />
              <h3 className="font-black text-highlight uppercase tracking-widest text-sm">BTO Transformation Roadmap</h3>
            </div>
            <p className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">{roadmap.bto_roadmap}</p>
          </Card>

          {/* Change Control submissions */}
          {roadmap.change_control_submissions?.length > 0 && (
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <ShieldCheck size={16} className="text-emerald-400" />
                <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Submitted to Change Control Agency</h3>
              </div>
              <div className="space-y-2">
                {roadmap.change_control_submissions.map((s: any, i: number) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-900 text-xs">
                    <span className="text-slate-300 font-bold truncate">{s.title ?? s.error ?? 'submission'}</span>
                    {s.cca_id && <span className="font-mono text-[10px] text-slate-500 shrink-0">{s.impact_tier} · {s.cca_id}</span>}
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

const Metric: React.FC<{ label: string; value: any; tone?: 'good' | 'warn' }> = ({ label, value, tone }) => (
  <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
    <p className={`text-xl font-black ${tone === 'good' ? 'text-emerald-400' : tone === 'warn' ? 'text-amber-400' : 'text-white'}`}>{value}</p>
    <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mt-1">{label}</p>
  </div>
);
