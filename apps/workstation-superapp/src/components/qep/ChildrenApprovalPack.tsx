import React, { useCallback, useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { apiJson, errorMessage } from '../../lib/api';

// W739 (P5.21, Owner ruling 2026-10-14: "I want the tools built so that the scholar can see what to approve as a
// whole") — THE CHILDREN'S TOOLS, SEEN AND DECIDED AS ONE. Everything a child could meet is in one pack: the rules
// every children's tool keeps, each tool as a child would meet it, and the learner-facing text awaiting a decision
// (listed in full below this card). One decision covers the whole pack and is bound to its fingerprint: a change to
// any part re-opens review. No children's tool opens until sign-in is on AND the current pack is approved.

interface Rule { id: string; rule: string }
interface Tool { id: string; name: string; run_by: string; what_a_child_sees: string; steps?: string[]; wording?: string[]; arabic_from?: string }
interface Pack {
  pack_hash: string; state: string; basis: string; whole: string;
  sections: { rules: Rule[]; tools: Tool[]; learner_content: unknown[] };
  counts: { rules: number; tools: number; learner_content: number };
  children_tools: { open: boolean; basis: string };
}

export const ChildrenApprovalPack: React.FC<{ roster: [string, { name: string }][]; chosen: string }> = ({ roster, chosen }) => {
  const [pack, setPack] = useState<Pack | null>(null);
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [notes, setNotes] = useState('');
  const [busy, setBusy] = useState(false);
  const load = useCallback(async () => {
    try { setPack(await apiJson<Pack>('/api/v1/scholar-review/pack')); setErr(''); }
    catch (e) { setErr(`The approval pack could not be read. ${errorMessage(e)}`); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  const decide = async (decision: 'approve' | 'return') => {
    if (!pack) return;
    setBusy(true); setMsg('');
    try {
      await apiJson('/api/v1/scholar-review/pack/decide', { method: 'POST',
        body: { scholar_id: chosen, decision, notes, seen_hash: pack.pack_hash } });
      setMsg(decision === 'approve' ? 'The whole pack is recorded as approved.' : 'The pack is recorded as returned, with your notes.');
      setNotes(''); await load();
    } catch (e) { setMsg(`Not recorded. ${errorMessage(e)}`); }
    setBusy(false);
  };

  return (
    <Card className="p-6 border-aura/30 bg-aura/5" data-testid="children-approval-pack">
      <h4 className="text-[10px] font-black uppercase tracking-widest text-aura mb-2">The children's tools — one approval pack</h4>
      {err && <p role="alert" className="text-xs text-vital font-semibold mb-2">{err}</p>}
      {pack && (<>
        <p className="text-[11px] text-slate-300 leading-relaxed" data-testid="pack-state">
          State: <span className="font-bold text-white">{pack.state.replace(/_/g, ' ')}</span> — {pack.basis}. {pack.whole}.
        </p>
        <p className="text-[11px] text-amber-400 font-semibold mt-1" data-testid="pack-gate">Children's tools: {pack.children_tools.basis}</p>
        <p className="text-[9px] text-slate-600 font-mono mt-1">pack {pack.pack_hash} · {pack.counts.rules} rules · {pack.counts.tools} tools · {pack.counts.learner_content} learner texts (listed below)</p>
        <a href="/api/v1/scholar-review/pack.md" download="children-tools-approval-pack.md" className="inline-block text-[11px] text-aura font-bold underline mt-2">Download the whole pack as one document</a>

        <h5 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mt-4 mb-2">1. The rules every children's tool keeps</h5>
        <ul className="space-y-1">{pack.sections.rules.map(r => <li key={r.id} className="text-[11px] text-slate-300"><span className="font-bold text-white">{r.id}</span> {r.rule}</li>)}</ul>

        <h5 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mt-4 mb-2">2. The tools, as a child would meet them</h5>
        {pack.sections.tools.length === 0
          ? <p className="text-[11px] text-slate-500">No children's tool is built yet. Each one is added to this pack in the change that builds it, so nothing reaches review unseen.</p>
          : pack.sections.tools.map(t => (
            <div key={t.id} className="p-3 rounded-xl bg-slate-950 border border-slate-900 mb-2" data-testid="pack-tool">
              <p className="text-[11px] font-bold text-white">{t.name} <span className="text-slate-500 font-normal">— run by {t.run_by}</span></p>
              <p className="text-[11px] text-slate-300 mt-1">{t.what_a_child_sees}</p>
              {t.steps && <ol className="list-decimal ml-5 mt-1 text-[11px] text-slate-400">{t.steps.map((s, i) => <li key={i}>{s}</li>)}</ol>}
              {t.wording && <div className="mt-1">{t.wording.map((w, i) => <p key={i} className="text-[11px] text-slate-300 italic">“{w}”</p>)}</div>}
              {t.arabic_from && <p className="text-[10px] text-slate-500 mt-1">Arabic from: {t.arabic_from}</p>}
            </div>
          ))}

        <h5 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mt-4 mb-2">3. The decision on the whole pack</h5>
        {roster.length === 0
          ? <p className="text-[11px] text-slate-500" data-testid="pack-no-scholar">No scholar is on the roster, so no decision on the pack can be recorded.</p>
          : (<>
            <textarea aria-label="Notes on the pack" value={notes} onChange={e => setNotes(e.target.value)} rows={3}
              placeholder="notes for the whole pack (what to change, if returned)"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white" />
            <div className="flex gap-2 mt-2">
              <Button type="button" disabled={busy || !chosen} onClick={() => decide('approve')} className="text-xs">Approve the whole pack</Button>
              <Button type="button" disabled={busy || !chosen} onClick={() => decide('return')} className="text-xs">Return with notes</Button>
            </div>
            {!chosen && <p className="text-[10px] text-slate-500 mt-1">Choose the scholar the decision is entered for, below.</p>}
          </>)}
        {msg && <p role="status" className="text-[11px] text-slate-300 mt-2">{msg}</p>}
      </>)}
    </Card>
  );
};
