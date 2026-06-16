import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { DollarSign, BarChart3, PieChart, TrendingUp, Wallet } from 'lucide-react';
import axios from 'axios';
import fallbackData from '../../data/fallbackData.json';

export const CFO: React.FC = () => {
  const [data, setData] = useState<any>(fallbackData.financials);

  useEffect(() => {
    axios.get('/api/csuite/cfo/metrics')
      .then(res => setData(res.data))
      .catch(() => console.warn("Using fallback financial data."));
  }, []);

  return (
    <div className="space-y-10">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-2xl @lg:text-3xl @3xl:text-4xl font-black mb-2 break-words">CFO Agent</h1>
          <p className="text-slate-500">Financial Orchestration & Tokenomics Optimization.</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-black text-slate-500 uppercase">Treasury Balance</p>
          <p className="text-3xl font-black text-vital">52,400 WST</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <MetricCard title="Revenue (24h)" value={`${data.revenue.toLocaleString()} WST`} delta={data.growth} icon={DollarSign} />
        <MetricCard title="Operating Costs" value={`${data.operating_costs.toLocaleString()} WST`} delta="-4.2%" icon={PieChart} />
        <MetricCard title="Liquidity" value={`${data.liquidity.toLocaleString()} WST`} delta="Stable" icon={Wallet} />
        {data.kpis.map((kpi: any) => (
          <MetricCard key={kpi.label} title={kpi.label} value={kpi.value} delta="+0.2%" icon={TrendingUp} />
        ))}
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex flex-col">
         <h3 className="text-xl font-bold mb-6">Financial Projections</h3>
         <div className="flex-1 bg-slate-800/20 rounded-2xl border border-slate-700/30 flex items-center justify-center italic text-slate-600">
           Real-time projection chart integration...
         </div>
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, delta, icon: Icon }: { title: string, value: string, delta: string, icon: any }) => (
  <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <div className="flex justify-between items-center mb-4">
      <div className="p-2 bg-slate-800 rounded-lg text-aura">
        <Icon size={20} />
      </div>
      <span className={`text-[10px] font-black ${delta.startsWith('+') ? 'text-vital' : 'text-rose-500'}`}>
        {delta}
      </span>
    </div>
    <div className="text-2xl font-black">{value}</div>
    <div className="text-[10px] font-black uppercase text-slate-500 mt-1">{title}</div>
  </div>
);
