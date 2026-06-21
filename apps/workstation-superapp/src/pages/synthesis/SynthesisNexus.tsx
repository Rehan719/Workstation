import React, { useState, useRef, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Sparkles, Loader2, CheckCircle2, AlertCircle,
  ChevronDown, ChevronUp, Brain, Eye, Zap, Layers,
  Code2, BookOpen, FlaskConical, Briefcase, Network,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface NexusEvent {
  stage: string;
  label: string;
  content: string;
  data?: {
    engines?: string[];
    phases?: string[];
    layer?: number;
    engine?: string;
    layers_completed?: number;
    cognitive_engines?: number;
    mjm_phases?: number;
    stage_num?: number;
    total?: number;
  };
}

// ── SSE stream helper ─────────────────────────────────────────────────────────

async function streamPost(
  url: string,
  body: object,
  onChunk: (ev: NexusEvent) => void,
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

const ACTIVITY_OPTIONS = [
  { id: 'auto',        label: 'Auto',        icon: Sparkles,    desc: 'AI selects the optimal engine' },
  { id: 'synthesis',   label: 'Synthesis',   icon: Briefcase,   desc: 'Business Development Process' },
  { id: 'research',    label: 'Research',    icon: FlaskConical, desc: 'Scientific Process Intelligence' },
  { id: 'authorship',  label: 'Authorship',  icon: BookOpen,    desc: 'Scholarship & Authorship' },
  { id: 'development', label: 'Development', icon: Code2,       desc: 'Design & Development' },
];

const DOMAINS = [
  'enterprise', 'science', 'law', 'care', 'education', 'career',
  'fintech', 'healthtech', 'edtech',
];

const NEXUS_LAYERS = [
  { key: 'cognitive', label: 'Cognitive Cascade',  icon: Brain,       desc: '6 cognitive engines: Inkashaf → Samajh → Soch → Aqal → Hoshiyari → Iman' },
  { key: 'mjm',       label: 'MJM Assessment',     icon: Eye,         desc: 'Mushahida → Jaiza → Muaina (Observe · Analyse · Act)' },
  { key: 'engine',    label: 'Primary Engine',      icon: Network,     desc: 'Selected intelligence pipeline — enriched by cognitive + MJM' },
  { key: 'synthesis', label: 'Nexus Synthesis',     icon: Layers,      desc: 'Apex integration — unified intelligence from all layers' },
];

// Stage events that belong to the "primary engine" layer (not cognitive/MJM/nexus)
const ENGINE_META_STAGES = new Set([
  'init', 'cognitive_start', 'cognitive_complete',
  'mjm_start', 'mjm_complete', 'routing', 'engine_selected',
  'synthesis_start', 'nexus_complete',
]);

function layerFromStage(stage: string): 'cognitive' | 'mjm' | 'engine' | 'synthesis' | null {
  if (stage === 'cognitive_complete') return 'cognitive';
  if (stage === 'mjm_complete') return 'mjm';
  if (stage === 'nexus_complete') return 'synthesis';
  if (!ENGINE_META_STAGES.has(stage) && !stage.endsWith('_start')) return 'engine';
  return null;
}

function engineIcon(engineId: string) {
  if (engineId === 'apie') return BookOpen;
  if (engineId === 'ddpie') return Code2;
  if (engineId === 'spi') return FlaskConical;
  return Briefcase;
}

// ── Component ─────────────────────────────────────────────────────────────────

export const SynthesisNexus: React.FC = () => {
  const [challenge, setChallenge] = useState('');
  const [domain, setDomain] = useState('enterprise');
  const [activity, setActivity] = useState('auto');
  const [running, setRunning] = useState(false);
  const [events, setEvents] = useState<NexusEvent[]>([]);
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState<string | null>(null);
  const feedRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (feedRef.current) feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [events]);

  const run = async () => {
    if (!challenge.trim()) return;
    setRunning(true);
    setEvents([]);
    setError('');
    setExpanded(null);

    await streamPost(
      '/api/v1/intelligence/nexus',
      { challenge, domain, activity },
      ev => setEvents(prev => [...prev, ev]),
      () => setRunning(false),
      e => { setError(e); setRunning(false); },
    );
  };

  // Layer completion tracking
  const cognitiveEvent = events.find(e => e.stage === 'cognitive_complete');
  const mjmEvent = events.find(e => e.stage === 'mjm_complete');
  const engineSelectedEvent = events.find(e => e.stage === 'engine_selected');
  const nexusCompleteEvent = events.find(e => e.stage === 'nexus_complete');
  const selectedEngine = engineSelectedEvent?.data?.engine ?? '';

  const engineStageEvents = events.filter(e => layerFromStage(e.stage) === 'engine');

  const layersComplete = [cognitiveEvent, mjmEvent, engineStageEvents.length > 0, nexusCompleteEvent].filter(Boolean).length;

  return (
    <div className="space-y-10 pb-24">
      {/* Header */}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">
          Intelligence Engine · Nexus
        </p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Synthesis Nexus
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Four-layer autonomous intelligence. The Nexus chains all engines synergistically:
          Cognitive Cascade → MJM Meta-Assessment → AI-selected primary engine → Apex Synthesis.
          Every layer enriches the next.
        </p>
      </header>

      {/* Layer tracker */}
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-5">
          4-Layer Intelligence Architecture
        </h3>
        <div className="grid grid-cols-2 @[640px]:grid-cols-4 gap-3">
          {NEXUS_LAYERS.map(({ key, label, icon: Icon, desc }, i) => {
            const done =
              (key === 'cognitive' && !!cognitiveEvent) ||
              (key === 'mjm' && !!mjmEvent) ||
              (key === 'engine' && engineStageEvents.length > 0) ||
              (key === 'synthesis' && !!nexusCompleteEvent);
            const active =
              running && !done &&
              ((key === 'cognitive' && !cognitiveEvent) ||
               (key === 'mjm' && !!cognitiveEvent && !mjmEvent) ||
               (key === 'engine' && !!mjmEvent && !nexusCompleteEvent && engineStageEvents.length === 0) ||
               (key === 'synthesis' && !!mjmEvent && engineStageEvents.length > 0 && !nexusCompleteEvent));

            return (
              <div
                key={key}
                className={`p-4 rounded-2xl border transition-all ${
                  done
                    ? 'bg-highlight/10 border-highlight/20'
                    : active
                    ? 'bg-aura/10 border-aura/30 animate-pulse'
                    : 'bg-slate-900 border-slate-800'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                    done ? 'bg-highlight/20' : active ? 'bg-aura/20' : 'bg-slate-800'
                  }`}>
                    {done
                      ? <CheckCircle2 size={12} className="text-highlight" />
                      : active
                      ? <Loader2 size={12} className="text-aura animate-spin" />
                      : <Icon size={12} className="text-slate-500" />}
                  </div>
                  <span className={`text-[9px] font-black uppercase tracking-widest ${
                    done ? 'text-highlight' : active ? 'text-aura' : 'text-slate-600'
                  }`}>
                    Layer {i + 1}
                  </span>
                </div>
                <p className={`text-[11px] font-black mb-1 ${done ? 'text-white' : 'text-slate-400'}`}>
                  {label}
                </p>
                <p className="text-[9px] text-slate-600 leading-relaxed">{desc}</p>
              </div>
            );
          })}
        </div>

        {running && (
          <div className="mt-4">
            <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-highlight to-aura transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, (layersComplete / 4) * 100)}%` }}
              />
            </div>
            <p className="text-[9px] font-bold text-slate-500 mt-1.5 uppercase tracking-widest">
              {layersComplete} of 4 layers complete
            </p>
          </div>
        )}
      </Card>

      {/* Input form */}
      <Card className="p-8 space-y-7">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            Challenge / Goal / System
          </label>
          <textarea
            value={challenge}
            onChange={e => setChallenge(e.target.value)}
            placeholder="Describe what you want to synthesise, design, research, or build. The Nexus will autonomously select and chain the right engines..."
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none"
          />
        </div>

        {/* Activity selector */}
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-3 block">
            Activity Mode
          </label>
          <div className="grid grid-cols-2 @[440px]:grid-cols-5 gap-2">
            {ACTIVITY_OPTIONS.map(({ id, label, icon: Icon, desc }) => (
              <button
                key={id}
                type="button"
                onClick={() => setActivity(id)}
                className={`p-3 rounded-xl border text-left transition-all ${
                  activity === id
                    ? 'bg-highlight/15 border-highlight/40'
                    : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                }`}
              >
                <Icon size={14} className={activity === id ? 'text-highlight mb-1.5' : 'text-slate-500 mb-1.5'} />
                <p className={`text-[10px] font-black uppercase tracking-widest ${
                  activity === id ? 'text-highlight' : 'text-slate-400'
                }`}>
                  {label}
                </p>
                <p className="text-[9px] text-slate-600 mt-0.5 leading-tight">{desc}</p>
              </button>
            ))}
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

        <div className="flex items-center gap-4 pt-2">
          <Button
            onClick={run}
            disabled={running || !challenge.trim()}
            className="flex items-center gap-2 bg-highlight text-sovereign"
          >
            {running
              ? <Loader2 size={16} className="animate-spin" />
              : <Sparkles size={16} />}
            {running ? 'Nexus Running...' : 'Activate Synthesis Nexus'}
          </Button>
          {error && (
            <p className="text-vital text-xs font-bold flex items-center gap-2">
              <AlertCircle size={14} /> {error}
            </p>
          )}
        </div>
      </Card>

      {/* Live event feed */}
      {events.length > 0 && (
        <div className="space-y-4" ref={feedRef}>

          {/* Layer 1: Cognitive Cascade */}
          {cognitiveEvent && (
            <Card className="p-0 overflow-hidden border-slate-700/50">
              <button
                type="button"
                onClick={() => setExpanded(expanded === 'cognitive' ? null : 'cognitive')}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-highlight/10 flex items-center justify-center shrink-0">
                    <Brain size={14} className="text-highlight" />
                  </div>
                  <div>
                    <p className="font-black text-white text-sm">Cognitive Cascade</p>
                    <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                      Layer 1 · 6 cognitive engines
                    </p>
                  </div>
                  <CheckCircle2 size={14} className="text-emerald-400 ml-2 shrink-0" />
                </div>
                {expanded === 'cognitive'
                  ? <ChevronUp size={14} className="text-slate-500 shrink-0" />
                  : <ChevronDown size={14} className="text-slate-500 shrink-0" />}
              </button>
              {expanded === 'cognitive' && (
                <div className="px-5 pb-6 border-t border-slate-800/50">
                  <div className="flex flex-wrap gap-1.5 my-3">
                    {(cognitiveEvent.data?.engines ?? ['Inkashaf','Samajh','Soch','Aqal','Hoshiyari','Iman']).map(eng => (
                      <span key={eng} className="px-2 py-0.5 rounded-md bg-highlight/10 text-highlight text-[9px] font-black uppercase tracking-wider">
                        {eng}
                      </span>
                    ))}
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                    {cognitiveEvent.content}
                  </p>
                </div>
              )}
            </Card>
          )}

          {/* Layer 2: MJM */}
          {mjmEvent && (
            <Card className="p-0 overflow-hidden border-slate-700/50">
              <button
                type="button"
                onClick={() => setExpanded(expanded === 'mjm' ? null : 'mjm')}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-aura/10 flex items-center justify-center shrink-0">
                    <Eye size={14} className="text-aura" />
                  </div>
                  <div>
                    <p className="font-black text-white text-sm">MJM Meta-Assessment</p>
                    <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                      Layer 2 · Mushahida · Jaiza · Muaina
                    </p>
                  </div>
                  <CheckCircle2 size={14} className="text-emerald-400 ml-2 shrink-0" />
                </div>
                {expanded === 'mjm'
                  ? <ChevronUp size={14} className="text-slate-500 shrink-0" />
                  : <ChevronDown size={14} className="text-slate-500 shrink-0" />}
              </button>
              {expanded === 'mjm' && (
                <div className="px-5 pb-6 border-t border-slate-800/50">
                  <div className="flex flex-wrap gap-1.5 my-3">
                    {(mjmEvent.data?.phases ?? ['Mushahida','Jaiza','Muaina']).map(ph => (
                      <span key={ph} className="px-2 py-0.5 rounded-md bg-aura/10 text-aura text-[9px] font-black uppercase tracking-wider">
                        {ph}
                      </span>
                    ))}
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                    {mjmEvent.content}
                  </p>
                </div>
              )}
            </Card>
          )}

          {/* Engine selection banner */}
          {engineSelectedEvent && (
            <div className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800">
              {React.createElement(engineIcon(selectedEngine), { size: 12, className: 'text-highlight shrink-0' })}
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-400">
                Routing to primary engine:
                <span className="text-highlight ml-2">{selectedEngine.toUpperCase()}</span>
              </p>
            </div>
          )}

          {/* Layer 3: Primary engine stages */}
          {engineStageEvents.length > 0 && (
            <div className="space-y-2">
              <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 px-1">
                Layer 3 · {selectedEngine.toUpperCase()} Pipeline — {engineStageEvents.length} stage{engineStageEvents.length !== 1 ? 's' : ''} complete
              </p>
              {engineStageEvents.map((ev, i) => {
                const EngIcon = engineIcon(selectedEngine);
                const evKey = `engine-${i}`;
                return (
                  <Card key={evKey} className="p-0 overflow-hidden border-slate-800/80">
                    <button
                      type="button"
                      onClick={() => setExpanded(expanded === evKey ? null : evKey)}
                      className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-7 h-7 rounded-xl bg-slate-800 flex items-center justify-center shrink-0">
                          <EngIcon size={12} className="text-slate-400" />
                        </div>
                        <div>
                          <p className="font-black text-white text-sm">{ev.label}</p>
                          <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                            Stage {i + 1}
                            {ev.data?.total ? ` of ${ev.data.total}` : ''} · {selectedEngine.toUpperCase()}
                          </p>
                        </div>
                        <CheckCircle2 size={12} className="text-emerald-400 ml-2 shrink-0" />
                      </div>
                      {expanded === evKey
                        ? <ChevronUp size={14} className="text-slate-500 shrink-0" />
                        : <ChevronDown size={14} className="text-slate-500 shrink-0" />}
                    </button>
                    {expanded === evKey && (
                      <div className="px-5 pb-5 border-t border-slate-800/50">
                        <p className="mt-4 text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                          {ev.content}
                        </p>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>
          )}

          {/* Layer 4: Nexus Synthesis */}
          {nexusCompleteEvent && (
            <Card className="p-0 overflow-hidden border-highlight/30 bg-highlight/5">
              <button
                type="button"
                onClick={() => setExpanded(expanded === 'nexus' ? null : 'nexus')}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-highlight/5 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-highlight/20 flex items-center justify-center shrink-0">
                    <Layers size={14} className="text-highlight" />
                  </div>
                  <div>
                    <p className="font-black text-highlight text-sm uppercase tracking-wide">Nexus Synthesis</p>
                    <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                      Layer 4 · Apex integration ·{' '}
                      {nexusCompleteEvent.data?.layers_completed ?? 4} layers ·{' '}
                      {nexusCompleteEvent.data?.cognitive_engines ?? 6} cognitive engines
                    </p>
                  </div>
                  <Zap size={14} className="text-highlight ml-2 shrink-0" />
                </div>
                {expanded === 'nexus'
                  ? <ChevronUp size={14} className="text-slate-500 shrink-0" />
                  : <ChevronDown size={14} className="text-slate-500 shrink-0" />}
              </button>
              {expanded === 'nexus' && (
                <div className="px-5 pb-6 border-t border-highlight/20">
                  <p className="mt-4 text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
                    {nexusCompleteEvent.content}
                  </p>
                </div>
              )}
            </Card>
          )}

          {running && (
            <div className="flex items-center gap-2 p-4 text-slate-500">
              <Loader2 size={14} className="animate-spin" />
              <span className="text-xs font-bold">Processing next layer...</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
