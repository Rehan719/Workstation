import React, { useState, useRef, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Code2, Loader2, CheckCircle2, AlertCircle,
  ChevronDown, ChevronUp, Layout, Database, Lock,
  Map, TestTube2, Rocket, ShieldCheck, FileCode2, Zap, ListChecks,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface DDEvent {
  stage: string;
  label: string;
  content: string;
  data?: { stage_num?: number; total?: number };
}

// ── SSE stream helper ─────────────────────────────────────────────────────────

async function streamPost(
  url: string,
  body: object,
  onChunk: (ev: DDEvent) => void,
  onDone: () => void,
  onError: (e: string) => void,
) {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) { onError(`HTTP ${res.status}`); return; }
    const reader = res.body!.getReader();
    const dec = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop()!;
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const raw = line.slice(6).trim();
          if (raw === '[DONE]') continue;
          try { onChunk(JSON.parse(raw)); } catch {}
        }
      }
    }
    onDone();
  } catch (e: any) {
    onError(e?.message ?? String(e));
  }
}

// ── Constants ─────────────────────────────────────────────────────────────────

const DDPIE_STAGES = [
  { key: 'requirements_intelligence', label: 'Requirements',         icon: ListChecks },
  { key: 'architecture_design',       label: 'Architecture',         icon: Layout },
  { key: 'domain_modelling',          label: 'Domain Modelling',     icon: Database },
  { key: 'api_contract',              label: 'API Contract',         icon: FileCode2 },
  { key: 'security_architecture',     label: 'Security',             icon: Lock },
  { key: 'implementation_blueprint',  label: 'Implementation',       icon: Map },
  { key: 'test_strategy',             label: 'Test Strategy',        icon: TestTube2 },
  { key: 'devops_pipeline',           label: 'DevOps Pipeline',      icon: Rocket },
  { key: 'technical_review',          label: 'Technical Review',     icon: ShieldCheck },
];

const SCALES = ['startup', 'scaleup', 'enterprise'];
const DEPLOYMENT_TARGETS = ['cloud', 'on-prem', 'hybrid', 'serverless', 'edge'];
const DOMAINS = ['enterprise', 'science', 'law', 'care', 'education', 'career', 'fintech', 'healthtech', 'edtech'];
const PRESET_STACKS = [
  'Python / FastAPI / React / PostgreSQL',
  'Node.js / Express / Next.js / MongoDB',
  'Java / Spring Boot / Angular / MySQL',
  'Go / Gin / React / PostgreSQL',
  '.NET / C# / Blazor / SQL Server',
  'Python / Django / Vue.js / Redis',
];

// ── Component ─────────────────────────────────────────────────────────────────

