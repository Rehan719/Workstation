import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { Dashboard } from './pages/Dashboard';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { AdminPanel } from './pages/AdminPanel';
import { Forge } from './pages/developers/Forge';
import { LearnerRealm } from './pages/learner/LearnerRealm';
import { EnterpriseRealm } from './pages/enterprise/EnterpriseRealm';
import { ScholarRealm } from './pages/scholar/ScholarRealm';
import { CFO } from './pages/c-suite/CFO';
import { KnowledgeHub } from './pages/coe/KnowledgeHub';
import { QEPEngine } from './pages/QEPEngine';
import { Introspection } from './pages/cognitive/Introspection';
import { Extrospection } from './pages/cognitive/Extrospection';
import { Evolution } from './pages/cognitive/Evolution';
import { FederationPortal } from './pages/federation/FederationPortal';
import { DAODashboard } from './pages/governance/DAODashboard';
import { Sanctum } from './pages/governance/Sanctum';
import { PredictionMarket } from './pages/markets/PredictionMarket';
import { CivilizationDashboard } from './pages/civilization/CivilizationDashboard';
import { RealityDashboard } from './pages/civilization/RealityDashboard';
import { SoulRecordExplorer } from './pages/profile/SoulRecordExplorer';
import { CosmicNervousSystem } from './pages/cosmic/CosmicNervousSystem';
import { CreatorStudio } from './pages/create/CreatorStudio';
import { Wallet } from './pages/profile/Wallet';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { PhysicalSymbiosis } from './pages/physical/PhysicalSymbiosis';
import { PublicRoadmap } from './pages/PublicRoadmap';
import { QuestLog } from './pages/quests/QuestLog';
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
        // Handle Realm-specific rendering
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
          case 'cfo': return <CFO />;
          case 'bto': return <BTOCatalog />;
          case 'coe': return <KnowledgeHub />;
          case 'qep': return <QEPEngine />;
          case 'mind':
          case 'introspection': return <Introspection />;
          case 'extrospection': return <Extrospection />;
          case 'evolution': return <Evolution />;
          case 'gov-facet':
          case 'fed-portal': return <FederationPortal />;
          case 'governance': return <DAODashboard />;
          case 'sanctum': return <Sanctum />;
          case 'wisdom': return <PredictionMarket />;
          case 'civilization': return <CivilizationDashboard />;
          case 'cosmic': return <CosmicNervousSystem />;
          case 'reality': return <RealityDashboard />;
          case 'eco-facet':
          case 'wallet': return <Wallet />;
          case 'marketplace': return <LivingMarketplace />;
          case 'iot': return <PhysicalSymbiosis />;
          case 'soul-record': return <SoulRecordExplorer />;
          case 'roadmap': return <PublicRoadmap />;
          case 'create': return <CreatorStudio />;
          case 'forge': return <Forge />;
          case 'quests': return <QuestLog />;
          case 'admin': return <AdminPanel />;
          default:
            return (
              <div className="flex items-center justify-center h-full text-center">
                <div>
                   <h2 className="text-2xl font-black text-slate-800 uppercase tracking-widest">Protocol v3.0</h2>
                   <p className="text-slate-500 mt-2">Accessing {activeTab} via Sovereign Mesh...</p>
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
