import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Eye, HelpCircle } from 'lucide-react';

// P2.16 — THE COMPANION SURFACE: the record as the user sees it.
//
// THE RULE THIS PAGE IS BUILT ON. Nothing here may claim an alignment the kernel did not evaluate. Every
// field below is three-state, and the middle state is the one that matters: a term the kernel could not
// evaluate renders as NOT EVALUATED, never as a pass, and a PROCEED reached over unevaluated terms says
// so on its face. A page that drew a green tick for "no escalations" when nothing had compressed the
// request would be asserting exactly the thing this item exists to prevent.
//
// THE THREE STATES OF A LIST FIELD, which is the distinction the whole page turns on:
//   raised        the compression named escalations, and here they are
//   none raised   the compression ANSWERED, and the answer was none
//   not evaluated no compression ran, so there is no list — and its ABSENCE IS NOT AN ABSENCE OF
//                 ESCALATIONS. On this deployment, with no model provisioned, this is the ordinary state.
//
// CONSUMPTION IS NOT BUILT YET (P2.15), and the page says so rather than showing a zero. A zero that
// means "not measured" is the defect this programme keeps removing, and it would be worst here, on the
// surface a user reads to understand what their request cost.

interface Term {
  term: string;
  fired: boolean | null;
  basis: string;
}

interface IntentRecord {
  intent_id: string;
  asked: string | null;
  asked_basis: string;
  surface: string | null;
  source: string | null;
  compression: string;
  compression_basis: string;
  served_by: string | null;
  domain?: string;
  stakes?: string;
  escalations?: string[];
  missing?: string[];
  fields_present: string[];
  fields_absent: string[];
  fields_basis: string;
  decision: string | null;
  decision_terms: Term[] | null;
  decision_basis: string | null;
  reflection_tag: string | null;
  reflection_tag_by: string | null;
  reflection_tag_basis: string;
  gated?: boolean;
  gating_basis?: string;
}

interface Records {
  records: IntentRecord[];
  total: number;
  not_compressed: number;
  observed_not_enforced: number;
  history_cap: number;
  basis: string;
}

const NOT_EVALUATED = 'Not evaluated';

/** A list field's three states, rendered as three DIFFERENT things. */
const ListField: React.FC<{ label: string; items?: string[] }> = ({ label, items }) => {
  const answered = Array.isArray(items);
  const raised = answered && items!.length > 0;
  return (
    <div data-testid={`field-${label.toLowerCase().replace(/\s+/g, '-')}`}>
      <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">{label}</dt>
      {raised ? (
        <dd className="text-amber-400 font-bold">{items!.join(' · ')}</dd>
      ) : answered ? (
        <dd className="text-slate-300 font-bold">None raised — the compression answered</dd>
      ) : (
        // THE MIDDLE STATE, and the sentence is the point: an absent list is not an empty one.
        <dd className="text-slate-500 font-bold">
          {NOT_EVALUATED} — nothing compressed this request, so no list exists.{' '}
          <span className="text-amber-400/80">Its absence is not an absence of {label.toLowerCase()}.</span>
        </dd>
      )}
    </div>
  );
};

/** A compression field: present, or ABSENT with the reason. Never blank, never defaulted. */
const TextField: React.FC<{ label: string; value?: string }> = ({ label, value }) => (
  <div data-testid={`field-${label.toLowerCase().replace(/\s+/g, '-')}`}>
    <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">{label}</dt>
    {value ? (
      <dd className="text-slate-200 font-bold">{value}</dd>
    ) : (
      <dd className="text-slate-500 font-bold">{NOT_EVALUATED} — no compression produced this field</dd>
    )}
  </div>
);

interface Measured { value: unknown; measured: boolean; basis: string }
interface OwnerField { value: string | null; basis: string }
interface Consumption { computed: Record<string, Measured>; owner: Record<string, OwnerField> }

/** Reshape a ConsumptionRecord into the two groups the card renders, keyed by intent. */
const byIntent = (rows: Record<string, unknown>[]): Record<string, Consumption> => {
  const out: Record<string, Consumption> = {};
  for (const row of rows) {
    const id = row.intent_id as string | null;
    if (!id) continue;
    const computed: Record<string, Measured> = {};
    for (const f of (row.computed_fields as string[]) || []) {
      const m = row[f] as Measured | undefined;
      if (m) computed[f] = m;
    }
    const owner: Record<string, OwnerField> = {};
    for (const f of (row.owner_fields as string[]) || []) {
      owner[f] = { value: (row[f] as string | null) ?? null, basis: (row[`${f}_basis`] as string) || '' };
    }
    out[id] = { computed, owner };
  }
  return out;
};

