import React from 'react';
import { motion } from 'framer-motion';
import CumulativeDashboard from '../components/dashboards/CumulativeDashboard';
import { LayoutGrid, Brain, Book, Gavel, Briefcase, GraduationCap } from 'lucide-react';

const UnifiedDashboard = ({ userProfile, mockData }) => {
  const products = [
    { id: 'religion', name: 'Sanctuary', icon: Book, color: 'emerald' },
    { id: 'education', name: 'Academy', icon: GraduationCap, color: 'blue' },
    { id: 'science', name: 'Reactor', icon: Brain, color: 'purple' },
    { id: 'law', name: 'Counsel', icon: Gavel, color: 'orange' },
    { id: 'employment', name: 'Launchpad', icon: Briefcase, color: 'teal' }
  ];

  const impactStats = [
    { label: 'Papers Incubated', value: 12, color: 'purple' },
    { label: 'Verses Mastered', value: 450, color: 'emerald' },
    { label: 'Active Contracts', value: 8, color: 'orange' },
    { label: 'Job Readiness', value: '94%', color: 'teal' }
  ];

  return (
    <div className="space-y-12 pb-20 px-4 md:px-0">
      <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
        <div>
          <p className="text-amber-500 font-bold uppercase tracking-widest text-xs mb-2">Cross-Domain Overview</p>
          <h2 className="text-3xl md:text-4xl font-black text-white leading-tight">Unified Workspace</h2>
        </div>
        <div className="flex gap-2">
          {products.map(p => (
            <div key={p.id} className={`w-10 h-10 rounded-lg flex items-center justify-center bg-${p.color}-500/20 text-${p.color}-400 border border-${p.color}-500/30`}>
              <p.icon size={20} />
            </div>
          ))}
        </div>
      </header>

      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
        {impactStats.map((stat, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className={`p-6 rounded-2xl bg-${stat.color}-500/5 border border-${stat.color}-500/10 backdrop-blur-sm shadow-xl`}
          >
            <p className={`text-[10px] font-black uppercase text-${stat.color}-400 mb-1`}>{stat.label}</p>
            <p className="text-3xl font-black text-white">{stat.value}</p>
          </motion.div>
        ))}
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <CumulativeDashboard domain="business" data={mockData} />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div whileHover={{ scale: 1.02 }} className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
              <h4 className="text-white font-bold mb-4 flex items-center gap-2">
                <LayoutGrid size={18} className="text-amber-500" />
                Active Synergy Workflows
              </h4>
              <ul className="space-y-3 text-sm text-slate-400">
                <li className="flex justify-between">
                  <span>{"Research -> Copyright"}</span>
                  <span className="text-emerald-500 font-mono">RUNNING</span>
                </li>
                <li className="flex justify-between">
                  <span>{"Isnad -> Education"}</span>
                  <span className="text-amber-500 font-mono">PENDING</span>
                </li>
              </ul>
            </motion.div>

            <motion.div whileHover={{ scale: 1.02 }} className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
              <h4 className="text-white font-bold mb-4">Entity Recommendations</h4>
              <p className="text-sm text-slate-400 italic">
                "Based on your recent Science research, I suggest reviewing the Law reactor's Intellectual Property modules."
              </p>
            </motion.div>
          </div>
        </div>

        <aside className="space-y-8">
          <div className="p-8 rounded-3xl bg-gradient-to-br from-amber-500 to-orange-600 text-slate-900 shadow-2xl">
            <h3 className="text-2xl font-black mb-4">Apotheosis v120.0</h3>
            <p className="text-sm font-medium opacity-80 mb-6">Your cross-domain synergy is at 99.9% fidelity.</p>
            <div className="w-full bg-black/20 rounded-full h-3 overflow-hidden">
               <motion.div
                 initial={{ width: 0 }}
                 animate={{ width: '99.9%' }}
                 className="h-full bg-white"
               />
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
            <h4 className="text-white font-bold mb-4 uppercase tracking-tighter text-xs">Recent Events</h4>
            <div className="space-y-4">
              {[
                { domain: 'Science', msg: 'Paper synthesis complete', time: '12m ago' },
                { domain: 'Law', msg: 'Compliance audit passed', time: '1h ago' },
                { domain: 'Religion', msg: 'Daily Hifz target met', time: '2h ago' }
              ].map((ev, i) => (
                <div key={i} className="flex justify-between items-center text-xs">
                  <span className="text-slate-300 font-bold">{ev.domain}</span>
                  <span className="text-slate-500">{ev.msg}</span>
                  <span className="text-slate-600 italic">{ev.time}</span>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </section>
    </div>
  );
};

export default UnifiedDashboard;
