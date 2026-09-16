import { provenanceMapBadge, apiJson, errorMessage } from '../../lib/api';
import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Crown, Loader2, AlertCircle, ShieldCheck, ChevronDown, ChevronUp,
  Users, GitBranch, Sparkles, UserCog,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Director { id: string; title: string; mandate: string }
// W398 — GET /api/v1/board/charter had no caller, so the governance INVARIANT it states was
// invisible in the product: direction flows Owner → Chief → Board → AI CEO, and the AI CEO and below
// cannot instruct the board or mutate the genome. That constraint is the point of the structure.
interface Charter {
  owner?: { name?: string; role?: string; vision_summary?: string };
  arms_length_agency?: string;
  applies_to?: string;
  ratification?: string;   // W464 — the Board's ratification duty
}
// W464 (FU-012) — a HIGH change a review approved, waiting for the Board (GET /api/v1/board/ratifications)
interface PendingRatification {
  cca_id: string; title: string; change_type?: string; impact_tier?: string;
  decision_source?: string; approved_at?: string | null; submitted_by?: string; vsb_id?: string | null;
  description?: string; review_result?: string;
  twin_prevalidation?: { verdict?: string; source?: string; source_label?: string } | null;
}
interface Status {
  board: string; represents_owner: string; hierarchy: string[];
  chief: Director; directors: Director[]; live?: { organism_health?: number };
  recent_directives?: any[];
}
interface ChiefResult {
  directive_id: string; owner: string; instruction: string;
  chief_directive: string; ceo_action_plan: string; delegation_chain: string[]; created_at: string;
  // W270/W284 — the apex runs on the §6 fabric: provenance + gaas verdict + the plan objectives landed
  ai_provenance?: { served_by?: Record<string, number>; any_external?: boolean };
  governance?: { status?: string };
  objectives_added?: number;
  business_plan_scope?: string;
}
// W279/W284 — a persisted board deliberation (directors' REAL grounded inputs)
interface RecentDirective {
  kind?: string; topic?: string; instruction?: string; created_at?: string;
  directors_engaged?: string[];
  director_inputs?: Record<string, { title: string; live_grounding: string; input: string }>;
}

// ── Component ─────────────────────────────────────────────────────────────────

