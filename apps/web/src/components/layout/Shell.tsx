import React, { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CommandCenter } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';

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
    <div className="flex h-screen overflow-hidden bg-sovereign text-white font-inter">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      {/* Sidebar - Fixed Height and Independent Scroll */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Header - Occupies top row */}
        <Header wsStatus={wsStatus} />

        {/* Main Content Area - Independent Scroll */}
        <main className="flex-1 overflow-y-auto custom-scrollbar p-8">
          <div className="max-w-[1600px] mx-auto">
            {children(activeTab)}
          </div>
        </main>
      </div>
    </div>
  );
};
