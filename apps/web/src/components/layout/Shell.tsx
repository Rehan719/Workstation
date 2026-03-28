import React, { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CommandCenter } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';
import {
  Panel,
  PanelGroup,
  PanelResizeHandle,
} from 'react-resizable-panels';

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
    <div className="flex flex-col h-screen overflow-hidden bg-sovereign text-white font-inter">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      {/* Header - Occupies top row, 100% width, sticky-like via flex layout */}
      <Header wsStatus={wsStatus} />

      <div className="flex-1 flex min-h-0 overflow-hidden">
        <PanelGroup direction="horizontal">
          {/* Panel 1: Left Navigation (Collapsible, adjustable) */}
          <Panel defaultSize={20} minSize={15} collapsible className="flex">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
          </Panel>

          <PanelResizeHandle className="w-1 bg-slate-900 hover:bg-aura/30 transition-colors cursor-col-resize" />

          {/* Panel 2: Middle Workspace & Right Output (Main Content) */}
          <Panel defaultSize={80} minSize={30}>
            <PanelGroup direction="horizontal">
              {/* Middle Panel: Main Content */}
              <Panel defaultSize={60} minSize={30}>
                <main className="h-full overflow-y-auto custom-scrollbar p-8 relative">
                  <div className="max-w-full mx-auto">
                    {children(activeTab)}
                  </div>
                </main>
              </Panel>

              <PanelResizeHandle className="w-1 bg-slate-900 hover:bg-aura/30 transition-colors cursor-col-resize" />

              {/* Right Panel: Output/Simulation Area */}
              <Panel defaultSize={40} minSize={15} collapsible>
                <aside className="h-full bg-slate-900/30 border-l border-slate-800 p-8 overflow-y-auto custom-scrollbar">
                  <h3 className="text-xs font-black uppercase tracking-widest text-aura mb-6">Sovereign Output</h3>
                  <div className="space-y-6">
                    <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
                      <p className="text-[10px] text-slate-500 font-bold uppercase mb-2">Simulation Engine</p>
                      <p className="text-xs text-slate-300 italic">Ready for multi-modal synthesis.</p>
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
