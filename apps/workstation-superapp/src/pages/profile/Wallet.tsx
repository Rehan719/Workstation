import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Wallet as WalletIcon, ArrowUpRight, ArrowDownLeft, ShieldCheck, Activity, Star, Shield, CreditCard, Landmark, DollarSign, Loader2 } from 'lucide-react';

interface FundStatus {
  total_capital: number;
  currency: string;
  allocated: number;
  available: number;
  utilisation_pct: number;
  allocation_count: number;
  fund_health: string;
}

interface Allocation {
  allocation_id: string;
  project_name: string;
  amount: number;
  purpose: string;
  domain: string;
  realm: string;
  allocated_at?: string;
  // W672 (ledger v16 R6.5) - what the allocation passed, as the fund recorded it
  governance?: { gate?: string; change_control?: string; recipient_registered?: boolean | null; basis?: string };
  // FU-794 - the change that authorised it (absent on a row stored before allocations were governed)
  cca_id?: string | null;
  record_state?: string;
  record_state_label?: string;
  // W861 (FU-1005) - an allocation is reversed by a recorded reversal, held for a person's decision first
  status?: string;
  reversal?: { reason: string; reversed_at: string; requested_by?: string; cca_id?: string } | null;
}

// W861 (FU-1005) - request the reversal of an active allocation: held at Change Control, applied when requested again
const ReverseAllocation: React.FC<{ id: string }> = ({ id }) => {
  const [reason, setReason] = useState('');
  const [said, setSaid] = useState('');
  //  W981 (FU-399 part 14) - a request that could not be sent is said, and a refusal gives its status with its reason
  const ask = async () => {
    try {
      const r = await axios.post(`/api/v1/fund/allocations/${encodeURIComponent(id)}/reverse`, { reason },
        { validateStatus: () => true });
      setSaid(r.status === 200
        ? String(r.data?.basis ?? '') + (r.data?.request_recorded && r.data.request_recorded !== 'recorded'
            ? ` The request's details were ${String(r.data.request_recorded)} on the hold.` : '')
        : `Not requested (HTTP ${r.status}): ${flat(r.data?.detail)}`);
    } catch {
      setSaid('Not requested: the server could not be reached, so nothing was asked of Change Control.');
    }
  };
  return (
    <div className="mt-2 flex flex-wrap items-center gap-2" data-testid="wallet-allocation-reverse">
      <input value={reason} onChange={e => setReason(e.target.value)} placeholder="why this allocation is reversed…"
        className="text-[10px] bg-slate-900 border border-slate-800 rounded p-1.5 text-slate-300 w-64" />
      <button type="button" onClick={ask} disabled={reason.trim().length < 12}
        className="text-[9px] font-black uppercase px-2 py-1 rounded border border-slate-700 text-slate-300 disabled:opacity-40">request reversal</button>
      {said && <span data-testid="wallet-allocation-reverse-said" className="text-[9px] text-amber-400/80 normal-case">{said}</span>}
    </div>
  );
};

// FU-794 - a REQUEST for an allocation, as its Change Control record stands now. Not an allocation.
interface AllocationRequest {
  cca_id: string;
  state: string;
  state_label: string;
  project_id?: string | null;
  project_name?: string | null;
  amount?: number | null;
  decided_by?: string | null;
  decided_by_verified?: boolean | null;
  allocation_id?: string | null;
}

// a refusal's detail may be a string or an object: it is flattened to text and never rendered as a child
const flat = (d: unknown): string =>
  typeof d === 'string' ? d : d == null ? 'no reason was given' : JSON.stringify(d);

