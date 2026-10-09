import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * FU-467 (P3.23) — A.8's transparent donor view. What came in, by channel, read from the entity's own books;
 * and what its waterfall WOULD allocate, which is NOT a distribution and is labelled so. A silent template
 * fallback and untagged postings are shown, not hidden.
 */
export const QepDonorStatement: React.FC = () => {
  const [ids, setIds] = useState<string[]>([]);
  const [sel, setSel] = useState('');
  const [st, setSt] = useState<Dict | null>(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    apiJson<Dict>('/api/v1/economy/living-vsbs')
      .then(r => {
        const q = (r.living_vsbs || []).filter((v: Dict) => v.entity_type === 'qep_waqf_trust').map((v: Dict) => String(v.vsb_id));
        setIds(q); if (q.length) setSel(q[0]);
      })
      .catch(e => setErr(`The roster could not be read: ${String(e?.message ?? e)}`));
  }, []);
  useEffect(() => {
    if (!sel) { setSt(null); return; }
    apiJson<Dict>(`/api/v1/qep/contribute/statement/${sel}`).then(r => { setSt(r); setErr(''); })
      .catch(e => { setSt(null); setErr(`No statement: ${String(e?.message ?? e)}`); });
  }, [sel]);

  return (
    <div className="space-y-2 text-[11px]" data-testid="qep-donor-statement">
      <h3 className="text-sm font-black text-white uppercase tracking-wide">Donor statement</h3>
      {ids.length === 0 && <p className="text-slate-500">No QEP entity is on the living roster, so there is no statement to show.</p>}
      {ids.length > 1 && (
        <select value={sel} onChange={e => setSel(e.target.value)} className="bg-slate-950 border border-slate-800 rounded px-2 py-1">
          {ids.map(i => <option key={i} value={i}>{i}</option>)}
        </select>
      )}
      {err && <p className="text-vital">{err}</p>}
      {st && (
        <>
          <p className="text-slate-200" data-testid="qep-contributions">
            Received: {String(st.contributions_total_wst)} WST in {String(st.contributions_count)} contribution(s) ·{' '}
            {Object.entries(st.contributions_by_channel_wst || {}).map(([k, v]) => `${k} ${String(v)}`).join(' · ') || 'no channel recorded'}
          </p>
          <p className="text-amber-300" data-testid="qep-would-allocate">
            WOULD allocate (the waterfall's split of that total, NOT a distribution):{' '}
            {Object.entries(st.would_allocate_wst || {}).map(([k, v]) => `${k} ${String(v)}`).join(' · ')}
          </p>
          <p className="text-[10px] text-slate-500">{String(st.allocation_basis ?? '')}</p>
          {st.template_is_a_fallback && <p className="text-[10px] text-vital" data-testid="qep-template-fallback">The waterfall shown is a FALLBACK template: {String(st.template_basis ?? '')}</p>}
          {Number(st.untagged_postings || 0) > 0 && <p className="text-[10px] text-amber-400" data-testid="qep-untagged">{String(st.untagged_postings)} posting(s) carry no channel tag and are not counted by channel.</p>}
        </>
      )}
    </div>
  );
};

export default QepDonorStatement;
