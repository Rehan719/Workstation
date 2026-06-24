import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
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
  engines_used: string[];
  deliverable: string;
  status: string;
}

const REALMS = ['enterprise', 'learning', 'developing', 'scholarship'];
const DOMAINS = ['enterprise', 'science', 'law', 'care', 'education', 'career', 'fintech', 'healthtech', 'edtech'];

// ── Component ─────────────────────────────────────────────────────────────────

export const GenesisJourney: React.FC = () => {
  const navigate = useNavigate();
  const [problem, setProblem] = useState('');
  const [domain, setDomain] = useState('enterprise');
  const [realm, setRealm] = useState('enterprise');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<JourneyResult | null>(null);
  const [open, setOpen] = useState<string>('phase1');
  const [establishing, setEstablishing] = useState(false);
  const [vsb, setVsb] = useState<{ vsb_id: string; name: string; dashboard: string; governance?: any } | null>(null);

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
          IDBO · Sovereign Journey
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
