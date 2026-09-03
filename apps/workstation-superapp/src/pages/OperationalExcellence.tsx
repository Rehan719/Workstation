import React, { useEffect, useState } from 'react';
import { provenanceBadge } from '../lib/api';
import { Card } from '@workstation/ui';
import { Gauge, TrendingUp, Cpu, CheckCircle2, Loader2 } from 'lucide-react';

interface Summary {
  total_runs: number; success_rate: number; in_house_rate: number;
  distinct_resources: number; top_resource: string | null; kinds: string[];
}
interface Ranking {
  resource: string; kind: string; runs: number; success_rate: number;
  avg_duration_ms: number; in_house_rate: number; last_seen: string;
}
interface Outcome {
  id: string; kind: string; resource: string; served_by: string;
  is_external: boolean; duration_ms: number; success: boolean; created_at: string;
}
interface ModelHealth { name: string; runs: number; success_rate: number; avg_ms: number; deprioritised: boolean }

const pct = (n: number) => `${Math.round((n ?? 0) * 100)}%`;

export const OperationalExcellence: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [rankings, setRankings] = useState<Ranking[]>([]);
  const [outcomes, setOutcomes] = useState<Outcome[]>([]);
  const [models, setModels] = useState<ModelHealth[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/api/v1/operations/summary').then(r => r.json()),
      fetch('/api/v1/operations/rankings').then(r => r.json()),
      fetch('/api/v1/operations/outcomes?limit=40').then(r => r.json()),
      fetch('/api/v1/operations/model-health').then(r => r.json()),
    ]).then(([s, r, o, m]) => {
      setSummary(s); setRankings(r.rankings || []); setOutcomes(o.outcomes || []); setModels(m.models || []);
    })
      .catch(() => setError('Failed to load operational metrics'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Operational Excellence</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Learning Loop</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The real, recorded outcomes of every run on Workstation's <span className="text-highlight">own</span> resources —
          swarm cascades, deliverables, transformations — aggregated into honest per-resource rankings the platform learns from.
          Empty until runs happen; never fabricated.
        </p>
      </header>

      {error && <p className="text-vital text-xs font-bold">{error}</p>}

      {loading && !error && (
        <div className="flex items-center gap-2 text-[11px] font-bold text-slate-500"><Loader2 size={14} className="animate-spin" /> Loading operational metrics…</div>
      )}

      {summary && (
        <div className="grid grid-cols-2 @[640px]:grid-cols-4 gap-3">
          <Stat icon={Gauge} label="Total runs" value={String(summary.total_runs)} />
          <Stat icon={CheckCircle2} label="Success rate" value={pct(summary.success_rate)} />
          <Stat icon={Cpu} label="In-house rate" value={pct(summary.in_house_rate)} />
          <Stat icon={TrendingUp} label="Resources" value={String(summary.distinct_resources)} />
        </div>
      )}

      {/* Rankings */}
      <div>
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><TrendingUp size={14} /> Resource rankings</h3>
        {!loading && rankings.length === 0 && <p className="text-[11px] text-slate-600">No runs recorded yet — run a swarm, produce a deliverable, or orchestrate a transformation, and outcomes will appear here.</p>}
        {rankings.length > 0 && (
          <Card className="p-0 overflow-hidden">
            <table className="w-full text-left">
              <thead>
                <tr className="text-[8px] font-black uppercase tracking-widest text-slate-600 border-b border-slate-900">
                  <th className="p-3">Resource</th><th className="p-3">Runs</th><th className="p-3">Success</th>
                  <th className="p-3">In-house</th><th className="p-3">Avg ms</th>
                </tr>
              </thead>
              <tbody>
                {rankings.map((r, i) => (
                  <tr key={r.resource} className={`text-[11px] ${i % 2 ? 'bg-slate-950/40' : ''}`}>
                    <td className="p-3 font-bold text-white">{r.resource} <span className="text-[8px] text-slate-600 uppercase">{r.kind}</span></td>
                    <td className="p-3 text-slate-400">{r.runs}</td>
                    <td className="p-3"><span className="text-emerald-400 font-bold">{pct(r.success_rate)}</span></td>
                    <td className="p-3"><span className={r.in_house_rate >= 1 ? 'text-aura font-bold' : 'text-amber-400'}>{pct(r.in_house_rate)}</span></td>
                    <td className="p-3 text-slate-500">{r.avg_duration_ms}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        )}
      </div>

      {/* Model performance — the fabric's learning (W7) */}
      {models.length > 0 && (
        <div>
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Cpu size={14} /> Model performance — the fabric's learning</h3>
          {/* §6 (W426) — this described the pre-W380 rule. The threshold moved 0.6 -> 0.25 and
              probation was added; the old copy quoted the 0.6 figure as a percentage and never
              mentioned probation, so the page explained a policy the fabric had stopped using.
              The guard forbids that figure appearing anywhere in this file, comments included —
              which is why it is referred to and not reproduced here. */}
          <p className="text-[9px] text-slate-600 mb-3">
            A non-native model ranks <em>below</em> the always-available native floor only when it is
            effectively dead — at least 5 attempts in the window <em>and</em> under 25% success.
            Ordering a model after the floor means it is never tried at all (the floor always
            answers), so demotion is reserved for that, not for merely imperfect: every failure is
            caught by the floor anyway, and the real cost of trying is latency, not a broken
            response. A demoted model is not exiled — after 10 minutes untried it earns one fresh
            attempt (probation) and returns to the preferred set if it succeeds.
          </p>
          <Card className="p-0 overflow-hidden">
            <table className="w-full text-left">
              <thead>
                <tr className="text-[8px] font-black uppercase tracking-widest text-slate-600 border-b border-slate-900">
                  <th scope="col" className="p-3">Model</th><th scope="col" className="p-3">Attempts</th>
                  <th scope="col" className="p-3">Success</th><th scope="col" className="p-3">Avg ms</th><th scope="col" className="p-3">Status</th>
                </tr>
              </thead>
              <tbody>
                {models.map((m, i) => (
                  <tr key={m.name} className={`text-[11px] ${i % 2 ? 'bg-slate-950/40' : ''}`}>
                    <td className="p-3 font-bold text-white">{m.name}</td>
                    <td className="p-3 text-slate-400">{m.runs}</td>
                    {/* §6 (W426) — coloured against the threshold that ACTUALLY governs demotion.
                        W380 moved the floor from 0.6 to 0.25 ("only an effectively-dead model goes
                        behind the floor", orchestrator.py:69) and this cell was never updated, so a
                        model at 0.4 rendered amber — reading as failing — while the orchestrator
                        still preferred it. The colour now means what the system does. */}
                    <td className="p-3"><span className={m.success_rate >= 0.25 ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}
                      title={m.success_rate >= 0.25
                        ? 'Above the 0.25 demotion floor — this model is still preferred by the orchestrator.'
                        : 'Below the 0.25 demotion floor — effectively dead, so it ranks behind the deterministic native floor. It earns one fresh attempt after 10 minutes untried (probation).'}>{pct(m.success_rate)}</span></td>
                    <td className="p-3 text-slate-500">{m.avg_ms}</td>
                    <td className="p-3">{m.deprioritised
                      ? <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400">deprioritised</span>
                      : <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400">preferred</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>
      )}

      {/* Recent outcomes */}
      <div>
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Recent outcomes ({outcomes.length})</h3>
        <div className="space-y-1.5">
          {outcomes.map(o => (
            <div key={o.id} className="flex items-center gap-2 text-[10px] p-2 rounded-lg bg-slate-950 border border-slate-900">
              {o.success ? <CheckCircle2 size={11} className="text-emerald-400" /> : <span className="text-vital">✕</span>}
              <span className="font-bold text-white">{o.resource}</span>
              <span className="text-slate-600 uppercase">{o.kind}</span>
              <span className={`ml-auto text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${o.is_external ? 'bg-amber-500/10 text-amber-400' : 'bg-aura/10 text-aura'}`}>
                {provenanceBadge(o.served_by, o.is_external).label}
              </span>
              <span className="text-slate-600">{o.duration_ms}ms</span>
            </div>
          ))}
          {!loading && outcomes.length === 0 && <p className="text-[11px] text-slate-600">No outcomes recorded yet.</p>}
        </div>
      </div>
    </div>
  );
};

const Stat: React.FC<{ icon: React.ElementType; label: string; value: string }> = ({ icon: Icon, label, value }) => (
  <Card className="p-4">
    <div className="flex items-center gap-2 mb-1"><Icon size={14} className="text-aura" /><p className="text-[9px] font-black uppercase tracking-widest text-slate-500">{label}</p></div>
    <p className="text-2xl font-black text-white">{value}</p>
  </Card>
);
