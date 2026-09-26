import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button, toast } from '@workstation/ui';
import {
  ShieldCheck, AlertCircle, CheckCircle2, XCircle, History,
  Lock, Key, Shield, RefreshCw, Eye, EyeOff, Copy, Check,
  Sparkles, Award, Database, X, Vote, ThumbsUp, ThumbsDown, Activity,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { progressWidthClass } from '../../lib/progressWidth';
import { apiJson, errorMessage } from '../../lib/api';

// ── Governance Proposals sub-component ────────────────────────────────────────

interface Proposal {
  id: string;
  project_id: string;
  project_title: string;
  from_stage: 'concept' | 'prototype' | 'commercialise';
  to_stage: 'concept' | 'prototype' | 'commercialise';
  status: 'pending' | 'approved' | 'rejected';
  votes_for: number;
  votes_against: number;
  created_at: number;
}

const ProposalsPanel: React.FC = () => {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [loading, setLoading]     = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const r = await axios.get<Proposal[]>('/api/v1/projects/governance/proposals');
      setProposals(r.data);
    } catch {
      setProposals([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const vote = async (proposal_id: string, approve: boolean) => {
    try {
      await axios.post(`/api/v1/projects/governance/proposals/${proposal_id}/vote?approve=${approve}`);
      toast(approve ? 'Proposal approved — stage advanced.' : 'Proposal rejected.');
      load();
    } catch (e: any) {
      toast(e?.response?.data?.detail ?? 'Vote failed');
    }
  };

  if (loading) return <p className="text-xs text-slate-500 py-4">Loading proposals…</p>;
  if (proposals.length === 0) return (
    <div className="py-8 text-center">
      <Vote size={28} className="text-slate-700 mx-auto mb-2" />
      <p className="text-xs text-slate-500">No proposals yet.</p>
      <p className="text-[9px] text-slate-600 mt-1">In a Project, click <strong>Propose Advance</strong> to request a stage vote here.</p>
    </div>
  );

  return (
    <div className="space-y-3">
      {proposals.map(p => (
        <div key={p.id} className="p-4 rounded-2xl bg-slate-950 border border-slate-900 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-black text-white">{p.project_title}</p>
              <p className="text-[9px] text-slate-500 uppercase mt-0.5">
                {p.from_stage} → {p.to_stage} &nbsp;·&nbsp; {new Date(p.created_at * 1000).toLocaleDateString()}
              </p>
            </div>
            <Badge color={p.status === 'approved' ? 'emerald-500' : p.status === 'rejected' ? 'vital' : 'aura'}>
              {p.status.toUpperCase()}
            </Badge>
          </div>
          {p.status === 'pending' && (
            <div className="flex gap-2">
              <Button
                onClick={() => vote(p.id, true)}
                className="flex-1 bg-emerald-500 text-white font-black text-[9px] py-1.5 flex items-center justify-center gap-1"
              >
                <ThumbsUp size={11} /> Approve
              </Button>
              <Button
                onClick={() => vote(p.id, false)}
                variant="outline"
                className="flex-1 border-vital text-vital font-black text-[9px] py-1.5 flex items-center justify-center gap-1"
              >
                <ThumbsDown size={11} /> Reject
              </Button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

type Tab = 'audit' | 'vault' | 'sanctum';

// ── Audit tab ─────────────────────────────────────────────────────────────

const AuditTab: React.FC = () => {
  const navigate = useNavigate();
  // Ledger cluster 3 — the audit surface is REAL now. "Run Manual Audit" recomputes the whole
  // tamper-evident UEG hash chain (GET /api/v1/gaas/ueg/verify) and the log lists ACTUAL
  // constitutional events. The old tab fabricated PASSED commit rows with Math.random() hashes
  // and hardcoded inventory stats — deleted.
  // W492 (FU-196) - `valid` alone cannot carry three different outcomes: an unreadable ledger, a hash
  // mismatch, and a clean recomputation whose tail anchor could not be checked.
  const [verify, setVerify] = useState<{
    valid: boolean; events: number | null; root_hash: string | null;
    outcome?: 'verified' | 'unreadable' | 'hash_mismatch' | 'anchor_mismatch' | 'node_count_below_anchor';
    reason?: string | null; anchor_checked?: boolean; anchor_state?: string; verified_basis?: string;
  } | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [auditRuns, setAuditRuns] = useState<{ at: string; valid: boolean; events: number | null;
    root: string | null; outcome?: string; anchorChecked?: boolean }[]>([]);
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'FLAGGED'>('ALL');
  const [auditing, setAuditing] = useState(false);
  const [loadErr, setLoadErr] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<any>(null);

  const load = async () => {
    try {
      const [v, ev] = await Promise.all([
        apiJson('/api/v1/gaas/ueg/verify'),
        apiJson('/api/v1/gaas/ueg/events?limit=40'),
      ]);
      setVerify(v);
      setEvents((ev.events ?? []).slice().reverse());   // newest first
      setLoadErr('');
    } catch (e) { setLoadErr(errorMessage(e)); }
  };
  useEffect(() => { load(); }, []);

  // W460 (P1.12) — the level comes from the backend's classification of what the event IS. The old test
  // (decision==='deny' / status==='denied' / type contains 'violation') matched nothing the gate writes, so a
  // blocked action's policy_gate_halt rendered as a green "CHAINED".
  const flagLevel = (e: any): 'flagged' | 'review' | 'recorded' | 'unclassified' => e?.flag?.level ?? 'unclassified';
  const isFlagged = (e: any) => flagLevel(e) === 'flagged' || flagLevel(e) === 'review';
  const levelBadge = (e: any) => {
    const l = flagLevel(e);
    return l === 'flagged' ? { color: 'vital', text: 'FLAGGED' } : l === 'review' ? { color: 'highlight', text: 'REVIEW' }
      : l === 'recorded' ? { color: 'slate', text: 'CHAINED' } : { color: 'slate', text: 'UNCLASSIFIED' };
  };
  const filteredEvents = statusFilter === 'ALL' ? events : events.filter(isFlagged);
  const fmtTs = (ts: number) => { try { return new Date(ts * 1000).toLocaleString(); } catch { return String(ts); } };

  const runManualAudit = async () => {
    setAuditing(true);
    try {
      const v = await apiJson('/api/v1/gaas/ueg/verify');   // REAL: recomputes the full chain
      setVerify(v);
      // W492 - an unreadable verify has no root_hash, and String(undefined).slice(0,12) logged the
      // literal "undefined" as one
      // a hash mismatch omits `events` entirely, so normalise absent to null rather than storing undefined
      setAuditRuns(prev => [{ at: new Date().toLocaleString(), valid: v.valid,
                              events: typeof v.events === 'number' ? v.events : null,
                              root: v.root_hash ? String(v.root_hash).slice(0, 12) : null,
                              outcome: v.outcome, anchorChecked: v.anchor_checked }, ...prev]);
      await load();
    } catch (e) { setLoadErr(errorMessage(e)); }
    setAuditing(false);
  };

  return (
    <div className="space-y-10">
      <div className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h2 className="text-2xl font-black text-white uppercase tracking-tight">GaaS Audit Center</h2>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em] mt-1">Constitutional UEG chain · tamper-evidence recomputed on demand</p>
        </div>
        <div className="flex gap-3 flex-wrap shrink-0">
          <Button onClick={() => navigate('/change-control')} variant="outline" className="border-slate-800"><History size={16} /> Full History</Button>
          <Button onClick={runManualAudit} disabled={auditing} className="bg-white text-sovereign shadow-xl">
            <ShieldCheck size={16} /> {auditing ? 'Verifying chain...' : 'Run Manual Audit'}
          </Button>
        </div>
      </div>

      {loadErr && <p className="text-vital text-xs font-bold">{loadErr}</p>}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {/* W492 (refutation) - an unreadable ledger returns events:null and root_hash:null, and a hash
            mismatch omits both keys entirely, so these cards printed "null..." and a bare null. No figure
            is shown for a ledger that was not read whole. */}
        <AuditStatCard label="UEG Events"
          value={typeof verify?.events === 'number' ? verify.events : '—'}
          icon={CheckCircle2} color="text-aura" />
        <AuditStatCard label="Chain Integrity"
          value={!verify ? '—'
            : verify.outcome === 'unreadable' ? 'UNREADABLE'
            : verify.valid ? (verify.anchor_checked ? 'VALID' : 'HASHES OK')
            : 'BROKEN'}
          icon={ShieldCheck}
          color={!verify ? 'text-slate-500'
            : verify.outcome === 'unreadable' ? 'text-amber-400'
            : verify.valid ? (verify.anchor_checked ? 'text-emerald-500' : 'text-amber-400')
            : 'text-vital'} />
        <AuditStatCard label="Flagged (last loaded)" value={events.filter(e => flagLevel(e) === 'flagged').length} icon={XCircle} color="text-vital" />
        <AuditStatCard label="Root Hash"
          value={verify?.root_hash ? `${String(verify.root_hash).slice(0, 10)}…` : '—'}
          icon={AlertCircle} color="text-highlight" />
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
        <div className="@[440px]:col-span-8">
          <Card className="p-8 space-y-8">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-black text-white uppercase tracking-tight">Constitutional Event Log</h3>
              <div className="flex gap-2 p-1 rounded-xl bg-slate-900 border border-slate-800">
                {(['ALL', 'FLAGGED'] as const).map(f => (
                  <button
                    key={f}
                    type="button"
                    onClick={() => setStatusFilter(f)}
                    {...({ 'aria-pressed': statusFilter === f ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
                    className={`px-3 py-1 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all ${statusFilter === f ? 'bg-slate-800 text-aura' : 'text-slate-500'}`}
                  >
                    {f === 'ALL' ? 'All' : 'Flagged + review'}
                  </button>
                ))}
              </div>
            </div>

            {auditRuns.length > 0 && (
              <div className="space-y-2">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">Audit runs (this session — each recomputed the full chain)</p>
                {auditRuns.map((r, i) => (
                  <div key={i} className={`p-3 rounded-xl border flex items-center justify-between text-[10px] font-black uppercase ${
                    r.outcome === 'unreadable' ? 'bg-amber-500/5 border-amber-500/20 text-amber-400'
                    : r.valid ? (r.anchorChecked ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400'
                                                 : 'bg-amber-500/5 border-amber-500/20 text-amber-400')
                    : 'bg-vital/5 border-vital/20 text-vital'}`}>
                    <span>{r.at}</span>
                    <span>{r.outcome === 'unreadable' ? 'NOT ASSESSED — LEDGER UNREADABLE'
                      : r.valid ? (r.anchorChecked ? 'CHAIN VALID' : 'HASHES OK · ANCHOR NOT CHECKED')
                      : 'CHAIN BROKEN'}
                      {typeof r.events === 'number' ? ` · ${r.events} events` : ''}
                      {r.root ? ` · root ${r.root}…` : ''}</span>
                  </div>
                ))}
              </div>
            )}

            <div className="space-y-3">
              {filteredEvents.length === 0 && (
                <p className="text-sm text-slate-500 font-bold">{loadErr ? 'Event log unavailable.' : statusFilter === 'FLAGGED' ? 'No flagged or review events among the events loaded.' : 'No constitutional events recorded yet.'}</p>
              )}
              {filteredEvents.map((ev) => (
                <motion.div key={ev.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
                  className="p-5 rounded-2xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                  <div className="flex items-center gap-5">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${flagLevel(ev) === 'flagged' ? 'bg-vital/10 text-vital' : flagLevel(ev) === 'review' ? 'bg-highlight/10 text-highlight' : 'bg-slate-800 text-slate-500'}`}>
                      {isFlagged(ev) ? <AlertCircle size={20} /> : <Activity size={20} />}
                    </div>
                    <div>
                      <p className="text-sm font-black text-white uppercase tracking-widest">{String(ev.data?.type ?? 'event')} · {ev.id}</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase">{fmtTs(ev.timestamp)}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge color={levelBadge(ev).color} className="event-level">{levelBadge(ev).text}</Badge>
                    <Button onClick={() => setSelectedEvent(ev)} variant="outline" className="px-3 py-1.5 text-[8px]">View Event</Button>
                  </div>
                </motion.div>
              ))}
            </div>
          </Card>
        </div>

        <div className="@[440px]:col-span-4 space-y-6">
          <Card className="p-6 border-aura/20 bg-aura/5">
            <h4 className="text-sm font-black text-white mb-3 uppercase tracking-tight flex items-center gap-2">
              <Vote size={14} className="text-aura" /> Stage Proposals
            </h4>
            <ProposalsPanel />
          </Card>
          <Card className="p-8 bg-aura/5 border-aura/20">
            <h4 className="text-base font-black text-white mb-4 uppercase tracking-tight">Audit Intelligence</h4>
            <p className="text-sm text-slate-400 font-bold leading-relaxed mb-6">
              {/* W492 (FU-196) - verify.valid alone drove all three claims on this page. An
                  UNREADABLE ledger returns valid:false with only a reason, and this said the hashes did
                  not match - tampering that was never found. And a missing or corrupt tail anchor still
                  returns valid:true, so truncation and rollback detection vanished while the page said
                  every event was verified. The outcome and the anchor state are separate facts. */}
              {verify
                ? (verify.outcome === 'unreadable'
                    ? `The constitutional ledger could not be read whole (${verify.reason ?? 'no reason given'}), so nothing was verified. This is not evidence of tampering.`
                    : verify.valid
                    ? (verify.anchor_checked
                        ? `All ${verify.events} constitutional events verified against the recomputed hash chain, and the chain head matches the tail anchor.`
                        : `All ${verify.events} constitutional events verified against the recomputed hash chain — but truncation and rollback are NOT ruled out: the tail anchor is ${verify.anchor_state ?? 'unavailable'}.`)
                    : `CHAIN VERIFICATION FAILED — ${verify.reason ?? 'the ledger does not match its recomputed hashes'}. Investigate immediately.`)
                : loadErr || 'Verifying the constitutional ledger…'}
            </p>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                <span>Chain verified</span>
                <span className="text-white" data-testid="chain-verified-figure"
                      title={verify?.verified_basis}>
                  {!verify ? '—'
                    : verify.outcome === 'unreadable' ? 'NOT ASSESSED'
                    : verify.valid ? (verify.anchor_checked ? '100%' : 'hashes only')
                    : 'FAILED'}
                </span>
              </div>
              <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                <div className={`h-full ${!verify ? 'bg-slate-700 w-0'
                  : verify.outcome === 'unreadable' ? 'bg-amber-500 w-0'
                  : !verify.valid ? 'bg-vital w-1/4'
                  : verify.anchor_checked ? 'bg-aura w-full' : 'bg-amber-500 w-3/4'}`} />
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Event report panel */}
      <AnimatePresence>
        {selectedEvent && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-6"
            onClick={() => setSelectedEvent(null)}>
            <div className="bg-slate-950 border border-slate-800 rounded-3xl p-10 max-w-md w-full space-y-6 shadow-2xl"
              onClick={e => e.stopPropagation()}>
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-black text-white uppercase tracking-tight">UEG Event</h3>
                <button type="button" onClick={() => setSelectedEvent(null)} aria-label="Close report" title="Close" className="text-slate-500 hover:text-white transition-colors"><X size={20} /></button>
              </div>
              <div className="space-y-3 text-sm font-bold">
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Event</span><span className="text-white font-mono">{selectedEvent.id}</span></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Status</span><Badge color={levelBadge(selectedEvent).color}>{levelBadge(selectedEvent).text}</Badge></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Time</span><span className="text-white">{fmtTs(selectedEvent.timestamp)}</span></div>
                <div className="flex justify-between"><span className="text-slate-500 uppercase tracking-widest text-[10px]">Hash</span><span className="text-white font-mono">{String(selectedEvent.hash ?? '').slice(0, 16)}…</span></div>
                <div className="pt-4 border-t border-slate-800">
                  <p className="text-[10px] text-slate-500 uppercase tracking-widest mb-2">Event data (verbatim)</p>
                  <pre className="text-[10px] text-slate-400 font-mono whitespace-pre-wrap max-h-48 overflow-y-auto">{JSON.stringify(selectedEvent.data ?? {}, null, 2)}</pre>
                </div>
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
  const navigate = useNavigate();
  // W314 — honest: DEMO rows (no real secrets backend exists); labels no longer fabricate
  // post-quantum algorithms or invented constitutional articles.
  const [secrets, setSecrets] = useState([
    { id: 1, name: 'Demo-Credential-A', type: 'DEMO (no vault backend)', status: 'DEMO', lastSync: '—' },
    { id: 2, name: 'Demo-Credential-B', type: 'DEMO (no vault backend)', status: 'DEMO', lastSync: '—' },
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
    navigator.clipboard.writeText(`${s.name} (${s.type})`).catch(() => toast('Copy failed — clipboard unavailable'));   // W329
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
          <p className="text-vital font-black uppercase text-[10px] tracking-[0.3em] mt-1">Demo surface — no real secrets backend; real credentials live in server-side env/config only</p>
        </div>
        <div className="flex gap-3 flex-wrap shrink-0">
          <Button onClick={rotateAll} variant="outline" className="bg-vital/10 border-vital/30 text-vital"><RefreshCw size={16} /> Rotate All</Button>
          <Button onClick={() => toast('No vault backend exists yet — this tab is a demo surface. Real credentials are server-side env/config.')} className="bg-white text-sovereign shadow-xl shadow-white/10"><Key size={16} /> Add Secret</Button>
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
            <h3 className="text-xl font-black text-white mb-1.5 uppercase tracking-tight">Honest Security Posture</h3>
            <p className="text-sm text-slate-400 font-bold leading-relaxed max-w-2xl">
              Honest posture: this vault is a DEMO surface — there is no secrets backend, no PQC implementation, and no multi-sig council. Real credentials are held server-side in environment configuration; consequential changes route through the real Change Control Agency.
            </p>
          </div>
          <Button onClick={() => navigate('/change-control')} variant="outline" className="border-vital/30 text-vital hover:bg-vital hover:text-white transition-all px-8 shrink-0">Audit Logs</Button>
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
  const [showProposalForm, setShowProposalForm] = useState(false);
  const [proposalInput, setProposalInput] = useState('');
  const [submittingProposal, setSubmittingProposal] = useState(false);

  const submitMetaProposal = async () => {
    if (!proposalInput.trim()) return;
    setSubmittingProposal(true);
    try {
      const res = await fetch('/api/v1/cca/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: proposalInput,
          description: `Constitutional Meta-Amendment: ${proposalInput}`,
          change_type: 'constitutional',
          // the real request field is submitted_by (unknown fields are silently dropped by pydantic)
          submitted_by: 'sovereign-sanctum',
        }),
      });
      // Ledger cluster 2 — a 4xx/5xx must never produce the success toast + a phantom list entry
      if (!res.ok) {
        const detail = await res.json().then(d => d?.detail).catch(() => null);
        toast(`Submission failed (HTTP ${res.status})${detail ? `: ${String(detail).slice(0, 120)}` : ''}`);
        return;
      }
      const data = await res.json();
      setProposalInput('');
      setShowProposalForm(false);
      toast(`Constitutional meta-proposal ${data.cca_id ?? ''} submitted to the Change Control Agency (CRITICAL tier)`);
      await loadSanctum();   // the REAL entry appears from the CCA store, not a local phantom
    } catch {
      toast('Submission failed — please try again');
    } finally {
      setSubmittingProposal(false);
    }
  };

  const [sanctumErr, setSanctumErr] = useState('');
  const [votingId, setVotingId] = useState('');

  // W459 — the hold is tier-based, so the Sanctum lists every pending CRITICAL change (not only the
  // constitutional type), read from the uncapped queue rather than the 50-row list.
  // Ledger cluster 3 — the Sanctum is REAL now: proposals are the actual pending CRITICAL
  // change requests in the CCA, the access gate is the constitutional ledger answering (no fake
  // reputation timer), and a sovereign vote is the Owner's audit-trailed review override. The old
  // tab hardcoded two proposals and incremented a local percentage that vanished on reload.
  const loadSanctum = async () => {
    try {
      await apiJson('/api/v1/gaas/ueg/verify');   // the constitutional ledger must answer
      setAccessGranted(true);
      const d = await apiJson('/api/v1/cca/queue');
      setProposals((d.queue ?? [])
        // W463 — also every change HELD for an explicit decision (a hold_reason), and every economy hold filed
        // after a rejection from the moment it is filed: no other page can decide those, so they were stranded.
        // W464 (FU-014) — every material economy hold is CRITICAL now (the queue reports the tier a record is decided
        // under, so a hold filed as MEDIUM before the ruling is listed too): all of them are decided here
        .filter((c: any) => (c.impact_tier === 'CRITICAL' || c.hold_reason || c.follows_rejection) && ['submitted', 'under_review'].includes(c.status))
        .map((c: any) => ({ id: c.cca_id, title: c.title, status: c.status, tier: c.impact_tier,
                            change_type: c.change_type, submitted_at: c.submitted_at,
                            hold_reason: c.hold_reason, est: c.est_distributable_wst,
                            follows_rejection: c.follows_rejection })));
      setSanctumErr('');
    } catch (e) {
      setAccessGranted(true);   // never fake a lock — show the honest error instead
      setProposals([]);
      setSanctumErr(errorMessage(e));
    }
  };
  useEffect(() => { loadSanctum(); }, []);

  const castSovereignVote = async (id: string, decision: 'approved' | 'rejected') => {
    const p = proposals.find(x => x.id === id);
    setVotingId(id); setSanctumErr('');
    try {
      // W459 — the Sanctum button IS the explicit Owner decision on a CRITICAL change, so it sends
      // the acknowledgement the route now requires (without it the vote is refused, correctly)
      const res = await apiJson(`/api/v1/cca/${id}/review`, { method: 'POST',
        body: { override_decision: decision, admin_decision_for_critical: true,
                // W463 — the amount this card showed: if the hold moved since, the decision is refused (409)
                ...(p?.est != null ? { expected_est_distributable_wst: p.est } : {}),
                reviewer_notes: 'Sovereign vote — Owner decision from the Sanctum' } });
      // W464 (FU-013) — the decision is on the change record and, when the write landed, on the constitutional ledger
      toast(`Sovereign ${decision === 'approved' ? 'approval' : 'rejection'} recorded for ${id} — on the change's audit trail`
            + (res?.ueg_logged === true ? ' and the constitutional ledger' : res?.ueg_logged === false ? ' (the ledger entry did not land)' : ''));
      await loadSanctum();
    } catch (e) { setSanctumErr(errorMessage(e)); }
    setVotingId('');
  };

  if (!accessGranted) {
    return (
      <div className="h-64 flex flex-col items-center justify-center text-center gap-6">
        <Lock size={48} className="text-slate-700" />
        <h2 className="text-xl font-black text-slate-500 uppercase tracking-[0.4em]">The Sanctum</h2>
        <p className="text-slate-600 font-bold max-w-xs text-sm">Verifying the constitutional ledger (UEG chain)…</p>
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
              <Sparkles size={20} className="text-aura" /> Awaiting an explicit decision
            </h3>
            <button type="button" onClick={() => setShowProposalForm(v => !v)}
              className="px-5 py-2 border border-aura/30 text-aura font-black rounded-xl text-xs uppercase tracking-widest hover:bg-aura/10 transition-all">
              {showProposalForm ? 'Cancel' : 'New Meta-Proposal'}
            </button>
          </div>

          {showProposalForm && (
            <div className="p-6 bg-aura/5 border border-aura/20 rounded-2xl space-y-4">
              <input
                value={proposalInput}
                onChange={e => setProposalInput(e.target.value)}
                placeholder="Amendment title (e.g. Evolve Article 1096: Post-Quantum Autonomy)..."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-700 focus:outline-none focus:border-aura/50"
              />
              <button
                type="button"
                onClick={submitMetaProposal}
                disabled={submittingProposal || !proposalInput.trim()}
                className="w-full py-3 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest disabled:opacity-50 transition-all"
              >
                {submittingProposal ? 'Submitting…' : 'Submit to CCA'}
              </button>
            </div>
          )}

          {/* W459 — a refused vote or a failed load was silent (sanctumErr was set and never shown) */}
          {sanctumErr && (
            <p className="text-xs font-bold text-vital" data-testid="sanctum-error">{sanctumErr}</p>
          )}

          <div className="space-y-5">
            {proposals.map(p => (
              <div key={p.id} className="p-7 glass-card border-aura/20 bg-aura/5 hover:bg-aura/10 transition-all">
                <div className="flex justify-between items-start mb-5">
                  <div className="text-[10px] font-black text-aura uppercase tracking-[0.2em] border border-aura/30 px-3 py-1 rounded-full">{p.status}</div>
                  <span className="text-sm font-black text-vital">{p.tier ?? 'CRITICAL'} tier{p.change_type ? ` · ${String(p.change_type).replace(/_/g, ' ')}` : ''}</span>
                </div>
                <h4 className="text-xl font-black mb-4 leading-tight">{p.title}</h4>
                {(p.est != null || p.hold_reason || p.follows_rejection) && (
                  <p className="text-[11px] font-bold text-slate-400 mb-4" data-testid="sanctum-hold-detail">
                    {/* W463 — an approval releases ONE later action of this kind of at most this amount (the backend's
                        rule); a rejection refuses exactly this action */}
                    {p.est != null ? `Amount: ${p.est} WST (virtual) — approving releases one action of at most this amount; rejecting refuses exactly this action` : ''}
                    {p.est != null && (p.hold_reason || p.follows_rejection) ? ' · ' : ''}
                    {p.hold_reason ? `Held: ${String(p.hold_reason).replace(/_/g, ' ')}` : ''}
                    {p.hold_reason && p.follows_rejection ? ' · ' : ''}
                    {p.follows_rejection ? `Follows the rejection of ${p.follows_rejection}` : ''}
                  </p>
                )}
                <div className="flex gap-3">
                  <button type="button" onClick={() => castSovereignVote(p.id, 'approved')} disabled={votingId === p.id}
                    className="flex-1 py-3 bg-aura text-sovereign font-black rounded-xl text-xs uppercase tracking-widest disabled:opacity-50">
                    {votingId === p.id ? 'Recording…' : 'Sovereign Approve'}
                  </button>
                  <button type="button" onClick={() => castSovereignVote(p.id, 'rejected')} disabled={votingId === p.id}
                    className="py-3 px-4 bg-vital/15 text-vital border border-vital/30 font-black rounded-xl text-xs uppercase tracking-widest disabled:opacity-50">
                    Reject
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
                      <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Status: <span className="text-aura">{p.status}</span> • Submitted: <span className="text-aura">{p.submitted_at ?? 'unknown'}</span></p>
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
              <Award size={18} className="text-highlight" /> Sovereign Authority
            </h3>
            {/* Ledger cluster 3 — the old panel fabricated a "1,420 reputation / 2.42x voting
                weight / 142 cross-realm contributions" persona. Workstation is Owner-sovereign:
                the real authority is the Owner's override on a CRITICAL-tier change, and the real
                counts come from the CCA store. No invented reputation economy. */}
            <div className="space-y-5">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Authority</p>
                <p className="text-2xl font-black text-white">Owner · sovereign</p>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Awaiting an explicit decision</p>
                <p className="text-xl font-black text-aura">{sanctumErr ? '—' : proposals.length}</p>
              </div>
              <div className="pt-4 border-t border-white/5 text-[10px] text-slate-500 font-bold leading-relaxed">
                A sovereign vote here writes the Owner's decision straight onto the change request in the
                Change Control Agency — a CRITICAL-tier change (every material economy action is one: only
                your explicit decision here releases or refuses it), or one a review held for an explicit
                decision — recorded in that change's own audit trail, as an explicit admin decision, with the
                principal that made it, and, when that write lands, on the constitutional ledger (the confirmation
                says whether it did). A HIGH-tier change a review
                approved is ratified or refused on the Board page instead.
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
