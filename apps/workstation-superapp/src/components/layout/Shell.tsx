import React, { useState, useRef } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { RightDock } from './RightDock';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { AvatarWidget } from '../avatar/AvatarWidget';
import { VoiceVisualizer } from '../avatar/VoiceVisualizer';
import { ConversationPanel } from '../avatar/ConversationPanel';
import { useAvatarSession } from '../../hooks/useAvatarSession';
import { progressWidthClass, heightClass, FOOTER_MIN_HEIGHT_PX, FOOTER_MAX_HEIGHT_PX } from '../../lib/progressWidth';

interface ShellProps {
  children: (activeTab: string) => React.ReactNode;
}

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const activeTab = useStore(state => state.currentTab);
  const setActiveTab = useStore(state => state.setCurrentTab);
  const [commandOpen, setCommandOpen] = useState(false);
  const { updateSystemVitals } = useStore();

  // Single shared user<->avatar session, driving all three footer sections
  // (voice visualizer, conversation panel, avatar figure) plus the larger
  // Sovereign Output panel below — one real conversation, several views.
  const avatar = useAvatarSession();

  // Mirrors the live drag state of both panel groups so the full-width footer
  // below can size its three sections to match the panels above exactly.
  const [outerSizes, setOuterSizes] = useState<number[]>([20, 80]);
  const [innerSizes, setInnerSizes] = useState<number[]>([60, 40]);
  const leftPct = outerSizes[0] ?? 20;
  const restPct = outerSizes[1] ?? 80;
  const centerPct = (restPct * (innerSizes[0] ?? 60)) / 100;
  const rightPct = (restPct * (innerSizes[1] ?? 40)) / 100;

  // Draggable footer height — snapped to literal Tailwind height classes
  // (see lib/progressWidth.ts) so resizing never needs an inline style.
  const [footerHeightPx, setFooterHeightPx] = useState(96);
  const footerDragState = useRef<{ startY: number; startHeight: number } | null>(null);

  const handleFooterResizeStart = (e: React.MouseEvent) => {
    footerDragState.current = { startY: e.clientY, startHeight: footerHeightPx };
    const handleMove = (moveEvent: MouseEvent) => {
      if (!footerDragState.current) return;
      const delta = footerDragState.current.startY - moveEvent.clientY;
      const next = Math.max(FOOTER_MIN_HEIGHT_PX, Math.min(FOOTER_MAX_HEIGHT_PX, footerDragState.current.startHeight + delta));
      setFooterHeightPx(next);
    };
    const handleUp = () => {
      footerDragState.current = null;
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleUp);
    };
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
  };

  const { status: wsStatus } = useResilientWebSocket('ws://localhost:8000/api/v154/ws/streams', (data) => {
    if (data.type === 'SYSTEM_VITALS') {
      updateSystemVitals(data.payload);
    }
  });

  return (
    <div className="font-inter flex h-screen overflow-hidden bg-sovereign text-white">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <div className="flex flex-1 min-h-0 flex-col overflow-hidden">
        <Header wsStatus={wsStatus} avatar={avatar} />

        <div className="flex min-h-0 flex-1 overflow-hidden">
          <PanelGroup direction="horizontal" onLayout={setOuterSizes}>
            <Panel defaultSize={20} minSize={15} collapsible className="flex @container min-w-0">
              <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
            </Panel>

            <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

            <Panel defaultSize={80} minSize={30}>
              <PanelGroup direction="horizontal" onLayout={setInnerSizes}>

                {/* Center panel: page content only — the chat input now lives in the
                    full-width footer below, alongside its Voice/Avatar siblings. */}
                <Panel defaultSize={60} minSize={30} className="@container min-w-0">
                  <div className="flex flex-col h-full min-w-0">
                    <main className="custom-scrollbar relative flex-1 overflow-y-auto overflow-x-hidden p-8 min-w-0">
                      <div className="mx-auto max-w-full min-w-0">
                        {children(activeTab)}
                      </div>
                    </main>
                  </div>
                </Panel>

                <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

                {/* Right panel: Sovereign Output — a larger view of the same real
                    avatar conversation that lives in the footer, not a separate
                    simulated chat. */}
                <Panel defaultSize={40} minSize={15} collapsible className="@container min-w-0">
                  <aside className="flex flex-col h-full border-l border-slate-800 bg-slate-900/30 min-w-0">
                    <div className="shrink-0 px-8 pt-8 pb-4 flex items-center justify-between gap-3">
                      <h3 className="text-xs font-black uppercase tracking-widest text-aura truncate">Sovereign Output</h3>
                      {avatar.messages.length > 0 && (
                        <button
                          type="button"
                          onClick={avatar.clearConversation}
                          className="shrink-0 text-[9px] font-black uppercase tracking-widest text-slate-600 hover:text-slate-400 transition-colors"
                        >
                          Clear
                        </button>
                      )}
                    </div>

                    {avatar.messages.length === 0 && !avatar.sending ? (
                      <div className="flex-1 overflow-y-auto px-8 pb-8 space-y-6">
                        <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                          <p className="mb-2 text-[10px] font-bold uppercase text-slate-500">Simulation Engine</p>
                          <p className="text-xs italic text-slate-300">Ready for multi-modal synthesis.</p>
                        </div>
                        <div className="rounded-2xl border border-slate-800/50 bg-slate-950/40 p-4 space-y-3">
                          <p className="text-[10px] font-black uppercase tracking-widest text-slate-600">Avatar</p>
                          <p className="text-xs text-slate-500 leading-relaxed">
                            Type a query in the footer below to talk to your avatar. Responses appear here too.
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                            <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">L12 Fabric standby</span>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="flex-1 overflow-y-auto custom-scrollbar px-6 pb-6 space-y-4">
                        {avatar.messages.map((msg, i) => (
                          <div key={i} className={`flex flex-col gap-1 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                            <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 px-2">
                              {msg.role === 'user' ? 'You' : '⚡ Avatar'}
                            </span>
                            <div className={`max-w-[90%] rounded-2xl px-4 py-3 text-xs leading-relaxed font-medium ${
                              msg.role === 'user'
                                ? 'bg-aura/10 border border-aura/20 text-white rounded-tr-sm'
                                : 'bg-slate-950 border border-slate-800 text-slate-300 rounded-tl-sm'
                            }`}>
                              {msg.content}
                            </div>
                          </div>
                        ))}

                        {avatar.sending && (
                          <div className="flex flex-col gap-1 items-start">
                            <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 px-2">⚡ Avatar</span>
                            <div className="bg-slate-950 border border-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-2">
                              <div className="flex gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:0ms]" />
                                <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:150ms]" />
                                <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:300ms]" />
                              </div>
                              <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">Synthesizing…</span>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </aside>
                </Panel>

              </PanelGroup>
            </Panel>
          </PanelGroup>
        </div>

        {/* Drag handle to resize the footer's height */}
        <div
          onMouseDown={handleFooterResizeStart}
          className="h-1 shrink-0 cursor-row-resize bg-slate-900 transition-colors hover:bg-aura/30"
          role="separator"
          aria-orientation="horizontal"
          aria-label="Resize footer height"
        />

        {/* Full-width footer — three sections kept in sync with the panel widths
            above: left (real-time voice/sound interaction display, under the
            Sidebar), center (rich-text avatar conversation, under the Center
            panel), right (Avatar figure, under Sovereign Output). Height is
            user-resizable via the drag handle above. */}
        <div className={`flex ${heightClass(footerHeightPx)} shrink-0 border-t border-slate-800/60 bg-sovereign/60 backdrop-blur-sm`}>
          <div className={`${progressWidthClass(leftPct)} h-full shrink-0 px-4 py-3 border-r border-slate-800/40 @container min-w-0`}>
            <VoiceVisualizer avatar={avatar} />
          </div>

          <div className={`${progressWidthClass(centerPct)} h-full shrink-0 px-6 py-3 @container min-w-0`}>
            <ConversationPanel avatar={avatar} />
          </div>

          <div className={`${progressWidthClass(rightPct)} h-full shrink-0 px-4 py-3 border-l border-slate-800/40 @container min-w-0`}>
            <AvatarWidget avatar={avatar} />
          </div>
        </div>
      </div>

      <RightDock />
    </div>
  );
};
