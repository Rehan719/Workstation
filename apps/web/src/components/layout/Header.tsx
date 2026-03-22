import React, { useState, useEffect } from 'react';
import { Bell, Search, Activity, ChevronDown, Zap, Sparkles, MessageCircle, X, Shield, Star, Award, Moon, Sun, Play } from 'lucide-react';
import { useModeStore } from '../../store/modeStore';
import { useStore } from '@workstation/shared';

export const Header: React.FC = () => {
  const { currentRealm, setCurrentRealm } = useStore();
  const [showAssistant, setShowAssistant] = useState(false);
  const [activeMode, setActiveMode] = useState('WORK');

  const modes = [
    { id: 'WORK', icon: Zap, color: 'text-aura' },
    { id: 'REST', icon: Moon, color: 'text-highlight' },
    { id: 'PLAY', icon: Play, color: 'text-vital' }
  ];

  return (
    <header className="h-20 border-b border-slate-800 px-8 flex items-center justify-between bg-sovereign/50 backdrop-blur-md sticky top-0 z-20">
      <div className="relative w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
        <input
          type="text"
          placeholder="Query Planetary Mesh..."
          className="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-aura transition-colors font-bold text-white"
        />
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 shadow-inner">
           {modes.map((m) => (
             <button
               key={m.id}
               onClick={() => setActiveMode(m.id)}
               className={`p-2.5 rounded-lg transition-all flex items-center gap-2 ${activeMode === m.id ? 'bg-slate-800 shadow-lg' : 'opacity-40 hover:opacity-100'}`}
               title={`${m.id} Mode`}
             >
                <m.icon size={16} className={m.id === activeMode ? m.color : 'text-slate-400'} />
                {activeMode === m.id && <span className={`text-[10px] font-black uppercase tracking-widest ${m.color}`}>{m.id}</span>}
             </button>
           ))}
        </div>

        <div className="h-8 w-px bg-slate-800 mx-2" />

        <div className="flex items-center gap-2 px-4 py-2 bg-vital/10 border border-vital/30 rounded-full">
          <Activity size={14} className="text-vital" />
          <span className="text-[10px] font-black text-vital uppercase tracking-widest">Mesh Operational</span>
        </div>

        <button
          onClick={() => setShowAssistant(!showAssistant)}
          className={`p-3 rounded-xl transition-all ${showAssistant ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura hover:scale-105'}`}
        >
          <Sparkles size={20} />
        </button>

        <button className="relative p-2 text-slate-400 hover:text-white transition-colors">
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-aura rounded-full shadow-[0_0_8px_rgba(100,255,218,0.8)]"></span>
        </button>
      </div>

      {showAssistant && (
        <div className="fixed top-24 right-8 w-96 bg-slate-900 border border-aura/30 rounded-3xl shadow-2xl overflow-hidden z-[100] animate-in slide-in-from-right-4 duration-300">
           <div className="p-6 border-b border-white/10 bg-aura/5 flex justify-between items-center">
              <h3 className="font-black uppercase tracking-widest text-xs text-aura">Sovereign Assistant</h3>
              <button onClick={() => setShowAssistant(false)} className="text-slate-500 hover:text-white">
                <X size={16} />
              </button>
           </div>
           <div className="p-6 h-80 overflow-y-auto space-y-4 custom-scrollbar">
              <div className="p-4 bg-slate-800/50 rounded-2xl border border-white/5 text-xs leading-relaxed text-slate-300">
                L12 Multi-Modal Fabric Active. Mesh latency is currently 28ms. How can I assist with your v3.0 operation?
              </div>
           </div>
           <div className="p-4 border-t border-white/10 bg-slate-950 flex gap-2">
              <input placeholder="Ask the mesh..." className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-xs text-white" />
              <button className="p-2 bg-aura text-sovereign rounded-lg"><MessageCircle size={16} /></button>
           </div>
        </div>
      )}
    </header>
  );
};
