import React, { useState, useEffect } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { useNavigate } from 'react-router-dom';
import { Shield, Sparkles, FileText, Send, History, CheckCircle2, AlertTriangle, Search, Activity, Zap, TrendingUp, Clock, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const ConstitutionalUI: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'articles' | 'timeline' | 'history'>('articles');
  const [search, setSearch] = useState('');
  const [articles, setArticles] = useState<any[]>([]);
  // W495 (FU-126, S10.3) - the endpoint's own report: whether a canon is present, why not, and what
  // governs in its place. A missing canon is a state, not an occasion to show one invented article.
  const [summary, setSummary] = useState<{ breach?: string[]; noMechanism?: string[]; note?: string }>({});
  const [canon, setCanon] = useState<{ canon_present?: boolean; canon_basis?: string;
    what_governs_instead?: string[]; categories_available?: string[] } | null>(null);
  const [gaas, setGaas] = useState<any>(null);
  const [ueg, setUeg] = useState<any[]>([]);
  // W491 — the chain's real size, so the badge can say what its 40 rows are 40 *of*
  const [uegTotal, setUegTotal] = useState<number | null>(null);
  // W491 (refutation) - the chain's own "I could not be read whole" signal was fetched and thrown away,
  // so an unreadable ledger rendered as "No constitutional events logged yet" - the opposite claim.
  const [uegUnreadable, setUegUnreadable] = useState<string | null>(null);
  const [integrity, setIntegrity] = useState<{
    valid: boolean; events: number | null; root_hash: string | null;
    outcome?: string; reason?: string | null; anchor_checked?: boolean; verified_basis?: string;
  } | null>(null);

  useEffect(() => {
    // W495 (FU-126, S10.3) - the comment said "all 1127 articles" and the endpoint returned ONE
    // fabricated article whenever the canon file was absent, which it is: a cleanup moved it to the
    // archive, and the archived copy is the inherited Jules-era document, excluded as dated. The
    // endpoint now reports canon_present:false with a basis and names what governs instead; the page
    // shows that rather than presenting an invented article as the constitution.
    fetch('/api/v1/gaas/ueg/verify').then(r => r.json()).then(setIntegrity).catch(() => setIntegrity(null));
    fetch('/api/v154/constitution/articles')
      .then(res => res.json())
      .then(data => {
        // the endpoint used to return a bare array; it now returns an object carrying the basis
        if (Array.isArray(data)) { setArticles(data); setCanon(null); return; }
        setArticles(Array.isArray(data?.articles) ? data.articles : []);
        setSummary({ breach: data?.articles_recording_a_breach ?? [],
                     noMechanism: data?.articles_naming_no_mechanism ?? [],
                     note: data?.verification_note });
        setCanon(data ?? null);
      })
      .catch(() => { setArticles([]); setCanon(null); });
  }, []);

  // Live GaaS v5 constitutional engine (v16-Omega interceptor + UEG audit log)
  const refreshGaas = () => {
    // W460 — a failing poll clears the verdict (a stale green NOMINAL used to outlive the backend)
    fetch('/api/v1/gaas/status').then(r => (r.ok ? r.json() : null)).then(setGaas).catch(() => setGaas(null));
    // W491 (sweep S10.14, C10) — the badge counted these 40 fetched rows and read as the trail's
    // total, freezing at 40 however large the chain grew (the same page showed 177+ elsewhere). The
    // response already carries summary.total_events and this threw it away.
    fetch('/api/v1/gaas/ueg/events?limit=40').then(r => r.json())
      .then(d => {
        setUeg(Array.isArray(d?.events) ? [...d.events].reverse() : []);
        setUegTotal(typeof d?.summary?.total_events === 'number' ? d.summary.total_events : null);
        setUegUnreadable(d?.summary?.unreadable ? String(d.summary.unreadable) : null);
      }).catch(() => {});
  };
  useEffect(() => {
    refreshGaas();
    const t = setInterval(refreshGaas, 15000);
    return () => clearInterval(t);
  }, []);

  const timeline = [
    { id: 'ev-1', title: 'Illustrative example (demo — not a real event)', type: 'DEMO', rationale: 'W314: fabricated self-ratified articles removed; real changes appear via Change Control.', time: '—' },
    
  ];

  const filtered = articles.filter(a =>
    a?.title?.toLowerCase().includes(search.toLowerCase()) ||
    a?.category?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Constitutional Core</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Self-Modification Engine • Universal Governance • Phase 4</p>
        </div>
        <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800 flex-wrap shrink-0">
           {['articles', 'timeline', 'history'].map((tab) => (
             <button
               key={tab}
               onClick={() => setActiveTab(tab as any)}
               className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === tab ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
             >
               {tab}
             </button>
           ))}
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <aside className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-4 text-aura">
                  <Shield size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Adaptation Engine</h4>
               </div>
               <p className="text-sm text-slate-400 font-bold leading-relaxed">
                  LOW-tier changes are auto-approved by Change Control when organism health is at least 0.6 and the immune
                  threat is NOMINAL or ELEVATED; the immune system's defensive levers are auto-approved only when an admin
                  runs the immune reconfigure action (nothing triggers it automatically); other changes are reviewed there,
                  and a CRITICAL one is decided only by an explicit admin decision.
               </p>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  {/* W411 — "Trust Score 0.96 (SOVEREIGN)" with a fixed w-[96%] bar used to be here.
                      Nothing computes trust, and a filled bar is a strong visual claim of a
                      measurement. There IS a real integrity signal for a governance page — the UEG
                      hash chain — so it is shown instead: verified or not, over a real event count. */}
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Ledger integrity</span>
                     <span className={!integrity ? "text-slate-500"
                       : integrity.outcome === 'unreadable' ? "text-amber-400"
                       : integrity.valid ? (integrity.anchor_checked ? "text-aura" : "text-amber-400")
                       : "text-vital"}>
                        {/* W492 (FU-196) - "TAMPER DETECTED" was shown for an UNREADABLE ledger,
                             where nothing was checked at all, and "VERIFIED" was shown when the tail
                             anchor was missing or corrupt, so truncation was never ruled out. */}
                        <span data-testid="ledger-integrity-verdict" title={integrity?.verified_basis}>
                        {integrity === null ? "—"
                          : integrity.outcome === 'unreadable' ? "NOT ASSESSED — LEDGER UNREADABLE"
                          : integrity.valid ? (integrity.anchor_checked ? "VERIFIED"
                                               : "HASHES VERIFIED — TRUNCATION NOT RULED OUT")
                          : "TAMPER DETECTED"}
                        </span>
                     </span>
                  </div>
                  {/* W492 (FU-196) - for an unreadable ledger there is no count and no root hash; this
                      printed String(undefined) as one. No figure is claimed for books not read. */}
                  {integrity && (
                     <p className="text-[9px] font-bold text-slate-600" data-testid="ledger-integrity-figures">
                        {/* W492 (refutation) - "the ledger was not read" was shown for a hash mismatch
                            too, where the ledger WAS read and a stored hash disagreed. Only the
                            unreadable outcome means it could not be read. */}
                        {typeof integrity.events === 'number' && integrity.root_hash
                          ? `${integrity.events.toLocaleString()} events · root ${String(integrity.root_hash).slice(0, 12)}…`
                          : integrity.outcome === 'unreadable'
                          ? 'no event count or root hash — the ledger was not read'
                          : 'no event count or root hash was reported for this outcome'}
                     </p>
                  )}
               </div>
               <Button type="button" onClick={() => navigate('/change-control')} className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-aura/20">
                  <Sparkles size={18} /> Propose Amendment
               </Button>
            </Card>

            {/* Live GaaS v5 constitutional engine */}
            <Card className="p-8 space-y-5 border-slate-800">
               <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-aura">
                     <Terminal size={18} />
                     <h4 className="text-[11px] font-black uppercase tracking-widest">Constitutional Engine</h4>
                  </div>
                  {/* W460 — the green verdict used to show even when the status call never answered.
                      W494 (FU-141) — and the verdict describes ONE route's breaker, not the engine: the
                      badge names the node it read rather than implying a platform-wide state. */}
                  <Badge color={!gaas?.circuit_breaker ? 'slate' : gaas.circuit_breaker.tripped ? 'vital' : 'slate'}
                         title={gaas?.circuit_breaker_scope} data-testid="gaas-breaker-badge">
                     {!gaas?.circuit_breaker ? 'UNAVAILABLE'
                       : gaas.circuit_breaker.tripped ? 'BREAKER OPEN'
                       : `${gaas.circuit_breaker_node ?? 'node'} BREAKER CLOSED`}
                  </Badge>
               </div>
               <p className="text-[9px] font-mono text-slate-600">{gaas?.interceptor ?? '—'}</p>
               {/* W494 (FU-141) — the three figures below are this ONE interceptor's; every other governed
                   path builds its own per call and nothing aggregates them. Said, not left to a hover. */}
               {gaas?.circuit_breaker_scope && (
                 <p className="text-[9px] text-amber-400/80 leading-relaxed" data-testid="gaas-breaker-scope">
                   These figures cover {gaas.circuit_breaker_scope}
                 </p>
               )}
               <div className="space-y-3">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Breaker Threshold</span>
                     <span className="text-white">{gaas?.circuit_breaker?.threshold ?? '—'}</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Error Rate</span>
                     <span className="text-white">{gaas?.circuit_breaker?.error_rate ?? '—'}</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>UEG Events</span>
                     <span className={gaas?.ueg ? 'text-aura' : 'text-slate-500'}>{gaas?.ueg?.total_events ?? '—'}</span>
                  </div>
               </div>
               {gaas?.ueg?.root_hash && (
                  <p className="text-[8px] font-mono text-slate-700 break-all pt-2 border-t border-slate-900">
                     root: {String(gaas.ueg.root_hash).slice(0, 32)}…
                  </p>
               )}
            </Card>

            <Card className="p-10 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Filter Codex</h4>
               <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-900">
                  <Search size={18} className="text-slate-700" />
                  <input
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    placeholder="Search by Title, Category..."
                    className="bg-transparent border-none outline-none text-xs text-white font-bold w-full"
                  />
               </div>
               {/* W495 (FU-126, S10.3) - the four chips were hard-coded and three of them matched
                   nothing; the parser assigns every article the CORE category. Driven by what was
                   actually parsed, so a chip exists only if something carries it. */}
               {canon && canon.canon_present === false && (
                 <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30" data-testid="canon-absent">
                   <p className="text-[10px] font-black uppercase tracking-widest text-amber-400">
                     No constitution document is present
                   </p>
                   <p className="text-[10px] text-amber-400/80 mt-1 leading-relaxed">{canon.canon_basis}</p>
                   {!!canon.what_governs_instead?.length && (
                     <>
                       <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mt-2">What governs instead</p>
                       <ul className="mt-1 space-y-0.5">
                         {canon.what_governs_instead.map(w => (
                           <li key={w} className="text-[9px] text-slate-400">{w}</li>
                         ))}
                       </ul>
                     </>
                   )}
                 </div>
               )}
               <div className="flex flex-wrap gap-2">
                  {(canon?.categories_available?.length
                     ? canon.categories_available
                     : Array.from(new Set(articles.map(a => a.category).filter(Boolean)))).map(cat => (
                    <button type="button" key={cat} onClick={() => setSearch(cat)} className="px-3 py-1 rounded-lg bg-slate-900 text-[8px] font-black text-slate-500 hover:text-aura transition-all">{cat}</button>
                  ))}
               </div>
            </Card>
         </aside>

         <main className="@[440px]:col-span-8">
            <AnimatePresence mode="wait">
               {activeTab === 'articles' && (
                 <motion.div key="articles" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
                    {/* W515 (FU-295) - Article 33 says this document names its own unmet articles, so a
                        reader must see that without diffing every card. A zero here is stated as a zero, never
                        as compliance: when no canon is present these lists are empty for that reason. */}
                    {articles.length > 0 && (
                      <div className="mb-8 p-6 rounded-3xl bg-slate-950/60 border border-slate-900 text-[11px] font-bold">
                        <span className="text-slate-400">{articles.length} articles · </span>
                        {(summary.breach?.length ?? 0) > 0 ? (
                          <span className="text-vital">{summary.breach!.length} record their own breach (Art. {summary.breach!.join(', ')})</span>
                        ) : (
                          <span className="text-slate-500">none records a breach</span>
                        )}
                        {(summary.noMechanism?.length ?? 0) > 0 && (
                          <span className="text-amber-500/80"> · {summary.noMechanism!.length} name no verification mechanism (Art. {summary.noMechanism!.join(', ')})</span>
                        )}
                        {summary.note && <span className="block mt-2 text-slate-600 font-medium">{summary.note}</span>}
                      </div>
                    )}
                    {filtered.map((art, i) => (
                      <div key={art.id} className="p-10 rounded-[2.5rem] bg-slate-950/80 border border-slate-900 group hover:border-aura/30 transition-all">
                         <div className="flex justify-between items-center mb-6">
                            <div className="flex items-center gap-4">
                               <div className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-black text-aura uppercase">Article {art.id}</div>
                               <Badge color={art.category === 'COSMIC' ? 'highlight' : 'aura'}>{art.category}</Badge>
                            </div>
                         </div>
                         <h3 className="text-3xl font-black mb-4 text-white uppercase tracking-tight">{art.title}</h3>
                         <p className="text-lg text-slate-400 font-bold leading-relaxed">{art.content}</p>
                         {/* W515 (FU-295) - an article without its verification mechanism cannot be audited,
                             and a governance page that lists rules without them is the defect the document
                             exists to remove. `verified` is null (never an empty string) when the document
                             names no mechanism, and that case is labelled rather than left blank. */}
                         {art.verified ? (
                           <p className="mt-6 text-[11px] font-bold text-slate-500 leading-relaxed">
                             <span className="text-aura uppercase tracking-widest">Verified by </span>{art.verified}
                           </p>
                         ) : (
                           <p className="mt-6 text-[11px] font-bold text-amber-500/80 leading-relaxed">
                             This article names no verification mechanism — it is a statement, not a checkable rule.
                           </p>
                         )}
                         {art.unmet && (
                           <p className="mt-3 text-[11px] font-black text-vital leading-relaxed">
                             <span className="uppercase tracking-widest">Unmet — </span>
                             {art.unmet_reason || 'this article records its own breach and states no reason'}
                           </p>
                         )}
                      </div>
                    ))}
                 </motion.div>
               )}

               {activeTab === 'timeline' && (
                 <motion.div key="timeline" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
                    <Card className="p-10">
                       <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4 mb-10">
                          <Clock size={24} className="text-aura" />
                          Evolution Timeline
                       </h3>
                       <div className="space-y-8 relative before:absolute before:left-7 before:top-2 before:bottom-2 before:w-px before:bg-slate-800">
                          {timeline.map((ev, i) => (
                            <div key={ev.id} className="relative pl-20">
                               <div className="absolute left-4 top-1 w-6 h-6 rounded-full bg-slate-950 border-2 border-aura flex items-center justify-center z-10">
                                  <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                               </div>
                               <div className="p-8 rounded-[2.5rem] bg-slate-900/50 border border-slate-800 group hover:border-aura/30 transition-all">
                                  <div className="flex justify-between items-start mb-4">
                                     <div>
                                        <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{ev.title}</p>
                                        <Badge color="aura">{ev.type}</Badge>
                                     </div>
                                     <span className="text-[10px] font-black text-slate-600 uppercase">{ev.time}</span>
                                  </div>
                                  <p className="text-sm text-slate-400 font-bold leading-relaxed">{ev.rationale}</p>
                               </div>
                            </div>
                          ))}
                       </div>
                    </Card>
                 </motion.div>
               )}

               {activeTab === 'history' && (
                 <motion.div key="history" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                    <Card className="p-10">
                       <div className="flex justify-between items-center mb-8">
                          <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                             <History size={24} className="text-aura" />
                             UEG Audit Trail
                          </h3>
                          {/* W491 — says what it covers; an unreadable chain shows —, never 0 */}
                          <Badge color="aura"><span data-testid="ueg-trail-count">latest {ueg.length} of {uegTotal ?? '—'} events</span></Badge>
                       </div>
                       {uegUnreadable ? (
                          <p className="text-sm text-amber-400 font-bold" data-testid="ueg-unreadable">
                             The constitutional ledger could not be read whole ({uegUnreadable}), so no events are
                             shown and no count is claimed. This is not the same as no events having been logged.
                          </p>
                       ) : ueg.length === 0 ? (
                          <p className="text-sm text-slate-500 font-bold">No constitutional events logged yet. Actions routed through the engine appear here.</p>
                       ) : (
                          <div className="space-y-3">
                             {ueg.map((node: any) => {
                               const d = node?.data ?? {};
                               const kind = d.type ?? 'event';
                               // W505 (FU-032) — read the backend's CLASSIFICATION instead of naming two event
                               // types. Keying the tone to 'circuit_breaker_trip' and 'policy_gate_halt' meant a
                               // compliance failure and a governance bypass rendered like a routine append, while
                               // an Owner's recorded refusal rendered as adverse. A decision is neither.
                               const nat = node?.flag?.nature ?? (node?.flag?.level === 'flagged' ? 'fault'
                                 : node?.flag?.level === 'review' ? 'hold' : 'routine');
                               const tone = nat === 'fault' ? 'text-vital' : nat === 'hold' ? 'text-highlight'
                                 : nat === 'decision' ? 'text-aura' : 'text-slate-400';
                               const why = typeof node?.flag?.why === 'string' ? node.flag.why : null;
                               return (
                                 <div key={node.id} className="p-5 rounded-2xl bg-slate-950 border border-slate-900 flex items-start justify-between gap-4">
                                    <div className="min-w-0">
                                       <p className={`text-[10px] font-black uppercase tracking-widest ${tone}`}>{kind.replace(/_/g, ' ')}</p>
                                       <p className="text-xs text-slate-400 font-bold mt-1 truncate">
                                          {d.action ?? d.reason ?? d.checkpoint_id ?? node.id}
                                       </p>
                                       {/* the classifier's own reason, including "a decision, not a fault" */}
                                       {why && <p className={`text-[10px] font-bold mt-1 ${tone}`}>{why}</p>}
                                       <p className="text-[8px] font-mono text-slate-700 mt-1 break-all">{String(node.hash ?? '').slice(0, 24)}…</p>
                                    </div>
                                    <Activity size={14} className="text-slate-700 shrink-0 mt-1" />
                                 </div>
                               );
                             })}
                          </div>
                       )}
                    </Card>
                 </motion.div>
               )}
            </AnimatePresence>
         </main>
      </div>
    </div>
  );
};
