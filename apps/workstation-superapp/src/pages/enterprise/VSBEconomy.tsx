import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import {
  Coins, Recycle, Activity, Sprout, Building2, PiggyBank,
  Loader2, AlertCircle, HeartPulse, ShieldCheck, Gift,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface EntityType {
  id: string; name: string; description: string;
  distributes_profit: boolean; capital_preserved: boolean; waterfall: Record<string, number>;
}
interface Cycle {
  intake_revenue: number; homeostasis_reserves: number; distributable_profit: number;
  circulation: Record<string, { amount_wst: number; role: string }>;
  giving_back: { grants: { cause: string; amount_wst: number; score: number }[] } | null;
  metabolic_energy: number | null; entity_name: string; capital_preserved: boolean;
  energy_state?: string; reserve_rate_applied?: number;   // §8→§12 economic survival instinct
  biogeochemical_model: string;
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
  const [entity, setEntity] = useState('waqf_ltd_hybrid');
  const [revenue, setRevenue] = useState(10000);
  const [costs, setCosts] = useState(1000);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [cycle, setCycle] = useState<Cycle | null>(null);
  const [gov, setGov] = useState<string>('');
  // §4/§8/§10 — Owner-adjustable profit waterfall (virtual, template-bounded)
  const [wf, setWf] = useState<WaterfallState | null>(null);
  const [wfDraft, setWfDraft] = useState<Record<string, number>>({});   // percentages (0-100) the Owner edits
  const [wfSaving, setWfSaving] = useState(false);
  const [wfMsg, setWfMsg] = useState('');
  const [wfErr, setWfErr] = useState<string[]>([]);
  // §7 — Owner-payments ledger (virtual; real rails disabled+gated)
  const [pay, setPay] = useState<any>(null);
  const [payoutAmt, setPayoutAmt] = useState(0);
  const [payingOut, setPayingOut] = useState(false);
  const [payMsg, setPayMsg] = useState('');
  const [payErr, setPayErr] = useState('');

  const loadOwnerPay = () =>
    fetch(`/api/v1/economy/owner-payments?vsb_id=${encodeURIComponent(vsbId)}`)
      .then(r => r.json()).then(setPay).catch(() => {});
  // §7 — the live financial Board Pack (capstone statement)
  const [bp, setBp] = useState<any>(null);
  const [bpLoading, setBpLoading] = useState(false);
  const loadBoardPack = () => {
    setBpLoading(true);
    fetch(`/api/v1/economy/board-pack?vsb_id=${encodeURIComponent(vsbId)}&entity_type=${entity}`)
      .then(r => r.json()).then(setBp).catch(() => {}).finally(() => setBpLoading(false));
  };
  // §4 — the established living VSB enterprises the organism autonomously tends
  const [living, setLiving] = useState<any>(null);
  const loadLiving = () =>
    fetch('/api/v1/economy/living-vsbs').then(r => r.json()).then(setLiving).catch(() => {});

  useEffect(() => {
    fetch('/api/v1/economy/entity-types').then(r => r.json()).then(d => setTypes(d.types ?? [])).catch(() => {});
    loadOwnerPay();
    loadBoardPack();
    loadLiving();
  }, []);

  // W298 - the scoped ledgers follow the selected entity
  useEffect(() => { loadOwnerPay(); loadBoardPack(); }, [vsbId]);

  // Load the effective waterfall whenever the entity form changes (per VSB = workstation-idbo).
  useEffect(() => {
    setWfMsg(''); setWfErr([]);
    fetch(`/api/v1/economy/waterfall?vsb_id=${encodeURIComponent(vsbId)}&entity_type=${entity}`)
      .then(r => r.json()).then((d: WaterfallState) => {
        setWf(d);
        setWfDraft(Object.fromEntries((d.stages || []).map(s => [s, Math.round((d.waterfall[s] ?? 0) * 100)])));
      }).catch(() => {});
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
      if (!r.ok) { setError(`HTTP ${r.status}`); setRunning(false); return; }
      const d = await r.json();
      setCycle(d.cycle); setGov(d.governance?.status ?? '');
      loadOwnerPay();   // the cycle accrued the Owner's §4 share — refresh the ledger
      loadBoardPack();  // refresh the live financial Board Pack
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
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
          <select value={vsbId} onChange={e => setVsbId(e.target.value)}
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

      {/* Cycle result */}
      {cycle && (
        <div className="space-y-6">
          <Card className="p-6">
            <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3 text-center">
              <Metric label="Intake (revenue)" value={cycle.intake_revenue} />
              <Metric label="Reserves (homeostasis)" value={cycle.homeostasis_reserves} />
              <Metric label="Distributable" value={cycle.distributable_profit} tone="good" />
              <Metric label="Metabolic Energy" value={cycle.metabolic_energy != null ? `${Math.round(cycle.metabolic_energy * 100)}%` : '—'} tone="good" />
            </div>
            {cycle.energy_state && cycle.energy_state !== 'healthy' && (
              <p className="text-[9px] font-black uppercase tracking-widest text-amber-400 mt-2" title="§8→§12 — the living organism's energy is low, so the economic organism conserves more (raises reserves).">
                §8→§12 survival instinct: {cycle.energy_state}{cycle.reserve_rate_applied != null ? ` · reserve ${Math.round(cycle.reserve_rate_applied * 100)}%` : ''}
              </p>
            )}
            <p className="text-[9px] font-mono text-slate-600 mt-3 flex items-center gap-2"><ShieldCheck size={11} className="text-emerald-400" /> governance: {gov} · {cycle.biogeochemical_model}</p>
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
            <Metric label="Owner balance" value={`${(bp.owner_payments?.balance_wst ?? 0).toLocaleString()} WST`} tone="good" />
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
          <p className="text-[9px] font-mono text-slate-600 mt-3 flex items-center gap-2"><ShieldCheck size={11} className="text-emerald-400" /> {bp.governance}</p>
          <p className="text-[9px] text-amber-400/80 italic mt-1">{bp.disclaimer}</p>
        </Card>
      )}

      {/* §4 — living enterprises the organism autonomously tends (continually operated on the heartbeat) */}
      {living && (living.living_vsbs?.length ?? 0) > 0 && (
        <Card className="p-6">
          <div className="flex items-center justify-between gap-3 flex-wrap mb-1">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><HeartPulse size={14} className="text-emerald-400" /> Living Enterprises · autonomously tended (§4)</h3>
            <span className="text-[8px] font-black uppercase px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400">{living.total} living</span>
          </div>
          <p className="text-[10px] text-slate-500 font-bold mb-4">Established VSB IDBO enterprises the organism operates continually on the circadian heartbeat — each runs paced virtual economy cycles, forever, led by its Chief.</p>
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
                </div>
              </div>
            ))}
          </div>
          <p className="text-[9px] text-amber-400/80 italic mt-3">{living.note}</p>
        </Card>
      )}
    </div>
  );
};

const Metric: React.FC<{ label: string; value: any; tone?: 'good' }> = ({ label, value, tone }) => (
  <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
    <p className={`text-xl font-black ${tone === 'good' ? 'text-emerald-400' : 'text-white'}`}>{typeof value === 'number' ? value.toLocaleString() : value}</p>
    <p className="text-[8px] font-black uppercase tracking-widest text-slate-600 mt-1">{label}</p>
  </div>
);
