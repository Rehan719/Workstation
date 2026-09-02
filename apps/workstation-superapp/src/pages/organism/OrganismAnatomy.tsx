import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Dna, Loader2, Settings2, ShieldCheck, Waves, Play, GitMerge, Sparkles, Send } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

// W438 — the organism's ANATOMY, finally reachable: 18 routes (config · genome · nervous ·
// self-healing · health/lifecycle) existed server-side with no page. Every sub-area was AUDITED
// (5 verdicts, ~30 findings fixed) before this tab shipped; the honesty fields the fixes added —
// provenance, wiring truth, basis strings, nulls-with-reasons — are the product here, so this
// component renders them prominently rather than hiding them behind pretty numbers.

interface HealthSummary {
  composite_health: number; composite_health_measured_only: number | null;
  composite_health_terms: Record<string, { weight: number; value: number | null; measured: boolean; basis?: string }> | null;
  health_basis: string; mode: string; summary: string; context_error?: string;
}
interface Lifecycle {
  farthest_stage: string; lifecycle_stages_reached: string[]; stages_note: string;
  vsb_spawned: boolean; vsb_operational: boolean;
  projects: { total_projects: number; by_stage: Record<string, number>; running: number; pipeline_health: string; pipeline_health_basis: string };
  vsb_entities: { total: number; operational: number; by_status: Record<string, number> };
  commercialisation_readiness: number; commercialisation_readiness_basis: string;
}
interface Systems {
  immune: { health: number; threat_level: string; errors_in_window: number; response_playbook: string[]; hot_endpoint?: string | null; hot_endpoint_errors?: number | null; hot_endpoint_tied?: string[] };
  nervous: { arousal_state: string; arousal_thresholds: Record<string, string>; signal_rate_per_second: number; total_signals: Record<string, number>; buffer_size: number; buffer_capacity: number; scope: string };
  self_healing: { overall_health: number | null; health_basis: string; open_circuits: number; tracked_endpoints: number; circuits: Record<string, { state: string; failures_in_window: number; total_calls: number; total_failures: number; failure_rate: number }>; thresholds: Record<string, number>; scope: string };
  scope: string;
}
interface NervSignal { age_seconds: number; signal_type: string; source: string; payload: string; intensity: number }
interface Genome {
  genome_id: string; entity_name: string; generation: number; fitness_score: number;
  fitness_provenance: string; encoded: boolean | null; created_at: string; domain?: string;
  traits?: Record<string, number>; trait_provenance?: { parsed: string[]; defaulted: string[] };
  served_by?: string; mutations?: string[]; encoding_note?: string; crossover_method?: string;
  parent_genomes?: string[];
}
interface ConfigPayload {
  config: Record<string, any>; governed_keys: string[]; note: string;
  key_wiring: { section: string; key: string; wired: boolean; consumer: string; governed: boolean }[];
}
interface Suggestion { section: string; key: string; suggested_value: string; coerced_value: any; valid: boolean; invalid_reason?: string; rationale: string; wired: boolean; consumer: string; governed: boolean }

const pct = (v: number | null | undefined) => (v === null || v === undefined ? '—' : `${Math.round(v * 100)}%`);

