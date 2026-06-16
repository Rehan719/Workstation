import React, { useState } from 'react';
import {
  UserCheck,
  Clock,
  AlertCircle,
  FileSearch,
  CheckCircle,
  XCircle,
  ShieldCheck,
  Zap
} from 'lucide-react';

interface OversightItem {
  id: string;
  source: string;
  content: string;
  issue: string;
  time: string;
  priority: 'High' | 'Medium' | 'Low';
}

const HumanOversightQueue: React.FC = () => {
  const [items, setItems] = useState<OversightItem[]>([
    {
      id: 'it-456',
      source: 'TheologicalConsistencyChecker',
      content: 'Lesson 01 - Al-Fatiha',
      issue: 'Potential ambiguity in Tafsir of Surah Al-Fatiha verse 4.',
      time: '12m ago',
      priority: 'High'
    },
    {
      id: 'it-789',
      source: 'ContentQualityPredictor',
      content: 'Lesson 05 - Al-Anam',
      issue: 'Unverified historical reference found in source material.',
      time: '45m ago',
      priority: 'Medium'
    },
    {
      id: 'it-901',
      source: 'BiasDetector',
      content: 'Community Lesson - Hadith Context',
      issue: 'Regional dialect bias detected in audio sample (96% confidence).',
      time: '2h ago',
      priority: 'Low'
    }
  ]);

  const resolveItem = (id: string) => {
    setItems(items.filter(i => i.id !== id));
  };

  return (
    <div className="min-h-screen bg-[#0A0B10] text-white p-8">
      <header className="mb-12">
        <div className="flex items-center gap-3 mb-2">
          <UserCheck className="text-amber-500" size={24} />
          <span className="text-amber-500 font-mono tracking-widest text-sm uppercase">Scholar Realm :: Human Oversight</span>
        </div>
        <h1 className="text-4xl font-bold tracking-tight">AI Decision Oversight Queue</h1>
        <p className="text-slate-400 mt-2">v8.6 Critical Decisions Requiring Scholarly/Manual Verification</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3 space-y-4">
          {items.map(item => (
            <div key={item.id} className="bg-[#15171E] border border-slate-800 p-6 rounded-xl hover:border-slate-700 transition-all group">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${
                    item.priority === 'High' ? 'bg-red-500/10 text-red-500' :
                    item.priority === 'Medium' ? 'bg-amber-500/10 text-amber-500' :
                    'bg-blue-500/10 text-blue-500'
                  }`}>
                    <AlertCircle size={20} />
                  </div>
                  <div>
                    <div className="text-slate-500 text-[10px] uppercase font-mono tracking-wider">{item.source}</div>
                    <div className="text-lg font-bold">{item.content}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-slate-500 text-xs font-mono">
                  <Clock size={14} />
                  {item.time}
                </div>
              </div>

              <p className="text-slate-300 text-sm mb-6 bg-black/30 p-4 rounded-lg border border-slate-800/50 italic">
                "{item.issue}"
              </p>

              <div className="flex justify-between items-center">
                 <div className="flex gap-4">
                   <button
                     onClick={() => resolveItem(item.id)}
                     className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 rounded-lg hover:bg-emerald-500/20 text-sm transition-all"
                   >
                     <CheckCircle size={16} />
                     Approve AI Decision
                   </button>
                   <button
                     onClick={() => resolveItem(item.id)}
                     className="flex items-center gap-2 px-4 py-2 bg-red-500/10 border border-red-500/20 text-red-500 rounded-lg hover:bg-red-500/20 text-sm transition-all"
                   >
                     <XCircle size={16} />
                     Reject & Flag
                   </button>
                 </div>
                 <button type="button" onClick={() => alert(`XAI Trace\n\nIssue: ${item.issue}\nTime: ${item.time}`)} className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 text-slate-400 rounded-lg hover:bg-slate-800 text-sm transition-all">
                   <FileSearch size={16} />
                   View Full XAI Trace
                 </button>
              </div>
            </div>
          ))}

          {items.length === 0 && (
            <div className="flex flex-col items-center justify-center py-24 text-slate-500">
               <ShieldCheck size={48} className="mb-4 text-[#00FF85]" />
               <p className="font-mono text-sm">ALL CRITICAL AI DECISIONS VERIFIED</p>
               <p className="text-xs italic mt-1">Oversight Queue Empty (0 Pending Items)</p>
            </div>
          )}
        </div>

        <div className="space-y-6">
           <div className="bg-[#15171E] border border-slate-800 p-6 rounded-xl">
              <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Zap size={20} className="text-amber-500" />
                Workflow Stats
              </h3>
              <div className="space-y-4">
                 <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Items Pending</span>
                    <span className="text-2xl font-bold font-mono">{items.length}</span>
                 </div>
                 <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Mean TTR</span>
                    <span className="text-2xl font-bold font-mono text-[#00FF85]">1.4h</span>
                 </div>
                 <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Decisions Approved</span>
                    <span className="text-2xl font-bold font-mono">92.4%</span>
                 </div>
              </div>
           </div>

           <div className="bg-amber-500/5 border border-amber-500/10 p-6 rounded-xl italic text-xs text-amber-500 leading-relaxed">
              "Human-in-the-Loop oversight is mandatory for any theological content scoring below 0.95 or when sources are unverified. Scholar decisions are final and override AI-generated pathways."
           </div>
        </div>
      </div>
    </div>
  );
};

export default HumanOversightQueue;
