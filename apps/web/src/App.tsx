import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { Dashboard } from './pages/Dashboard';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { AdminPanel } from './pages/AdminPanel';
import { Forge } from './pages/developers/Forge';
import { DigitalReactor } from './pages/developers/DigitalReactor';
import { Incubator } from './pages/developers/Incubator';
import { LearnerRealm } from './pages/learner/LearnerRealm';
import { EnterpriseRealm } from './pages/enterprise/EnterpriseRealm';
import { OffspringManagement } from './pages/enterprise/OffspringManagement';
import { ScholarRealm } from './pages/scholar/ScholarRealm';
import { ConstitutionalUI } from './pages/governance/ConstitutionalUI';
import { CouncilInterface } from './pages/governance/CouncilInterface';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { QEPEngine } from './pages/QEPEngine';
import { useStore } from '@workstation/shared';
import { ThemeProvider } from './theme/ThemeContext';
import { PlayfulEffectsManager } from './components/gamification/PlayfulEffectsManager';

function App() {
  const { currentRealm } = useStore();

  return (
    <ThemeProvider>
    <PlayfulEffectsManager />
    <Shell>
      {(activeTab) => {
        // Multi-Realm Unified Dashboard
        if (activeTab === 'dashboard') {
          switch (currentRealm) {
            case 'LEARNER': return <LearnerRealm />;
            case 'DEVELOPER': return <Forge />;
            case 'ENTERPRISE': return <EnterpriseRealm />;
            case 'SCHOLAR': return <ScholarRealm />;
            default: return <Dashboard />;
          }
        }

        switch (activeTab) {
          case 'ceo': return <CEOChat />;
          case 'bto': return <BTOCatalog />;
          case 'forge': return <Forge />;
          case 'reactor': return <DigitalReactor />;
          case 'incubator': return <Incubator />;
          case 'offspring': return <OffspringManagement />;
          case 'qep': return <QEPEngine />;
          case 'constitution': return <ConstitutionalUI />;
          case 'council': return <CouncilInterface />;
          case 'marketplace': return <LivingMarketplace />;
          case 'admin': return <AdminPanel />;
          default:
            return (
              <div className="flex items-center justify-center h-full text-center">
                <div>
                   <h2 className="text-2xl font-black text-slate-800 uppercase tracking-widest">Sovereign Protocol v3.0</h2>
                   <p className="text-slate-500 mt-2">Converging {activeTab} via Eternal Mesh...</p>
                </div>
              </div>
            );
        }
      }}
    </Shell>
    </ThemeProvider>
  );
}

export default App;
