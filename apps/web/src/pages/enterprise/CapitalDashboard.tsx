import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import {
  TrendingUp, ShieldAlert, PieChart, Activity,
  BarChart3, MessageCircle, AlertTriangle, RefreshCw
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

interface InvestmentRecommendation {
  asset: string;
  allocation: number;
  expectedReturn: number;
  confidence: number;
  reasoning: string;
}

interface TwinForecast {
  day: number;
  predicted_balance: number;
  timestamp: string;
}

interface CycleHealth {
  name: string;
  score: number;
  status: 'optimal' | 'correcting' | 'imbalanced';
}

export const CapitalDashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState<CapitalMetrics | null>(null);
  const [recommendation, setRecommendation] = useState<InvestmentRecommendation | null>(null);
  const [forecast, setTwinForecast] = useState<TwinForecast[]>([]);
  const [cycles, setCycles] = useState<CycleHealth[]>([]);
  const [consultation, setConsultation] = useState<any>(null);

  useEffect(() => {
    // Simulated fetch for Phase 2
    setMetrics({
      balance: 12500,
      totalDeposited: 10000,
      unrealisedProfit: 1500,
      realisedProfit: 1000,
      riskScore: 0.92,
      homeostasisStatus: 'stable'
    });

    setRecommendation({
      asset: "Science Reactor (AlphaFold 3)",
      allocation: 0.4,
      expectedReturn: 12.5,
      confidence: 0.94,
      reasoning: "High-yield potential detected in biomolecular research. MJM v4.0 forecasts 95% CI for positive returns over 30 days using biospheric analogical transfer."
    });

    setTwinForecast([
      { day: 1, predicted_balance: 12500, timestamp: '2026-05-08' },
      { day: 2, predicted_balance: 12620, timestamp: '2026-05-09' },
      { day: 3, predicted_balance: 12750, timestamp: '2026-05-10' },
      { day: 4, predicted_balance: 12680, timestamp: '2026-05-11' },
      { day: 5, predicted_balance: 12890, timestamp: '2026-05-12' },
      { day: 6, predicted_balance: 13100, timestamp: '2026-05-13' },
      { day: 7, predicted_balance: 13450, timestamp: '2026-05-14' },
    ]);

    setCycles([
      { name: 'Water', score: 1.0, status: 'optimal' },
      { name: 'Carbon', score: 0.98, status: 'optimal' },
      { name: 'Nitrogen', score: 0.95, status: 'correcting' },
      { name: 'Oxygen', score: 1.0, status: 'optimal' },
      { name: 'Phosphorus', score: 0.92, status: 'optimal' },
      { name: 'Sulfur', score: 1.0, status: 'optimal' },
    ]);

    setConsultation({
      consensus_score: 0.88,
      engines: [
        { name: 'Inkashaf', status: 'AGREED', reasoning: 'Bullish pattern match.' },
        { name: 'Aqal', status: 'AGREED', reasoning: 'Logic validated.' },
        { name: 'Iman', status: 'AGREED', reasoning: 'Ethically aligned.' },
      ]
    });
  }, []);

  const handleAction = (msg: string) => {
    alert(msg);
  };

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-5xl font-black text-white uppercase italic">Sovereign Capital</h1>
          <p className="text-slate-500 font-bold tracking-widest uppercase text-xs mt-2">vΩ∞-CAPITAL-FUND | Living Investment Organism</p>
        </div>
        <div className="flex gap-4">
            <Badge variant="outline" className="border-aura text-aura font-black">PHASE 2: SELF-REFLECTIVE</Badge>
            <Badge variant="outline" className="border-green-500 text-green-500 font-black uppercase">Homeostasis: Stable</Badge>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <Card className="p-6 bg-slate-900/50 border-slate-800">
          <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Current Balance</p>
          <p className="text-3xl font-black text-white">${metrics?.balance.toLocaleString()}</p>
        </Card>
        <Card className="p-6 bg-slate-900/50 border-slate-800">
          <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Total Growth</p>
          <p className="text-3xl font-black text-green-500">+{((metrics?.unrealisedProfit || 0) / (metrics?.totalDeposited || 1) * 100).toFixed(1)}%</p>
        </Card>
        <Card className="p-6 bg-slate-900/50 border-slate-800">
          <p className="text-xs font-black text-slate-500 uppercase tracking-tighter mb-1">Risk Index</p>
          <div className="flex items-center gap-2">
            <Activity className="text-aura" size={20} />
            <p className="text-3xl font-black text-white">{(metrics?.riskScore || 0 * 100).toFixed(1)}%</p>
          </div>
        </Card>
        <Card className="p-6 bg-aura/10 border-aura/20">
            <div className="flex flex-col h-full justify-between">
                <Button onClick={() => handleAction("Redirecting to Stripe...")} className="w-full bg-aura text-slate-950 font-black hover:bg-white transition-all uppercase italic">Deposit Capital</Button>
            </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          {/* Digital Twin Forecast */}
          <Card className="p-8 border-slate-800 bg-slate-950/50">
             <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                   <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><BarChart3 size={20} /></div>
                   <h3 className="text-xl font-black text-white uppercase italic">7-Day Digital Twin Forecast</h3>
                </div>
                <div className="text-right">
                   <p className="text-[10px] font-black text-slate-500 uppercase">Predicted P&L</p>
                   <p className="text-sm font-black text-green-400">+$950.00</p>
                </div>
             </div>
             <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                   <AreaChart data={forecast}>
                      <defs>
                        <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="day" stroke="#475569" fontSize={10} />
                      <YAxis stroke="#475569" fontSize={10} domain={['auto', 'auto']} />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b' }}
                        itemStyle={{ color: '#fff' }}
                      />
                      <Area type="monotone" dataKey="predicted_balance" stroke="#3b82f6" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={3} />
                   </AreaChart>
                </ResponsiveContainer>
             </div>
          </Card>

          {/* AI Strategy & Consultation */}
          <Card className="p-8 border-aura/30 bg-slate-950 shadow-[0_0_50px_-12px_rgba(168,85,247,0.2)]">
            <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-aura rounded-2xl text-slate-950"><TrendingUp size={24} /></div>
                <div>
                  <h3 className="text-2xl font-black text-white uppercase italic">AI Allocation Strategy</h3>
                  <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">MJM v4.0 Recursive Consensus</p>
                </div>
              </div>
              <Badge className="bg-green-500/20 text-green-500 border-green-500/30 font-black">94% CONFIDENCE</Badge>
            </div>

            <div className="p-6 bg-slate-900/80 rounded-3xl border border-slate-800 mb-8">
              <p className="text-slate-300 font-medium leading-relaxed italic">"{recommendation?.reasoning}"</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div>
                    <p className="text-xs font-black text-slate-500 uppercase mb-4 tracking-widest">Investment Target</p>
                    <div className="flex items-center justify-between p-4 bg-slate-900 rounded-2xl border border-slate-800">
                        <span className="text-sm font-bold text-white">{recommendation?.asset}</span>
                        <span className="text-lg font-black text-aura">{(recommendation?.allocation || 0 * 100).toFixed(0)}%</span>
                    </div>
                </div>
                <div>
                    <p className="text-xs font-black text-slate-500 uppercase mb-4 tracking-widest">Mushāwara Consensus</p>
                    <div className="flex items-center gap-3">
                        {consultation?.engines.map((eng: any) => (
                            <div key={eng.name} className="flex-1 text-center p-2 bg-slate-900 rounded-xl border border-slate-800">
                                <p className="text-[9px] font-black text-slate-500 uppercase">{eng.name}</p>
                                <div className="text-[8px] font-black text-green-400 mt-1">{eng.status}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="flex gap-4">
              <Button onClick={() => handleAction("Strategy deployed and logged to UEG.")} className="flex-1 bg-white text-slate-950 font-black hover:bg-aura transition-colors uppercase italic">Accept & Rebalance</Button>
              <Button onClick={() => handleAction("Manual override mode active.")} variant="outline" className="flex-1 border-slate-700 text-slate-400 font-black hover:text-white uppercase italic">Manual Override</Button>
            </div>
          </Card>
        </div>

        <div className="space-y-8">
            {/* Geospheric Health */}
            <Card className="p-8 space-y-6 bg-slate-900/30 border-slate-800">
                <div className="flex items-center gap-4 text-aura">
                    <RefreshCw size={24} />
                    <h3 className="text-xl font-black uppercase italic text-white">Homeostasis</h3>
                </div>
                <div className="space-y-4">
                    {cycles.map(cycle => (
                        <div key={cycle.name}>
                            <div className="flex justify-between text-[10px] font-black uppercase mb-1">
                                <span className="text-slate-400">{cycle.name} Cycle</span>
                                <span className={cycle.status === 'optimal' ? 'text-green-400' : 'text-yellow-400'}>{cycle.status}</span>
                            </div>
                            <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                <div
                                    className={`h-full transition-all duration-1000 ${cycle.status === 'optimal' ? 'bg-green-500' : 'bg-yellow-500'}`}
                                    style={{ width: `${cycle.score * 100}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </Card>

            {/* Governance & Audit */}
            <Card className="p-8 space-y-6 bg-slate-900/30 border-slate-800">
                <div className="flex items-center gap-4 text-slate-400">
                    <ShieldAlert size={24} />
                    <h3 className="text-xl font-black uppercase italic text-white">Governance</h3>
                </div>
                <div className="p-4 bg-red-500/5 border border-red-500/20 rounded-2xl flex gap-3">
                    <AlertTriangle className="text-red-500 shrink-0" size={16} />
                    <p className="text-[10px] text-slate-400 leading-relaxed font-bold uppercase">Withdrawals >5% AUM require 3/5 MultiSigCouncil quorum.</p>
                </div>

                <div className="pt-4 border-t border-slate-800 space-y-4">
                    <Button onClick={() => handleAction("Withdrawal requested.")} variant="outline" className="w-full border-slate-700 text-slate-300 font-black hover:bg-red-500/10 hover:text-red-500 hover:border-red-500/50 transition-all uppercase italic">Withdraw Profit</Button>
                    <Button onClick={() => handleAction("Exporting audit log...")} variant="outline" className="w-full border-slate-800 text-slate-500 font-black hover:text-white uppercase italic text-[10px]">Generate Audit Bundle</Button>
                </div>

                <footer className="text-[10px] text-slate-600 font-bold uppercase text-center mt-4">
                    All financial actions logged to UEG with SHA-3-512 integrity.
                </footer>
            </Card>
        </div>
      </div>
    </div>
  );
};
