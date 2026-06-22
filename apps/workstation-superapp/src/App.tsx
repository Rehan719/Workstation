import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ProjectsHub } from './pages/projects/ProjectsHub';
import { ErrorBoundary } from './components/ErrorBoundary';
import { Shell } from './components/layout/Shell';
import { DashboardNew as Dashboard } from './pages/DashboardNew';
import { CEOChat } from './pages/CEOChat';
import { BTOCatalog } from './pages/BTOCatalog';
import { AdminPanel } from './pages/AdminPanel';
import { Forge } from './pages/developers/Forge';
import VisualAgentComposer from './components/organism/VisualAgentComposer';
import SwarmIntelligence from './components/organism/SwarmIntelligence';
import { DigitalReactor } from './pages/developers/DigitalReactor';
import { Incubator } from './pages/developers/Incubator';
import { PetriDish } from './pages/developers/PetriDish';
import { Factory } from './pages/developers/Factory';
import { Pipelines } from './pages/developers/Pipelines';
import { Marketplace as DevMarketplace } from './pages/developers/Marketplace';
import { DevPortal } from './pages/developers/DevPortal';
import { GenomeExplorer } from './pages/genome/GenomeExplorer';
import { GRNDashboard } from './pages/genome/GRNDashboard';
import { MethylationEditor } from './pages/genome/MethylationEditor';
import { TranscriptionalMonitor } from './pages/genome/TranscriptionalMonitor';
import { PhenotypePreview } from './pages/genome/PhenotypePreview';
import { ReligionHub } from './pages/domains/ReligionHub';
import { QEPReligionHub } from './pages/domains/QEPReligionHub';
import { QEPStudentPortalPage } from './pages/domains/QEPStudentPortalPage';
import { QEPCommunityPortalPage } from './pages/domains/QEPCommunityPortalPage';
import { ScienceHub } from './pages/domains/ScienceHub';
import { LawHub } from './pages/domains/LawHub';
import { EmploymentHub } from './pages/domains/EmploymentHub';
import { EducationHub } from './pages/domains/EducationHub';
import { CareHub } from './pages/domains/CareHub';
import { KnowledgeGarden } from './pages/learner/KnowledgeGarden';
import { LearnerRealm } from './pages/learner/LearnerRealm';
import { EnterpriseRealm } from './pages/enterprise/EnterpriseRealm';
import { VSBSpawnStudio } from './pages/enterprise/VSBSpawnStudio';
import { IntelligenceLab } from './pages/IntelligenceLab';
import { AuthorshipEngine } from './pages/synthesis/AuthorshipEngine';
import { DesignDevEngine } from './pages/developers/DesignDevEngine';
import { SynthesisNexus } from './pages/synthesis/SynthesisNexus';
import { GenesisJourney } from './pages/synthesis/GenesisJourney';
import { SovereignEvolution } from './pages/evolution/SovereignEvolution';
import { ResourceFabric } from './pages/synthesis/ResourceFabric';
import { BoardOfDirectors } from './pages/enterprise/BoardOfDirectors';
import { VSBEconomy } from './pages/enterprise/VSBEconomy';
import { TransformationDashboard } from './pages/TransformationDashboard';
import { HeartbeatMonitor } from './pages/organism/HeartbeatMonitor';
import { CognitionIntegration } from './pages/CognitionIntegration';
import { BusinessPlan } from './pages/enterprise/BusinessPlan';
import { ForgePipeline } from './pages/developers/ForgePipeline';
import { DigitalTwins } from './pages/developers/DigitalTwins';
import { NativeAI } from './pages/developers/NativeAI';
import { ComplianceChecker } from './pages/governance/ComplianceChecker';
import { OrganismDashboard } from './pages/organism/OrganismDashboard';
import { ManagementSystemsHub } from './pages/enterprise/ManagementSystemsHub';
import { ChangeControlAgency } from './pages/enterprise/ChangeControlAgency';
import { OffspringManagement } from './pages/enterprise/OffspringManagement';
import { TreatyDashboard } from './pages/enterprise/TreatyDashboard';
import { SeedingInterface } from './pages/enterprise/SeedingInterface';
import { InterstellarDiplomacy } from './pages/enterprise/InterstellarDiplomacy';
import { CapitalDashboard } from './pages/enterprise/CapitalDashboard';
import { GlobalFederationMap } from './pages/federation/GlobalFederationMap';
import { OrbitalDashboard } from './pages/federation/OrbitalDashboard';
import { CosmicMeshDashboard } from './pages/federation/CosmicMeshDashboard';
import { HomeostaticOrchestrator } from './pages/federation/Performance';
import { FederationPortal } from './pages/federation/FederationPortal';
import { JoinFederationWizard } from './pages/federation/JoinWizard';
import { TwinManagement } from './pages/federation/TwinManagement';
import { WorkstationExplorer } from './pages/federation/WorkstationExplorer';
import { TreatyStudio } from './pages/federation/TreatyStudio';
import { GovernanceHub } from './pages/governance/GovernanceHub';
import { Sanctum } from './pages/governance/Sanctum';
import { CredentialsVault } from './pages/governance/CredentialsVault';
import { DAODashboard } from './pages/governance/DAODashboard';
import { DelegationDashboard } from './pages/governance/DelegationDashboard';
import { FileHub } from './pages/tools/FileHub';
import { UVAIDDashboard } from './pages/tools/UVAIDDashboard';
import { BackgroundTextIndex } from './pages/tools/BackgroundTextIndex';
import { AuditDashboard } from './pages/tools/AuditDashboard';
import { SynthesisStudio } from './pages/synthesis/SynthesisStudio';
import { SolutionsPlatform } from './pages/SolutionsPlatform';
import { RealmEditor } from './pages/realms/RealmEditor';
import { Observatory } from './pages/scholar/Observatory';
import { LegacyVault } from './pages/scholar/LegacyVault';
import { ScholarRealm } from './pages/scholar/ScholarRealm';
import { ConstitutionalUI } from './pages/governance/ConstitutionalUI';
import { CouncilInterface } from './pages/governance/CouncilInterface';
import { DebateLog } from './pages/c-suite/DebateLog';
import { CFO } from './pages/c-suite/CFO';
import { CTO } from './pages/c-suite/CTO';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { Contribute } from './pages/Contribute';
import { QEPEngine } from './pages/QEPEngine';
import { QEPLanding } from './pages/QEPLanding';
import { SovereignXAIObservatory as QEPObservatoryPage } from './pages/domains/QEPObservatoryPage';
import { QEPGovernancePortal } from './pages/domains/QEPGovernancePortal';
import QEPAnalyticsPage from './pages/domains/QEPAnalyticsPage';
import QEPOpsPage from './pages/domains/QEPOpsPage';
import HumanOversightQueue from './components/qep/scholar/HumanOversightQueue';
import { IntrospectionDashboard } from './pages/IntrospectionDashboard';
import CouncilJudiciary from './pages/council/Judiciary';
import BugBountyPortal from './pages/security/BugBounty';
import { ARVRSandbox } from './pages/platforms/ARVRSandbox';
import { WearableSync } from './pages/platforms/WearableSync';
import { EmbodimentStudio } from './pages/platforms/EmbodimentStudio';
import { CivilizationDashboard } from './pages/civilization/CivilizationDashboard';
import { RealityDashboard } from './pages/civilization/RealityDashboard';
import { CreatorStudio } from './pages/create/CreatorStudio';
import { BusinessPlanWizard } from './pages/entrepreneur/BusinessPlanWizard';
import { KnowledgeHub } from './pages/coe/KnowledgeHub';
import { EvolutionDashboard } from './pages/evolution/Dashboard';
import { ABTestingPanel } from './pages/evolution/ABTesting';
import { LearningDashboard } from './pages/evolution/LearningDashboard';
import { EvolutionProposals } from './pages/evolution/Proposals';
import { PredictionMarket } from './pages/markets/PredictionMarket';
import { PhysicalSymbiosis } from './pages/physical/PhysicalSymbiosis';
import { Wallet } from './pages/profile/Wallet';
import { UserImpact } from './pages/profile/Impact';
import { SoulRecordExplorer } from './pages/profile/SoulRecordExplorer';
import GrandOpsDashboard from './pages/GrandOpsDashboard';
import AuditPortal from './pages/regulatory/AuditPortal';
import { useStore } from '@workstation/shared';
import { ThemeProvider } from './theme/ThemeContext';
import { AdaptiveUIProvider } from './components/AdaptiveUIProvider';
import { PlayfulEffectsManager } from './components/gamification/PlayfulEffectsManager';
import Joyride from 'react-joyride';
import { Evolution as CognitiveEvolution } from './pages/cognitive/Evolution';
import { Extrospection } from './pages/cognitive/Extrospection';
import { Introspection as CognitiveIntrospection } from './pages/cognitive/Introspection';
import { CosmicNervousSystem } from './pages/cosmic/CosmicNervousSystem';
import CouncilDashboard from './pages/council/Dashboard';
import { GlobalSearch } from './pages/federation/GlobalSearch';
import { FederationGovernance } from './pages/federation/Governance';
import InstitutionalOnboarding from './pages/institutional/Onboarding';
import { LandingPage } from './pages/landing/LandingPage';
import { ProductCatalog } from './pages/ProductCatalog';
import { PublicRoadmap } from './pages/PublicRoadmap';

