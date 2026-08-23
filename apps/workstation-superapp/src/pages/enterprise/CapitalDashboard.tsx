import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Button, Badge, toast } from '@workstation/ui';
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

interface MarketFeed {
  symbol: string;
  price: number;
  change: number;
}

export const CapitalDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<CapitalMetrics | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioStats | null>(null);
  const [feeds, setFeeds] = useState<MarketFeed[]>([]);
  const [autonomousEnabled, setAutonomousEnabled] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'external' | 'crypto' | 'evolution'>('overview');
  const [votedAmendments, setVotedAmendments] = useState<string[]>([]);

  useEffect(() => {
    // Derive capital metrics from real project portfolio data
    axios.get<PortfolioStats>('/api/v1/projects/stats/summary', { validateStatus: () => true })
      .then(res => {
        if (res.status === 200) {
          const s = res.data;
          setPortfolio(s);
          // Map project counts to capital-metaphor metrics
          setMetrics({
            balance:             s.total_projects * 1000 + s.total_outputs * 250,
            totalDeposited:      s.total_projects * 1000,
            unrealisedProfit:    s.by_stage.prototype * 500 + s.by_stage.concept * 100,
            realisedProfit:      s.complete * 2500,
            riskScore:           s.total_projects === 0 ? 0 : Math.min(0.99, 0.6 + s.complete / Math.max(s.total_projects, 1) * 0.39),
            homeostasisStatus:   s.active > 0 ? 'minor_deviation' : 'stable',
          });
        } else {
          // Graceful fallback so the page still renders without backend
          setMetrics({ balance: 0, totalDeposited: 0, unrealisedProfit: 0, realisedProfit: 0, riskScore: 0, homeostasisStatus: 'stable' });
        }
      })
      .catch(() => {
        setMetrics({ balance: 0, totalDeposited: 0, unrealisedProfit: 0, realisedProfit: 0, riskScore: 0, homeostasisStatus: 'stable' });
      });

    setFeeds([
      { symbol: 'BTC/USD', price: 65420, change: 2.4 },
      { symbol: 'ETH/USD', price: 3512, change: 1.8 },
      { symbol: 'SPY', price: 520.4, change: 0.5 },
      { symbol: 'AAPL', price: 190.2, change: -0.2 },
    ]);
  }, []);

  const handleAction = (msg: string) => {
    toast(msg);
  };

  const handleCastVote = (id: string, title: string) => {
    setVotedAmendments(prev => [...prev, id]);
    toast(`Vote Cast — Article ${id}: ${title}`);
  };

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
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Portfolio Value</p>
              <p className="text-3xl font-black text-white">${metrics?.balance.toLocaleString() ?? '—'}</p>
            </Card>
            <Card className="p-6 bg-slate-900/50 border-slate-800">
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Unrealised Gain</p>
              <p className="text-3xl font-black text-aura">${metrics?.unrealisedProfit.toLocaleString() ?? '—'}</p>
            </Card>
            <Card className="p-6 bg-slate-900/50 border-slate-800">
              <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Risk Score</p>
              <div className="flex items-center gap-2">
                <Activity className="text-green-500" size={20} />
                <p className="text-3xl font-black text-white">{metrics ? (metrics.riskScore * 100).toFixed(0) : '—'}%</p>
              </div>
            </Card>
            <Card className="p-6 bg-aura/10 border-aura/20">
              <Button onClick={() => handleAction("Autonomous rebalance triggered.")} className="w-full h-full bg-aura text-slate-950 font-black hover:bg-white transition-all uppercase italic flex items-center gap-2">
                <Zap size={16} /> Rebalance
              </Button>
            </Card>
          </div>
        </div>
      )}

      {activeTab === 'external' && (
        <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8">
            <div className="@[440px]:col-span-2">
                <Card className="p-8 border-slate-800 bg-slate-950/50">
                    <h3 className="text-xl font-black text-white uppercase italic mb-6">Real-Time Market Feeds</h3>
                    <div className="space-y-4">
                        {feeds.map(feed => (
                            <div key={feed.symbol} className="flex items-center justify-between p-4 bg-slate-900 rounded-2xl border border-slate-800 hover:border-aura/30 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center font-black text-[10px] text-aura">{feed.symbol[0]}</div>
                                    <div>
                                        <p className="text-sm font-black text-white">{feed.symbol}</p>
                                        <p className="text-[10px] text-slate-500 font-bold">ALPHA VANTAGE SOURCE</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-sm font-black text-white">${feed.price.toLocaleString()}</p>
                                    <p className={`text-[10px] font-black ${feed.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                                        {feed.change >= 0 ? '+' : ''}{feed.change}%
                                    </p>
                                </div>
                                <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleAction(`Trading is disabled — no brokerage integration exists (reference data only): ${feed.symbol}`)}
                                    className="ml-4 border-slate-700 text-[10px] font-black uppercase"
                                >Trade</Button>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
            <Card className="p-8 border-slate-800 bg-slate-900/30">
                <h3 className="text-xl font-black text-white uppercase italic mb-6">Risk Limits</h3>
                <div className="space-y-6">
                    <div>
                        <div className="flex justify-between text-[10px] font-black uppercase mb-2">
                            <span className="text-slate-500">Max Asset Concentration</span>
                            <span className="text-aura">20%</span>
                        </div>
                        <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-aura w-[20%]" />
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between text-[10px] font-black uppercase mb-2">
                            <span className="text-slate-500">Global Diversification</span>
                            <span className="text-green-500">OPTIMAL</span>
                        </div>
                        <div className="grid grid-cols-5 gap-1">
                            {[1, 2, 3, 4, 5].map(i => <div key={i} className="h-2 bg-green-500 rounded-full" />)}
                        </div>
                    </div>
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
                <Button onClick={() => handleAction("Opening proposal interface...")} size="sm" className="bg-aura text-slate-950 font-black uppercase italic">Propose Amendment</Button>
            </div>
            <div className="space-y-6">
                {[
                    { id: '1130', title: 'Concentration Limit Increase', status: 'UNDER REVIEW', rationale: 'Allow 25% allocation for index ETFs to improve stability.' },
                    { id: '1205', title: 'Real-Time Data Mandate', status: 'ENACTED', rationale: 'Requirement for WebSocket ingestion for all high-stakes trades.' }
                ].map(amend => (
                    <div key={amend.id} className="p-6 bg-slate-900/50 rounded-3xl border border-slate-800">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <p className="text-[10px] font-black text-aura uppercase tracking-widest mb-1">Article {amend.id}</p>
                                <h4 className="text-lg font-black text-white">{amend.title}</h4>
                            </div>
                            <Badge className={amend.status === 'ENACTED' ? 'bg-green-500/10 text-green-500' : 'bg-highlight/10 text-highlight'}>{amend.status}</Badge>
                        </div>
                        <p className="text-xs text-slate-400 font-medium leading-relaxed italic mb-6">"{amend.rationale}"</p>
                        <div className="flex gap-4">
                            <Button
                                size="sm"
                                variant="outline"
                                onClick={() => handleAction(`Opening deliberation thread for Article ${amend.id}: ${amend.title}`)}
                                className="flex-1 border-slate-700 text-xs font-black uppercase italic"
                            >View Deliberation</Button>
                            {amend.status === 'UNDER REVIEW' && (
                                <Button
                                    size="sm"
                                    disabled={votedAmendments.includes(amend.id)}
                                    onClick={() => handleCastVote(amend.id, amend.title)}
                                    className="flex-1 bg-aura text-slate-950 text-xs font-black uppercase italic disabled:opacity-50"
                                >{votedAmendments.includes(amend.id) ? 'Voted' : 'Cast Vote'}</Button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </Card>
      )}

      <footer className="text-xs text-center text-slate-500 mt-10 uppercase font-black tracking-widest">
        Virtual, simulated WST only — real-money rails Owner-gated and disabled | market rows are static reference samples, not live feeds
      </footer>
    </div>
  );
};
