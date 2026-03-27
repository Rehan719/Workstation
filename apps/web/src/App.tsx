import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { DashboardNew as Dashboard } from './pages/DashboardNew';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { AdminPanel } from './pages/AdminPanel';
import { Forge } from './pages/developers/Forge';
import { DigitalReactor } from './pages/developers/DigitalReactor';
import { Incubator } from './pages/developers/Incubator';
import { PetriDish } from './pages/developers/PetriDish';
import { Factory } from './pages/developers/Factory';
import { Pipelines } from './pages/developers/Pipelines';
import { GenomeExplorer } from './pages/genome/GenomeExplorer';
import { GRNDashboard } from './pages/genome/GRNDashboard';
import { MethylationEditor } from './pages/genome/MethylationEditor';
import { TranscriptionalMonitor } from './pages/genome/TranscriptionalMonitor';
import { PhenotypePreview } from './pages/genome/PhenotypePreview';
import { ReligionHub } from './pages/domains/ReligionHub';
import { ScienceHub } from './pages/domains/ScienceHub';
import { LawHub } from './pages/domains/LawHub';
import { EmploymentHub } from './pages/domains/EmploymentHub';
import { EducationHub } from './pages/domains/EducationHub';
import { CareHub } from './pages/domains/CareHub';
import { KnowledgeGarden } from './pages/learner/KnowledgeGarden';
import { EnterpriseRealm } from './pages/enterprise/EnterpriseRealm';
import { OffspringManagement } from './pages/enterprise/OffspringManagement';
import { TreatyDashboard } from './pages/enterprise/TreatyDashboard';
import { SeedingInterface } from './pages/enterprise/SeedingInterface';
import { InterstellarDiplomacy } from './pages/enterprise/InterstellarDiplomacy';
import { GlobalFederationMap } from './pages/federation/GlobalFederationMap';
import { OrbitalDashboard } from './pages/federation/OrbitalDashboard';
import { CosmicMeshDashboard } from './pages/federation/CosmicMeshDashboard';
import { HomeostaticOrchestrator } from './pages/federation/Performance';
import { CredentialsVault } from './pages/governance/CredentialsVault';
import { FileHub } from './pages/tools/FileHub';
import { UVAIDDashboard } from './pages/tools/UVAIDDashboard';
import { BackgroundTextIndex } from './pages/tools/BackgroundTextIndex';
import { AuditDashboard } from './pages/tools/AuditDashboard';
import { RealmEditor } from './pages/realms/RealmEditor';
import { Observatory } from './pages/scholar/Observatory';
import { LegacyVault } from './pages/scholar/LegacyVault';
import { ConstitutionalUI } from './pages/governance/ConstitutionalUI';
import { CouncilInterface } from './pages/governance/CouncilInterface';
import { DebateLog } from './pages/c-suite/DebateLog';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { Contribute } from './pages/Contribute';
import { QEPEngine } from './pages/QEPEngine';
import { QEPLanding } from './pages/QEPLanding';
import { IntrospectionDashboard } from './pages/IntrospectionDashboard';
import { ARVRSandbox } from './pages/platforms/ARVRSandbox';
import { WearableSync } from './pages/platforms/WearableSync';
import { EmbodimentStudio } from './pages/platforms/EmbodimentStudio';
import { useStore } from '@workstation/shared';
import { ThemeProvider } from './theme/ThemeContext';
import { AdaptiveUIProvider } from './components/AdaptiveUIProvider';
import { PlayfulEffectsManager } from './components/gamification/PlayfulEffectsManager';
import Joyride from 'react-joyride';

