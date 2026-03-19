import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';

interface ShellProps {
  children: (activeTab: string) => React.ReactNode;
}

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [commandOpen, setCommandOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-sovereign text-white font-inter">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="p-8 flex-1">
          {children(activeTab)}
        </main>
      </div>
    </div>
  );
};
