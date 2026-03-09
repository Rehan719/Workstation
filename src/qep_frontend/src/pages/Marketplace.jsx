import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Rocket, Filter, ShieldCheck, Zap } from 'lucide-react';

const Marketplace = () => {
  const [search, setSearch] = useState('');

  const reactors = [
    // Science (8)
    { id: 'sci:physics', name: 'Physics Reactor', domain: 'Science', icon: '⚛️', status: 'GOLD' },
    { id: 'sci:chem', name: 'Chemistry Lab', domain: 'Science', icon: '🧪', status: 'GOLD' },
    { id: 'sci:bio', name: 'Biology Lab', domain: 'Science', icon: '🧬', status: 'GOLD' },
    { id: 'sci:compsci', name: 'CompSci Lab', domain: 'Science', icon: '💻', status: 'GOLD' },
    { id: 'sci:materials', name: 'Materials Science', domain: 'Science', icon: '💎', status: 'GOLD' },
    { id: 'sci:astro', name: 'Astronomy Reactor', domain: 'Science', icon: '🔭', status: 'GOLD' },
    { id: 'sci:math', name: 'Mathematics Reactor', domain: 'Science', icon: '➗', status: 'GOLD' },
    { id: 'sci:inter', name: 'Interdisciplinary', domain: 'Science', icon: '🧩', status: 'GOLD' },
    // Religion (8)
    { id: 'rel:tafsir', name: 'Tafsir Reactor', domain: 'Religion', icon: '📖', status: 'GOLD' },
    { id: 'rel:hadith', name: 'Hadith Sciences', domain: 'Religion', icon: '📜', status: 'GOLD' },
    { id: 'rel:fiqh', name: 'Fiqh Reactor', domain: 'Religion', icon: '⚖️', status: 'GOLD' },
    { id: 'rel:aqidah', name: 'Aqidah Reactor', domain: 'Religion', icon: '🛐', status: 'GOLD' },
    { id: 'rel:sirah', name: 'Sirah Reactor', domain: 'Religion', icon: '🕌', status: 'GOLD' },
    { id: 'rel:qiraat', name: 'Qiraat Reactor', domain: 'Religion', icon: '🎙️', status: 'GOLD' },
    { id: 'rel:dawah', name: 'Dawah Reactor', domain: 'Religion', icon: '📢', status: 'GOLD' },
    { id: 'rel:finance', name: 'Islamic Finance', domain: 'Religion', icon: '💰', status: 'GOLD' },
    // Law (8)
    { id: 'law:contract', name: 'Contract Smith', domain: 'Law', icon: '🖋️', status: 'GOLD' },
    { id: 'law:corp', name: 'Corporate Counsel', domain: 'Law', icon: '🏢', status: 'GOLD' },
    { id: 'law:ip', name: 'IP Counsel', domain: 'Law', icon: '🛡️', status: 'GOLD' },
    { id: 'law:lit', name: 'Litigation Reactor', domain: 'Law', icon: '🏛️', status: 'GOLD' },
    { id: 'law:reg', name: 'Regulatory Audit', domain: 'Law', icon: '📋', status: 'GOLD' },
    { id: 'law:tax', name: 'Tax Law Reactor', domain: 'Law', icon: '📉', status: 'GOLD' },
    { id: 'law:emp', name: 'Labor Law Reactor', domain: 'Law', icon: '🤝', status: 'GOLD' },
    { id: 'law:int', name: 'International Law', domain: 'Law', icon: '🌍', status: 'GOLD' },
    // Career (8)
    { id: 'emp:resume', name: 'Resume Pro', domain: 'Career', icon: '👔', status: 'GOLD' },
    { id: 'emp:cover', name: 'Cover Letter Pro', domain: 'Career', icon: '📝', status: 'GOLD' },
    { id: 'emp:link', name: 'LinkedIn Catalyst', domain: 'Career', icon: '🔗', status: 'GOLD' },
    { id: 'emp:int', name: 'Interview Coach', domain: 'Career', icon: '🎙️', status: 'GOLD' },
    { id: 'emp:path', name: 'Career Path Map', domain: 'Career', icon: '🗺️', status: 'GOLD' },
    { id: 'emp:job', name: 'Job Search Agent', domain: 'Career', icon: '🔍', status: 'GOLD' },
    { id: 'emp:skill', name: 'Skill Dev Reactor', domain: 'Career', icon: '⚡', status: 'GOLD' },
    { id: 'emp:brand', name: 'Branding Suite', domain: 'Career', icon: '🎨', status: 'GOLD' },
    // Education (8)
    { id: 'edu:k12', name: 'K-12 Academy', domain: 'Education', icon: '📚', status: 'GOLD' },
    { id: 'edu:high', name: 'Higher Ed Lab', domain: 'Education', icon: '🎓', status: 'GOLD' },
    { id: 'edu:voc', name: 'Vocational Prep', domain: 'Education', icon: '🛠️', status: 'GOLD' },
    { id: 'edu:lang', name: 'Language Lab', domain: 'Education', icon: '🗣️', status: 'GOLD' },
    { id: 'edu:stem', name: 'STEM Academy', domain: 'Education', icon: '🔬', status: 'GOLD' },
    { id: 'edu:hum', name: 'Humanities Suite', domain: 'Education', icon: '🎭', status: 'GOLD' },
    { id: 'edu:spec', name: 'Special Ed Suite', domain: 'Education', icon: '♿', status: 'GOLD' },
    { id: 'edu:teach', name: 'Teacher Support', domain: 'Education', icon: '👩‍🏫', status: 'GOLD' }
  ];

  return (
    <div className="space-y-8 p-8">
      <header>
        <h1 className="text-4xl font-black text-white mb-2">Reactor Marketplace</h1>
        <p className="text-slate-400">Browse and launch 46+ hyper-specialized sub-reactors (v100.0).</p>
      </header>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          <input
            type="text"
            placeholder="Search for capabilities (e.g. 'LaTeX', 'Sharia', 'ATS')..."
            className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white focus:outline-none focus:border-amber-500"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <button className="px-6 py-3 bg-white/5 border border-white/10 rounded-xl text-slate-300 flex items-center gap-2">
          <Filter size={18} /> Filters
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reactors.map(r => (
          <motion.div
            key={r.id}
            whileHover={{ y: -5 }}
            className="p-6 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl group cursor-pointer"
          >
             <div className="flex justify-between items-start mb-6">
               <div className="text-4xl">{r.icon}</div>
               <span className={`text-[8px] font-black px-2 py-1 rounded ${r.status === 'GOLD' ? 'bg-amber-500 text-slate-900' : 'bg-slate-800 text-slate-400'}`}>
                 {r.status}
               </span>
             </div>
             <h3 className="text-lg font-bold text-white mb-1 group-hover:text-amber-500 transition-colors">{r.name}</h3>
             <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">{r.domain}</p>

             <div className="flex gap-2 mb-6">
                <ShieldCheck size={14} className="text-emerald-500" />
                <Zap size={14} className="text-blue-500" />
             </div>

             <button className="w-full py-3 bg-white/5 group-hover:bg-amber-500 group-hover:text-slate-900 text-white rounded-xl text-xs font-black transition-all flex items-center justify-center gap-2">
               <Rocket size={14} /> Launch Sub-Reactor
             </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Marketplace;
