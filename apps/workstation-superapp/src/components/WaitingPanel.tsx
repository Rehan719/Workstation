//  W1086 (P5.18 clause 3, FU-1267); W1087 (P5.14 clause 4, FU-1269) - THE ONE LIST OF WHAT WAITS ON YOU, on the
//  first screen and on the Law page. Everything here is the route's own (agentic_core/api/waiting.py): what falls due,
//  or lapses, within the window or past its date, soonest first; each decision a project or Change Control waits on,
//  oldest first; and what waits for a confirmation or a fresh declaration. Each says the record it is on and where it
//  is acted on. A store the route could not read is said in its place, with why, and never as nothing waiting there;
//  with sign-in off, the route's sentence that agreement and asset records are kept only after sign-in is said. The
//  list says what it reads and what it does not read yet, so an empty list says only that nothing it reads is
//  waiting. A read that fails is said with its reason, never as nothing waiting.
import React, { useCallback, useEffect, useState } from 'react';
import { apiJson, asClause, errorMessage } from '../lib/api';

const keyOf = (i: any) =>
  `${i.source}-${i.kind}-${i.obligation_id ?? i.proposal_id ?? i.evidence_id ?? i.cca_id ?? i.on}`;

export default function WaitingPanel() {
  const [w, setW] = useState<any | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const read = useCallback(async () => {
    setErr(''); setBusy(true);
    try {
      setW(await apiJson('/api/v1/waiting'));
    } catch (e) {
      setW(null);
      setErr(`What waits on you could not be read (${errorMessage(e)}), so nothing is said about it here.`);
    } finally { setBusy(false); }
  }, []);
  useEffect(() => { read(); }, [read]);

  const items: any[] = w?.items ?? [];
  return (
    <div className="space-y-3" data-testid="waiting-panel">
      <h3 className="text-lg font-black text-white uppercase tracking-tight">What waits on you</h3>
      {w === null && !err && <p className="text-[11px] text-slate-500">Reading what waits on you…</p>}
      {err && <p data-testid="waiting-unread" className="text-[11px] text-rose-300">{err}</p>}
      {w && w.not_kept && <p data-testid="waiting-not-kept" className="text-[11px] text-amber-300">{w.not_kept}</p>}
      {w && (w.unread ?? []).map((u: any) => (
        <p key={u.store} data-testid="waiting-store-unread" className="text-[11px] text-rose-300">{u.said}</p>
      ))}
      {w && (items.length === 0 ? (
        <p data-testid="waiting-none" className="text-[11px] text-slate-500">{w.said}</p>
      ) : (
        <ul className="space-y-1">
          {items.map((i: any) => (
            <li key={keyOf(i)} data-testid="waiting-item" className="text-[11px] text-slate-300">
              {`${i.what} (${i.ref ? `${i.ref}, ` : ''}on ${i.on}): ${asClause(String(i.said ?? ''))}${i.kind === 'falls_due' && !i.confirmed ? '; not confirmed by a person yet' : ''}. It is acted on in ${i.where}.`}
            </li>
          ))}
        </ul>
      ))}
      {w && (
        <p data-testid="waiting-reads" className="text-[10px] text-slate-500">
          {`This list reads ${(w.reads ?? []).join('; ')}.${(w.not_read_yet ?? []).length ? ` It does not read yet: ${(w.not_read_yet ?? []).join('; ')}.` : ''} ${w.date_basis ?? ''}`}
        </p>
      )}
      <button type="button" disabled={busy} onClick={read}
        className="px-3 py-1.5 rounded-lg bg-slate-800 text-[10px] font-black uppercase tracking-widest text-aura disabled:opacity-40">
        Read it again
      </button>
    </div>
  );
}
