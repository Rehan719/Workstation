import React, { useState } from 'react';
import { Bell, Zap, Sparkles, MessageCircle, X, Moon, Play, ShieldCheck, Loader2 } from 'lucide-react';
import { useStore } from '@workstation/shared';
import { useNavigate } from 'react-router-dom';
import type { UseAvatarSessionReturn } from '../../hooks/useAvatarSession';

interface HeaderProps {
  avatar: UseAvatarSessionReturn;
}

const IDBOIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" className="w-7 h-7">
    {/* Outer field — organic irregular membrane, not a perfect circle */}
    <path d="M12 1 C16 0.5 20 4 21.5 8 C23 12 22 17 19.5 20 C17 23 13 24.5 9.5 23 C6 21.5 3 18 2 14 C1 10 2.5 5.5 5.5 3.5 C7.5 2 10 1.2 12 1 Z" strokeWidth="0.4" opacity="0.28" />
    {/* Dendrites — 6 organic C-bezier branches, asymmetric like real neurites */}
    <path d="M10 8.5 C9 6.5 7.5 4.5 6 2.5" strokeWidth="1.3" />
    <path d="M14 8 C15.5 6 17 4.5 18.5 2.5" strokeWidth="1.25" />
    <path d="M8.5 12 C6 11.5 3.5 11.2 1.5 11.5" strokeWidth="1.25" />
    <path d="M15.5 13.5 C18 14 20.5 14.5 22.5 14" strokeWidth="1.2" />
    <path d="M14 15.5 C15.5 18 17.5 20.5 19 22" strokeWidth="1.2" />
    <path d="M10 15.5 C8.5 18 7 20.5 6 22.5" strokeWidth="1.15" />
    {/* Secondary bifurcation — upper-left dendrite splits naturally */}
    <path d="M6 2.5 C5 1.5 4 0.8 3 0.5" strokeWidth="0.75" opacity="0.6" />
    <path d="M6 2.5 C6.2 1.5 6.8 0.8 7.5 0.5" strokeWidth="0.75" opacity="0.6" />
    {/* Synaptic terminals — filled dots, slightly varied sizes */}
    <circle cx="6" cy="2.5" r="1.35" fill="currentColor" fillOpacity="0.85" strokeWidth="0" />
    <circle cx="18.5" cy="2.5" r="1.35" fill="currentColor" fillOpacity="0.85" strokeWidth="0" />
    <circle cx="1.5" cy="11.5" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    <circle cx="22.5" cy="14" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    <circle cx="19" cy="22" r="1.25" fill="currentColor" fillOpacity="0.8" strokeWidth="0" />
    <circle cx="6" cy="22.5" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    {/* Cell soma — slightly oval, semi-transparent fill */}
    <ellipse cx="12" cy="12" rx="4.5" ry="4.3" strokeWidth="1.55" fill="currentColor" fillOpacity="0.11" />
    {/* Nucleus — slightly off-center for natural asymmetry */}
    <ellipse cx="11.8" cy="12" rx="2" ry="2.65" strokeWidth="1.05" />
    {/* DNA double helix — two interleaving S-curves */}
    <path d="M11 9.8 C12.5 10.7 11 11.5 12.5 12.4 C14 13.2 12 14 13 14.8" strokeWidth="0.65" />
    <path d="M13 9.8 C11.5 10.7 13 11.5 11.5 12.4 C10 13.2 12 14 11 14.8" strokeWidth="0.65" />
    {/* Mitochondrion — small organelle near soma edge */}
    <ellipse cx="18.5" cy="10.5" rx="1.5" ry="0.85" strokeWidth="0.7" transform="rotate(-30 18.5 10.5)" />
  </svg>
);

