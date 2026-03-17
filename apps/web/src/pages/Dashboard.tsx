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
    <div className="space-y-10" role="main" aria-label="Workstation Dashboard">
      <header>
        <h1 className="text-4xl font-black mb-2 focus:outline-none" tabIndex={-1}>Welcome back, Guardian</h1>
        <p className="text-slate-500">The Workstation ecosystem is resonating at optimal frequencies.</p>
      </header>

      <section aria-label="System Overview Stats" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm focus-within:ring-2 focus-within:ring-aura"
            tabIndex={0}
            role="article"
            aria-labelledby={`stat-label-${i}`}
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-xl bg-slate-800/50 ${stat.color}`} aria-hidden="true">
                <stat.icon size={24} />
              </div>
              <span className="text-[10px] font-black px-2 py-1 rounded bg-slate-800 text-slate-400" aria-label={`Change: ${stat.delta}`}>
                {stat.delta}
              </span>
            </div>
            <div className="text-3xl font-black mb-1" aria-label={`${stat.label} value is ${stat.value}`}>{stat.value}</div>
            <div id={`stat-label-${i}`} className="text-xs font-bold uppercase tracking-widest text-slate-500">{stat.label}</div>
          </motion.div>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <section aria-label="UEG Resonance Map" className="lg:col-span-2 p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex flex-col items-center justify-center">
          <p className="text-slate-600 font-bold uppercase tracking-[0.2em]">UEG Resonance Map Visualization</p>
          <div className="sr-only">
            This visualization shows the real-time resonance of the Unified Event Graph across the federation.
            All nodes are currently within optimal operational parameters (98%+ fidelity).
          </div>
        </section>
        <section aria-label="Recent Activity Log" className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-96 flex flex-col">
          <h3 className="text-xl font-bold mb-6">Recent Activity</h3>
          <div className="space-y-4 overflow-y-auto custom-scrollbar pr-2" aria-live="polite">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex gap-4 p-4 rounded-xl bg-slate-800/30 border border-slate-700/50 focus-within:ring-1 focus-within:ring-aura" tabIndex={0}>
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
