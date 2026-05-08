import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { TrendingUp, ShieldAlert, PieChart, Activity } from 'lucide-react';

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

export const CapitalDashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState<CapitalMetrics | null>(null);
  const [recommendation, setRecommendation] = useState<InvestmentRecommendation | null>(null);

  useEffect(() => {
    // Simulated fetch for Phase 1
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
      reasoning: "High-yield potential detected in biomolecular research. MJM v4.0 forecasts 95% CI for positive returns over 30 days."
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
          <p className="text-slate-500 font-bold tracking-widest uppercase text-xs mt-2">vΩ∞-CAPITAL-FUND | Intelligent Growth System</p>
        </div>
        <Badge variant="outline" className="border-aura text-aura font-black">STABLE HOMEOSTASIS</Badge>
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
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-8 border-aura/30 bg-slate-950 shadow-[0_0_50px_-12px_rgba(168,85,247,0.2)]">
            <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-aura rounded-2xl text-slate-950"><TrendingUp size={24} /></div>
                <div>
                  <h3 className="text-2xl font-black text-white uppercase italic">AI Allocation Strategy</h3>
                  <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Recommended by MJM v4.0</p>
                </div>
              </div>
              <Badge className="bg-green-500/20 text-green-500 border-green-500/30">94% Confidence</Badge>
            </div>

            <div className="p-6 bg-slate-900/80 rounded-3xl border border-slate-800 mb-8">
              <p className="text-slate-300 font-medium leading-relaxed italic">"{recommendation?.reasoning}"</p>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-8">
               <div className="text-center p-4 bg-slate-900 rounded-2xl border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Target</p>
                  <p className="text-xs font-bold text-white truncate">{recommendation?.asset}</p>
               </div>
               <div className="text-center p-4 bg-slate-900 rounded-2xl border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Allocation</p>
                  <p className="text-sm font-bold text-aura">{(recommendation?.allocation || 0 * 100).toFixed(0)}%</p>
               </div>
               <div className="text-center p-4 bg-slate-900 rounded-2xl border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Exp. ROI</p>
                  <p className="text-sm font-bold text-green-400">+{recommendation?.expectedReturn}%</p>
               </div>
            </div>

            <div className="flex gap-4">
              <Button onClick={() => handleAction("Strategy deployed and logged to UEG.")} className="flex-1 bg-white text-slate-950 font-black hover:bg-aura transition-colors uppercase italic">Accept & Rebalance</Button>
              <Button onClick={() => handleAction("Manual override mode active.")} variant="outline" className="flex-1 border-slate-700 text-slate-400 font-black hover:text-white uppercase italic">Manual Override</Button>
            </div>
          </Card>
        </div>

        <Card className="p-8 space-y-6 bg-slate-900/30 border-slate-800">
          <div className="flex items-center gap-4 text-slate-400">
            <ShieldAlert size={24} />
            <h3 className="text-xl font-black uppercase italic text-white">Governance</h3>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed font-bold uppercase tracking-wider">Withdrawals exceeding 5% of total fund value require MultiSigCouncil approval (3/5 signatures).</p>

          <div className="pt-4 border-t border-slate-800 space-y-4">
             <Button onClick={() => handleAction("Withdrawal requested.")} variant="outline" className="w-full border-slate-700 text-slate-300 font-black hover:bg-red-500/10 hover:text-red-500 hover:border-red-500/50 transition-all uppercase italic">Withdraw Profit</Button>
             <Button onClick={() => handleAction("Exporting audit log...")} variant="outline" className="w-full border-slate-800 text-slate-500 font-black hover:text-white uppercase italic text-[10px]">Generate Audit Report</Button>
          </div>

          <footer className="text-[10px] text-slate-600 font-bold uppercase text-center mt-10">
            Every transaction is logged to the UEG Merkle-DAG with SHA-3-512 cryptographic integrity.
          </footer>
        </Card>
      </div>
    </div>
  );
};
