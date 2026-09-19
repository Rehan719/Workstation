import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import {
  Coins, Recycle, Activity, Sprout, Building2, PiggyBank,
  Loader2, AlertCircle, HeartPulse, ShieldCheck, Gift,
} from 'lucide-react';
import { ServiceContracts } from './ServiceContracts';
import { CharityDirectives } from './CharityDirectives';
import { VenturePortfolioPanel, TransferPanel } from './EconomyOperations';

// ── Types ─────────────────────────────────────────────────────────────────────

interface EntityType {
  id: string; name: string; description: string;
  distributes_profit: boolean; capital_preserved: boolean; waterfall: Record<string, number>;
}
interface Cycle {
  intake_revenue: number; homeostasis_reserves: number; operating_costs?: number; distributable_profit: number;
  circulation: Record<string, { amount_wst: number; role: string }>;
  giving_back: { grants: { cause: string; amount_wst: number; score: number }[] } | null;
  metabolic_energy: number | null; entity_name: string; capital_preserved: boolean;
  energy_state?: string; reserve_rate_applied?: number;   // §8→§12 economic survival instinct
  biogeochemical_model: string;
  // W465 (FU-016) — whether this cycle's owner share was recorded in Owner Payments
  owner_accrual?: { accrued: boolean; amount_wst: number; error?: string; note?: string; ueg_logged?: boolean };
}

interface WaterfallState {
  waterfall: Record<string, number>; source: string; template_default: Record<string, number>;
  stages: string[]; constraints: { distributes_profit: boolean; capital_preserved: boolean };
}

const STAGE_ICON: Record<string, React.ComponentType<any>> = {
  owner: Coins, self_investment: Sprout, capital_fund: PiggyBank,
  user_projects: Activity, charity: Recycle,
};
const STAGE_LABEL: Record<string, string> = {
  owner: 'Owner', self_investment: 'Self-Investment', capital_fund: 'Capital Fund',
  user_projects: 'User Projects', charity: 'Charity (return loop)',
};

// ── Component ─────────────────────────────────────────────────────────────────

