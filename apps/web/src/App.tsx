import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
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
import { QEPReligionHub } from './pages/domains/QEPReligionHub';
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
import { Ingest } from './pages/tools/Ingest';
import { SynthesisStudio } from './pages/synthesis/SynthesisStudio';
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
    { target: '.neon-text', content: 'Welcome to the v1.0 Sovereign Workstation! This is your control center.' },
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

  const MultiRealmDashboard = () => {
    switch (currentRealm) {
      case 'LEARNER': return <KnowledgeGarden />;
      case 'DEVELOPER': return <Forge />;
      case 'ENTERPRISE': return <EnterpriseRealm />;
      case 'SCHOLAR': return <Observatory />;
      case 'GENOME': return <GenomeExplorer />;
      default: return <Dashboard />;
    }
  };

  return (
    <ThemeProvider>
    <AdaptiveUIProvider>
    <PlayfulEffectsManager />
    <Joyride steps={steps} run={runTutorial} continuous showProgress showSkipButton />
    <Shell>
      {(activeTab) => (
        <Routes>
          <Route path="/" element={<MultiRealmDashboard />} />
          <Route path="/dashboard" element={<Navigate to="/" replace />} />
          <Route path="/ceo" element={<CEOChat />} />
          <Route path="/bto" element={<BTOCatalog />} />
          <Route path="/religion" element={<ReligionHub />} />
          <Route path="/qep-religion" element={<QEPReligionHub />} />
          <Route path="/science" element={<ScienceHub />} />
          <Route path="/law" element={<LawHub />} />
          <Route path="/employment" element={<EmploymentHub />} />
          <Route path="/education" element={<EducationHub />} />
          <Route path="/care" element={<CareHub />} />
          <Route path="/fed-map" element={<GlobalFederationMap />} />
          <Route path="/orchestrator" element={<HomeostaticOrchestrator />} />
          <Route path="/orbital" element={<OrbitalDashboard />} />
          <Route path="/cosmic" element={<CosmicMeshDashboard />} />
          <Route path="/seeding" element={<SeedingInterface />} />
          <Route path="/diplomacy" element={<InterstellarDiplomacy />} />
          <Route path="/treaties" element={<TreatyDashboard />} />
          <Route path="/offspring" element={<OffspringManagement />} />
          <Route path="/vault" element={<CredentialsVault />} />
          <Route path="/forge" element={<Forge />} />
          <Route path="/reactor" element={<DigitalReactor />} />
          <Route path="/incubator" element={<Incubator />} />
          <Route path="/petri" element={<PetriDish />} />
          <Route path="/factory" element={<Factory />} />
          <Route path="/pipelines" element={<Pipelines />} />
          <Route path="/genome-explorer" element={<GenomeExplorer />} />
          <Route path="/grn-dashboard" element={<GRNDashboard />} />
          <Route path="/methylation" element={<MethylationEditor />} />
          <Route path="/transcriptional" element={<TranscriptionalMonitor />} />
          <Route path="/phenotype" element={<PhenotypePreview />} />
          <Route path="/garden" element={<KnowledgeGarden />} />
          <Route path="/observatory" element={<Observatory />} />
          <Route path="/file-hub" element={<Ingest />} />
          <Route path="/synthesis" element={<SynthesisStudio />} />
          <Route path="/uvaid" element={<UVAIDDashboard />} />
          <Route path="/text-index" element={<BackgroundTextIndex />} />
          <Route path="/audit" element={<AuditDashboard />} />
          <Route path="/realm-editor" element={<RealmEditor />} />
          <Route path="/contribute" element={<Contribute />} />
          <Route path="/ar-vr" element={<ARVRSandbox />} />
          <Route path="/wearables" element={<WearableSync />} />
          <Route path="/embodiment" element={<EmbodimentStudio />} />
          <Route path="/qep" element={<QEPReligionHub />} />
          <Route path="/constitution" element={<ConstitutionalUI />} />
          <Route path="/council" element={<CouncilInterface />} />
          <Route path="/debate" element={<DebateLog />} />
          <Route path="/marketplace" element={<LivingMarketplace />} />
          <Route path="/introspection" element={<IntrospectionDashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/transparency" element={<AuditDashboard />} />
          <Route path="/settings" element={
            <div className="p-10">
              <h2 className="text-3xl font-black mb-6">System Settings</h2>
              <p className="text-slate-500">Configure your Workstation v1.0 parameters.</p>
            </div>
          } />
          <Route path="*" element={
            <div className="flex items-center justify-center h-full text-center">
              <div>
                 <h2 className="text-2xl font-black text-slate-800 uppercase tracking-widest">Sovereign Protocol v3.0</h2>
                 <p className="text-slate-500 mt-2">Converging mesh via Eternal Mesh...</p>
              </div>
            </div>
          } />
        </Routes>
      )}
    </Shell>
    </AdaptiveUIProvider>
    </ThemeProvider>
  );
}

export default App;
