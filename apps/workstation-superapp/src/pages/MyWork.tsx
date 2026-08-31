import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import { Copy, Download, Trash2, Check, FolderOpen, Clock, Sparkles } from 'lucide-react';
import {
  listOutputs, removeOutput, clearOutputs, clearWorkspaceEverywhere,
  syncWorkspaceFromServer, lastSyncError, type OutputRecord,
} from '../lib/outputHistory';
import { getToken } from '../lib/auth';

// §9 — "My Work": revisit the outputs you've generated (domain tools + journeys).
//
// Storage is two-tier (see lib/outputHistory.ts): signed in → the server-side per-user workspace,
// which follows the user across devices; auth off → localStorage only. This page used to read
// localStorage ONLY and describe itself as local-only regardless — so a signed-in user opening it on
// a second device saw an empty page while their work sat on the server, and was told, wrongly, that
// nothing had ever been stored server-side. It now pulls the workspace on mount, describes the tier
// actually in play, and clears BOTH tiers when the user clears.
export const MyWork: React.FC = () => {
  const navigate = useNavigate();
  const [records, setRecords] = useState<OutputRecord[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncError, setSyncError] = useState('');

  const signedIn = (() => { try { return !!getToken(); } catch { return false; } })();

  const refresh = () => setRecords(listOutputs());
  useEffect(() => {
    let cancelled = false;
    refresh();
    // Pull the server-side workspace before rendering a verdict about what the user has. Without
    // this the page reports "no saved outputs" for work that exists.
    if (signedIn) {
      setSyncing(true);
      syncWorkspaceFromServer()
        .then(() => { if (!cancelled) { refresh(); setSyncError(lastSyncError()); } })
        .catch(() => { if (!cancelled) setSyncError(lastSyncError() || 'Could not reach your workspace.'); })
        .finally(() => { if (!cancelled) setSyncing(false); });
    }
    const h = () => refresh();
    window.addEventListener('ws:output-history', h);
    return () => { cancelled = true; window.removeEventListener('ws:output-history', h); };
  }, [signedIn]);

  const clearAll = async () => {
    // Clearing must reach the tier the work actually lives in, or it comes back on the next sync.
    if (signedIn) {
      try { await clearWorkspaceEverywhere(); } catch { setSyncError(lastSyncError() || 'Could not clear your server workspace.'); }
    } else {
      clearOutputs();
    }
    refresh();
  };

  const copy = async (rec: OutputRecord) => {
    try { await navigator.clipboard.writeText(rec.output); setCopiedId(rec.id); setTimeout(() => setCopiedId(null), 1500); } catch { /* ignore */ }
  };
  const download = (rec: OutputRecord) => {
    const slug = rec.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'output';
    const blob = new Blob([rec.output], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${slug}.md`;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 pb-16">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-4">
        <div>
          <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2">Workstation IDBO · Your History</p>
          <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">My Work</h1>
          <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
            The outputs you&rsquo;ve generated — revisit, copy, download or remove them.{' '}
            {signedIn
              ? 'Saved to your account workspace on the server, so they follow you across devices and browsers.'
              : 'Saved locally in this browser (not on a server), so nothing is lost on navigation.'}
          </p>
          {syncing && (
            <p className="text-[10px] font-bold text-slate-600 mt-1">Checking your workspace…</p>
          )}
          {syncError && (
            <p role="alert" className="text-[10px] font-bold text-vital mt-1">
              Workspace sync failed — showing what is stored in this browser. {syncError}
            </p>
          )}
        </div>
        {records.length > 0 && (
          <Button type="button" onClick={clearAll}
            variant="outline" className="text-[10px] border-slate-800 text-slate-400 shrink-0">
            <Trash2 size={14} /> Clear all
          </Button>
        )}
      </header>

      {/* Do not assert "nothing saved" while the workspace pull is still in flight — that verdict
          was wrong for every signed-in user on a device that had not synced yet. */}
      {records.length === 0 && syncing ? (
        <Card className="p-10 text-center border-dashed border-slate-800">
          <Clock size={28} className="mx-auto text-slate-700 mb-3" />
          <p className="text-slate-500 font-black uppercase tracking-widest text-xs">Loading your workspace…</p>
        </Card>
      ) : records.length === 0 ? (
        <Card className="p-12 text-center border-dashed border-slate-800">
          <FolderOpen className="mx-auto text-slate-700 mb-4" size={44} />
          <p className="text-slate-500 font-black uppercase tracking-widest text-xs mb-2">No saved outputs yet</p>
          <p className="text-slate-600 text-xs max-w-md mx-auto mb-6">
            Run a domain tool or a Genesis journey, and your results will appear here automatically.
          </p>
          <div className="flex items-center justify-center gap-3 flex-wrap">
            <Button type="button" onClick={() => navigate('/domains')} className="bg-aura text-sovereign text-xs"><Sparkles size={14} /> Open Domains</Button>
            <Button type="button" onClick={() => navigate('/genesis')} variant="outline" className="text-xs border-slate-800 text-slate-300">Start a Genesis</Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {records.map(rec => {
            const open = openId === rec.id;
            return (
              <Card key={rec.id} className="p-5">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <button type="button" onClick={() => setOpenId(open ? null : rec.id)} className="flex items-center gap-3 min-w-0 text-left flex-1">
                    <div className="w-9 h-9 rounded-xl bg-aura/10 flex items-center justify-center shrink-0"><Sparkles size={15} className="text-aura" /></div>
                    <div className="min-w-0">
                      <p className="font-black text-white text-sm truncate">{rec.title}</p>
                      <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 flex items-center gap-2 mt-0.5">
                        <Clock size={9} /> {new Date(rec.ts).toLocaleString()}
                        {rec.domain ? <span className="text-slate-500">· {rec.domain}</span> : null}
                        {rec.provenance ? <span className={rec.provenance.is_external ? 'text-amber-400' : 'text-emerald-400'}>· {rec.provenance.is_external ? `via ${rec.provenance.served_by}` : 'in-house'}</span> : null}
                        {/* W337 — refinement history is visible: the latest text IS the record; priors kept */}
                        {(rec.refineCount ?? 0) > 0 ? <span className="text-aura">· v{(rec.refineCount ?? 0) + 1} ({rec.versions?.length ?? 0} prior kept)</span> : null}
                      </p>
                    </div>
                  </button>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <button type="button" onClick={() => copy(rec)} aria-label="Copy" className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1">
                      {copiedId === rec.id ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />}
                    </button>
                    <button type="button" onClick={() => download(rec)} aria-label="Download" className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1"><Download size={11} /></button>
                    {/* W303 - any saved work can become a venture: the bridge carries the OUTPUT */}
                    <button type="button" aria-label="Commercialise via Genesis" onClick={() => { const sid = `seed_${Date.now().toString(36)}`; try { sessionStorage.setItem(`ws_genesis_${sid}`, JSON.stringify({ title: rec.title, domain: rec.domain, input: rec.input || rec.title, output: rec.output })); } catch { /* best-effort */ } navigate(`/genesis?seed=${sid}${rec.domain ? `&domain=${encodeURIComponent(rec.domain)}` : ""}`); }} className="text-[8px] font-black uppercase px-2 py-1 rounded bg-highlight/15 text-highlight hover:bg-highlight/25 flex items-center gap-1"><Sparkles size={11} /> Venture</button>
                    <button type="button" onClick={() => { removeOutput(rec.id); refresh(); }} aria-label="Remove" className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-400 hover:text-vital flex items-center gap-1"><Trash2 size={11} /></button>
                  </div>
                </div>
                {rec.input && (
                  <p className="text-[10px] text-slate-600 italic mt-3 line-clamp-2">Asked: {rec.input}</p>
                )}
                {open && (
                  <>
                    <pre className="mt-3 text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 border border-slate-900 rounded-xl p-4 max-h-[420px] overflow-y-auto">
                      {rec.output}
                    </pre>
                    {/* §9 (W-versions) — the prior refinement versions were STORED but unviewable;
                        each is now readable + copyable (newest prior first). */}
                    {(rec.versions?.length ?? 0) > 0 && (
                      <div className="mt-2 space-y-1.5">
                        <p className="text-[8px] font-black uppercase tracking-widest text-slate-600">Prior versions ({rec.versions!.length})</p>
                        {rec.versions!.slice().reverse().map((v, i) => {
                          const label = `${rec.id}-v${rec.versions!.length - 1 - i}`;
                          const vopen = openId === label;
                          return (
                            <div key={label} className="border border-slate-900 rounded-lg">
                              <div className="flex items-center justify-between px-3 py-1.5">
                                <button type="button" onClick={() => setOpenId(vopen ? rec.id : label)}
                                  className="text-[9px] font-black uppercase text-slate-400 hover:text-aura">
                                  v{rec.versions!.length - 1 - i} · {new Date(v.refinedAt).toLocaleString()}
                                </button>
                                <button type="button" aria-label="Copy this version"
                                  onClick={() => { try { navigator.clipboard.writeText(v.output); } catch { /* clipboard unavailable */ } }}
                                  className="text-[8px] font-black uppercase text-slate-500 hover:text-aura">Copy</button>
                              </div>
                              {vopen && (
                                <pre className="text-[10px] text-slate-400 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 rounded-b-lg p-3 max-h-[300px] overflow-y-auto">{v.output}</pre>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </>
                )}
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