export const VSBEconomy: React.FC = () => {
  const [types, setTypes] = useState<EntityType[]>([]);
  // W298 - the economy surface is SCOPE-AWARE: manage the workstation apex OR any of YOUR
  // established VSBs (the backend was already fully per-VSB; only this UI pinned the apex).
  const [sp] = useSearchParams();
  const [vsbId, setVsbId] = useState(sp.get('vsb') ?? 'workstation-idbo');
  // W465 — the entity a load was issued for is compared with the one on screen when its answer lands: an answer for
  // an entity the Owner has since switched away from is dropped, never shown under the new one
  const currentVsb = useRef(vsbId);
  currentVsb.current = vsbId;
  const [entity, setEntity] = useState('waqf_ltd_hybrid');
  const [revenue, setRevenue] = useState(10000);
  const [costs, setCosts] = useState(1000);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [cycle, setCycle] = useState<Cycle | null>(null);
  const [gov, setGov] = useState<string>('');
  // Ledger cluster 1 — a MATERIAL cycle returns 200 {cycle:null, governance:held...}; that hold
  // must be VISIBLE (it is exactly the flow the Owner has to approve), never a silent no-op.
  const [hold, setHold] = useState<{ status?: string; cca_id?: string; note?: string; follows_rejection?: string; rejected_by?: string; decided_concurrently?: boolean } | null>(null);
  // §4/§8/§10 — Owner-adjustable profit waterfall (virtual, template-bounded)
  const [wf, setWf] = useState<WaterfallState | null>(null);
  const [wfDraft, setWfDraft] = useState<Record<string, number>>({});   // percentages (0-100) the Owner edits
  const [wfSaving, setWfSaving] = useState(false);
  const [wfMsg, setWfMsg] = useState('');
  const [wfErr, setWfErr] = useState<string[]>([]);
  const [wfLoadErr, setWfLoadErr] = useState('');
  const [transferring, setTransferring] = useState(false);   // a TransferPanel transfer in flight
  // §7 — Owner-payments ledger (virtual; real rails disabled+gated)
  const [pay, setPay] = useState<any>(null);
  const [payoutAmt, setPayoutAmt] = useState(0);
  const [payingOut, setPayingOut] = useState(false);
  const [payMsg, setPayMsg] = useState('');
  const [payErr, setPayErr] = useState('');

  // W465 (FU-016) — an error answer used to be stored as the account and shown as 0 WST with a live payout button;
  // the store's own refusal (503: unreadable, never overwritten) is now shown as what it is
  const [payLoadErr, setPayLoadErr] = useState('');
  const loadOwnerPay = () => {
    const issuedFor = vsbId;
    return fetch(`/api/v1/economy/owner-payments?vsb_id=${encodeURIComponent(issuedFor)}`)
      .then(async r => {
        const d = await r.json().catch(() => null);
        if (issuedFor !== currentVsb.current) return;   // a late answer for another entity
        // an error answer, or a body that is not an account, is never stored as one (it rendered as 0 WST)
        if (!r.ok || !d || typeof d.balance_wst !== 'number') {
          setPay(null);
          setPayLoadErr(typeof d?.detail === 'string' ? d.detail : `Could not load the owner payments (HTTP ${r.status}).`);
          return;
        }
        setPayLoadErr('');
        setPay(d);
      }).catch(() => {
        if (issuedFor !== currentVsb.current) return;
        setPay(null); setPayLoadErr('Could not load the owner payments — showing nothing rather than zero balances.');
      });
  };
  // §7 — the live financial Board Pack (capstone statement)
  const [bp, setBp] = useState<any>(null);
  const [bpLoading, setBpLoading] = useState(false);
  const [bpLoadErr, setBpLoadErr] = useState('');   // its own state: a later good load clears it
  const loadBoardPack = () => {
    const issuedFor = vsbId;
    if (issuedFor === currentVsb.current) setBpLoading(true);
    fetch(`/api/v1/economy/board-pack?vsb_id=${encodeURIComponent(issuedFor)}&entity_type=${entity}`)
      .then(async r => {
        const d = await r.json().catch(() => null);
        if (issuedFor !== currentVsb.current) return;   // a late answer for another entity
        if (!r.ok || !d) { setBp(null); setBpLoadErr(typeof d?.detail === 'string' ? d.detail : `Could not load the board pack (HTTP ${r.status}).`); return; }
        setBpLoadErr('');
        setBp(d);
      }).catch(() => {
        if (issuedFor !== currentVsb.current) return;
        setBp(null); setBpLoadErr('Could not load the board pack — showing nothing rather than stale figures.');
      }).finally(() => { if (issuedFor === currentVsb.current) setBpLoading(false); });
  };
  // a transfer that finishes after an entity switch refreshes the pack of the entity ON SCREEN, not the one its
  // button was rendered for
  const loadBoardPackRef = useRef(loadBoardPack);
  loadBoardPackRef.current = loadBoardPack;
  // §4 — the established living VSB enterprises the organism autonomously tends
  const [living, setLiving] = useState<any>(null);
  // W395 — these loads used to fail silently (`.catch(() => {})`), leaving the page's headline
  // figures simply absent with no indication anything had gone wrong. An empty panel that means
  // "the request failed" is indistinguishable from one that means "there is no data".
  const [loadErr, setLoadErr] = useState('');
  const loadLiving = () =>
    fetch('/api/v1/economy/living-vsbs').then(r => r.json()).then(setLiving).catch(() => setLoadErr('Could not load the living entities — showing nothing rather than stale figures.'));

  useEffect(() => {
    fetch('/api/v1/economy/entity-types').then(r => r.json()).then(d => setTypes(d.types ?? [])).catch(() => {});
    loadOwnerPay();
    loadBoardPack();
    loadLiving();
  }, []);

  // W298 - the scoped ledgers follow the selected entity
  // W465 — another entity's figures, cycle report, hold and messages are cleared on a switch (its waterfall split by
  // the waterfall effect, its transfer form by remounting the panel); a load still in flight for the previous entity
  // is dropped when it lands (the guard above), and the picker is locked while a cycle, payout, period close,
  // waterfall save or transfer runs, so none of those can finish under a different entity than the one it acted on
  useEffect(() => {
    setPay(null); setBp(null); setPayLoadErr(''); setBpLoadErr('');
    setCycle(null); setGov(''); setHold(null); setError('');
    setPayMsg(''); setPayErr(''); setCloseMsg(''); setCloseErr('');
    loadOwnerPay(); loadBoardPack();
  }, [vsbId]);

  // Load the effective waterfall whenever the entity form changes (per VSB = workstation-idbo).
  useEffect(() => {
    let live = true;   // W465 — an answer for a previous entity or form is dropped
    // …and the previous entity's split is never left on screen, editable and saveable under this one
    setWf(null); setWfDraft({}); setWfLoadErr('');
    setWfMsg(''); setWfErr([]);
    fetch(`/api/v1/economy/waterfall?vsb_id=${encodeURIComponent(vsbId)}&entity_type=${entity}`)
      .then(async r => {
        const d = await r.json().catch(() => null) as WaterfallState | null;
        if (!live) return;
        if (!r.ok || !d || !Array.isArray(d.stages) || !d.waterfall) {
          setWfLoadErr(`Could not load the waterfall (HTTP ${r.status}) — showing nothing rather than another entity's split.`);
          return;
        }
        setWf(d);
        setWfDraft(Object.fromEntries(d.stages.map(s => [s, Math.round((d.waterfall[s] ?? 0) * 100)])));
      }).catch(() => { if (live) setWfLoadErr("Could not load the waterfall — showing nothing rather than another entity's split."); });
    return () => { live = false; };
  }, [entity, vsbId]);

  const wfDraftSum = Object.values(wfDraft).reduce((a, b) => a + (Number(b) || 0), 0);

  const saveWaterfall = async () => {
    setWfSaving(true); setWfMsg(''); setWfErr([]);
    try {
      const proportions = Object.fromEntries(Object.entries(wfDraft).map(([k, v]) => [k, (Number(v) || 0) / 100]));
      const r = await fetch('/api/v1/economy/waterfall', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vsb_id: vsbId, entity_type: entity, proportions }),
      });
      const d = await r.json();
      if (!r.ok) { setWfErr((d?.detail?.violations) || [`HTTP ${r.status}`]); setWfSaving(false); return; }
      setWf(prev => prev ? { ...prev, waterfall: d.waterfall, source: d.source } : prev);
      setWfDraft(Object.fromEntries(Object.entries(d.waterfall as Record<string, number>).map(([k, v]) => [k, Math.round(v * 100)])));
      setWfMsg('Saved — effective from the next cycle (virtual; logged to the UEG).');
    } catch (e: any) { setWfErr([e?.message ?? String(e)]); }
    setWfSaving(false);
  };

  const selected = types.find(t => t.id === entity);

  const runCycle = async () => {
    setRunning(true); setError('');
    try {
      const r = await fetch('/api/v1/economy/cycle', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vsb_id: vsbId, entity_type: entity, revenue, costs }),
      });
      if (!r.ok) {
        // W468 — the server says why (e.g. a ledger that could not be read, and that nothing was posted); a bare status hid it
        const fail = await r.json().catch(() => null);
        // a refused input (422) carries a list of reasons, not a string
        const reasons = Array.isArray(fail?.detail)
          ? fail.detail.map((d: any) => d?.msg && `${Array.isArray(d.loc) && d.loc.length ? `${d.loc[d.loc.length - 1]}: ` : ''}${d.msg}`)
            .filter(Boolean).join('; ') : '';
        const why = typeof fail?.detail === 'string' ? fail.detail : reasons ? `No cycle ran — ${reasons}.` : '';
        setError(why || `HTTP ${r.status}`); setRunning(false); return;
      }
      const d = await r.json();
      setCycle(d.cycle); setGov(d.governance?.status ?? '');
      setHold(d.cycle == null ? (d.governance ?? { status: 'no_cycle', note: 'The cycle returned no result.' }) : null);
      loadOwnerPay();   // refresh the ledger (the cycle's report says whether the Owner's §4 share was recorded)
      loadBoardPack();  // refresh the live financial Board Pack
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  // W442 — §9.1 period close existed server-side with no surface: cumulative P&L figures grew
  // forever with no "books closed" moment, and the CFO's three statements shipped in the board
  // pack but rendered nowhere.
  const [closing, setClosing] = useState(false);
  const [closeMsg, setCloseMsg] = useState('');
  const [closeErr, setCloseErr] = useState('');
  const doClosePeriod = async () => {
    setClosing(true); setCloseMsg(''); setCloseErr('');
    try {
      const r = await fetch('/api/v1/economy/close-period', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vsb_id: vsbId }),
      });
      const d = await r.json();
      if (!r.ok) { setCloseErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setClosing(false); return; }
      setCloseMsg(`Books closed — net profit ${(d.close?.net_profit_wst ?? 0).toLocaleString()} WST → retained earnings ${(d.retained_earnings_wst ?? 0).toLocaleString()} WST. `
        + `Next period starts clean.${d.ueg_logged ? ' UEG-logged.' : ' (UEG event did NOT land — logging was unavailable.)'}`);
      loadBoardPack();
    } catch (e: any) { setCloseErr(e?.message ?? String(e)); }
    setClosing(false);
  };

  const doPayout = async () => {
    setPayingOut(true); setPayMsg(''); setPayErr('');
    try {
      const r = await fetch('/api/v1/economy/owner-payments/payout', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vsb_id: vsbId, amount: payoutAmt }),
      });
      const d = await r.json();
      if (!r.ok) { setPayErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setPayingOut(false); return; }
      setPayMsg(`Virtual payout recorded — no real money moved. Remaining ${d.remaining_balance_wst.toLocaleString()} WST.`);
      setPayoutAmt(0); loadOwnerPay();
    } catch (e: any) { setPayErr(e?.message ?? String(e)); }
    setPayingOut(false);
  };

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">VSB · Living Economy</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Economic Metabolism</h1>
        {loadErr && (
          <p role="alert" className="text-[10px] font-bold text-vital mt-2">{loadErr}</p>
        )}
        {bpLoadErr && (
          <p role="alert" className="text-[10px] font-bold text-vital mt-2" data-testid="board-pack-error">{bpLoadErr}</p>
        )}
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The VSB's value flows like a <span className="text-highlight">biogeochemical nutrient cycle</span> — intake →
          homeostasis → circulation → giving-back → storage → growth. A hybrid Waqf/Trust/Multinational entity that pays
          you, reinvests, funds users, and donates intelligently. <span className="text-amber-400">All flows are virtual/simulated WST — no real money moves.</span>
        </p>
      </header>

      {/* W298 — WHICH entity's economy: the workstation apex or any established living VSB */}
      <Card className="p-5">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Entity</span>
          <select value={vsbId} onChange={e => setVsbId(e.target.value)} disabled={running || payingOut || closing || wfSaving || transferring}
            title={running || payingOut || closing || wfSaving || transferring ? 'Wait for the running action to finish before switching entity.' : undefined}
            className="text-xs bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-highlight/50">
            <option value="workstation-idbo">Workstation IDBO (apex)</option>
            {((living?.living_vsbs) ?? []).map((v: any) => (
              <option key={v.vsb_id} value={v.vsb_id}>{v.name || v.vsb_id}</option>
            ))}
          </select>
          <span className="text-[9px] text-slate-500">cycles · waterfall · owner payments · board pack all follow this selection (virtual WST)</span>
        </div>
      </Card>

      {/* Entity-type selection */}
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2"><Building2 size={14} /> Legal / Economic Form</h3>
        <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-3">
          {types.map(t => (
            <button key={t.id} type="button" onClick={() => setEntity(t.id)}
              className={`text-left p-4 rounded-2xl border transition-all ${entity === t.id ? 'bg-highlight/10 border-highlight/50' : 'bg-slate-900 border-slate-800 hover:border-slate-700'}`}>
              <p className="font-black text-white text-sm">{t.name}</p>
              <p className="text-[10px] text-slate-500 leading-relaxed mt-1">{t.description}</p>
              <div className="flex gap-1.5 mt-2">
                {t.capital_preserved && <span className="px-2 py-0.5 rounded-md bg-aura/10 text-aura text-[8px] font-black uppercase">capital preserved</span>}
                {!t.distributes_profit && <span className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-400 text-[8px] font-black uppercase">non-profit</span>}
              </div>
            </button>
          ))}
        </div>
      </Card>

      {/* §4/§8/§10 — Owner-adjustable profit-distribution waterfall (virtual, template-bounded) */}
      {wfLoadErr && (
        <p role="alert" className="text-[10px] font-bold text-vital" data-testid="waterfall-error">{wfLoadErr}</p>
      )}
      {wf && (
        <Card className="p-6">
          <div className="flex items-center justify-between gap-3 flex-wrap mb-1">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><PiggyBank size={14} /> Profit-Distribution Waterfall · Owner-adjustable</h3>
            <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${wf.source === 'owner_override' ? 'bg-highlight/15 text-highlight' : 'bg-slate-800 text-slate-400'}`}>
              {wf.source === 'owner_override' ? 'owner-set' : 'template default'}
            </span>
          </div>
          <p className="text-[10px] text-slate-500 font-bold mb-4">
            Proportions of distributable profit (after reserves). Adjust and save — the next cycle uses your split.
            {wf.constraints.capital_preserved && <span className="text-aura"> · this form preserves capital (capital fund must be &gt; 0)</span>}
            {!wf.constraints.distributes_profit && <span className="text-amber-400"> · this form distributes no owner profit (owner must be 0)</span>}
          </p>
          <div className="grid grid-cols-2 @[560px]:grid-cols-5 gap-3">
            {(wf.stages || []).map(s => {
              const Icon = STAGE_ICON[s] ?? Coins;
              return (
                <div key={s} className="p-3 rounded-2xl bg-slate-900 border border-slate-800">
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-1.5 mb-2"><Icon size={11} className="text-highlight" /> {STAGE_LABEL[s] ?? s}</p>
                  <div className="flex items-center gap-1">
                    <input type="number" min={0} max={100} value={wfDraft[s] ?? 0}
                      onChange={e => setWfDraft({ ...wfDraft, [s]: Number(e.target.value) })}
                      aria-label={`${STAGE_LABEL[s] ?? s} percent`}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm text-white font-black focus:outline-none focus:border-highlight/50" />
                    <span className="text-[10px] font-black text-slate-600">%</span>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="flex items-center justify-between gap-3 flex-wrap mt-4">
            <span className={`text-[10px] font-black uppercase tracking-widest ${Math.abs(wfDraftSum - 100) < 0.5 ? 'text-emerald-400' : 'text-slate-500'}`}>
              sum {wfDraftSum}% {Math.abs(wfDraftSum - 100) >= 0.5 && <span className="text-slate-600 normal-case">(will be normalised to 100%)</span>}
            </span>
            <Button onClick={saveWaterfall} disabled={wfSaving} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
              {wfSaving ? <Loader2 size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
              {wfSaving ? 'Saving…' : 'Save proportions'}
            </Button>
          </div>
          {wfMsg && <p className="text-emerald-400 text-[10px] font-bold mt-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {wfMsg}</p>}
          {wfErr.length > 0 && (
            <div className="mt-2 space-y-1">
              {wfErr.map((v, i) => <p key={i} className="text-vital text-[10px] font-bold flex items-center gap-1.5"><AlertCircle size={12} /> {v}</p>)}
            </div>
          )}
        </Card>
      )}

      {/* Cycle controls */}
      <Card className="p-8 space-y-6">
        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-6">
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Revenue (WST, virtual)</label>
            <input type="number" value={revenue} onChange={e => setRevenue(Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-highlight/50" />
          </div>
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Costs (WST, virtual)</label>
            <input type="number" value={costs} onChange={e => setCosts(Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-highlight/50" />
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Button onClick={runCycle} disabled={running} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <HeartPulse size={16} />}
            {running ? 'Cycling…' : 'Run Metabolic Cycle'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {/* §7 — Owner-Payments ledger (virtual; real rails disabled + gated) */}
      {payLoadErr && (
        <p role="alert" className="text-[10px] font-bold text-vital" data-testid="owner-payments-error">{payLoadErr}</p>
      )}
      {pay && (
        <Card className="p-6">
          <div className="flex items-center justify-between gap-3 flex-wrap mb-4">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><Coins size={14} /> Owner Payments · your accrued share (§7)</h3>
            <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-amber-500/15 text-amber-400" title="Real-money payout rails are disabled and gated until you authorise them + a compliance/KYC review passes.">real rails: {pay.real_money_rails}</span>
          </div>
          <div className="grid grid-cols-3 gap-3 text-center">
            <Metric label="Accrued (total)" value={`${(pay.accrued_total_wst ?? 0).toLocaleString()} WST`} />
            <Metric label="Paid out (virtual)" value={`${(pay.paid_out_total_wst ?? 0).toLocaleString()} WST`} />
            <Metric label="Balance" value={`${(pay.balance_wst ?? 0).toLocaleString()} WST`} tone="good" />
          </div>
          <div className="flex items-end gap-3 mt-5 flex-wrap">
            <div className="flex-1 min-w-[160px]">
              <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Virtual payout (WST)</label>
              <input type="number" min={0} value={payoutAmt} onChange={e => setPayoutAmt(Number(e.target.value))}
                aria-label="Virtual payout amount"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-highlight/50" />
            </div>
            <Button onClick={doPayout} disabled={payingOut || payoutAmt <= 0} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
              {payingOut ? <Loader2 size={14} className="animate-spin" /> : <Coins size={14} />}
              {payingOut ? 'Recording…' : 'Record virtual payout'}
            </Button>
          </div>
          <p className="text-[9px] text-amber-400/80 italic mt-2">{pay.note}</p>
          {payMsg && <p className="text-emerald-400 text-[10px] font-bold mt-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {payMsg}</p>}
          {payErr && <p className="text-vital text-[10px] font-bold mt-2 flex items-center gap-1.5"><AlertCircle size={12} /> {payErr}</p>}
          {pay.entries && pay.entries.length > 0 && (
            <div className="mt-4 space-y-1.5">
              <p className="text-[9px] font-black uppercase tracking-widest text-slate-600">Recent entries</p>
              {pay.entries.slice(0, 6).map((e: any) => (
                <div key={e.id} className="flex items-center justify-between p-2 rounded-lg bg-slate-950 border border-slate-900 text-[10px]">
                  <span className={`font-black uppercase ${e.type === 'accrual' ? 'text-emerald-400' : 'text-amber-400'}`}>{e.type === 'accrual' ? 'accrual' : 'payout (virtual)'}</span>
                  <span className="text-slate-400 truncate px-2 flex-1">{e.memo}</span>
                  <span className="font-mono text-slate-300 shrink-0">{e.amount_wst.toLocaleString()} WST</span>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Governance hold — a material distribution awaiting Owner approval (rendered FIRST:
          this is the branch the Owner must see, not a silent no-op). */}
      {hold && (
        <Card className={`p-6 ${['blocked', 'halted'].includes(hold.status || '') ? 'border-vital/40' : 'border-amber-500/40'}`}>
          {/* W442 refuter catch: every non-null hold rendered "Held for Change Control — Owner
              approval required", including a constitutional-gate BLOCK (no CCA request exists,
              approval releases nothing) and a Change Control REJECTION (the note contradicted
              the header). The three verdicts now say what they mean. */}
          <p className={`text-[10px] font-black uppercase tracking-widest flex items-center gap-2 ${['blocked', 'halted'].includes(hold.status || '') ? 'text-vital' : 'text-amber-400'}`}>
            <ShieldCheck size={14} /> {['blocked', 'halted'].includes(hold.status || '')
              ? `Blocked by the constitutional gate (${hold.status}) — nothing ran, nothing posted`
              : hold.status === 'rejected_by_change_control' ? 'Rejected by Change Control — asked again when the action changes'
              // W464 (refutation) — no decision is pending in these two cases: never send the Owner to decide one
              : hold.decided_concurrently ? 'Held — the change request was decided while this cycle ran; run it again'
              : !hold.cca_id ? 'Held — the governance check could not complete; nothing ran'
              : 'Held for Change Control — awaiting the Owner\'s decision'}
          </p>
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">{hold.note || 'This distribution is material: no WST moves until the Owner approves it in the Sovereign Sanctum.'}</p>
          {hold.cca_id && (hold.decided_concurrently ? (
            <p className="text-[10px] font-mono text-slate-500 mt-2" data-testid="hold-decided-concurrently">
              Change request: <span className="text-aura">{hold.cca_id}</span> — decided while this cycle ran. Run the cycle again.
            </p>
          ) : hold.status === 'rejected_by_change_control' ? (
            // W463 — a rejected record cannot be reviewed: the same cycle stays refused; a changed one is asked again
            <p className="text-[10px] font-mono text-slate-500 mt-2" data-testid="hold-rejected">
              {/* W463 — a rejection is not always the Owner's: say what rejected it */}
              Change request: <span className="text-aura">{hold.cca_id}</span> — rejected {hold.rejected_by === 'admin_override' ? 'by an explicit decision'
                : hold.rejected_by === 'model_decision_marker' ? "by the reviewing model's decision marker"
                : hold.rejected_by === 'health_threshold_rule' ? 'by the organism-health threshold rule' : 'by Change Control'} for exactly this action. Running the same
              cycle again is refused; a different amount or new intake is asked again as a fresh hold.
            </p>
          ) : hold.follows_rejection ? (
            // W463 — a hold filed after a rejection says so. W464: every material hold is decided only by the Owner
            <p className="text-[10px] font-mono text-slate-500 mt-2" data-testid="hold-follows-rejection">
              Change request: <span className="text-aura">{hold.cca_id}</span> — it follows the rejection of {hold.follows_rejection}.
              Only your explicit decision decides it: decide it in the{' '}
              <a href="/governance-hub" className="text-aura underline underline-offset-2">Governance hub's Sovereign Sanctum</a>, then run the cycle again.
            </p>
          ) : (
            // W464 (FU-014) — a material distribution is CRITICAL: a review never decides it, so the page no longer sends
            // the Owner to request one
            <p className="text-[10px] font-mono text-slate-500 mt-2" data-testid="hold-held-sanctum">
              Change request: <span className="text-aura">{hold.cca_id}</span> — a material distribution is decided only by your
              explicit decision: decide it in the{' '}
              <a href="/governance-hub" className="text-aura underline underline-offset-2">Governance hub's Sovereign Sanctum</a>, then run the cycle again.
            </p>
          ))}
        </Card>
      )}

      {/* Cycle result */}
      {cycle && (
        <div className="space-y-6">
          <Card className="p-6">
            <div className="grid grid-cols-2 @[560px]:grid-cols-5 gap-3 text-center">
              <Metric label="Intake (revenue)" value={cycle.intake_revenue} />
              {/* W475 (ledger v4 R6.1) — costs are an expense posted on their own; the reserve is revenue x rate only
                  (W377 labelled one figure 'Costs + reserves' when both were posted to the reserve fund). */}
              <Metric label="Operating costs" value={cycle.operating_costs ?? 0} />
              <Metric label="Reserve" value={cycle.homeostasis_reserves} />
              <Metric label="Distributable" value={cycle.distributable_profit} tone="good" />
              <Metric label="Metabolic Energy" value={cycle.metabolic_energy != null ? `${Math.round(cycle.metabolic_energy * 100)}%` : '—'} tone="good" />
            </div>
            {cycle.energy_state && cycle.energy_state !== 'healthy' && (
              <p className="text-[9px] font-black uppercase tracking-widest text-amber-400 mt-2" title="§8→§12 — the living organism's energy is low, so the economic organism conserves more (raises reserves).">
                §8→§12 survival instinct: {cycle.energy_state}{cycle.reserve_rate_applied != null ? ` · reserve ${Math.round(cycle.reserve_rate_applied * 100)}%` : ''}
              </p>
            )}
            <p className="text-[9px] font-mono text-slate-600 mt-3 flex items-center gap-2"><ShieldCheck size={11} className={gov === 'allowed' ? 'text-emerald-400' : gov ? 'text-amber-400' : 'text-slate-500'} /> governance: {gov} · {cycle.biogeochemical_model}</p>
            {cycle.owner_accrual && cycle.owner_accrual.accrued === false && cycle.owner_accrual.error && (
              <p role="alert" data-testid="owner-accrual-failed" className="text-[10px] font-bold text-vital mt-2">
                The owner share of {cycle.owner_accrual.amount_wst.toLocaleString()} WST was distributed but NOT recorded in Owner
                Payments ({cycle.owner_accrual.error}) — your balance is short by this amount
                {cycle.owner_accrual.ueg_logged === true
                  ? ' (logged on the constitutional ledger).'
                  : ' (the ledger entry did not land either — see the server log).'}
              </p>
            )}
          </Card>

          {/* Circulation waterfall */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Activity size={14} /> Circulation — the distribution waterfall</h3>
            <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-3">
              {Object.entries(cycle.circulation).map(([stage, v]) => {
                const Icon = STAGE_ICON[stage] ?? Coins;
                return (
                  <div key={stage} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex items-start gap-3">
                    <div className="w-9 h-9 rounded-xl bg-highlight/10 flex items-center justify-center shrink-0"><Icon size={15} className="text-highlight" /></div>
                    <div className="min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <p className="font-black text-white text-sm">{STAGE_LABEL[stage] ?? stage}</p>
                        <p className="font-black text-highlight text-sm">{v.amount_wst.toLocaleString()} <span className="text-[9px] text-slate-500">WST</span></p>
                      </div>
                      <p className="text-[10px] text-slate-500 italic mt-0.5">≈ {v.role}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Charity grants (the nutrient-return loop) */}
          {cycle.giving_back && cycle.giving_back.grants.length > 0 && (
            <Card className="p-6 border-aura/30 bg-aura/5">
              <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-4 flex items-center gap-2"><Gift size={14} /> Intelligent Charitable Giving (nutrient-return loop)</h3>
              <div className="space-y-2">
                {cycle.giving_back.grants.map((g, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-900">
                    <div className="flex items-center gap-3">
                      <Recycle size={13} className="text-aura" />
                      <span className="text-sm text-slate-300 font-bold">{g.cause}</span>
                    </div>
                    <div className="flex items-center gap-3 text-[10px] font-mono">
                      <span className="text-slate-600">score {g.score}</span>
                      <span className="text-aura font-black">{g.amount_wst.toLocaleString()} WST</span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-[9px] text-slate-600 mt-3">Ranked by urgency × gravity × reach × marginal-impact × trust. Virtual/simulated — live feeds pending Owner approval.</p>
            </Card>
          )}
        </div>
      )}

      {/* §7 — Financial Board Pack (the capstone live statement) */}
      {bp && (
        <Card className="p-6 border-highlight/20">
          <div className="flex items-center justify-between gap-3 flex-wrap mb-4">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><Building2 size={14} /> Financial Board Pack (§7) · {bp.entity_name}</h3>
            <button type="button" onClick={loadBoardPack} disabled={bpLoading} className="text-[9px] font-black uppercase tracking-widest text-slate-500 hover:text-white flex items-center gap-1.5">
              {bpLoading ? <Loader2 size={11} className="animate-spin" /> : <Recycle size={11} />} refresh
            </button>
          </div>
          <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3 text-center">
            <Metric label="Revenue (cumulative)" value={`${(bp.profit_and_loss?.total_revenue_wst ?? 0).toLocaleString()} WST`} />
            <Metric label="Reserves" value={`${(bp.profit_and_loss?.total_reserves_wst ?? 0).toLocaleString()} WST`} />
            <Metric label="Distributed" value={`${(bp.profit_and_loss?.total_distributed_wst ?? 0).toLocaleString()} WST`} tone="good" />
            <Metric label="Owner balance" value={bp.owner_payments?.available === false ? 'unavailable' : `${(bp.owner_payments?.balance_wst ?? 0).toLocaleString()} WST`} tone={bp.owner_payments?.available === false ? undefined : 'good'} />
          </div>
          <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-3 mt-3">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">Venture portfolio (§6)</p>
              <p className="text-sm font-black text-white">{(bp.venture_portfolio?.invested_total_wst ?? 0).toLocaleString()} WST <span className="text-[9px] text-slate-500">· {bp.venture_portfolio?.positions ?? 0} positions</span></p>
              {(bp.venture_portfolio?.holdings ?? []).slice(0, 3).map((h: any) => (
                <p key={h.id} className="text-[9px] text-slate-500 truncate mt-0.5">{h.name} · {h.invested_wst.toLocaleString()} WST</p>
              ))}
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">Charitable giving (§5)</p>
              <p className="text-sm font-black text-aura">{(bp.charitable_giving?.total_given_wst ?? 0).toLocaleString()} WST</p>
              <p className="text-[9px] text-slate-600 mt-0.5">nutrient-return loop</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">§8 organism posture</p>
              <p className="text-sm font-black text-white capitalize">{bp.organism_posture?.mode ?? '—'}</p>
              <p className="text-[9px] text-slate-500 mt-0.5">ATP {bp.organism_posture?.atp_ratio != null ? `${Math.round(bp.organism_posture.atp_ratio * 100)}%` : '—'} · health {bp.organism_posture?.composite_health != null ? `${Math.round(bp.organism_posture.composite_health * 100)}%` : '—'}</p>
            </div>
          </div>
          {/* W442 — §9.1: the CFO's current-period statements (real double-entry postings) + the
              period-close act itself, previously API-only. */}
          {bp.statements && (
            <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-3 mt-3">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">P&L · this period</p>
                <p className="text-sm font-black text-white">{(bp.statements.profit_and_loss?.net_profit_wst ?? 0).toLocaleString()} WST <span className="text-[9px] text-slate-500">net</span></p>
                <p className="text-[9px] text-slate-500 mt-0.5">income {(bp.statements.profit_and_loss?.total_income_wst ?? 0).toLocaleString()} · expenses {(bp.statements.profit_and_loss?.total_expenses_wst ?? 0).toLocaleString()}</p>
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">Balance sheet</p>
                <p className="text-sm font-black text-white">{(bp.statements.balance_sheet?.assets_total_wst ?? 0).toLocaleString()} WST <span className="text-[9px] text-slate-500">assets</span></p>
                <p className={`text-[9px] mt-0.5 ${bp.statements.balance_sheet?.balanced ? 'text-emerald-400' : 'text-vital'}`}>{bp.statements.balance_sheet?.balanced ? 'balanced' : 'NOT balanced'} · {bp.statements.trial_balance?.postings ?? 0} postings</p>
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mb-1">Cash flow · this period</p>
                <p className="text-sm font-black text-white">{(bp.statements.cash_flow?.net_cash_movement_wst ?? 0).toLocaleString()} WST <span className="text-[9px] text-slate-500">net</span></p>
                <p className="text-[9px] text-slate-500 mt-0.5">period {bp.statements.period?.opened_after_close ?? 0} · {bp.statements.period?.postings ?? 0} postings</p>
              </div>
            </div>
          )}
          <div className="flex items-center gap-3 flex-wrap mt-4">
            <Button onClick={doClosePeriod} disabled={closing} className="flex items-center gap-2 bg-slate-800 text-white text-xs">
              {closing ? <Loader2 size={14} className="animate-spin" /> : <PiggyBank size={14} />}
              {closing ? 'Closing…' : 'Close period (CFO)'}
            </Button>
            <span className="text-[9px] text-slate-600">rolls this period's income/expenses into retained earnings — the next period starts clean (virtual)</span>
          </div>
          {closeMsg && <p className="text-emerald-400 text-[10px] font-bold mt-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {closeMsg}</p>}
          {closeErr && <p className="text-vital text-[10px] font-bold mt-2 flex items-center gap-1.5"><AlertCircle size={12} /> {closeErr}</p>}
          <p className="text-[9px] font-mono text-slate-600 mt-3 flex items-center gap-2"><ShieldCheck size={11} className="text-slate-500" /> {bp.governance}</p>
          <p className="text-[9px] text-amber-400/80 italic mt-1">{bp.disclaimer}</p>
        </Card>
      )}

      {/* W442 — §6: the venture portfolio + the return half of the recycle loop (previously the
          board pack truncated to 3 invested-only names and no surface could record a return). */}
      <VenturePortfolioPanel vsbId={vsbId} />

      {/* W442 — the governed federation transfer primitive, Owner-initiated (previously reachable
          only via contract settlement). Rendered always: the honest empty state names the
          precondition (a registered living receiver). */}
      <TransferPanel key={vsbId} fromVsb={vsbId} entities={(living?.living_vsbs ?? []).map((v: any) => ({ vsb_id: v.vsb_id, name: v.name }))}
        onDone={() => { loadBoardPackRef.current(); }} onBusyChange={setTransferring} />

      {/* W472 (P1.15) — a roster or a compliance history that could not be read whole is SAID here, never an empty list */}
      {living?.roster_unavailable && (
        <Card className="p-6 border-amber-500/40">
          <p className="text-[10px] font-black uppercase tracking-widest text-amber-400 mb-1" data-testid="roster-unavailable">Living roster unavailable</p>
          <p className="text-[11px] text-slate-400 leading-relaxed">{living.roster_unavailable}. No entity is tended and nothing is written to the roster until it can be read whole.</p>
        </Card>
      )}
      {living?.history_unavailable && (
        <p className="text-[10px] text-amber-400/90 font-bold" data-testid="history-unavailable">Compliance history unavailable — {living.history_unavailable}. Each entity's standing is unknown, not clean; no cycle runs until it can be read whole.</p>
      )}
      {/* §4 — living enterprises the organism autonomously tends (continually operated on the heartbeat) */}
      {living && (living.living_vsbs?.length ?? 0) > 0 && (
        <Card className="p-6">
          <div className="flex items-center justify-between gap-3 flex-wrap mb-1">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><HeartPulse size={14} className="text-emerald-400" /> Living Enterprises · the living roster (§4)</h3>
            <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400">{living.total} living</span>
          </div>
          {/* W475 (ledger v4 R2.0) — the present tense only while the heartbeat's Self-run lever is on */}
          {living.autonomous_cycles === false
            ? <p className="text-[10px] text-amber-400 font-bold mb-4">{living.autonomous_cycles_note || 'Autonomous economy cycles are OFF — enable Self-run on the Heartbeat page.'} These enterprises are registered; none is being operated until the lever is on.</p>
            : <p className="text-[10px] text-slate-500 font-bold mb-4">Established VSB IDBO enterprises the organism operates on the circadian heartbeat — each runs paced virtual economy cycles, led by its Chief.</p>}
          <div className="space-y-2">
            {(living.living_vsbs || []).slice(0, 8).map((v: any) => (
              <div key={v.vsb_id} className="flex items-center justify-between gap-3 p-3 rounded-xl bg-slate-950 border border-slate-900">
                <div className="min-w-0">
                  <p className="text-sm font-black text-white truncate">{v.name}</p>
                  <p className="text-[9px] font-mono text-slate-600">{v.vsb_id} · {v.entity_type} · {v.domain}</p>
                </div>
                <div className="text-right shrink-0">
                  <p className="text-sm font-black text-emerald-400">{v.operating_cycles} <span className="text-[9px] text-slate-500">cycles</span></p>
                  <p className="text-[8px] text-slate-600">{v.last_operated ? `last ${v.last_operated.slice(0, 10)}` : 'awaiting first tick'}</p>
                  {/* §11 × §13 (W421) — the compliance verdict and the economic consequence it causes,
                      where the entity's OWNER can see them. Both existed only as side effects: the
                      hold was written to the store and the UEG, so a held enterprise looked idle. */}
                  <div className="flex items-center gap-1 justify-end mt-1">
                    {v.economy_held?.held && (
                      <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-vital/15 text-vital"
                        title={v.economy_held.consequence || 'this entity is held'}>
                        held · {String(v.economy_held.reason).replace(/_/g, ' ')}
                      </span>
                    )}
                    {/* W468 — a heartbeat visit that raised advances the rotation; without this it looked freshly tended */}
                    {v.economy_held?.last_visit_error && (
                      <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-400"
                        title={`The last heartbeat visit raised: ${v.economy_held.last_visit_error}`} data-testid="living-visit-error">
                        last visit failed
                      </span>
                    )}
                    {v.compliance?.never_screened ? (
                      <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-500"
                        title="§11 has not screened this entity yet. Switch on Self-defend (auto_compliance) on the Heartbeat surface to re-screen every entity each beat. Not screened is NOT the same as clean.">
                        not screened
                      </span>
                    ) : (
                      <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${v.compliance?.verdict === 'fail' ? 'bg-vital/15 text-vital' : v.compliance?.verdict === 'review' ? 'bg-amber-500/15 text-amber-400' : v.compliance?.verdict === 'pass' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500'}`}
                        title={`§11 — ${(v.compliance?.verdicts || []).map((x: any) => `${x.framework}:${x.status}`).join(' · ') || 'no framework detail recorded'}${v.compliance?.screened_at ? `
screened ${v.compliance.screened_at}` : ''}`}>
                        §11 {v.compliance?.verdict}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          {/* W460 — the list shows eight; the rest used to vanish with no status and no word */}
          {(living.living_vsbs || []).length > 8 && (
            <p className="text-[9px] text-slate-500 font-bold mt-2">{(living.living_vsbs || []).length - 8} more living entities are not shown here, so their §11 status is not shown either.</p>
          )}
          <p className="text-[9px] text-amber-400/80 italic mt-3">{living.note}</p>
        </Card>
      )}

      {/* §15 (W394) — entity-to-entity service contracts. The lifecycle existed server-side since
          W330 with no UI, so none of it was reachable from the product. */}
      <ServiceContracts entities={(living?.living_vsbs ?? []).map((v: any) => ({ vsb_id: v.vsb_id, name: v.name }))} />

      {/* §5 (W397) — the Owner's charity directives had GET/POST endpoints and no UI, so the
          priorities governing a whole waterfall stage were visible only to code. */}
      <CharityDirectives />
    </div>
  );
};

const Metric: React.FC<{ label: string; value: any; tone?: 'good' }> = ({ label, value, tone }) => (
  <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
    <p className={`text-xl font-black ${tone === 'good' ? 'text-emerald-400' : 'text-white'}`}>{typeof value === 'number' ? value.toLocaleString() : value}</p>
    <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mt-1">{label}</p>
  </div>
);
