import React from 'react';
import { motion } from 'framer-motion';
import { DollarSign, BarChart3, PieChart } from 'lucide-react';

export const CFO: React.FC = () => {
  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black mb-2">CFO Agent</h1>
          <p className="text-slate-500">Financial Orchestration & Tokenomics Optimization.</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-black text-slate-500 uppercase">Treasury Balance</p>
          <p className="text-3xl font-black text-vital">52,400 WST</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard title="Revenue (24h)" value="1,240 WST" delta="+12%" icon={DollarSign} />
        <MetricCard title="Operating Costs" value="450 WST" delta="-5%" icon={PieChart} />
        <MetricCard title="Market Cap" value="1.4M WST" delta="+2.4%" icon={BarChart3} />
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
