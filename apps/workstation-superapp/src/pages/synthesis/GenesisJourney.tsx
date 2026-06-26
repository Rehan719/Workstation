import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
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
  phase_2_design_development: string;
  phase_3_commercialisation: string;
  governance: { status: string; checkpoint: string | null; node: string };
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

const REALMS = ['enterprise', 'learning', 'developing', 'scholarship'];
// §17.1 — the six canonical Domains (matches the Domains section hubs). Realm (who you are) is separate.
const DOMAINS = ['religion', 'science', 'education', 'law', 'employment', 'care'];

// ── Component ─────────────────────────────────────────────────────────────────

export const GenesisJourney: React.FC = () => {
  const navigate = useNavigate();
  const [sp] = useSearchParams();   // seedable from a domain tool (offering 1 -> offering 2, §3A)
  const [problem, setProblem] = useState(() => sp.get('problem') || '');
  const [domain, setDomain] = useState(() => { const d = sp.get('domain') || 'science'; return DOMAINS.includes(d) ? d : 'science'; });
  const [realm, setRealm] = useState(() => { const r = sp.get('realm') || 'enterprise'; return REALMS.includes(r) ? r : 'enterprise'; });
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<JourneyResult | null>(null);
  const [open, setOpen] = useState<string>('phase1');
  const [establishing, setEstablishing] = useState(false);
  const [vsb, setVsb] = useState<{ vsb_id: string; name: string; dashboard: string; governance?: any } | null>(null);
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
        body: JSON.stringify({ problem, domain, realm }),
      });
      if (!res.ok) { setError(`HTTP ${res.status}`); setRunning(false); return; }
      setResult(await res.json());
    } catch (e: any) {
      setError(e?.message ?? String(e));
    }
    setRunning(false);
  };

  const establish = async () => {
    if (!result) return;
    setEstablishing(true);
    try {
      const res = await fetch('/api/v1/genesis/establish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem, domain, realm,
          concept: result.phase_1_conceptualisation.concept,
          design: result.phase_2_design_development,
          commercialisation: result.phase_3_commercialisation,
        }),
      });
      setVsb(await res.json());
    } catch { /* surfaced by absence of vsb */ }
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

      {/* Phase rail */}
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-5">3-Phase Concept → Commercialisation Cascade</h3>
        <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-3">
          {[
            { icon: Lightbulb, label: 'Conceptualisation', desc: 'Cognitive cascade + MJM → optimal concept' },
            { icon: Layers, label: 'Design & Development', desc: 'Architecture, components, MVP scope' },
            { icon: Rocket, label: 'Commercialisation', desc: 'GTM + revenue + living VSB blueprint' },
          ].map(({ icon: Icon, label, desc }, i) => {
            const done = !!result;
            return (
              <div key={label} className={`p-4 rounded-2xl border transition-all ${done ? 'bg-highlight/10 border-highlight/20' : running ? 'bg-aura/10 border-aura/30 animate-pulse' : 'bg-slate-900 border-slate-800'}`}>
                <div className="flex items-center gap-2 mb-2">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center ${done ? 'bg-highlight/20' : 'bg-slate-800'}`}>
                    <Icon size={12} className={done ? 'text-highlight' : 'text-slate-500'} />
                  </div>
                  <span className={`text-[9px] font-black uppercase tracking-widest ${done ? 'text-highlight' : 'text-slate-600'}`}>Phase {i + 1}</span>
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
        <div className="flex items-center gap-4 pt-2">
          <Button onClick={run} disabled={running || !problem.trim()} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {running ? 'Running Sovereign Journey…' : 'Launch Genesis Journey'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {/* Result */}
      {result && (
        <div className="space-y-4">
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
                <Button onClick={establish} disabled={establishing} className="flex items-center gap-2 bg-highlight text-sovereign">
                  {establishing ? <Loader2 size={16} className="animate-spin" /> : <Rocket size={16} />}
                  {establishing ? 'Establishing VSB…' : 'Establish VSB IDBO Entity'}
                </Button>
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
                    <button type="button" onClick={() => navigate('/vsb-cockpit')}
                      className="text-[10px] font-black uppercase tracking-widest text-aura border border-aura/40 px-3 py-1.5 rounded-lg hover:bg-aura/10 transition-colors">
                      VSB Cockpit →
                    </button>
                  </div>
                  <p className="text-[9px] text-slate-500 mt-2 leading-relaxed">
                    Its plan already opens with an Executive Summary · Concept · Vision, seeded from this journey.
                  </p>

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
