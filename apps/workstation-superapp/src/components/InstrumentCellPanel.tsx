import React, { useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

// W640 (plan item P3.31) — THE INSTRUMENT CELL, ON THE FABRIC'S OWN PAGE.
// Everything shown here is the server's statement, printed with its basis: which resources the fabric can
// actually run (and why not, when it cannot), and a PROPOSAL for an objective — the smallest available set
// covering requirements the person states. A proposal saves nothing and runs nothing, and the panel says so
// in the server's words. No status here is decided in the browser.

interface Avail {
  id: string; name: string; state: string; reason: string; endpoint_state: string; endpoint_basis: string; not_checked: string;
  // P3.31 clause 1 (round 10) - what the registration declares it needs, checked by the server at the call
  needs_declared?: boolean; needs_state?: string; needs_basis?: string; needs_per_run?: string[];
  needs_narrowed?: { needs: string; why: string }[];
  checked?: string; checked_basis?: string;
}
interface AvailReply {
  resources: Avail[]; counts: Record<string, number>; total: number; basis: string; available_without_engine?: string[];
  needs_counts?: Record<string, number>; checked_counts?: Record<string, number>; needs_declared?: number; needs_basis?: string;
  declaration_defects: { id: string; endpoint_state: string; basis: string }[];
}
interface Selected {
  id: string; name: string; covers: string[];
  contract: { when_run: string; persists: string; persists_basis: string; equivalents: string[] };
  availability: { state: string; endpoint_state?: string; endpoint_basis?: string;
                  needs_state?: string; needs_basis?: string; needs_per_run?: string[];
                  needs_narrowed?: { needs: string; why: string }[] };
}
interface Proposal {
  what_this_is: string; saved: boolean; ran: boolean; requirements_confirmed: boolean;
  objective?: string;
  suggested_requirements?: { capability: string; first_declared_by: string }[];
  suggestion_basis?: string;
  selection: null | {
    selected: Selected[]; uncovered: string[]; uncovered_basis: string; method: string;
    requirements?: string[];
    excluded: { id: string; would_cover: string[]; because: string }[];
  };
  alternatives?: Record<string, { id: string; availability: string }[]>;
  alternatives_basis?: string;
  limits: { max_stages: number; ceiling: number; ceiling_basis: string; attempts_per_resource: number; attempts_basis: string };
}
// P3.31 (round 9) - clause 5 on the page. A criterion and its evidence are objects or strings as the
// server sent them; both are turned into text before they are drawn (an object is never a React child).
interface RunRow {
  run_id: string; name: string; created_at: string;
  real_resources?: { resource: string; outcome?: string; alternative_for?: string }[];
  specification?: SpecLink | null;
}
interface RunList { runs?: RunRow[]; listing_is_incomplete?: boolean; listing_basis?: string }
interface CriterionRow { criterion: unknown; state: string; evidence: unknown; basis: string }
interface VerifyReply {
  run_id: string; criteria: CriterionRow[]; counts: Record<string, number>; all_met: boolean; all_met_basis: string;
  attempted?: string[]; not_attempted?: string[] | null; attempt_basis?: string;
  stand_ins?: { for: string; resource: string; outcome?: string; label: string }[];
  criteria_source?: string; criteria_source_basis?: string;
}
// P3.31 - a proposal a person chose to KEEP (an assembly specification), and what a run made from one
// records. Every field is the server's; nothing here decides a status.
interface SpecLink {
  specification_id: string; specification_digest: string; version?: number | null; proposed?: string[];
  refused?: boolean;
  executed?: { resource: string; outcome?: string | null; available_at_run?: boolean | null; stand_in?: { tried?: string | null } }[];
  not_attempted?: { resource: string; why: string; basis?: string | null }[];
  not_in_specification?: { resource: string; outcome?: string | null; alternative_for?: string }[];
  unavailable_at_run?: { id: string; because: string }[];
  basis?: string;
}
interface SpecRow {
  id: string; lineage?: string; version: number; digest: string; supersedes?: string | null;
  superseded_by?: string | null; is_latest?: boolean; digest_ok?: boolean;
  objective: string; required_capabilities?: string[]; acceptance_criteria?: unknown[];
  proposed?: { id: string; covers?: string[] }[]; selection_rule?: string; uncovered?: string[];
  saved_by?: string; saved_at?: string;
}
interface SpecList { specifications?: SpecRow[] }
interface SpecSaveReply extends SpecRow { saved: boolean; already_saved?: boolean }
interface SpecDetail extends SpecRow {
  versions?: { id: string; version: number; digest: string }[];
  availability_now?: { id: string; available: boolean; because: string; registration_changed?: boolean | null; equivalents?: string[] }[];
  replay?: { basis?: string; compositions?: { id: string; name: string; missing: string[]; extra: string[] }[] };
}
interface ReplayReply {
  run_id?: string; refused?: boolean; final?: unknown; specification?: SpecLink | null;
  run_record?: { persisted: boolean; reason?: string };
}
const fetchSpecs = () => apiJson<SpecList>('/api/v1/resources/specifications');
const OUTCOMES = ['produced', 'read', 'assessed', 'specified', 'narrated'];
const VERDICT_WORD: Record<string, string> = { met: 'met', unmet: 'NOT met', not_assessed: 'not assessed' };
const VERDICT_STYLE: Record<string, string> = {
  met: 'border-emerald-500/30 text-emerald-300',
  unmet: 'border-rose-500/40 text-rose-300',
  not_assessed: 'border-slate-600 text-slate-400',
};
const asText = (v: unknown): string => (typeof v === 'string' ? v : JSON.stringify(v));

const STATE_STYLE: Record<string, string> = {
  available: 'border-emerald-500/30 text-emerald-300',
  prompt_stage_only: 'border-amber-500/40 text-amber-300',
  not_checked: 'border-slate-600 text-slate-400',
};
const STATE_WORD: Record<string, string> = {
  available: 'fabric can run it',
  prompt_stage_only: 'prompt stage only — engine not run',
  not_checked: 'not checked',
};
// P3.31 clause 1 (round 10) - the clause's own three words, and the server's word shown as itself when new
const CHECKED_WORD: Record<string, string> = {
  available: 'available', unavailable: 'unavailable', not_checked: 'not checked',
};
const NEED_WORD: Record<string, string> = {
  met: 'declared needs met', unmet: 'a declared need is NOT met', not_declared: 'needs NOT DECLARED',
  not_checked: 'needs could not be checked',
};

export function InstrumentCellPanel() {
  const [avail, setAvail] = useState<AvailReply | null>(null);
  const [err, setErr] = useState('');
  const [objective, setObjective] = useState('');
  const [reqs, setReqs] = useState('');
  const [busy, setBusy] = useState(false);
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [showAll, setShowAll] = useState(false);
  // P3.31 (round 9) - check a recorded run against stated criteria
  const [runs, setRuns] = useState<RunRow[]>([]);
  const [runsErr, setRunsErr] = useState('');
  const [runsNote, setRunsNote] = useState('');
  const [runId, setRunId] = useState('');
  const [want, setWant] = useState<Record<string, string>>({});
  const [wantGate, setWantGate] = useState(false);
  const [freeText, setFreeText] = useState('');
  const [verdict, setVerdict] = useState<VerifyReply | null>(null);
  const [vBusy, setVBusy] = useState(false);
  const [vErr, setVErr] = useState('');
  // P3.31 - keep a proposal, list kept ones, run one again, and see proposed versus executed
  const [specs, setSpecs] = useState<SpecRow[]>([]);
  const [specErr, setSpecErr] = useState('');
  const [specMsg, setSpecMsg] = useState('');
  const [specBusy, setSpecBusy] = useState(false);
  const [specDetail, setSpecDetail] = useState<SpecDetail | null>(null);
  const [specComp, setSpecComp] = useState('');
  const [replay, setReplay] = useState<ReplayReply | null>(null);
  const [specWant, setSpecWant] = useState<Record<string, string>>({});
  const [specGate, setSpecGate] = useState(false);
  const [specText, setSpecText] = useState('');

  useEffect(() => {
    apiJson<AvailReply>('/api/v1/resources/cell/availability').then(setAvail).catch(e => setErr(errorMessage(e)));
    apiJson<RunList>('/api/v1/resources/compositions/runs?limit=10')
      .then(d => { setRuns(d.runs ?? []); setRunsNote(d.listing_is_incomplete ? (d.listing_basis ?? 'The run history could not be read whole.') : ''); })
      .catch(e => setRunsErr(errorMessage(e)));
    fetchSpecs().then(d => setSpecs(d.specifications ?? [])).catch(e => setSpecErr(errorMessage(e)));
  }, []);

  const propose = async (required: string[]) => {
    setBusy(true); setErr('');
    try {
      setProposal(await apiJson<Proposal>('/api/v1/resources/cell/propose', {
        method: 'POST', body: { objective, required_capabilities: required },
      }));
    } catch (e) { setErr(errorMessage(e)); }
    setBusy(false);
  };
  const stated = reqs.split(',').map(s => s.trim()).filter(Boolean);
  const notRunnable = (avail?.resources ?? []).filter(r => r.state !== 'available');
  const keepSpec = async (supersedes: string | null) => {
    // what is kept is fixed HERE, before the request, from the proposal the server returned - not from the
    // two inputs, which may have been typed in since
    const shown = proposal;
    const sel = shown?.selection;
    if (!shown || !sel) { setSpecErr('There is no proposal to keep.'); return; }
    const criteria: unknown[] = [];
    for (const s of sel.selected) {
      const outcome = specWant[s.id];
      if (outcome) criteria.push({ kind: 'resource_outcome', resource: s.id, is: outcome });
    }
    if (specGate) criteria.push({ kind: 'quality_gate' });
    for (const line of specText.split('\n').map(x => x.trim()).filter(Boolean)) criteria.push(line);
    setSpecBusy(true); setSpecErr(''); setSpecMsg('');
    try {
      const kept = await apiJson<SpecSaveReply>('/api/v1/resources/specifications', {
        method: 'POST',
        body: {
          objective: shown.objective ?? objective, required_capabilities: sel.requirements ?? stated,
          acceptance_criteria: criteria, ...(supersedes ? { supersedes } : {}),
        },
      });
      setSpecMsg(kept.saved
        ? `Kept as ${kept.id}, version ${kept.version}, digest ${String(kept.digest).slice(0, 12)}. Nothing was run.`
        : `This content is already kept as ${kept.id}, version ${kept.version}. Nothing new was written.`);
      const d = await fetchSpecs();
      setSpecs(d.specifications ?? []);
    } catch (e) { setSpecErr(errorMessage(e)); }
    setSpecBusy(false);
  };
  const openSpec = async (id: string) => {
    setSpecErr(''); setReplay(null); setSpecComp('');
    try {
      setSpecDetail(await apiJson<SpecDetail>(`/api/v1/resources/specifications/${encodeURIComponent(id)}`));
    } catch (e) { setSpecErr(errorMessage(e)); }
  };
  const runSpec = async () => {
    // which specification and which composition are fixed HERE, before the request
    const spec = specDetail;
    const cid = specComp;
    if (!spec || !cid) { setSpecErr('Open a kept specification and pick a saved composition to run it through.'); return; }
    setSpecBusy(true); setSpecErr(''); setReplay(null);
    try {
      setReplay(await apiJson<ReplayReply>(`/api/v1/resources/compositions/${encodeURIComponent(cid)}/run`, {
        method: 'POST',
        body: { objective: spec.objective, specification_id: spec.id, specification_digest: spec.digest },
      }));
    } catch (e) { setSpecErr(errorMessage(e)); }
    setSpecBusy(false);
  };
  const verifyKept = async () => {
    // no criteria are sent: the server reads the run against the criteria kept with its specification
    const id = runId;
    if (!id) { setVErr('Pick a recorded run.'); return; }
    setVBusy(true); setVErr(''); setVerdict(null);
    try {
      setVerdict(await apiJson<VerifyReply>('/api/v1/resources/cell/verify', { method: 'POST', body: { run_id: id } }));
    } catch (e) { setVErr(errorMessage(e)); }
    setVBusy(false);
  };
  const pickedRun = runs.find(r => r.run_id === runId) ?? null;
  const verify = async () => {
    // what is being checked is fixed HERE, before the request: a selection changed while it is in flight
    // must not be the one the answer is filed under
    const id = runId;
    const picked = runs.find(r => r.run_id === id);
    const criteria: unknown[] = [];
    for (const rr of (picked?.real_resources ?? [])) {
      const outcome = want[rr.resource];
      if (outcome) criteria.push({ kind: 'resource_outcome', resource: rr.resource, is: outcome });
    }
    if (wantGate) criteria.push({ kind: 'quality_gate' });
    for (const line of freeText.split('\n').map(s => s.trim()).filter(Boolean)) criteria.push(line);
    if (!id || criteria.length === 0) { setVErr('Pick a recorded run and state at least one criterion.'); return; }
    setVBusy(true); setVErr(''); setVerdict(null);
    try {
      setVerdict(await apiJson<VerifyReply>('/api/v1/resources/cell/verify', {
        method: 'POST', body: { run_id: id, criteria },
      }));
    } catch (e) { setVErr(errorMessage(e)); }
    setVBusy(false);
  };

  return (
    <section data-testid="instrument-cell" className="p-5 rounded-2xl border border-slate-800 bg-slate-950/60 space-y-4">
      <div>
        <h2 className="text-sm font-black uppercase tracking-widest text-white">Instrument Cell</h2>
        <p className="text-[11px] text-slate-400 mt-1">
          Which resources the fabric can run now, and a proposal for an objective. A proposal saves nothing and runs nothing.
        </p>
      </div>
      {err && <p className="text-[11px] text-rose-400">{err}</p>}

      {avail && (
        <div data-testid="cell-availability" className="space-y-2">
          <p className="text-[11px] text-slate-300">
            {Object.entries(avail.counts).map(([k, v]) => `${v} ${STATE_WORD[k] ?? k}`).join(' · ')} — of {avail.total} registered.
          </p>
          <p className="text-[10px] text-slate-500">{avail.basis}</p>
          {Array.isArray(avail.available_without_engine) && avail.available_without_engine.length > 0 && (
            <p data-testid="cell-available-without-engine" className="text-[10px] text-amber-300/90">
              {avail.available_without_engine.length} of the available run no engine when composed: {avail.available_without_engine.join(', ')}.
            </p>
          )}
          {avail.checked_counts && (
            <p data-testid="cell-checked" className="text-[11px] text-slate-300">
              Checked against what each declares it needs: {Object.entries(avail.checked_counts).map(([k, v]) => `${v} ${CHECKED_WORD[k] ?? k}`).join(' · ')}.
              <span className="block text-[10px] text-slate-500">{avail.needs_basis}</span>
            </p>
          )}
          {(avail.resources ?? []).filter(r => r.needs_state === 'unmet').length > 0 && (
            <ul data-testid="cell-needs-unmet" className="space-y-1">
              {avail.resources.filter(r => r.needs_state === 'unmet').map(r => (
                <li key={r.id} className="text-[11px] px-2 py-1 rounded-lg border border-rose-500/40 text-rose-300">
                  <span className="font-bold">{r.name}</span> — unavailable. {r.needs_basis}
                </li>
              ))}
            </ul>
          )}
          {notRunnable.length > 0 && (
            <ul className="space-y-1">
              {notRunnable.map(r => (
                <li key={r.id} className={`text-[11px] px-2 py-1 rounded-lg border ${STATE_STYLE[r.state] ?? STATE_STYLE.not_checked}`}>
                  <span className="font-bold">{r.name}</span> — {STATE_WORD[r.state] ?? r.state}. {r.reason}
                </li>
              ))}
            </ul>
          )}
          {avail.declaration_defects.length > 0 && (
            <ul data-testid="cell-declaration-defects" className="space-y-1">
              {avail.declaration_defects.map(d => (
                <li key={d.id} className="text-[11px] px-2 py-1 rounded-lg border border-rose-500/40 text-rose-300">
                  <span className="font-bold">{d.id}</span> — {d.basis}
                </li>
              ))}
            </ul>
          )}
          <button type="button" onClick={() => setShowAll(v => !v)} className="text-[10px] text-sky-400 underline underline-offset-2">
            {showAll ? 'Hide' : 'Show'} all {avail.total}
          </button>
          {showAll && (
            <ul className="grid grid-cols-1 @[640px]:grid-cols-2 gap-1">
              {avail.resources.map(r => (
                <li key={r.id} className={`text-[10px] px-2 py-1 rounded-lg border ${STATE_STYLE[r.state] ?? STATE_STYLE.not_checked}`}>
                  {r.name} — {STATE_WORD[r.state] ?? r.state}
                  {r.needs_state ? ` · ${NEED_WORD[r.needs_state] ?? r.needs_state}` : ''}
                  {(r.needs_narrowed ?? []).map(n => (
                    <span key={n.needs} data-testid="cell-listed-narrowed" className="block text-amber-300">Here, without {n.needs}: {n.why}</span>
                  ))}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="space-y-2">
        <input value={objective} onChange={e => setObjective(e.target.value)} placeholder="Objective"
          aria-label="Objective" className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white" />
        <input value={reqs} onChange={e => setReqs(e.target.value)} placeholder="Required capabilities, comma-separated (leave empty for suggestions)"
          aria-label="Required capabilities" className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white" />
        <button type="button" disabled={busy || !objective.trim()} onClick={() => propose(stated)}
          className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-[11px] font-bold disabled:opacity-40">
          {busy ? 'Working…' : stated.length ? 'Propose a set' : 'Suggest requirements'}
        </button>
      </div>

      {proposal && (
        <div data-testid="cell-proposal" className="space-y-2 p-3 rounded-xl border border-slate-800">
          <p className="text-[11px] text-amber-300">{proposal.what_this_is}</p>
          {!proposal.requirements_confirmed && (
            <>
              <p className="text-[10px] text-slate-500">{proposal.suggestion_basis}</p>
              {(proposal.suggested_requirements ?? []).length === 0
                ? <p className="text-[11px] text-slate-300">No capability tag appears in that objective. State the capabilities you need.</p>
                : (
                  <div className="flex flex-wrap gap-1">
                    {(proposal.suggested_requirements ?? []).map(s => (
                      <button key={s.capability} type="button"
                        onClick={() => setReqs(prev => (prev.trim() ? `${prev}, ${s.capability}` : s.capability))}
                        className="text-[10px] px-2 py-0.5 rounded-full border border-slate-700 text-slate-300">
                        + {s.capability}
                      </button>
                    ))}
                  </div>
                )}
            </>
          )}
          {proposal.selection && (
            <>
              <p className="text-[10px] text-slate-500">{proposal.selection.method}</p>
              {proposal.selection.selected.length === 0 && (
                <p className="text-[11px] text-slate-300">No available resource covers what was stated.</p>
              )}
              <ul className="space-y-1">
                {proposal.selection.selected.map(s => (
                  <li key={s.id} className="text-[11px] px-2 py-1 rounded-lg border border-emerald-500/30 text-slate-200">
                    <span className="font-bold">{s.name}</span> — covers {s.covers.join(', ')}. {s.contract.when_run}.
                    <span className="block text-[10px] text-slate-500">What it persists: {s.contract.persists_basis}</span>
                    {s.availability.needs_state === 'not_declared' && (
                      <span data-testid="cell-needs-not-declared" className="block text-[10px] text-amber-300">
                        Its needs are not declared: it is proposed because the fabric has a handler for it, and nothing else about it was checked.
                      </span>
                    )}
                    {(s.availability.needs_per_run ?? []).length > 0 && (
                      <span data-testid="cell-needs-per-run" className="block text-[10px] text-amber-300">
                        Runs nothing unless configured: {(s.availability.needs_per_run ?? []).join(', ')}.
                      </span>
                    )}
                    {(s.availability.needs_narrowed ?? []).map(n => (
                      <span key={n.needs} data-testid="cell-needs-narrowed" className="block text-[10px] text-amber-300">
                        Here, without {n.needs}: {n.why}
                      </span>
                    ))}
                    {(s.availability.endpoint_state === 'not_served' || s.availability.endpoint_state === 'method_mismatch') && (
                      <span data-testid="cell-endpoint-defect" className="block text-[10px] text-rose-300">
                        Its declaration is wrong: {s.availability.endpoint_basis}. The fabric runs this resource in-process and does not call that address, so it can still run.
                      </span>
                    )}
                    {(proposal.alternatives?.[s.id] ?? []).length > 0 && (
                      <span className="block text-[10px] text-slate-500">
                        Declared equivalent: {(proposal.alternatives?.[s.id] ?? []).map(a => `${a.id} (${STATE_WORD[a.availability] ?? a.availability})`).join(', ')}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
              {proposal.selection.uncovered.length > 0 && (
                <p data-testid="cell-uncovered" className="text-[11px] text-rose-300">
                  Not covered by anything: {proposal.selection.uncovered.join(', ')}. <span className="text-slate-500">{proposal.selection.uncovered_basis}</span>
                </p>
              )}
              {proposal.selection.excluded.length > 0 && (
                <ul className="space-y-1">
                  {proposal.selection.excluded.map(x => (
                    <li key={x.id} className="text-[10px] text-slate-500">Left out — {x.id}: {x.because}</li>
                  ))}
                </ul>
              )}
              {proposal.alternatives_basis && <p className="text-[10px] text-slate-500">{proposal.alternatives_basis}</p>}
            </>
          )}
          <p className="text-[10px] text-slate-600">
            Limit: {proposal.limits.max_stages} resources per proposal (ceiling {proposal.limits.ceiling} — {proposal.limits.ceiling_basis}). {proposal.limits.attempts_basis}.
          </p>
          {proposal.selection && proposal.selection.selected.length > 0 && (
            <div data-testid="cell-keep" className="space-y-2 pt-2 border-t border-slate-800">
              <p className="text-[11px] font-bold text-slate-200">Keep this proposal as a specification</p>
              <p className="text-[10px] text-slate-500">
                Keeping records the objective, the requirements, the criteria below and the proposed resources, with a digest of that content. It runs nothing. A kept specification is never edited: keeping a changed one makes a new version.
              </p>
              {proposal.selection.selected.map(s => (
                <label key={s.id} className="flex flex-wrap items-center gap-2 text-[11px] text-slate-300">
                  <span className="font-mono">{s.id}</span>
                  <span className="text-[10px] text-slate-500">must end</span>
                  <select value={specWant[s.id] ?? ''} aria-label={`Required outcome of ${s.id} in the specification`}
                    onChange={e => { const v = e.target.value; setSpecWant(w => ({ ...w, [s.id]: v })); }}
                    className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-white">
                    <option value="">no criterion</option>
                    {OUTCOMES.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                </label>
              ))}
              <label className="flex items-center gap-2 text-[11px] text-slate-300">
                <input type="checkbox" checked={specGate} onChange={e => setSpecGate(e.target.checked)} /> the quality gate passed
              </label>
              <textarea value={specText} onChange={e => setSpecText(e.target.value)} rows={2} aria-label="Other acceptance criteria"
                placeholder="Other acceptance criteria, one per line. Nothing here can read a run against a sentence, so each will be recorded as not assessed."
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white" />
              <div className="flex flex-wrap gap-2">
                <button type="button" disabled={specBusy} onClick={() => keepSpec(null)}
                  className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-[11px] font-bold disabled:opacity-40">
                  {specBusy ? 'Working...' : 'Keep as a new specification'}
                </button>
                {specDetail && specDetail.is_latest && (
                  <button type="button" disabled={specBusy} onClick={() => keepSpec(specDetail.id)}
                    className="px-3 py-1.5 rounded-lg border border-slate-700 text-slate-300 text-[11px] font-bold disabled:opacity-40">
                    Keep as the next version of {specDetail.id}
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      <div data-testid="cell-specifications" className="space-y-2 p-3 rounded-xl border border-slate-800">
        <p className="text-[11px] font-bold text-slate-200">Kept specifications</p>
        {specErr && <p role="alert" data-testid="cell-spec-error" className="text-[11px] text-rose-400">{specErr}</p>}
        {specMsg && <p data-testid="cell-spec-message" className="text-[11px] text-emerald-300">{specMsg}</p>}
        {specs.length === 0 && !specErr && <p className="text-[11px] text-slate-400">No specification has been kept.</p>}
        <ul className="space-y-1">
          {specs.map(s => (
            <li key={s.id} className="text-[11px] px-2 py-1 rounded-lg border border-slate-800 text-slate-300">
              <button type="button" onClick={() => openSpec(s.id)} className="font-mono text-sky-400 underline underline-offset-2">{s.id}</button>
              {` version ${s.version}, digest ${String(s.digest ?? '').slice(0, 12)}: ${s.objective}`}
              {s.superseded_by ? <span className="text-amber-300"> Superseded by {s.superseded_by}.</span> : null}
              {s.digest_ok === false ? <span className="text-rose-300"> Its content no longer has the digest it was kept under.</span> : null}
            </li>
          ))}
        </ul>
        {specDetail && (
          <div data-testid="cell-spec-detail" className="space-y-1 pt-2 border-t border-slate-800">
            <p className="text-[11px] text-slate-200">
              {specDetail.id}, version {specDetail.version}. Kept by {specDetail.saved_by ?? 'not recorded'} at {specDetail.saved_at ?? 'not recorded'}. Digest {specDetail.digest}.
            </p>
            <p className="text-[11px] text-slate-300">
              Objective: {specDetail.objective}. Requirements: {(specDetail.required_capabilities ?? []).join(', ') || 'none'}. Not covered: {(specDetail.uncovered ?? []).join(', ') || 'nothing'}.
            </p>
            <p className="text-[10px] text-slate-500">{specDetail.selection_rule}</p>
            <p className="text-[11px] text-slate-300">Criteria: {(specDetail.acceptance_criteria ?? []).map(c => asText(c)).join(' | ') || 'none stated'}</p>
            <p data-testid="cell-spec-versions" className="text-[10px] text-slate-400">
              Versions: {(specDetail.versions ?? []).map(v => `${v.version} = ${v.id}, digest ${String(v.digest ?? '').slice(0, 12)}`).join('; ') || 'not listed'}
            </p>
            <ul className="space-y-1">
              {(specDetail.availability_now ?? []).map(a => (
                <li key={a.id} data-testid="cell-spec-now"
                  className={`text-[11px] px-2 py-1 rounded-lg border ${a.available ? 'border-emerald-500/30 text-slate-200' : 'border-rose-500/40 text-rose-300'}`}>
                  <span className="font-mono">{a.id}</span>: {a.available ? 'available now' : 'NOT available now'}. {a.because}
                  {a.registration_changed ? ' Its registration is not the one that was proposed.' : ''}
                  {!a.available && (a.equivalents ?? []).length > 0 ? ` Declared equivalent: ${(a.equivalents ?? []).join(', ')}.` : ''}
                </li>
              ))}
            </ul>
            <p className="text-[10px] text-slate-500">{specDetail.replay?.basis}</p>
            <select value={specComp} aria-label="Composition to run this specification through"
              onChange={e => { setSpecComp(e.target.value); setReplay(null); }}
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white">
              <option value="">Pick a saved composition</option>
              {(specDetail.replay?.compositions ?? []).map(c => (
                <option key={c.id} value={c.id}>
                  {`${c.name}: ${c.missing.length === 0 && c.extra.length === 0 ? 'holds exactly what was proposed' : `missing ${c.missing.join(', ') || 'nothing'}; extra ${c.extra.join(', ') || 'nothing'}`}`}
                </option>
              ))}
            </select>
            <button type="button" disabled={specBusy || !specComp} onClick={runSpec}
              className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-[11px] font-bold disabled:opacity-40">
              {specBusy ? 'Working...' : 'Run it again from this specification'}
            </button>
            {replay && (
              <div data-testid="cell-replay" className="space-y-1">
                {replay.refused && <p className="text-[11px] text-rose-300">{asText(replay.final ?? 'The run was refused.')}</p>}
                {replay.run_id && (
                  <p className="text-[11px] text-slate-200">
                    Run {replay.run_id}.{replay.run_record && replay.run_record.persisted === false ? ` Its record was NOT filed: ${replay.run_record.reason ?? 'no reason given'}.` : ''}
                  </p>
                )}
                {replay.specification && <ProposedVsExecuted link={replay.specification} />}
              </div>
            )}
          </div>
        )}
      </div>

      <div data-testid="cell-verify" className="space-y-2 p-3 rounded-xl border border-slate-800">
        <p className="text-[11px] font-bold text-slate-200">Check a recorded run against stated criteria</p>
        <p className="text-[10px] text-slate-500">
          This reads a run that already happened; it runs nothing. A criterion nothing here can read ends as not assessed, and not assessed never counts as met.
        </p>
        {runsErr && <p role="alert" data-testid="cell-runs-error" className="text-[11px] text-rose-400">{runsErr} No run is listed.</p>}
        {runsNote && <p className="text-[10px] text-amber-300">{runsNote}</p>}
        {!runsErr && runs.length === 0 && (
          <p className="text-[11px] text-slate-400">No recorded run is listed, so there is nothing to check yet.</p>
        )}
        {runs.length > 0 && (
          <>
            <select value={runId} aria-label="Run to check"
              onChange={e => { setRunId(e.target.value); setWant({}); setVerdict(null); setVErr(''); }}
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white">
              <option value="">Pick a recorded run…</option>
              {runs.map(r => <option key={r.run_id} value={r.run_id}>{r.run_id} — {r.name} — {r.created_at}</option>)}
            </select>
            {(pickedRun?.real_resources ?? []).map(rr => (
              <label key={rr.resource} className="flex flex-wrap items-center gap-2 text-[11px] text-slate-300">
                <span className="font-mono">{rr.resource}</span>
                {rr.alternative_for && <span className="text-[10px] text-amber-300">stand-in for {rr.alternative_for} — not composed</span>}
                <span className="text-[10px] text-slate-500">recorded: {rr.outcome ?? 'not recorded'} · must be</span>
                <select value={want[rr.resource] ?? ''} aria-label={`Required outcome of ${rr.resource}`}
                  onChange={e => { const v = e.target.value; setWant(w => ({ ...w, [rr.resource]: v })); }}
                  className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-white">
                  <option value="">no criterion</option>
                  {OUTCOMES.map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              </label>
            ))}
            <label className="flex items-center gap-2 text-[11px] text-slate-300">
              <input type="checkbox" checked={wantGate} onChange={e => setWantGate(e.target.checked)} /> the quality gate passed
            </label>
            <textarea value={freeText} onChange={e => setFreeText(e.target.value)} rows={2} aria-label="Other criteria"
              placeholder="Other criteria, one per line. Nothing here can read a run against a sentence, so each is recorded as not assessed."
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-[12px] text-white" />
            <button type="button" disabled={vBusy || !runId} onClick={verify}
              className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-[11px] font-bold disabled:opacity-40">
              {vBusy ? 'Working…' : 'Check the run'}
            </button>
          </>
        )}
        {pickedRun && pickedRun.specification && (
          <div data-testid="cell-run-specification" className="space-y-1">
            <ProposedVsExecuted link={pickedRun.specification} />
            <button type="button" disabled={vBusy} onClick={verifyKept}
              className="px-3 py-1.5 rounded-lg border border-slate-700 text-slate-300 text-[11px] font-bold disabled:opacity-40">
              Check it against the criteria kept with its specification
            </button>
          </div>
        )}
        {vErr && <p role="alert" data-testid="cell-verify-error" className="text-[11px] text-rose-400">{vErr}</p>}
        {verdict && (
          <div data-testid="cell-verdict" className="space-y-1">
            <p className="text-[11px] text-slate-200">
              Run {verdict.run_id}: {verdict.counts.met ?? 0} met · {verdict.counts.unmet ?? 0} not met · {verdict.counts.not_assessed ?? 0} not assessed — {verdict.all_met ? 'every stated criterion was assessed and met' : 'NOT every stated criterion is met'}.
            </p>
            <p className="text-[10px] text-slate-500">{verdict.all_met_basis}</p>
            {verdict.criteria_source_basis && (
              <p data-testid="cell-criteria-source" className="text-[10px] text-slate-400">{verdict.criteria_source_basis}</p>
            )}
            <ul className="space-y-1">
              {verdict.criteria.map((row, i) => (
                <li key={i} className={`text-[11px] px-2 py-1 rounded-lg border ${VERDICT_STYLE[row.state] ?? VERDICT_STYLE.not_assessed}`}>
                  <span className="font-bold">{VERDICT_WORD[row.state] ?? row.state}</span> — {asText(row.criterion)}
                  <span className="block text-[10px] text-slate-500">Evidence: {row.evidence == null ? 'none' : asText(row.evidence)}. {row.basis}</span>
                </li>
              ))}
            </ul>
            {verdict.attempted && (
              <p data-testid="cell-attempted" className="text-[10px] text-slate-400">
                Attempted: {verdict.attempted.join(', ') || 'none'}. Not attempted: {verdict.not_attempted == null ? 'not known for this run' : (verdict.not_attempted.join(', ') || 'none')}. <span className="text-slate-500">{verdict.attempt_basis}</span>
              </p>
            )}
            {(verdict.stand_ins ?? []).map(s => (
              <p key={s.resource} data-testid="cell-stand-in" className="text-[10px] text-amber-300">{s.label}</p>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

// P3.31 - PROPOSED VERSUS EXECUTED for one run, exactly as the server computed it from the run's own rows.
// Declared after the panel on purpose (a function declaration is hoisted).
function ProposedVsExecuted({ link }: { link: SpecLink }) {
  const executed = link.executed ?? [];
  const extra = link.not_in_specification ?? [];
  return (
    <div data-testid="cell-proposed-vs-executed" className="space-y-1 p-2 rounded-lg border border-slate-800">
      <p className="text-[11px] text-slate-200">
        From specification {link.specification_id}{link.version != null ? `, version ${link.version}` : ''}. Proposed: {(link.proposed ?? []).join(', ') || 'none'}.
      </p>
      {link.refused && <p className="text-[11px] text-rose-300">The run was refused before anything ran.</p>}
      <p data-testid="cell-executed" className="text-[11px] text-emerald-300">
        Executed: {executed.map(x => `${x.resource} [${x.outcome ?? 'no outcome word recorded'}${x.stand_in?.tried ? `; stand-in tried: ${x.stand_in.tried}` : ''}${x.available_at_run === false ? '; read unavailable before the run' : ''}]`).join(', ') || 'none'}.
      </p>
      {(link.not_attempted ?? []).map(x => (
        <p key={x.resource} data-testid="cell-not-attempted" className="text-[11px] text-amber-300">
          Not attempted: {x.resource} ({x.why}). <span className="text-slate-500">{x.basis ?? ''}</span>
        </p>
      ))}
      {extra.length > 0 && (
        <p data-testid="cell-not-in-specification" className="text-[11px] text-amber-300">
          Executed and NOT in the specification: {extra.map(x => `${x.resource} [${x.outcome ?? 'no outcome word recorded'}${x.alternative_for ? `; stand-in for ${x.alternative_for}` : ''}]`).join(', ')}.
        </p>
      )}
      {(link.unavailable_at_run ?? []).map(x => (
        <p key={x.id} data-testid="cell-unavailable-at-run" className="text-[11px] text-rose-300">
          Unavailable when the run started: {x.id}. {x.because}
        </p>
      ))}
      {link.basis && <p className="text-[10px] text-slate-500">{link.basis}</p>}
    </div>
  );
}

export default InstrumentCellPanel;
