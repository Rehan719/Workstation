/**
 * W442 — the economy ops that existed server-side with no surface.
 *
 *   • VenturePortfolioPanel — GET /ventures/portfolio + POST /ventures/return. The §6 spec promises
 *     "returns recycle into the waterfall", but only pytest could press that button: the product
 *     showed a top-3 invested-only view with no return figures, so a pending 500-WST return was
 *     indistinguishable from nothing. Returns are CALLER-ASSERTED (nothing measures them) — the
 *     backend bounds them at 10× invested and this panel says so rather than implying measurement.
 *   • TransferPanel — POST /transfer between the Owner's own entities. The primitive was fully
 *     governed (tenant-scoped, validate-first, materiality-held, gaas-gated, UEG-logged) but fired
 *     only inside contract settlement. The held branch renders as the SAME amber Change-Control
 *     card the cycle uses — a held transfer is the flow the Owner must see, never a silent no-op.
 *
 * All figures are virtual/simulated WST — no real money moves.
 */
import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Sprout, Loader2, AlertCircle, ShieldCheck, ArrowRightLeft, Recycle } from 'lucide-react';

// ── §6 Venture Portfolio ──────────────────────────────────────────────────────

interface Holding {
  id: string; name: string; domain?: string; invested_wst: number;
  returned_wst?: number; rounds?: number; last_score?: number; last_return_at?: string;
}

