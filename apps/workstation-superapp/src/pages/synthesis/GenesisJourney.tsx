import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { saveOutput } from '../../lib/outputHistory';
import { Card, Button } from '@workstation/ui';
import { AttachDocument, appendDocBlock } from '../../components/AttachDocument';
import { DictateButton } from '../../components/DictateButton';
import { getPrefs } from '../../lib/userPrefs';
import {
  Sparkles, Loader2, AlertCircle, ChevronDown, ChevronUp,
  Lightbulb, Layers, Rocket, ShieldCheck, Brain, Eye,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface JourneyResult {
  problem: string;
  domain: string;
  realm: string;
  phase_1_conceptualisation: { cognitive_cascade: string; mjm_assessment: string; concept: string };
  stage_3_innovate_research?: string;   // §4.3 — best/latest approaches + innovative options
  // §4.5 — candidate solutions modelled + evidence-ranked → best selected.
  stage_5_model_simulate_rank?: {
    method: string; selected: string; selection_basis: string;
    candidates: { id: string; framing: string; rank: number; score: number; coverage: number;
      specificity: number; structure: number; approach: string }[];
  };
  phase_2_design_development: string;
  stage_7_operational_intelligence?: string;   // §4.7 — deliverable · compliant · operable
  phase_3_commercialisation: string;
  governance: { status: string; checkpoint: string | null; node: string };
  // §5 — each stage verified/tested/validated on real measured proxies
  stage_verifications?: Record<string, { verified: boolean; score: number; sections_present: string }>;
  stages_verified?: string;
  quality_assurance?: {
    quality?: { qms_gate_passed?: boolean; delivery_coverage?: number; bar?: string[];
      quality_record_hash?: string; document_controlled?: boolean;
      compliance?: { overall?: string; compliant?: boolean; verdicts?: { framework: string; status: string }[] } };
    biomimetic?: { immune?: { health?: number }; circadian?: string; layers?: string[]; self?: string };
  };
  engines_used: string[];
  deliverable: string;
  status: string;
}
interface RepoManifest {
  vsb_id: string; name: string; file_count: number; total_bytes: number; tree: string[];
  integrated_surfaces: { website: string; webapp: string; mobile: string };
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean } } };
}
interface WebsiteManifest {
  vsb_id: string; name: string; kind: string; page_count: number; total_bytes: number;
  nav: { label: string; href: string }[]; preview: string;
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean } } };
}
interface WebAppManifest {
  vsb_id: string; name: string; kind: string; interactive: boolean; file_count: number;
  features: string[]; preview: string;
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean } } };
}
interface PwaManifest {
  vsb_id: string; name: string; kind: string; installable: boolean; offline_capable: boolean;
  file_count: number; features: string[]; preview: string;
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean } } };
}
interface BoardPack {
  vsb_id: string; name: string; kind: string; narrative: string; dcs_registered: boolean; dcs_hash?: string;
  layers: Record<string, unknown>;
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean } } };
}
interface ReviewGates {
  mode: string; stages: string[];
  lifecycle: { id: string; name: string; description: string }[];
  statuses: { stage: string; gated: boolean; status: string; blocks_progress: boolean }[];
}

// W303 — idempotent seed reader: module-level cache survives React StrictMode's double-mount
// (a side-effectful useState initializer would consume the seed on the discarded first mount).
const _seedCache: Record<string, { title?: string; domain?: string; input?: string; output?: string } | null> = {};
function readGenesisSeed(sid: string) {
  if (!(sid in _seedCache)) {
    try {
      const raw = sessionStorage.getItem(`ws_genesis_${sid}`);
      _seedCache[sid] = raw ? JSON.parse(raw) : null;
      sessionStorage.removeItem(`ws_genesis_${sid}`);
    } catch { _seedCache[sid] = null; }
  }
  return _seedCache[sid];
}

const REALMS = ['enterprise', 'learning', 'developing', 'scholarship'];
// §17.1 — the six canonical Domains (matches the Domains section hubs). Realm (who you are) is separate.
const DOMAINS = ['religion', 'science', 'education', 'law', 'employment', 'care'];

// ── Component ─────────────────────────────────────────────────────────────────

