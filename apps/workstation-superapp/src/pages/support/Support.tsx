import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LifeBuoy, CheckCircle2, XCircle, AlertTriangle, FileText } from 'lucide-react';
import { provenanceBadge } from '../../lib/api';

// P3.18 — the support surface, told truthfully.
//
// THE PAGE EXISTS BECAUSE THE ARCHIVED VERSION OF THIS COMPONENT WOULD HAVE LOOKED PERFECT HERE. Its
// agent slept a tier-shaped latency and returned a formatted string announcing a resolution of whatever
// was asked, with success set unconditionally; its SLA monitor then divided a real sum by a real length
// over tickets it had invented and printed 100%. Nothing about that reads as a fabrication on screen — a
// fast answer, a green tick and a perfect rate. So this page is built so the honest states are the ones
// that are easy to render and the dishonest ones have nowhere to go:
//
//   * THE RATE CARD HAS NO PERCENTAGE PATH AT ALL. When the backend reports rate === null the card prints
//     the backend's own basis sentence. It never computes a percentage from the counts itself, and it
//     never falls back to 0 — a zero would read as "we resolve nothing" and a one as the archived
//     monitor's figure. The number shown, when there is one, is the one the backend computed.
//   * RESOLVED IS NEVER DRAWN FROM "ANSWERED". The answer card shows the answer; the resolution is a
//     separate state that only the confirm buttons below can write, and until one is pressed the card
//     says so in words.
//   * A FAILED CALL IS DRAWN AS A FAILURE, never as an empty answer. The two are indistinguishable if you
//     render `answer ?? ''`, and only one of them is the platform's fault.
//   * PROVENANCE TRAVELS WITH THE ANSWER through the one shared helper, so the deterministic floor cannot
//     wear an in-house badge here when eight other renderers were already corrected for exactly that.

interface Provenance {
  served_by: string | null;
  is_external: boolean;
  failed: boolean;
  latency_ms: number;
  provenance_basis: string;
}

interface AskResponse {
  ticket_id: string;
  answer: string | null;
  answered: boolean;
  provenance: Provenance;
  resolved: boolean | null;
  resolved_basis: string;
  next_step: string;
  escalated: boolean;
  ledger: { recorded: boolean; ledger_entry: string | null; basis: string };
}

interface Sla {
  rate: number | null;
  confirmed_resolved: number | null;
  confirmed_unresolved: number | null;
  unconfirmed: number | null;
  answered: number | null;
  tickets: number | null;
  unreadable: string | null;
  basis: string;
  method: string;
}

