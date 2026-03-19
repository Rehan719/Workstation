import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { Dashboard } from './pages/Dashboard';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { AdminPanel } from './pages/AdminPanel';
import { ReligionHub } from './pages/domains/ReligionHub';
import { ScienceHub } from './pages/domains/ScienceHub';
import { LawHub } from './pages/domains/LawHub';
import { EmploymentHub } from './pages/domains/EmploymentHub';
import { EducationHub } from './pages/domains/EducationHub';
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
import { ModelManager } from './components/settings/ModelManager';

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
          case 'cfo':
            return <CFO />;
          case 'bto':
            return <BTOCatalog />;
          case 'coe':
            return <KnowledgeHub />;
          case 'qep':
            return <QEPEngine />;
          case 'introspection':
          case 'mind':
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
          case 'gov-facet':
            return <FederationPortal />;
          case 'governance':
            return <FederationGovernance />;
          case 'wallet':
          case 'eco-facet':
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
              <div className="space-y-12">
                <header>
                  <h1 className="text-5xl font-black mb-2 tracking-tight">System Settings</h1>
                  <p className="text-slate-500 font-bold text-lg">Configure your Workstation preferences and sovereign protocol parameters.</p>
                </header>

                <ModelManager />

                <div className="p-12 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
                  <h3 className="text-2xl font-black mb-6">Identity & Access</h3>
                  <p className="text-slate-400 font-bold mb-8 max-w-xl leading-relaxed">Refresh your sovereign handshake with the global federation to re-sync Citizen Passport credentials.</p>
                  <button className="px-10 py-5 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all shadow-lg shadow-aura/20 uppercase tracking-widest text-sm">Refresh Sovereign Handshake</button>
                </div>
              </div>
            );
          case 'admin':
            return <AdminPanel />;
          case 'religion':
            return <ReligionHub />;
          case 'science':
            return <ScienceHub />;
          case 'law':
            return <LawHub />;
          case 'employment':
            return <EmploymentHub />;
          case 'education':
            return <EducationHub />;
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
