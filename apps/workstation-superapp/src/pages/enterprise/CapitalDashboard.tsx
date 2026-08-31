import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { apiJson, errorMessage } from '../../lib/api';
import { Card, Button, Badge, notImplemented } from '@workstation/ui';
import {
  TrendingUp, ShieldAlert, PieChart, Activity,
  BarChart3, MessageCircle, AlertTriangle, RefreshCw,
  Globe, Wallet, Zap, Code
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, AreaChart, Area
} from 'recharts';

interface CapitalMetrics {
  balance: number;
  totalDeposited: number;
  unrealisedProfit: number;
  realisedProfit: number;
  riskScore: number;
  homeostasisStatus: 'stable' | 'minor_deviation' | 'major_deviation';
}

interface PortfolioStats {
  total_projects: number;
  by_stage: { concept: number; prototype: number; commercialise: number };
  by_realm: Record<string, number>;
  total_outputs: number;
  active: number;
  complete: number;
}

// The real capital fund, as /api/v1/fund/status reports it. Virtual WST by design.
interface FundStatus {
  total_capital: number;
  allocated: number;
  available: number;
  utilisation_pct: number;
  allocation_count: number;
  fund_health: string;
  currency?: string;
}

// The real governance change record, as GET /api/v1/cca reports it (change_control.py:_list_changes).
interface CcaChange {
  cca_id: string;
  title: string;
  change_type: string;
  impact_tier: string;
  status: string;
  submitted_by: string;
  submitted_at: string;
  decision?: string | null;
}