function Chip({ tone, children, title }: { tone: 'ok' | 'warn' | 'dim' | 'gov'; children: React.ReactNode; title?: string }) {
  const cls = tone === 'ok' ? 'bg-emerald-500/15 text-emerald-400' : tone === 'warn' ? 'bg-amber-500/20 text-amber-400'
    : tone === 'gov' ? 'bg-highlight/15 text-highlight' : 'bg-slate-800 text-slate-500';
  return <span title={title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cls}`}>{children}</span>;
}

export const OrganismAnatomy: React.FC = () => {
  const [health, setHealth] = useState<HealthSummary | null>(null);
  const [life, setLife] = useState<Lifecycle | null>(null);
  const [systems, setSystems] = useState<Systems | null>(null);
  const [signals, setSignals] = useState<NervSignal[]>([]);
  const [healLog, setHealLog] = useState<{ events: { ts: string; endpoint: string; state: string; reason: string }[]; events_ever: number; capacity: number } | null>(null);
  const [genomes, setGenomes] = useState<Genome[] | null>(null);   // null = not loaded (never conflate with empty)
  const [config, setConfig] = useState<ConfigPayload | null>(null);
  const [err, setErr] = useState('');
  const [loadErrs, setLoadErrs] = useState<string[]>([]);

  const loadAll = () => {
    setLoadErrs([]);
    // r.ok checked on every GET — the repo's Round-11 class-kill ("HTTP-status blindness"): a raw
    // .then(r => r.json()) renders a FastAPI error body as a result, and a swallowed catch turns
    // a failed fetch into a fabricated empty state
    const getJson = (url: string, set: (d: any) => void) =>
      fetch(url)
        .then(r => (r.ok ? r.json() : Promise.reject(new Error(`${url} → HTTP ${r.status}`))))
        .then(set)
        .catch(e => setLoadErrs(errs => [...errs, String(e?.message ?? e)]));
    getJson('/api/v1/organism/health-summary', setHealth);
    getJson('/api/v1/organism/lifecycle', setLife);
    getJson('/api/v1/organism/systems', setSystems);
    getJson('/api/v1/organism/nervous/signals?n=25', d => setSignals(d.signals || []));
    getJson('/api/v1/organism/self-healing/log', setHealLog);
    getJson('/api/v1/organism/genome', d => setGenomes(d.genomes || []));
    getJson('/api/v1/organism/config', setConfig);
  };
  useEffect(loadAll, []);

  // ── genome lab actions ──
  const [encName, setEncName] = useState('Halal community meal service');
  const [encDomain, setEncDomain] = useState('care');
  const [busy, setBusy] = useState('');
  const [selGenome, setSelGenome] = useState<Genome | null>(null);
  const [crossB, setCrossB] = useState('');

  const openGenome = async (id: string) => {
    try { setSelGenome(await apiJson(`/api/v1/organism/genome/${id}`)); } catch (e) { setErr(errorMessage(e)); }
  };
  const runEncode = async () => {
    setBusy('encode'); setErr('');
    try { setSelGenome(await apiJson('/api/v1/organism/genome/encode', { method: 'POST', body: { entity_name: encName, domain: encDomain } })); loadAll(); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  const runMutate = async (id: string) => {
    setBusy('mutate'); setErr('');
    try { setSelGenome(await apiJson('/api/v1/organism/genome/mutate', { method: 'POST', body: { genome_id: id } })); loadAll(); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  const runCross = async (a: string) => {
    if (!crossB) return;
    setBusy('cross'); setErr('');
    try { setSelGenome(await apiJson('/api/v1/organism/genome/crossover', { method: 'POST', body: { genome_a_id: a, genome_b_id: crossB } })); loadAll(); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── nervous stimulate ──
  const [stimType, setStimType] = useState<'sensory' | 'motor' | 'reflex' | 'cognitive'>('sensory');
  const runStim = async () => {
    setBusy('stim'); setErr('');
    try { await apiJson('/api/v1/organism/nervous/stimulate', { method: 'POST', body: { signal_type: stimType, source: 'anatomy-panel', payload: 'manual test signal' } }); loadAll(); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── config: ai-suggest + governed proposal via CCA ──
  const [suggest, setSuggest] = useState<{ suggestions: Suggestion[]; served_by: string; is_external: boolean } | null>(null);
  const [proposal, setProposal] = useState<{ section: string; key: string; value: string } | null>(null);
  const [ccaResult, setCcaResult] = useState<{ cca_id: string; status: string; impact_tier: string } | null>(null);
  const runSuggest = async () => {
    setBusy('suggest'); setErr(''); setSuggest(null);
    try { setSuggest(await apiJson('/api/v1/organism/config/ai-suggest', { method: 'POST', body: {} })); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  const submitProposal = async () => {
    if (!proposal) return;
    setBusy('propose'); setErr(''); setCcaResult(null);
    try {
      setCcaResult(await apiJson('/api/v1/cca/submit', { method: 'POST', body: {
        title: `Set ${proposal.section}.${proposal.key} = ${proposal.value}`,
        change_type: 'config_major',
        description: `Owner-proposed organism lever change from the Anatomy panel`,
        submitted_by: 'owner-anatomy-panel',
        config_change: { section: proposal.section, key: proposal.key, value: proposal.value },
      } }));
      setProposal(null);
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  const traitAxes = selGenome?.traits ? Object.keys(selGenome.traits) : [];

  return (
    <div className="space-y-6">
      {err && <p className="text-vital text-xs font-bold">{err}</p>}
      {loadErrs.length > 0 && (
        <p className="text-amber-400 text-[10px] font-bold">
          {loadErrs.length} section(s) failed to load — {loadErrs.slice(0, 3).join(' · ')}
        </p>
      )}

      {/* ── Health & lifecycle ─────────────────────────────────────────── */}
      <div className="grid grid-cols-1 @[960px]:grid-cols-2 gap-4">
        {health && (
          <Card className="p-5">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-2"><ShieldCheck size={14} /> Composite health — measured vs blended</h3>
            <div className="flex items-baseline gap-4 mb-2">
              <div><p className="text-3xl font-black text-white">{pct(health.composite_health_measured_only)}</p>
                <p className="text-[8px] font-black uppercase text-emerald-400">measured only</p></div>
              <div><p className="text-xl font-black text-slate-400">{pct(health.composite_health)}</p>
                <p className="text-[8px] font-black uppercase text-slate-600">blended (20% simulated)</p></div>
              <Chip tone="dim">{health.mode}</Chip>
            </div>
            <p className="text-[10px] text-slate-500 leading-relaxed mb-2">{health.health_basis}</p>
            {health.composite_health_terms && (
              <div className="flex flex-wrap gap-1.5">
                {Object.entries(health.composite_health_terms).map(([k, t]) => (
                  <Chip key={k} tone={t.measured ? 'ok' : 'warn'} title={t.basis || (t.measured ? 'measured' : 'simulated')}>
                    {k} {pct(t.value)} · w{t.weight} · {t.measured ? 'measured' : 'SIMULATED'}
                  </Chip>
                ))}
              </div>
            )}
            {health.context_error && <p className="text-[10px] text-amber-400 mt-2">organism context degraded: {health.context_error}</p>}
          </Card>
        )}
        {life && (
          <Card className="p-5">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Lifecycle pipeline</h3>
            <div className="flex items-center gap-2 flex-wrap mb-2">
              {['concept', 'prototype', 'commercialise'].map(s => (
                <Chip key={s} tone={life.lifecycle_stages_reached.includes(s) ? 'ok' : 'dim'}>{s} · {life.projects.by_stage?.[s] ?? 0}</Chip>
              ))}
              <Chip tone={life.vsb_spawned ? 'ok' : 'dim'}>VSBs {life.vsb_entities.total}</Chip>
              <Chip tone={life.vsb_operational ? 'ok' : 'dim'}>{life.vsb_entities.operational} operational</Chip>
            </div>
            <p className="text-[11px] text-slate-300 mb-1">Readiness {pct(life.commercialisation_readiness)} <span className="text-slate-600">· {life.projects.pipeline_health}</span></p>
            <p className="text-[9px] text-slate-600 leading-relaxed">{life.commercialisation_readiness_basis}</p>
            <p className="text-[9px] text-amber-200/60 italic leading-relaxed mt-1.5">{life.stages_note}</p>
          </Card>
        )}
      </div>

      {/* ── Systems: immune · nervous · self-healing ───────────────────── */}
      {systems && (
        <Card className="p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-2"><Waves size={14} /> Biomimetic systems</h3>
            <Chip tone="dim" title={systems.scope}>per-process, since start</Chip>
          </div>
          <div className="grid grid-cols-1 @[960px]:grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[9px] font-black uppercase text-slate-500 mb-1.5">Immune</p>
              <p className="text-lg font-black text-white">{pct(systems.immune.health)} <Chip tone={systems.immune.threat_level === 'NOMINAL' ? 'ok' : 'warn'}>{systems.immune.threat_level}</Chip></p>
              <p className="text-[9px] text-slate-600 mb-1">{systems.immune.errors_in_window} errors in window</p>
              {systems.immune.hot_endpoint && <p className="text-[9px] text-amber-400">hot: {systems.immune.hot_endpoint} ({systems.immune.hot_endpoint_errors} errors)</p>}
              {(systems.immune.hot_endpoint_tied || []).length > 1 && (
                <p className="text-[9px] text-slate-500">{systems.immune.hot_endpoint_tied!.length} endpoints tie at the top — none is singly hot</p>
              )}
              {(systems.immune.response_playbook || []).map((r, i) => <p key={i} className="text-[9px] text-slate-500">{r}</p>)}
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[9px] font-black uppercase text-slate-500 mb-1.5">Nervous</p>
              <p className="text-lg font-black text-white" title={Object.entries(systems.nervous.arousal_thresholds || {}).map(([k, v]) => `${k}: ${v}`).join(' · ')}>
                {systems.nervous.arousal_state} <span className="text-[10px] text-slate-500 font-bold">{systems.nervous.signal_rate_per_second}/s</span>
              </p>
              <div className="flex flex-wrap gap-1 my-1.5">
                {Object.entries(systems.nervous.total_signals).map(([k, v]) => <Chip key={k} tone="dim">{k} {v}</Chip>)}
              </div>
              <div className="flex items-center gap-1.5 mt-2">
                <select value={stimType} onChange={e => setStimType(e.target.value as any)}
                  className="text-[10px] bg-slate-900 border border-slate-800 rounded-lg p-1.5 text-slate-300">
                  {['sensory', 'motor', 'reflex', 'cognitive'].map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <button type="button" onClick={runStim} disabled={busy === 'stim'}
                  className="text-[9px] font-black uppercase px-2 py-1.5 rounded-lg border border-slate-700 text-slate-400 hover:text-white">
                  {busy === 'stim' ? '…' : 'Stimulate'}
                </button>
              </div>
              <p className="text-[8px] text-slate-700 mt-1">injections are recorded with a manual: prefix — they cannot masquerade as organic signals</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[9px] font-black uppercase text-slate-500 mb-1.5">Self-healing</p>
              <p className="text-lg font-black text-white">{systems.self_healing.overall_health === null ? <span className="text-slate-500 text-sm">no data yet</span> : pct(systems.self_healing.overall_health)}</p>
              <p className="text-[9px] text-slate-600 leading-snug mb-1" title={systems.self_healing.health_basis}>{systems.self_healing.tracked_endpoints} circuits tracked · {systems.self_healing.open_circuits} open</p>
              {Object.entries(systems.self_healing.circuits).slice(0, 4).map(([ep, c]) => (
                <p key={ep} className="text-[9px] text-slate-500 truncate">{ep}: <span className={c.state.startsWith('OPEN') ? 'text-amber-400' : 'text-emerald-400'}>{c.state}</span> · {c.total_failures}/{c.total_calls} failed</p>
              ))}
              <p className="text-[8px] text-slate-700 mt-1">trip rule: {systems.self_healing.thresholds.failure_threshold} consecutive failures (≤{systems.self_healing.thresholds.window_seconds}s apart) · retry after {systems.self_healing.thresholds.recovery_timeout}s</p>
            </div>
          </div>
          <div className="grid grid-cols-1 @[960px]:grid-cols-2 gap-3 mt-3">
            <div>
              <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">Signal feed (latest 25)</p>
              <div className="max-h-36 overflow-y-auto space-y-0.5">
                {signals.map((s, i) => (
                  <p key={i} className="text-[9px] text-slate-500 truncate">
                    <span className="text-slate-600">{s.age_seconds}s</span> · <span className="text-aura">{s.signal_type}</span> · {s.source} — {s.payload}
                  </p>
                ))}
              </div>
            </div>
            <div>
              <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">
                Healing log {healLog && <span className="normal-case">· showing {healLog.events.length} of {healLog.events_ever} events ever (cap {healLog.capacity})</span>}
              </p>
              <div className="max-h-36 overflow-y-auto space-y-0.5">
                {(healLog?.events || []).slice().reverse().map((e, i) => (
                  <p key={i} className="text-[9px] text-slate-500 truncate">{e.ts.slice(11, 19)} · {e.endpoint} → <span className="text-amber-400">{e.state}</span> — {e.reason}</p>
                ))}
                {(!healLog || healLog.events.length === 0) && <p className="text-[9px] text-slate-700 italic">no healing events this process</p>}
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* ── Genome Lab ─────────────────────────────────────────────────── */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Dna size={14} /> Genome lab</h3>
        <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">
          Encode an entity into a 10-axis trait genome, then mutate or cross lineages. Every number carries its
          provenance — an unencoded genome says so instead of wearing a flat radar, and <span className="text-aura">no fitness here is ever evaluated</span> (there is no selection step; the labels say inherited, not earned).
        </p>
        <div className="flex items-center gap-2 flex-wrap mb-3">
          <input value={encName} onChange={e => setEncName(e.target.value)}
            className="flex-1 min-w-48 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="Entity to encode…" />
          <input value={encDomain} onChange={e => setEncDomain(e.target.value)}
            className="w-28 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="domain" />
          <Button onClick={runEncode} disabled={busy === 'encode' || !encName.trim()} className="flex items-center gap-1.5 bg-aura text-sovereign text-[11px]">
            {busy === 'encode' ? <Loader2 size={12} className="animate-spin" /> : <Sparkles size={12} />} Encode
          </Button>
        </div>
        <div className="grid grid-cols-1 @[960px]:grid-cols-2 gap-3">
          <div className="max-h-56 overflow-y-auto space-y-1.5">
            {(genomes ?? []).map(g => (
              <button key={g.genome_id} type="button" onClick={() => openGenome(g.genome_id)}
                className={`w-full text-left p-2 rounded-lg border transition-colors ${selGenome?.genome_id === g.genome_id ? 'border-aura/40 bg-aura/5' : 'border-slate-900 bg-slate-950 hover:border-slate-700'}`}>
                <p className="text-[11px] font-bold text-white truncate">{g.entity_name} <span className="text-slate-600">g{g.generation}</span></p>
                <p className="text-[9px] text-slate-600 truncate" title={g.fitness_provenance}>
                  fitness {g.fitness_score} · {g.fitness_provenance?.split(' ')[0]}
                  {g.encoded === false && <span className="text-amber-400"> · NOT ENCODED</span>}
                </p>
              </button>
            ))}
            {genomes !== null && genomes.length === 0 && <p className="text-[10px] text-slate-700 italic">no genomes yet — encode one above</p>}
            {genomes === null && loadErrs.length > 0 && <p className="text-[10px] text-amber-400 italic">genome list failed to load — not empty, unknown</p>}
          </div>
          {selGenome ? (
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[11px] font-black text-white mb-1">{selGenome.entity_name} <span className="text-slate-600">gen {selGenome.generation}</span></p>
              <div className="flex flex-wrap gap-1 mb-2">
                {selGenome.served_by && <Chip tone={selGenome.encoded ? 'ok' : 'warn'}>served by {selGenome.served_by}</Chip>}
                {selGenome.encoded === false && <Chip tone="warn">not encoded — defaults</Chip>}
                <Chip tone="dim" title={selGenome.fitness_provenance || 'this genome predates provenance tracking'}>
                  fitness {selGenome.fitness_score} · {
                    !selGenome.fitness_provenance ? 'provenance unknown (pre-W438)'
                    : selGenome.fitness_provenance.includes('inherited') ? 'inherited'
                    : selGenome.fitness_provenance.includes('default') ? 'default'
                    : 'ai-declared'}
                </Chip>
                {selGenome.crossover_method && <Chip tone="dim">{selGenome.crossover_method} crossover</Chip>}
              </div>
              {selGenome.encoding_note && <p className="text-[9px] text-amber-200/70 italic mb-2">{selGenome.encoding_note}</p>}
              {!selGenome.trait_provenance && (
                <p className="text-[9px] text-amber-200/70 italic mb-2">
                  encoded before provenance tracking (pre-W438) — whether these axes were analysed
                  or defaulted is unknown; a flat all-0.5 vector here is almost certainly unencoded
                </p>
              )}
              <div className="space-y-0.5 mb-2">
                {traitAxes.map(a => {
                  const defaulted = selGenome.trait_provenance?.defaulted?.includes(a);
                  const v = selGenome.traits![a];
                  return (
                    <div key={a} className="flex items-center gap-2">
                      <span className={`text-[8px] font-bold uppercase w-24 shrink-0 ${defaulted ? 'text-slate-700' : 'text-slate-500'}`}>{a}</span>
                      <div className="flex-1 h-1.5 rounded bg-slate-900"><div className={`h-1.5 rounded ${defaulted ? 'bg-slate-700' : 'bg-aura'}`} style={{ width: `${v * 100}%` }} /></div>
                      <span className={`text-[9px] w-8 ${defaulted ? 'text-slate-700' : 'text-slate-400'}`}>{v.toFixed(2)}</span>
                    </div>
                  );
                })}
              </div>
              {(selGenome.mutations || []).length > 0 && (
                <div className="mb-2">
                  <p className="text-[8px] font-black uppercase text-slate-600">mutations (before → after)</p>
                  {selGenome.mutations!.map((m, i) => <p key={i} className="text-[9px] text-slate-500">{m}</p>)}
                </div>
              )}
              <div className="flex items-center gap-1.5 flex-wrap">
                <button type="button" onClick={() => runMutate(selGenome.genome_id)} disabled={!!busy}
                  className="text-[9px] font-black uppercase px-2 py-1 rounded-lg border border-slate-700 text-slate-400 hover:text-white flex items-center gap-1">
                  {busy === 'mutate' ? '…' : <><Play size={10} /> Mutate</>}
                </button>
                <select value={crossB} onChange={e => setCrossB(e.target.value)}
                  className="text-[9px] bg-slate-900 border border-slate-800 rounded-lg p-1 text-slate-400 max-w-36">
                  <option value="">× cross with…</option>
                  {(genomes ?? []).filter(g => g.genome_id !== selGenome.genome_id).map(g => <option key={g.genome_id} value={g.genome_id}>{g.entity_name}</option>)}
                </select>
                <button type="button" onClick={() => runCross(selGenome.genome_id)} disabled={!!busy || !crossB}
                  className="text-[9px] font-black uppercase px-2 py-1 rounded-lg border border-slate-700 text-slate-400 hover:text-white flex items-center gap-1 disabled:opacity-40">
                  {busy === 'cross' ? '…' : <><GitMerge size={10} /> Crossover</>}
                </button>
              </div>
            </div>
          ) : <p className="text-[10px] text-slate-700 italic p-3">select a genome to inspect its provenance</p>}
        </div>
      </Card>

      {/* ── Config — an honest lever panel, not a settings form ─────────── */}
      {config && (
        <Card className="p-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Settings2 size={14} /> Reconfiguration — the wiring truth</h3>
          <p className="text-[10px] text-slate-500 mb-3 leading-relaxed">
            Only <span className="text-aura">wired</span> keys change live behaviour; stored-only keys are displayed so a dead
            switch can never pass as a control. The four live levers are <span className="text-highlight">CCA-governed</span> —
            proposing one submits an audited change request (review + apply happen on the Change Control surface, arms-length).
          </p>
          <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-1.5 mb-3">
            {config.key_wiring.map(k => {
              const val = config.config?.[k.section]?.[k.key];
              return (
                <div key={`${k.section}.${k.key}`} className="flex items-center justify-between gap-2 p-2 rounded-lg bg-slate-950 border border-slate-900">
                  <div className="min-w-0">
                    <p className="text-[10px] font-bold text-slate-300 truncate">{k.section}.{k.key} = <span className="text-white">{String(val)}</span></p>
                    <p className="text-[8px] text-slate-600 truncate" title={k.consumer}>{k.consumer}</p>
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    {k.governed && <Chip tone="gov">governed</Chip>}
                    <Chip tone={k.wired ? 'ok' : 'dim'}>{k.wired ? 'wired' : 'stored-only'}</Chip>
                    {k.governed && (
                      <button type="button" onClick={() => setProposal({ section: k.section, key: k.key, value: String(val) })}
                        className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded border border-highlight/40 text-highlight hover:bg-highlight/10">propose</button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
          {proposal && (
            <div className="p-3 rounded-xl bg-highlight/5 border border-highlight/20 mb-3 flex items-center gap-2 flex-wrap">
              <p className="text-[10px] font-bold text-slate-300">Propose {proposal.section}.{proposal.key} =</p>
              <input value={proposal.value} onChange={e => setProposal({ ...proposal, value: e.target.value })}
                className="w-24 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-white" />
              <Button onClick={submitProposal} disabled={busy === 'propose'} className="flex items-center gap-1.5 bg-highlight text-sovereign text-[10px]">
                {busy === 'propose' ? <Loader2 size={11} className="animate-spin" /> : <Send size={11} />} Submit to CCA
              </Button>
              <button type="button" onClick={() => setProposal(null)} className="text-[9px] text-slate-500 hover:text-white">cancel</button>
            </div>
          )}
          {ccaResult && (
            <p className="text-[10px] text-emerald-400 mb-3">
              Submitted as {ccaResult.cca_id} · tier {ccaResult.impact_tier} · status {ccaResult.status} — track and implement it on the Change Control page.
            </p>
          )}
          <div className="flex items-center gap-2 mb-2">
            <Button onClick={runSuggest} disabled={busy === 'suggest'} className="flex items-center gap-1.5 bg-slate-900 text-slate-300 text-[10px]">
              {busy === 'suggest' ? <Loader2 size={11} className="animate-spin" /> : <Sparkles size={11} />} AI-suggest changes
            </Button>
            {suggest && <Chip tone={suggest.is_external ? 'warn' : 'ok'}>served by {suggest.served_by}</Chip>}
          </div>
          {suggest && suggest.suggestions.length === 0 && <p className="text-[10px] text-slate-600 italic">no suggestions parsed from this serve — advisory only, nothing fabricated to fill the gap</p>}
          {(suggest?.suggestions || []).map((s, i) => (
            <div key={i} className="p-2 rounded-lg bg-slate-950 border border-slate-900 mb-1 flex items-center justify-between gap-2">
              <div className="min-w-0">
                <p className="text-[10px] text-slate-300 truncate">{s.section}.{s.key} → <span className="text-white">{s.suggested_value}</span></p>
                <p className="text-[8px] text-slate-600 truncate">{s.rationale}</p>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                {!s.valid && <Chip tone="warn" title={s.invalid_reason}>invalid</Chip>}
                <Chip tone={s.wired ? 'ok' : 'dim'}>{s.wired ? 'wired' : 'changes nothing'}</Chip>
                {s.valid && s.governed && (
                  <button type="button" onClick={() => setProposal({ section: s.section, key: s.key, value: String(s.coerced_value) })}
                    className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded border border-highlight/40 text-highlight hover:bg-highlight/10">propose</button>
                )}
              </div>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
};
