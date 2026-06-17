import React from 'react';
import {
  Activity,
  ShieldCheck,
  Eye,
  Lock,
  PieChart,
  Target
} from 'lucide-react';

const QEPAnalyticsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0A0B10] text-white p-8">
      <header className="mb-12">
        <div className="flex items-center gap-3 mb-2">
          <Target className="text-[#00F2FF]" size={24} />
          <span className="text-[#00F2FF] font-mono tracking-widest text-sm uppercase">Sovereign Knowledge Domain</span>
        </div>
        <h1 className="text-4xl font-bold tracking-tight">AI Analytics & Privacy Observatory</h1>
        <p className="text-slate-400 mt-2">v8.6 Production Signature Product Monitoring — Real-time AI Performance & Privacy Budget Tracking</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-slate-400 font-medium">Privacy Budget (ε)</h3>
            <Lock className="text-[#00F2FF]" size={20} />
          </div>
          <div className="text-3xl font-bold">0.42 / 1.0</div>
          <div className="mt-4 h-2 bg-slate-900 rounded-full overflow-hidden">
            <div className="h-full bg-[#00F2FF]" style={{ width: '42%' }}></div>
          </div>
          <p className="text-xs text-slate-500 mt-2">Differential Privacy Level: HIGH</p>
        </div>

        <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-slate-400 font-medium">Model Bias Score</h3>
            <ShieldCheck className="text-[#00F2FF]" size={20} />
          </div>
          <div className="text-3xl font-bold">1.2%</div>
          <p className="text-xs text-green-500 mt-2">↓ 0.3% from last cycle (TARGET: &lt; 2%)</p>
        </div>

        <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-slate-400 font-medium">Inference Confidence</h3>
            <Activity className="text-[#00F2FF]" size={20} />
          </div>
          <div className="text-3xl font-bold">96.8%</div>
          <p className="text-xs text-slate-500 mt-2">Across 5.2k daily learning path optimizations</p>
        </div>
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-6">
        <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
          <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <PieChart size={20} className="text-[#00F2FF]" />
            Demographic Fairness Distribution
          </h3>
          <div className="space-y-4">
            {[
              { label: 'Sectarian Neutrality', val: 99.4 },
              { label: 'Gender Parity', val: 98.7 },
              { label: 'Dialect Inclusivity', val: 96.2 },
              { label: 'Cultural Sensitivity', val: 97.5 },
            ].map(item => (
              <div key={item.label}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">{item.label}</span>
                  <span className="text-white font-mono">{item.val}%</span>
                </div>
                <div className="h-1.5 bg-slate-900 rounded-full">
                  <div className="h-full bg-[#00F2FF]" style={{ width: `${item.val}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
          <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Eye size={20} className="text-[#00F2FF]" />
            Privacy Preservation Comparison
          </h3>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="text-slate-500 border-b border-slate-800">
                <th className="pb-3 font-medium">Metric</th>
                <th className="pb-3 font-medium">Raw Value</th>
                <th className="pb-3 font-medium">Privacy-Preserved</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              <tr className="text-slate-300">
                <td className="py-4">Avg Student Score</td>
                <td className="py-4 font-mono">85.42</td>
                <td className="py-4 font-mono text-[#00F2FF]">85.18 (+0.24 noise)</td>
              </tr>
              <tr className="text-slate-300">
                <td className="py-4">Lesson Completion Rate</td>
                <td className="py-4 font-mono">72.1%</td>
                <td className="py-4 font-mono text-[#00F2FF]">72.5% (+0.4% noise)</td>
              </tr>
              <tr className="text-slate-300">
                <td className="py-4">Retention (30-day)</td>
                <td className="py-4 font-mono">68.5%</td>
                <td className="py-4 font-mono text-[#00F2FF]">67.9% (-0.6% noise)</td>
              </tr>
            </tbody>
          </table>
          <p className="text-[10px] text-slate-500 mt-4 italic">
            *Noise added via Laplace distribution (ε=0.42). Raw data is never stored in production logs.
          </p>
        </div>
      </div>
    </div>
  );
};

export default QEPAnalyticsPage;
