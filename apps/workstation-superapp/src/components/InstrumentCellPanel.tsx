import React, { useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

// W640 (plan item P3.31) — THE INSTRUMENT CELL, ON THE FABRIC'S OWN PAGE.
// Everything shown here is the server's statement, printed with its basis: which resources the fabric can
// actually run (and why not, when it cannot), and a PROPOSAL for an objective — the smallest available set
// covering requirements the person states. A proposal saves nothing and runs nothing, and the panel says so
// in the server's words. No status here is decided in the browser.

interface Avail {
  id: string; name: string; state: string; reason: string; endpoint_state: string; endpoint_basis: string; not_checked: string;
}
interface AvailReply {
  resources: Avail[]; counts: Record<string, number>; total: number; basis: string;
  declaration_defects: { id: string; endpoint_state: string; basis: string }[];
}
interface Selected {
  id: string; name: string; covers: string[];
  contract: { when_run: string; persists: string; persists_basis: string; equivalents: string[] };
  availability: { state: string };
}
interface Proposal {
  what_this_is: string; saved: boolean; ran: boolean; requirements_confirmed: boolean;
  suggested_requirements?: { capability: string; first_declared_by: string }[];
  suggestion_basis?: string;
  selection: null | {
    selected: Selected[]; uncovered: string[]; uncovered_basis: string; method: string;
    excluded: { id: string; would_cover: string[]; because: string }[];
  };
  alternatives?: Record<string, { id: string; availability: string }[]>;
  alternatives_basis?: string;
  limits: { max_stages: number; ceiling: number; ceiling_basis: string; attempts_per_resource: number; attempts_basis: string };
}

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

export function InstrumentCellPanel() {
  const [avail, setAvail] = useState<AvailReply | null>(null);
  const [err, setErr] = useState('');
  const [objective, setObjective] = useState('');
  const [reqs, setReqs] = useState('');
  const [busy, setBusy] = useState(false);
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    apiJson<AvailReply>('/api/v1/resources/cell/availability').then(setAvail).catch(e => setErr(errorMessage(e)));
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
        </div>
      )}
    </section>
  );
}

export default InstrumentCellPanel;
