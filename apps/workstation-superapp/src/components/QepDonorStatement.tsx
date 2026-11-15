import React, { useEffect, useState } from 'react';
import { errorMessage } from '../lib/api';   // W1015 - a caught failure, said as what it was
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * FU-467 (P3.23) — A.8's transparent donor view. What came in, by channel, read from the entity's own books;
 * and what its waterfall WOULD allocate, which is NOT a distribution and is labelled so. A silent template
 * fallback and untagged postings are shown, not hidden.
 */
export const QepDonorStatement: React.FC = () => {
  //  W1070 - the QEP entities, by id and name, and null until the roster's read answers: an unread roster was said
  //  as one with no QEP entity on it
  const [ids, setIds] = useState<{ id: string; name: string }[] | null>(null);
  const [rosterErr, setRosterErr] = useState('');
  const [sel, setSel] = useState('');
  const [st, setSt] = useState<Dict | null>(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    apiJson<Dict>('/api/v1/economy/living-vsbs')
      .then(r => {
        const q = (r.living_vsbs || []).filter((v: Dict) => v.entity_type === 'qep_waqf_trust')
          .map((v: Dict) => ({ id: String(v.vsb_id), name: String(v.name || v.vsb_id) }));
        setIds(q); if (q.length) setSel(q[0].id);
      })
      .catch(e => setRosterErr(`The living roster could not be read: ${errorMessage(e)}`));
  }, []);
  useEffect(() => {
    if (!sel) { setSt(null); return; }
    //  W1070 - a statement is said only under the entity it was read for: one that answers after another entity
    //  was chosen is dropped
    let live = true;
    setSt(null); setErr('');
    apiJson<Dict>(`/api/v1/qep/contribute/statement/${sel}`).then(r => { if (live) { setSt(r); setErr(''); } })
      .catch(e => { if (live) { setSt(null); setErr(`No statement: ${errorMessage(e)}`); } });
    return () => { live = false; };
  }, [sel]);

  return (
    <div className="space-y-2 text-[11px]" data-testid="qep-donor-statement">
      <h3 className="text-sm font-black text-white uppercase tracking-wide">Donor statement</h3>
      {rosterErr && <p role="alert" className="text-vital" data-testid="qep-roster-unread">{rosterErr}</p>}
      {!rosterErr && ids === null && <p className="text-slate-500">Reading the living roster…</p>}
      {ids && ids.length === 0 && <p className="text-slate-500">No QEP entity is on the living roster, so there is no statement to show.</p>}
      {ids && ids.length > 1 && (
        <select aria-label="QEP entity" value={sel} onChange={e => setSel(e.target.value)} className="bg-slate-950 border border-slate-800 rounded px-2 py-1">
          {ids.map(i => <option key={i.id} value={i.id}>{i.name} ({i.id})</option>)}
        </select>
      )}
      {ids && ids.length === 1 && <p className="text-slate-300" data-testid="qep-statement-entity">{ids[0].name} ({ids[0].id})</p>}
      {err && <p className="text-vital">{err}</p>}
      {sel && !st && !err && <p className="text-slate-500">Reading the statement…</p>}
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
          {Number(st.untagged_postings?.count || 0) > 0 && <p className="text-[10px] text-amber-400" data-testid="qep-untagged">{String(st.untagged_postings.count)} posting(s), {String(st.untagged_postings.total_wst)} WST in all, carry no channel tag and are not counted by channel.</p>}
        </>
      )}
    </div>
  );
};

export default QepDonorStatement;
