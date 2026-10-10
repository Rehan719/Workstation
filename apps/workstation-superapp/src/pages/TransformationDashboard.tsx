import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Target, Activity, GitBranch, CheckCircle2, Circle, Loader2,
  Sparkles, HeartPulse, AlertCircle, Eye, Map, Workflow, ShieldCheck, ListChecks,
} from 'lucide-react';
import { apiJson, errorMessage, provenanceBadge } from '../lib/api';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Evidence { label: string; met: boolean | null; basis?: string }
interface Pillar { id: string; pillar: string; realisation: number; status: string; evidence: Evidence[];
  checks_met?: number; checks_assessed?: number; checks_status?: string; coverage_basis?: string }   // W655
interface Picture {
  vision_summary: string;
  realisation: { overall_realisation: number; pillars: Pillar[]; evidence_counts: Record<string, any>; route_census?: { basis?: string; paths?: number } };
  transformation_plan: { immediate_gaps: { pillar: string; realisation: number; missing: string[] }[]; short_term: string[]; long_term: string[] };
}

// W461 — verified is three-state: true (checked, passed) · false (checked, failed) · null (not assessable)
interface CascadeStage { step: number; tier: string; delegates_to: string; action: string; verified: boolean | null; basis?: string | null; signal: string;
  checks?: 'presence' | 'decision' | 'artifact' | 'delivery' | 'none' }   // W481 — what KIND of check ran
interface OrchRunSummary { transformation_id: string; scope: string; objective: string; validated: boolean | null; created_at: string }
interface OrchestrationRun {
  transformation_id: string;
  objective: string;
  cascade: CascadeStage[];
  digital_twin: { model_id: string; projection?: { projected?: number; current?: number; formula?: string; note?: string; of?: string;
    compared_with_current?: string } };
  // W494 (FU-130) - the shared intent-gate result carries what it screened
  governance: { status: string; checkpoint?: string;
                scope?: string; screened?: string; content_screened?: boolean };
  validation: { stages: number; assessable_stages?: number; not_assessable_stages?: number; presence_stages?: number;
    delivery_verified_stages?: number[]; verified_stages: number; end_to_end_chief_to_bto: boolean;
    biomimetic_signals_fired: number; validated: boolean | null; validated_basis?: string; report: string };
}

