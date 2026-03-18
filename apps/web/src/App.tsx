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
import { LearningDashboard } from './pages/evolution/LearningDashboard';
import { EvolutionProposals } from './pages/evolution/Proposals';
import { Contribute } from './pages/Contribute';
import { Wallet } from './pages/profile/Wallet';
import { UserImpact } from './pages/profile/Impact';
import { FederationPortal } from './pages/federation/FederationPortal';
import { FederationGovernance } from './pages/federation/Governance';
import { EvolutionDashboard } from './pages/evolution/Dashboard';
import { FedPerformance } from './pages/federation/Performance';
import { JoinFederationWizard } from './pages/federation/JoinWizard';
import { Marketplace } from './pages/developers/Marketplace';
import { DevPortal } from './pages/developers/DevPortal';
import { PublicRoadmap } from './pages/PublicRoadmap';
import { OnboardingTour } from './components/onboarding/OnboardingTour';
import { ThemeProvider } from './theme/ThemeContext';

function App() {
  return (
    <ThemeProvider>
    <OnboardingTour />
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
          case 'learning':
            return <LearningDashboard />;
          case 'proposals':
            return <EvolutionProposals />;
          case 'contribute':
            return <Contribute />;
          case 'fed-portal':
            return <FederationPortal />;
          case 'governance':
            return <FederationGovernance />;
          case 'wallet':
            return <Wallet />;
          case 'marketplace':
            return <Marketplace />;
          case 'impact':
            return <UserImpact />;
          case 'evolution-facet':
            return <EvolutionDashboard />;
          case 'performance':
            return <FedPerformance />;
          case 'join-fed':
            return <JoinFederationWizard />;
          case 'dev-portal':
            return <DevPortal />;
          case 'roadmap':
            return <PublicRoadmap />;
          case 'settings':
            return (
              <div className="space-y-6">
                <h1 className="text-4xl font-black mb-2">Settings</h1>
                <p className="text-slate-500">Configure your Workstation preferences and protocol parameters.</p>
                <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
                  <h3 className="text-xl font-bold mb-4">Identity & Access</h3>
                  <button className="px-6 py-2 bg-aura text-sovereign font-bold rounded-xl">Refresh Sovereign Handshake</button>
                </div>
              </div>
            );
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
    </ThemeProvider>
  );
}

export default App;
