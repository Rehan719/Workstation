import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { Network, CheckCircle2, Circle, Loader2, Sparkles, GitBranch, Layers, Brain } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';
import { StageBadge, StageMark, FLOOR_STAGE_NOTE, stageOutcome, type StageData } from '../components/StageOutcome';

interface Tier { tier: string; endpoint: string; role: string; connected: boolean }
interface Wiring { tiers: Tier[]; connected: number; total: number; coherence: number; principle: string }
interface Gap { gap: string; realisation: number; routed_to: string; endpoint: string; action: string; missing: string[] }
interface Align { overall_realisation: number; gaps_routed: Gap[]; executed: any[] }

export const CognitionIntegration: React.FC = () => {
  const [wiring, setWiring] = useState<Wiring | null>(null);
  const [knowledge, setKnowledge] = useState<any>(null);
  const [align, setAlign] = useState<Align | null>(null);
  const [alignErr, setAlignErr] = useState('');   // W329 — actions never fail silently
  // W493 (FU-176) - the page claimed CONTINUOUS alignment; that is the heartbeat's auto_align lever,
  // so the lever is read and its real state is stated. null means it could not be read.
  const [autoAlign, setAutoAlign] = useState<boolean | null>(null);
  // W493 (refutation) - a lever set to true does nothing while the heartbeat is STOPPED
  const [beating, setBeating] = useState<boolean | null>(null);
  const [busy, setBusy] = useState(false);
  // §7 — run the Cognitive Cascade with a user-selected subset of engines (reconfigurable resource)
  const [engineCat, setEngineCat] = useState<{ id: string; name: string }[]>([]);
  const [selEngines, setSelEngines] = useState<Set<string>>(new Set());
  const [problem, setProblem] = useState('');
  const [solving, setSolving] = useState(false);
  const [solveRes, setSolveRes] = useState<any>(null);

  useEffect(() => {
    fetch('/api/v1/cognition/wiring').then(r => r.json()).then(setWiring).catch(() => {});
    fetch('/api/v1/cognition/knowledge').then(r => r.json()).then(setKnowledge).catch(() => {});
    fetch('/api/v1/intelligence/cognitive-engines').then(r => r.json()).then(d => setEngineCat(d.engines || [])).catch(() => {});
  }, []);

  const toggleEngine = (id: string) =>
    setSelEngines(prev => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });

  const runSolve = async () => {
    if (!problem.trim()) return;
    setSolving(true); setSolveRes(null);
    try {
      // Ledger cluster 2 — a failed cascade must say WHY, never render an empty success pane
      setSolveRes(await apiJson('/api/v1/intelligence/solve', {
        method: 'POST', body: { problem, domain: 'general', engines: [...selEngines] } }));
    } catch (e) { setAlignErr(errorMessage(e)); }
    setSolving(false);
  };

  useEffect(() => {
    apiJson<{ auto_align?: boolean; running?: boolean }>('/api/v1/heartbeat/status')
      .then(d => {
        setAutoAlign(typeof d?.auto_align === 'boolean' ? d.auto_align : null);
        setBeating(typeof d?.running === 'boolean' ? d.running : null);
      })
      .catch(() => { setAutoAlign(null); setBeating(null); });
  }, []);

  const runAlign = async () => {
    setBusy(true);
    try { setAlign(await apiJson('/api/v1/cognition/align', { method: 'POST', body: { execute: false } })); }
    catch (e) { setAlignErr(errorMessage(e)); }   // W329 + cluster 2: 4xx/5xx surfaces too
    setBusy(false);
  };

  return (
    <div className="space-y-10 pb-24">
      {alignErr && <p className="text-vital text-xs font-bold">{alignErr}</p>}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Integration</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Cognition &amp; Alignment</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The knowledge system wired into every living tier — Chief · Board · AI CEO · C-Suite · CoE · BTO · swarm ·
          arms-length Change Control · heartbeat · evolution. It measures vision realisation and
          <span className="text-highlight"> names the tier that owns each gap</span>.
          {/* W493 (FU-176, sweep S7.5, C4) - this said the organism "self-aligns ... governed and
              continuous". The button posts execute:false, so nothing is sent to any tier, and the
              heartbeat's auto_align lever is off, so nothing does it on a beat either. */}
          <span className="block mt-1 text-slate-600">
            Mapping only: naming an owner is not acting on it. Nothing is sent to any tier from this page,
            and continuous alignment runs only when the heartbeat&apos;s Self-align lever is on AND the
            heartbeat is actually beating
            {autoAlign === null ? ' (lever state unread)'
              : !autoAlign ? ' — the lever is OFF'
              : beating === false ? ' — the lever is on but the heartbeat is STOPPED, so it is not running'
              : beating === null ? ' — the lever is ON (whether the heartbeat beats could not be read)'
              : ' — the lever is ON and the heartbeat is beating'}.
          </span>
        </p>
      </header>

      {/* §7 — Cognitive Cascade runner: reconfigure WHICH engines run, then run on the native fabric */}
      <Card className="p-6 border-aura/30 bg-aura/5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-3 flex items-center gap-2"><Brain size={14} /> Cognitive Cascade · reconfigurable engines (§7)</h3>
        <textarea value={problem} onChange={e => setProblem(e.target.value)} rows={3}
          placeholder="Describe a problem to analyse through the cognitive engines…"
          className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-aura/50 resize-none" />
        {engineCat.length > 0 && (
          <div className="mt-3">
            <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-2">Engines <span className="normal-case font-bold text-slate-600">(none selected = all run)</span></p>
            <div className="flex flex-wrap gap-2">
              {engineCat.map(e => (
                <button key={e.id} type="button" onClick={() => toggleEngine(e.id)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    selEngines.has(e.id) ? 'bg-aura/20 text-aura border border-aura/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}
                  title={e.name}>
                  {e.id}
                </button>
              ))}
            </div>
          </div>
        )}
        <div className="mt-4">
          <Button onClick={runSolve} disabled={solving || !problem.trim()} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
            {solving ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
            {solving ? 'Running cascade…' : `Run cascade${selEngines.size ? ` (${selEngines.size} engine${selEngines.size > 1 ? 's' : ''})` : ''}`}
          </Button>
        </div>
        {solveRes && (
          <div className="mt-4 space-y-3">
            {/* W479 (FU-121 refutation) — three gateway calls: the lenses as ONE prompt, MJM, the synthesis. The list
                names only what ran; each section says what served it (the structured floor is never shown as analysis). */}
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">
              {solveRes.status && solveRes.status !== 'complete' && <span className="text-vital mr-2">{solveRes.status}</span>}
              Lenses selected: <span className="text-aura">{(solveRes.engines_used || []).join(' · ') || 'none'}</span>
            </p>
            {/* W490 (refutation) — the round gave /solve engines_used_basis, calls_made and
                run_summary precisely because "Ran: INKASHAF · SAMAJH · … · MJM · AIGateway" named eight
                analysers over THREE gateway calls, and a floor-served call has failed=False — so a run
                where nothing analysed anything still listed eight engines. It changed the API and not
                this page, which is the one the reader sees. */}
            {solveRes.engines_used_basis && (
              <p className="text-[9px] font-bold text-slate-600" data-testid="solve-engines-basis">
                {solveRes.engines_used_basis}
              </p>
            )}
            {solveRes.run_summary && (
              <p className="text-[10px] font-bold text-amber-400/90" data-testid="solve-run-summary">
                {solveRes.run_summary}
              </p>
            )}
            {solveRes.cognitive_cascade && (
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1 flex items-center gap-2">
                  <StageMark data={solveRes.provenance?.cognitive_cascade as StageData} size={10} />
                  Cognitive lenses · one prompt <StageBadge data={solveRes.provenance?.cognitive_cascade as StageData} />
                </p>
                <p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-52 overflow-y-auto">{solveRes.cognitive_cascade}</p>
                {stageOutcome(solveRes.provenance?.cognitive_cascade as StageData) === 'floor' && (
                  <p className="text-[10px] font-bold text-amber-400/80 mt-2" data-testid="solve-floor-note-cognitive_cascade">{FLOOR_STAGE_NOTE}</p>
                )}
              </div>
            )}
            {solveRes.mjm_assessment && (
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-300 mb-1 flex items-center gap-2">
                  <StageMark data={solveRes.provenance?.mjm_assessment as StageData} size={10} />
                  MJM · Mushahida → Jaiza → Muaina <StageBadge data={solveRes.provenance?.mjm_assessment as StageData} />
                </p>
                <p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-52 overflow-y-auto">{solveRes.mjm_assessment}</p>
                {stageOutcome(solveRes.provenance?.mjm_assessment as StageData) === 'floor' && (
                  <p className="text-[10px] font-bold text-amber-400/80 mt-2" data-testid="solve-floor-note-mjm_assessment">{FLOOR_STAGE_NOTE}</p>
                )}
              </div>
            )}
            {solveRes.synthesis && (
              <div className="p-3 rounded-xl bg-slate-950 border border-highlight/20">
                <p className="text-[9px] font-black uppercase tracking-widest text-highlight mb-1 flex items-center gap-2">
                  <StageMark data={solveRes.provenance?.synthesis as StageData} size={10} />
                  Synthesis <StageBadge data={solveRes.provenance?.synthesis as StageData} />
                </p>
                <p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-52 overflow-y-auto">{solveRes.synthesis}</p>
                {stageOutcome(solveRes.provenance?.synthesis as StageData) === 'floor' && (
                  <p className="text-[10px] font-bold text-amber-400/80 mt-2" data-testid="solve-floor-note-synthesis">{FLOOR_STAGE_NOTE}</p>
                )}
              </div>
            )}
          </div>
        )}
      </Card>

      {/* Four knowledge layers */}
      {knowledge && (
        <Card className="p-6">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2"><Layers size={14} /> Four Synchronised Knowledge Layers</h3>
          <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3">
            {[
              { k: 'Understanding', d: 'the same-page artifact' },
              { k: 'Plan', d: 'vision↔state↔action' },
              { k: 'Memory', d: 'durable agent memory' },
              { k: 'Code / Live-State', d: `realisation ${knowledge.code_live_state?.overall_realisation != null ? Math.round(knowledge.code_live_state.overall_realisation * 100) + '%' : '—'}` },
            ].map(l => (
              <div key={l.k} className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <Brain size={14} className="text-highlight mb-2" />
                <p className="text-[11px] font-black text-white">{l.k}</p>
                <p className="text-[9px] text-slate-500 mt-0.5">{l.d}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Wiring map */}
      {wiring && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><Network size={14} /> Integration Wiring</h3>
            <span className="text-[10px] font-black text-emerald-400">{wiring.connected}/{wiring.total} connected · {Math.round(wiring.coherence * 100)}% coherence</span>
          </div>
          <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-2">
            {wiring.tiers.map(t => (
              <div key={t.tier} className="flex items-start gap-3 p-3 rounded-xl bg-slate-950 border border-slate-900">
                {t.connected ? <CheckCircle2 size={14} className="text-emerald-400 mt-0.5 shrink-0" /> : <Circle size={14} className="text-slate-600 mt-0.5 shrink-0" />}
                <div className="min-w-0">
                  <p className="text-xs font-black text-white">{t.tier}</p>
                  <p className="text-[9px] text-slate-500">{t.role}</p>
                  <p className="text-[8px] font-mono text-slate-700 mt-0.5">{t.endpoint}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="text-[9px] text-slate-600 italic mt-3">{wiring.principle}</p>
        </Card>
      )}

      {/* Alignment */}
      <Card className="p-6 border-highlight/30 bg-highlight/5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-black text-highlight uppercase tracking-widest text-sm flex items-center gap-2"><GitBranch size={16} /> Autonomous Alignment</h3>
          <Button onClick={runAlign} disabled={busy} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
            {busy ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} Route Gaps
          </Button>
        </div>
        {align ? (
          align.gaps_routed.length === 0
            ? <p className="text-sm text-emerald-400 font-bold">Fully aligned — no open vision gaps.</p>
            : (
              <div className="space-y-2">
                {/* W493 (FU-176) - "routed" reads as sent; every gap comes back executed:false */}
                <p className="text-[10px] font-black uppercase text-slate-500" data-testid="align-result">
                  Overall realisation {Math.round(align.overall_realisation * 100)}% ·{' '}
                  {align.gaps_routed.length} gap(s) mapped to an owning tier ·{' '}
                  {(align.executed || []).length} acted on
                  {(align.executed || []).length === 0 ? ' (plan only — nothing was sent)' : ''}
                </p>
                {align.gaps_routed.map((g, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-900">
                    <div className="min-w-0">
                      <p className="text-sm text-slate-300 font-bold truncate">{g.gap}</p>
                      <p className="text-[9px] text-slate-600">{g.action}</p>
                    </div>
                    <span className="text-[10px] font-black text-highlight uppercase shrink-0 ml-3">→ {g.routed_to}</span>
                  </div>
                ))}
              </div>
            )
        ) : <p className="text-sm text-slate-500">Run alignment to route each open vision gap to the tier that owns it.</p>}
      </Card>
    </div>
  );
};