export const Support: React.FC = () => {
  const [query, setQuery] = useState('');
  const [asking, setAsking] = useState(false);
  const [ans, setAns] = useState<AskResponse | null>(null);
  const [err, setErr] = useState('');
  const [sla, setSla] = useState<Sla | null>(null);
  const [slaErr, setSlaErr] = useState('');
  const [confirmed, setConfirmed] = useState<boolean | null>(null);

  const loadSla = () => {
    axios.get<Sla>('/api/v1/support/sla', { validateStatus: () => true })
      .then(r => {
        if (r.status === 200 && r.data) { setSla(r.data); setSlaErr(''); }
        else { setSla(null); setSlaErr(`The support record is not reporting (HTTP ${r.status}).`); }
      })
      .catch(() => { setSla(null); setSlaErr('The support record could not be reached.'); });
  };
  useEffect(() => { loadSla(); }, []);

  const ask = () => {
    if (!query.trim()) return;
    setAsking(true); setErr(''); setAns(null); setConfirmed(null);
    axios.post<AskResponse>('/api/v1/support/ask', { query }, { validateStatus: () => true })
      .then(r => {
        if (r.status === 200 && r.data) setAns(r.data);
        else setErr(`The support surface did not answer (HTTP ${r.status}). Nothing was recorded as an answer.`);
      })
      .catch(() => setErr('The support surface could not be reached. Nothing was recorded as an answer.'))
      .finally(() => { setAsking(false); loadSla(); });
  };

  const confirm = (resolved: boolean) => {
    if (!ans) return;
    axios.post('/api/v1/support/confirm',
      { ticket_id: ans.ticket_id, resolved, by: '' }, { validateStatus: () => true })
      .then(r => { if (r.status === 200) setConfirmed(resolved); })
      .finally(() => loadSla());
  };

  const badge = ans ? provenanceBadge(ans.provenance.served_by, ans.provenance.is_external) : null;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-5xl font-black tracking-tighter uppercase flex items-center gap-3">
          <LifeBuoy className="w-10 h-10 text-aura" /> Support
        </h1>
        <p className="text-slate-500 font-bold max-w-2xl leading-relaxed mt-2">
          Ask a technical question about this platform. Every answer says what served it and how long that
          took; whether it resolved anything is yours to say, not ours.
        </p>
      </header>

      <section className="space-y-3">
        <textarea
          value={query}
          onChange={e => setQuery(e.target.value)}
          rows={3}
          placeholder="What is going wrong?"
          className="w-full bg-slate-900/60 border border-slate-700 rounded-xl p-4 text-slate-200 font-medium"
        />
        <button
          type="button" onClick={ask} disabled={asking || !query.trim()}
          className="px-6 py-3 rounded-xl bg-aura/20 text-aura font-black uppercase tracking-widest disabled:opacity-40"
        >
          {asking ? 'Asking…' : 'Ask'}
        </button>
        {err && <div role="alert" className="text-vital font-bold">{err}</div>}
      </section>

      {ans && (
        <section className="space-y-4 border border-slate-800 rounded-2xl p-6 bg-slate-900/40">
          {/* A failed call is a failure on screen. Rendering `answer ?? ''` would make it an empty answer. */}
          {ans.answered && ans.answer ? (
            <p className="text-slate-200 whitespace-pre-wrap leading-relaxed">{ans.answer}</p>
          ) : (
            <div role="alert" className="flex items-start gap-2 text-amber-400 font-bold">
              <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
              <span>No answer was produced for this ticket. {ans.provenance.provenance_basis}</span>
            </div>
          )}

          {badge && (
            <div className="flex items-center gap-3 flex-wrap">
              <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${badge.cls}`}
                    title={badge.title}>{badge.label}</span>
              <span className="text-slate-500 text-xs font-bold">{ans.provenance.latency_ms} ms measured</span>
              {/* The backend's own sentence, not a second wording of it. Both branches of the append carry
                  a basis for exactly this reason: a page that paraphrases "appended" and "not appended"
                  itself is a second place the truth can drift, and the drift always favours the happy one.
                  It also matters here because the attestation is an UNSIGNED digest when no key is
                  configured, and only the backend knows which of those two it just produced. */}
              <span className="text-slate-600 text-xs font-bold">{ans.ledger.basis}</span>
            </div>
          )}

          {/* RESOLVED IS ITS OWN STATE. Nothing above writes it. */}
          <div className="border-t border-slate-800 pt-4 space-y-3">
            <p className="text-slate-400 text-sm font-bold">{ans.next_step}</p>
            {confirmed === null ? (
              <>
                <p className="text-slate-500 text-xs font-bold italic">{ans.resolved_basis}</p>
                <div className="flex gap-3">
                  <button type="button" onClick={() => confirm(true)}
                          className="px-4 py-2 rounded-lg bg-emerald-500/15 text-emerald-400 font-black text-sm uppercase flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" /> This resolved it
                  </button>
                  <button type="button" onClick={() => confirm(false)}
                          className="px-4 py-2 rounded-lg bg-rose-500/15 text-rose-400 font-black text-sm uppercase flex items-center gap-2">
                    <XCircle className="w-4 h-4" /> It did not
                  </button>
                </div>
              </>
            ) : (
              <p className={`font-black text-sm uppercase ${confirmed ? 'text-emerald-400' : 'text-rose-400'}`}>
                {confirmed ? 'Recorded as resolved — thank you.' : 'Recorded as unresolved. It stays open.'}
              </p>
            )}
          </div>
        </section>
      )}

      <section className="border border-slate-800 rounded-2xl p-6 bg-slate-900/40 space-y-3">
        <h2 className="text-xl font-black uppercase tracking-wider flex items-center gap-2 text-slate-300">
          <FileText className="w-5 h-5" /> Resolution record
        </h2>
        {slaErr && <div role="alert" className="text-vital font-bold">{slaErr} No figure is shown.</div>}
        {!slaErr && !sla && <p className="text-slate-500 font-bold animate-pulse">Reading the record…</p>}
        {sla && (
          <>
            {sla.unreadable ? (
              <div role="alert" className="text-vital font-bold">{sla.basis}</div>
            ) : sla.rate === null ? (
              /* NO NUMBER HERE, BY DESIGN — not a zero, not a one. The backend's own sentence. */
              <p className="text-amber-400 font-bold leading-relaxed">{sla.basis}</p>
            ) : (
              <>
                <p className="text-5xl font-black text-emerald-400 tabular-nums">
                  {sla.confirmed_resolved} <span className="text-slate-600 text-2xl">of</span>{' '}
                  {(sla.confirmed_resolved ?? 0) + (sla.confirmed_unresolved ?? 0)}
                </p>
                <p className="text-slate-400 font-bold text-sm leading-relaxed">{sla.basis}</p>
              </>
            )}
            <p className="text-slate-600 text-xs font-bold leading-relaxed border-t border-slate-800 pt-3">
              {sla.method}
            </p>
          </>
        )}
      </section>
    </div>
  );
};

export default Support;