// W462 — the follow-up register (GET /api/v1/plan/followups): found-but-not-done work, scheduled in plan order
interface FollowupPriority { score: number; area: string | null; tier: number | null; parts: Record<string, number>; basis: Record<string, string> }
// W499 — `slot_source` is why a row sits on THIS item when the routing heuristic would have sent
// it elsewhere. It was written into the register and shown nowhere, so a reader saw the placement
// and not the reason for it.
interface FollowupRow { id: string; title: string; why: string; severity: string; slot: string; source: string; slot_source?: string | null; priority?: FollowupPriority }
// W469 — the delivery plan's live state (PLAN NOW), derived on every call from the plan's items and the register
interface PlanItemNow { slot: string; title: string; followups: number; by_severity: Record<string, number> }
interface PlanNow {
  next: PlanItemNow | null; open_items: PlanItemNow[]; phases: { phase: string; done: number; total: number }[];
  done: number; total: number; unscheduled: string[]; readable?: boolean;
}
// W486 — the PACE the plan is moving at, derived on every call from the register's own record of
// which round closed each row and which round found it. `assessable` false means no projection can
// be justified, and `not_assessable_because` says why — it is never replaced by a guess.
interface Forecast {
  assessable: boolean; not_assessable_because?: string | null;
  window: { rounds: string[]; count: number; closed_per_round: number; found_per_round: number; net_per_round: number };
  steady?: { rounds: string[]; count: number; excluded: string[]; closed_per_round: number; found_per_round: number; net_per_round: number };
  rate_used?: { closed_per_round: number; net_per_round: number; rounds: number; source: string };
  open_rows: number;
  next_item: { slot: string; title: string; open_rows: number; rounds_projected: number | null } | null;
  all_rows_rounds_projected: number | null;
  // W499 — PLAN COMPLETION is a different population from the rows, and this page showed only the
  // rows: a reader saw "~12 rounds for all open rows" and had no way to know the PLAN is 110 build
  // rounds from done. The partition travels with the figure: switches the Owner flips are not
  // projected, and the coverage says how much of the population was ever sized.
  items_open: number;
  items_open_build: number;
  items_open_owner_switch: number;
  items_owner_switch_slots: string[];
  items_open_unmarked: string[];
  items_rounds_projected: number | null;
  item_build_rate_per_round: number;
  item_rate_phases: string[];
  items_sized_build: number;
  items_with_no_row: string[];
}
// W501 (P2.17a) — the round a generator proposes: one FILE-CONNECTED subsystem cut by item. A batch is
// one mechanism across its consumers; a bundle is one subsystem's worth of reading, which is what a
// round costs. `above_measured_ceiling` means larger than any round has yet closed — a flag, not a bar.
interface Bundle {
  slot: string; size: number; files_count: number; component_size: number;
  also_touching: string[]; priority: number; above_measured_ceiling: boolean;
  possibly_under_connected: boolean;
}
interface Bundles {
  bundles: Bundle[]; components?: number; basis?: string;
  ceiling?: { rows: number | null; rounds: string[]; median?: number | null; basis?: string };
}
interface Followups {
  available: boolean; reason?: string;
  forecast?: Forecast;
  bundles?: Bundles;
  counts: { open: number; scheduled: number; high: number; awaiting_owner: number; done: number; dropped: number; unscheduled?: number };
  next_plan_item: string | null;
  schedule: { slot: string; title: string; items: FollowupRow[]; delivered_by?: string | null }[];
  unscheduled?: FollowupRow[];
  awaiting_owner: FollowupRow[];
  plan?: PlanNow;
  integrity: { ok: boolean; problems: string[] };
  // W478 — the priority in force: completion weighted by what the rows are worth (follow-up rows, not plan items)
  priority?: { gate_phase: string | null; config: string; config_problems: string[]; suggested_order: string[];
    completion: { overall_weighted_pct: number | null; by_phase: Record<string, { weighted_pct: number | null; rows_closed: number; rows_open: number }> } };
}
const PLAN_REFRESH_MS = 60_000;


// ── Component ─────────────────────────────────────────────────────────────────