function App() {
  const { currentRealm } = useStore();
  const [runTutorial, setRunTutorial] = useState(true);

  const isQEPStandalone = import.meta.env.VITE_QEP_STANDALONE === 'true';

  const steps = [
    { target: '.neon-text', content: 'Welcome to the v0.5 Sovereign Workstation! This is your control center.' },
    { target: 'aside nav', content: 'Navigate through the five flagships realms and sovereign domains here.' },
    { target: '.gaas-audit-btn', content: 'Every action is validated against the 1127 constitutional articles.' }
  ];

  if (isQEPStandalone) {
    return (
      <ThemeProvider>
        <AdaptiveUIProvider>
           <QEPLanding />
        </AdaptiveUIProvider>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider>
    <AdaptiveUIProvider>
    <PlayfulEffectsManager />
    <Joyride steps={steps} run={runTutorial} continuous showProgress showSkipButton />
    <Shell>
      {(activeTab) => {
        // Multi-Realm Unified Dashboard
        if (activeTab === 'dashboard') {
          switch (currentRealm) {
            case 'LEARNER': return <KnowledgeGarden />;
            case 'DEVELOPER': return <Forge />;
            case 'ENTERPRISE': return <EnterpriseRealm />;
            case 'SCHOLAR': return <Observatory />;
            case 'GENOME': return <GenomeExplorer />;
            default: return <Dashboard />;
          }
        }

        switch (activeTab) {
          case 'ceo': return <CEOChat />;
          case 'bto': return <BTOCatalog />;
          case 'religion': return <ReligionHub />;
          case 'science': return <ScienceHub />;
          case 'law': return <LawHub />;
          case 'employment': return <EmploymentHub />;
          case 'education': return <EducationHub />;
          case 'care': return <CareHub />;
          case 'fed-map': return <GlobalFederationMap />;
          case 'orchestrator': return <HomeostaticOrchestrator />;
          case 'bto': return <BTOCatalog />;
          case 'orbital': return <OrbitalDashboard />;
          case 'cosmic': return <CosmicMeshDashboard />;
          case 'seeding': return <SeedingInterface />;
          case 'diplomacy': return <InterstellarDiplomacy />;
          case 'treaties': return <TreatyDashboard />;
          case 'offspring': return <OffspringManagement />;
          case 'vault': return <CredentialsVault />;
          case 'forge': return <Forge />;
          case 'reactor': return <DigitalReactor />;
          case 'incubator': return <Incubator />;
          case 'petri': return <PetriDish />;
          case 'factory': return <Factory />;
          case 'pipelines': return <Pipelines />;
          case 'genome-explorer': return <GenomeExplorer />;
          case 'grn-dashboard': return <GRNDashboard />;
          case 'methylation': return <MethylationEditor />;
          case 'transcriptional': return <TranscriptionalMonitor />;
          case 'phenotype': return <PhenotypePreview />;
          case 'garden': return <KnowledgeGarden />;
          case 'offspring': return <OffspringManagement />;
          case 'treaties': return <TreatyDashboard />;
          case 'seeding': return <SeedingInterface />;
          case 'diplomacy': return <InterstellarDiplomacy />;
          case 'fed-map': return <GlobalFederationMap />;
          case 'orbital': return <OrbitalDashboard />;
          case 'cosmic': return <CosmicMeshDashboard />;
          case 'orchestrator': return <HomeostaticOrchestrator />;
          case 'observatory': return <Observatory />;
          case 'vault': return <CredentialsVault />;
          case 'file-hub': return <FileHub />;
          case 'uvaid': return <UVAIDDashboard />;
          case 'text-index': return <BackgroundTextIndex />;
          case 'audit': return <AuditDashboard />;
          case 'realm-editor': return <RealmEditor />;
          case 'contribute': return <Contribute />;
          case 'ar-vr': return <ARVRSandbox />;
          case 'wearables': return <WearableSync />;
          case 'embodiment': return <EmbodimentStudio />;
          case 'qep': return <QEPEngine />;
          case 'constitution': return <ConstitutionalUI />;
          case 'council': return <CouncilInterface />;
          case 'debate': return <DebateLog />;
          case 'marketplace': return <LivingMarketplace />;
          case 'introspection': return <IntrospectionDashboard />;
          case 'admin': return <AdminPanel />;
          case 'transparency': return <AuditDashboard />;
          case 'settings':
            return (
              <div className="p-10">
                <h2 className="text-3xl font-black mb-6">System Settings</h2>
                <p className="text-slate-500">Configure your Workstation v1.0 parameters.</p>
              </div>
            );
          case 'voice':
            return (
              <div className="p-10">
                <h2 className="text-3xl font-black mb-6">Voice Control</h2>
                <p className="text-slate-500">Multilingual voice command integration active.</p>
              </div>
            );
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
    </AdaptiveUIProvider>
    </ThemeProvider>
  );
}

export default App;
