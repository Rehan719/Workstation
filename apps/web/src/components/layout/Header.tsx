import React from 'react';
import { Bell, Search, Activity } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-20 border-b border-slate-800 px-8 flex items-center justify-between bg-sovereign/50 backdrop-blur-md sticky top-0 z-20">
      <div className="relative w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
        <input
          type="text"
          placeholder="Search ecosystem..."
          className="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-aura transition-colors"
        />
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 px-4 py-2 bg-vital/10 border border-vital/30 rounded-full">
          <Activity size={14} className="text-vital" />
          <span className="text-[10px] font-black text-vital uppercase tracking-widest">System Operational</span>
        </div>

        <button className="relative p-2 text-slate-400 hover:text-white transition-colors">
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-highlight rounded-full"></span>
        </button>
      </div>
    </header>
  );
};
