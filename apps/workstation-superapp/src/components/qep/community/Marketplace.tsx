import React from 'react';
import { notImplemented } from '@workstation/ui';

interface Contribution {
  id: string;
  title: string;
  category: string;
  contributor: string;
  scholar_rating: number;
  community_rating: number;
  tags: string[];
}

const Marketplace: React.FC = () => {
  const [contributions, setContributions] = React.useState<Contribution[]>([
    {
      id: "CONT-001",
      title: "Extended Tajweed Audio Samples - Warsh",
      category: "Audio",
      contributor: "Qari-Ahmad-Warsh",
      scholar_rating: 4.9,
      community_rating: 4.8,
      tags: ["Tajweed", "Warsh", "Audio"]
    },
    {
      id: "CONT-002",
      title: "Intro to Quranic Arabic: Level 1 Interactive Exercises",
      category: "Interactive",
      contributor: "ArabicTeacher-Sarah",
      scholar_rating: 4.7,
      community_rating: 4.9,
      tags: ["Arabic", "Beginner", "Interactive"]
    }
  ]);

  return (
    <div className="marketplace-container p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-emerald-400">Community Marketplace</h2>
        <div className="filters flex gap-4">
          <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-sm border border-emerald-500/30">All Modules</span>
          <span className="px-3 py-1 bg-slate-800 text-slate-400 rounded-full text-sm border border-slate-700">Trending</span>
          <span className="px-3 py-1 bg-slate-800 text-slate-400 rounded-full text-sm border border-slate-700">New</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {contributions.map((item) => (
          <div key={item.id} className="contribution-card p-5 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-emerald-500/50 transition-all cursor-pointer group">
            <div className="flex justify-between items-start mb-4">
              <span className="text-xs font-mono text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded">{item.category}</span>
              <div className="flex items-center gap-1 text-yellow-500">
                <span className="text-sm font-bold">★ {item.scholar_rating}</span>
                <span className="text-[10px] text-slate-500">(Scholar Approved)</span>
              </div>
            </div>
            <h3 className="text-lg font-semibold group-hover:text-emerald-400 mb-2">{item.title}</h3>
            <p className="text-sm text-slate-400 mb-4">by <span className="text-emerald-500/80">{item.contributor}</span></p>

            <div className="flex flex-wrap gap-2 mb-6">
              {item.tags.map(tag => (
                <span key={tag} className="text-[10px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded">#{tag}</span>
              ))}
            </div>

            <button onClick={() => notImplemented('Integrate with My Portal')} className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded transition-colors text-sm shadow-lg shadow-emerald-900/20">
              Integrate with My Portal
            </button>
          </div>
        ))}
      </div>

      <div className="mt-12 p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-lg">
        <h4 className="text-emerald-400 font-bold mb-2 text-sm flex items-center gap-2">
          <span>💡</span> VSB Reusability Note
        </h4>
        <p className="text-xs text-slate-400 leading-relaxed">
          These mechanisms are cross-domain adaptable. Any VSB signature product can implement this marketplace pattern using the <code className="text-emerald-500/70">community_marketplace_plugin</code>.
        </p>
      </div>
    </div>
  );
};

export default Marketplace;
