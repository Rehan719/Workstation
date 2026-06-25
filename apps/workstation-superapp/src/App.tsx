import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import { Shell } from './components/layout/Shell';
import { ThemeProvider } from './theme/ThemeContext';
import { AdaptiveUIProvider } from './components/AdaptiveUIProvider';
import { PlayfulEffectsManager } from './components/gamification/PlayfulEffectsManager';
import Joyride from 'react-joyride';

// ── 1. Home / organism overview ──────────────────────────────────────────
import { DashboardNew as Dashboard } from './pages/DashboardNew';
import GrandOpsDashboard from './pages/GrandOpsDashboard';
import { IntrospectionDashboard } from './pages/IntrospectionDashboard';
import { OrganismDashboard } from './pages/organism/OrganismDashboard';
import { HeartbeatMonitor } from './pages/organism/HeartbeatMonitor';
import { CognitionIntegration } from './pages/CognitionIntegration';

// ── 2. Native AI Fabric ──────────────────────────────────────────────────
import { NativeAI } from './pages/developers/NativeAI';
import { AIToolsCatalogue } from './pages/AIToolsCatalogue';
import { CEOChat } from './pages/CEOChat';
import { BoardOfDirectors } from './pages/enterprise/BoardOfDirectors';
import VisualAgentComposer from './components/organism/VisualAgentComposer';
import SwarmIntelligence from './components/organism/SwarmIntelligence';

// ── 3. Domains ───────────────────────────────────────────────────────────
import { DomainsHub } from './pages/domains/DomainsHub';
import { ReligionHub } from './pages/domains/ReligionHub';
import { ScienceHub } from './pages/domains/ScienceHub';
import { LawHub } from './pages/domains/LawHub';
import { EducationHub } from './pages/domains/EducationHub';
import { CareHub } from './pages/domains/CareHub';
import { EmploymentHub } from './pages/domains/EmploymentHub';
import { QEPReligionHub } from './pages/domains/QEPReligionHub';
// QEP sprawl (engine/community/observatory/governance/oversight) archived to _archive/frontend-pages —
// grandiose/mock/fabricated-metrics; the genuine Qur'an Education Platform (QEPReligionHub, /qep) is kept.

// ── 4. VSB Enterprises ───────────────────────────────────────────────────
import { VSBSpawnStudio } from './pages/enterprise/VSBSpawnStudio';
import { VSBCockpit } from './pages/enterprise/VSBCockpit';
import { EnterpriseRealm } from './pages/enterprise/EnterpriseRealm';
import { GenesisJourney } from './pages/synthesis/GenesisJourney';
import { BusinessPlan } from './pages/enterprise/BusinessPlan';
import { ManagementSystemsHub } from './pages/enterprise/ManagementSystemsHub';
import { ChangeControlAgency } from './pages/enterprise/ChangeControlAgency';
import { DigitalTwins } from './pages/developers/DigitalTwins';
import { CapitalDashboard } from './pages/enterprise/CapitalDashboard';
import { ProjectsHub } from './pages/projects/ProjectsHub';

// ── 5. Resource Fabric ───────────────────────────────────────────────────
import { ResourceFabric } from './pages/synthesis/ResourceFabric';
import { SynthesisStudio } from './pages/synthesis/SynthesisStudio';
import { SynthesisNexus } from './pages/synthesis/SynthesisNexus';
import { ForgePipeline } from './pages/developers/ForgePipeline';
import { DigitalReactor } from './pages/developers/DigitalReactor';
import { Incubator } from './pages/developers/Incubator';
import { ReactorStudio } from './pages/synthesis/ReactorStudio';
import { Factory } from './pages/developers/Factory';
import { IntelligenceLab } from './pages/IntelligenceLab';
import { AuthorshipEngine } from './pages/synthesis/AuthorshipEngine';
import { DesignDevEngine } from './pages/developers/DesignDevEngine';
import { SolutionsPlatform } from './pages/SolutionsPlatform';
import { BTOCatalog } from './pages/BTOCatalog';

