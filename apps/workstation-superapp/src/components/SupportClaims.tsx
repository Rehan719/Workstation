// W942 (P5.3 part 2) — CLAIMS THAT AN OUTPUT IS WRONG, on the support page. A person raises a claim against one of
// their deliverables and reads every claim back: OPEN until a person decides the change it was filed as, then
// ANSWERED with that decision and whether the decision reached the ledger (GET/POST /api/v1/support/claims, W941).
// Every sentence about a claim's state, its owner and the rules is the server's; this component types none of them.
// A refusal is shown in the server's own words; a failed read is said, and never drawn as "no claims".
// W964 (FU-1190): a claim may name an answer that was never saved - the tool that gave it, what served it as the answer
// said, and the fingerprint of its text (the text itself is never sent) - and the server's sentence on what it holds.
import React, { useCallback, useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

interface Claim {
  claim_id: string;
  artefact_kind: string;
  artefact_id: string;
  what_is_wrong: string;
  raised_by: string;
  raised_at: string;
  state: string;
  state_basis: string;
  decision?: string;
  answer_logged?: boolean;
  answer_logged_basis?: string;
  named_owner: { owner: string | null; basis: string };
  artefact: { title?: string; version?: number; tool?: string; served_by_as_reported?: string | null; basis?: string };
}
interface Claims { claims: Claim[]; open: number; basis: string }
interface Deliverable { id: string; title: string }

//  what a claim names: a deliverable by its title and version, or an answer by its tool, what served it as the answer
//  said, and the start of its fingerprint
const named = (c: Claim): string => c.artefact_kind === 'answer'
  ? `an answer from ${c.artefact.tool}${c.artefact.served_by_as_reported ? `, served by ${c.artefact.served_by_as_reported}` : ''} (sha256 ${c.artefact_id.slice(0, 12)})`
  : `${c.artefact.title} (version ${c.artefact.version})`;

export const SupportClaims: React.FC = () => {
  const [answer, setAnswer] = useState<Claims | null>(null);
  const [works, setWorks] = useState<Deliverable[]>([]);
  const [readError, setReadError] = useState('');
  const [artefact, setArtefact] = useState('');
  const [wrong, setWrong] = useState('');
  const [refused, setRefused] = useState('');
  const [done, setDone] = useState('');
  const [busy, setBusy] = useState(false);

  //  the claims and the deliverables a claim can name are read together; either failing is said
  const read = useCallback(() => Promise.all([
    apiJson<Claims>('/api/v1/support/claims'),
    apiJson<{ deliverables: Deliverable[] }>('/api/v1/deliverables'),
  ]), []);

  useEffect(() => {
    let live = true;
    read()
      .then(([c, d]) => { if (live) { setAnswer(c); setWorks(d.deliverables); } })
      .catch(e => { if (live) setReadError(errorMessage(e)); });
    return () => { live = false; };
  }, [read]);

  const raise = async () => {
    setBusy(true);
    setRefused('');
    setDone('');
    try {
      const c = await apiJson<Claim>('/api/v1/support/claims', {
        method: 'POST', body: { artefact_kind: 'deliverable', artefact_id: artefact, what_is_wrong: wrong } });
      setDone(`Raised: ${c.claim_id} — ${c.state}.`);
      setWrong('');
      try {
        const [cl, d] = await read();
        setAnswer(cl);
        setWorks(d.deliverables);
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
  return (
    <section data-testid="support-claims" className="space-y-3">
      <h2 className="text-[10px] font-black uppercase tracking-widest text-highlight">Claims that an output is wrong</h2>
      {readError ? (
        <p data-testid="claims-unread" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">
          Could not read the claims — {readError}
        </p>
      ) : !answer ? (
        <p className="text-[10px] text-slate-600">Reading the claims…</p>
      ) : (
        <>
          <p data-testid="claims-basis" className="text-[10px] text-slate-500 leading-relaxed">{answer.basis}</p>
          <p data-testid="claims-open" className="text-[10px] font-black uppercase tracking-widest text-slate-300">
            {answer.open} open of {answer.claims.length}
          </p>
          {answer.claims.length === 0 && (
            <p data-testid="claims-none" className="text-[10px] text-slate-600">No claim has been raised.</p>
          )}
          {answer.claims.map(c => (
            <div key={c.claim_id} data-testid={`claim-${c.claim_id}`} className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <p className="text-sm font-black text-white">{c.state} — {named(c)}</p>
              {c.artefact_kind === 'answer' && c.artefact.basis && (
                <p data-testid={`claim-answer-${c.claim_id}`} className="text-[10px] text-slate-500">{c.artefact.basis}</p>
              )}
              <p className="text-[10px] text-slate-400">What is wrong: {c.what_is_wrong}</p>
              <p className="text-[10px] text-slate-400">{c.state_basis}.</p>
              <p className="text-[10px] text-slate-500">Answered by: {c.named_owner.owner ?? 'an administrator'} — {c.named_owner.basis}.</p>
              {c.answer_logged_basis && (
                <p data-testid={`claim-logged-${c.claim_id}`} className="text-[10px] text-slate-500">{c.answer_logged_basis}.</p>
              )}
              <p className="text-[9px] text-slate-600">Raised by {c.raised_by} at {c.raised_at}</p>
            </div>
          ))}
          {works.length === 0 ? (
            <p data-testid="claims-no-deliverable" className="text-[10px] text-slate-600">
              You have no deliverable to raise a claim against.
            </p>
          ) : (
            <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-2">
              <select value={artefact} aria-label="Deliverable the claim is about" onChange={e => setArtefact(e.target.value)} className={field}>
                <option value="">Deliverable</option>
                {works.map(w => <option key={w.id} value={w.id}>{w.title}</option>)}
              </select>
              <input value={wrong} aria-label="What is wrong" placeholder="What is wrong with it"
                onChange={e => setWrong(e.target.value)} className={field} />
              <button type="button" disabled={busy || !artefact} onClick={raise}
                className="text-[10px] font-black uppercase text-sovereign bg-highlight px-3 py-1.5 rounded-lg">Raise a claim</button>
            </div>
          )}
          {refused && <p data-testid="claims-refused" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">{refused}</p>}
          {done && <p data-testid="claims-done" className="text-[11px] text-slate-300">{done}</p>}
        </>
      )}
    </section>
  );
};
