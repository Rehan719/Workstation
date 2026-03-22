import { useState } from 'react';
import { Shell } from './components/layout/Shell';
import { Dashboard } from './pages/Dashboard';
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
import { GlobalFederationMap } from './pages/federation/GlobalFederationMap';
import { OrbitalDashboard } from './pages/federation/OrbitalDashboard';
import { Observatory } from './pages/scholar/Observatory';
import { ConstitutionalUI } from './pages/governance/ConstitutionalUI';
import { CouncilInterface } from './pages/governance/CouncilInterface';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { Contribute } from './pages/Contribute';
import { QEPEngine } from './pages/QEPEngine';
import { ARVRSandbox } from './pages/platforms/ARVRSandbox';
import { WearableSync } from './pages/platforms/WearableSync';
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
            case 'LEARNER': return <KnowledgeGarden />;
            case 'DEVELOPER': return <Forge />;
            case 'ENTERPRISE': return <EnterpriseRealm />;
            case 'SCHOLAR': return <Observatory />;
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
          case 'fed-map': return <GlobalFederationMap />;
          case 'orbital': return <OrbitalDashboard />;
          case 'observatory': return <Observatory />;
          case 'contribute': return <Contribute />;
          case 'ar-vr': return <ARVRSandbox />;
          case 'wearables': return <WearableSync />;
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
