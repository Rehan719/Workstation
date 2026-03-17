import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { Dashboard } from './pages/Dashboard';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { CFO } from './pages/c-suite/CFO';
import { KnowledgeHub } from './pages/coe/KnowledgeHub';
import { QEPEngine } from './pages/QEPEngine';
import { Introspection } from './pages/cognitive/Introspection';
import { Extrospection } from './pages/cognitive/Extrospection';
import { Evolution } from './pages/cognitive/Evolution';

function App() {
  return (
    <Shell>
      {(activeTab) => {
        switch (activeTab) {
          case 'dashboard':
            return <Dashboard />;
          case 'ceo':
            return <CEOChat />;
          case 'bto':
            return <BTOCatalog />;
          case 'coe':
            return <KnowledgeHub />;
          case 'qep':
            return <QEPEngine />;
          case 'introspection':
            return <Introspection />;
          case 'extrospection':
            return <Extrospection />;
          case 'evolution':
            return <Evolution />;
          default:
            return (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <h2 className="text-2xl font-black text-slate-700 uppercase tracking-widest">Module Under Construction</h2>
                  <p className="text-slate-500 mt-2">v138.0 protocol integration in progress.</p>
                </div>
              </div>
            );
        }
      }}
    </Shell>
  );
}

export default App;
