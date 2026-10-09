import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * P3.23 (FU-278) — the legal specialist's surface. The clerk ASSEMBLES from the one named folder: every
 * particular shows the document and line it came from, or is a BLANK; every authority is resolved or REFUSED;
 * the checks that did not resolve are listed HERE, on the page, not only in a log; and the not-legal-advice
 * statement is shown where the work is read.
 */
export const MatterAssemblyPanel: React.FC = () => {
  const [bundle, setBundle] = useState<Dict | null>(null);
  const [particular, setParticular] = useState('');
  const [words, setWords] = useState('');
  const [authority, setAuthority] = useState('');
  const [art, setArt] = useState<Dict | null>(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    apiJson<Dict>('/api/v1/law/bundle').then(setBundle).catch(e => setErr(`The matter folder could not be read: ${String(e?.message ?? e)}`));
  }, []);

  const assemble = async () => {
    try {
      const body = {
        template_id: 'et1_claim',
        particulars: particular.trim() ? [{ name: particular.trim(), words: words.split(',').map(w => w.trim()).filter(Boolean) }] : [],
        authorities: authority.trim() ? [authority.trim()] : [],
      };
      setArt(await apiJson<Dict>('/api/v1/law/matter/assemble', { method: 'POST', body }));
      setErr('');
    } catch (e: any) { setErr(`Not assembled: ${String(e?.message ?? e)}`); }
  };

  return (
    <div className="space-y-3" data-testid="matter-assembly-panel">
      <h3 className="text-sm font-black text-white uppercase tracking-wide">Matter bundle: assemble with provenance</h3>
      <p className="text-[11px] text-amber-300/90 font-bold" data-testid="matter-not-legal-advice">
        {art?.not_legal_advice ?? 'Nothing here is legal advice. This platform assembles and cites as a clerk would; it is never counsel, and it never forecasts an outcome.'}
      </p>
      {bundle && (
        <p className="text-[10px] text-slate-500 leading-relaxed" data-testid="matter-bundle-state">
          Folder: {String(bundle.folder_state)} · {bundle.document_count === null || bundle.document_count === undefined ? 'no documents can be counted' : `${bundle.document_count} document(s)`} · {String(bundle.bundle_indexing_basis ?? '')}
        </p>
      )}
      {err && <p className="text-[10px] text-vital">{err}</p>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
        <input value={particular} onChange={e => setParticular(e.target.value)} placeholder="particular, e.g. date of dismissal"
          className="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-[11px] text-slate-200" />
        <input value={words} onChange={e => setWords(e.target.value)} placeholder="words to find, comma-separated"
          className="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-[11px] text-slate-200" />
        <input value={authority} onChange={e => setAuthority(e.target.value)} placeholder="an authority, e.g. Equality Act 2010"
          className="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-[11px] text-slate-200" />
      </div>
      <button type="button" onClick={assemble} className="px-3 py-1 rounded bg-slate-800 text-[10px] text-white">Assemble draft</button>
      {art && (
        <div className="space-y-2 text-[11px]" data-testid="matter-artefact">
          <p className="text-slate-300 font-bold">{String(art.status)} · {String(art.face)}</p>
          <ul className="space-y-1" data-testid="matter-particulars">
            {(art.particulars || []).map((p: Dict, i: number) => (
              <li key={i} className={p.found ? 'text-slate-200' : 'text-amber-300'}>
                {String(p.particular)}: {String(p.rendered)}{p.found ? ` — ${String(p.document)}:${String(p.line)} (${String(p.verification?.verdict)})` : ''}
              </li>
            ))}
          </ul>
          <ul className="space-y-1" data-testid="matter-authorities">
            {(art.authorities || []).map((a: Dict, i: number) => (
              <li key={i} className={a.resolved ? 'text-slate-300' : 'text-vital'}>{String(a.authority)}: {a.resolved ? 'resolved' : 'REFUSED'} — {String(a.basis)}</li>
            ))}
          </ul>
          <p className="text-[10px] text-vital" data-testid="matter-unresolved-checks">
            {(art.unresolved_checks || []).length === 0 && (art.authorities_refused || []).length === 0
              ? 'No unresolved check.'
              : `Unresolved: ${[...(art.unresolved_checks || []).map((x: string) => `${x} (located line failed re-verification)`), ...(art.authorities_refused || []).map((x: string) => `${x} (authority refused)`)].join('; ')}`}
          </p>
          {art.filing_shaped && <p className="text-[10px] text-amber-400">Filing-shaped: this stays a draft until the Owner records an approval.</p>}
        </div>
      )}
    </div>
  );
};

export default MatterAssemblyPanel;
