import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldAlert, AlertTriangle, BookOpen, HeartHandshake } from 'lucide-react';

// P2.12 — the three guardrails, each with what it did NOT look at, and the distress route field shown
// as UNFILLED.
//
// THE FIELD THAT DECIDES THIS PAGE. `distress_routes` is empty on this platform and must render as
// NOT SUPPLIED, visibly. A placeholder, a default or a plausible-looking number is the single most
// dangerous thing this page could contain — a person in distress might act on it, and that is the one
// mistake no later correction reaches. So there is no fallback string anywhere in this file: when the
// list is empty the page prints the backend's own basis, which says the field is unfilled and why.
//
// AND NO GATE IS SHOWN AS A CLEARANCE. Each is an English phrase screen, so a non-match means its own
// patterns found nothing — not that the subject was absent. Every gate card carries its limit, and the
// summary says in words that the screens certify nothing, because a page listing three green gates would
// tell a reader the opposite of what the gates can support.

interface Gate {
  gate: string;
  refuses: string;
  limit: string;
  certifies_absence: boolean;
}

// W554 (P2.11) — AND THE SEAM, WHICH OBSERVES AND DOES NOT GATE. This page is called Guardrails and is
// full of gates, so a reader arriving here would reasonably take the whole of Horizon for something that
// stops requests. The seam does not: it watches the domain routes and the run outcomes, records what it
// saw, and nothing downstream reads it. That has to be said HERE, on the page that creates the
// impression, and in the backend's own words — a stored ESCALATE nobody acted on is the most misleading
// row in that store, and a page implying otherwise is how a reader comes to trust it.
interface Seam {
  gates: boolean;
  gating_basis: string;
  decision_is_constant: string;
  domain_prefixes: string[];
  observed_methods: string[];
  observed_kinds: string[];
  not_observed_kinds: Record<string, string>;
  body_read: boolean;
  body_basis: string;
  observed_total: number;
  observed_not_served: number;
  observed_decisions: Record<string, number>;
  error_count: number;
  store_cap: number;
  basis: string;
}

interface Guardrails {
  gates: Gate[];
  distress_routes: Array<Record<string, string | number | boolean>> | null;
  distress_routes_supplied: boolean;
  distress_routes_basis: string;
  // THREE STATES, not two. A route last confirmed years ago is SUPPLIED, so a boolean alone renders it
  // as current — which is exactly what the required check date exists to prevent.
  distress_routes_state: 'NOT_SUPPLIED' | 'SUPPLIED_STALE' | 'SUPPLIED_FRESH';
  distress_routes_stale_count: number;
  distress_routes_jurisdictions: string[];
  distress_routes_cover_anywhere: boolean;
  distress_routes_refused: string[];
  not_a_person_statement: string;
  escalation_defaults_on_when_undecidable: boolean;
  basis: string;
  unchanged_refusals: string[];
}

const ICONS: Record<string, React.ReactNode> = {
  religious_ruling: <BookOpen className="w-5 h-5" />,
  theological_proof: <AlertTriangle className="w-5 h-5" />,
  clinical_care: <HeartHandshake className="w-5 h-5" />,
};

