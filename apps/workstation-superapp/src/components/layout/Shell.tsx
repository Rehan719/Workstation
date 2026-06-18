import React, { useState, useRef } from 'react';
import { useWorkstationBiometrics } from '../../hooks/useWorkstationBiometrics';
import { BiometricStatus } from '../BiometricStatus';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { FourthColumn } from './FourthColumn';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';
import { Panel, PanelGroup, PanelResizeHandle, type ImperativePanelHandle } from 'react-resizable-panels';
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

  const avatar = useAvatarSession();

  // Track inner panel sizes so footer sections align with panels above
  const [innerSizes, setInnerSizes] = useState<number[]>([60, 30, 10]);

  const [isFourthCollapsed, setIsFourthCollapsed] = useState(true);
  const fourthPanelRef = useRef<ImperativePanelHandle>(null);

  const toggleFourthColumn = () => {
    if (isFourthCollapsed) {
      fourthPanelRef.current?.resize(20);
      setIsFourthCollapsed(false);
    } else {
      fourthPanelRef.current?.collapse();
      setIsFourthCollapsed(true);
    }
  };

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

  const biometrics = useWorkstationBiometrics();

  const _wsBase = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/^http/, 'ws');
  useResilientWebSocket(`${_wsBase}/api/v154/ws/streams`, (data) => {
    if (data.type === 'SYSTEM_VITALS') {
      updateSystemVitals(data.payload);
    }
  });

  return (
    <div className="font-inter flex flex-col h-screen overflow-hidden bg-sovereign text-white">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <Header avatar={avatar} />

      {/* Root horizontal split: sidebar | right content */}
      <div className="flex-1 min-h-0 overflow-hidden">
      <PanelGroup direction="horizontal" className="h-full">
        <Panel defaultSize={20} minSize={12} collapsible className="flex @container min-w-0">
          <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        </Panel>

        <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

        {/* Right side: content panels + resizable footer, stacked vertically */}
        <Panel defaultSize={80} minSize={30} className="flex flex-col min-h-0 min-w-0 overflow-hidden">
          <div className="flex min-h-0 flex-1 overflow-hidden">
            <PanelGroup direction="horizontal" onLayout={setInnerSizes}>

              {/* Center: page content */}
              <Panel defaultSize={65} minSize={30} className="@container min-w-0">
                <div className="flex flex-col h-full min-w-0">
                  <main className="custom-scrollbar relative flex-1 overflow-y-auto overflow-x-hidden p-8 min-w-0">
                    <div className="mx-auto max-w-full min-w-0">
                      {children(activeTab)}
                    </div>
                  </main>
                </div>
              </Panel>

              <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

              {/* Sovereign Output */}
              <Panel defaultSize={30} minSize={15} collapsible className="@container min-w-0">
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
                    <div className="flex-1 overflow-y-auto custom-scrollbar px-8 pb-8 space-y-6">
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

              <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

              {/* Fourth column */}
              <Panel
                ref={fourthPanelRef}
                collapsible
                collapsedSize={5}
                defaultSize={5}
                minSize={5}
                onCollapse={() => setIsFourthCollapsed(true)}
                onExpand={() => setIsFourthCollapsed(false)}
                className="@container min-w-0"
              >
                <FourthColumn isCollapsed={isFourthCollapsed} onToggle={toggleFourthColumn} />
              </Panel>

            </PanelGroup>
          </div>

          {/* Drag handle to resize footer height */}
          <div
            onMouseDown={handleFooterResizeStart}
            className="h-1 shrink-0 cursor-row-resize bg-slate-900 transition-colors hover:bg-aura/30"
            role="separator"
            aria-orientation="horizontal"
            aria-label="Resize footer height"
          />

          {/* Footer — three sections aligned with the inner panels above */}
          <div className={`flex ${heightClass(footerHeightPx)} shrink-0 border-t border-slate-800/60 bg-sovereign/60 backdrop-blur-sm`}>
            <div className={`${progressWidthClass(innerSizes[0] ?? 60)} h-full shrink-0 flex items-center justify-center @container min-w-0`}>
              <ConversationPanel avatar={avatar} />
            </div>

            <div className={`${progressWidthClass(innerSizes[1] ?? 30)} h-full shrink-0 flex items-center justify-center gap-3 px-3 border-l border-slate-800/40 min-w-0 overflow-hidden`}>
              <div className="h-[78%] aspect-square shrink-0 min-h-0 opacity-70">
                <AvatarWidget avatar={avatar} />
              </div>
              <div className="h-full w-[28%] max-w-[80px] min-w-[44px] shrink-0 py-1.5 opacity-60">
                <VoiceVisualizer avatar={avatar} />
              </div>
            </div>

            <div className={`${isFourthCollapsed ? 'w-14' : progressWidthClass(innerSizes[2] ?? 10)} min-w-[3.5rem] h-full shrink-0 flex items-center justify-center border-l border-slate-800/60 @container overflow-hidden`}>
              <BiometricStatus biometrics={biometrics} compact={true} />
            </div>
          </div>

        </Panel>
      </PanelGroup>
      </div>
    </div>
  );
};