export const Header: React.FC<HeaderProps> = ({ avatar }) => {
  const { currentMode, setCurrentMode, setCurrentTab } = useStore();
  const navigate = useNavigate();
  const [showAssistant, setShowAssistant] = useState(false);
  const { messages, input, setInput, sending, sendMessage } = avatar;

  const modes = [
    { id: 'ACTIVE' as const, label: 'Active', icon: Zap, color: 'text-aura' },
    { id: 'REST' as const, label: 'Rest', icon: Moon, color: 'text-highlight' },
    { id: 'EVOLUTION' as const, label: 'Evolution', icon: Play, color: 'text-vital' }
  ];

  return (
    <header className="h-20 shrink-0 border-b border-slate-800 px-4 flex items-center gap-3 bg-sovereign/50 backdrop-blur-md z-50">

      {/* Brand identity — always at the far left, spanning the full header */}
      <div className="shrink-0 flex items-center gap-3 pr-4 border-r border-slate-800/60">
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-aura to-highlight flex items-center justify-center text-sovereign shadow-[0_0_18px_rgba(100,255,218,0.22)]">
          <IDBOIcon />
        </div>
        <div className="flex flex-col items-start">
          <h2 className="text-xl font-black tracking-tight text-white uppercase leading-none">Workstation</h2>
          <p className="text-[11px] uppercase tracking-[0.2em] text-aura font-black mt-1">v3.0 · IDBO</p>
        </div>
      </div>

      {/* Vision tagline — fills the space the legacy realm-selector occupied; the IDBO is one
          living organism navigated via the eight vision sections in the sidebar. */}
      <div className="flex-1 min-w-0 flex items-center px-3 overflow-hidden">
        <p className="text-[10px] font-black uppercase tracking-[0.22em] text-slate-600 truncate hidden md:block">
          One living in-house AI organism · Concept → Commercialise
        </p>
      </div>

      {/* Mode selector — shrink-0, labels auto-hide when needed */}
      <div className="shrink-0 flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 shadow-inner">
        {modes.map((m) => (
          <button
            key={m.id}
            type="button"
            onClick={() => setCurrentMode(m.id)}
            className={`flex items-center gap-1.5 py-2 px-2 rounded-lg transition-all ${currentMode === m.id ? 'bg-slate-800 shadow-lg' : 'opacity-40 hover:opacity-100'}`}
            title={`${m.label} Mode`}
          >
            <m.icon size={14} className={`shrink-0 ${m.id === currentMode ? m.color : 'text-slate-400'}`} />
            {currentMode === m.id && (
              <span className={`text-[9px] font-black uppercase tracking-widest ${m.color} hidden sm:block`}>{m.label}</span>
            )}
          </button>
        ))}
      </div>

      {/* Action buttons — shrink-0, grouped tightly on the right */}
      <div className="shrink-0 flex items-center gap-1.5">
        <button
          type="button"
          onClick={() => setShowAssistant(!showAssistant)}
          className={`p-2.5 rounded-xl transition-all ${showAssistant ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura hover:scale-105'}`}
          title="Toggle Sovereign Assistant"
          aria-label="Toggle Sovereign Assistant"
        >
          <Sparkles size={16} />
        </button>

        <button
          type="button"
          onClick={() => { setCurrentTab('audit'); navigate('/audit'); }}
          className="p-2.5 rounded-xl bg-slate-800 text-emerald-500 hover:scale-105 transition-all gaas-audit-btn"
          title="Constitutional Audit"
          aria-label="Constitutional Audit"
        >
          <ShieldCheck size={16} />
        </button>

        <button
          type="button"
          onClick={() => { setCurrentTab('transparency'); navigate('/transparency'); }}
          className="relative p-2 text-slate-400 hover:text-white transition-colors"
          title="View Notifications / Transparency"
          aria-label="View Notifications"
        >
          <Bell size={16} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-aura rounded-full shadow-[0_0_8px_rgba(100,255,218,0.8)]"></span>
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
                Ask your avatar anything — this is a quick-access view of the same conversation shown in full at the bottom of the screen.
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
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') sendMessage(); }}
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