function App() {
  const { currentRealm } = useStore();
  const [runTutorial] = useState(false);

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
      case 'LEARNER':    return <KnowledgeGarden />;
      case 'DEVELOPER':  return <Forge />;
      case 'ENTERPRISE': return <EnterpriseRealm />;
      case 'SCHOLAR':    return <Observatory />;
      case 'GENOME':     return <GenomeExplorer />;
      default:           return <Dashboard />;
    }
  };

  return (
    <ThemeProvider>
    <AdaptiveUIProvider>
    <ErrorBoundary>
    <PlayfulEffectsManager />
    <Joyride steps={steps} run={runTutorial} continuous showProgress showSkipButton />
    <Shell>
      {() => (
        <ErrorBoundary>
        <Routes>
          {/* ── Core ─────────────────────────────────────────────── */}
          <Route path="/"          element={<MultiRealmDashboard />} />
          <Route path="/dashboard" element={<Navigate to="/" replace />} />
          <Route path="/ceo"       element={<CEOChat />} />
          <Route path="/creator"   element={<CreatorStudio />} />

          {/* ── Productivity ──────────────────────────────────────── */}
          <Route path="/bto"          element={<BTOCatalog />} />
          <Route path="/solutions"    element={<SolutionsPlatform />} />
          <Route path="/synthesis"    element={<SynthesisStudio />} />
          <Route path="/projects"     element={<ProjectsHub />} />
          <Route path="/capital"      element={<CapitalDashboard />} />
          <Route path="/marketplace"  element={<LivingMarketplace />} />
          <Route path="/products"     element={<Navigate to="/bto" replace />} />
          <Route path="/entrepreneur" element={<BusinessPlanWizard />} />

          {/* ── Domains ───────────────────────────────────────────── */}
          <Route path="/religion"    element={<ReligionHub />} />
          <Route path="/qep-religion" element={<QEPReligionHub />} />
          <Route path="/qep"         element={<QEPReligionHub />} />
          <Route path="/science"     element={<ScienceHub />} />
          <Route path="/law"         element={<LawHub />} />
          <Route path="/employment"  element={<EmploymentHub />} />
          <Route path="/education"   element={<EducationHub />} />
          <Route path="/care"        element={<CareHub />} />
          <Route path="/qep-portal"      element={<QEPStudentPortalPage />} />
          <Route path="/qep-community"   element={<QEPCommunityPortalPage />} />
          <Route path="/qep/observatory" element={<QEPObservatoryPage />} />
          <Route path="/qep/governance"  element={<QEPGovernancePortal />} />
          <Route path="/qep/analytics"   element={<QEPAnalyticsPage />} />
          <Route path="/qep/ops"         element={<QEPOpsPage />} />
          <Route path="/qep/oversight"   element={<HumanOversightQueue />} />
          <Route path="/qep/ai"          element={<Navigate to="/solutions" replace />} />
          <Route path="/qep/multi-domain" element={<Navigate to="/solutions" replace />} />
          <Route path="/qep/global"      element={<Navigate to="/solutions" replace />} />
          <Route path="/qep/facility"    element={<Navigate to="/solutions" replace />} />
          <Route path="/qep/v9"          element={<Navigate to="/solutions" replace />} />

          {/* ── Developer Realm ───────────────────────────────────── */}
          <Route path="/forge"        element={<Forge />} />
          <Route path="/reactor"      element={<DigitalReactor />} />
          <Route path="/incubator"    element={<Incubator />} />
          <Route path="/factory"      element={<Factory />} />
          <Route path="/pipelines"    element={<Pipelines />} />
          <Route path="/petri"        element={<PetriDish />} />
          <Route path="/dev-portal"   element={<DevPortal />} />
          <Route path="/dev-marketplace" element={<DevMarketplace />} />
          <Route path="/visual-composer"  element={<VisualAgentComposer />} />
          <Route path="/swarm-intelligence" element={<SwarmIntelligence />} />

          {/* ── Learner Realm ─────────────────────────────────────── */}
          <Route path="/garden"      element={<KnowledgeGarden />} />
          <Route path="/learner"     element={<LearnerRealm />} />

          {/* ── Scholar Realm ─────────────────────────────────────── */}
          <Route path="/observatory" element={<Observatory />} />
          <Route path="/legacy-vault" element={<LegacyVault />} />
          <Route path="/scholar"     element={<ScholarRealm />} />

          {/* ── Enterprise Realm ──────────────────────────────────── */}
          <Route path="/enterprise"      element={<EnterpriseRealm />} />
          <Route path="/vsb"             element={<VSBSpawnStudio />} />
          <Route path="/vsb-spawn"       element={<VSBSpawnStudio />} />
          <Route path="/intelligence"    element={<IntelligenceLab />} />
          <Route path="/authorship"      element={<AuthorshipEngine />} />
          <Route path="/design-dev"      element={<DesignDevEngine />} />
          <Route path="/nexus"           element={<SynthesisNexus />} />
          <Route path="/genesis"         element={<GenesisJourney />} />
          <Route path="/sovereign-evolution" element={<SovereignEvolution />} />
          <Route path="/resource-fabric" element={<ResourceFabric />} />
          <Route path="/board" element={<BoardOfDirectors />} />
          <Route path="/economy" element={<VSBEconomy />} />
          <Route path="/transformation" element={<TransformationDashboard />} />
          <Route path="/heartbeat" element={<HeartbeatMonitor />} />
          <Route path="/cognition" element={<CognitionIntegration />} />
          <Route path="/business-plan" element={<BusinessPlan />} />
          <Route path="/forge-pipeline" element={<ForgePipeline />} />
          <Route path="/digital-twins" element={<DigitalTwins />} />
          <Route path="/native-ai" element={<NativeAI />} />
          <Route path="/compliance" element={<ComplianceChecker />} />
          <Route path="/organism"        element={<OrganismDashboard />} />
          <Route path="/management"      element={<ManagementSystemsHub />} />
          <Route path="/change-control"  element={<ChangeControlAgency />} />
          <Route path="/seeding"         element={<SeedingInterface />} />
          <Route path="/diplomacy"       element={<InterstellarDiplomacy />} />
          <Route path="/treaties"        element={<TreatyDashboard />} />
          <Route path="/offspring"       element={<OffspringManagement />} />

          {/* ── Genome ────────────────────────────────────────────── */}
          <Route path="/genome-explorer"  element={<GenomeExplorer />} />
          <Route path="/grn-dashboard"    element={<GRNDashboard />} />
          <Route path="/methylation"      element={<MethylationEditor />} />
          <Route path="/transcriptional"  element={<TranscriptionalMonitor />} />
          <Route path="/phenotype"        element={<PhenotypePreview />} />

          {/* ── Evolution ─────────────────────────────────────────── */}
          <Route path="/introspection"        element={<IntrospectionDashboard />} />
          <Route path="/orchestrator"         element={<HomeostaticOrchestrator />} />
          <Route path="/evolution"            element={<EvolutionDashboard />} />
          <Route path="/ab-testing"           element={<ABTestingPanel />} />
          <Route path="/learning-dashboard"   element={<LearningDashboard />} />
          <Route path="/evolution-proposals"  element={<EvolutionProposals />} />
          <Route path="/cognitive-evolution"  element={<CognitiveEvolution />} />
          <Route path="/extrospection"        element={<Extrospection />} />
          <Route path="/cognitive-introspection" element={<CognitiveIntrospection />} />
          <Route path="/cosmic-nervous"       element={<CosmicNervousSystem />} />

          {/* ── Federation ────────────────────────────────────────── */}
          <Route path="/fed-map"              element={<GlobalFederationMap />} />
          <Route path="/federation"           element={<FederationPortal />} />
          <Route path="/join-federation"      element={<JoinFederationWizard />} />
          <Route path="/twin-management"      element={<TwinManagement />} />
          <Route path="/workstation-explorer" element={<WorkstationExplorer />} />
          <Route path="/treaty-studio"        element={<TreatyStudio />} />
          <Route path="/global-search"        element={<GlobalSearch />} />
          <Route path="/fed-governance"       element={<FederationGovernance />} />
          <Route path="/orbital"              element={<OrbitalDashboard />} />
          <Route path="/cosmic"               element={<CosmicMeshDashboard />} />

          {/* ── Council ───────────────────────────────────────────── */}
          <Route path="/council-dashboard" element={<CouncilDashboard />} />

          {/* ── Governance ────────────────────────────────────────── */}
          <Route path="/governance-hub"  element={<GovernanceHub />} />
          <Route path="/constitution"    element={<ConstitutionalUI />} />
          <Route path="/council"         element={<CouncilInterface />} />
          <Route path="/council/judiciary" element={<CouncilJudiciary />} />
          <Route path="/sanctum"         element={<Sanctum />} />
          <Route path="/credentials"     element={<CredentialsVault />} />
          <Route path="/dao"             element={<DAODashboard />} />
          <Route path="/delegation"      element={<DelegationDashboard />} />
          <Route path="/debate"          element={<DebateLog />} />
          <Route path="/audit"           element={<Navigate to="/governance-hub" replace />} />
          <Route path="/transparency"    element={<Navigate to="/governance-hub" replace />} />
          <Route path="/vault"           element={<Navigate to="/governance-hub" replace />} />
          <Route path="/realm-editor"    element={<RealmEditor />} />
          <Route path="/contribute"      element={<Contribute />} />

          {/* ── C-Suite ───────────────────────────────────────────── */}
          <Route path="/cfo"   element={<CFO />} />
          <Route path="/cto"   element={<CTO />} />
          <Route path="/coe"   element={<KnowledgeHub />} />

          {/* ── Civilization / Intelligence ───────────────────────── */}
          <Route path="/civilization" element={<CivilizationDashboard />} />
          <Route path="/reality"      element={<RealityDashboard />} />
          <Route path="/grand-ops"    element={<GrandOpsDashboard />} />

          {/* ── Markets & Commerce ────────────────────────────────── */}
          <Route path="/prediction-market" element={<PredictionMarket />} />
          <Route path="/product-catalog"   element={<ProductCatalog />} />
          <Route path="/roadmap"           element={<PublicRoadmap />} />

          {/* ── Profile ───────────────────────────────────────────── */}
          <Route path="/wallet"      element={<Wallet />} />
          <Route path="/impact"      element={<UserImpact />} />
          <Route path="/soul-record" element={<SoulRecordExplorer />} />

          {/* ── Tools ─────────────────────────────────────────────── */}
          <Route path="/uvaid"          element={<UVAIDDashboard />} />
          <Route path="/text-index"     element={<BackgroundTextIndex />} />
          <Route path="/file-hub"       element={<FileHub />} />
          <Route path="/audit-dashboard" element={<AuditDashboard />} />
          <Route path="/audit-portal"   element={<AuditPortal />} />

          {/* ── Physical & Platforms ──────────────────────────────── */}
          <Route path="/physical"    element={<PhysicalSymbiosis />} />
          <Route path="/ar-vr"       element={<ARVRSandbox />} />
          <Route path="/wearables"   element={<WearableSync />} />
          <Route path="/embodiment"  element={<EmbodimentStudio />} />

          {/* ── Security ──────────────────────────────────────────── */}
          <Route path="/security/bounty" element={<BugBountyPortal />} />

          {/* ── Onboarding & Landing ──────────────────────────────── */}
          <Route path="/onboarding" element={<InstitutionalOnboarding />} />
          <Route path="/landing"    element={<LandingPage />} />

          {/* ── Admin ─────────────────────────────────────────────── */}
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/settings" element={
            <div className="p-10">
              <h2 className="text-3xl font-black mb-6">System Settings</h2>
              <p className="text-slate-500">Configure your Workstation v1.0 parameters.</p>
            </div>
          } />

          {/* ── 404 ───────────────────────────────────────────────── */}
          <Route path="*" element={
            <div className="flex items-center justify-center h-full text-center p-10">
              <div>
                <h2 className="text-2xl font-black text-slate-600 uppercase tracking-widest mb-3">Page Not Found</h2>
                <p className="text-slate-500 text-sm">Navigate using the sidebar or return to the dashboard.</p>
              </div>
            </div>
          } />
        </Routes>
        </ErrorBoundary>
      )}
    </Shell>
    </ErrorBoundary>
    </AdaptiveUIProvider>
    </ThemeProvider>
  );
}

export default App;