export const HorizonGuardrails: React.FC = () => {
  const [g, setG] = useState<Guardrails | null>(null);
  const [s, setS] = useState<Seam | null>(null);
  const [err, setErr] = useState('');
  const [seamErr, setSeamErr] = useState('');

  useEffect(() => {
    axios.get<Guardrails>('/api/v1/horizon/guardrails', { validateStatus: () => true })
      .then(r => {
        if (r.status === 200 && r.data) { setG(r.data); setErr(''); }
        else { setG(null); setErr(`The guardrails are not reporting (HTTP ${r.status}).`); }
      })
      .catch(() => { setG(null); setErr('The guardrails could not be reached.'); });
    // The seam is fetched SEPARATELY and fails separately: a seam that cannot be read must not blank the
    // guardrails, and — more to the point — must not leave the page silent about gating.
    axios.get<Seam>('/api/v1/horizon/seam', { validateStatus: () => true })
      .then(r => {
        if (r.status === 200 && r.data) { setS(r.data); setSeamErr(''); }
        else { setS(null); setSeamErr(`The seam is not reporting (HTTP ${r.status}).`); }
      })
      .catch(() => { setS(null); setSeamErr('The seam could not be reached.'); });
  }, []);

  return (
    <div className="space-y-10 pb-24">
      <header>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight uppercase italic flex items-center gap-3">
          <ShieldAlert className="w-9 h-9 text-amber-400" /> Horizon Guardrails
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-3xl leading-relaxed">
          Three gates attached to the constitutional interceptor. Each reports a verdict{' '}
          <span className="text-amber-400">and what it did not look at</span> — none of them can certify
          that a subject was absent, and none of them judges the person asking.
        </p>
      </header>

      {err && <div role="alert" className="text-vital font-bold">{err} Nothing is shown, because nothing was received.</div>}
      {!err && !g && <p className="text-slate-500 font-bold animate-pulse">Reading the guardrails…</p>}

      {g && (
        <>
          {/* THE DISTRESS ROUTE FIELD, FIRST AND UNMISSABLE. Empty renders as empty. */}
          <section
            role={g.distress_routes_state === 'SUPPLIED_FRESH' ? undefined : 'alert'}
            data-testid="horizon-distress-routes"
            data-route-state={g.distress_routes_state}
            className={`rounded-2xl p-6 border-2 ${g.distress_routes_state === 'SUPPLIED_FRESH'
              ? 'border-emerald-500/40 bg-emerald-500/5'
              : 'border-amber-500/60 bg-amber-500/10'}`}
          >
            <h2 className="text-sm font-black uppercase tracking-widest text-amber-400 mb-3">
              Human distress route
            </h2>
            {g.distress_routes_state === 'SUPPLIED_STALE' && (
              /* A STALE ROUTE IS SHOWN, AND SHOWN AS STALE. Withholding it would leave a person with
                 nothing; showing it as current would tell them someone had checked. Both are wrong, so
                 it is shown with the fact. */
              <p
                data-testid="horizon-routes-stale"
                className="text-xl font-black text-amber-400 uppercase tracking-wide mb-3"
              >
                Last checked too long ago — {g.distress_routes_stale_count} of{' '}
                {g.distress_routes?.length ?? 0} route(s) may have changed since anyone confirmed them
              </p>
            )}
            {g.distress_routes && g.distress_routes.length > 0 ? (
              <ul className="space-y-2">
                {g.distress_routes.map((r, i) => (
                  <li
                    key={i}
                    data-testid={r.stale ? 'horizon-route-stale-row' : 'horizon-route-row'}
                    className={r.stale ? 'text-amber-300 font-bold' : 'text-slate-200 font-bold'}
                  >
                    {Object.entries(r).map(([k, v]) => `${k}: ${v}`).join(' · ')}
                  </li>
                ))}
              </ul>
            ) : (
              <>
                <p className="text-3xl font-black text-amber-400 uppercase tracking-wide mb-3">
                  Not supplied
                </p>
                {/* The backend's own sentence. There is deliberately no fallback text here: a second
                    wording of this field is a second place a placeholder could appear. */}
                <p className="text-slate-300 font-bold leading-relaxed">{g.distress_routes_basis}</p>
              </>
            )}
            {g.distress_routes && g.distress_routes.length > 0 && (
              /* WHERE IT ANSWERS. A route for one named place shown to someone outside it sends them
                 somewhere instead of telling them the truth, so the coverage is on the surface. */
              <p data-testid="horizon-routes-coverage" className="text-slate-400 text-xs font-bold mt-3">
                {g.distress_routes_cover_anywhere
                  ? 'Reviewed as correct wherever the person is: it names no specific service.'
                  : `Reviewed for ${g.distress_routes_jurisdictions.join(', ')} only — a person outside` +
                    ' that is not covered by this route.'}
                {' '}{g.distress_routes_basis}
              </p>
            )}
          </section>

          <section className="rounded-2xl p-6 border border-slate-800 bg-slate-900/40">
            <h2 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-3">
              What is said when a distress signal is detected
            </h2>
            <p className="text-slate-200 font-bold leading-relaxed italic">“{g.not_a_person_statement}”</p>
            <p className="text-slate-500 text-xs font-bold mt-3">
              AI counsel is withheld. This is a statement about what the platform is, not advice about
              what anyone should do.
            </p>
          </section>

          <section className="grid gap-4 @[900px]:grid-cols-3">
            {g.gates.map(gate => (
              <div key={gate.gate} className="rounded-2xl p-5 border border-slate-800 bg-slate-900/40">
                <div className="flex items-center gap-2 text-amber-400 mb-2">
                  {ICONS[gate.gate]}
                  <h3 className="text-xs font-black uppercase tracking-widest">
                    {gate.gate.replace(/_/g, ' ')}
                  </h3>
                </div>
                <p className="text-slate-300 text-sm font-bold leading-relaxed">Refuses: {gate.refuses}</p>
                {/* THE LIMIT, ON EVERY CARD. A verdict without its coverage is what this item exists to
                    prevent: a screen that reads as a clearance because nothing matched. */}
                <p className="text-slate-500 text-[11px] font-bold leading-relaxed mt-3 border-t border-slate-800 pt-3">
                  Did not look at: {gate.limit}
                </p>
                <p className="text-amber-400/80 text-[11px] font-black uppercase tracking-wider mt-2">
                  {gate.certifies_absence ? 'certifies absence' : 'certifies no absence'}
                </p>
              </div>
            ))}
          </section>


          <section className="rounded-2xl p-6 border border-slate-800 bg-slate-900/40 space-y-3">
            <p className="text-slate-400 font-bold leading-relaxed">{g.basis}</p>
            <h2 className="text-xs font-black uppercase tracking-widest text-slate-400 pt-3 border-t border-slate-800">
              Unchanged and unrelaxed
            </h2>
            <ul className="space-y-1">
              {g.unchanged_refusals.map((r, i) => (
                <li key={i} className="text-slate-400 text-sm font-bold">· {r}</li>
              ))}
            </ul>
          </section>
        </>
      )}

      {/* THE SEAM, OUTSIDE the guardrails block. It was inside it, and loading the page while the
          backend was still booting showed what that cost: /guardrails answered 500, the page correctly
          said nothing was received, and the denial of gating disappeared with it — leaving the title and
          three gate cards as the page's only statement about Horizon, which is the impression this block
          exists to correct. Its own comment claimed it rendered "whether or not the seam reports", which
          was true of the SEAM's failure and false of the guardrails'. A section that only appears when a
          DIFFERENT request succeeds is not an unconditional statement. */}
      <section
        data-testid="horizon-seam"
        className="rounded-2xl p-6 border-2 border-sky-500/40 bg-sky-500/5 space-y-3"
      >
        <h2 className="text-sm font-black uppercase tracking-widest text-sky-400">
          The seam in front of the domain routes
        </h2>
        {seamErr && (
          <p role="alert" className="text-vital font-bold">
            {seamErr} Nothing about the seam is shown, because nothing was received — not that it
            observed nothing.
          </p>
        )}
        {s && (
          <>
            <p className="text-3xl font-black text-sky-400 uppercase tracking-wide">
              {s.gates ? 'Gates requests' : 'Observes · does not gate'}
            </p>
            {/* The backend's own sentences, both of them. No second wording of a claim this
                load-bearing. */}
            <p className="text-slate-300 font-bold leading-relaxed">{s.gating_basis}</p>
            <p className="text-slate-400 text-sm font-bold leading-relaxed border-t border-sky-500/20 pt-3">
              {s.decision_is_constant}
            </p>
            <p className="text-slate-400 text-sm font-bold leading-relaxed">{s.body_basis}</p>
            <dl className="grid gap-3 @[640px]:grid-cols-3 pt-3 border-t border-sky-500/20">
              <div>
                <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">
                  Observed this process
                </dt>
                <dd className="text-xl font-black text-slate-200">{s.observed_total}</dd>
              </div>
              <div>
                <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">
                  Of those, not served
                </dt>
                <dd className="text-xl font-black text-slate-200">{s.observed_not_served}</dd>
              </div>
              <div>
                <dt className="text-[11px] font-black uppercase tracking-widest text-slate-500">
                  Observations that failed
                </dt>
                <dd className="text-xl font-black text-slate-200">{s.error_count}</dd>
              </div>
            </dl>
            <p className="text-slate-500 text-xs font-bold leading-relaxed">{s.basis}</p>
            <h3 className="text-[11px] font-black uppercase tracking-widest text-slate-500 pt-3 border-t border-sky-500/20">
              Deliberately not observed
            </h3>
            <ul className="space-y-1">
              {Object.entries(s.not_observed_kinds).map(([k, why]) => (
                <li key={k} className="text-slate-400 text-sm font-bold leading-relaxed">
                  · <span className="text-slate-300">{k}</span> — {why}
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </div>
  );
};

export default HorizonGuardrails;
