import React, { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CommandCenter } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';

interface ShellProps {
  children: (activeTab: string) => React.ReactNode;
}

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const activeTab = useStore(state => state.currentTab);
  const setActiveTab = useStore(state => state.setCurrentTab);
  const [commandOpen, setCommandOpen] = useState(false);
  const { updateSystemVitals, updateAgentVitals } = useStore();

  const { status: wsStatus } = useResilientWebSocket('ws://localhost:8000/api/v154/ws/streams', (data) => {
    if (data.type === 'SYSTEM_VITALS') {
      updateSystemVitals(data.payload);
    } else if (data.type === 'AGENT_SIGNAL') {
      console.log('Agent Signal Received:', data.payload);
    }
  });

  return (
    <div className="font-inter flex h-screen flex-col overflow-hidden bg-sovereign text-white">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      {/* Header - Occupies top row, 100% width, sticky-like via flex layout */}
      <Header wsStatus={wsStatus} />

      <div className="flex min-h-0 flex-1 overflow-hidden">
        <PanelGroup direction="horizontal">
          {/* Panel 1: Left Navigation (Collapsible, adjustable) */}
          <Panel defaultSize={20} minSize={15} collapsible className="flex">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
          </Panel>

          <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

          {/* Panel 2: Middle Workspace & Right Output (Main Content) */}
          <Panel defaultSize={80} minSize={30}>
            <PanelGroup direction="horizontal">
              {/* Middle Panel: Main Content */}
              <Panel defaultSize={60} minSize={30}>
                <main className="custom-scrollbar relative h-full overflow-y-auto p-8">
                  <div className="mx-auto max-w-full">
                    {children(activeTab)}
                  </div>
                </main>
              </Panel>

              <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

              {/* Right Panel: Output/Simulation Area */}
              <Panel defaultSize={40} minSize={15} collapsible>
                <aside className="custom-scrollbar h-full overflow-y-auto border-l border-slate-800 bg-slate-900/30 p-8">
                  <h3 className="mb-6 text-xs font-black uppercase tracking-widest text-aura">Sovereign Output</h3>
                  <div className="space-y-6">
                    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                      <p className="mb-2 text-[10px] font-bold uppercase text-slate-500">Simulation Engine</p>
                      <p className="text-xs italic text-slate-300">Ready for multi-modal synthesis.</p>
                    </div>
                  </div>
                </aside>
              </Panel>
            </PanelGroup>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
};
