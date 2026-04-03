import React from 'react';
import Marketplace from '../../components/qep/community/Marketplace';
import CommunityContributionForm from '../../components/qep/community/CommunityContributionForm';
import ScholarVerificationInterface from '../../components/qep/scholar/ScholarVerificationInterface';

export const QEPCommunityPortalPage: React.FC = () => {
  const [activePortal, setActivePortal] = React.useState<'Learner' | 'Contributor' | 'Scholar'>('Learner');

  return (
    <div className="qep-community-portal-page min-h-screen bg-black text-white p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 flex justify-between items-end">
          <div>
            <h1 className="text-5xl font-extrabold tracking-tight text-emerald-500 mb-4 flex items-center gap-4">
              <span>🕌</span> QEP COMMUNITY HUB
            </h1>
            <p className="text-lg text-slate-400 max-w-2xl font-light leading-relaxed">
              Sovereign VSB Signature Product v8.3 — Empowering the Ummah through crowdsourced knowledge, scholar verification, and pipeline synergization.
            </p>
          </div>
          <div className="text-right">
            <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
              STATUS: VSB-SIG-QEP-8.3-ACTIVE
            </span>
          </div>
        </header>

        <nav className="flex gap-8 mb-12 border-b border-slate-800 pb-6">
          <button
            onClick={() => setActivePortal('Learner')}
            className={`text-lg font-bold transition-all ${activePortal === 'Learner' ? 'text-emerald-400 scale-105' : 'text-slate-500 hover:text-slate-300'}`}
          >
            Learner Marketplace
          </button>
          <button
            onClick={() => setActivePortal('Contributor')}
            className={`text-lg font-bold transition-all ${activePortal === 'Contributor' ? 'text-emerald-400 scale-105' : 'text-slate-500 hover:text-slate-300'}`}
          >
            Contributor Portal
          </button>
          <button
            onClick={() => setActivePortal('Scholar')}
            className={`text-lg font-bold transition-all ${activePortal === 'Scholar' ? 'text-emerald-400 scale-105' : 'text-slate-500 hover:text-slate-300'}`}
          >
            Scholar Governance
          </button>
        </nav>

        <div className="portal-content grid grid-cols-1 lg:grid-cols-3 gap-12">
          <div className="lg:col-span-2">
            {activePortal === 'Learner' && <Marketplace />}
            {activePortal === 'Contributor' && <CommunityContributionForm />}
            {activePortal === 'Scholar' && <ScholarVerificationInterface />}
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
              </div>
            </div>

            <div className="p-6 bg-emerald-900/10 rounded-xl border border-emerald-500/20 shadow-xl">
              <h3 className="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
                <span>🛡️</span> Community Guardian
              </h3>
              <p className="text-xs text-slate-400 mb-4 leading-relaxed">
                Top contributors are awarded the <span className="text-emerald-400 font-bold">Tier 9: Community Guardian</span> badge. This badge signifies absolute trustworthiness in moderation and scholarship.
              </p>
              <div className="flex -space-x-3 overflow-hidden mb-6">
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-emerald-500 flex items-center justify-center text-[10px] font-bold">JD</div>
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-blue-500 flex items-center justify-center text-[10px] font-bold">AS</div>
                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-slate-900 bg-purple-500 flex items-center justify-center text-[10px] font-bold">RK</div>
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-slate-800 text-[8px] font-bold ring-2 ring-slate-900">+12</div>
              </div>
              <button className="w-full py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded text-xs transition-all">
                View Leaderboard
              </button>
            </div>

            <div className="p-6 bg-slate-900/50 rounded-xl border border-slate-800 shadow-xl opacity-60 grayscale hover:grayscale-0 transition-all cursor-not-allowed group">
              <h3 className="text-lg font-bold text-slate-500 group-hover:text-emerald-400 mb-4 flex items-center gap-2">
                <span>⚙️</span> API Discovery
              </h3>
              <p className="text-xs text-slate-500 leading-relaxed italic mb-4">
                Access the crowdsourced API registry for advanced scraping pipelines.
              </p>
              <div className="text-[10px] font-mono text-slate-600 bg-slate-800/50 p-2 rounded">
                registry: api_registry.yaml
              </div>
            </div>
          </aside>
        </div>

        <footer className="mt-20 pt-8 border-t border-slate-800 flex justify-between items-center text-slate-600">
          <div className="text-xs font-light">
            © 2026 Virtual Sovereign Business (VSB) — Quran Education Platform v8.3
          </div>
          <div className="flex gap-6 text-[10px] font-mono">
            <span>PIPELINES: 7/7 SYNERGIZED</span>
            <span>AUDIT: SHA-256-ACTIVE</span>
            <span>WCAG: 2.1 AA</span>
          </div>
        </footer>
      </div>
    </div>
  );
};
