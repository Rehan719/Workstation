import React from 'react';
import Marketplace from '../../components/qep/community/Marketplace';
import CommunityContributionForm from '../../components/qep/community/CommunityContributionForm';
import ScholarVerificationInterface from '../../components/qep/scholar/ScholarVerificationInterface';
import ProductionMonitoringDashboard from '../../components/qep/production/ProductionMonitoringDashboard';
import CrossDomainAdaptationPortal from '../../components/qep/cross_domain/CrossDomainAdaptationPortal';
import { notImplemented } from '@workstation/ui';

export const QEPCommunityPortalPage: React.FC = () => {
  const [activePortal, setActivePortal] = React.useState<'Learner' | 'Contributor' | 'Scholar' | 'Production' | 'CrossDomain'>('Learner');

  return (
    <div className="qep-community-portal-page min-h-screen bg-black text-white p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 mb-12">
          <div>
            <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-extrabold tracking-tight text-emerald-500 mb-4 flex items-center gap-4 break-words">
              <span>🕌</span> QEP COMMUNITY HUB
            </h1>
            <p className="text-lg text-slate-400 max-w-2xl font-light leading-relaxed">
              Sovereign VSB Signature Product v8.4 — Production-Ready, Cross-Domain Adaptable, and Community-Enhanced.
            </p>
          </div>
          <div className="text-right flex flex-col items-end gap-2">
            <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
              STATUS: VSB-SIG-QEP-8.4-PRODUCTION-READY
            </span>
            <span className="text-[8px] font-mono text-slate-500">
              SLA: 99.99% | WCAG: 2.1 AA | GDPR: COMPLIANT
            </span>
          </div>
        </header>

        <nav className="flex gap-8 mb-12 border-b border-slate-800 pb-6 overflow-x-auto whitespace-nowrap scrollbar-hide">
          {[
            { id: 'Learner', label: 'Learner Marketplace' },
            { id: 'Contributor', label: 'Contributor Portal' },
            { id: 'Scholar', label: 'Scholar Governance' },
            { id: 'Production', label: 'Production Ops' },
            { id: 'CrossDomain', label: 'Cross-Domain' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActivePortal(tab.id as any)}
              className={`text-lg font-bold transition-all ${activePortal === tab.id ? 'text-emerald-400 scale-105' : 'text-slate-500 hover:text-slate-300'}`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="portal-content grid grid-cols-1 @[440px]:grid-cols-3 gap-12">
          <div className="@[440px]:col-span-2">
            {activePortal === 'Learner' && <Marketplace />}
            {activePortal === 'Contributor' && <CommunityContributionForm />}
            {activePortal === 'Scholar' && <ScholarVerificationInterface />}
            {activePortal === 'Production' && <ProductionMonitoringDashboard />}
            {activePortal === 'CrossDomain' && <CrossDomainAdaptationPortal />}
          </div>

          <aside className="space-y-8">
            <div className="p-6 bg-slate-900/50 rounded-xl border border-slate-800 shadow-xl">
              <h3 className="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
                <span>📊</span> Hub Statistics
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center bg-slate-800/30 p-3 rounded">
                  <span className="text-xs text-slate-400">Total Contributors</span>
                  <span className="text-sm font-bold text-emerald-500">1,250+</span>
                </div>
                <div className="flex justify-between items-center bg-slate-800/30 p-3 rounded">
                  <span className="text-xs text-slate-400">Scholar Reviews</span>
                  <span className="text-sm font-bold text-emerald-500">335</span>
                </div>
                <div className="flex justify-between items-center bg-slate-800/30 p-3 rounded">
                  <span className="text-xs text-slate-400">Approved Modules</span>
                  <span className="text-sm font-bold text-emerald-500">48</span>
                </div>
                <div className="flex justify-between items-center bg-slate-800/30 p-3 rounded">
                  <span className="text-xs text-slate-400">Adapted Mechanisms</span>
                  <span className="text-sm font-bold text-emerald-500">35</span>
                </div>
              </div>
            </div>

            <div className="p-6 bg-emerald-900/10 rounded-xl border border-emerald-500/20 shadow-xl">
              <h3 className="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
                <span>🌐</span> Cross-Domain Adaptation
              </h3>
              <p className="text-xs text-slate-400 mb-4 leading-relaxed">
                QEP mechanisms are now fully production-adaptable for Science, Law, Employment, and Care. Awarded to the <span className="text-emerald-400 font-bold">Tier 10: Cross-Domain Adapter</span>.
              </p>
              <div className="flex -space-x-3 overflow-hidden mb-6">
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-emerald-500 flex items-center justify-center text-[10px] font-bold">JD</div>
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-blue-500 flex items-center justify-center text-[10px] font-bold">AS</div>
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-purple-500 flex items-center justify-center text-[10px] font-bold">RK</div>
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-slate-800 text-[8px] font-bold ring-2 ring-slate-900">+5</div>
              </div>
              <button onClick={() => notImplemented('View Adaptation Registry')} className="w-full py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded text-xs transition-all">
                View Adaptation Registry
              </button>
            </div>

            <div className="p-6 bg-slate-900/50 rounded-xl border border-slate-800 shadow-xl opacity-80 group">
              <h3 className="text-lg font-bold text-slate-300 group-hover:text-emerald-400 mb-4 flex items-center gap-2">
                <span>⚙️</span> API Registry (v8.4)
              </h3>
              <p className="text-xs text-slate-500 leading-relaxed italic mb-4">
                Access crowdsourced API endpoints with production-grade rate limiting and monitoring.
              </p>
              <div className="text-[10px] font-mono text-slate-400 bg-slate-800/50 p-2 rounded">
                production_api_mgmt: enabled
              </div>
            </div>
          </aside>
        </div>

        <footer className="mt-20 pt-8 border-t border-slate-800 flex justify-between items-center text-slate-600">
          <div className="text-xs font-light">
            © 2026 Virtual Sovereign Business (VSB) — Quran Education Platform v8.4
          </div>
          <div className="flex gap-6 text-[10px] font-mono">
            <span>PIPELINES: 7/7 PRODUCTION-OPTIMIZED</span>
            <span>AUDIT: SHA-256-V84</span>
            <span>SLA: 99.99%</span>
          </div>
        </footer>
      </div>
    </div>
  );
};