//  W1033 - request an allocation. The fund's route is built: it checks the recipient exists, holds the request at
//  Change Control for an explicit decision, and applies it once when the same allocation is requested again. This
//  page's "Allocate" said "not implemented" over it
const RequestAllocation: React.FC = () => {
  const [to, setTo] = useState('');
  const [name, setName] = useState('');
  const [amount, setAmount] = useState('');
  const [purpose, setPurpose] = useState('');
  const [said, setSaid] = useState('');
  const ask = async () => {
    try {
      const r = await axios.post('/api/v1/fund/allocate',
        { project_id: to.trim(), project_name: name.trim(), amount: Number(amount), purpose: purpose.trim() },
        { validateStatus: () => true });
      setSaid(r.status === 200
        ? String(r.data?.governance?.basis ?? r.data?.status_label ?? 'The fund answered and said nothing of what it did.')
        : `Not requested (HTTP ${r.status}): ${flat(r.data?.detail)}`);
    } catch {
      setSaid('Not requested: the server could not be reached, so nothing was asked of Change Control.');
    }
  };
  const ready = to.trim() !== '' && name.trim() !== '' && Number(amount) > 0 && purpose.trim() !== '';
  const field = 'text-[11px] bg-slate-900 border border-slate-800 rounded-lg p-2 text-slate-300';
  return (
    <div className="mt-6 flex flex-wrap items-center gap-2" data-testid="wallet-allocation-request">
      <input aria-label="Recipient id" value={to} onChange={e => setTo(e.target.value)} placeholder="the entity's or project's id" className={`${field} w-56`} />
      <input aria-label="Recipient name" value={name} onChange={e => setName(e.target.value)} placeholder="its name" className={`${field} w-48`} />
      <input aria-label="Amount (WST)" value={amount} onChange={e => setAmount(e.target.value)} placeholder="amount in WST" inputMode="decimal" className={`${field} w-32`} />
      <input aria-label="Purpose" value={purpose} onChange={e => setPurpose(e.target.value)} placeholder="what it is for" className={`${field} w-64`} />
      <button type="button" onClick={ask} disabled={!ready}
        className="text-[10px] font-black uppercase px-3 py-2 rounded-lg border border-aura/40 text-aura disabled:opacity-40">request the allocation</button>
      {said && <p data-testid="wallet-allocation-request-said" className="basis-full text-[11px] text-amber-400/80">{said}</p>}
    </div>
  );
};

