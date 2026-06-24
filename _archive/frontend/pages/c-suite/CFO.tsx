import React from 'react';
import { DollarSign, PieChart, TrendingUp, Wallet, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface CfoMetrics {
  portfolio_value: number;
  realised_gain: number;
  unrealised_gain: number;
  operating_costs: number;
  roi_percent: number;
  liquidity: number;
  total_projects: number;
  total_outputs: number;
  token_balance: number;
  token_tier: string;
  token_spend_24h: number;
}

const fetchMetrics = (): Promise<CfoMetrics> =>
  axios.get<CfoMetrics>('/api/csuite/cfo/metrics').then(r => r.data);

export const CFO: React.FC = () => {
  const { data, isLoading, error } = useQuery<CfoMetrics>({
    queryKey: ['cfo-metrics'],
    queryFn: fetchMetrics,
    refetchInterval: 60_000,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 size={28} className="animate-spin text-aura" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-64 flex-col gap-3">
        <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">
          Backend offline — start the API server to view live metrics.
        </p>
      </div>
    );
  }

  const metrics = [
    { title: 'Portfolio Value',  value: `${data.portfolio_value.toLocaleString()} WST`,  delta: '+computed',  icon: TrendingUp },
    { title: 'Realised Gain',   value: `${data.realised_gain.toLocaleString()} WST`,    delta: '+realised',  icon: DollarSign },
    { title: 'Operating Costs', value: `${data.operating_costs.toLocaleString()} WST`,  delta: '-costs',     icon: PieChart   },
    { title: 'Token Balance',   value: `${data.token_balance.toLocaleString()} credits`, delta: data.token_tier, icon: Wallet },
  ];

  return (
    <div className="space-y-10">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black mb-2 break-words">CFO Agent</h1>
          <p className="text-slate-500">Financial Orchestration — live metrics from the project portfolio.</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-black text-slate-500 uppercase">Portfolio Value</p>
          <p className="text-3xl font-black text-vital">{data.portfolio_value.toLocaleString()} WST</p>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 @[700px]:grid-cols-4 gap-6">
        {metrics.map(m => (
          <MetricCard key={m.title} {...m} />
        ))}
      </div>

      <div className="grid grid-cols-1 @[480px]:grid-cols-3 gap-6">
        <StatBlock label="Total Projects"  value={String(data.total_projects)} />
        <StatBlock label="AI Deliverables" value={String(data.total_outputs)}  />
        <StatBlock label="ROI"             value={`${data.roi_percent}%`}      />
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-6">Liquidity &amp; Cost Breakdown</h3>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1">Unrealised Gain</p>
            <p className="text-xl font-black text-white">{data.unrealised_gain.toLocaleString()} WST</p>
          </div>
          <div>
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1">Token Spend (24h)</p>
            <p className="text-xl font-black text-white">{data.token_spend_24h} credits</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, delta, icon: Icon }: { title: string; value: string; delta: string; icon: any }) => (
  <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <div className="flex justify-between items-center mb-4">
      <div className="p-2 bg-slate-800 rounded-lg text-aura"><Icon size={20} /></div>
      <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">{delta}</span>
    </div>
    <div className="text-2xl font-black">{value}</div>
    <div className="text-[10px] font-black uppercase text-slate-500 mt-1">{title}</div>
  </div>
);

const StatBlock = ({ label, value }: { label: string; value: string }) => (
  <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
    <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-1">{label}</p>
    <p className="text-2xl font-black text-white">{value}</p>
  </div>
);
