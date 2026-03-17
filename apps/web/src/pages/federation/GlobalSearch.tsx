import React, { useState } from 'react';
import axios from 'axios';
import { Search, Globe, ArrowUpRight } from 'lucide-react';

export const GlobalSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    const res = await axios.get(`/api/v250/search/global?q=${query}`);
    setResults(res.data);
  };

  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      <header>
        <h1 className="text-4xl font-black mb-2">Global Federated Search</h1>
        <p className="text-slate-500">Query the collective knowledge of the entire Workstation federation via UVIAP.</p>
      </header>

      <div className="relative max-w-3xl">
        <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSearch()}
          placeholder="Search all federated nodes..."
          className="w-full bg-slate-900 border border-slate-700 rounded-[2rem] py-6 pl-16 pr-8 text-xl focus:outline-none focus:border-aura transition-all shadow-2xl"
        />
      </div>

      <div className="space-y-4">
        {results.map((r, i) => (
          <div key={i} className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 hover:border-aura transition-all group">
             <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                   <Globe size={18} className="text-aura" />
                   <span className="text-xs font-black uppercase text-slate-500 bg-slate-800 px-2 py-0.5 rounded">Node-{r.node}</span>
                </div>
                <ArrowUpRight size={20} className="text-slate-700 group-hover:text-aura transition-colors" />
             </div>
             <h3 className="text-xl font-bold mb-2">{r.title}</h3>
             <div className="flex items-center gap-2">
                <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
                   <div className="h-full bg-aura" style={{ width: `${r.relevance * 100}%` }}></div>
                </div>
                <span className="text-[10px] font-black text-slate-500">Relevance: {(r.relevance * 100).toFixed(0)}%</span>
             </div>
          </div>
        ))}
        {results.length === 0 && query && (
           <p className="p-20 text-center text-slate-600 font-bold uppercase tracking-widest italic">Awaiting Federated Synthesis...</p>
        )}
      </div>
    </div>
  );
};
