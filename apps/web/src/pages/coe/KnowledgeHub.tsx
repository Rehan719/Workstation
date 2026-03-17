import React from 'react';
import { Search, Book, FileText } from 'lucide-react';

export const KnowledgeHub: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Centers of Excellence</h1>
        <p className="text-slate-500">Federated knowledge hubs across the Workstation ecosystem.</p>
      </header>

      <div className="relative max-w-2xl">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Search CoE knowledge base..."
          className="w-full bg-slate-900 border border-slate-700 rounded-2xl py-4 pl-12 pr-6 text-lg focus:outline-none focus:border-aura transition-all"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {['AI Ethics', 'Data Science', 'Security', 'UX Design'].map(coe => (
          <div key={coe} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-aura transition-all group cursor-pointer">
            <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-4 group-hover:bg-aura group-hover:text-sovereign transition-colors">
              <Book size={24} />
            </div>
            <h3 className="text-lg font-bold mb-1">{coe} CoE</h3>
            <p className="text-xs text-slate-500">124 Articles • 12 Active Scholars</p>
          </div>
        ))}
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-bold">Latest Insights</h3>
        {[1, 2, 3].map(i => (
          <div key={i} className="flex items-center justify-between p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
            <div className="flex items-center gap-4">
              <FileText className="text-aura" />
              <div>
                <p className="font-bold">Constitutional Governance in Agentic Swarms</p>
                <p className="text-[10px] text-slate-500 font-bold uppercase">AI Ethics • 2 hours ago</p>
              </div>
            </div>
            <button className="text-xs font-bold text-aura hover:underline">Read Article</button>
          </div>
        ))}
      </div>
    </div>
  );
};
