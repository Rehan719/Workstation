import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Users, Cpu, Zap } from 'lucide-react';

const stats = [
  { label: 'System Fidelity', value: '99.98%', delta: '+0.02%', icon: Zap, color: 'text-aura' },
  { label: 'Active Agents', value: '42', delta: '+4 today', icon: Cpu, color: 'text-vital' },
  { label: 'Network Depth', value: '1.42M', delta: '+12k/hr', icon: TrendingUp, color: 'text-highlight' },
  { label: 'Global Nodes', value: '108', delta: 'Stable', icon: Users, color: 'text-slate-400' },
];

export const Dashboard: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Welcome back, Guardian</h1>
        <p className="text-slate-500">The Workstation ecosystem is resonating at optimal frequencies.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm"
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-xl bg-slate-800/50 ${stat.color}`}>
                <stat.icon size={24} />
              </div>
              <span className="text-[10px] font-black px-2 py-1 rounded bg-slate-800 text-slate-400">
                {stat.delta}
              </span>
            </div>
            <div className="text-3xl font-black mb-1">{stat.value}</div>
            <div className="text-xs font-bold uppercase tracking-widest text-slate-500">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex items-center justify-center">
          <p className="text-slate-600 font-bold uppercase tracking-[0.2em]">UEG Resonance Map Visualization</p>
        </div>
        <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex flex-col">
          <h3 className="text-xl font-bold mb-6">Recent Activity</h3>
          <div className="space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex gap-4 p-4 rounded-xl bg-slate-800/30 border border-slate-700/50">
                <div className="w-2 h-2 rounded-full bg-aura mt-1.5 shadow-[0_0_8px_rgba(56,189,248,0.5)]"></div>
                <div>
                  <p className="text-sm font-bold">Protocol v138.0 Synchronized</p>
                  <p className="text-[10px] text-slate-500">2 minutes ago • System</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
