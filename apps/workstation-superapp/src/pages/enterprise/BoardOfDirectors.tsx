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

  useEffect(() => {
    fetch('/api/v1/board/status').then(r => r.json()).then(setStatus)
      .catch(() => setLoadErr('Could not load the board status.'));
    fetch('/api/v1/board/charter').then(r => r.json()).then(setCharter)
      .catch(() => setLoadErr('Could not load the board charter.'));
  }, []);

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
          {charter.owner?.role && (
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-600 mt-3">
              {charter.owner.name ?? 'Owner'} · {charter.owner.role}
            </p>
          )}
        </Card>
      )}

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
            <ShieldCheck size={12} className="text-emerald-400" /> {result.directive_id} · chain: {result.delegation_chain.join(' → ')}
          </div>
          {/* W270/W284 — apex honesty chips: which OWNED resource served, the gaas verdict, what landed on the plan */}
          <div className="flex flex-wrap items-center gap-1.5">
            {result.ai_provenance?.served_by && (
              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${result.ai_provenance.any_external ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                served by {Object.entries(result.ai_provenance.served_by).map(([k, v]) => `${k}×${v}`).join(' · ')}{result.ai_provenance.any_external ? '' : ' · in-house'}
              </span>
            )}
            {result.governance?.status && (
              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300">gaas: {result.governance.status}</span>
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
