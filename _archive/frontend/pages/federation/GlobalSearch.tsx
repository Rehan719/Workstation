import React, { useState } from 'react';
import axios from 'axios';
import { Search, Globe, ArrowUpRight } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';

export const GlobalSearch: React.FC = () => {
  const { theme } = useTheme();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    const res = await axios.get(`/api/v250/search/global?q=${query}`);
    setResults(res.data);
  };

  const isAdvanced = theme === 'advanced';

  return (
    <div className={`space-y-10 transition-all duration-1000 ${isAdvanced ? 'animate-in fade-in slide-in-from-bottom-4' : 'animate-in fade-in'}`} role="main" aria-label="Global Federated Search">
      <header>
        <h1 className="text-4xl font-black mb-2">Global Federated Search</h1>
        <p className="text-slate-500">Query the collective knowledge of the entire Workstation federation via UVIAP.</p>
      </header>

      <div className="relative max-w-3xl">
        <Search className={`absolute left-6 top-1/2 -translate-y-1/2 transition-colors ${isAdvanced ? 'text-aura' : 'text-slate-500'}`} />
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSearch()}
          placeholder="Search all federated nodes..."
          className={`w-full rounded-[2rem] py-6 pl-16 pr-8 text-xl focus:outline-none transition-all shadow-2xl ${
            isAdvanced
              ? 'bg-sovereign border-aura/30 focus:border-aura shadow-aura/10 text-white placeholder-slate-600'
              : 'bg-slate-900 border-slate-700 focus:border-aura text-white'
          }`}
          aria-label="Search all federated nodes"
        />
      </div>

      <div className="space-y-4">
        {results.map((r, i) => (
          <div key={i} className={`p-8 rounded-3xl border transition-all group ${
            isAdvanced
              ? 'bg-sovereign border-aura/10 hover:border-aura/50 shadow-lg'
              : 'bg-slate-900/40 border-slate-800 hover:border-aura'
          }`} role="article" aria-label={`Search result: ${r.title} from Node-${r.node}`}>
             <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                   <Globe size={18} className="text-aura" />
                   <span className={`text-xs font-black uppercase px-2 py-0.5 rounded ${
                     isAdvanced ? 'text-aura bg-aura/10' : 'text-slate-500 bg-slate-800'
                   }`}>Node-{r.node}</span>
                </div>
                <ArrowUpRight size={20} className={`transition-colors ${isAdvanced ? 'text-aura/50 group-hover:text-aura' : 'text-slate-700 group-hover:text-aura'}`} />
             </div>
             <h3 className="text-xl font-bold mb-2">{r.title}</h3>
             <div className="flex items-center gap-2">
                <progress value={r.relevance} max={1} aria-label={`Relevance ${(r.relevance * 100).toFixed(0)}%`}
                  className="flex-1 h-1 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
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