export const VenturePortfolioPanel: React.FC<{ vsbId: string }> = ({ vsbId }) => {
  const [pf, setPf] = useState<any>(null);
  const [loadErr, setLoadErr] = useState('');
  const [retAmt, setRetAmt] = useState<Record<string, number>>({});
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  // §6's visible loop start: what the next cycle's user_projects allocation selects from
  const [cands, setCands] = useState<any>(null);
  const load = () => {
    setLoadErr('');
    // W442 refuter catch: `.then(r => r.json()).then(setPf)` with no r.ok check rendered a
    // tenant-scoped 404 as the "no holdings" empty state — the documented HTTP-status-blindness
    // class apiJson exists to kill.
    fetch(`/api/v1/economy/ventures/portfolio?vsb_id=${encodeURIComponent(vsbId)}`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(setPf)
      .catch(e => setLoadErr(`Could not load the venture portfolio — ${e?.message ?? 'backend unreachable'} (this is not "no holdings").`));
    fetch(`/api/v1/economy/ventures/candidates?vsb_id=${encodeURIComponent(vsbId)}&top=5`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(setCands)
      .catch(() => setCands(null));   // candidates are supplementary — the portfolio's own error state governs
  };
  useEffect(() => { load(); }, [vsbId]);

  const recordReturn = async (holdingId: string) => {
    const amount = Number(retAmt[holdingId] || 0);
    setBusy(holdingId); setMsg(''); setErr('');
    try {
      const r = await fetch('/api/v1/economy/ventures/return', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vsb_id: vsbId, holding_id: holdingId, amount }),
      });
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setBusy(''); return; }
      setMsg(`${d.returned_wst.toLocaleString()} WST recorded on ${holdingId} — ${d.recycles}. (${d.amount_source})`);
      setRetAmt({ ...retAmt, [holdingId]: 0 });
      load();
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy('');
  };

  const holdings: Holding[] = pf?.holdings ?? [];
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between gap-3 flex-wrap mb-1">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
          <Sprout size={14} /> Venture Portfolio (§6) · returns recycle
        </h3>
        {pf && <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-400">
          invested {(pf.invested_total ?? 0).toLocaleString()} WST · pending returns {(pf.pending_returns_wst ?? 0).toLocaleString()} WST
        </span>}
      </div>
      <p className="text-[10px] text-slate-500 font-bold mb-4">
        Every holding with its invested capital AND its returns — the recycle half of the §6 loop. A recorded
        return queues as pending and the next metabolic cycle consumes it as intake revenue.
        <span className="text-amber-400"> Returns are caller-asserted (nothing measures them) — cumulative returns bounded at 10× invested. Virtual WST.</span>
      </p>
      {loadErr && <p role="alert" className="text-[10px] font-bold text-vital">{loadErr}</p>}
      {!loadErr && holdings.length === 0 && (
        <p className="text-[10px] text-slate-600 italic">{pf?.note || 'No venture investments yet (virtual) — positions accrue from each cycle’s user_projects allocation.'}</p>
      )}
      <div className="space-y-2">
        {holdings.map(h => (
          <div key={h.id} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
            <div className="flex items-center justify-between gap-3 flex-wrap">
              <div className="min-w-0">
                <p className="text-sm font-black text-white truncate">{h.name || h.id}</p>
                <p className="text-[9px] font-mono text-slate-600">
                  invested {h.invested_wst.toLocaleString()} WST · returned {(h.returned_wst ?? 0).toLocaleString()} WST
                  · {h.rounds ?? 0} rounds{h.last_return_at ? ` · last return ${h.last_return_at.slice(0, 10)}` : ''}
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <input type="number" min={0} value={retAmt[h.id] ?? ''} placeholder="WST"
                  onChange={e => setRetAmt({ ...retAmt, [h.id]: Number(e.target.value) })}
                  aria-label={`return amount for ${h.id}`}
                  className="w-24 bg-slate-900 border border-slate-800 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-highlight/50" />
                <Button onClick={() => recordReturn(h.id)} disabled={!!busy || !(retAmt[h.id] > 0)}
                  className="flex items-center gap-1.5 bg-highlight text-sovereign text-[10px]">
                  {busy === h.id ? <Loader2 size={12} className="animate-spin" /> : <Recycle size={12} />}
                  Record return
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
      {msg && <p className="text-emerald-400 text-[10px] font-bold mt-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {msg}</p>}
      {err && <p className="text-vital text-[10px] font-bold mt-2 flex items-center gap-1.5"><AlertCircle size={12} /> {err}</p>}
      {/* W442 — the §6 loop's visible START: the ranked candidates the next cycle's
          user_projects allocation selects from (read-only; the cycle invests, not this panel). */}
      {cands && (cands.candidates?.length ?? 0) > 0 && (
        <div className="mt-4 pt-3 border-t border-slate-900">
          <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-2">
            Investment candidates — ranked; the next cycle's user-projects allocation selects from these
            {cands.using_demo_candidates && <span className="text-amber-400"> · DEMO SET (platform has no real candidates yet)</span>}
          </p>
          <div className="space-y-1">
            {cands.candidates.map((c: any) => (
              <div key={c.id} className="flex items-center justify-between gap-2 p-2 rounded-lg bg-slate-950 border border-slate-900 text-[10px]">
                <span className="text-slate-300 font-bold truncate">{c.name || c.id}<span className="text-slate-600 font-mono"> · {c.domain || '—'}</span></span>
                <span className="font-mono text-slate-400 shrink-0">score {c.score}</span>
              </div>
            ))}
          </div>
          <p className="text-[9px] text-slate-600 mt-1.5">{cands.disclaimer}</p>
        </div>
      )}
    </Card>
  );
};

// ── Federation transfer (Owner-initiated, between the Owner's own entities) ───

export const TransferPanel: React.FC<{ fromVsb: string; entities: { vsb_id: string; name?: string }[]; onDone?: () => void }> =
  ({ fromVsb, entities, onDone }) => {
  const [to, setTo] = useState('');
  const [amount, setAmount] = useState(0);
  const [memo, setMemo] = useState('');
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [held, setHeld] = useState<any>(null);
  const [err, setErr] = useState('');

  const targets = entities.filter(e => e.vsb_id !== fromVsb);

  const doTransfer = async () => {
    setBusy(true); setErr(''); setResult(null); setHeld(null);
    try {
      const r = await fetch('/api/v1/economy/transfer', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_vsb: fromVsb, to_vsb: to, amount, memo }),
      });
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setBusy(false); return; }
      if (d.transfer == null) { setHeld(d.governance ?? { note: 'The transfer returned no result.' }); setBusy(false); return; }
      setResult({ ...d.transfer, governance: d.governance });
      setAmount(0); setMemo('');
      onDone?.();
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy(false);
  };

  return (
    <Card className="p-6">
      <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-1">
        <ArrowRightLeft size={14} /> Transfer WST between your entities (federation)
      </h3>
      <p className="text-[10px] text-slate-500 font-bold mb-4">
        The sender pays from its reserve fund (double-entry, refused on insufficient virtual funds); the
        receiver's next metabolic cycle consumes it as intake revenue. Material transfers are HELD for
        Change Control. <span className="text-amber-400">Virtual WST only — no real funds.</span>
      </p>
      {targets.length === 0 ? (
        <p className="text-[10px] text-slate-600 italic">No other living entities to transfer to — establish a second entity first (the receiver must be a registered living VSB).</p>
      ) : (
        <div className="flex items-end gap-3 flex-wrap">
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">From</label>
            <span className="inline-block bg-slate-950 border border-slate-900 rounded-xl px-3 py-2.5 text-xs font-mono text-slate-400">{fromVsb}</span>
          </div>
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">To</label>
            <select value={to} onChange={e => setTo(e.target.value)} aria-label="transfer receiver"
              className="text-xs bg-slate-900 border border-slate-800 rounded-xl px-3 py-2.5 text-white focus:outline-none focus:border-highlight/50">
              <option value="">select receiver…</option>
              {targets.map(t => <option key={t.vsb_id} value={t.vsb_id}>{t.name || t.vsb_id}</option>)}
            </select>
          </div>
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Amount (WST)</label>
            <input type="number" min={0} value={amount || ''} onChange={e => setAmount(Number(e.target.value))}
              aria-label="transfer amount"
              className="w-28 bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-highlight/50" />
          </div>
          <div className="flex-1 min-w-[140px]">
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Memo</label>
            <input value={memo} onChange={e => setMemo(e.target.value)} aria-label="transfer memo"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-highlight/50" />
          </div>
          <Button onClick={doTransfer} disabled={busy || !to || amount <= 0}
            className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
            {busy ? <Loader2 size={14} className="animate-spin" /> : <ArrowRightLeft size={14} />}
            Transfer
          </Button>
        </div>
      )}
      {held && (
        <div className={`mt-4 p-4 rounded-2xl border ${['blocked', 'halted'].includes(held.status) ? 'border-vital/40 bg-vital/5' : 'border-amber-500/40 bg-amber-500/5'}`}>
          {/* W442 refuter catch: a constitutional-gate BLOCK rendered as "Held for Change Control —
              Owner approval required" — both claims false (no CCA request exists; approval won't
              release it). The three verdicts are distinct and say distinct things. */}
          <p className={`text-[10px] font-black uppercase tracking-widest flex items-center gap-2 ${['blocked', 'halted'].includes(held.status) ? 'text-vital' : 'text-amber-400'}`}>
            <ShieldCheck size={13} /> {['blocked', 'halted'].includes(held.status)
              ? `Blocked by the constitutional gate (${held.status}) — nothing ran, nothing posted`
              : held.status === 'rejected_by_change_control' ? 'Rejected by Change Control'
              : 'Held for Change Control — Owner approval required'}
          </p>
          <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{held.note || (['blocked', 'halted'].includes(held.status)
            ? 'The gaas.v5 constitutional gate refused this transfer; no WST moved and no Change Control request exists.'
            : 'This transfer is material and awaits Change Control approval before any WST moves.')}</p>
          {held.cca_id && (
            <p className="text-[10px] font-mono text-slate-500 mt-1.5">
              Change request: <span className="text-aura">{held.cca_id}</span> — review it on the{' '}
              <a href="/change-control" className="text-aura underline underline-offset-2">Change Control Agency</a> page, then transfer again.
            </p>
          )}
        </div>
      )}
      {result && (
        <div className="mt-4 p-4 rounded-2xl border border-emerald-500/30 bg-emerald-500/5">
          <p className="text-[10px] font-black uppercase tracking-widest text-emerald-400 flex items-center gap-2">
            <ShieldCheck size={13} /> Transfer posted · {result.transfer_id}
          </p>
          <p className="text-xs text-slate-400 mt-1.5">
            {result.amount_wst.toLocaleString()} WST → {result.to_vsb} · sender reserve after: {result.sender_reserve_fund_after_wst.toLocaleString()} WST
          </p>
          <p className="text-[9px] text-slate-600 mt-1">{result.settlement}</p>
          {result.governance?.status === 'ungated_bypass_logged' && (
            <p className="text-[10px] font-black text-vital mt-1.5">governance gate was unavailable — the transfer ran ungated and a loud UEG bypass event was logged.</p>
          )}
          <p className="text-[9px] text-amber-400/80 italic mt-1">{result.disclaimer}</p>
        </div>
      )}
      {err && <p className="text-vital text-[10px] font-bold mt-3 flex items-center gap-1.5"><AlertCircle size={12} /> {err}</p>}
    </Card>
  );
};
