import React, { useState } from 'react';
import { Gauge, Zap, Globe, Activity, List, LayoutGrid, Volume2 } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';

export const FedPerformance: React.FC = () => {
  const { theme } = useTheme();
  const [viewMode, setViewMode] = useState<'visual' | 'table'>('visual');
  const isAdvanced = theme === 'advanced';

  return (
    <div className={`space-y-12 ${isAdvanced ? 'animate-in fade-in slide-in-from-bottom-4 duration-1000' : ''}`} role="main" aria-label="Federation Performance Dashboard">
      <header>
        <h1 className="text-4xl font-black mb-2">Federation Performance</h1>
        <p className="text-slate-500">Real-time health and throughput metrics for the global Workstation network (1,000+ Nodes).</p>
      </header>

      <section aria-label="Key Performance Indicators" className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <PerfCard label="Total Nodes" value="1,024" icon={Globe} color="text-aura" theme={theme} />
        <PerfCard label="Avg Latency" value="142ms" icon={Zap} color="text-highlight" theme={theme} />
        <PerfCard label="Treaty Velocity" value="42/min" icon={Activity} color="text-vital" theme={theme} />
        <PerfCard label="Ecosystem Uptime" value="99.99%" icon={Gauge} color="text-emerald-400" theme={theme} />
      </section>

      <section aria-label="Global Gossipsub Convergence Analysis" className={`p-8 rounded-3xl border transition-all duration-700 ${
        isAdvanced ? 'bg-sovereign border-aura/30' : 'bg-slate-900/40 border-slate-800'
      }`}>
        <div className="flex justify-between items-center mb-8">
           <h3 className="text-xl font-bold">Global Gossipsub Convergence</h3>
           <div className="flex items-center gap-2 bg-slate-800/50 p-1 rounded-xl border border-slate-700">
              <button
                onClick={() => setViewMode('visual')}
                className={`p-2 rounded-lg transition-all ${viewMode === 'visual' ? 'bg-aura text-sovereign shadow-lg shadow-aura/20' : 'text-slate-500 hover:text-white'}`}
                title="Visual Mode"
                aria-label="Switch to visual chart view"
                aria-pressed={viewMode === 'visual'}
              >
                 <LayoutGrid size={16} />
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`p-2 rounded-lg transition-all ${viewMode === 'table' ? 'bg-aura text-sovereign shadow-lg shadow-aura/20' : 'text-slate-500 hover:text-white'}`}
                title="Table Mode"
                aria-label="Switch to accessible data table view"
                aria-pressed={viewMode === 'table'}
              >
                 <List size={16} />
              </button>
           </div>
        </div>

        {viewMode === 'visual' ? (
          <div className="h-96 flex flex-col items-center justify-center text-center" role="img" aria-label="Animated visualization of node convergence showing 98% network alignment. High contrast and movement indicating real-time cytokine propagation.">
             <div className="w-32 h-32 rounded-full border-8 border-aura/20 border-t-aura animate-spin-slow mb-8"></div>
             <p className="text-slate-500 max-w-sm">Visualizing real-time propagation of cytokine signals across 1,024 federated nodes.</p>
             <button className="mt-4 flex items-center gap-2 text-[10px] font-black text-aura uppercase tracking-widest hover:underline" aria-label="Listen to audio rendering of network trends">
                <Volume2 size={14} />
                Generate Audio Summary
             </button>
          </div>
        ) : (
          <div className="h-96 overflow-y-auto pr-2 custom-scrollbar">
             <table className="w-full text-left text-sm border-collapse">
                <thead className="sticky top-0 bg-sovereign z-10 border-b border-aura/20 text-aura font-black uppercase text-[10px] tracking-widest">
                   <tr>
                      <th className="py-4 px-2">Node Group</th>
                      <th className="py-4 px-2">Health</th>
                      <th className="py-4 px-2">Latency</th>
                      <th className="py-4 px-2">Convergence</th>
                   </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                   {[
                     { g: 'Alpha (EU)', h: 'Optimal', l: '42ms', c: '99.8%' },
                     { g: 'Beta (US)', h: 'Optimal', l: '88ms', c: '99.2%' },
                     { g: 'Gamma (Asia)', h: 'Warning', l: '192ms', c: '97.4%' },
                     { g: 'Delta (LatAm)', h: 'Optimal', l: '114ms', c: '98.9%' },
                     { g: 'Edge Swarm A', h: 'Scaling', l: '24ms', c: '100%' },
                   ].map((row, i) => (
                     <tr key={i} className="hover:bg-aura/5 transition-colors">
                        <td className="py-4 px-2 font-bold">{row.g}</td>
                        <td className={`py-4 px-2 font-bold ${row.h === 'Optimal' ? 'text-vital' : 'text-amber-500'}`}>{row.h}</td>
                        <td className="py-4 px-2 text-slate-400 font-mono">{row.l}</td>
                        <td className="py-4 px-2 text-aura font-mono font-bold">{row.c}</td>
                     </tr>
                   ))}
                </tbody>
             </table>
          </div>
        )}
      </section>
    </div>
  );
};

const PerfCard = ({ label, value, icon: Icon, color, theme }: any) => {
  const isAdvanced = theme === 'advanced';
  return (
    <div
      className={`p-8 rounded-3xl border transition-all duration-700 backdrop-blur-sm focus-within:ring-2 focus-within:ring-aura ${
        isAdvanced ? 'bg-sovereign border-aura/30 shadow-lg shadow-aura/5' : 'bg-slate-900/40 border-slate-800'
      }`}
      tabIndex={0}
      role="article"
      aria-label={`${label}: ${value}`}
    >
      <Icon size={24} className={`${color} mb-4`} aria-hidden="true" />
      <div className="text-3xl font-black" aria-hidden="true">{value}</div>
      <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1" aria-hidden="true">{label}</p>
    </div>
  );
};
