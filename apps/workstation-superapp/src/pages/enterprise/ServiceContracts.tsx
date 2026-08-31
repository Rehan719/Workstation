/**
 * §15 — entity-to-entity service contracts (W394).
 *
 * The backend lifecycle has existed since W330 and had no UI at all, so none of it was reachable:
 *   POST /api/v1/economy/contracts              client offers work to a provider entity
 *   POST /api/v1/economy/contracts/{id}/accept  provider accepts   (provider only)
 *   POST /api/v1/economy/contracts/{id}/deliver provider delivers  (runs a REAL org cascade scoped
 *                                               to the provider, binding its QMS quality verdict)
 *   POST /api/v1/economy/contracts/{id}/settle  client pays        (gaas-gated double-entry transfer)
 *
 * Honesty rules this surface follows, because the backend is honest and the UI must not undo that:
 *   • A delivery's real quality verdict and the resource that served it are shown as returned. A weak
 *     delivery reads as weak — nothing here upgrades it.
 *   • Settlement can be HELD by governance. The backend then leaves the contract at "delivered" and
 *     says so; this shows the hold rather than implying payment succeeded.
 *   • Every action reports its real failure. A 409 ("contract is accepted, not offered") is a fact
 *     about state, not a glitch to swallow.
 *   • Money is virtual WST. No real-money rail is involved.
 */

import React, { useEffect, useState, useCallback } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { Handshake, Loader2, AlertTriangle, ArrowRight } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

interface Entity { vsb_id: string; name?: string }

interface Contract {
  id: string;
  client_vsb: string;
  provider_vsb: string;
  brief: string;
  price_wst: number;
  status: string;                       // offered | accepted | delivered | settled
  delivery?: { run_id?: string; quality?: unknown; served_by?: string } | null;
  settlement?: { transfer_id?: string; held?: boolean; governance?: unknown } | null;
  offered_at?: string;
  note?: string;
}

const NEXT_ACTION: Record<string, { verb: string; path: string; who: string }> = {
  offered:   { verb: 'Accept',  path: 'accept',  who: 'provider' },
  accepted:  { verb: 'Deliver', path: 'deliver', who: 'provider' },
  delivered: { verb: 'Settle',  path: 'settle',  who: 'client' },
};

const STATUS_TONE: Record<string, string> = {
  offered:   'text-slate-400',
  accepted:  'text-highlight',
  delivered: 'text-aura',
  settled:   'text-emerald-400',
};

/** Renders whatever the backend returned for a quality verdict without asserting a shape. */
function qualityText(q: unknown): string | null {
  if (q === null || q === undefined) return null;
  if (typeof q === 'string' || typeof q === 'number') return String(q);
  if (typeof q === 'object') {
    const o = q as Record<string, unknown>;
    const v = o.verdict ?? o.overall ?? o.score ?? o.grade;
    if (v !== undefined) return String(v);
    try { return JSON.stringify(q).slice(0, 90); } catch { return null; }
  }
  return null;
}

