import React, { useState } from 'react';
import { Bell, Search, Activity, Zap, Sparkles, MessageCircle, X, Moon, Play, GraduationCap, Terminal, Briefcase, Microscope, Binary, LayoutDashboard, ShieldCheck, Loader2 } from 'lucide-react';
import { useStore } from '@workstation/shared';
import { useNavigate } from 'react-router-dom';
import type { UseAvatarSessionReturn } from '../../hooks/useAvatarSession';

interface HeaderProps {
  wsStatus?: 'CONNECTING' | 'CONNECTED' | 'DISCONNECTED';
  avatar: UseAvatarSessionReturn;
}

export const Header: React.FC<HeaderProps> = ({ wsStatus, avatar }) => {
  const { currentRealm, setCurrentRealm, currentMode, setCurrentMode, setCurrentTab } = useStore();
  const navigate = useNavigate();
  const [showAssistant, setShowAssistant] = useState(false);

  // This popup is a quick-access window onto the same real avatar session
  // that drives the footer (useAvatarSession, shared via Shell) — not a
  // separate, disconnected, canned-reply demo.
  const { messages, input, setInput, sending, sendMessage } = avatar;

  const realms: { id: typeof currentRealm; label: string; icon: any }[] = [
    { id: 'LEARNER', label: 'Learner', icon: GraduationCap },
    { id: 'DEVELOPER', label: 'Developer', icon: Terminal },
    { id: 'ENTERPRISE', label: 'Enterprise', icon: Briefcase },
    { id: 'SCHOLAR', label: 'Scholar', icon: Microscope },
    { id: 'GENOME', label: 'Genome', icon: Binary },
    { id: 'UNIFIED', label: 'Unified', icon: LayoutDashboard },
  ];

  const modes = [
    { id: 'ACTIVE' as const, label: 'Active', icon: Zap, color: 'text-aura' },
    { id: 'REST' as const, label: 'Rest', icon: Moon, color: 'text-highlight' },
    { id: 'EVOLUTION' as const, label: 'Evolution', icon: Play, color: 'text-vital' }
  ];

  return (
    <header className="h-20 shrink-0 border-b border-slate-800 px-8 flex items-center justify-between bg-sovereign/50 backdrop-blur-md z-50 sticky top-0">
      <div className="flex items-center gap-4">
        <div className="relative w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          <input
            type="text"
            placeholder="Query Planetary Mesh..."
            className="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-aura transition-colors font-bold text-white"
          />
        </div>

        <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 shadow-inner">
          {realms.map((r) => (
            <button
              key={r.id}
              type="button"
              onClick={() => setCurrentRealm(r.id)}
              className={`p-2 rounded-lg transition-all flex items-center gap-2 ${currentRealm === r.id ? 'bg-slate-800 shadow-lg border border-white/5' : 'opacity-40 hover:opacity-100'}`}
              title={`${r.label} Realm`}
            >
              <r.icon size={16} className={currentRealm === r.id ? 'text-aura' : 'text-slate-400'} />
              {currentRealm === r.id && <span className="text-[10px] font-black uppercase tracking-widest text-aura">{r.label}</span>}
            </button>
          ))}
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 shadow-inner">
           {modes.map((m) => (
             <button
               key={m.id}
               type="button"
               onClick={() => setCurrentMode(m.id)}
               className={`p-2.5 rounded-lg transition-all flex items-center gap-2 ${currentMode === m.id ? 'bg-slate-800 shadow-lg' : 'opacity-40 hover:opacity-100'}`}
               title={`${m.label} Mode`}
             >
                <m.icon size={16} className={m.id === currentMode ? m.color : 'text-slate-400'} />
                {currentMode === m.id && <span className={`text-[10px] font-black uppercase tracking-widest ${m.color}`}>{m.label}</span>}
             </button>
           ))}
        </div>

        <div className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-colors ${
          wsStatus === 'CONNECTED' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500' :
          wsStatus === 'CONNECTING' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-500' :
          'bg-vital/10 border-vital/30 text-vital'
        }`}>
          <Activity size={14} className={wsStatus === 'CONNECTING' ? 'animate-pulse' : ''} />
          <span className="text-[10px] font-black uppercase tracking-widest">
            {wsStatus === 'CONNECTED' ? 'Mesh Operational' :
             wsStatus === 'CONNECTING' ? 'Syncing Mesh...' :
             'Mesh Offline'}
          </span>
        </div>

        <button
          type="button"
          onClick={() => setShowAssistant(!showAssistant)}
          className={`p-3 rounded-xl transition-all ${showAssistant ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura hover:scale-105'}`}
          title="Toggle Sovereign Assistant"
          aria-label="Toggle Sovereign Assistant"
        >
          <Sparkles size={20} />
        </button>

        <button
          type="button"
          onClick={() => { setCurrentTab('audit'); navigate('/audit'); }}
          className="p-3 rounded-xl bg-slate-800 text-emerald-500 hover:scale-105 transition-all gaas-audit-btn"
          title="Constitutional Audit"
          aria-label="Constitutional Audit"
        >
          <ShieldCheck size={20} />
        </button>

        <button
          type="button"
          onClick={() => { setCurrentTab('transparency'); navigate('/transparency'); }}
          className="relative p-2 text-slate-400 hover:text-white transition-colors"
          title="View Notifications / Transparency"
          aria-label="View Notifications"
        >
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-aura rounded-full shadow-[0_0_8px_rgba(100,255,218,0.8)]"></span>
        </button>
      </div>

      {showAssistant && (
        <div className="fixed top-24 right-8 w-96 bg-slate-900 border border-aura/30 rounded-3xl shadow-2xl overflow-hidden z-[100] animate-in slide-in-from-right-4 duration-300">
           <div className="p-6 border-b border-white/10 bg-aura/5 flex justify-between items-center">
              <h3 className="font-black uppercase tracking-widest text-xs text-aura">Sovereign Assistant</h3>
              <button
                type="button"
                onClick={() => setShowAssistant(false)}
                aria-label="Close assistant"
                title="Close assistant"
                className="text-slate-500 hover:text-white"
              >
                <X size={16} />
              </button>
           </div>
           <div className="p-6 h-80 overflow-y-auto space-y-4 custom-scrollbar">
              {messages.length === 0 && (
                <div className="p-4 bg-slate-800/50 rounded-2xl border border-white/5 text-xs leading-relaxed text-slate-300">
                  Ask your avatar anything — this is a quick-access view of the same conversation shown in full at
                  the bottom of the screen.
                </div>
              )}
              {messages.map((m, i) => (
                <div key={i} className={`p-4 rounded-2xl border text-xs leading-relaxed ${m.role === 'user' ? 'bg-aura/10 border-aura/20 text-white' : 'bg-slate-800/50 border-white/5 text-slate-300'}`}>
                  {m.content}
                </div>
              ))}
              {sending && (
                <div className="flex items-center gap-2 text-[10px] text-slate-500 font-bold px-1">
                  <Loader2 size={12} className="animate-spin" /> Thinking...
                </div>
              )}
           </div>
           <div className="p-4 border-t border-white/10 bg-slate-950 flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') sendMessage(); }}
                placeholder="Ask your avatar..."
                className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-xs text-white"
              />
              <button
                type="button"
                onClick={() => sendMessage()}
                disabled={!input.trim() || sending}
                className="p-2 bg-aura text-sovereign rounded-lg disabled:opacity-40"
                title="Send Message"
                aria-label="Send Message"
              >
                <MessageCircle size={16} />
              </button>
           </div>
        </div>
      )}
    </header>
  );
};