export const BoardOfDirectors: React.FC = () => {
  const [status, setStatus] = useState<Status | null>(null);
  const [instruction, setInstruction] = useState('');
  const [cascade, setCascade] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<ChiefResult | null>(null);
  const [open, setOpen] = useState<'directive' | 'plan'>('directive');
  const [charter, setCharter] = useState<Charter | null>(null);
  const [loadErr, setLoadErr] = useState('');
  // W464 (FU-012) — the ratification queue and the Board's decision on it
  const [ratQueue, setRatQueue] = useState<PendingRatification[] | null>(null);
  const [ratLoadErr, setRatLoadErr] = useState('');
  const [ratNotes, setRatNotes] = useState<Record<string, string>>({});
  const [ownerDirection, setOwnerDirection] = useState<Record<string, boolean>>({});
  const [ratBusy, setRatBusy] = useState<string | null>(null);
  const [ratResult, setRatResult] = useState<{ id: string; ok: boolean; message: string } | null>(null);

  const loadRatifications = async () => {
    try {
      const r = await apiJson<{ pending: PendingRatification[] }>('/api/v1/board/ratifications');
      setRatQueue(r.pending ?? []);
      setRatLoadErr('');
    } catch (e) { setRatLoadErr(`Could not load the ratification queue — ${errorMessage(e)}`); }
  };

  useEffect(() => {
    fetch('/api/v1/board/status').then(r => r.json()).then(setStatus)
      .catch(() => setLoadErr('Could not load the board status.'));
    fetch('/api/v1/board/charter').then(r => r.json()).then(setCharter)
      .catch(() => setLoadErr('Could not load the board charter.'));
    loadRatifications();
  }, []);

  const decideRatification = async (id: string, decision: 'ratify' | 'refuse') => {
    setRatBusy(id); setRatResult(null);
    try {
      const r = await apiJson<{ decision: string; note?: string; ueg_logged?: boolean }>(
        `/api/v1/board/ratifications/${id}`,
        { method: 'POST', body: { decision, notes: ratNotes[id] ?? '', on_owner_direction: ownerDirection[id] === true } });
      setRatResult({ id, ok: true, message: `${r.decision.toUpperCase()} — ${r.note ?? ''}${r.ueg_logged === false ? ' (the ledger entry did not land — see the server log)' : ' Recorded on the constitutional ledger.'}` });
    } catch (e) {
      // the backend's own refusal (403 not an admin / no Owner direction, 409 no longer awaiting) — never a success
      setRatResult({ id, ok: false, message: errorMessage(e) });
    } finally {
      setRatBusy(null);
      loadRatifications();
    }
  };

  const instruct = async () => {
    if (!instruction.trim()) return;
    setRunning(true); setError(''); setResult(null);
    try {
      const r = await fetch('/api/v1/board/chief/instruct', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instruction, owner: status?.represents_owner ?? 'Rehan', cascade_to_ceo: cascade }),
      });
      if (!r.ok) { setError(`HTTP ${r.status}`); setRunning(false); return; }
      setResult(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Apex Governance</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Board of Directors</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The apex governance tier — above the AI CEO. Chaired by your <span className="text-highlight">Chief</span>,
          a digital twin of you ({status?.represents_owner ?? 'the Owner'}) that represents you faithfully in your
          presence and absence, and directs the whole organism on your behalf.
        </p>
      </header>

      {loadErr && (
        <p role="alert" className="text-[10px] font-bold text-vital">{loadErr}</p>
      )}

      {/* W398 — the charter's constitutional invariant, previously fetched by nobody */}
      {charter?.arms_length_agency && (
        <Card className="p-6 border-highlight/20">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-3 flex items-center gap-2">
            <ShieldCheck size={13} /> Charter · the constraint that makes this a governance tier
          </h3>
          <p className="text-xs text-slate-300 font-semibold leading-relaxed">{charter.arms_length_agency}</p>
          {charter.applies_to && (
            <p className="text-[10px] font-bold text-slate-500 mt-3">Applies to: {charter.applies_to}</p>
          )}
          {charter.ratification && (
            <p className="text-[11px] text-slate-400 font-semibold leading-relaxed mt-3" data-testid="board-ratification-duty">{charter.ratification}</p>
          )}
          {charter.owner?.role && (
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-600 mt-3">
              {charter.owner.name ?? 'Owner'} · {charter.owner.role}
            </p>
          )}
        </Card>
      )}

      {/* W464 (FU-012) — the ratification queue: a HIGH change a review approved waits here; nothing implements it
          until the Board records the Owner's decision. No AI call decides it. */}
      <Card className="p-6 space-y-4 border-orange-400/20" data-testid="board-ratifications">
        <div className="flex items-center justify-between gap-3">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-2">
            <ShieldCheck size={13} /> Pending Board ratification
            {ratQueue && <span className="text-orange-300" data-testid="board-ratification-count">{ratQueue.length}</span>}
          </h3>
          <button type="button" onClick={loadRatifications} className="text-[10px] font-bold text-slate-500 hover:text-slate-300">Refresh</button>
        </div>
        <p className="text-[11px] text-slate-500 leading-relaxed">
          A HIGH-tier change approved by a review — the reviewing model&rsquo;s decision marker or the organism-health
          threshold rule, not your explicit decision; a decision made before W459 that recorded no source is read as a
          review&rsquo;s — is not implemented until the Board ratifies it on your direction.
          Refusing it rejects the change. Each decision is recorded on the change and, when that write lands, on the
          constitutional ledger (the result below says whether it did).
        </p>
        {ratLoadErr && <p role="alert" className="text-[10px] font-bold text-vital">{ratLoadErr}</p>}
        {ratQueue && ratQueue.length === 0 && !ratLoadErr && (
          <p className="text-[11px] text-slate-600">No change is waiting for ratification.</p>
        )}
        {ratResult && !(ratQueue ?? []).some(q => q.cca_id === ratResult.id) && (
          <p role="status" data-testid="board-ratification-result" className={`text-[11px] font-bold ${ratResult.ok ? 'text-emerald-400' : 'text-vital'}`}>{ratResult.id}: {ratResult.message}</p>
        )}
        {(ratQueue ?? []).map(q => (
          <div key={q.cca_id} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-2" data-testid="board-ratification-row">
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-black text-white">{q.title}</p>
              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-orange-500/15 text-orange-300">{q.impact_tier}</span>
              <span className="text-[9px] font-mono text-slate-500">{q.change_type} · {q.cca_id}</span>
            </div>
            <p className="text-[11px] text-slate-400">
              approved by: {q.decision_source === 'model_decision_marker' ? 'the reviewing model\u2019s decision marker'
                : q.decision_source === 'health_threshold_rule' ? 'the organism-health threshold rule (not the model)'
                : q.decision_source === 'unrecorded_decision' ? 'a decision made before W459 that recorded no source (read as a review\u2019s)'
                : q.decision_source}
              {q.approved_at ? ` · ${q.approved_at}` : ''}{q.submitted_by ? ` · submitted by ${q.submitted_by}` : ''}{q.vsb_id ? ` · VSB ${q.vsb_id}` : ''}
            </p>
            <p className="text-[11px] text-slate-500">
              §17.5 pre-validation: {q.twin_prevalidation?.verdict
                ? `${q.twin_prevalidation.verdict.toUpperCase()} (${q.twin_prevalidation.source_label ?? q.twin_prevalidation.source})`
                : 'none recorded — implementing it will still need one'}
            </p>
            {q.description && <p className="text-[11px] text-slate-400 leading-relaxed">{q.description}</p>}
            {q.review_result && (
              <details className="text-[10px] text-slate-500"><summary className="cursor-pointer">The review that approved it</summary>
                <pre className="whitespace-pre-wrap font-mono mt-1">{q.review_result}</pre></details>
            )}
            <input value={ratNotes[q.cca_id] ?? ''} onChange={e => setRatNotes(n => ({ ...n, [q.cca_id]: e.target.value }))}
              placeholder="Notes for the record (optional)"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-[11px] text-white placeholder:text-slate-600" />
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" data-testid="board-ratification-owner-direction" checked={ownerDirection[q.cca_id] === true}
                onChange={e => setOwnerDirection(o => ({ ...o, [q.cca_id]: e.target.checked }))} className="accent-highlight w-4 h-4" />
              <span className="text-[11px] font-bold text-slate-400">I record this decision as the Owner&rsquo;s direction</span>
            </label>
            <div className="flex flex-wrap items-center gap-2">
              <Button onClick={() => decideRatification(q.cca_id, 'ratify')} disabled={ratBusy === q.cca_id || ownerDirection[q.cca_id] !== true}
                className="bg-emerald-600/80 text-white text-xs" data-testid="board-ratify">Ratify</Button>
              <Button onClick={() => decideRatification(q.cca_id, 'refuse')} disabled={ratBusy === q.cca_id || ownerDirection[q.cca_id] !== true}
                className="bg-slate-800 text-slate-200 text-xs" data-testid="board-refuse">Refuse</Button>
              {ratBusy === q.cca_id && <Loader2 size={14} className="animate-spin text-slate-500" />}
              {ratResult?.id === q.cca_id && (
                <p role="status" className={`text-[11px] font-bold ${ratResult.ok ? 'text-emerald-400' : 'text-vital'}`}>{ratResult.message}</p>
              )}
            </div>
          </div>
        ))}
      </Card>

      {/* Hierarchy */}
      {status && (
        <Card className="p-6">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4">Governance Hierarchy (arms-length: direction flows down)</h3>
          <div className="flex flex-wrap items-center gap-2">
            {status.hierarchy.map((tier, i) => (
              <React.Fragment key={tier}>
                <span className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest ${i <= 2 ? 'bg-highlight/15 text-highlight border border-highlight/30' : 'bg-slate-900 text-slate-500 border border-slate-800'}`}>{tier}</span>
                {i < status.hierarchy.length - 1 && <ChevronDown size={12} className="text-slate-700 rotate-[-90deg]" />}
              </React.Fragment>
            ))}
          </div>
        </Card>
      )}

      {/* Chief instruction */}
      <Card className="p-8 space-y-6 border-highlight/30 bg-highlight/5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-highlight/20 flex items-center justify-center"><Crown size={18} className="text-highlight" /></div>
          <div>
            <h3 className="font-black text-white text-sm uppercase tracking-wide">Instruct your Chief (your Digital Twin)</h3>
            <p className="text-[10px] text-slate-500 font-bold">Faithfully interpreted → board directive → delegated to the AI CEO</p>
          </div>
        </div>
        <textarea
          value={instruction}
          onChange={e => setInstruction(e.target.value)}
          placeholder="Give your Chief an instruction — a wish, a priority, a decision. It will represent you precisely and direct the organism accordingly."
          rows={3}
          className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none"
        />
        <div className="flex flex-wrap items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={cascade} onChange={e => setCascade(e.target.checked)} className="accent-highlight w-4 h-4" />
            <span className="text-[11px] font-bold text-slate-400">Delegate a timelined action plan to the AI CEO</span>
          </label>
          <Button onClick={instruct} disabled={running || !instruction.trim()} className="flex items-center gap-2 bg-highlight text-sovereign ml-auto">
            {running ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {running ? 'Chief deliberating…' : 'Issue Instruction'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {/* Chief result */}
      {result && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-[9px] font-mono text-slate-500">
            <ShieldCheck size={12} className="text-slate-500" /> {result.directive_id} · chain: {result.delegation_chain.join(' → ')}
          </div>
          {/* W270/W284 — apex honesty chips: which OWNED resource served, the gaas verdict, what landed on the plan */}
          <div className="flex flex-wrap items-center gap-1.5">
            {result.ai_provenance?.served_by && (
              (() => { const b = provenanceMapBadge(result.ai_provenance?.served_by, result.ai_provenance?.any_external); return <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`} title={`${b.title ? b.title + ' — ' : ''}calls: ${Object.entries(result.ai_provenance?.served_by ?? {}).map(([k, v]) => `${k}×${v}`).join(' · ') || 'none'}`}>{b.label}</span>; })()
            )}
            {result.governance?.status && (
              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${result.governance.status === 'allowed' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>gaas: {result.governance.status}</span>
            )}
            {typeof result.objectives_added === 'number' && (
              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${result.objectives_added > 0 ? 'bg-highlight/15 text-highlight' : 'bg-slate-800 text-slate-500'}`}>
                {result.objectives_added} objective{result.objectives_added === 1 ? '' : 's'} → living plan{result.business_plan_scope ? ` (${result.business_plan_scope})` : ''}
              </span>
            )}
          </div>
          <Card className="p-0 overflow-hidden border-slate-800/80">
            <button type="button" onClick={() => setOpen('directive')} className={`w-full flex items-center justify-between p-5 text-left ${open === 'directive' ? 'bg-slate-800/30' : ''}`}>
              <div className="flex items-center gap-3"><Crown size={14} className="text-highlight" /><p className="font-black text-white text-sm">Chief's Board Directive</p></div>
              {open === 'directive' ? <ChevronUp size={14} className="text-slate-500" /> : <ChevronDown size={14} className="text-slate-500" />}
            </button>
            {open === 'directive' && <div className="px-5 pb-6 border-t border-slate-800/50 pt-4"><p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{result.chief_directive}</p></div>}
          </Card>
          {result.ceo_action_plan && (
            <Card className="p-0 overflow-hidden border-slate-800/80">
              <button type="button" onClick={() => setOpen('plan')} className={`w-full flex items-center justify-between p-5 text-left ${open === 'plan' ? 'bg-slate-800/30' : ''}`}>
                <div className="flex items-center gap-3"><GitBranch size={14} className="text-aura" /><p className="font-black text-white text-sm">AI CEO Action Plan (delegated)</p></div>
                {open === 'plan' ? <ChevronUp size={14} className="text-slate-500" /> : <ChevronDown size={14} className="text-slate-500" />}
              </button>
              {open === 'plan' && <div className="px-5 pb-6 border-t border-slate-800/50 pt-4"><p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{result.ceo_action_plan}</p></div>}
            </Card>
          )}
        </div>
      )}

      {/* W279/W284 — recent board deliberations: the directors' REAL grounded inputs, previously
          typed on Status but never rendered */}
      {(status?.recent_directives ?? []).filter((d: RecentDirective) => d.director_inputs || d.topic || d.instruction).length > 0 && (
        <div>
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><GitBranch size={14} /> Recent Board Deliberations</h3>
          <div className="space-y-3">
            {(status!.recent_directives as RecentDirective[]).slice(-5).reverse().map((d, i) => (
              <Card key={i} className="p-5 space-y-2">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-500">{d.kind ?? 'chief_instruction'}</span>
                  <p className="text-sm font-black text-white">{d.topic ?? d.instruction}</p>
                  <span className="text-[8px] text-slate-600 ml-auto">{d.created_at}</span>
                </div>
                {d.director_inputs && Object.values(d.director_inputs).map(di => (
                  <div key={di.title} className="border-l-2 border-highlight/30 pl-3 space-y-0.5">
                    <p className="text-[10px] font-black uppercase text-highlight">{di.title}</p>
                    <p className="text-[9px] text-slate-500 italic">live grounding: {di.live_grounding}</p>
                    <p className="text-[11px] text-slate-300 leading-relaxed">{di.input.slice(0, 400)}{di.input.length > 400 ? '…' : ''}</p>
                  </div>
                ))}
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Board roster */}
      {status && (
        <div>
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Users size={14} /> The Board</h3>
          <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-3">
            <div className="p-5 rounded-2xl bg-highlight/10 border border-highlight/30">
              <div className="flex items-center gap-2 mb-1"><Crown size={15} className="text-highlight" /><p className="font-black text-white text-sm">{status.chief.title}</p></div>
              <p className="text-[11px] text-slate-400 leading-relaxed">{status.chief.mandate}</p>
            </div>
            {status.directors.map(d => (
              <div key={d.id} className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
                <div className="flex items-center gap-2 mb-1"><UserCog size={15} className="text-slate-400" /><p className="font-black text-white text-sm">{d.title}</p></div>
                <p className="text-[11px] text-slate-500 leading-relaxed">{d.mandate}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
