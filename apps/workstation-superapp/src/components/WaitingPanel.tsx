//  W1086 (P5.18 clause 3, FU-1267) - THE ONE LIST OF WHAT WAITS ON YOU, on the Law page above the agreements it reads
//  today. Everything here is the route's own (agentic_core/api/waiting.py, W1085): an obligation falling due within the
//  window or past its date, soonest first, and an obligation no person has confirmed, each with the clause it was read
//  from and the agreement it is on. The list says what it reads and what it does not read yet, so an empty list says
//  only that nothing it reads is waiting. With sign-in off nothing is kept, and the panel says the route's reason. A
//  read that fails is said with its reason, never as nothing waiting.
import React, { useCallback, useEffect, useState } from 'react';
import { apiJson, asClause, errorMessage } from '../lib/api';

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

  return (
    <div className="space-y-3" data-testid="waiting-panel">
      <h3 className="text-lg font-black text-white uppercase tracking-tight">What waits on you</h3>
      {w === null && !err && <p className="text-[11px] text-slate-500">Reading what waits on you…</p>}
      {err && <p data-testid="waiting-unread" className="text-[11px] text-rose-300">{err}</p>}
      {w && w.kept === false && <p data-testid="waiting-not-kept" className="text-[11px] text-amber-300">{w.said}</p>}
      {w && w.kept === true && ((w.items ?? []).length === 0 ? (
        <p data-testid="waiting-none" className="text-[11px] text-slate-500">{w.said}</p>
      ) : (
        <ul className="space-y-1">
          {(w.items ?? []).map((i: any) => (
            <li key={`${i.kind}-${i.obligation_id}`} data-testid="waiting-item" className="text-[11px] text-slate-300">
              {`${i.what} (${i.clause}, on ${i.agreement_title}): ${asClause(String(i.said ?? ''))}${i.kind === 'falls_due' && !i.confirmed ? '; not confirmed by a person yet' : ''}.`}
            </li>
          ))}
        </ul>
      ))}
      {w && (
        <p data-testid="waiting-reads" className="text-[10px] text-slate-500">
          {`This list reads ${(w.reads ?? []).join('; ')}. It does not read yet: ${(w.not_read_yet ?? []).join('; ')}. ${w.date_basis ?? ''}`}
        </p>
      )}
      <button type="button" disabled={busy} onClick={read}
        className="px-3 py-1.5 rounded-lg bg-slate-800 text-[10px] font-black uppercase tracking-widest text-aura disabled:opacity-40">
        Read it again
      </button>
    </div>
  );
}