export const Wallet: React.FC = () => {
  const [fund, setFund] = useState<FundStatus | null>(null);
  const [allocOpen, setAllocOpen] = useState(false);   // W1033 - the request, opened by "Allocate"
  const [allocations, setAllocations] = useState<Allocation[]>([]);
  const [allocBasis, setAllocBasis] = useState<string | null>(null);   // W577 (FU-298)
  const [requests, setRequests] = useState<AllocationRequest[]>([]);          // FU-794
  const [requestsUnread, setRequestsUnread] = useState<string | null>(null);  // FU-794
  //  W861 (FU-1005) - the reversal requests, each as its Change Control record stands, with its reason
  const [reversals, setReversals] = useState<any[] | null>([]);
  const [reversalsBasis, setReversalsBasis] = useState<string>('');
  const [portfolioErr, setPortfolioErr] = useState<string | null>(null);      // FU-794
  //  W981 (FU-399 part 14) - a refused read of the fund's status is said, never shown as figures of zero
  const [statusErr, setStatusErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [down, setDown] = useState(false);

  useEffect(() => {
    Promise.all([
      axios.get('/api/v1/fund/status', { validateStatus: () => true }),
      axios.get('/api/v1/fund/portfolio', { validateStatus: () => true }),
    ]).then(([statusRes, portfolioRes]) => {
      if (statusRes.status === 200) setFund(statusRes.data);
      else setStatusErr(`The fund's status could not be read (HTTP ${statusRes.status}): ${flat(statusRes.data?.detail)}`);
      if (portfolioRes.status === 200) {
        const allocs: Allocation[] = portfolioRes.data.allocations ?? [];
        // W577 (FU-298) — the portfolio is where a missing allocation is most invisible: every
        // by_domain and by_realm total is a sum over rows that may not all be here.
        setAllocBasis(portfolioRes.data.allocations_are_incomplete
          ? (portfolioRes.data.allocations_basis ?? '') : null);
        setAllocations(allocs.slice(-8).reverse());
        // FU-794 - an unreadable list arrives as null with its reason, and is never shown as an empty one
        setReversals(Array.isArray(portfolioRes.data.reversal_requests) ? portfolioRes.data.reversal_requests.slice(0, 8) : null);
        setReversalsBasis(flat(portfolioRes.data.reversal_requests_basis ?? ''));
        const reqs: unknown = portfolioRes.data.allocation_requests;
        if (Array.isArray(reqs)) {
          setRequests((reqs as AllocationRequest[]).slice(0, 8));
        } else {
          setRequestsUnread(flat(portfolioRes.data.allocation_requests_basis ?? 'the allocation requests could not be read'));
        }
      } else {
        setPortfolioErr(`The portfolio could not be read (HTTP ${portfolioRes.status}): ${flat(portfolioRes.data?.detail)}`);
      }
    }).catch(() => {
      //  W981 - an unreachable server is said where each read is shown, never as an empty portfolio
      setDown(true);
      setPortfolioErr('The portfolio could not be read: the server could not be reached.');
    }).finally(() => setLoading(false));
  }, []);

  // W329 — honest: a dead backend shows '—', never a fabricated 10,000,000 WST / HEALTHY
  //  W981 (FU-399 part 14) - and a status that could not be read shows a dash for each figure, never a zero
  const wst = fund?.available;
  const allocated = fund ? fund.allocated : undefined;
  const health = fund ? (fund.fund_health ?? '?') : (down ? 'BACKEND UNREACHABLE' : statusErr ? 'NOT READ' : '…');

  return (
    <div className="space-y-12 animate-in fade-in duration-1000">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black tracking-tight neon-text break-words">Sovereign Economy</h1>
          <p className="text-slate-500 font-bold text-lg mt-2">Capital Fund — WST liquidity and virtual capital allocation.</p>
        </div>
        <div className="text-right flex items-center gap-6">
           <div>
             <p className="text-[10px] font-black text-slate-500 uppercase">Available WST</p>
             {loading ? <div className="h-10 w-32 bg-slate-800 animate-pulse rounded" /> :
               <p className="text-4xl font-black text-aura">{wst !== undefined ? wst.toLocaleString() : '—'}</p>}
           </div>
           <div className="h-10 w-[1px] bg-white/10"></div>
           <div>
             <p className="text-[10px] font-black text-slate-500 uppercase">Allocated</p>
             {loading ? <div className="h-10 w-24 bg-slate-800 animate-pulse rounded" /> :
               <p className="text-4xl font-black text-white" data-testid="wallet-allocated">{allocated !== undefined ? allocated.toLocaleString() : '—'}</p>}
           </div>
        </div>
      </header>
      {statusErr && (
        <p data-testid="wallet-status-unread" className="text-[11px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400">{statusErr}</p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <BalanceCard label="Utilisation" value={fund ? `${fund.utilisation_pct}%` : '—'} icon={Activity} color="text-vital" />
        <BalanceCard label="Fund Health" value={health} icon={ShieldCheck} color={health === 'HEALTHY' ? 'text-aura' : 'text-yellow-400'} />
        <BalanceCard label="Allocations" value={fund ? String(fund.allocation_count ?? '—') : '—'} icon={CreditCard} color="text-highlight" />
        {/* W981 (FU-399 part 14) - the pool as the fund states it: rounded to whole millions, 10,000 WST read "0M WST" */}
        <BalanceCard label="Total Pool" value={fund ? `${fund.total_capital.toLocaleString()} WST` : '—'} icon={Star} color="text-aura" />
      </div>

      <div className="p-12 glass-card bg-aura/5 border-aura/20 flex items-center justify-between">
         <div className="flex items-center gap-6">
            <div className="p-4 bg-aura/20 rounded-2xl text-aura">
               <Landmark size={32} />
            </div>
            <div>
               <h3 className="text-2xl font-black">Allocate Capital</h3>
               <p className="text-slate-400 font-bold">Deploy sovereign capital to projects and VSB entities from the fund.</p>
               <p className="text-slate-500 text-xs font-bold mt-1" data-testid="wallet-allocation-governed">An allocation is requested, held at Change Control for an explicit decision, and applied only after it is approved.</p>
            </div>
         </div>
         <button type="button" onClick={() => setAllocOpen(o => !o)} aria-expanded={allocOpen} className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all">Allocate</button>
      </div>
      {allocOpen && <RequestAllocation />}

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800" data-testid="wallet-allocation-requests">
        <h3 className="text-xl font-bold mb-2">Allocation Requests</h3>
        <p className="text-[11px] text-slate-500 font-bold mb-6">A request moves nothing. It is held at Change Control until an explicit decision approves it, and it is applied when the same allocation is requested again.</p>
        {portfolioErr && (
          <p data-testid="wallet-portfolio-error" className="text-[11px] font-bold px-2 py-1 rounded bg-rose-500/20 text-rose-400 mb-3">{portfolioErr}</p>
        )}
        {requestsUnread !== null && (
          <p data-testid="wallet-requests-unread" className="text-[11px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400 mb-3">{requestsUnread}</p>
        )}
        {!loading && !portfolioErr && requestsUnread === null && requests.length === 0 && (
          <p className="text-slate-600 text-sm">No allocation has been requested.</p>
        )}
        <div className="space-y-3">
          {requests.map((req) => (
            <div key={req.cca_id} data-testid="wallet-allocation-request" className="flex items-center justify-between p-4 rounded-2xl bg-slate-800/30 border border-slate-700/50">
              <div>
                <p className="font-bold uppercase tracking-widest text-xs text-white">{String(req.project_name ?? req.project_id ?? 'recipient not recorded')}</p>
                <p data-testid="wallet-allocation-request-state" className={`text-[10px] font-black mt-1 ${req.state === 'applied' ? 'text-emerald-400' : req.state === 'rejected' || req.state === 'withdrawn' ? 'text-rose-400' : 'text-amber-400'}`}>{req.state_label}</p>
                <p className="text-[10px] text-slate-500 mt-1">
                  Change {req.cca_id}
                  {req.decided_by ? ` · decided by ${req.decided_by}${req.decided_by_verified ? '' : ' (a name the platform did not check)'}` : ' · not decided'}
                </p>
              </div>
              <div className="text-sm font-black text-slate-300">
                {typeof req.amount === 'number' ? req.amount.toLocaleString() : '—'} WST {req.state === 'applied' ? 'applied' : 'requested'}
              </div>
            </div>
          ))}
        </div>
        {reversals === null && (
          <p data-testid="wallet-reversals-unread" className="text-[11px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400 mt-3">{reversalsBasis}</p>
        )}
        {reversals && reversals.length > 0 && (
          <div className="mt-6 space-y-2" data-testid="wallet-reversal-requests">
            <h4 className="text-xs font-black uppercase tracking-widest text-slate-400" title={reversalsBasis}>Reversal requests</h4>
            {reversals.map((rv: any) => (
              <p key={rv.cca_id} className="text-[10px] text-slate-400" data-testid="wallet-reversal-request">
                {rv.allocation_id} · {typeof rv.amount === 'number' ? rv.amount.toLocaleString() : '—'} WST · {rv.status} · change {rv.cca_id}
                {rv.reason ? ` · "${rv.reason}"` : ''}{rv.requested_by ? ` · asked by ${rv.requested_by}` : ''}{rv.requested_at ? ` at ${rv.requested_at}` : ''}
              </p>
            ))}
          </div>
        )}
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8">Recent Capital Allocations</h3>
        {loading ? (
          <div className="flex items-center gap-2 text-slate-500 text-sm"><Loader2 size={14} className="animate-spin" /> Loading allocations…</div>
        ) : portfolioErr ? (
          <p data-testid="wallet-allocations-unread" className="text-slate-500 text-sm">
            The portfolio was not read, so whether any capital has been allocated is not known.
          </p>
        ) : allocations.length === 0 ? (
          <p className="text-slate-600 text-sm" data-testid="wallet-allocations-none">
            {allocBasis !== null
              ? "The fund store could not be read whole, so whether any capital has been allocated is unknown — this is not an empty portfolio."
              : "No capital has been allocated."}
          </p>
        ) : (
          <div className="space-y-4">
            {allocBasis !== null && (
              <p data-testid="wallet-allocations-incomplete" title={allocBasis || undefined}
                 className="text-[10px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400">
                allocations are missing from this portfolio — the fund store could not be read whole
              </p>
            )}
            {allocations.map((alloc) => (
              <div key={alloc.allocation_id} className="flex items-center justify-between p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
                 <div className="flex items-center gap-4">
                   <div className="p-2 rounded-lg bg-vital/10 text-vital">
                     <ArrowDownLeft size={20} />
                   </div>
                   <div>
                     <p className="font-bold uppercase tracking-widest text-xs text-white">{alloc.project_name}</p>
                     <p className="text-[10px] text-slate-500 mt-1">{alloc.purpose} · {alloc.domain} · {alloc.realm}</p>
                     {alloc.governance?.basis && (
                       <p data-testid="wallet-allocation-governance" className="text-[9px] text-amber-400/80 mt-1 normal-case">{alloc.governance.basis}</p>
                     )}
                     {alloc.record_state_label && (
                       <p data-testid="wallet-allocation-state" className="text-[9px] text-slate-500 mt-1 normal-case">{alloc.record_state_label}{alloc.cca_id ? ` · change ${alloc.cca_id}` : ''}</p>
                     )}
                     {alloc.status === 'reversed' && alloc.reversal ? (
                       <p data-testid="wallet-allocation-reversed" className="text-[9px] text-slate-400 mt-1 normal-case">
                         REVERSED {alloc.reversal.reversed_at}: {alloc.reversal.reason}{alloc.reversal.cca_id ? ` · change ${alloc.reversal.cca_id}` : ''}{alloc.reversal.requested_by ? ` · asked by ${alloc.reversal.requested_by}` : ''}
                       </p>
                     ) : (alloc.status ?? 'active') === 'active' && <ReverseAllocation id={alloc.allocation_id} />}
                   </div>
                 </div>
                 <div className="text-lg font-black text-vital">
                   +{alloc.amount.toLocaleString()} WST
                 </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const BalanceCard = ({ label, value, icon: Icon, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <div className="flex justify-between items-center mb-6">
      <div className={`p-3 rounded-xl bg-slate-800/50 ${color}`}>
        <Icon size={24} />
      </div>
    </div>
    <div className="text-3xl font-black">{typeof value === 'number' ? value.toLocaleString() : value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
