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
    <div className="flex flex-col h-screen overflow-hidden bg-sovereign text-white font-inter">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      {/* Header - Occupies top row, 100% width */}
      <Header wsStatus={wsStatus} />

      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Sidebar - Sibling to main content */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Content Area - Independent Scroll */}
        <main className="flex-1 overflow-y-auto custom-scrollbar p-8 relative">
          <div className="max-w-[1600px] mx-auto">
            {children(activeTab)}
          </div>
        </main>
      </div>
    </div>
  );
};
