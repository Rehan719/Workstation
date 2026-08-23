import React, { useState, useRef, useEffect } from 'react';
import { DOMAINS as CANON_DOMAINS } from '../lib/taxonomy';
import { Card, Button } from '@workstation/ui';
import {
  TrendingUp, Microscope, Loader2, CheckCircle2, Circle,
  AlertCircle, Brain, Zap, ChevronDown, ChevronUp,
} from 'lucide-react';

// ── SSE helper ────────────────────────────────────────────────────────────────

interface IntelEvent {
  stage: string;
  label: string;
  content: string;
  stage_number?: number;
  total_stages?: number;
}

async function streamPost(
  url: string,
  body: object,
  onChunk: (ev: IntelEvent) => void,
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

// ── Stage display ─────────────────────────────────────────────────────────────

const BDP_STAGES = [
  'Market Analysis', 'Value Proposition', 'Customer Discovery',
  'Business Model', 'Go-to-Market', 'Financial Modelling',
  'Risk & Resilience', 'Executive Summary',
];

const SPI_STAGES = [
  'Problem Formulation', 'Literature Synthesis', 'Hypothesis Generation',
  'Methodology Design', 'Data Strategy', 'Validation Plan',
  'Impact Assessment', 'Dissemination Plan',
];

// ── Component ─────────────────────────────────────────────────────────────────

export const IntelligenceLab: React.FC = () => {
  const [mode, setMode] = useState<'bdp' | 'spi'>('bdp');
  const [input, setInput] = useState('');
  const [domain, setDomain] = useState('enterprise');
  // §7 user design control — reconfigure the engine's behaviour (honored at run time)
  const [rigor, setRigor] = useState<'standard' | 'rigorous' | 'exhaustive'>('standard');
  const [focus, setFocus] = useState('');
  const [running, setRunning] = useState(false);
  const [events, setEvents] = useState<IntelEvent[]>([]);
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);
  const feedRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (feedRef.current) feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [events]);

  const isBDP = mode === 'bdp';
  const stageNames = isBDP ? BDP_STAGES : SPI_STAGES;

  const run = async () => {
    if (!input.trim()) return;
    setRunning(true);
    setEvents([]);
    setError('');
    setExpanded(null);

    const url = `/api/v1/intelligence/${mode}`;
    const body = { challenge: input, domain, rigor, focus };

    await streamPost(url, body,
      ev => setEvents(prev => [...prev, ev]),
      () => setRunning(false),
      e => { setError(e); setRunning(false); },
    );
  };

  // Filter out init/prime events for the results view
  const stageEvents = events.filter(
    ev => !['init', 'cognitive_prime', 'cognitive_complete'].includes(ev.stage)
      && ev.stage !== 'complete'
  );
  const completeEvent = events.find(ev => ev.stage === 'complete');
  const currentStageNum = stageEvents.length;
  const progress = Math.min(100, Math.round((currentStageNum / 8) * 100));

  const DOMAINS = ['enterprise', ...CANON_DOMAINS];   // §17.1 (W321)

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">
          Intelligence Engines
        </p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Intelligence Lab
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-xl leading-relaxed">
          {isBDP
            ? 'Business Development Process: 8-stage structured methodology powered by Nine Cognitive Engines + MJM.'
            : 'Scientific Process Intelligence: research methodology from hypothesis to dissemination.'}
        </p>
      </header>

      {/* Mode toggle */}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => { setMode('bdp'); setEvents([]); setError(''); }}
          className={`flex items-center gap-2 px-5 py-3 rounded-2xl font-black text-sm uppercase tracking-wide transition-all ${
            isBDP
              ? 'bg-highlight/20 text-highlight border border-highlight/40'
              : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
          }`}
        >
          <TrendingUp size={16} />
          Business Dev (BDP)
        </button>
        <button
          type="button"
          onClick={() => { setMode('spi'); setEvents([]); setError(''); }}
          className={`flex items-center gap-2 px-5 py-3 rounded-2xl font-black text-sm uppercase tracking-wide transition-all ${
            !isBDP
              ? 'bg-highlight/20 text-highlight border border-highlight/40'
              : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
          }`}
        >
          <Microscope size={16} />
          Science (SPI)
        </button>
      </div>

      {/* Stage tracker */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500">
            8-Stage Pipeline
          </h3>
          {running && (
            <span className="text-[10px] font-black text-highlight uppercase tracking-widest">
              {progress}% Complete
            </span>
          )}
        </div>
        <div className="flex gap-2 flex-wrap">
          {stageNames.map((name, i) => {
            const done = i < currentStageNum;
            const active = i === currentStageNum && running;
            return (
              <div
                key={name}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-wider border transition-all ${
                  done
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                    : active
                    ? 'bg-highlight/10 text-highlight border-highlight/30 animate-pulse'
                    : 'bg-slate-900 text-slate-600 border-slate-800'
                }`}
              >
                {done ? <CheckCircle2 size={10} /> : active ? <Loader2 size={10} className="animate-spin" /> : <Circle size={10} />}
                {name}
              </div>
            );
          })}
        </div>
      </Card>

      {/* Input */}
      <Card className="p-8 space-y-6">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            {isBDP ? 'Business Challenge / Opportunity' : 'Research Question / Scientific Problem'}
          </label>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder={
              isBDP
                ? 'Describe your business challenge, opportunity, or venture concept...'
                : 'State your research question, hypothesis to investigate, or scientific problem...'
            }
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none"
          />
        </div>

        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Domain</label>
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

        {/* §7 user design control — reconfigure the engine before running */}
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-4">
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
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Focus lens <span className="text-slate-600 normal-case font-bold">(optional)</span></label>
            <input value={focus} onChange={e => setFocus(e.target.value)}
              placeholder="e.g. unit economics + compliance"
              className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-[11px] text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
          </div>
        </div>

        <div className="flex items-center gap-4 pt-2">
          <Button
            onClick={run}
            disabled={running || !input.trim()}
            className="flex items-center gap-2"
          >
            {running ? <Loader2 size={16} className="animate-spin" /> : <Brain size={16} />}
            {running ? 'Running Intelligence Pipeline...' : `Run ${isBDP ? 'BDP' : 'SPI'} Engine`}
          </Button>
          {error && (
            <p className="text-vital text-xs font-bold flex items-center gap-2">
              <AlertCircle size={14} /> {error}
            </p>
          )}
        </div>
      </Card>

      {/* Results: accordion per stage */}
      {stageEvents.length > 0 && (
        <div className="space-y-3" ref={feedRef}>
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">
            Analysis Results
          </h3>
          {stageEvents.map((ev, i) => (
            <Card key={i} className="p-0 overflow-hidden">
              <button
                type="button"
                onClick={() => setExpanded(expanded === i ? null : i)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
              >
                <div className="flex items-center gap-3">
                  <CheckCircle2 size={14} className="text-emerald-400 shrink-0" />
                  <div>
                    <p className="font-black text-white text-sm">{ev.label}</p>
                    <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                      Stage {i + 1} of 8
                    </p>
                  </div>
                </div>
                {expanded === i ? (
                  <ChevronUp size={14} className="text-slate-500 shrink-0" />
                ) : (
                  <ChevronDown size={14} className="text-slate-500 shrink-0" />
                )}
              </button>
              {expanded === i && (
                <div className="px-5 pb-5 border-t border-slate-800/50">
                  <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap mt-4">
                    {ev.content}
                  </p>
                </div>
              )}
            </Card>
          ))}

          {/* Executive summary / complete */}
          {completeEvent && (
            <Card className="p-6 border-aura/20 bg-aura/5">
              <div className="flex items-center gap-3 mb-4">
                <Zap size={18} className="text-aura" />
                <h3 className="font-black text-aura uppercase tracking-widest text-sm">
                  {completeEvent.label}
                </h3>
              </div>
              <p className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
                {completeEvent.content}
              </p>
            </Card>
          )}

          {/* Still streaming */}
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