export const GenesisJourney: React.FC = () => {
  const navigate = useNavigate();
  const [sp] = useSearchParams();   // seedable from a domain tool (offering 1 -> offering 2, §3A)
  // W303 - the bridge carries the user's actual WORK PRODUCT (not a truncated input slice):
  // a sessionStorage seed written by DomainTool / My Work is folded into the problem once.
  const [problem, setProblem] = useState<string>(() => {
    const sid = sp.get('seed');
    if (sid) {
      const seed = readGenesisSeed(sid);
      if (seed) {
        const base = String(seed.input || seed.title || '').slice(0, 600);
        const work = String(seed.output || '').slice(0, 12000);
        return work
          ? `${base}\n\nPRIOR DOMAIN WORK (Offering-1 output — build on this):\n${work}`
          : base;
      }
    }
    return sp.get('problem') || '';
  });
  const [domain, setDomain] = useState(() => { const d = sp.get('domain') || 'science'; return DOMAINS.includes(d) ? d : 'science'; });
  const [realm, setRealm] = useState(() => { const r = sp.get('realm') || 'enterprise'; return REALMS.includes(r) ? r : 'enterprise'; });
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<JourneyResult | null>(null);
  const [open, setOpen] = useState<string>('phase1');
  const [establishing, setEstablishing] = useState(false);
  // §5 — the live birth log: each entry is a REAL completed establishment step from the SSE stream
  const [birthStages, setBirthStages] = useState<{ stage: string; label: string; content: string }[]>([]);
  const [vsb, setVsb] = useState<{ vsb_id: string; name: string; dashboard: string; governance?: any } | null>(null);
  // §2 — the VSB's legal/economic form, selected by the user at generation (wired to the economy templates)
  const [entityTypes, setEntityTypes] = useState<{ id: string; name: string; description: string }[]>([]);
  const [entityType, setEntityType] = useState('waqf_ltd_hybrid');
  const [establishOnComplete, setEstablishOnComplete] = useState(false);   // §5 — one continuous workflow → living enterprise

  useEffect(() => {
    fetch('/api/v1/economy/entity-types').then(r => r.json())
      .then(d => { setEntityTypes(d.types ?? []); if (d.default) setEntityType(d.default); })
      .catch(() => {});
  }, []);
  // §13 — the VSB IDBO Entity Repository (integrated Website · Web app · Phone app scaffold)
  const [repo, setRepo] = useState<RepoManifest | null>(null);
  const [repoBusy, setRepoBusy] = useState(false);
  const [site, setSite] = useState<WebsiteManifest | null>(null);
  const [siteBusy, setSiteBusy] = useState(false);
  const [webapp, setWebapp] = useState<WebAppManifest | null>(null);
  const [webappBusy, setWebappBusy] = useState(false);
  const [pwa, setPwa] = useState<PwaManifest | null>(null);
  const [pwaBusy, setPwaBusy] = useState(false);
  const [pack, setPack] = useState<BoardPack | null>(null);
  const [packBusy, setPackBusy] = useState(false);
  const [gates, setGates] = useState<ReviewGates | null>(null);
  const [gatesOpen, setGatesOpen] = useState(false);

  const run = async () => {
    if (!problem.trim()) return;
    setRunning(true);
    setError('');
    setResult(null);
    setVsb(null);
    try {
      const res = await fetch('/api/v1/genesis/journey', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // §5 — when "establish on completion" is on, ONE continuous workflow takes the challenge all the way
        // to a living VSB enterprise (W222 seam); else the journey stops at the blueprint (two-step establish).
        body: JSON.stringify(establishOnComplete
          ? { problem, domain, realm, establish: true, entity_type: entityType }
          : { problem, domain, realm }),
      });
      if (!res.ok) { setError(`HTTP ${res.status}`); setRunning(false); return; }
      const data = await res.json();
      setResult(data);
      if (data?.established_vsb && !data.established_vsb.error) setVsb(data.established_vsb);   // one-call living enterprise
      // W303 - the My Work claim is TRUE now: every Genesis journey persists automatically.
      try {
        const stages = [data?.phase_1_conceptualisation?.concept, data?.stage_3_innovate_research,
          data?.phase_2_design_development, data?.phase_3_commercialisation]
          .filter(Boolean).map(String).join('\n\n---\n\n');
        saveOutput({ kind: 'genesis', title: `Genesis: ${problem.slice(0, 70)}`, domain,
          output: (stages || JSON.stringify(data).slice(0, 4000)),
          provenance: data?.ai_provenance ?? null,
          vsb_id: data?.established_vsb?.vsb_id });
      } catch { /* history is best-effort */ }
    } catch (e: any) {
      setError(e?.message ?? String(e));
    }
    setRunning(false);
  };

  const establish = async () => {
    if (!result) return;
    setEstablishing(true);
    setBirthStages([]);
    const body = JSON.stringify({
      problem, domain, realm, entity_type: entityType,
      concept: result.phase_1_conceptualisation.concept,
      design: result.phase_2_design_development,
      commercialisation: result.phase_3_commercialisation,
    });
    try {
      // §5 — watch the VSB being born: each SSE event reflects a REAL completed establishment step
      const res = await fetch('/api/v1/genesis/establish/stream', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body,
      });
      if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = '';
      let complete: any = null;
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop() ?? '';
        for (const raw of lines) {
          if (!raw.startsWith('data: ')) continue;
          try {
            const ev = JSON.parse(raw.slice(6));
            setBirthStages(s => [...s, { stage: ev.stage, label: ev.label, content: ev.content }]);
            if (ev.stage === 'complete' && ev.data) complete = ev.data;
          } catch { /* skip malformed frame */ }
        }
      }
      if (!complete) throw new Error('stream ended without completion');
      setVsb(complete);
    } catch {
      // fallback — the blocking establish (same machinery, no live stages)
      try {
        const res = await fetch('/api/v1/genesis/establish', {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body,
        });
        setVsb(await res.json());
      } catch { /* surfaced by absence of vsb */ }
    }
    setEstablishing(false);
  };

  // §13 — generate the bespoke VSB IDBO Entity Repository (integrated Website · Web app · Phone app scaffold)
  const generateRepo = async () => {
    if (!vsb) return;
    setRepoBusy(true); setRepo(null);
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/repo`, { method: 'POST' });
      if (res.ok) setRepo(await res.json());
    } catch { /* ignore */ }
    setRepoBusy(false);
  };

  // §13 increment 2 — generate the integrated Website (real multi-page static HTML/CSS into the repo)
  const generateWebsite = async () => {
    if (!vsb) return;
    setSiteBusy(true); setSite(null);
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/website`, { method: 'POST' });
      if (res.ok) setSite(await res.json());
    } catch { /* ignore */ }
    setSiteBusy(false);
  };

  // §13 increment 3 — generate the interactive Web app (real client-side vanilla-JS app into the repo)
  const generateWebApp = async () => {
    if (!vsb) return;
    setWebappBusy(true); setWebapp(null);
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/webapp`, { method: 'POST' });
      if (res.ok) setWebapp(await res.json());
    } catch { /* ignore */ }
    setWebappBusy(false);
  };

  // §13 increment 4 — generate the Phone app (real installable PWA into the repo's mobile/)
  const generatePhoneApp = async () => {
    if (!vsb) return;
    setPwaBusy(true); setPwa(null);
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/mobile`, { method: 'POST' });
      if (res.ok) setPwa(await res.json());
    } catch { /* ignore */ }
    setPwaBusy(false);
  };

  // §17.3 — assemble the Living Business System's on-demand Board Pack (DCS-registered)
  const generateBoardPack = async () => {
    if (!vsb) return;
    setPackBusy(true); setPack(null);
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/board-pack`, { method: 'POST' });
      if (res.ok) setPack(await res.json());
    } catch { /* ignore */ }
    setPackBusy(false);
  };

  // §17.4 Mode 3 — configure optional human review gates (genome-set) for the VSB
  const openGates = async () => {
    setGatesOpen(true);
    if (!vsb) return;
    try { setGates(await fetch(`/api/v1/vsb/${vsb.vsb_id}/review-gates`).then(r => r.json())); } catch { /* */ }
  };
  const toggleGate = async (stageId: string) => {
    if (!vsb || !gates) return;
    const next = gates.stages.includes(stageId) ? gates.stages.filter(s => s !== stageId) : [...gates.stages, stageId];
    try {
      const res = await fetch(`/api/v1/vsb/${vsb.vsb_id}/review-gates`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ stages: next }),
      });
      if (res.ok) setGates(await res.json());
    } catch { /* */ }
  };
  const decideGate = async (stage: string, decision: 'approve' | 'reject') => {
    if (!vsb) return;
    try {
      await fetch(`/api/v1/vsb/${vsb.vsb_id}/review-gates/${stage}/decision`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ decision }),
      });
      setGates(await fetch(`/api/v1/vsb/${vsb.vsb_id}/review-gates`).then(r => r.json()));
    } catch { /* */ }
  };

  const phases = result ? [
    { key: 'phase1', n: 1, icon: Lightbulb, label: 'Conceptualisation',
      blurb: 'Understand → analyse → optimal solution concept',
      body: (
        <div className="space-y-5">
          <Section icon={Brain} title="Cognitive Cascade (6 engines)" text={result.phase_1_conceptualisation.cognitive_cascade} />
          <Section icon={Eye} title="MJM Assessment" text={result.phase_1_conceptualisation.mjm_assessment} />
          <Section icon={Lightbulb} title="Optimal Solution Concept" text={result.phase_1_conceptualisation.concept} highlight />
        </div>
      ) },
    { key: 'phase2', n: 2, icon: Layers, label: 'Design & Development',
      blurb: 'Concept → buildable solution design',
      body: <PlainText text={result.phase_2_design_development} /> },
    { key: 'phase3', n: 3, icon: Rocket, label: 'Enterprise Commercialisation',
      blurb: 'Go-to-market + the user’s own living VSB',
      body: <PlainText text={result.phase_3_commercialisation} /> },
  ] : [];

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">
          Workstation IDBO · Offering 2 · Build an Enterprise
        </p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Genesis
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          One progressive, intelligently-autonomous workflow that takes a problem from
          <span className="text-highlight"> Conceptualisation → Design &amp; Development → Commercialisation</span> —
          composing the six cognitive engines, MJM, the design and business engines, and the constitutional
          gate into your own living VSB blueprint.
        </p>
      </header>

      {/* Whole-journey progress map (§4 / §9) — the full Concept→Commercialisation arc + where you are now.
          Each milestone lights from REAL state (no fabrication): described → explored → established →
          surfaces generated → operating. */}
      {(() => {
        const surfaces = !!(repo || site || webapp || pwa);
        const steps = [
          { id: 'describe',  label: 'Describe',     done: !!problem.trim(), hint: 'Your challenge / concept' },
          { id: 'explore',   label: 'Explore',      done: !!result,         hint: 'Conceptualise · Design · Commercialise' },
          { id: 'establish', label: 'Establish',    done: !!vsb,            hint: 'Your living VSB IDBO entity' },
          { id: 'deliver',   label: 'Deliver',      done: surfaces,         hint: 'Repo · Website · Web app · Phone app' },
          { id: 'operate',   label: 'Operate',      done: !!vsb && surfaces, hint: 'Run · defend · improve · grow' },
        ];
        const currentIdx = steps.findIndex(s => !s.done);
        return (
          <div className="flex items-stretch gap-2 overflow-x-auto pb-1">
            {steps.map((s, i) => {
              const isCurrent = i === currentIdx;
              return (
                <div key={s.id} className="flex items-center gap-2 shrink-0">
                  <div className={`px-3 py-2 rounded-xl border min-w-[112px] transition-all ${
                    s.done ? 'bg-highlight/10 border-highlight/30' : isCurrent ? 'bg-aura/10 border-aura/40' : 'bg-slate-900 border-slate-800'}`}>
                    <div className="flex items-center gap-1.5">
                      <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-black ${
                        s.done ? 'bg-highlight text-sovereign' : isCurrent ? 'bg-aura text-sovereign' : 'bg-slate-800 text-slate-500'}`}>
                        {s.done ? '✓' : i + 1}
                      </span>
                      <span className={`text-[10px] font-black uppercase tracking-widest ${s.done ? 'text-highlight' : isCurrent ? 'text-aura' : 'text-slate-500'}`}>{s.label}</span>
                    </div>
                    <p className="text-[8px] text-slate-600 mt-1 leading-tight">{s.hint}</p>
                  </div>
                  {i < steps.length - 1 && <div className={`w-4 h-px ${s.done ? 'bg-highlight/40' : 'bg-slate-800'}`} />}
                </div>
              );
            })}
          </div>
        );
      })()}

      {/* Stage rail — the §4 fine-resolution Concept → Commercialisation lifecycle the journey runs */}
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-5">Concept → Commercialisation · fine-resolution lifecycle (§4)</h3>
        <div className="grid grid-cols-1 @[560px]:grid-cols-3 @[900px]:grid-cols-6 gap-3">
          {[
            { icon: Lightbulb,  label: 'Conceptualise',          desc: 'Cognitive cascade + MJM → optimal concept' },
            { icon: Eye,        label: 'Innovate & Research',     desc: 'Best/latest approaches: science·tech·business·law' },
            { icon: Brain,      label: 'Model · Simulate · Rank', desc: 'Candidate solutions scored on evidence → best' },
            { icon: Layers,     label: 'Design & Development',    desc: 'Architecture, components, MVP scope' },
            { icon: ShieldCheck,label: 'Operational Intelligence',desc: 'Deliverable · compliant · operable' },
            { icon: Rocket,     label: 'Commercialise',           desc: 'GTM + revenue + living VSB blueprint' },
          ].map(({ icon: Icon, label, desc }, i) => {
            const done = !!result;
            return (
              <div key={label} className={`p-4 rounded-2xl border transition-all ${done ? 'bg-highlight/10 border-highlight/20' : running ? 'bg-aura/10 border-aura/30 animate-pulse' : 'bg-slate-900 border-slate-800'}`}>
                <div className="flex items-center gap-2 mb-2">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center ${done ? 'bg-highlight/20' : 'bg-slate-800'}`}>
                    <Icon size={12} className={done ? 'text-highlight' : 'text-slate-500'} />
                  </div>
                  <span className={`text-[9px] font-black uppercase tracking-widest ${done ? 'text-highlight' : 'text-slate-600'}`}>Stage {i + 1}</span>
                </div>
                <p className={`text-[11px] font-black mb-1 ${done ? 'text-white' : 'text-slate-400'}`}>{label}</p>
                <p className="text-[9px] text-slate-600 leading-relaxed">{desc}</p>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Input */}
      <Card className="p-8 space-y-7">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Problem / Goal / Concept</label>
          <textarea
            value={problem}
            onChange={e => setProblem(e.target.value)}
            placeholder="Describe the problem to solve or the concept to commercialise. Genesis drives it end-to-end into your own VSB."
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none"
          />
          {/* §9 — multimodal input: attach your own data and/or dictate the challenge by voice */}
          <div className="mt-2 flex items-start gap-2 flex-wrap">
            <AttachDocument
              hint="bring your own data — research report, brief, dataset (read in-browser, stays with this request)"
              onText={block => setProblem(p => appendDocBlock(p, block))} />
            <DictateButton lang={getPrefs().language || 'en-US'} onTranscript={text => setProblem(p => (p ? p + ' ' : '') + text)} />
          </div>
        </div>
        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-6">
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Realm</label>
            <div className="flex flex-wrap gap-2">
              {REALMS.map(r => (
                <button key={r} type="button" onClick={() => setRealm(r)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${realm === r ? 'bg-highlight/20 text-highlight border border-highlight/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}>{r}</button>
              ))}
            </div>
          </div>
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Domain</label>
            <div className="flex flex-wrap gap-2">
              {DOMAINS.map(d => (
                <button key={d} type="button" onClick={() => setDomain(d)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${domain === d ? 'bg-highlight/20 text-highlight border border-highlight/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}>{d}</button>
              ))}
            </div>
          </div>
        </div>
        {/* §5 — one continuous workflow: optionally take the challenge all the way to a living VSB enterprise */}
        <div className="pt-2 flex flex-col @[560px]:flex-row @[560px]:items-end gap-3 flex-wrap">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input type="checkbox" checked={establishOnComplete} onChange={e => setEstablishOnComplete(e.target.checked)}
              className="accent-highlight w-4 h-4" aria-label="Establish living VSB on completion" />
            <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">Establish living VSB on completion <span className="text-slate-600 normal-case">(one continuous workflow → living enterprise)</span></span>
          </label>
          {establishOnComplete && entityTypes.length > 0 && (
            <div>
              <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-1 block">Legal / economic form</label>
              <select aria-label="Legal / economic form" value={entityType} onChange={e => setEntityType(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-lg text-[11px] font-black uppercase text-slate-300 px-3 py-2 focus:outline-none focus:border-highlight/50">
                {entityTypes.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
          )}
        </div>
        <div className="flex items-center gap-4 pt-2">
          <Button onClick={run} disabled={running || !problem.trim()} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {running ? (establishOnComplete ? 'Concept → living enterprise…' : 'Running Sovereign Journey…')
                     : (establishOnComplete ? 'Launch Journey → Establish VSB' : 'Launch Genesis Journey')}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {/* Result */}
      {result && (
        <div className="space-y-4">
          {/* §5 — each stage verified/tested/validated (real measured proxies) */}
          {result.stage_verifications && (
            <Card className="p-4 border-emerald-500/20">
              <div className="flex items-center justify-between gap-3 flex-wrap mb-2">
                <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2"><ShieldCheck size={13} className="text-emerald-400" /> Stage verification — each stage tested &amp; validated (§5)</h3>
                {result.stages_verified && <span className="text-[9px] font-black uppercase text-emerald-400">{result.stages_verified} verified</span>}
              </div>
              <div className="flex flex-wrap gap-2">
                {Object.entries(result.stage_verifications).map(([stage, v]) => (
                  <span key={stage} title={`score ${v.score} · sections ${v.sections_present}`}
                    className={`text-[9px] font-black uppercase px-2 py-1 rounded ${v.verified ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                    {v.verified ? '✓' : '⚠'} {stage} · {Math.round(v.score * 100)}%
                  </span>
                ))}
              </div>
            </Card>
          )}
          {phases.map(p => (
            <Card key={p.key} className="p-0 overflow-hidden border-slate-800/80">
              <button type="button" onClick={() => setOpen(open === p.key ? '' : p.key)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-highlight/10 flex items-center justify-center"><p.icon size={14} className="text-highlight" /></div>
                  <div>
                    <p className="font-black text-white text-sm">Phase {p.n} · {p.label}</p>
                    <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">{p.blurb}</p>
                  </div>
                </div>
                {open === p.key ? <ChevronUp size={14} className="text-slate-500" /> : <ChevronDown size={14} className="text-slate-500" />}
              </button>
              {open === p.key && <div className="px-5 pb-6 border-t border-slate-800/50 pt-4">{p.body}</div>}
            </Card>
          ))}

          {/* §4.3 — Innovate & Research: best/latest approaches across science·tech·business·ops·law */}
          {result.stage_3_innovate_research && (
            <Card className="p-5 border-slate-800">
              <div className="flex items-center gap-2 mb-2">
                <Eye size={15} className="text-aura" />
                <h3 className="text-xs font-black uppercase tracking-widest text-aura">Innovate &amp; Research (§4.3)</h3>
              </div>
              <p className="text-[10px] text-slate-600 mb-2">Best &amp; latest approaches + innovative options across science · technology · business · operations · law — feeding the candidate solutions below.</p>
              <PlainText text={result.stage_3_innovate_research} />
            </Card>
          )}

          {/* §4.5 — Model · Simulate · Optimise · Rank: candidate solutions evidence-ranked, best selected */}
          {result.stage_5_model_simulate_rank && (
            <Card className="p-5 border-aura/30 bg-aura/5">
              <div className="flex items-center gap-2 mb-1">
                <Layers size={15} className="text-aura" />
                <h3 className="text-xs font-black uppercase tracking-widest text-aura">Model · Simulate · Optimise · Rank (§4.5)</h3>
              </div>
              <p className="text-[10px] text-slate-500 mb-3">{result.stage_5_model_simulate_rank.method}</p>
              <div className="space-y-2">
                {result.stage_5_model_simulate_rank.candidates.map(c => {
                  const isWin = c.id === result.stage_5_model_simulate_rank!.selected;
                  return (
                    <div key={c.id} className={`p-3 rounded-xl border ${isWin ? 'border-aura/50 bg-aura/10' : 'border-slate-800 bg-slate-950'}`}>
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2 min-w-0">
                          <span className={`text-[9px] font-black w-5 h-5 rounded-full flex items-center justify-center ${isWin ? 'bg-aura text-sovereign' : 'bg-slate-800 text-slate-400'}`}>{c.rank}</span>
                          <span className="text-[11px] font-black text-white uppercase tracking-wide truncate">{c.id}</span>
                          {isWin && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/20 text-aura shrink-0">selected</span>}
                        </div>
                        <span className="text-[9px] font-mono text-slate-500 shrink-0" title={`coverage ${c.coverage} · specificity ${c.specificity} · structure ${c.structure}`}>score {c.score}</span>
                      </div>
                      <p className="text-[9px] text-slate-500 mt-1 leading-snug">{c.framing}</p>
                    </div>
                  );
                })}
              </div>
              <p className="text-[9px] text-slate-600 mt-2">{result.stage_5_model_simulate_rank.selection_basis} — the winner is carried into Design.</p>
            </Card>
          )}

          {/* §4.7 — Enhance via Operational Intelligence: deliverable · compliant · operable */}
          {result.stage_7_operational_intelligence && (
            <Card className="p-5 border-slate-800">
              <div className="flex items-center gap-2 mb-2">
                <ShieldCheck size={15} className="text-aura" />
                <h3 className="text-xs font-black uppercase tracking-widest text-aura">Operational Intelligence (§4.7)</h3>
              </div>
              <p className="text-[10px] text-slate-600 mb-2">Makes the solution not just innovative but deliverable, compliant (legal · regulatory · EHS · Sharia · ethical) and operable — before commercialisation.</p>
              <PlainText text={result.stage_7_operational_intelligence} />
            </Card>
          )}

          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <div className="flex items-center gap-3 mb-3">
              <ShieldCheck size={18} className="text-highlight" />
              <h3 className="font-black text-highlight uppercase tracking-widest text-sm">Sovereign Journey Complete</h3>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed">{result.deliverable}</p>
            <div className="flex flex-wrap items-center gap-2 mt-4">
              {result.engines_used.map(e => (
                <span key={e} className="px-2 py-0.5 rounded-md bg-highlight/10 text-highlight text-[9px] font-black uppercase tracking-wider">{e}</span>
              ))}
            </div>
            <p className="text-[9px] font-mono text-slate-500 mt-3">
              governance: {result.governance.status} · checkpoint {result.governance.checkpoint ?? '—'}
            </p>
            {/* Continual operational delivery within the living QMS — §10 bar + §8 organism */}
            {result.quality_assurance?.quality && (
              <div className="flex flex-wrap items-center gap-2 mt-2">
                {typeof result.quality_assurance.quality.qms_gate_passed === 'boolean' && (
                  <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${result.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                    title={`§10 Solution-Quality Bar: ${(result.quality_assurance.quality.bar || []).join(' · ')}${result.quality_assurance.quality.quality_record_hash ? `\nDocument-controlled under the QMS (DCMS) · record ${result.quality_assurance.quality.quality_record_hash.slice(0, 16)}…` : ''}`}>
                    Living-QMS gate: {result.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'} · cov {Math.round((result.quality_assurance.quality.delivery_coverage || 0) * 100)}%{result.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                  </span>
                )}
                {result.quality_assurance.biomimetic?.immune && (
                  <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-violet-500/15 text-violet-300"
                    title={`7 biomimetic layers · ${result.quality_assurance.biomimetic.self || ''}`}>
                    organism: immune {Math.round((result.quality_assurance.biomimetic.immune.health ?? 0) * 100)}% · {result.quality_assurance.biomimetic.circadian}
                  </span>
                )}
                {result.quality_assurance.quality?.compliance && (
                  <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${result.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                    title={`§11 live compliance — ${(result.quality_assurance.quality.compliance.verdicts || []).map(v => `${v.framework}:${v.status}`).join(' · ')}`}>
                    compliance: {result.quality_assurance.quality.compliance.overall}
                  </span>
                )}
              </div>
            )}

            <div className="mt-5 pt-4 border-t border-highlight/20">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">
                Deliver the outcome — generate the living Enterprise IDBO
              </p>
              {!vsb ? (
                <div className="space-y-3">
                  {/* §2 — select the VSB's legal / economic form at generation */}
                  {entityTypes.length > 0 && (
                    <div>
                      <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-1.5 block">Legal / economic form</label>
                      <select aria-label="Legal / economic form" value={entityType} onChange={e => setEntityType(e.target.value)}
                        className="w-full @[480px]:w-auto bg-slate-900 border border-slate-800 rounded-lg text-[11px] font-black uppercase text-slate-300 px-3 py-2 focus:outline-none focus:border-highlight/50">
                        {entityTypes.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                      </select>
                      <p className="text-[9px] text-slate-600 mt-1">{entityTypes.find(t => t.id === entityType)?.description}</p>
                    </div>
                  )}
                  <Button onClick={establish} disabled={establishing} className="flex items-center gap-2 bg-highlight text-sovereign">
                    {establishing ? <Loader2 size={16} className="animate-spin" /> : <Rocket size={16} />}
                    {establishing ? 'Establishing VSB…' : 'Establish VSB IDBO Entity'}
                  </Button>
                  {birthStages.length > 0 && (
                    <div className="mt-3 p-3 rounded-2xl bg-slate-950 border border-slate-800 space-y-1.5">
                      <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500">The VSB being born — live</p>
                      {birthStages.map((s, i) => (
                        <div key={`${s.stage}-${i}`} className="flex items-start gap-2">
                          <span className={`mt-1 w-1.5 h-1.5 rounded-full shrink-0 ${s.stage === 'complete' ? 'bg-emerald-400' : 'bg-highlight'}`} />
                          <p className="text-[10px] text-slate-300 leading-snug">
                            <span className="font-black uppercase tracking-widest text-slate-400">{s.label}</span>
                            <span className="text-slate-500"> — {s.content}</span>
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-4 rounded-2xl bg-slate-950 border border-emerald-500/30">
                  <div className="flex items-center gap-2 mb-1">
                    <ShieldCheck size={14} className="text-emerald-400" />
                    <p className="font-black text-white text-sm">{vsb.name}</p>
                  </div>
                  <p className="text-[10px] text-slate-500 font-mono">
                    {vsb.vsb_id} · operational · governance {vsb.governance?.status ?? 'allowed'}
                  </p>
                  <p className="text-[10px] text-emerald-400 font-bold mt-1">
                    Living Enterprise IDBO generated — dashboard {vsb.dashboard}
                  </p>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <button type="button" onClick={() => navigate(`/business-plan?scope=${encodeURIComponent(vsb.vsb_id)}`)}
                      className="text-[10px] font-black uppercase tracking-widest text-highlight border border-highlight/40 px-3 py-1.5 rounded-lg hover:bg-highlight/10 transition-colors">
                      Open the VSB’s Business Plan →
                    </button>
                    <button type="button" onClick={() => navigate(`/vsb-cockpit?vsb=${encodeURIComponent(vsb.vsb_id)}`)}
                      className="text-[10px] font-black uppercase tracking-widest text-aura border border-aura/40 px-3 py-1.5 rounded-lg hover:bg-aura/10 transition-colors">
                      VSB Cockpit →
                    </button>
                  </div>
                  <p className="text-[9px] text-slate-500 mt-2 leading-relaxed">
                    Its plan already opens with an Executive Summary · Concept · Vision, seeded from this journey.
                  </p>
                  {birthStages.length > 0 && (
                    <div className="mt-3 p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1.5">
                      <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500">Birth record — every step really happened</p>
                      {birthStages.map((s, i) => (
                        <div key={`br-${s.stage}-${i}`} className="flex items-start gap-2">
                          <span className={`mt-1 w-1.5 h-1.5 rounded-full shrink-0 ${s.stage === 'complete' ? 'bg-emerald-400' : 'bg-highlight'}`} />
                          <p className="text-[10px] text-slate-300 leading-snug">
                            <span className="font-black uppercase tracking-widest text-slate-400">{s.label}</span>
                            <span className="text-slate-500"> — {s.content}</span>
                          </p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* §13 — generate the bespoke VSB IDBO Entity Repository (Website · Web app · Phone app scaffold) */}
                  <div className="mt-3 pt-3 border-t border-slate-800">
                    <Button onClick={generateRepo} disabled={repoBusy} className="flex items-center gap-2 bg-slate-900 text-highlight text-[11px]">
                      {repoBusy ? <Loader2 size={13} className="animate-spin" /> : <Layers size={13} />}
                      {repoBusy ? 'Generating repository…' : 'Generate VSB Repository'}
                    </Button>
                    {repo && (
                      <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <div className="flex flex-wrap items-center gap-1.5">
                          <span className="text-[9px] font-black uppercase tracking-widest text-highlight">Repository</span>
                          <span className="text-[8px] font-mono text-slate-500">{repo.file_count} files · {repo.total_bytes} bytes</span>
                          {typeof repo.quality_assurance?.quality?.qms_gate_passed === 'boolean' && (
                            <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${repo.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                              QMS: {repo.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'}{repo.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                            </span>
                          )}
                          {repo.quality_assurance?.quality?.compliance && (
                            <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${repo.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                              compliance: {repo.quality_assurance.quality.compliance.overall}
                            </span>
                          )}
                        </div>
                        <p className="text-[9px] font-mono text-slate-400 leading-relaxed">{repo.tree.join('  ·  ')}</p>
                        <p className="text-[9px] text-slate-500">Integrated surfaces — Website: <span className="text-slate-400">{repo.integrated_surfaces.website}</span> · Web app: <span className="text-slate-400">{repo.integrated_surfaces.webapp}</span> · Phone app: <span className="text-slate-400">{repo.integrated_surfaces.mobile}</span></p>
                      </div>
                    )}

                    {/* §13 increment 2 — generate the integrated Website (real multi-page static HTML/CSS) */}
                    <div className="mt-3">
                      <Button onClick={generateWebsite} disabled={siteBusy} className="flex items-center gap-2 bg-slate-900 text-aura text-[11px]">
                        {siteBusy ? <Loader2 size={13} className="animate-spin" /> : <Layers size={13} />}
                        {siteBusy ? 'Generating website…' : 'Generate integrated Website'}
                      </Button>
                      {site && (
                        <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                          <div className="flex flex-wrap items-center gap-1.5">
                            <span className="text-[9px] font-black uppercase tracking-widest text-aura">Website · {site.kind}</span>
                            <span className="text-[8px] font-mono text-slate-500">{site.page_count} pages · {site.total_bytes} bytes</span>
                            {typeof site.quality_assurance?.quality?.qms_gate_passed === 'boolean' && (
                              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${site.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                QMS: {site.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'}{site.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                              </span>
                            )}
                            {site.quality_assurance?.quality?.compliance && (
                              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${site.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                compliance: {site.quality_assurance.quality.compliance.overall}
                              </span>
                            )}
                          </div>
                          <p className="text-[9px] text-slate-500">Pages: {site.nav.map(n => n.label).join(' · ')}</p>
                          <a href={site.preview} target="_blank" rel="noreferrer"
                            className="inline-block text-[10px] font-black uppercase tracking-widest text-aura border border-aura/40 px-3 py-1.5 rounded-lg hover:bg-aura/10 transition-colors">
                            Open the live site →
                          </a>
                        </div>
                      )}

                      {/* §13 increment 3 — generate the interactive Web app (real client-side vanilla JS) */}
                      <div className="mt-3">
                        <Button onClick={generateWebApp} disabled={webappBusy} className="flex items-center gap-2 bg-slate-900 text-highlight text-[11px]">
                          {webappBusy ? <Loader2 size={13} className="animate-spin" /> : <Layers size={13} />}
                          {webappBusy ? 'Generating web app…' : 'Generate interactive Web app'}
                        </Button>
                        {webapp && (
                          <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                            <div className="flex flex-wrap items-center gap-1.5">
                              <span className="text-[9px] font-black uppercase tracking-widest text-highlight">Web app · {webapp.kind}</span>
                              {webapp.interactive && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/15 text-aura">interactive</span>}
                              {typeof webapp.quality_assurance?.quality?.qms_gate_passed === 'boolean' && (
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${webapp.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                  QMS: {webapp.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'}{webapp.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                                </span>
                              )}
                              {webapp.quality_assurance?.quality?.compliance && (
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${webapp.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                  compliance: {webapp.quality_assurance.quality.compliance.overall}
                                </span>
                              )}
                            </div>
                            <p className="text-[9px] text-slate-500">{webapp.features.join(' · ')}</p>
                            <a href={webapp.preview} target="_blank" rel="noreferrer"
                              className="inline-block text-[10px] font-black uppercase tracking-widest text-highlight border border-highlight/40 px-3 py-1.5 rounded-lg hover:bg-highlight/10 transition-colors">
                              Open the web app →
                            </a>
                          </div>
                        )}
                      </div>

                      {/* §13 increment 4 — generate the Phone app (real installable PWA) */}
                      <div className="mt-3">
                        <Button onClick={generatePhoneApp} disabled={pwaBusy} className="flex items-center gap-2 bg-slate-900 text-aura text-[11px]">
                          {pwaBusy ? <Loader2 size={13} className="animate-spin" /> : <Layers size={13} />}
                          {pwaBusy ? 'Generating phone app…' : 'Generate Phone app (PWA)'}
                        </Button>
                        {pwa && (
                          <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                            <div className="flex flex-wrap items-center gap-1.5">
                              <span className="text-[9px] font-black uppercase tracking-widest text-aura">Phone app · {pwa.kind}</span>
                              {pwa.installable && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-aura/15 text-aura">installable</span>}
                              {pwa.offline_capable && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400">offline</span>}
                              {typeof pwa.quality_assurance?.quality?.qms_gate_passed === 'boolean' && (
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${pwa.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                  QMS: {pwa.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'}{pwa.quality_assurance.quality.document_controlled ? ' · doc-controlled' : ''}
                                </span>
                              )}
                              {pwa.quality_assurance?.quality?.compliance && (
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${pwa.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                  compliance: {pwa.quality_assurance.quality.compliance.overall}
                                </span>
                              )}
                            </div>
                            <p className="text-[9px] text-slate-500">{pwa.features.join(' · ')}</p>
                            <a href={pwa.preview} target="_blank" rel="noreferrer"
                              className="inline-block text-[10px] font-black uppercase tracking-widest text-aura border border-aura/40 px-3 py-1.5 rounded-lg hover:bg-aura/10 transition-colors">
                              Open the phone app →
                            </a>
                          </div>
                        )}
                      </div>

                      {/* §17.3 — the Living Business System's on-demand Board Pack (assembled fresh, DCS-registered) */}
                      <div className="mt-3">
                        <Button onClick={generateBoardPack} disabled={packBusy} className="flex items-center gap-2 bg-slate-900 text-highlight text-[11px]">
                          {packBusy ? <Loader2 size={13} className="animate-spin" /> : <ShieldCheck size={13} />}
                          {packBusy ? 'Assembling board pack…' : 'Assemble Board Pack'}
                        </Button>
                        {pack && (
                          <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                            <div className="flex flex-wrap items-center gap-1.5">
                              <span className="text-[9px] font-black uppercase tracking-widest text-highlight">Board Pack</span>
                              <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300">{Object.keys(pack.layers).join(' · ')}</span>
                              {pack.dcs_registered && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400" title={pack.dcs_hash}>DCS-registered</span>}
                              {pack.quality_assurance?.quality?.compliance && (
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${pack.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}>
                                  compliance: {pack.quality_assurance.quality.compliance.overall}
                                </span>
                              )}
                            </div>
                            <pre className="text-[10px] text-slate-400 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto font-sans">{pack.narrative.slice(0, 1200)}</pre>
                          </div>
                        )}
                      </div>

                      {/* §17.4 Mode 3 — optional human review gates at any Concept→Commercialisation stage */}
                      <div className="mt-3">
                        <Button onClick={openGates} disabled={gatesOpen && !!gates} className="flex items-center gap-2 bg-slate-900 text-aura text-[11px]">
                          <ShieldCheck size={13} /> Human review gates (Mode 3)
                        </Button>
                        {gatesOpen && gates && (
                          <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                            <p className="text-[9px] text-slate-500">{gates.mode} — tap a stage to gate/ungate; each change is DCS-audited.</p>
                            <div className="flex flex-wrap gap-1.5">
                              {gates.lifecycle.map(stage => {
                                const st = gates.statuses.find(s => s.stage === stage.id);
                                const gated = !!st?.gated;
                                const tone = !gated ? 'bg-slate-800 text-slate-400 border-slate-700'
                                  : st?.status === 'approved' ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/40'
                                  : st?.status === 'rejected' ? 'bg-vital/15 text-vital border-vital/40'
                                  : 'bg-amber-500/15 text-amber-400 border-amber-500/40';
                                return (
                                  <div key={stage.id} className={`flex items-center gap-1 rounded-lg border px-2 py-1 ${tone}`}>
                                    <button type="button" onClick={() => toggleGate(stage.id)} title={stage.description}
                                      className="text-[9px] font-black uppercase tracking-wider">
                                      {stage.name}{gated ? ` · ${st?.status}` : ''}
                                    </button>
                                    {gated && st?.status === 'pending' && (
                                      <>
                                        <button type="button" onClick={() => decideGate(stage.id, 'approve')} className="text-emerald-400 text-[10px] font-black" title="Approve">✓</button>
                                        <button type="button" onClick={() => decideGate(stage.id, 'reject')} className="text-vital text-[10px] font-black" title="Reject">✗</button>
                                      </>
                                    )}
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const PlainText: React.FC<{ text: string }> = ({ text }) => (
  <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{text}</p>
);

const Section: React.FC<{ icon: React.ComponentType<any>; title: string; text: string; highlight?: boolean }> = ({ icon: Icon, title, text, highlight }) => (
  <div className={`p-4 rounded-xl border ${highlight ? 'border-highlight/30 bg-highlight/5' : 'border-slate-800 bg-slate-950'}`}>
    <div className="flex items-center gap-2 mb-2">
      <Icon size={13} className={highlight ? 'text-highlight' : 'text-slate-500'} />
      <p className={`text-[10px] font-black uppercase tracking-widest ${highlight ? 'text-highlight' : 'text-slate-400'}`}>{title}</p>
    </div>
    <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{text}</p>
  </div>
);
