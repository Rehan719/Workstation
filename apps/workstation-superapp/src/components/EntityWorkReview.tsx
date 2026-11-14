// W935 (P5.15 clauses 5 and 6; row FU-1178, its last part) — THE REVIEW THIS ENTITY'S WORK HAS REACHED, on its page.
// Each of the entity's deliverables is shown with the tier its current text has reached, in the server's words
// (GET /api/v1/entity-specialists/{id}/signatures, W934): signed by a qualified person — a specialist on the entity's
// own roster, the credential as stated — or unreviewed. Every signature is listed with whether it counts and, when it
// does not, the server's reason. A specialist holding a place signs one deliverable here. A refusal is shown in the
// server's own words; a failed read is said, and never drawn as "nothing is signed". This component types none of
// the sentences about the rules.
import React, { useCallback, useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

interface Review { tier: string; label: string; basis: string; title: string; version: number }
interface Signature {
  signature_id: string;
  name: string;
  deliverable_title: string;
  version: number;
  reviewed: string;
  date: string;
  lapses_on: string;
  counts: boolean;
  why_not: string | null;
}
interface Signatures { signatures: Signature[]; deliverables: Record<string, Review>; basis: string; credential_basis: string }
interface Held { specialist_id: string; name: string; discipline: string }

const BLANK = { specialist_id: '', deliverable_id: '', reviewed: '', date: '', lapses_on: '' };

export const EntityWorkReview: React.FC<{ vsbId: string }> = ({ vsbId }) => {
  const [answer, setAnswer] = useState<Signatures | null>(null);
  const [held, setHeld] = useState<Held[]>([]);
  const [readError, setReadError] = useState('');
  const [form, setForm] = useState(BLANK);
  const [refused, setRefused] = useState('');
  const [done, setDone] = useState('');
  const [busy, setBusy] = useState(false);
  const base = `/api/v1/entity-specialists/${encodeURIComponent(vsbId)}`;

  //  the signatures and who holds a place are read together; either failing is said, and nothing is drawn
  const read = useCallback(() => Promise.all([
    apiJson<Signatures>(`${base}/signatures`),
    apiJson<{ active: Held[] }>(base),
  ]), [base]);

  useEffect(() => {
    let live = true;
    setAnswer(null);
    setHeld([]);
    setReadError('');
    setRefused('');
    setDone('');
    read()
      .then(([s, r]) => { if (live) { setAnswer(s); setHeld(r.active); } })
      .catch(e => { if (live) setReadError(errorMessage(e)); });
    return () => { live = false; };
  }, [read]);

  const sign = async () => {
    setBusy(true);
    setRefused('');
    setDone('');
    const { specialist_id, ...body } = form;
    try {
      const a = await apiJson<{ signature: Signature }>(`${base}/${encodeURIComponent(specialist_id)}/sign`,
        { method: 'POST', body });
      setDone(`Signed by ${a.signature.name}, for version ${a.signature.version}.`);
      setForm(BLANK);
      try {
        const [s, r] = await read();
        setAnswer(s);
        setHeld(r.active);
        setReadError('');
      } catch (e) {
        setAnswer(null);
        setReadError(errorMessage(e));
      }
    } catch (e) {
      setRefused(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const field = 'bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white';
  const works = answer ? Object.entries(answer.deliverables) : [];
  return (
    <div data-testid="entity-work-review" className="space-y-3">
      <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight">The review this entity's work has reached</h4>
      {readError ? (
        <p data-testid="work-review-unread" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">
          Could not read the review of this entity's work — {readError}
        </p>
      ) : !answer ? (
        <p className="text-[10px] text-slate-600">Reading the review of this entity's work…</p>
      ) : (
        <>
          <p data-testid="work-review-basis" className="text-[10px] text-slate-500 leading-relaxed">{answer.basis}</p>
          <p data-testid="work-review-credential" className="text-[10px] text-slate-500 leading-relaxed">Credentials: {answer.credential_basis}.</p>
          {works.length === 0 && (
            <p data-testid="work-review-none" className="text-[10px] text-slate-600">This entity has no deliverable to review yet.</p>
          )}
          {works.map(([id, r]) => (
            <div key={id} data-testid={`work-review-${id}`} className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <p className="text-sm font-black text-white">{r.title} — version {r.version}</p>
              <p className="text-[10px] text-slate-400 leading-relaxed">
                <span className="font-black uppercase tracking-widest text-[9px] text-slate-300">Review reached: {r.label}</span>
                {' — '}{r.basis}.
              </p>
            </div>
          ))}
          {answer.signatures.map(s => (
            <p key={s.signature_id} data-testid={`signature-${s.signature_id}`} className="text-[10px] text-slate-500 leading-relaxed">
              {s.name} signed {s.deliverable_title} (version {s.version}) on {s.date}, until {s.lapses_on}: {s.reviewed}.
              {s.counts ? ' It counts.' : ` It does not count: ${s.why_not}.`}
            </p>
          ))}
          {held.length === 0 ? (
            <p data-testid="work-review-no-specialist" className="text-[10px] text-slate-600">
              No specialist holds a place on this entity's roster, so nothing can be signed here.
            </p>
          ) : works.length > 0 && (
            <>
              <div className="grid grid-cols-1 @[560px]:grid-cols-5 gap-2">
                <select value={form.specialist_id} aria-label="Specialist who signs"
                  onChange={e => setForm(f => ({ ...f, specialist_id: e.target.value }))} className={field}>
                  <option value="">Specialist</option>
                  {held.map(h => <option key={h.specialist_id} value={h.specialist_id}>{h.name} — {h.discipline}</option>)}
                </select>
                <select value={form.deliverable_id} aria-label="Deliverable signed"
                  onChange={e => setForm(f => ({ ...f, deliverable_id: e.target.value }))} className={field}>
                  <option value="">Deliverable</option>
                  {works.map(([id, r]) => <option key={id} value={id}>{r.title}</option>)}
                </select>
                <input value={form.reviewed} aria-label="What in it they reviewed" placeholder="What in it they reviewed"
                  onChange={e => setForm(f => ({ ...f, reviewed: e.target.value }))} className={field} />
                <input type="date" value={form.date} aria-label="Date reviewed"
                  onChange={e => setForm(f => ({ ...f, date: e.target.value }))} className={field} />
                <input type="date" value={form.lapses_on} aria-label="Signature lapses on"
                  onChange={e => setForm(f => ({ ...f, lapses_on: e.target.value }))} className={field} />
              </div>
              <button type="button" disabled={busy || !form.specialist_id} onClick={sign}
                className="text-[10px] font-black uppercase text-sovereign bg-highlight px-3 py-1.5 rounded-lg">Record the signature</button>
            </>
          )}
          {refused && <p data-testid="work-review-refused" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">{refused}</p>}
          {done && <p data-testid="work-review-done" className="text-[11px] text-slate-300">{done}</p>}
        </>
      )}
    </div>
  );
};
