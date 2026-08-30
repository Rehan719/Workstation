import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  GitBranch, CheckCircle2, XCircle, Clock, Loader2,
  Plus, RefreshCw, ChevronDown, ChevronUp, Zap, Shield, Undo2,
  type LucideIcon
} from 'lucide-react';

// ── Types — matched to the REAL backend contract (agentic_core/api/change_control.py):
//    list rows carry cca_id / impact_tier / lowercase status; the full record (description,
//    review_result, twin_prevalidation) lives on GET /api/v1/cca/{cca_id}. (Ledger cluster 1.)

type Tier = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
type Status = 'submitted' | 'under_review' | 'approved' | 'rejected' | 'implemented' | 'withdrawn';

interface CCARow {
  cca_id: string;
  title: string;
  change_type: string;
  impact_tier: Tier;
  status: Status;
  submitted_by?: string;
  submitted_at: string;
  reviewed_at?: string | null;
  decision?: string | null;
}

interface CCADetail extends CCARow {
  description?: string;
  rationale?: string | null;
  review_result?: string | null;
  rollback_plan?: string | null;
  twin_prevalidation?: { verdict?: string; source?: string } | null;
}

interface CCAStats {
  total: number;
  pending: number;
  approved: number;
  rejected: number;
  implemented: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const TIER_COLORS: Record<Tier, string> = {
  LOW:      'text-green-400 bg-green-500/10 border-green-500/20',
  MEDIUM:   'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
  HIGH:     'text-orange-400 bg-orange-500/10 border-orange-500/20',
  CRITICAL: 'text-red-400 bg-red-500/10 border-red-500/20',
};

const STATUS_COLORS: Record<Status, string> = {
  submitted:    'text-yellow-400',
  under_review: 'text-amber-400',
  approved:     'text-green-400',
  rejected:     'text-red-400',
  implemented:  'text-blue-400',
  withdrawn:    'text-slate-400',
};

const STATUS_ICONS: Record<Status, LucideIcon> = {
  submitted:    Clock,
  under_review: Shield,
  approved:     CheckCircle2,
  rejected:     XCircle,
  implemented:  Zap,
  withdrawn:    Undo2,
};

const CHANGE_TYPES = [
  { value: 'config_minor',       label: 'Config — Minor',        tier: 'LOW'      },
  { value: 'config_major',       label: 'Config — Major',        tier: 'MEDIUM'   },
  { value: 'organism_mutation',  label: 'Organism Mutation',     tier: 'HIGH'     },
  { value: 'constitutional',     label: 'Constitutional Change',  tier: 'CRITICAL' },
];

function fmtDate(iso: string) {
  try { return new Date(iso).toLocaleString(); } catch { return iso; }
}

const isPending = (s: Status) => s === 'submitted' || s === 'under_review';

// ── Entry card ────────────────────────────────────────────────────────────────

function CCACard({ entry, onReview, onImplement, refreshing, actionError }: {
  entry: CCARow;
  onReview: (id: string) => void;
  onImplement: (id: string) => void;
  refreshing: string | null;
  actionError: { id: string; message: string } | null;
}) {
  const [expanded, setExpanded] = useState(false);
  const [detail, setDetail] = useState<CCADetail | null>(null);
  const Icon = STATUS_ICONS[entry.status] ?? Clock;

  // The list row is intentionally thin — the description/review live on the detail record.
  const toggle = async () => {
    const opening = !expanded;
    setExpanded(opening);
    if (opening && !detail) {
      try {
        const r = await axios.get(`/api/v1/cca/${entry.cca_id}`);
        setDetail(r.data);
      } catch { /* the row still renders; detail pane shows an honest fallback below */ }
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/4 border border-white/10 rounded-xl overflow-hidden"
    >
      <div className="flex items-start gap-3 p-4 cursor-pointer hover:bg-white/3" onClick={toggle}>
        <Icon size={16} className={`mt-0.5 shrink-0 ${STATUS_COLORS[entry.status] ?? 'text-white/40'}`} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <p className="text-sm font-semibold text-white leading-tight">{entry.title}</p>
            <div className="flex items-center gap-2 shrink-0">
              <span className={`text-xs px-2 py-0.5 rounded border font-mono ${TIER_COLORS[entry.impact_tier] ?? TIER_COLORS.MEDIUM}`}>{entry.impact_tier}</span>
              {entry.decision === 'auto_approved' && (
                <span className="text-xs px-2 py-0.5 rounded border text-green-400 bg-green-500/10 border-green-500/20">AUTO</span>
              )}
              <span className={`text-xs font-mono uppercase ${STATUS_COLORS[entry.status] ?? 'text-white/40'}`}>{entry.status.replace('_', ' ')}</span>
            </div>
          </div>
          <div className="flex items-center gap-3 mt-1 text-xs text-white/40">
            <span className="font-mono">{entry.change_type}</span>
            <span>·</span>
            <span>{fmtDate(entry.submitted_at)}</span>
            {entry.submitted_by && (
              <>
                <span>·</span>
                <span>{entry.submitted_by}</span>
              </>
            )}
          </div>
        </div>
        {expanded ? <ChevronUp size={14} className="text-white/30 shrink-0 mt-1" /> : <ChevronDown size={14} className="text-white/30 shrink-0 mt-1" />}
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0 }} animate={{ height: 'auto' }} exit={{ height: 0 }}
            className="overflow-hidden border-t border-white/8"
          >
            <div className="p-4 space-y-3">
              {detail
                ? <p className="text-sm text-white/60">{detail.description || 'No description recorded.'}</p>
                : <p className="text-sm text-white/30">Loading details…</p>}

              {detail?.review_result && (
                <div className="bg-white/3 border border-white/8 rounded-lg p-3">
                  <p className="text-xs text-white/40 mb-1 font-semibold uppercase tracking-wider">
                    Review {detail.decision ? `— ${detail.decision.replace('_', ' ')}` : ''}
                  </p>
                  <pre className="text-xs text-white/60 font-mono whitespace-pre-wrap leading-relaxed">{detail.review_result}</pre>
                </div>
              )}

              {detail?.twin_prevalidation?.verdict && (
                <p className="text-xs font-mono text-white/40">
                  §17.5 twin pre-validation:{' '}
                  <span className={detail.twin_prevalidation.verdict === 'pass' ? 'text-green-400' : 'text-red-400'}>
                    {detail.twin_prevalidation.verdict.toUpperCase()}
                  </span>{' '}({detail.twin_prevalidation.source})
                </p>
              )}

              <div className="flex items-center gap-2 pt-1">
                {isPending(entry.status) && (
                  <button
                    onClick={e => { e.stopPropagation(); onReview(entry.cca_id); }}
                    disabled={refreshing === entry.cca_id}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600/20 hover:bg-blue-600/35 text-blue-300 border border-blue-500/25 disabled:opacity-50"
                  >
                    {refreshing === entry.cca_id ? <Loader2 size={12} className="animate-spin" /> : <Shield size={12} />}
                    AI Review
                  </button>
                )}
                {entry.status === 'approved' && (
                  <button
                    onClick={e => { e.stopPropagation(); onImplement(entry.cca_id); }}
                    disabled={refreshing === entry.cca_id}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-green-600/20 hover:bg-green-600/35 text-green-300 border border-green-500/25 disabled:opacity-50"
                  >
                    {refreshing === entry.cca_id ? <Loader2 size={12} className="animate-spin" /> : <Zap size={12} />}
                    Implement
                  </button>
                )}
                <span className="text-xs text-white/30 font-mono">{entry.cca_id}</span>
              </div>

              {actionError?.id === entry.cca_id && (
                <p className="text-xs text-red-400">{actionError.message}</p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

// ── Submit form ───────────────────────────────────────────────────────────────

function SubmitForm({ onSubmitted }: { onSubmitted: () => void }) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [type, setType] = useState('config_minor');
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const submit = async () => {
    if (!title.trim() || !desc.trim()) return;
    setLoading(true); setMsg(null);
    try {
      const res = await axios.post('/api/v1/cca/submit', {
        title, description: desc, change_type: type, submitted_by: 'workstation-ui'
      });
      // Auto-approval is signalled by the returned status (the backend sends no auto_approved key).
      setMsg(res.data.status === 'approved'
        ? '✓ Change auto-approved (LOW tier + healthy organism)'
        : '✓ Change submitted — awaiting AI review');
      setTitle(''); setDesc(''); setType('config_minor');
      setTimeout(() => { onSubmitted(); setOpen(false); setMsg(null); }, 1500);
    } catch (e: any) {
      setMsg(`Error: ${e?.response?.data?.detail ?? 'request failed'}`);
    } finally { setLoading(false); }
  };

  return (
    <div>
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/25 hover:bg-blue-600/40 text-blue-300 border border-blue-500/25 font-semibold text-sm"
      >
        <Plus size={14} />
        Submit Change Request
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-3 bg-white/5 border border-white/12 rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-bold text-white">New Change Request</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="flex flex-col gap-1">
                  <label className="text-xs text-white/40 uppercase tracking-wider font-mono">Title</label>
                  <input
                    value={title} onChange={e => setTitle(e.target.value)}
                    placeholder="Brief change title"
                    className="bg-white/5 border border-white/15 rounded-lg px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-white/30"
                  />
                </div>
                <div className="flex flex-col gap-1">
                  <label className="text-xs text-white/40 uppercase tracking-wider font-mono">Change Type</label>
                  <select
                    value={type} onChange={e => setType(e.target.value)}
                    className="bg-white/5 border border-white/15 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-white/30"
                  >
                    {CHANGE_TYPES.map(ct => (
                      <option key={ct.value} value={ct.value} className="bg-slate-900">
                        {ct.label} ({ct.tier})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-xs text-white/40 uppercase tracking-wider font-mono">Description</label>
                <textarea
                  value={desc} onChange={e => setDesc(e.target.value)}
                  placeholder="Describe the change, rationale, and expected impact..."
                  rows={3}
                  className="bg-white/5 border border-white/15 rounded-lg px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-white/30 resize-none"
                />
              </div>

              {/* Tier indicator */}
              <div className="flex items-center gap-2 text-xs text-white/40">
                <Shield size={12} />
                <span>Tier: <span className={`font-semibold ${TIER_COLORS[CHANGE_TYPES.find(c=>c.value===type)?.tier as Tier ?? 'LOW'].split(' ')[0]}`}>
                  {CHANGE_TYPES.find(c => c.value === type)?.tier}
                </span></span>
                <span>— LOW tier changes are auto-approved when organism health ≥ 60%</span>
              </div>

              {msg && (
                <p className={`text-sm ${msg.startsWith('Error') ? 'text-red-400' : 'text-green-400'}`}>{msg}</p>
              )}

              <div className="flex gap-2">
                <button
                  onClick={submit}
                  disabled={loading || !title.trim() || !desc.trim()}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/30 hover:bg-blue-600/50 text-blue-300 border border-blue-500/25 font-semibold text-sm disabled:opacity-50"
                >
                  {loading ? <Loader2 size={14} className="animate-spin" /> : <Plus size={14} />}
                  Submit
                </button>
                <button onClick={() => setOpen(false)} className="px-4 py-2 rounded-xl text-sm text-white/40 hover:text-white/60 hover:bg-white/5">
                  Cancel
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

type FilterTab = 'all' | 'pending' | 'approved' | 'rejected' | 'implemented';

export const ChangeControlAgency: React.FC = () => {
  const [entries, setEntries] = useState<CCARow[]>([]);
  const [filter, setFilter] = useState<FilterTab>('all');
  const [stats, setStats] = useState<CCAStats>({ total: 0, pending: 0, approved: 0, rejected: 0, implemented: 0 });
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [actionId, setActionId] = useState<string | null>(null);
  const [actionError, setActionError] = useState<{ id: string; message: string } | null>(null);

  const load = useCallback(async () => {
    try {
      // NOTE: no trailing slash — the SPA catch-all route intercepts '/api/v1/cca/' before
      // FastAPI's slash-redirect can fire, returning 404. (Discovered by the cluster-1 probe.)
      const allRes = await axios.get('/api/v1/cca');
      const all: CCARow[] = allRes.data.changes ?? [];
      setEntries(all);
      setLoadError(null);
      const pending = all.filter(e => isPending(e.status)).length;
      const approved = all.filter(e => e.status === 'approved').length;
      const rejected = all.filter(e => e.status === 'rejected').length;
      const implemented = all.filter(e => e.status === 'implemented').length;
      setStats({ total: all.length, pending, approved, rejected, implemented });
    } catch {
      setLoadError('Could not load the change queue — backend unreachable.');
    } finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const runAction = async (id: string, act: () => Promise<unknown>) => {
    setActionId(id); setActionError(null);
    try {
      await act();
      await load();
    } catch (e: any) {
      // Surface the real reason — the 409s here (twin pre-validation) are meaningful governance messages.
      setActionError({ id, message: String(e?.response?.data?.detail ?? 'Request failed — backend unreachable.') });
    } finally { setActionId(null); }
  };

  const triggerReview = (id: string) =>
    // ReviewDecision body is required by the endpoint; empty overrides = "let the AI decide".
    runAction(id, () => axios.post(`/api/v1/cca/${id}/review`, { reviewer_notes: 'Requested via the Change Control Agency UI' }));

  const triggerImplement = (id: string) =>
    runAction(id, () => axios.post(`/api/v1/cca/${id}/implement`));

  const filtered = filter === 'all'
    ? entries
    : filter === 'pending'
      ? entries.filter(e => isPending(e.status))
      : entries.filter(e => e.status === filter);

  const FILTER_TABS: { id: FilterTab; label: string; count: number; color: string }[] = [
    { id: 'all',         label: 'All',         count: stats.total,       color: 'text-white/60'   },
    { id: 'pending',     label: 'Pending',      count: stats.pending,     color: 'text-yellow-400' },
    { id: 'approved',    label: 'Approved',     count: stats.approved,    color: 'text-green-400'  },
    { id: 'rejected',    label: 'Rejected',     count: stats.rejected,    color: 'text-red-400'    },
    { id: 'implemented', label: 'Implemented',  count: stats.implemented, color: 'text-blue-400'   },
  ];

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
          <GitBranch size={22} className="text-purple-400" />
          Change Control Agency
        </h1>
        <p className="text-sm text-white/40 mt-1">Governance gateway — every organism change is tier-gated, AI-reviewed, and logged</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: 'Pending', value: stats.pending, color: 'text-yellow-400' },
          { label: 'Approved', value: stats.approved, color: 'text-green-400' },
          { label: 'Rejected', value: stats.rejected, color: 'text-red-400' },
          { label: 'Implemented', value: stats.implemented, color: 'text-blue-400' },
        ].map(s => (
          <div key={s.label} className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
            <p className={`text-2xl font-black ${s.color}`}>{s.value}</p>
            <p className="text-xs text-white/40 mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Tier legend */}
      <div className="flex flex-wrap gap-2 text-xs">
        {CHANGE_TYPES.map(ct => (
          <span key={ct.value} className={`px-2 py-1 rounded border font-mono ${TIER_COLORS[ct.tier as Tier]}`}>
            {ct.tier} — {ct.label}
          </span>
        ))}
      </div>

      {/* Submit + Refresh */}
      <div className="flex items-center gap-3">
        <SubmitForm onSubmitted={load} />
        <button onClick={load} className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold text-white/40 hover:text-white/70 hover:bg-white/5 border border-white/8">
          <RefreshCw size={12} />
          Refresh
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {FILTER_TABS.map(ft => (
          <button
            key={ft.id}
            onClick={() => setFilter(ft.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-semibold border transition-all ${
              filter === ft.id
                ? 'bg-white/10 border-white/20 text-white'
                : 'bg-white/3 border-white/8 text-white/40 hover:text-white/60'
            }`}
          >
            {ft.label}
            <span className={`ml-1.5 ${ft.color}`}>{ft.count}</span>
          </button>
        ))}
      </div>

      {/* Entry list */}
      {loading ? (
        <div className="flex items-center justify-center py-20 text-white/30">
          <Loader2 size={20} className="animate-spin mr-2" />
          Loading change queue...
        </div>
      ) : loadError ? (
        <div className="text-center py-16">
          <p className="text-sm text-red-400">{loadError}</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 text-white/25">
          <GitBranch size={36} className="mx-auto mb-3 opacity-30" />
          <p className="text-sm">
            {filter === 'all' ? 'No change requests yet. Submit one above.' : `No ${filter} changes.`}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {filtered.map(entry => (
              <CCACard
                key={entry.cca_id}
                entry={entry}
                onReview={triggerReview}
                onImplement={triggerImplement}
                refreshing={actionId}
                actionError={actionError}
              />
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
};

export default ChangeControlAgency;