export const ServiceContracts: React.FC<{ entities: Entity[] }> = ({ entities }) => {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState<string | null>(null);
  const [elapsed, setElapsed] = useState(0);
  const [notice, setNotice] = useState('');

  const [client, setClient] = useState('');
  const [provider, setProvider] = useState('');
  const [brief, setBrief] = useState('');
  const [price, setPrice] = useState('100');
  const [offering, setOffering] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    apiJson<{ contracts?: Contract[] }>('/api/v1/economy/contracts')
      .then(d => { setContracts(d.contracts ?? []); setError(''); })
      .catch(e => setError(errorMessage(e)))
      .finally(() => setLoading(false));
  }, []);
  useEffect(load, [load]);

  const offer = async () => {
    if (!client || !provider || !brief.trim()) return;
    setOffering(true); setError(''); setNotice('');
    try {
      await apiJson('/api/v1/economy/contracts', {
        method: 'POST',
        body: { client_vsb: client, provider_vsb: provider, brief: brief.trim(), price_wst: Number(price) || 0 },
      });
      setBrief('');
      setNotice('Contract offered. The provider must accept before any work or money moves.');
      load();
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setOffering(false);
    }
  };

  const advance = async (c: Contract) => {
    const step = NEXT_ACTION[c.status];
    if (!step) return;
    setBusy(c.id); setError(''); setNotice('');
    // Deliver runs the full org cascade — roughly 22 model calls across Chief → Board → AI CEO →
    // C-Suite → CoE → BTO → catalogue. On a local model that is 15–25 minutes. Measured, not
    // guessed: a first run was still going at 15 minutes. Without this the button just spins in
    // silence and reads as a hang, which is precisely the failure this surface exists to avoid.
    let tick: ReturnType<typeof setInterval> | null = null;
    if (step.path === 'deliver') {
      const t0 = Date.now();
      setElapsed(0);
      tick = setInterval(() => setElapsed(Math.round((Date.now() - t0) / 1000)), 1000);
    }
    try {
      const res = await apiJson<Contract>(`/api/v1/economy/contracts/${c.id}/${step.path}`, { method: 'POST' });
      // A held settlement comes back 200 with the contract still "delivered" and a note. Report it.
      if (res.settlement?.held || (res.note && /held/i.test(res.note))) {
        setNotice(res.note || 'Settlement was held by governance — the contract stays delivered. Retry once the hold clears.');
      } else if (step.path === 'settle') {
        setNotice(`Settled — transfer ${res.settlement?.transfer_id ?? 'recorded'} (virtual WST).`);
      } else {
        setNotice(`Contract ${res.status}.`);
      }
      load();
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      if (tick) clearInterval(tick);
      setElapsed(0);
      setBusy(null);
    }
  };

  const nameOf = (id: string) => entities.find(e => e.vsb_id === id)?.name || id;

  return (
    <Card className="p-5 space-y-4">
      <div>
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
          <Handshake size={14} /> §15 · Service contracts between entities
        </h3>
        <p className="text-slate-500 text-xs font-semibold mt-2 leading-relaxed max-w-3xl">
          One entity commissions another. The provider accepts, then delivers — which runs a real
          org cascade scoped to that entity and binds its quality verdict — and the client settles
          through the governed transfer rail. Virtual WST; no real-money rail is involved.
        </p>
      </div>

      {/* Offer */}
      <div className="grid grid-cols-1 @[720px]:grid-cols-2 gap-3">
        <label className="flex flex-col gap-1">
          <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Client (commissions &amp; pays)</span>
          <select value={client} onChange={e => setClient(e.target.value)} aria-label="Client entity"
            className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white">
            <option value="">Select an entity…</option>
            {entities.map(e => <option key={e.vsb_id} value={e.vsb_id}>{e.name || e.vsb_id}</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Provider (accepts &amp; delivers)</span>
          <select value={provider} onChange={e => setProvider(e.target.value)} aria-label="Provider entity"
            className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white">
            <option value="">Select an entity…</option>
            {entities.filter(e => e.vsb_id !== client).map(e => <option key={e.vsb_id} value={e.vsb_id}>{e.name || e.vsb_id}</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-1 @[720px]:col-span-2">
          <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Brief</span>
          <textarea value={brief} onChange={e => setBrief(e.target.value)} rows={2}
            placeholder="What is being commissioned?"
            className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white resize-none" />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Price (WST, virtual)</span>
          <input type="number" min="0" value={price} onChange={e => setPrice(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
        </label>
        <div className="flex items-end">
          <Button type="button" onClick={offer} disabled={offering || !client || !provider || !brief.trim()}>
            {offering ? <Loader2 size={13} className="animate-spin" /> : 'Offer contract'}
          </Button>
        </div>
      </div>

      {error && (
        <div role="alert" className="flex items-start gap-2 rounded-xl border border-vital/30 bg-vital/10 px-3 py-2">
          <AlertTriangle size={12} className="text-vital shrink-0 mt-0.5" />
          <p className="text-[10px] font-bold text-vital leading-relaxed">{error}</p>
        </div>
      )}
      {notice && (
        <div role="status" className="rounded-xl border border-aura/30 bg-aura/10 px-3 py-2">
          <p className="text-[10px] font-bold text-aura leading-relaxed">{notice}</p>
        </div>
      )}

      {/* Ledger of contracts */}
      {loading ? (
        <p className="text-[10px] font-bold text-slate-600 flex items-center gap-2"><Loader2 size={11} className="animate-spin" /> Loading contracts…</p>
      ) : contracts.length === 0 ? (
        <p className="text-xs text-slate-500 italic py-4">
          No contracts yet. Offer one above — nothing is created until you do.
        </p>
      ) : (
        <div className="space-y-2">
          {contracts.map(c => {
            const step = NEXT_ACTION[c.status];
            const q = qualityText(c.delivery?.quality);
            return (
              <div key={c.id} className="rounded-xl border border-slate-800 bg-slate-950/50 p-3 space-y-1.5">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-2 text-[10px] font-bold text-slate-400 min-w-0">
                    <span className="truncate max-w-[180px]">{nameOf(c.client_vsb)}</span>
                    <ArrowRight size={11} className="text-slate-600 shrink-0" />
                    <span className="truncate max-w-[180px]">{nameOf(c.provider_vsb)}</span>
                  </div>
                  <span className={`text-[9px] font-black uppercase tracking-widest ${STATUS_TONE[c.status] ?? 'text-slate-500'}`}>
                    {c.status}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">{c.brief}</p>
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-2 flex-wrap text-[9px] font-black uppercase tracking-widest text-slate-600">
                    <span className="text-aura">{c.price_wst.toLocaleString()} WST</span>
                    {q && <><span>·</span><span>quality {q}</span></>}
                    {c.delivery?.served_by && <><span>·</span><span>served by {c.delivery.served_by}</span></>}
                    {c.settlement?.held && <Badge className="text-[8px]">settlement held</Badge>}
                    {c.settlement?.transfer_id && <><span>·</span><span>transfer {String(c.settlement.transfer_id).slice(0, 10)}</span></>}
                    {c.status === 'accepted' && (
                      <span className="normal-case tracking-normal font-semibold text-slate-500">
                        · delivering runs a full org cascade (~22 model calls) — expect 15–25 minutes
                      </span>
                    )}
                  </div>
                  {step && (
                    <Button type="button" onClick={() => advance(c)} disabled={busy === c.id}
                      className="text-[9px] px-3 py-1.5">
                      {busy === c.id
                        ? <span className="flex items-center gap-1.5"><Loader2 size={11} className="animate-spin" />
                            {step.path === 'deliver' ? `${elapsed}s` : ''}</span>
                        : `${step.verb} (${step.who})`}
                    </Button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
};