export const CapitalDashboard: React.FC = () => {
  const [portfolio, setPortfolio] = useState<PortfolioStats | null>(null);
  const [fund, setFund] = useState<FundStatus | null>(null);
  const [fundError, setFundError] = useState('');
  const [autonomousEnabled, setAutonomousEnabled] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'external' | 'crypto' | 'evolution'>('overview');
  const [changes, setChanges] = useState<CcaChange[] | null>(null);
  const [changesError, setChangesError] = useState('');

  // W405 — the block that used to be here computed "capital metrics" from PROJECT COUNTS:
  //   balance          = total_projects * 1000 + total_outputs * 250
  //   unrealisedProfit = by_stage.prototype * 500 + by_stage.concept * 100
  //   realisedProfit   = complete * 2500
  // under a comment reading "Map project counts to capital-metaphor metrics", and rendered the
  // results as "Portfolio Value $X" and "Unrealised Gain $X". A project count multiplied by an
  // arbitrary constant is not a balance, and putting a dollar sign in front of it does not make it
  // one. A real fund API existed the whole time and is used now.
  useEffect(() => {
    apiJson<FundStatus>("/api/v1/fund/status")
      .then(f => { setFund(f); setFundError(""); })
      .catch(e => setFundError(errorMessage(e)));

    axios.get<PortfolioStats>("/api/v1/projects/stats/summary", { validateStatus: () => true })
      .then(res => { if (res.status === 200) setPortfolio(res.data); })
      .catch(() => {});

    // W415 — the Evolution tab used to render two hardcoded "constitutional articles" (see below).
    // The real record of governance change is the Change Control Agency store, so read that.
    apiJson<{ changes: CcaChange[] }>("/api/v1/cca")
      .then(d => { setChanges(Array.isArray(d?.changes) ? d.changes : []); setChangesError(""); })
      .catch(e => { setChanges([]); setChangesError(errorMessage(e)); });
  }, []);

  return (
    <div className="space-y-10">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black text-white uppercase italic break-words">Sovereign Capital</h1>
          <p className="text-slate-500 font-bold tracking-widest uppercase text-xs mt-2">vΩ∞-CAPITAL-FUND | Global Investment Civilisation</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
            <Badge variant="outline" className="border-aura text-aura font-black">PHASE 3: EXTERNALLY INTEGRATED</Badge>
            <div className="flex items-center gap-2 bg-slate-900 px-4 py-2 rounded-2xl border border-slate-800">
                <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Semi-Autonomous</span>
                <button
                    type="button"
                    aria-label={`Toggle Semi-Autonomous mode: currently ${autonomousEnabled ? 'On' : 'Off'}`}
                    title={`Semi-Autonomous mode: ${autonomousEnabled ? 'On' : 'Off'}`}
                    onClick={() => setAutonomousEnabled(!autonomousEnabled)}
                    className={`w-10 h-5 rounded-full transition-colors relative ${autonomousEnabled ? 'bg-aura' : 'bg-slate-700'}`}
                >
                    <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${autonomousEnabled ? 'left-6' : 'left-1'}`} />
                </button>
            </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="flex gap-2 p-1 bg-slate-900/50 rounded-2xl border border-slate-800 w-fit">
        {[
            { id: 'overview', label: 'Overview', icon: PieChart },
            { id: 'external', label: 'External Markets', icon: Globe },
            { id: 'crypto', label: 'Real-Money Rails (gated)', icon: Wallet },
            { id: 'evolution', label: 'Evolution', icon: Code }
        ].map(tab => (
            <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === tab.id ? 'bg-aura text-slate-950 shadow-lg shadow-aura/20' : 'text-slate-500 hover:text-white'}`}
            >
                <tab.icon size={14} />
                {tab.label}
            </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Live portfolio stats sourced from /api/v1/projects/stats/summary */}
          {portfolio && (
            <div className="grid grid-cols-2 @[440px]:grid-cols-4 gap-4">
              <Card className="p-4 bg-slate-900/50 border-slate-800">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Projects</p>
                <p className="text-2xl font-black text-white">{portfolio.total_projects}</p>
                <p className="text-[8px] text-slate-600 mt-0.5">{portfolio.active} active</p>
              </Card>
              <Card className="p-4 bg-slate-900/50 border-slate-800">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Outputs</p>
                <p className="text-2xl font-black text-aura">{portfolio.total_outputs}</p>
                <p className="text-[8px] text-slate-600 mt-0.5">AI artifacts generated</p>
              </Card>
              <Card className="p-4 bg-slate-900/50 border-slate-800">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Commercialised</p>
                <p className="text-2xl font-black text-green-400">{portfolio.complete}</p>
                <p className="text-[8px] text-slate-600 mt-0.5">of {portfolio.total_projects} projects</p>
              </Card>
              <Card className="p-4 bg-slate-900/50 border-slate-800">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Stage Pipeline</p>
                <div className="flex gap-1 mt-1">
                  {(['concept', 'prototype', 'commercialise'] as const).map(s => (
                    <div key={s} className="flex-1 text-center">
                      <p className="text-sm font-black text-white">{portfolio.by_stage[s]}</p>
                      <p className="text-[7px] text-slate-600 capitalize">{s.slice(0,4)}</p>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
          <div className="grid grid-cols-1 @[440px]:grid-cols-4 gap-6">
            <Card className="p-6 bg-slate-900/50 border-slate-800">
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Fund Capital</p>
              <p className="text-3xl font-black text-white">
                {fund ? fund.total_capital.toLocaleString() : "—"}
                <span className="text-xs text-slate-500 ml-1">WST</span>
              </p>
            </Card>
            <Card className="p-6 bg-slate-900/50 border-slate-800">
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Available</p>
              <p className="text-3xl font-black text-aura">
                {fund ? fund.available.toLocaleString() : "—"}
                <span className="text-xs text-slate-500 ml-1">WST</span>
              </p>
            </Card>
            <Card className="p-6 bg-slate-900/50 border-slate-800">
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Utilisation</p>
              <div className="flex items-center gap-2">
                <Activity className="text-green-500" size={20} />
                <p className="text-3xl font-black text-white">{fund ? fund.utilisation_pct : "—"}%</p>
              </div>
              <p className="text-[9px] font-bold text-slate-600 mt-1">
                {fund ? `${fund.allocation_count} allocation(s) · ${fund.fund_health}` : ""}
              </p>
            </Card>
            <Card className="p-6 bg-aura/10 border-aura/20 flex items-center">
              <p className="text-[10px] font-bold text-slate-400 leading-relaxed">
                Figures are the real capital fund from <code>/api/v1/fund/status</code>, in virtual
                WST. They were previously derived from project counts and shown in dollars.
              </p>
            </Card>          </div>
        </div>
      )}

      {activeTab === 'external' && (
        <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8">
            <div className="@[440px]:col-span-2">
                <Card className="p-8 border-slate-800 bg-slate-950/50">
                    {/* W405 — this rendered four hardcoded prices (BTC/USD 65420, ETH/USD 3512,
                        SPY 520.4, AAPL 190.2) under the heading "Real-Time Market Feeds", each row
                        labelled "ALPHA VANTAGE SOURCE". Nothing fetched any market, and naming a
                        real commercial data provider as the source of invented dollar prices is a
                        far stronger claim than the numbers alone. */}
                    <h3 className="text-xl font-black text-white uppercase italic mb-4">External Markets</h3>
                    <p className="text-xs text-slate-500 font-semibold leading-relaxed max-w-xl">
                        No market-data provider is connected to this deployment, so no prices are
                        shown. Nothing here is fetched from any market.
                    </p>
                </Card>
            </div>
            <Card className="p-8 border-slate-800 bg-slate-900/30">
                {/* W415 — this card showed "Max Asset Concentration 20%" over a w-[20%] meter and
                    "Global Diversification OPTIMAL" over five hardcoded full green segments. Both
                    were literals in the markup: no risk limit is configured anywhere, no holdings
                    exist to concentrate, and no diversification verdict is computed. A filled meter
                    beside a percentage reads as a measurement of a live position against a policy
                    cap, which is the whole reason these were credible. Absent beats invented. */}
                <h3 className="text-xl font-black text-white uppercase italic mb-6">Risk Limits</h3>
                <div className="space-y-6">
                    <div>
                        <div className="flex justify-between text-[10px] font-black uppercase mb-2">
                            <span className="text-slate-500">Max Asset Concentration</span>
                            <span className="text-slate-600">NOT CONFIGURED</span>
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between text-[10px] font-black uppercase mb-2">
                            <span className="text-slate-500">Global Diversification</span>
                            <span className="text-slate-600">NOT MEASURED</span>
                        </div>
                    </div>
                    <p className="text-[10px] text-slate-500 font-semibold leading-relaxed">
                        No risk-limit policy is configured for this deployment and no holdings are
                        tracked, so there is nothing to measure concentration or diversification
                        against. These read "not configured" rather than showing a figure.
                    </p>
                </div>
            </Card>
        </div>
      )}

      {activeTab === 'crypto' && (
        <Card className="p-8 border-slate-800 bg-slate-950/50">
            <div className="flex items-center gap-4 mb-6">
                <div className="p-3 bg-aura text-slate-950 rounded-2xl"><Wallet size={24} /></div>
                <h3 className="text-xl font-black text-white uppercase italic">Real-Money Rails — Gated</h3>
            </div>
            {/* W314 — honesty: the previous card fabricated an on-chain gateway (Polygon, USDC/ETH
                deposits, invented transactions). Nothing on-chain exists. */}
            <p className="text-sm text-slate-400 font-bold leading-relaxed mb-4">
                No on-chain integration exists. All value on this platform is virtual, simulated WST —
                no real funds move. Real-money rails (deposits, withdrawals, exchange) remain DISABLED
                until the Owner explicitly authorises them and a compliance/KYC review passes.
            </p>
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-600">
                Honest by construction — nothing here fabricates transactions.
            </p>
        </Card>
      )}

      {activeTab === 'evolution' && (
        <Card className="p-8 border-slate-800 bg-slate-950/50">
            <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-highlight text-slate-950 rounded-2xl"><Code size={24} /></div>
                    <h3 className="text-xl font-black text-white uppercase italic">Constitutional Evolution</h3>
                </div>
                <Button onClick={() => notImplemented('Propose Amendment')} size="sm" className="bg-aura text-slate-950 font-black uppercase italic">Propose Amendment</Button>
            </div>
            {/* W415 — this panel rendered two literal objects as constitutional articles:
                  { id: '1130', title: 'Concentration Limit Increase', status: 'UNDER REVIEW', ... }
                  { id: '1205', title: 'Real-Time Data Mandate',       status: 'ENACTED',      ... }
                An ENACTED status badge asserts that the platform's constitution contains and has
                ratified Article 1205 — it does not; the real articles are served at
                /api/v154/constitution/articles and neither id appears there. The accompanying
                'Cast Vote' button toasted "Vote Cast — Article {id}" while pushing the id into
                local state only: nothing left the browser and no vote was ever recorded.
                Real constitutional/policy change in this platform runs through the Change Control
                Agency, so this now lists that agency's actual change requests, and says plainly
                that voting is not wired here. */}
            <div className="space-y-6">
                {changesError && (
                    <div className="p-4 rounded-2xl border border-red-500/30 bg-red-500/5 text-xs font-bold text-red-400">
                        Could not load change requests — {changesError}
                    </div>
                )}
                {changes === null && !changesError && (
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">Loading change requests…</p>
                )}
                {changes !== null && changes.length === 0 && !changesError && (
                    <p className="text-xs text-slate-500 font-semibold leading-relaxed max-w-xl">
                        No change requests have been submitted to the Change Control Agency. Nothing is
                        shown here because nothing has been proposed — this list is not seeded with examples.
                    </p>
                )}
                {(changes ?? []).map(change => (
                    <div key={change.cca_id} className="p-6 bg-slate-900/50 rounded-3xl border border-slate-800">
                        <div className="flex justify-between items-start mb-4 gap-4">
                            <div>
                                <p className="text-[10px] font-black text-aura uppercase tracking-widest mb-1">{change.cca_id}</p>
                                <h4 className="text-lg font-black text-white break-words">{change.title}</h4>
                            </div>
                            <Badge className={
                                change.status === 'implemented' || change.status === 'approved'
                                    ? 'bg-green-500/10 text-green-500'
                                    : change.status === 'rejected'
                                        ? 'bg-red-500/10 text-red-400'
                                        : 'bg-highlight/10 text-highlight'
                            }>{change.status.replace(/_/g, ' ').toUpperCase()}</Badge>
                        </div>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                            {change.change_type} · impact {change.impact_tier} · by {change.submitted_by}
                            {change.submitted_at ? ` · ${change.submitted_at}` : ''}
                        </p>
                        {change.decision && (
                            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">
                                Decision: {change.decision}
                            </p>
                        )}
                    </div>
                ))}
            </div>
            <p className="mt-6 text-[10px] font-bold text-slate-600 leading-relaxed">
                Read-only view of <code>/api/v1/cca</code>. No voting mechanism exists on this page —
                change requests are reviewed and decided in the Change Control Agency (/change-control),
                and any decision you see above was recorded there.
            </p>
        </Card>
      )}

      <footer className="text-xs text-center text-slate-500 mt-10 uppercase font-black tracking-widest">
        Virtual, simulated WST only — real-money rails Owner-gated and disabled | market rows are static reference samples, not live feeds
      </footer>
    </div>
  );
};