// ── 6. Transformation & Economy ──────────────────────────────────────────
import { TransformationDashboard } from './pages/TransformationDashboard';
import { VSBEconomy } from './pages/enterprise/VSBEconomy';
import { LivingMarketplace } from './pages/marketplace/LivingMarketplace';
import { Deliverables } from './pages/Deliverables';
// PredictionMarket archived — fabricated betting market (gambling-adjacent, conflicts halal ethics).
import { ProductCatalog } from './pages/ProductCatalog';
import { Wallet } from './pages/profile/Wallet';
import { UserImpact } from './pages/profile/Impact';
// SoulRecordExplorer archived — grandiose off-vision "multi-dimensional identity" page.

// ── 7. Governance & Operations ───────────────────────────────────────────
import { GovernanceHub } from './pages/governance/GovernanceHub';
import { ConstitutionalUI } from './pages/governance/ConstitutionalUI';
import { ComplianceChecker } from './pages/governance/ComplianceChecker';
import { OperationalExcellence } from './pages/OperationalExcellence';
import { SovereignEvolution } from './pages/evolution/SovereignEvolution';
import { KnowledgeHub } from './pages/coe/KnowledgeHub';
import { ABTestingPanel } from './pages/evolution/ABTesting';
import { LearningDashboard } from './pages/evolution/LearningDashboard';
import { AuditDashboard } from './pages/tools/AuditDashboard';

// ── 8. Developer Portal & system ─────────────────────────────────────────
import { DevPortal } from './pages/developers/DevPortal';
import { Contribute } from './pages/Contribute';
import { AdminPanel } from './pages/AdminPanel';
import { CreatorStudio } from './pages/create/CreatorStudio';
import { PublicRoadmap } from './pages/PublicRoadmap';
import { LandingPage } from './pages/landing/LandingPage';

// ── Extended (wired, reachable by URL — not in primary nav) ───────────────
// ScholarRealm archived to _archive/frontend-pages — grandiose research hub with fabricated "50+ federated nodes".
import { Introspection as CognitiveIntrospection } from './pages/cognitive/Introspection';

