import React, { useState, useRef, useEffect } from 'react';
import { useStore } from '@workstation/shared';
import { User, Bell, Radio, FileText, BarChart3, Sparkles, ShieldCheck, X, Activity, MessageCircle, Brain, Zap, Clock, TrendingUp, Cpu, ChevronDown, Loader2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button, Badge } from './index';
import OrganismVitals from '@superapp/components/organism/OrganismVitals';
import NeuralLink from '@superapp/components/organism/NeuralLink';
import SpatioTemporal from '@superapp/components/organism/SpatioTemporal';

class ChannelBoundary extends React.Component<{ children: React.ReactNode }, { err: boolean }> {
  state = { err: false };
  static getDerivedStateFromError() { return { err: true }; }
  render() {
    if (this.state.err) return (
      <div className="p-8 text-center text-[10px] font-black uppercase text-slate-600 tracking-widest">
        Channel stream unavailable
      </div>
    );
    return this.props.children;
  }
}

// How long the expanded channel grid stays open with no interaction before it
// auto-collapses back to just the trigger button.
const AUTO_COLLAPSE_MS = 4000;

interface CommandCenterProps {
  /** Which way the channel grid should expand. Use "up" when the trigger sits
   * near the bottom of the screen (e.g. the footer) so the popup doesn't open
   * off-screen. Defaults to "down" for its original top-header placement. */
  dropDirection?: 'down' | 'up';
  /** When true, renders the channel tiles directly (no trigger button, no popup).
   * Use inside a panel/column where the grid should fill the available space. */
  tiled?: boolean;
}

