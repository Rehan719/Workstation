import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * FU-471, option 3 (Owner ruling 2026-10-06) — the two RECORDS the avatar's clearance gates read.
 *
 * Gate 2 counts a learner's standing approval of what the avatar is for; a message is never a signature.
 * Gate 3 balances each reply over the Owner's recorded goals. Neither is assumed: until both exist, a reply is
 * withheld and says which one is missing. Scope is by MODE, not by content.
 */
export const AvatarClearancePanel: React.FC = () => {
  const [rats, setRats] = useState<Dict[]>([]);
  const [highImpact, setHighImpact] = useState<string[]>([]);
  const [purpose, setPurpose] = useState('');
  const [goals, setGoals] = useState<Dict | null>(null);
  const [err, setErr] = useState('');

  const load = async () => {
    try {
      const r = await apiJson<Dict>('/api/v1/avatar/ratifications');
      setRats(r.ratifications || []);
      setHighImpact(r.high_impact_modes || []);
      setGoals(await apiJson<Dict>('/api/v1/avatar/balance-objectives'));
      setErr('');
    } catch (e: any) {
      setErr(`The avatar's clearance records could not be read: ${String(e?.message ?? e)}`);
    }
  };
  useEffect(() => { load(); }, []);

  const record = async () => {
    try {
      await apiJson('/api/v1/avatar/ratifications', { method: 'POST', body: { purpose, modes: ['instructor'] } });
      setPurpose('');
      await load();
    } catch (e: any) { setErr(`Not recorded: ${String(e?.message ?? e)}`); }
  };
  const revoke = async (id: string) => {
    try { await apiJson(`/api/v1/avatar/ratifications/${id}/revoke`, { method: 'POST' }); await load(); }
    catch (e: any) { setErr(`Not revoked: ${String(e?.message ?? e)}`); }
  };

  const active = rats.filter(r => !r.revoked_at);
  return (
    <div className="space-y-3" data-testid="avatar-clearance-panel">
      <h3 className="text-sm font-black text-white uppercase tracking-wide">What I want the avatar for</h3>
      <p className="text-[11px] text-slate-500 leading-relaxed">
        The avatar's replies are checked by a constitutional clearance chain. One check asks whether you approved
        what the avatar is doing: a message on its own never counts. Record it once here; you can withdraw it at
        any time. The approval covers a MODE, not particular words. {highImpact.length > 0 && <>High-impact modes
        ({highImpact.join(', ')}) also need the Owner's co-signature.</>}
      </p>
      {err && <p className="text-[10px] text-vital" data-testid="avatar-clearance-error">{err}</p>}
      <ul className="space-y-1" data-testid="avatar-ratifications">
        {active.length === 0 && <li className="text-[10px] text-amber-400/90">No approval is recorded, so replies are not cleared by the chain.</li>}
        {active.map(r => (
          <li key={r.id} className="text-[10px] text-slate-300 flex items-center gap-2">
            <span>{String(r.purpose)} · modes {(r.modes || []).join(', ')} · signed by {(r.signatories || []).join(', ')}</span>
            <button type="button" className="px-2 py-0.5 rounded border border-slate-700 text-[9px]"
              onClick={() => revoke(r.id)}>Withdraw</button>
          </li>
        ))}
      </ul>
      <div className="flex gap-2">
        <input value={purpose} onChange={e => setPurpose(e.target.value)} placeholder="e.g. help me revise maths"
          className="flex-1 bg-slate-950 border border-slate-800 rounded px-2 py-1 text-[11px] text-slate-200"
          data-testid="avatar-ratification-purpose" />
        <button type="button" disabled={!purpose.trim()} onClick={record} data-testid="avatar-ratification-record"
          className="px-3 py-1 rounded bg-slate-800 text-[10px] text-white disabled:opacity-40">Record approval</button>
      </div>
      <p className="text-[10px] text-slate-500 leading-relaxed" data-testid="avatar-balance-goals">
        Reply goals (set by the Owner):{' '}
        {goals && Array.isArray(goals.objectives) && goals.objectives.length > 0
          ? goals.objectives.map((o: Dict) => `${o.name} → ${o.direction}`).join(' · ') + ` (${String(goals.basis ?? '')})`
          : `none recorded — ${String(goals?.basis ?? 'not read')}`}
      </p>
    </div>
  );
};

export default AvatarClearancePanel;
