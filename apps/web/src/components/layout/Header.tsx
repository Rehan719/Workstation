import React, { useState, useEffect } from 'react';
import { Bell, Search, Activity, ChevronDown, Zap, Sparkles, MessageCircle, X, Shield, Star, Award } from 'lucide-react';
import { useModeStore } from '../../store/modeStore';
import { useGamificationStore } from '../../store/gamificationStore';

export const Header: React.FC = () => {
  const { stats, fetchStats } = useGamificationStore();
  const { currentMode, setMode } = useModeStore();
  const [showAssistant, setShowAssistant] = useState(false);
  const [showGovernance, setShowGovernance] = useState(false);

  useEffect(() => {
    fetchStats('guardian');
  }, []);

  return (
    <header className="h-20 border-b border-slate-800 px-8 flex items-center justify-between bg-sovereign/50 backdrop-blur-md sticky top-0 z-20">
      <div className="relative w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
        <input
          type="text"
          placeholder="Search ecosystem..."
          aria-label="Search ecosystem"
          className="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-aura transition-colors font-bold"
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-50">
           <span className="text-[10px] font-black border border-white/20 px-1 rounded">⌘</span>
           <span className="text-[10px] font-black border border-white/20 px-1 rounded">K</span>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div
          className="relative group cursor-pointer"
          onMouseEnter={() => setShowGovernance(true)}
          onMouseLeave={() => setShowGovernance(false)}
        >
          <div className="flex items-center gap-2 p-3 bg-sovereign/40 border border-aura/30 rounded-xl hover:border-aura/60 transition-all shadow-lg shadow-aura/5">
             <Shield size={18} className="text-aura" />
             <span className="text-[10px] font-black uppercase tracking-widest text-aura">VSB</span>
          </div>
          {showGovernance && (
            <div className="absolute top-full left-0 mt-4 w-72 p-6 glass-card bg-sovereign/95 backdrop-blur-2xl border-aura/30 shadow-2xl z-[100] animate-in fade-in zoom-in-95 duration-300">
               <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-6">Governance Hierarchy</h4>
               <div className="space-y-6">
                  <div className="flex items-center gap-4">
                     <div className="w-8 h-8 rounded-lg bg-aura/20 border border-aura/40 flex items-center justify-center text-aura font-black text-xs shadow-[0_0_15px_rgba(100,255,218,0.2)]">E</div>
                     <div>
                        <p className="text-xs font-black text-white uppercase tracking-wider">The Entity</p>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Supervision Layer</p>
                     </div>
                  </div>
                  <div className="ml-4 h-6 border-l border-aura/20"></div>
                  <div className="flex items-center gap-4">
                     <div className="w-8 h-8 rounded-lg bg-vital/20 border border-vital/40 flex items-center justify-center text-vital font-black text-xs shadow-[0_0_15px_rgba(255,82,82,0.2)]">V</div>
                     <div>
                        <p className="text-xs font-black text-white uppercase tracking-wider">Virtual Sovereign Business</p>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Ownership & Assets</p>
                     </div>
                  </div>
                  <div className="ml-4 h-6 border-l border-vital/20"></div>
                  <div className="flex items-center gap-4">
                     <div className="w-8 h-8 rounded-lg bg-highlight/20 border border-highlight/40 flex items-center justify-center text-highlight font-black text-xs shadow-[0_0_15px_rgba(255,215,64,0.2)]">CEO</div>
                     <div>
                        <p className="text-xs font-black text-white uppercase tracking-wider">AI CEO & C-Suite</p>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Leadership & Strategy</p>
                     </div>
                  </div>
                  <div className="ml-4 h-6 border-l border-highlight/20"></div>
                  <div className="flex items-center gap-4">
                     <div className="w-8 h-8 rounded-lg bg-white/10 border border-white/20 flex items-center justify-center text-slate-400 font-black text-xs shadow-[0_0_15px_rgba(255,255,255,0.1)]">CoE</div>
                     <div>
                        <p className="text-xs font-black text-white uppercase tracking-wider">Centers of Excellence</p>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Sovereign Support</p>
                     </div>
                  </div>
               </div>
            </div>
          )}
        </div>

        <div className="flex items-center gap-6 px-4 py-2 bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-inner">
           <div className="flex items-center gap-3">
              <div className="p-2 bg-aura/20 rounded-lg text-aura">
                <Star size={16} fill="currentColor" />
              </div>
              <div className="text-right">
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Level {stats.level}</p>
                <div className="w-24 h-1.5 bg-slate-800 rounded-full mt-1 overflow-hidden border border-white/5">
                   <div className="h-full bg-aura shadow-[0_0_10px_rgba(100,255,218,0.5)]" style={{ width: `${(stats.xp % 100)}%` }}></div>
                </div>
              </div>
           </div>

           <div className="flex gap-2">
              {stats.badges.map((b: string) => (
                <div key={b} className="p-2 bg-vital/20 rounded-lg text-vital border border-vital/30 hover:scale-110 transition-transform cursor-help" title={`Badge Earned: ${b}`}>
                   <Award size={16} />
                </div>
              ))}
           </div>
        </div>

        <div className="flex items-center gap-3 bg-slate-900 border border-slate-700 px-4 py-2 rounded-xl group cursor-pointer relative">
          <Zap size={14} className="text-highlight" />
          <span className="text-xs font-bold uppercase tracking-widest">{currentMode} Mode</span>
          <ChevronDown size={14} className="text-slate-500" />

          <div className="absolute top-full right-0 mt-2 w-48 bg-slate-900 border border-slate-700 rounded-xl overflow-hidden hidden group-hover:block z-50 shadow-2xl">
            {['strategic', 'research', 'operational'].map(m => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className="w-full text-left px-4 py-3 text-xs font-bold uppercase hover:bg-aura hover:text-sovereign transition-colors"
              >
                {m}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2 px-4 py-2 bg-vital/10 border border-vital/30 rounded-full">
          <Activity size={14} className="text-vital" />
          <span className="text-[10px] font-black text-vital uppercase tracking-widest">System Operational</span>
        </div>

        <button
          onClick={() => setShowAssistant(!showAssistant)}
          aria-label="Toggle Civilization Assistant"
          title="Civilization Assistant"
          className={`p-3 rounded-xl transition-all ${showAssistant ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura hover:scale-105'}`}
        >
          <Sparkles size={20} />
        </button>

        <button
          className="relative p-2 text-slate-400 hover:text-white transition-colors"
          aria-label="View Notifications"
          title="Notifications"
        >
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-highlight rounded-full"></span>
        </button>
      </div>

      {showAssistant && (
        <div className="fixed top-24 right-8 w-96 bg-slate-900 border border-aura/30 rounded-3xl shadow-2xl overflow-hidden z-[100] animate-in slide-in-from-right-4 duration-300">
           <div className="p-6 border-b border-white/10 bg-aura/5 flex justify-between items-center">
              <h3 className="font-black uppercase tracking-widest text-xs text-aura">Civilization Assistant</h3>
              <button onClick={() => setShowAssistant(false)} className="text-slate-500 hover:text-white" aria-label="Close Assistant">
                <X size={16} />
              </button>
           </div>
           <div className="p-6 h-80 overflow-y-auto space-y-4 custom-scrollbar">
              <div className="p-4 bg-slate-800/50 rounded-2xl border border-white/5 text-xs leading-relaxed text-slate-300">
                Greetings, Guardian. I am the Civilization Intelligence layer. I recommend voting on **AMD-146** to optimize node resonance.
              </div>
           </div>
           <div className="p-4 border-t border-white/10 bg-slate-950 flex gap-2">
              <input
                placeholder="Ask the civilization..."
                aria-label="Message Assistant"
                className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-xs"
              />
              <button className="p-2 bg-aura text-sovereign rounded-lg" aria-label="Send Message"><MessageCircle size={16} /></button>
           </div>
        </div>
      )}
    </header>
  );
};
