import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * P3.30 r5 (Owner ruling 2026-10-11) - the protected-entities record, and the one place the Owner names
 * their own enterprises on it. Every sentence about the STATE comes from the route; nothing here decides
 * whether an enterprise is protected. Until the Owner's own are named, every removal stays refused.
 */
export const ProtectedEntitiesPanel: React.FC = () => {
  const [rec, setRec] = useState<Dict | null>(null);
  const [rows, setRows] = useState<{ id: string; why: string }[]>([{ id: '', why: '' }, { id: '', why: '' }]);
  const [confirm, setConfirm] = useState(false);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  const load = async () => {
    try { setRec(await apiJson<Dict>('/api/v1/economy/protected-entities')); setErr(''); }
    catch (e: any) { setErr(`The protected-entities record could not be read: ${String(e?.message ?? e)}`); }
  };
  useEffect(() => { load(); }, []);

  const save = async () => {
    setMsg(''); setErr('');
    const entities = Object.fromEntries(rows.filter(r => r.id.trim()).map(r => [r.id.trim(), r.why.trim()]));
    try {
      const r = await apiJson<Dict>('/api/v1/economy/protected-entities', {
        method: 'PUT', body: { entities, owner_confirms: confirm } });
      setMsg(String(r.basis ?? 'Recorded.'));
      await load();
    } catch (e: any) { setErr(`Not recorded: ${String(e?.message ?? e)}`); }
  };

  const named = Object.entries((rec?.named ?? {}) as Record<string, string>);
  return (
    <div className="space-y-3" data-testid="protected-entities-panel">
      <h3 className="text-sm font-black text-white uppercase tracking-wide">Protected enterprises</h3>
      {rec && <p className="text-[11px] text-slate-400 leading-relaxed" data-testid="protected-entities-rule">{String(rec.rule ?? '')}</p>}
      {rec && (
        <p className={`text-[11px] leading-relaxed font-bold ${rec.state === 'named' ? 'text-emerald-400' : 'text-amber-400'}`}
           data-testid="protected-entities-state">{String(rec.basis ?? '')}</p>
      )}
      {err && <p className="text-[10px] text-vital" data-testid="protected-entities-error">{err}</p>}
      {msg && <p className="text-[10px] text-emerald-400" data-testid="protected-entities-saved">{msg}</p>}
      {rec && (
        <ul className="space-y-1" data-testid="protected-entities-list">
          {((rec.apex ?? []) as string[]).map(a => (
            <li key={a} className="text-[10px] text-slate-300">{a} · the apex</li>
          ))}
          {named.map(([id, why]) => (
            <li key={id} className="text-[10px] text-slate-300">{id} · {String(why)}</li>
          ))}
        </ul>
      )}
      <div className="space-y-2">
        {rows.map((r, i) => (
          <div key={i} className="flex flex-wrap gap-2">
            <input aria-label={`Enterprise id ${i + 1}`} value={r.id} placeholder="vsb-…"
              onChange={e => setRows(prev => prev.map((x, k) => (k === i ? { ...x, id: e.target.value } : x)))}
              className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 font-mono" />
            <input aria-label={`Why enterprise ${i + 1} is protected`} value={r.why} placeholder="why it is protected"
              onChange={e => setRows(prev => prev.map((x, k) => (k === i ? { ...x, why: e.target.value } : x)))}
              className="flex-1 min-w-[180px] bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300" />
          </div>
        ))}
        <label className="flex items-center gap-2 text-[10px] text-slate-400">
          <input type="checkbox" checked={confirm} onChange={e => setConfirm(e.target.checked)} />
          This is the Owner's own direction.
        </label>
        <button type="button" onClick={save} disabled={!confirm || rows.every(r => !r.id.trim())}
          data-testid="protected-entities-save"
          className="px-3 py-2 rounded-lg text-[10px] font-black uppercase tracking-widest bg-aura/20 text-aura border border-aura/40 disabled:opacity-40">
          Name these as protected
        </button>
      </div>
    </div>
  );
};

export default ProtectedEntitiesPanel;