export const HorizonCompanion: React.FC = () => {
  const [d, setD] = useState<Records | null>(null);
  const [consumption, setConsumption] = useState<Record<string, Consumption>>({});
  const [err, setErr] = useState('');

  useEffect(() => {
    axios.get<Records>('/api/v1/horizon/records?limit=25', { validateStatus: () => true })
      .then(r => {
        if (r.status === 200 && r.data) { setD(r.data); setErr(''); }
        else { setD(null); setErr(`The records are not reporting (HTTP ${r.status}).`); }
      })
      .catch(() => { setD(null); setErr('The records could not be reached.'); });
    // Fetched SEPARATELY and failing separately: a consumption store that cannot be read must leave
    // the card saying "not recorded", which is true, rather than blanking the record above it.
    axios.get<{ records: Record<string, unknown>[] }>('/api/v1/horizon/consumption?limit=100',
      { validateStatus: () => true })
      .then(r => { if (r.status === 200 && r.data?.records) setConsumption(byIntent(r.data.records)); })
      .catch(() => { /* leaves the card at "Not recorded", which is what is true */ });
  }, []);

  return (
    <div className="space-y-8 pb-24">
      <header>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight uppercase italic flex items-center gap-3">
          <Eye className="w-9 h-9 text-sky-400" /> Horizon Companion
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-3xl leading-relaxed">
          Each request as it was recorded — what was asked, what the platform understood, and{' '}
          <span className="text-sky-400">what it did not evaluate</span>. Nothing here claims an
          alignment the kernel did not reach.
        </p>
      </header>

      {err && (
        <div role="alert" className="text-vital font-bold">
          {err} Nothing is shown, because nothing was received — not that nothing was recorded.
        </div>
      )}
      {!err && !d && <p className="text-slate-500 font-bold animate-pulse">Reading the records…</p>}

      {d && d.records.length === 0 && (
        <p className="text-slate-400 font-bold">
          No request has been recorded yet. That is not the same as none having been made.
        </p>
      )}

      {d && d.records.map(r => (
        <article
          key={r.intent_id}
          data-testid="companion-record"
          className="rounded-2xl p-6 border border-slate-800 bg-slate-900/40 space-y-4"
        >
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="text-sm font-black uppercase tracking-widest text-sky-400">What was asked</h2>
            <span className="text-[11px] font-bold text-slate-600">{r.surface || r.source}</span>
          </div>
          <p className="text-slate-100 font-bold text-lg leading-snug">
            {r.asked || <span className="text-slate-500">Not recorded for this row</span>}
          </p>
          <p className="text-slate-600 text-[11px] font-bold leading-relaxed">{r.asked_basis}</p>

          {/* THE COMPRESSION, AND WHY IT IS THE ORDINARY ANSWER HERE. */}
          <div className="rounded-xl p-4 bg-slate-950/40 border border-slate-800 space-y-3">
            <p className="text-2xl font-black uppercase tracking-wide text-slate-300">
              {r.compression === 'COMPRESSED' ? `Compressed by ${r.served_by}` : 'Not compressed'}
            </p>
            <p className="text-slate-400 text-sm font-bold leading-relaxed">{r.compression_basis}</p>
            <dl className="grid gap-3 @[640px]:grid-cols-2 pt-2 border-t border-slate-800">
              <TextField label="Domain" value={r.domain} />
              <TextField label="Stakes" value={r.stakes} />
              <ListField label="Escalations" items={r.escalations} />
              <ListField label="Missing inputs" items={r.missing} />
            </dl>
            <p className="text-slate-600 text-[11px] font-bold leading-relaxed">{r.fields_basis}</p>
          </div>

          {/* THE DECISION, WITH EVERY TERM — including the ones nothing could evaluate. */}
          <div className="space-y-2">
            <h3 className="text-[11px] font-black uppercase tracking-widest text-slate-500">
              The decision, and every term behind it
            </h3>
            <p className="text-xl font-black uppercase tracking-wide text-amber-400">{r.decision}</p>
            <ul className="space-y-1">
              {(r.decision_terms || []).map(t => (
                <li key={t.term} className="text-sm font-bold leading-relaxed" data-testid="decision-term">
                  <span className={t.fired === true ? 'text-amber-400'
                    : t.fired === false ? 'text-slate-300' : 'text-slate-500'}>
                    {t.fired === true ? 'FIRED' : t.fired === false ? 'did not fire' : NOT_EVALUATED}
                  </span>
                  <span className="text-slate-400"> · {t.term}</span>
                  <span className="text-slate-600 block text-[11px]">{t.basis}</span>
                </li>
              ))}
            </ul>
            <p className="text-slate-500 text-xs font-bold leading-relaxed">{r.decision_basis}</p>
            {r.gated === false && (
              <p className="text-slate-500 text-[11px] font-bold leading-relaxed border-t border-slate-800 pt-2">
                {r.gating_basis}
              </p>
            )}
          </div>

          {/* WHAT THE RUN CONSUMED (P2.15). Every figure carries what measured it, or says nothing
              did — and an unmeasured field is never a zero. */}
          <div data-testid="companion-consumption"
               className="rounded-xl p-4 border border-amber-500/30 bg-amber-500/5 space-y-2">
            <h3 className="text-[11px] font-black uppercase tracking-widest text-amber-400/90 flex items-center gap-2">
              <HelpCircle className="w-3 h-3" /> What this run consumed
            </h3>
            {consumption[r.intent_id] ? (
              <>
                <dl className="grid gap-2 @[640px]:grid-cols-2">
                  {Object.entries(consumption[r.intent_id].computed).map(([f, m]) => (
                    <div key={f} data-testid="consumption-field">
                      <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">
                        {f.replace(/_/g, ' ')}
                      </dt>
                      {m.measured ? (
                        <dd className="text-slate-200 font-bold">{JSON.stringify(m.value)}</dd>
                      ) : (
                        // NOT A ZERO. An unmeasured field and a measured nought are different facts.
                        <dd className="text-slate-500 font-bold">Not measured</dd>
                      )}
                      <dd className="text-slate-600 text-[10px] font-bold leading-relaxed">{m.basis}</dd>
                    </div>
                  ))}
                </dl>
                {/* THE OWNER'S OWN FIELDS, unfilled, rendered as unfilled — the item's clause (2). */}
                <div className="pt-2 border-t border-amber-500/20 space-y-2">
                  {Object.entries(consumption[r.intent_id].owner).map(([f, o]) => (
                    <div key={f} data-testid="consumption-owner-field">
                      <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">
                        {f.replace(/_/g, ' ')}
                      </dt>
                      {o.value ? (
                        <dd className="text-slate-200 font-bold italic">“{o.value}”</dd>
                      ) : (
                        <dd className="text-amber-400 font-black uppercase tracking-wide">Not filled</dd>
                      )}
                      <dd className="text-slate-600 text-[10px] font-bold leading-relaxed">{o.basis}</dd>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <>
                <p className="text-slate-300 font-bold">Not recorded</p>
                <p className="text-slate-500 text-[11px] font-bold leading-relaxed">
                  No ConsumptionRecord was joined to this run, so nothing accounted for what it cost. A
                  zero here would be a figure nobody computed, which is worse than the gap.
                </p>
              </>
            )}
          </div>

          {/* THE OWNER'S OWN ENTRY. Absent renders as the item's own words. */}
          <div data-testid="companion-reflection">
            <h3 className="text-[11px] font-black uppercase tracking-widest text-slate-500">
              The Owner's own entry
            </h3>
            {r.reflection_tag ? (
              <>
                <p className="text-slate-200 font-bold italic">“{r.reflection_tag}”</p>
                <p className="text-slate-600 text-[11px] font-bold">set by {r.reflection_tag_by}</p>
              </>
            ) : (
              <p className="text-slate-400 font-bold">No station assigned</p>
            )}
            <p className="text-slate-600 text-[11px] font-bold leading-relaxed mt-1">
              {r.reflection_tag_basis}
            </p>
          </div>
        </article>
      ))}

      {d && (
        <p className="text-slate-500 text-xs font-bold leading-relaxed">{d.basis}</p>
      )}
    </div>
  );
};

export default HorizonCompanion;