export const TransformationDashboard: React.FC = () => {
  const [pic, setPic] = useState<Picture | null>(null);
  const [assessing, setAssessing] = useState(false);
  const [ticking, setTicking] = useState(false);
  const [assessment, setAssessment] = useState('');
  const [orch, setOrch] = useState<OrchestrationRun | null>(null);
  const [orchestrating, setOrchestrating] = useState(false);
  const [runs, setRuns] = useState<OrchRunSummary[]>([]);
  const [error, setError] = useState('');
  const [followups, setFollowups] = useState<Followups | null>(null);
  const [followupsAt, setFollowupsAt] = useState('');       // when the live plan was last read
  const [followupsErr, setFollowupsErr] = useState('');     // a refresh that failed keeps the last good plan on screen

  const load = () => fetch('/api/v1/transformation').then(r => r.json()).then(setPic).catch(() => setError('Failed to load'));
  const loadRuns = () => fetch('/api/v1/transformation/orchestrate/runs').then(r => r.json()).then(d => setRuns(d.runs ?? [])).catch(() => {});
  // apiJson, so a 500 or a 404 from an older backend is named as such — never 'backend unreachable'
  const loadFollowups = () => apiJson<Followups>('/api/v1/plan/followups')
    .then(d => {
      if (!d.available) {
        setFollowupsErr(d.reason ?? 'the register is not readable');
        setFollowups(prev => (prev && prev.available ? prev : d));
        return;
      }
      setFollowups(d); setFollowupsErr(''); setFollowupsAt(new Date().toLocaleTimeString());
    })
    .catch(e => {
      const why = `The follow-up register could not be loaded (${errorMessage(e)}).`;
      setFollowupsErr(errorMessage(e));
      setFollowups(prev => (prev && prev.available ? prev : { available: false, reason: why } as Followups));
    });
  useEffect(() => { load(); loadRuns(); loadFollowups(); }, []);
  // W469 — the plan is live: re-read from the plan and the register every minute while the page is open
  useEffect(() => {
    const t = setInterval(loadFollowups, PLAN_REFRESH_MS);
    return () => clearInterval(t);
  }, []);

  const tick = async () => {
    setTicking(true);
    try { await apiJson('/api/v1/transformation/tick', { method: 'POST' }); await load(); } catch (e) { setError(errorMessage(e)); }   // cluster 2: 4xx/5xx surfaces too
    setTicking(false);
  };
  // W490 (sweep S6.7, C7) — a panel headed 'AI Assessment' over text the deterministic floor
  // composed from the prompt's own headings, with nothing saying so. The API now carries what
  // served it; this holds it so the panel can.
  const [assessProv, setAssessProv] = useState<{ served_by?: string | null; is_external?: boolean } | null>(null);
  const assess = async () => {
    setAssessing(true); setAssessment(''); setAssessProv(null);
    try {
      const d = await apiJson('/api/v1/transformation/assess', { method: 'POST' });
      setAssessment(d.assessment ?? '');
      setAssessProv(d.ai_provenance ?? null);
      if (!d.assessment) setError('Assessment returned no content.');
    } catch (e) { setError(errorMessage(e)); }
    setAssessing(false);
  };
  const orchestrate = async () => {
    setOrchestrating(true); setOrch(null);
    try {
      // Ledger cluster 2 — an error body must never reach the orch.validation render (it crashed the page)
      setOrch(await apiJson('/api/v1/transformation/orchestrate', {
        method: 'POST', body: { scope: 'workstation', owner_id: 'Rehan' } }));
      loadRuns();
    } catch (e) { setError(errorMessage(e)); }
    setOrchestrating(false);
  };

  const overall = pic ? Math.round(pic.realisation.overall_realisation * 100) : 0;

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Living Alignment</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Vision · Realisation · Transformation</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          One living picture — the realisation figure is API surface coverage (routers mounted, stores non-empty), not delivery: <span className="text-highlight">your vision</span>, how far the
          <span className="text-highlight"> current state realises it</span>, and the <span className="text-highlight">transformation plan</span> to close the gap.
          Continuously self-introspecting.
        </p>
        {pic?.realisation.route_census?.basis && (
          <p className="text-[10px] text-slate-600 mt-1" data-testid="route-census">Route census: {pic.realisation.route_census.basis}</p>
        )}
      </header>

      {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}

      {pic && (
        <>
          {/* Overall realisation */}
          <Card className="p-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3"><Eye size={18} className="text-highlight" /><h3 className="text-sm font-black text-white uppercase tracking-wide">Vision Realisation</h3></div>
              <div className="flex gap-2">
                <Button onClick={orchestrate} disabled={orchestrating} className="flex items-center gap-2 bg-emerald-500 text-sovereign text-xs">
                  {orchestrating ? <Loader2 size={14} className="animate-spin" /> : <Workflow size={14} />} Orchestrate
                </Button>
                <Button onClick={tick} disabled={ticking} className="flex items-center gap-2 bg-slate-800 text-white text-xs">
                  {ticking ? <Loader2 size={14} className="animate-spin" /> : <HeartPulse size={14} />} Tick
                </Button>
                <Button onClick={assess} disabled={assessing} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
                  {assessing ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} Assess
                </Button>
              </div>
            </div>
            <p className="text-slate-400 text-sm font-bold leading-relaxed mb-4">{pic.vision_summary}</p>
            <div className="flex items-end gap-3 mb-2">
              <span className="text-5xl font-black text-emerald-400">{overall}%</span>
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2">API surface coverage — not delivery (see the delivery plan)</span>
            </div>
            <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-emerald-400 to-highlight transition-all duration-700" style={{ width: `${overall}%` }} />
            </div>
            {assessment && (
              <div className="mt-5 p-4 rounded-2xl bg-slate-950 border border-highlight/20">
                <div className="flex items-center gap-2 flex-wrap mb-2">
                  <p className="text-[10px] font-black uppercase tracking-widest text-highlight">Assessment</p>
                  {/* W490 — what composed it. On the floor this is a scaffold of the headings the
                      prompt asked for, not an assessment of anything. */}
                  {(() => { const b = provenanceBadge(assessProv?.served_by, assessProv?.is_external);
                    return <span data-testid="assessment-provenance" className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`} title={b.title}>{b.label}</span>; })()}
                </div>
                <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{assessment}</p>
              </div>
            )}
          </Card>

          {/* Transformation cascade — Chief → Build-to-Order, through the VSB delivery org */}
          {orch && (
            <Card className="p-6 border-emerald-500/30 bg-emerald-500/5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-black text-emerald-400 uppercase tracking-widest text-sm flex items-center gap-2">
                  <Workflow size={16} /> Transformation Cascade · Chief → Build-to-Order
                </h3>
                {/* W481 (FU-122) — three states: a run that checked only presence is NOT ASSESSABLE */}
                <span className={`text-[10px] font-black uppercase px-2 py-1 rounded ${orch.validation.validated === true ? 'bg-emerald-500/20 text-emerald-400' : orch.validation.validated === false ? 'bg-vital/20 text-vital' : 'bg-slate-800 text-slate-400'}`}
                      title={orch.validation.validated_basis ?? ''}>
                  {orch.validation.validated === true ? 'VALIDATED' : orch.validation.validated === false ? 'NOT VALIDATED' : 'NOT ASSESSABLE'}
                </span>
              </div>
              <div className="space-y-2 mb-4">
                {orch.cascade.map(s => (
                  <div key={s.step} title={s.basis ?? ''} className="flex items-center gap-3 p-2.5 rounded-xl bg-slate-950 border border-slate-900">
                    <span className="text-[10px] font-black text-slate-600 w-4">{s.step}</span>
                    {s.verified === true ? <CheckCircle2 size={13} className={`shrink-0 ${s.checks === 'delivery' ? 'text-emerald-400' : 'text-slate-400'}`} />
                      : s.verified === null ? <span className="text-slate-500 font-black text-xs w-[13px] text-center shrink-0" aria-label="not assessable">—</span>
                      : <Circle size={13} className="text-amber-400 shrink-0" />}
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-black text-white truncate">{s.tier} <span className="text-slate-600 font-bold">→ {s.delegates_to}</span></p>
                      <p className="text-[10px] text-slate-500 truncate">{s.action}</p>
                      {/* W509 — the DELIVERY stage's verdict, on the page. It was legible only in the row's
                          `title` tooltip, and a basis that lives in a hover attribute is not on the page: not
                          in a screenshot, not in anything a reader keeps. This is the stage P2.8 is judged on,
                          so which of the four outcomes occurred is rendered rather than hinted. */}
                      {s.checks === 'delivery' && s.basis && (
                        <p data-testid="cascade-delivery-basis"
                           className={`text-[10px] mt-1 leading-relaxed ${
                             s.verified === true ? 'text-emerald-400'
                               : s.verified === false ? 'text-amber-400' : 'text-slate-400'}`}>
                          {s.basis}
                        </p>
                      )}
                    </div>
                    <span className="text-[9px] font-bold uppercase text-slate-700">{s.signal}</span>
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3 text-center">
                <Stat label="Stages verified" value={`${orch.validation.verified_stages}/${orch.validation.assessable_stages ?? orch.validation.stages} assessable · ${orch.validation.delivery_verified_stages?.length ?? 0} delivery`} />
                <Stat label="Bio signals" value={String(orch.validation.biomimetic_signals_fired)} />
                {/* W494 (FU-130 refutation) — the gate screens the intent label and a constant
                    attestation sentence, never what the delivery org produced. Said, not implied. */}
                <Stat label="Intent gate" icon={ShieldCheck}
                      value={`${orch.governance.status}${orch.governance.content_screened === false ? ' — content not screened' : ''}`} />
                <Stat label="Twin projection" value={String(orch.digital_twin.projection?.projected ?? '—')} />
              </div>
              <p className="text-[10px] text-slate-500 mt-3 leading-relaxed">{orch.validation.report}</p>
            </Card>
          )}

          {/* Recent orchestration runs (Chief → BTO history) */}
          {runs.length > 0 && (
            <Card className="p-6">
              <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2">
                <GitBranch size={14} /> Recent Transformation Orchestrations
              </h3>
              <div className="space-y-2">
                {runs.slice(0, 8).map(r => (
                  <div key={r.transformation_id} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950 border border-slate-900">
                    <div className="min-w-0">
                      <p className="text-xs font-bold text-white truncate">{r.objective}</p>
                      <p className="text-[9px] text-slate-600">{r.scope} · {r.created_at ? new Date(r.created_at).toLocaleString() : '—'}</p>
                    </div>
                    <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded shrink-0 ${r.validated === true ? 'bg-emerald-500/20 text-emerald-400' : r.validated === false ? 'bg-vital/20 text-vital' : 'bg-slate-800 text-slate-400'}`}>
                      {r.validated === true ? 'VALIDATED' : r.validated === false ? 'NOT VALIDATED' : 'NOT ASSESSABLE'}
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Pillars — vision mapped to live evidence */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Target size={14} /> Vision Pillars (router and store checks — coverage, not delivery)</h3>
            <div className="space-y-3">
              {pic.realisation.pillars.map(p => (
                <Card key={p.id} className="p-5">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-black text-white text-sm">{p.pillar}</p>
                    {/* W655 (ledger v15 R6.0) - a count of presence checks, said as that; never emerald, never "realised" */}
                    <span data-testid="pillar-checks" title={p.coverage_basis ?? ''} className="text-[10px] font-black uppercase text-slate-400">
                      {typeof p.checks_met === 'number' ? `${p.checks_met} of ${p.checks_assessed} checks present` : 'checks not reported'} · coverage, not delivery
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden mb-3">
                    <div className="h-full bg-slate-500 transition-all duration-500" style={{ width: `${p.realisation * 100}%` }} />
                  </div>
                  <div className="flex flex-wrap gap-x-4 gap-y-1">
                    {p.evidence.map((e, i) => (
                      <span key={i} className="flex items-center gap-1.5 text-[10px] font-bold">
                        {e.met ? <CheckCircle2 size={11} className="text-emerald-400" /> : <Circle size={11} className="text-slate-600" />}
                        {/* W613 (FU-504) — null is NOT ASSESSED (the route census could not be read), never "not mounted" */}
                        <span className={e.met ? 'text-slate-400' : 'text-slate-600'} title={e.basis}>{e.label}{e.met === null ? ' — not assessed' : ''}</span>
                      </span>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Transformation plan */}
          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <h3 className="font-black text-highlight uppercase tracking-widest text-sm mb-4 flex items-center gap-2"><GitBranch size={16} /> Transformation Plan (gap → action)</h3>
            {pic.transformation_plan.immediate_gaps.length > 0 && (
              <div className="mb-4">
                <p className="text-[10px] font-black uppercase tracking-widest text-amber-400 mb-2">Immediate gaps</p>
                <div className="space-y-2">
                  {pic.transformation_plan.immediate_gaps.map((g, i) => (
                    <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <p className="text-sm text-slate-300 font-bold">{g.pillar} <span className="text-amber-400 text-[10px]">({Math.round(g.realisation * 100)}%)</span></p>
                      <p className="text-[10px] text-slate-600 mt-0.5">missing: {g.missing.join(' · ')}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-4">
              <PlanList title="Short term" items={pic.transformation_plan.short_term} icon={Map} />
              <PlanList title="Long term" items={pic.transformation_plan.long_term} icon={Map} />
            </div>
          </Card>
        </>
      )}

      {/* W462 — every task a round found and did not do, slotted into the delivery plan and scheduled */}
      {followups && (
        <Card className="p-6" data-testid="followups-card">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2">
            <ListChecks size={14} /> Delivery plan — live
          </h3>
          <p className="text-[9px] text-slate-600 mb-3" data-testid="plan-live-stamp">
            {followupsAt
              ? `Read from the delivery plan and the follow-up register at ${followupsAt} · refreshes every minute`
              : (followupsErr ? 'The delivery plan has not been read yet · retrying every minute' : 'Reading the delivery plan…')}
            {followupsErr && followupsAt ? ` · the last refresh failed (${followupsErr}) — showing the plan as last read` : ''}
          </p>
          {!followups.available ? (
            <p className="text-[11px] text-slate-500">{followups.reason ?? 'The follow-up register is not readable here.'}</p>
          ) : (
            <>
              {/* W486 — where this is going, from the plan's own record. Never a date: rounds, the rate
                  they were measured from, and a plain refusal when no projection can be justified. */}
              {followups.forecast && (
                <div className="mb-3 p-3 rounded-xl bg-slate-950 border border-slate-800" data-testid="plan-pace">
                  <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-1">Where this is going</p>
                  {followups.forecast.assessable && followups.forecast.rate_used ? (
                    <>
                      <p className="text-[11px] font-black text-white">
                        {followups.forecast.next_item?.rounds_projected != null && (
                          <>~{followups.forecast.next_item.rounds_projected} round{followups.forecast.next_item.rounds_projected === 1 ? '' : 's'} to finish {followups.forecast.next_item.slot}
                            <span className="text-slate-500 font-bold"> ({followups.forecast.next_item.open_rows} open rows)</span> · </>
                        )}
                        ~{followups.forecast.all_rows_rounds_projected} round{followups.forecast.all_rows_rounds_projected === 1 ? '' : 's'} for all {followups.forecast.open_rows} open rows
                      </p>
                      <p className="text-[9px] text-slate-500 mt-1 leading-relaxed">
                        At {followups.forecast.rate_used.closed_per_round} rows closed per round, measured over{' '}
                        {followups.forecast.rate_used.rounds} round{followups.forecast.rate_used.rounds === 1 ? '' : 's'} ({followups.forecast.rate_used.source}),
                        net {followups.forecast.rate_used.net_per_round} per round after new findings.
                        {(followups.forecast.steady?.excluded?.length ?? 0) > 0 &&
                          ` One-time intake excluded: ${followups.forecast.steady!.excluded.join(', ')}.`}
                        {' '}Arithmetic over an observed mean, in rounds — not a date and not a promise.
                      </p>
                      {/* W499 — the plan's own completion, which this page did not show at all */}
                      <p className="text-[11px] font-black text-white mt-2" data-testid="plan-completion-pace">
                        {followups.forecast.items_rounds_projected != null
                          ? <>~{followups.forecast.items_rounds_projected} round{followups.forecast.items_rounds_projected === 1 ? '' : 's'} for the {followups.forecast.items_open_build} open BUILD plan items</>
                          : <>{followups.forecast.items_open_build} open build plan items — NOT PROJECTED</>}
                        {followups.forecast.items_open_owner_switch > 0 && (
                          <span className="text-slate-500 font-bold"> · {followups.forecast.items_open_owner_switch} the Owner flips ({followups.forecast.items_owner_switch_slots.join(', ')}) — not projected</span>
                        )}
                      </p>
                      {/* W501 — the bundle a round would take, with what it costs and what it is not */}
                      {followups.bundles?.bundles?.length ? (() => {
                        const bn = followups.bundles!.bundles[0];
                        const cl = followups.bundles!.ceiling;
                        return (
                          <p className="text-[10px] font-bold text-sky-300 mt-2" data-testid="next-bundle">
                            NEXT BUNDLE: {bn.slot} — one subsystem, {bn.size} row{bn.size === 1 ? '' : 's'} across {bn.files_count} file{bn.files_count === 1 ? '' : 's'}
                            {bn.component_size > bn.size && <span className="text-slate-500"> · cut from a {bn.component_size}-row component</span>}
                            {bn.also_touching.length > 0 && <span className="text-slate-500"> · advances {bn.also_touching.join(', ')} (advances — their own ACCEPT criteria close them)</span>}
                            {bn.above_measured_ceiling && cl?.rows != null && (
                              <span className="text-amber-400"> · LARGER THAN ANY ROUND YET ({cl.rows} is the most closed{cl.rounds?.length ? `, ${cl.rounds.join(', ')}` : ''})</span>
                            )}
                            {bn.possibly_under_connected && <span className="text-slate-500"> · single row: possibly under-connected, not isolated</span>}
                          </p>
                        );
                      })() : null}
                      <p className="text-[9px] text-slate-500 mt-1 leading-relaxed" data-testid="plan-completion-basis">
                        At {followups.forecast.item_build_rate_per_round} plan items per round — a rate measured
                        entirely on {followups.forecast.item_rate_phases.join(', ') || 'no completed phase'}, so it is the rate
                        THAT work closed at, applied to phases whose work differs.
                        {' '}Coverage: {followups.forecast.items_sized_build} of {followups.forecast.items_open_build} build
                        items carry a registered row; the other {followups.forecast.items_open_build - followups.forecast.items_sized_build}
                        {' '}have never been sized, so this is the weakest figure on this page.
                        {followups.forecast.items_open_unmarked.length > 0 &&
                          ` ${followups.forecast.items_open_unmarked.length} item(s) sit in a phase that declares no delivery kind and are left out: ${followups.forecast.items_open_unmarked.join(', ')}.`}
                      </p>
                    </>
                  ) : (
                    <p className="text-[11px] font-bold text-amber-400" data-testid="plan-pace-not-assessable">
                      No projection: {followups.forecast.not_assessable_because || 'the pace is not assessable yet'}.
                    </p>
                  )}
                </div>
              )}
              {followups.plan && (
                <div className="mb-3" data-testid="plan-now">
                  <p className="text-[10px] text-slate-400" hidden={followups.plan.readable === false || followups.plan.total === 0}>
                    Done {followups.plan.done} of {followups.plan.total} items — {followups.plan.phases.map(p => `${p.phase} ${p.done}/${p.total}`).join(' · ')}
                  </p>
                  {followups.plan.readable === false || followups.plan.total === 0 ? (
                    <p className="text-[11px] font-black text-amber-400 mt-1" data-testid="plan-unreadable">
                      The delivery plan could not be read — no items were found in it, so nothing here says what is next or done.
                    </p>
                  ) : followups.plan.next ? (
                    <p className="text-[11px] font-black text-white mt-1" data-testid="plan-next">
                      Next: {followups.plan.next.slot} <span className="text-slate-300 font-bold">{followups.plan.next.title}</span>
                      <span className="text-slate-500 font-bold"> — {followups.plan.next.followups
                        ? `${followups.plan.next.followups} follow-up${followups.plan.next.followups === 1 ? '' : 's'} ride it`
                        : 'no follow-ups ride it'}</span>
                    </p>
                  ) : (
                    <p className="text-[11px] font-black text-emerald-400 mt-1">Every delivery-plan item is done.</p>
                  )}
                </div>
              )}
              <p className="text-[10px] text-slate-500 mb-3">
                {followups.counts.open} follow-ups open · {followups.counts.scheduled} ride a plan item ({followups.counts.high} high)
                {followups.counts.unscheduled ? ` · ${followups.counts.unscheduled} unscheduled` : ''} · {followups.counts.awaiting_owner} awaiting the Owner · {followups.counts.done} done
              </p>
              {(() => {
                // W478 — the rows below run highest-priority first; say so, and what share of the gate's priority is closed
                const pr = followups.priority;
                const gp = pr && pr.gate_phase ? pr.completion.by_phase[pr.gate_phase] : undefined;
                return pr ? (
                  <p className="text-[10px] text-slate-500 mb-3" data-testid="plan-priority">
                    Rows run highest priority first (vision area × truth tier × reach × criticality × breadth × effort; weights in {pr.config})
                    {gp && gp.weighted_pct != null ? ` · follow-up completion weighted by priority — ${pr.gate_phase}: ${gp.weighted_pct}% of its rows' priority closed (${gp.rows_closed} of ${gp.rows_closed + gp.rows_open} rows)` : ''}
                    {pr.config_problems.length ? ` · the weights file has a problem, defaults serve: ${pr.config_problems[0]}` : ''}
                  </p>
                ) : null;
              })()}
              {!followups.integrity.ok && (
                <p className="text-[10px] text-amber-400 font-bold mb-3" title={followups.integrity.problems.join('\n')}>
                  The register is out of step with the plan — {followups.integrity.problems.length} problem(s): {followups.integrity.problems[0]}
                </p>
              )}
              <div className="space-y-3">
                {followups.schedule.map(s => (
                  <div key={s.slot}>
                    <p className="text-[10px] font-black text-white">{s.slot} <span className="text-slate-600 font-bold">— {s.title}</span>
                      {/* W499 — an item a round cannot close says so where it is queued */}
                      {s.delivered_by === 'owner-switch' && (
                        <span className="ml-2 text-[9px] text-amber-400 font-bold" data-testid={`slot-kind-${s.slot}`}>the Owner flips this — no round closes it</span>
                      )}</p>
                    {s.items.map(r => (
                      <p key={r.id} className="text-[10px] text-slate-400 mt-1 pl-3" title={`${r.why} (found ${r.source})${r.slot_source ? `\nplaced on ${r.slot} deliberately — ${r.slot_source}` : ''}${r.priority ? `\npriority ${r.priority.score}: ` + Object.entries(r.priority.basis).map(([k, v]) => `${k} — ${v}`).join('; ') : ''}`}>
                        <span className={r.severity === 'high' ? 'text-amber-400 font-black' : 'text-slate-500 font-black'}>{r.id} · {r.severity}{r.priority ? ` · p ${r.priority.score}` : ''}</span>{r.slot_source && <span className="ml-1 text-[9px] text-sky-400 font-bold" data-testid={`row-placed-${r.id}`}>placed here on purpose</span>} {r.title}
                      </p>
                    ))}
                  </div>
                ))}
                {(followups.unscheduled ?? []).length > 0 && (
                  <div data-testid="plan-unscheduled">
                    <p className="text-[10px] font-black text-amber-400">Unscheduled <span className="text-slate-500 font-bold">— riding no open plan item; each needs a slot</span></p>
                    {(followups.unscheduled ?? []).map(r => (
                      <p key={r.id} className="text-[10px] text-slate-400 mt-1 pl-3" title={`${r.why} (found ${r.source})`}>
                        <span className="text-amber-400 font-black">{r.id} · slot {r.slot}</span> {r.title}
                      </p>
                    ))}
                  </div>
                )}
                {followups.awaiting_owner.length > 0 && (
                  <div>
                    <p className="text-[10px] font-black text-white">Awaiting the Owner <span className="text-slate-600 font-bold">— recorded, never scheduled without your instruction</span></p>
                    {followups.awaiting_owner.map(r => (
                      <p key={r.id} className="text-[10px] text-slate-400 mt-1 pl-3" title={`${r.why} (found ${r.source})`}>
                        <span className="text-slate-500 font-black">{r.id}</span> {r.title}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </Card>
      )}
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string; icon?: React.ComponentType<any> }> = ({ label, value, icon: Icon }) => (
  <div className="p-2 rounded-xl bg-slate-950 border border-slate-900">
    <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1 flex items-center justify-center gap-1">{Icon && <Icon size={9} />}{label}</p>
    <p className="text-xs font-black text-emerald-400 truncate">{value}</p>
  </div>
);

const PlanList: React.FC<{ title: string; items: string[]; icon: React.ComponentType<any> }> = ({ title, items, icon: Icon }) => (
  <div>
    <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-1.5"><Icon size={12} /> {title}</p>
    <ul className="space-y-1.5">
      {items.map((it, i) => <li key={i} className="text-[11px] text-slate-500 leading-relaxed flex gap-2"><span className="text-slate-700">›</span>{it}</li>)}
    </ul>
  </div>
);