function App() {
  const [runTutorial] = useState(false);

  const steps = [
    { target: '.neon-text', content: 'Welcome to Workstation IDBO — your living, in-house AI organism.' },
    { target: 'aside nav', content: 'Navigate the eight vision sections: Home, Native AI, Domains, VSB, Resource Fabric, Transformation, Governance, Developer.' },
    { target: '.gaas-audit-btn', content: 'Every action is governed by the constitutional GaaS engine.' },
  ];

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
          {/* ── 1. Home / organism overview ─────────────────────────── */}
          <Route path="/"               element={<Dashboard />} />
          <Route path="/dashboard"      element={<Navigate to="/" replace />} />
          <Route path="/grand-ops"      element={<GrandOpsDashboard />} />
          <Route path="/introspection"  element={<IntrospectionDashboard />} />
          <Route path="/organism"       element={<OrganismDashboard />} />
          <Route path="/heartbeat"      element={<HeartbeatMonitor />} />
          <Route path="/cognition"      element={<CognitionIntegration />} />

          {/* ── 2. Native AI Fabric ─────────────────────────────────── */}
          <Route path="/native-ai"          element={<NativeAI />} />
          <Route path="/ai-tools"           element={<AIToolsCatalogue />} />
          <Route path="/ceo"                element={<CEOChat />} />
          <Route path="/board"              element={<BoardOfDirectors />} />
          <Route path="/visual-composer"    element={<VisualAgentComposer />} />
          <Route path="/swarm-intelligence" element={<SwarmIntelligence />} />

          {/* ── 3. Domains ──────────────────────────────────────────── */}
          <Route path="/domains"    element={<DomainsHub />} />
          <Route path="/religion"   element={<ReligionHub />} />
          <Route path="/science"    element={<ScienceHub />} />
          <Route path="/law"        element={<LawHub />} />
          <Route path="/education"  element={<EducationHub />} />
          <Route path="/care"       element={<CareHub />} />
          <Route path="/employment" element={<EmploymentHub />} />
          <Route path="/qep"            element={<QEPReligionHub />} />
          <Route path="/qep-religion"   element={<QEPReligionHub />} />

          {/* ── 4. VSB Enterprises ──────────────────────────────────── */}
          <Route path="/vsb"            element={<VSBSpawnStudio />} />
          <Route path="/vsb-spawn"      element={<VSBSpawnStudio />} />
          <Route path="/vsb-cockpit"    element={<VSBCockpit />} />
          <Route path="/enterprise"     element={<EnterpriseRealm />} />
          <Route path="/genesis"        element={<GenesisJourney />} />
          <Route path="/business-plan"  element={<BusinessPlan />} />
          <Route path="/management"     element={<ManagementSystemsHub />} />
          <Route path="/change-control" element={<ChangeControlAgency />} />
          <Route path="/digital-twins"  element={<DigitalTwins />} />
          <Route path="/capital"        element={<CapitalDashboard />} />
          <Route path="/projects"       element={<ProjectsHub />} />

          {/* ── 5. Resource Fabric ──────────────────────────────────── */}
          <Route path="/resource-fabric" element={<ResourceFabric />} />
          <Route path="/synthesis"       element={<SynthesisStudio />} />
          <Route path="/nexus"           element={<SynthesisNexus />} />
          <Route path="/forge-pipeline"  element={<ForgePipeline />} />
          <Route path="/reactor"         element={<DigitalReactor />} />
          <Route path="/incubator"       element={<Incubator />} />
          <Route path="/reactor-studio"  element={<ReactorStudio />} />
          <Route path="/factory"         element={<Factory />} />
          <Route path="/intelligence"    element={<IntelligenceLab />} />
          <Route path="/authorship"      element={<AuthorshipEngine />} />
          <Route path="/design-dev"      element={<DesignDevEngine />} />
          <Route path="/solutions"       element={<SolutionsPlatform />} />
          <Route path="/bto"             element={<BTOCatalog />} />
          <Route path="/products"        element={<Navigate to="/bto" replace />} />

          {/* ── 6. Transformation & Economy ─────────────────────────── */}
          <Route path="/transformation"    element={<TransformationDashboard />} />
          <Route path="/economy"           element={<VSBEconomy />} />
          <Route path="/marketplace"       element={<LivingMarketplace />} />
          <Route path="/dev-marketplace"   element={<Navigate to="/marketplace" replace />} />
          <Route path="/deliverables"      element={<Deliverables />} />
          <Route path="/product-catalog"   element={<ProductCatalog />} />
          <Route path="/wallet"            element={<Wallet />} />
          <Route path="/impact"            element={<UserImpact />} />

          {/* ── 7. Governance & Operations ──────────────────────────── */}
          <Route path="/governance-hub"     element={<GovernanceHub />} />
          <Route path="/constitution"       element={<ConstitutionalUI />} />
          <Route path="/compliance"         element={<ComplianceChecker />} />
          <Route path="/operations"         element={<OperationalExcellence />} />
          <Route path="/sovereign-evolution" element={<SovereignEvolution />} />
          <Route path="/coe"                element={<KnowledgeHub />} />
          <Route path="/ab-testing"         element={<ABTestingPanel />} />
          <Route path="/learning-dashboard" element={<LearningDashboard />} />
          <Route path="/audit-dashboard"    element={<AuditDashboard />} />
          <Route path="/audit"              element={<Navigate to="/governance-hub" replace />} />
          <Route path="/transparency"       element={<Navigate to="/governance-hub" replace />} />
          <Route path="/vault"              element={<Navigate to="/governance-hub" replace />} />

          {/* ── 8. Developer Portal & system ────────────────────────── */}
          <Route path="/dev-portal" element={<DevPortal />} />
          <Route path="/contribute" element={<Contribute />} />
          <Route path="/creator"    element={<CreatorStudio />} />
          <Route path="/admin"      element={<AdminPanel />} />
          <Route path="/roadmap"    element={<PublicRoadmap />} />
          <Route path="/landing"    element={<LandingPage />} />
          <Route path="/settings" element={
            <div className="p-10">
              <h2 className="text-3xl font-black mb-6">System Settings</h2>
              <p className="text-slate-500">Configure your Workstation parameters.</p>
            </div>
          } />

          {/* ── Extended (wired, reachable by URL) ───────────────────── */}
          <Route path="/cognitive-introspection" element={<CognitiveIntrospection />} />
          {/* Off-vision experimental pages (Cosmic/Reality/AR-VR/Wearables/Embodiment/Civilization)
              archived to _archive/frontend-pages — not part of the Workstation IDBO vision. */}

          {/* ── 404 ─────────────────────────────────────────────────── */}
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
