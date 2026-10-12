import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Wallet as WalletIcon, ArrowUpRight, ArrowDownLeft, ShieldCheck, Activity, Star, Shield, CreditCard, Landmark, DollarSign, Loader2 } from 'lucide-react';
import { notImplemented } from '@workstation/ui';

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
}

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

export const Wallet: React.FC = () => {
  const [fund, setFund] = useState<FundStatus | null>(null);
  const [allocations, setAllocations] = useState<Allocation[]>([]);
  const [allocBasis, setAllocBasis] = useState<string | null>(null);   // W577 (FU-298)
  const [requests, setRequests] = useState<AllocationRequest[]>([]);          // FU-794
  const [requestsUnread, setRequestsUnread] = useState<string | null>(null);  // FU-794
  const [portfolioErr, setPortfolioErr] = useState<string | null>(null);      // FU-794
  const [loading, setLoading] = useState(true);
  const [down, setDown] = useState(false);

  useEffect(() => {
    Promise.all([
      axios.get('/api/v1/fund/status', { validateStatus: () => true }),
      axios.get('/api/v1/fund/portfolio', { validateStatus: () => true }),
    ]).then(([statusRes, portfolioRes]) => {
      if (statusRes.status === 200) setFund(statusRes.data);
      if (portfolioRes.status === 200) {
        const allocs: Allocation[] = portfolioRes.data.allocations ?? [];
        // W577 (FU-298) — the portfolio is where a missing allocation is most invisible: every
        // by_domain and by_realm total is a sum over rows that may not all be here.
        setAllocBasis(portfolioRes.data.allocations_are_incomplete
          ? (portfolioRes.data.allocations_basis ?? '') : null);
        setAllocations(allocs.slice(-8).reverse());
        // FU-794 - an unreadable list arrives as null with its reason, and is never shown as an empty one
        const reqs: unknown = portfolioRes.data.allocation_requests;
        if (Array.isArray(reqs)) {
          setRequests((reqs as AllocationRequest[]).slice(0, 8));
        } else {
          setRequestsUnread(flat(portfolioRes.data.allocation_requests_basis ?? 'the allocation requests could not be read'));
        }
      } else {
        setPortfolioErr(`The portfolio could not be read (HTTP ${portfolioRes.status}): ${flat(portfolioRes.data?.detail)}`);
      }
    }).catch(() => setDown(true)).finally(() => setLoading(false));
  }, []);

  // W329 — honest: a dead backend shows '—', never a fabricated 10,000,000 WST / HEALTHY
  const wst = fund?.available;
  const allocated = fund?.allocated ?? 0;
  const health = fund ? (fund.fund_health ?? '?') : (down ? 'BACKEND UNREACHABLE' : '…');

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
               <p className="text-4xl font-black text-white">{allocated.toLocaleString()}</p>}
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <BalanceCard label="Utilisation" value={fund ? `${fund.utilisation_pct}%` : '—'} icon={Activity} color="text-vital" />
        <BalanceCard label="Fund Health" value={health} icon={ShieldCheck} color={health === 'HEALTHY' ? 'text-aura' : 'text-yellow-400'} />
        <BalanceCard label="Allocations" value={fund?.allocation_count?.toString() ?? '0'} icon={CreditCard} color="text-highlight" />
        <BalanceCard label="Total Pool" value={fund ? `${(fund.total_capital / 1_000_000).toFixed(0)}M WST` : '—'} icon={Star} color="text-aura" />
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
         <button type="button" onClick={() => notImplemented('Allocate Capital')} className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all">Allocate</button>
      </div>

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
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8">Recent Capital Allocations</h3>
        {loading ? (
          <div className="flex items-center gap-2 text-slate-500 text-sm"><Loader2 size={14} className="animate-spin" /> Loading allocations…</div>
        ) : allocations.length === 0 ? (
          <p className="text-slate-600 text-sm">
            {allocBasis !== null
              ? "The fund store could not be read whole, so whether any capital has been allocated is unknown — this is not an empty portfolio."
              : "No capital allocations yet. Deploy capital to a project to see transactions here."}
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
