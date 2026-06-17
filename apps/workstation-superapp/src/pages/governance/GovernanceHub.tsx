import React, { useState, useEffect } from 'react';
import { Card, Badge, Button, notImplemented } from '@workstation/ui';
import {
  ShieldCheck, AlertCircle, CheckCircle2, XCircle, History,
  Lock, Key, Shield, RefreshCw, Eye, EyeOff, Copy, Check,
  Sparkles, Award, Database, X,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { progressWidthClass } from '../../lib/progressWidth';

type Tab = 'audit' | 'vault' | 'sanctum';

// ── Audit tab ─────────────────────────────────────────────────────────────

const AuditTab: React.FC = () => {
  const [commits, setCommits] = useState<any[]>([]);
  const [inventory, setInventory] = useState<any>(null);
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'FAILED'>('ALL');
  const [auditing, setAuditing] = useState(false);
  const [selectedCommit, setSelectedCommit] = useState<any>(null);

  useEffect(() => {
    const mockInventory = {
      articles_verified: 1127,
      gaas_mutations: 12,
      zero_placeholder_integrity: true,
      critical_enforcement: '100%',
    };
    const mockCommits = [
      { hash: '2867f475', status: 'PASSED', date: '2026-03-26', issues: 0 },
      { hash: '77860782', status: 'PASSED', date: '2026-03-25', issues: 0 },
      { hash: 'a1b2c3d4', status: 'FAILED', date: '2026-03-24', issues: 2, msg: 'Missing GaaS validation on endpoint /api/v1/meta' },
    ];
    fetch('/api/v154/status')
      .then(() => { setInventory(mockInventory); setCommits(mockCommits); })
      .catch(() => { setInventory(mockInventory); setCommits(mockCommits); });
  }, []);

  const filteredCommits = statusFilter === 'ALL' ? commits : commits.filter(c => c.status === 'FAILED');

  const runManualAudit = () => {
    setAuditing(true);
    setTimeout(() => {
      setCommits(prev => [
        { hash: Math.random().toString(16).slice(2, 10), status: 'PASSED', date: new Date().toISOString().slice(0, 10), issues: 0 },
        ...prev,
      ]);
      setAuditing(false);
    }, 1200);
  };

  return (
    <div className="space-y-10">
      <div className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h2 className="text-2xl font-black text-white uppercase tracking-tight">GaaS Audit Center</h2>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em] mt-1">Constitutional Compliance • CI/CD Monitoring • v0.3</p>
        </div>
        <div className="flex gap-3 flex-wrap shrink-0">
          <Button onClick={() => notImplemented('Full History')} variant="outline" className="border-slate-800"><History size={16} /> Full History</Button>
          <Button onClick={runManualAudit} disabled={auditing} className="bg-white text-sovereign shadow-xl">
            <ShieldCheck size={16} /> {auditing ? 'Auditing...' : 'Run Manual Audit'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <AuditStatCard label="Articles Verified" value={inventory?.articles_verified || '0'} icon={CheckCircle2} color="text-aura" />
        <AuditStatCard label="Enforcement" value={inventory?.critical_enforcement || '0%'} icon={ShieldCheck} color="text-emerald-500" />
        <AuditStatCard label="Mutation Blocks" value="0" icon={XCircle} color="text-vital" />
        <AuditStatCard label="System Integrity" value="OPTIMAL" icon={AlertCircle} color="text-highlight" />
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
        <div className="@[440px]:col-span-8">
          <Card className="p-8 space-y-8">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-black text-white uppercase tracking-tight">Commit Compliance Log</h3>
              <div className="flex gap-2 p-1 rounded-xl bg-slate-900 border border-slate-800">
                {(['ALL', 'FAILED'] as const).map(f => (
                  <button
                    key={f}
                    type="button"
                    onClick={() => setStatusFilter(f)}
                    {...({ 'aria-pressed': statusFilter === f ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
                    className={`px-3 py-1 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all ${statusFilter === f ? 'bg-slate-800 text-aura' : 'text-slate-500'}`}
                  >
                    {f === 'ALL' ? 'All' : 'Failed'}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              {filteredCommits.map((c, i) => (
                <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
                  className="p-5 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                  <div className="flex items-center gap-5">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${c.status === 'PASSED' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-vital/10 text-vital'}`}>
                      {c.status === 'PASSED' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
                    </div>
                    <div>
                      <p className="text-sm font-black text-white uppercase tracking-widest">Commit: {c.hash}</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase">{c.date} • {c.issues} Issues</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge color={c.status === 'PASSED' ? 'emerald-500' : 'vital'}>{c.status}</Badge>
                    <Button onClick={() => setSelectedCommit(c)} variant="outline" className="px-3 py-1.5 text-[8px]">View Report</Button>
                  </div>
                </motion.div>
              ))}
            </div>
          </Card>
        </div>

        <div className="@[440px]:col-span-4">
          <Card className="p-8 bg-aura/5 border-aura/20">
            <h4 className="text-base font-black text-white mb-4 uppercase tracking-tight">Audit Intelligence</h4>
            <p className="text-sm text-slate-400 font-bold leading-relaxed mb-6">
              Constitutional AI scanning state mutations in real-time. No unauthorized behavioral drifts detected in the current epoch.
            </p>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                <span>Coverage</span><span className="text-white">100%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                <div className="h-full bg-aura w-full" />
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Commit report panel */}
      <AnimatePresence>
        {selectedCommit && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-6"
            onClick={() => setSelectedCommit(null)}>
            <div className="bg-slate-950 border border-slate-800 rounded-3xl p-10 max-w-md w-full space-y-6 shadow-2xl"
              onClick={e => e.stopPropagation()}>
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-black text-white uppercase tracking-tight">Commit Report</h3>
                <button type="button" onClick={() => setSelectedCommit(null)} aria-label="Close report" title="Close" className="text-slate-500 hover:text-white transition-colors"><X size={20} /></button>
              </div>
              <div className="space-y-3 text-sm font-bold">
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Hash</span><span className="text-white font-mono">{selectedCommit.hash}</span></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Status</span><Badge color={selectedCommit.status === 'PASSED' ? 'emerald-500' : 'vital'}>{selectedCommit.status}</Badge></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Date</span><span className="text-white">{selectedCommit.date}</span></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Issues</span><span className="text-white">{selectedCommit.issues}</span></div>
                {selectedCommit.msg && (
                  <div className="pt-4 border-t border-slate-800">
                    <p className="text-[10px] text-slate-500 uppercase tracking-widest mb-2">Details</p>
                    <p className="text-vital text-sm leading-relaxed">{selectedCommit.msg}</p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const AuditStatCard = ({ label, value, icon: Icon, color }: any) => (
  <Card className="p-5 flex items-center gap-4 group hover:scale-[1.02] transition-transform cursor-default">
    <div className={`p-3 rounded-xl bg-slate-900 border border-slate-800 ${color}`}><Icon size={20} /></div>
    <div>
      <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
      <p className="text-xl font-black text-white">{value}</p>
    </div>
  </Card>
);

// ── Vault tab ─────────────────────────────────────────────────────────────

const VaultTab: React.FC = () => {
  const [secrets, setSecrets] = useState([
    { id: 1, name: 'Main-Sovereign-PQC-Key', type: 'DILITHIUM-5', status: 'ROTATED', lastSync: '2h ago' },
    { id: 2, name: 'L11-Orbital-Auth-Token', type: 'JWT-RSA4096', status: 'ACTIVE', lastSync: '5m ago' },
    { id: 3, name: 'GaaS-Verification-Master', type: 'KYBER-1024', status: 'ACTIVE', lastSync: '1d ago' },
  ]);
  const [revealed, setRevealed] = useState<Set<number>>(new Set());
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const toggleReveal = (id: number) => {
    setRevealed(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const copyCredential = (s: { id: number; name: string; type: string }) => {
    navigator.clipboard.writeText(`${s.name} (${s.type})`).catch(() => {});
    setCopiedId(s.id);
    setTimeout(() => setCopiedId(null), 1500);
  };

  const rotateAll = () => {
    setSecrets(prev => prev.map(s => ({ ...s, status: 'ROTATED', lastSync: 'just now' })));
  };

  return (
    <div className="space-y-10">
      <div className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h2 className="text-2xl font-black text-white uppercase tracking-tight">Sovereign Vault</h2>
          <p className="text-vital font-black uppercase text-[10px] tracking-[0.3em] mt-1">Quantum-Resistant Credential Orchestration • Article 1107</p>
        </div>
        <div className="flex gap-3 flex-wrap shrink-0">
          <Button onClick={rotateAll} variant="outline" className="bg-vital/10 border-vital/30 text-vital"><RefreshCw size={16} /> Rotate All</Button>
          <Button onClick={() => notImplemented('Add Secret')} className="bg-white text-sovereign shadow-xl shadow-white/10"><Key size={16} /> Add Secret</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {secrets.map((s, i) => (
          <motion.div key={s.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <Card className="group hover:border-vital/30 transition-all border-white/5 bg-slate-950/40">
              <div className="flex justify-between items-start mb-5">
                <div className="p-3 rounded-xl bg-vital/20 text-vital"><Lock size={18} /></div>
                <Badge color={s.status === 'ACTIVE' ? 'emerald-500' : 'highlight'}>{s.status}</Badge>
              </div>
              <h3 className="text-base font-black text-white mb-1.5 uppercase tracking-widest">{s.name}</h3>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Type: {s.type}</p>
              {revealed.has(s.id) && (
                <p className="text-[10px] font-mono text-aura mb-3 break-all">{s.type}-••••-••••-{s.id.toString().padStart(4, '0')}</p>
              )}
              <div className="flex justify-between items-center pt-5 border-t border-white/5">
                <span className="text-[10px] font-mono text-slate-600">Sync: {s.lastSync}</span>
                <div className="flex gap-2">
                  <button type="button" onClick={() => toggleReveal(s.id)}
                    aria-label={revealed.has(s.id) ? 'Hide credential' : 'View credential'}
                    title={revealed.has(s.id) ? 'Hide credential' : 'View credential'}
                    className="p-2 text-slate-500 hover:text-white transition-colors">
                    {revealed.has(s.id) ? <EyeOff size={15} /> : <Eye size={15} />}
                  </button>
                  <button type="button" onClick={() => copyCredential(s)}
                    aria-label="Copy credential" title="Copy credential"
                    className="p-2 text-slate-500 hover:text-white transition-colors">
                    {copiedId === s.id ? <Check size={15} className="text-emerald-500" /> : <Copy size={15} />}
                  </button>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      <Card className="p-8 bg-vital/5 border-vital/10">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 rounded-2xl bg-vital flex items-center justify-center text-sovereign shadow-2xl shadow-vital/20">
            <Shield size={32} />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-black text-white mb-1.5 uppercase tracking-tight">Post-Quantum Integrity</h3>
            <p className="text-sm text-slate-400 font-bold leading-relaxed max-w-2xl">
              Vault access is governed by multi-sig council approval (Article 1112). Any attempt to rotate master PQC keys triggers a 10-minute system-wide veto window.
            </p>
          </div>
          <Button onClick={() => notImplemented('Audit Logs')} variant="outline" className="border-vital/30 text-vital hover:bg-vital hover:text-white transition-all px-8 shrink-0">Audit Logs</Button>
        </div>
      </Card>
    </div>
  );
};

// ── Sanctum tab ───────────────────────────────────────────────────────────

const SanctumTab: React.FC = () => {
  const [accessGranted, setAccessGranted] = useState(false);
  const [proposals, setProposals] = useState<any[]>([]);
  const [expandedProposal, setExpandedProposal] = useState<string | null>(null);

  useEffect(() => {
    setTimeout(() => setAccessGranted(true), 1500);
    setProposals([
      { id: 'meta-01', title: 'Evolve Article 1096: Post-Quantum Autonomy', status: 'Deliberation', support: '84%' },
      { id: 'meta-02', title: 'Modify Amendment Threshold to 75% Supermajority', status: 'Voting', support: '92%' },
    ]);
  }, []);

  const castSovereignVote = (id: string) => {
    setProposals(prev => prev.map(p => {
      if (p.id !== id) return p;
      const next = Math.min(100, parseFloat(p.support) + 1);
      return { ...p, support: `${next}%` };
    }));
  };

  if (!accessGranted) {
    return (
      <div className="h-64 flex flex-col items-center justify-center text-center gap-6">
        <Lock size={48} className="text-slate-700" />
        <h2 className="text-xl font-black text-slate-500 uppercase tracking-[0.4em]">The Sanctum</h2>
        <p className="text-slate-600 font-bold max-w-xs text-sm">Verifying multi-dimensional resonance. Minimum reputation threshold: 1,000.</p>
        <div className="w-40 h-1 bg-slate-900 rounded-full overflow-hidden">
          <div className={`h-full bg-aura animate-pulse ${progressWidthClass(65)}`} />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <header className="flex flex-col items-center text-center gap-4 py-10 border-b border-white/5 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.05)_0%,transparent_70%)]" />
        <div className="p-4 bg-aura/20 rounded-full text-aura shadow-[0_0_40px_rgba(100,255,218,0.2)] relative z-10">
          <Shield size={40} />
        </div>
        <div className="relative z-10">
          <h1 className="text-4xl font-black tracking-tighter neon-text">THE SANCTUM</h1>
          <p className="text-slate-500 font-bold text-base mt-2 uppercase tracking-widest">The Seat of Constitutional Sovereignty</p>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-10">
        <div className="@[440px]:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-black uppercase tracking-tight flex items-center gap-3">
              <Sparkles size={20} className="text-aura" /> Meta-Amendments
            </h3>
            <button type="button" onClick={() => notImplemented('New Meta-Proposal')}
              className="px-5 py-2 border border-aura/30 text-aura font-black rounded-xl text-xs uppercase tracking-widest hover:bg-aura/10 transition-all">
              New Meta-Proposal
            </button>
          </div>

          <div className="space-y-5">
            {proposals.map(p => (
              <div key={p.id} className="p-7 glass-card border-aura/20 bg-aura/5 hover:bg-aura/10 transition-all">
                <div className="flex justify-between items-start mb-5">
                  <div className="text-[10px] font-black text-aura uppercase tracking-[0.2em] border border-aura/30 px-3 py-1 rounded-full">{p.status}</div>
                  <span className="text-sm font-black text-white">{p.support} Consensus</span>
                </div>
                <h4 className="text-xl font-black mb-4 leading-tight">{p.title}</h4>
                <div className="flex gap-3">
                  <button type="button" onClick={() => castSovereignVote(p.id)}
                    className="flex-1 py-3 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest">
                    Cast Sovereign Vote
                  </button>
                  <button type="button" onClick={() => setExpandedProposal(expandedProposal === p.id ? null : p.id)}
                    aria-label="View proposal details" title="View proposal details"
                    className="p-3 bg-white/5 border border-white/10 rounded-xl text-slate-400 hover:text-white transition-all">
                    <Eye size={18} />
                  </button>
                </div>
                <AnimatePresence>
                  {expandedProposal === p.id && (
                    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                      className="mt-4 pt-4 border-t border-aura/20 space-y-2 overflow-hidden">
                      <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Proposal ID: {p.id}</p>
                      <p className="text-sm text-slate-300 font-bold">{p.title}</p>
                      <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Status: <span className="text-aura">{p.status}</span> • Consensus: <span className="text-aura">{p.support}</span></p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        </div>

        <aside className="space-y-6">
          <section className="p-7 glass-card border-white/5 bg-sovereign/40">
            <h3 className="text-lg font-bold mb-5 flex items-center gap-3">
              <Award size={18} className="text-highlight" /> Resonance Authority
            </h3>
            <div className="space-y-5">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Sovereign Reputation</p>
                <p className="text-4xl font-black text-white">1,420</p>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Meta-Voting Weight</p>
                <p className="text-xl font-black text-aura">2.42x</p>
              </div>
              <div className="pt-4 border-t border-white/5 text-[10px] text-slate-500 font-bold leading-relaxed">
                Authority derived from 142 cross-realm contributions and 12 passed constitutional amendments.
              </div>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
};

// ── GovernanceHub (root) ─────────────────────────────────────────────────

const TABS: { id: Tab; label: string; icon: React.FC<any> }[] = [
  { id: 'audit', label: 'Audit', icon: ShieldCheck },
  { id: 'vault', label: 'Sovereign Vault', icon: Database },
  { id: 'sanctum', label: 'The Sanctum', icon: Lock },
];

export const GovernanceHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('audit');

  return (
    <div className="space-y-8 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-5xl font-black text-white tracking-tighter uppercase italic break-words">Governance Hub</h1>
          <p className="text-slate-500 font-black uppercase text-[10px] tracking-[0.3em] mt-1">Audit • Sovereign Vault • The Sanctum</p>
        </div>
      </header>

      {/* Tab bar */}
      <div className="flex gap-2 p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => setActiveTab(id)}
            {...({ 'aria-pressed': activeTab === id ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
              activeTab === id ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-white'
            }`}
          >
            <Icon size={14} />
            {label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <AnimatePresence mode="wait">
        <motion.div key={activeTab} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }} transition={{ duration: 0.18 }}>
          {activeTab === 'audit' && <AuditTab />}
          {activeTab === 'vault' && <VaultTab />}
          {activeTab === 'sanctum' && <SanctumTab />}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