export const DesignDevEngine: React.FC = () => {
  const [system, setSystem] = useState('');
  const [domain, setDomain] = useState('enterprise');
  const [techStack, setTechStack] = useState('Python / FastAPI / React / PostgreSQL');
  const [scale, setScale] = useState('startup');
  const [deploymentTarget, setDeploymentTarget] = useState('cloud');
  const [rigor, setRigor] = useState<'standard' | 'rigorous' | 'exhaustive'>('standard');   // §7 user design control
  const [running, setRunning] = useState(false);
  const [events, setEvents] = useState<DDEvent[]>([]);
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);
  const [customStack, setCustomStack] = useState('');
  const feedRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (feedRef.current) feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [events]);

  const effectiveStack = customStack.trim() || techStack;

  const run = async () => {
    if (!system.trim()) return;
    setRunning(true);
    setEvents([]);
    setError('');
    setExpanded(null);

    await streamPost(
      '/api/v1/intelligence/design-dev',
      { system, domain, tech_stack: effectiveStack, scale, deployment_target: deploymentTarget, rigor },
      ev => setEvents(prev => [...prev, ev]),
      () => setRunning(false),
      e => { setError(e); setRunning(false); },
    );
  };

  const stageEvents = events.filter(
    ev => !['init', 'complete'].includes(ev.stage) && !ev.stage.endsWith('_start'),
  );
  const completeEvent = events.find(ev => ev.stage === 'complete');
  const currentStageNum = stageEvents.length;
  const progress = Math.min(100, Math.round((currentStageNum / DDPIE_STAGES.length) * 100));

  return (
    <div className="space-y-10 pb-24">
      {/* Header */}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">
          Intelligence Engine · DDPIE
        </p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Design & Dev Intelligence
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          9-stage Design & Development pipeline — from requirements engineering through architecture,
          domain modelling, API contract, security, implementation blueprint, test strategy, DevOps,
          and technical review. Powered by Nine Cognitive Engines + MJM.
        </p>
      </header>

      {/* Stage tracker */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500">
            9-Stage Design & Development Pipeline
          </h3>
          {running && (
            <span className="text-[10px] font-black text-highlight uppercase tracking-widest animate-pulse">
              {progress}% Complete
            </span>
          )}
        </div>
        <div className="flex gap-2 flex-wrap">
          {DDPIE_STAGES.map(({ key, label, icon: Icon }, i) => {
            const done = i < currentStageNum;
            const active = i === currentStageNum && running;
            return (
              <div
                key={key}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-wider border transition-all ${
                  done
                    ? 'bg-highlight/10 text-highlight border-highlight/20'
                    : active
                    ? 'bg-aura/10 text-aura border-aura/30 animate-pulse'
                    : 'bg-slate-900 text-slate-600 border-slate-800'
                }`}
              >
                {done
                  ? <CheckCircle2 size={10} />
                  : active
                  ? <Loader2 size={10} className="animate-spin" />
                  : <Icon size={10} />}
                {label}
              </div>
            );
          })}
        </div>
        {running && (
          <div className="mt-4">
            <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
              <div
                className="h-full bg-highlight transition-all duration-700 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </Card>

      {/* Input form */}
      <Card className="p-8 space-y-7">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            System / Product Description
          </label>
          <textarea
            value={system}
            onChange={e => setSystem(e.target.value)}
            placeholder="Describe the system or product to design and build — what it does, who it serves, and its key capabilities..."
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none font-mono"
          />
        </div>

        {/* Scale + Deployment */}
        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-6">
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Scale
            </label>
            <div className="flex gap-2">
              {SCALES.map(s => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setScale(s)}
                  className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
                    scale === s
                      ? 'bg-highlight/20 text-highlight border border-highlight/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Deployment Target
            </label>
            <div className="flex flex-wrap gap-2">
              {DEPLOYMENT_TARGETS.map(dt => (
                <button
                  key={dt}
                  type="button"
                  onClick={() => setDeploymentTarget(dt)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    deploymentTarget === dt
                      ? 'bg-highlight/20 text-highlight border border-highlight/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {dt}
                </button>
              ))}
            </div>
          </div>
          {/* §7 user design control — rigor (honored at run time) */}
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Rigor</label>
            <div className="flex flex-wrap gap-2">
              {(['standard', 'rigorous', 'exhaustive'] as const).map(r => (
                <button key={r} type="button" onClick={() => setRigor(r)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    rigor === r ? 'bg-highlight/20 text-highlight border border-highlight/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}>
                  {r}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Domain */}
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            Domain
          </label>
          <div className="flex flex-wrap gap-2">
            {DOMAINS.map(d => (
              <button
                key={d}
                type="button"
                onClick={() => setDomain(d)}
                className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                  domain === d
                    ? 'bg-highlight/20 text-highlight border border-highlight/40'
                    : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Tech stack */}
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            Technology Stack
          </label>
          <div className="flex flex-wrap gap-2 mb-3">
            {PRESET_STACKS.map(ps => (
              <button
                key={ps}
                type="button"
                onClick={() => { setTechStack(ps); setCustomStack(''); }}
                className={`px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all font-mono ${
                  techStack === ps && !customStack
                    ? 'bg-highlight/20 text-highlight border border-highlight/40'
                    : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                }`}
              >
                {ps}
              </button>
            ))}
          </div>
          <input
            value={customStack}
            onChange={e => setCustomStack(e.target.value)}
            placeholder="Or enter custom stack: e.g. Rust / Axum / SvelteKit / CockroachDB"
            className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 font-mono"
          />
          {effectiveStack && (
            <p className="text-[9px] font-mono text-highlight mt-1.5">
              → {effectiveStack}
            </p>
          )}
        </div>

        <div className="flex items-center gap-4 pt-2">
          <Button
            onClick={run}
            disabled={running || !system.trim()}
            className="flex items-center gap-2 bg-highlight text-sovereign"
          >
            {running ? <Loader2 size={16} className="animate-spin" /> : <Code2 size={16} />}
            {running ? 'Running Design Pipeline...' : 'Run DDPIE — 9 Stages'}
          </Button>
          {error && (
            <p className="text-vital text-xs font-bold flex items-center gap-2">
              <AlertCircle size={14} /> {error}
            </p>
          )}
        </div>
      </Card>

      {/* Results */}
      {stageEvents.length > 0 && (
        <div className="space-y-3" ref={feedRef}>
          <div className="flex items-center justify-between">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">
              Pipeline Output — {stageEvents.length} of {DDPIE_STAGES.length} Stages
            </h3>
            <div className="flex items-center gap-3 text-[9px] font-mono text-slate-600">
              <span>{effectiveStack}</span>
              <span>·</span>
              <span className="uppercase">{scale}</span>
              <span>·</span>
              <span className="uppercase">{deploymentTarget}</span>
            </div>
          </div>

          {stageEvents.map((ev, i) => {
            const stageInfo = DDPIE_STAGES[i];
            const StageIcon = stageInfo?.icon ?? Code2;
            return (
              <Card key={i} className="p-0 overflow-hidden border-slate-800/80">
                <button
                  type="button"
                  onClick={() => setExpanded(expanded === i ? null : i)}
                  className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-highlight/10 flex items-center justify-center shrink-0">
                      <StageIcon size={14} className="text-highlight" />
                    </div>
                    <div>
                      <p className="font-black text-white text-sm">{ev.label}</p>
                      <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                        Stage {i + 1} of {DDPIE_STAGES.length}
                      </p>
                    </div>
                    <CheckCircle2 size={14} className="text-emerald-400 ml-2 shrink-0" />
                  </div>
                  {expanded === i
                    ? <ChevronUp size={14} className="text-slate-500 shrink-0" />
                    : <ChevronDown size={14} className="text-slate-500 shrink-0" />}
                </button>
                {expanded === i && (
                  <div className="px-5 pb-6 border-t border-slate-800/50">
                    <div className="mt-4">
                      <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap font-mono text-[12px]">
                        {ev.content}
                      </p>
                    </div>
                  </div>
                )}
              </Card>
            );
          })}

          {/* Complete banner */}
          {completeEvent && (
            <Card className="p-6 border-highlight/30 bg-highlight/5">
              <div className="flex items-center gap-3 mb-3">
                <Zap size={18} className="text-highlight" />
                <h3 className="font-black text-highlight uppercase tracking-widest text-sm">
                  Design & Development Pipeline Complete
                </h3>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                {completeEvent.content}
              </p>
              <div className="flex items-center gap-3 mt-3 text-[9px] font-mono text-slate-500">
                <span>Stack: {(completeEvent.data as any)?.tech_stack ?? effectiveStack}</span>
                <span>·</span>
                <span>Scale: {(completeEvent.data as any)?.scale ?? scale}</span>
                <span>·</span>
                <span>Stages: {(completeEvent.data as any)?.stages_completed ?? DDPIE_STAGES.length}</span>
              </div>
            </Card>
          )}

          {running && (
            <div className="flex items-center gap-2 p-4 text-slate-500">
              <Loader2 size={14} className="animate-spin" />
              <span className="text-xs font-bold">Generating next stage...</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