export const CommandCenter: React.FC<CommandCenterProps> = ({ dropDirection = 'down', tiled = false }) => {
  const { currentMode } = useStore();
  const [open, setOpen] = useState(false);
  const [activeChannel, setActiveChannel] = useState<string | null>(null);
  const [queryInput, setQueryInput] = useState('');
  const [queryLog, setQueryLog] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  const collapseTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const scheduleCollapse = () => {
    if (collapseTimer.current) clearTimeout(collapseTimer.current);
    collapseTimer.current = setTimeout(() => setOpen(false), AUTO_COLLAPSE_MS);
  };

  const channels = [
    { id: 'avatar', name: 'Avatar', icon: User, color: 'text-aura', description: 'Real-time Interaction' },
    { id: 'notification', name: 'Notification', icon: Bell, color: 'text-highlight', description: 'System Alerts' },
    { id: 'signal', name: 'Signal', icon: Radio, color: 'text-vital', description: 'Agent Pheromones' },
    { id: 'summary', name: 'Summary', icon: FileText, color: 'text-aura', description: 'AI Reports' },
    { id: 'dashboard', name: 'Dashboard', icon: BarChart3, color: 'text-highlight', description: 'Live Metrics' },
    { id: 'predictive', name: 'Predictive', icon: Sparkles, color: 'text-vital', description: 'Forecasting' },
    { id: 'neural', name: 'Neural Link', icon: Zap, color: 'text-vital', description: 'L13 Interface' },
    { id: 'spatio', name: 'Spatio-Temporal', icon: Clock, color: 'text-aura', description: 'L14 Mapping' },
    { id: 'forge', name: 'Swarm Designer', icon: Cpu, color: 'text-aura', description: 'Opens Native AI' },
    { id: 'holo', name: 'Holo Forge', icon: Sparkles, color: 'text-highlight', description: '3D Immersion' },
    { id: 'ethical', name: 'Ethical', icon: ShieldCheck, color: 'text-aura', description: 'Constitutional AI' },
  ];

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(false);
        setActiveChannel(null);
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  useEffect(() => {
    setQueryInput('');
    setQueryLog([]);
  }, [activeChannel]);

  useEffect(() => {
    if (open) scheduleCollapse();
    return () => {
      if (collapseTimer.current) clearTimeout(collapseTimer.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // W491 (refutation) - this makes NO request: it appends the text to local state and clears the input.
  // Both branches labelled the control as sending a query and captioned the echo as a question asked, so
  // a user typing into a channel was told it had been sent and nothing ever answered. The labels now say what
  // the control does. Wiring it to a channel backend is separate work, not a label change.
  const handleSendQuery = () => {
    const text = queryInput.trim();
    if (!text) return;
    setQueryLog(prev => [...prev, text]);
    setQueryInput('');
  };

  // Tiled mode: fill the parent with a responsive grid of channel tiles, no trigger button.
  if (tiled) {
    return (
      <>
        <div className="grid grid-cols-2 gap-2 p-1 content-start">
          {channels.map((channel) => (
            <button
              key={channel.id}
              type="button"
              aria-label={channel.name}
              title={channel.description}
              onClick={() => setActiveChannel(channel.id)}
              className="flex flex-col items-center gap-2 p-3 rounded-2xl transition-all bg-slate-900/70 border border-slate-800/60 text-slate-500 hover:bg-slate-800 hover:text-white hover:border-slate-700 hover:scale-[1.03]"
            >
              <channel.icon size={18} className={channel.color} />
              <div className="text-center">
                <span className="text-[8px] font-black uppercase tracking-widest block leading-tight text-slate-300">{channel.name}</span>
                <span className="text-[7px] text-slate-600 font-bold leading-tight">{channel.description}</span>
              </div>
            </button>
          ))}
        </div>

        <AnimatePresence>
          {activeChannel && (
            <div
              className="fixed inset-0 z-[200] flex items-center justify-center p-8 bg-black/40"
              onClick={() => setActiveChannel(null)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                onClick={(e) => e.stopPropagation()}
                className="w-[480px] bg-slate-950/90 border border-aura/20 rounded-[3rem] shadow-2xl overflow-hidden backdrop-blur-3xl"
              >
                <div className="p-8 border-b border-white/5 bg-aura/5 flex justify-between items-center">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                      {(() => { const ch = channels.find(c => c.id === activeChannel); if (!ch) return null; const Icon = ch.icon; return <Icon size={24} />; })()}
                    </div>
                    <div>
                      <h3 className="text-xl font-black text-white uppercase tracking-tight">{activeChannel} Channel</h3>
                      <p className="text-[10px] font-black text-aura uppercase tracking-widest">Multi-Modal Fabric v3.0</p>
                    </div>
                  </div>
                  <button type="button" onClick={() => setActiveChannel(null)} aria-label="Close channel" title="Close channel" className="p-3 text-slate-500 hover:text-white hover:bg-white/5 rounded-2xl transition-all">
                    <X size={20} />
                  </button>
                </div>
                <div className="p-8 max-h-[600px] overflow-y-auto custom-scrollbar space-y-6">
                  <ChannelBoundary key={activeChannel}>
                    <ChannelContent id={activeChannel} />
                  </ChannelBoundary>
                  {queryLog.length > 0 && (
                    <div className="space-y-2 pt-4 border-t border-white/5">
                      {queryLog.map((q, i) => (
                        <div key={i} className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
                          <span className="text-slate-500 font-black uppercase text-[9px] tracking-widest block mb-1" data-testid="channel-note-label">Your note · not sent anywhere</span>
                          {q}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <div className="p-6 border-t border-white/5 bg-slate-950/50 flex gap-3">
                  <input
                    value={queryInput}
                    onChange={(e) => setQueryInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleSendQuery(); }}
                    placeholder={`Note to self about the ${activeChannel} channel...`}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl px-5 py-3 text-xs text-white focus:outline-none focus:border-aura/30"
                  />
                  <button type="button" onClick={handleSendQuery} disabled={!queryInput.trim()} data-testid="channel-note-keep" aria-label="Keep this note on screen" title="Keeps the note on this screen — nothing is sent and nothing answers" className="p-3 bg-aura text-sovereign rounded-2xl shadow-xl shadow-aura/20 hover:scale-110 transition-all disabled:opacity-30 disabled:hover:scale-100">
                    <MessageCircle size={20} />
                  </button>
                </div>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </>
    );
  }

  return (
    <>
    <div
      ref={containerRef}
      className="relative"
      onMouseEnter={() => { if (collapseTimer.current) clearTimeout(collapseTimer.current); }}
      onMouseLeave={() => { if (open) scheduleCollapse(); }}
    >
      <button
        type="button"
        onClick={() => setOpen(o => !o)}
        aria-label="Channels"
        title="Channels"
        className={`p-3 rounded-xl transition-all flex items-center gap-1 ${open ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura hover:scale-105'} ${currentMode === 'REST' ? 'grayscale-[50%] opacity-80' : ''}`}
      >
        {/* A STATIC three-bar glyph. W491 (FU-179): these bars used to animate continuously, which on a
            Channels control reads as live channel traffic - nothing here measures any. A control's icon
            names what the control does; it does not report activity it cannot see. */}
        <div className="flex items-end gap-0.5 h-5 w-5" aria-hidden="true">
          <span className="w-1 origin-bottom rounded-full bg-current h-[40%]" />
          <span className="w-1 origin-bottom rounded-full bg-current h-[70%]" />
          <span className="w-1 origin-bottom rounded-full bg-current h-[55%]" />
        </div>
        <ChevronDown size={12} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: dropDirection === 'up' ? 8 : -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: dropDirection === 'up' ? 8 : -8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className={`absolute left-0 w-80 p-3 rounded-3xl bg-slate-950/95 border border-slate-900 backdrop-blur-3xl shadow-2xl z-[110] grid grid-cols-3 gap-2 ${
              dropDirection === 'up' ? 'bottom-full mb-3' : 'top-full mt-3'
            }`}
          >
            {channels.map((channel) => (
              <button
                key={channel.id}
                type="button"
                aria-label={channel.name}
                title={channel.description}
                onClick={() => { setActiveChannel(channel.id); setOpen(false); }}
                className="flex flex-col items-center gap-2 p-3 rounded-2xl transition-all bg-slate-900 text-slate-500 hover:bg-slate-800 hover:text-white hover:scale-105"
              >
                <channel.icon size={20} />
                <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{channel.name}</span>
              </button>
            ))}

            <div className="col-span-3 h-px bg-slate-900 my-1" />

            <div className="col-span-3 flex items-center justify-center gap-2 pb-1">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
              <span className="text-[8px] font-black text-slate-700 uppercase tracking-widest">Live</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>

    <AnimatePresence>
       {activeChannel && (
         <div
           className="fixed inset-0 z-[200] flex items-center justify-center p-8 bg-black/40"
           onClick={() => setActiveChannel(null)}
         >
            <motion.div
               initial={{ opacity: 0, scale: 0.9 }}
               animate={{ opacity: 1, scale: 1 }}
               exit={{ opacity: 0, scale: 0.9 }}
               onClick={(e) => e.stopPropagation()}
               className="w-[480px] bg-slate-950/90 border border-aura/20 rounded-[3rem] shadow-2xl overflow-hidden backdrop-blur-3xl"
            >
               <div className="p-8 border-b border-white/5 bg-aura/5 flex justify-between items-center">
                  <div className="flex items-center gap-4">
                     <div className="w-12 h-12 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                        {(() => { const ch = channels.find(c => c.id === activeChannel); if (!ch) return null; const Icon = ch.icon; return <Icon size={24} />; })()}
                     </div>
                     <div>
                        <h3 className="text-xl font-black text-white uppercase tracking-tight">{activeChannel} Channel</h3>
                        <p className="text-[10px] font-black text-aura uppercase tracking-widest">Multi-Modal Fabric v3.0</p>
                     </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveChannel(null)}
                    aria-label="Close channel"
                    title="Close channel"
                    className="p-3 text-slate-500 hover:text-white hover:bg-white/5 rounded-2xl transition-all"
                  >
                     <X size={20} />
                  </button>
               </div>

               <div className="p-8 max-h-[600px] overflow-y-auto custom-scrollbar space-y-6">
                  <ChannelBoundary key={activeChannel}>
                    <ChannelContent id={activeChannel} />
                  </ChannelBoundary>

                  {queryLog.length > 0 && (
                    <div className="space-y-2 pt-4 border-t border-white/5">
                       {queryLog.map((q, i) => (
                         <div key={i} className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
                            <span className="text-slate-500 font-black uppercase text-[9px] tracking-widest block mb-1" data-testid="channel-note-label">Your note · not sent anywhere</span>
                            {q}
                         </div>
                       ))}
                    </div>
                  )}
               </div>

               <div className="p-6 border-t border-white/5 bg-slate-950/50 flex gap-3">
                  <input
                    value={queryInput}
                    onChange={(e) => setQueryInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleSendQuery(); }}
                    placeholder={`Note to self about the ${activeChannel} channel...`}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl px-5 py-3 text-xs text-white focus:outline-none focus:border-aura/30"
                  />
                  <button
                    type="button"
                    onClick={handleSendQuery}
                    disabled={!queryInput.trim()}
                    data-testid="channel-note-keep"
                    aria-label="Keep this note on screen"
                    title="Keeps the note on this screen — nothing is sent and nothing answers"
                    className="p-3 bg-aura text-sovereign rounded-2xl shadow-xl shadow-aura/20 hover:scale-110 transition-all disabled:opacity-30 disabled:hover:scale-100"
                  >
                     <MessageCircle size={20} />
                  </button>
               </div>
            </motion.div>
         </div>
       )}
    </AnimatePresence>
    </>
  );
};

const REALM_ORDER = ['LEARNER', 'DEVELOPER', 'ENTERPRISE', 'SCHOLAR', 'GENOME', 'UNIFIED'] as const;

const ChannelContent = ({ id }: { id: string }) => {
   const { currentRealm, currentMode, setCurrentRealm, setCurrentMode } = useStore();
   const [calibrating, setCalibrating] = useState(false);
   const [calibrated, setCalibrated] = useState(false);
   const [calibrateNote, setCalibrateNote] = useState('');
   const [suggestionDismissed, setSuggestionDismissed] = useState(false);
   const [restApplied, setRestApplied] = useState(false);

   const handleSwitchPersona = () => {
      const idx = REALM_ORDER.indexOf(currentRealm as any);
      const next = REALM_ORDER[(idx + 1) % REALM_ORDER.length];
      setCurrentRealm(next as any);
   };

   const handleCalibrateVoice = () => {
      // W475 (ledger v4 R4.0) — no voice pipeline exists: nothing is calibrated, and the button says so instead of
      // a 1.2 s timer that always ended 'Calibrated'.
      setCalibrating(false);
      setCalibrated(false);
      setCalibrateNote('Voice calibration is not built — nothing was calibrated');
   };

   const handleApplyRest = () => {
      setCurrentMode('REST');
      setRestApplied(true);
   };

   const contents: Record<string, any> = {
      avatar: (
         <div className="space-y-6 text-center">
            <div className="relative mx-auto w-40 h-40">
               <div className="absolute inset-0 rounded-full border-4 border-aura/20 animate-pulse-slow" />
               <div className="w-full h-full rounded-full bg-slate-900 border-2 border-aura flex items-center justify-center overflow-hidden">
                  <User size={80} className="text-aura opacity-30" />
               </div>
               <div className="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-emerald-500 border-4 border-slate-950 flex items-center justify-center">
                  <Activity size={14} className="text-white" />
               </div>
            </div>
            <div className="space-y-2">
               <h4 className="text-lg font-black text-white">Avatar — no stream connected</h4>
               <p className="text-xs text-slate-400 font-bold leading-relaxed px-6">
                  Nothing streams here and no latency is measured. Persona: <span className="text-aura uppercase tracking-widest">{currentRealm}</span>.
               </p>
            </div>
            <div className="grid grid-cols-2 gap-3">
               <Button variant="outline" className="text-[9px]" onClick={handleSwitchPersona}>Switch Persona</Button>
               <Button variant="outline" className="text-[9px]" onClick={handleCalibrateVoice} disabled={calibrating}>
                  {calibrating ? <Loader2 size={14} className="animate-spin" /> : calibrated ? <CheckCircle2 size={14} className="text-emerald-500" /> : null}
                  {calibrateNote || 'Calibrate Voice'}
               </Button>
            </div>
         </div>
      ),
      neural: (
         <div className="space-y-6">
            <NeuralLink />
         </div>
      ),
      spatio: (
         <div className="space-y-6">
            <SpatioTemporal />
         </div>
      ),
      predictive: (
         <div className="space-y-6">
            <div className="p-6 rounded-3xl bg-slate-900/50 border border-white/5 space-y-6">
               <div className="flex justify-between items-center">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Time-Series Forecast — not built</p>
                  <TrendingUp size={16} className="text-aura" />
               </div>
               <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">No forecast is computed — nothing streams into this channel</p>
               <div className="space-y-4">
                  <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                     <Activity size={18} className="text-vital" />
                     <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">No prediction is made — no model runs here.</p>
                  </div>
                  <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                     <Zap size={18} className="text-aura" />
                     <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">No energy telemetry is connected — nothing is detected.</p>
                  </div>
               </div>
            </div>

            {/* Proactive Suggestions Section */}
            {!suggestionDismissed && (
              <div className="space-y-4">
                 <div className="flex items-center gap-3">
                    <Brain size={18} className="text-aura" />
                    <h4 className="text-sm font-black text-white uppercase tracking-widest">RL-Powered Suggestions</h4>
                 </div>
                 <div className="p-6 rounded-3xl bg-aura/5 border border-aura/10 border-dashed space-y-4">
                    <p className="text-xs text-slate-400 font-bold leading-relaxed italic">
                       {restApplied
                         ? 'Rest Mode applied. Cognitive durability optimization in progress.'
                         : "Nothing measures your session length here — this suggestion is illustrative, not a reading: a REST transition after a long WORK stretch aids cognitive durability."}
                    </p>
                    <div className="flex gap-3">
                       <Button className="flex-1 text-[9px] py-2" onClick={handleApplyRest} disabled={restApplied}>
                          {restApplied ? 'Rest Mode Active' : 'Apply REST Mode'}
                       </Button>
                       <Button variant="ghost" className="text-[9px] py-2" onClick={() => setSuggestionDismissed(true)}>Dismiss</Button>
                    </div>
                 </div>
              </div>
            )}
         </div>
      ),
      forge: (
         <div className="space-y-4 p-6" data-testid="swarm-designer-card">
            {/* W460 (P1.12) — the Agent Forge canvas was retired: its nodes reached no swarm. */}
            <p className="text-sm text-slate-300 font-bold leading-relaxed">
               The swarm cascade designer is on Native AI: role + instruction stages, saved, editable and runnable;
               each stage reports which resource served it.
            </p>
            <Button className="w-full" onClick={() => { window.location.assign('/native-ai?focus=cascade-designer'); }}>Open the cascade designer</Button>
         </div>
      ),
      holo: (
         <div className="p-8 text-center space-y-4">
            <Sparkles size={32} className="text-highlight mx-auto opacity-50" />
            <p className="text-xs font-black text-slate-500 uppercase tracking-widest">3D holographic view — not built; nothing is loading</p>
         </div>
      ),
      dashboard: (
         <div className="space-y-6">
            <OrganismVitals />
         </div>
      ),
      ethical: (
         <div className="space-y-6">
            <div className="p-8 rounded-3xl bg-aura/5 border border-aura/20 relative overflow-hidden">
               <div className="absolute top-0 right-0 p-4 opacity-10">
                  <ShieldCheck size={60} className="text-aura" />
               </div>
               <p className="text-[10px] font-black text-aura uppercase tracking-widest mb-4">Constitutional Alignment</p>
               {/* W460 (P1.12) — this said the session "conforms to Floor 24 mandates", showed a green IDLE veto
                   window and a 0.08 / 0.1 privacy budget. Nothing evaluates a session; no veto window or ε budget
                   exists anywhere in the backend. */}
               <p className="text-sm text-white font-bold leading-relaxed relative z-10" data-testid="ethical-not-evaluated">
                  Per-session constitutional conformance is not evaluated. Actions routed through the gaas.v5 gate are
                  recorded on the UEG ledger — open the audit to read them.
               </p>
            </div>

            <Button variant="outline" className="w-full" onClick={() => { window.location.href = '/audit'; }}>View Full Ethical Audit</Button>
         </div>
      )
   };

   return contents[id] || (
      <div className="p-20 text-center space-y-6">
         <div className="w-16 h-16 rounded-2xl bg-slate-900 mx-auto flex items-center justify-center text-slate-700 animate-pulse">
            <Radio size={32} />
         </div>
         <p className="text-[10px] text-slate-600 font-black uppercase tracking-widest">
            No real-time stream is connected — nothing is initializing
         </p>
      </div>
   );
};
