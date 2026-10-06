import React, { useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * FU-462 (P3.23) — a SEARCH over the owned index, on a page. Located passages show their document and line;
 * a passage that exists but cannot be cited says so (not_citable, citation_basis); files the search could not
 * look inside are named. Lexical only: no embeddings are installed, and the result says what it searched.
 */
export const ArchiveSearchPanel: React.FC = () => {
  const [term, setTerm] = useState('');
  const [res, setRes] = useState<Dict | null>(null);
  const [err, setErr] = useState('');
  const run = async () => {
    try { setRes(await apiJson<Dict>(`/api/v1/horizon/archive/search?term=${encodeURIComponent(term)}`)); setErr(''); }
    catch (e: any) { setRes(null); setErr(`Search failed: ${String(e?.message ?? e)}`); }
  };
  return (
    <div className="space-y-2 text-[11px]" data-testid="archive-search-panel">
      <div className="flex gap-2">
        <input value={term} onChange={e => setTerm(e.target.value)} placeholder="search the indexed files (exact words)"
          className="flex-1 bg-slate-950 border border-slate-800 rounded px-2 py-1 text-slate-200" />
        <button type="button" disabled={!term.trim()} onClick={run} className="px-3 py-1 rounded bg-slate-800 text-white disabled:opacity-40">Search</button>
      </div>
      {err && <p className="text-vital">{err}</p>}
      {res && (
        <>
          <p className="text-slate-400" data-testid="archive-search-counts">
            {String(res.passages_matched ?? 0)} passage(s) matched · {String(res.shown_files ?? 0)} of {String(res.matched_files ?? 0)} file(s) shown · {String(res.file_hits_basis ?? '')}
          </p>
          <ul className="space-y-1" data-testid="archive-search-passages">
            {(res.passages || []).map((p: Dict, i: number) => (
              <li key={i} className="text-slate-300">{String(p.path)}:{String(p.line)} — {String(p.text ?? '')}</li>
            ))}
          </ul>
          <p className="text-[10px] text-slate-500" data-testid="archive-search-citation-basis">{String(res.citation_basis ?? '')}</p>
          {(res.not_citable || []).length > 0 && (
            <ul className="text-amber-300 space-y-1" data-testid="archive-search-not-citable">
              {(res.not_citable || []).map((n: Dict, i: number) => <li key={i}>NOT CITABLE: {String(n.path)} — {String(n.why)}</li>)}
            </ul>
          )}
          {(res.not_searched || []).length > 0 && (
            <p className="text-[10px] text-slate-500" data-testid="archive-search-not-searched">Not searched (not read into the index): {(res.not_searched || []).join(', ')}</p>
          )}
        </>
      )}
    </div>
  );
};

export default ArchiveSearchPanel;
