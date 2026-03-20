import React, { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CommandCenter } from '@workstation/ui';
import { useStore } from '@workstation/shared';

interface ShellProps {
  children: (activeTab: string) => React.ReactNode;
}

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [commandOpen, setCommandOpen] = useState(false);
  const { updateSystemVitals, updateAgentVitals } = useStore();

  useEffect(() => {
    // Connect to WebSocket Gateway
    const ws = new WebSocket('ws://localhost:8000/api/v154/ws/streams');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'SYSTEM_VITALS') {
        updateSystemVitals(data.payload);
      } else if (data.type === 'AGENT_SIGNAL') {
        console.log('Agent Signal Received:', data.payload);
        // Could update agent vitals or trigger UI effects
      }
    };

    ws.onopen = () => console.log('Sovereign Stream Connected');
    ws.onclose = () => console.log('Sovereign Stream Disconnected');

    return () => ws.close();
  }, [updateSystemVitals, updateAgentVitals]);

  return (
    <div className="flex min-h-screen bg-sovereign text-white font-inter">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="p-8 flex-1 ml-16">
          {children(activeTab)}
        </main>
      </div>
    </div>
  );
};
