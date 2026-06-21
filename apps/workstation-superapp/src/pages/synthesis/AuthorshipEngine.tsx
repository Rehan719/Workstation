import React, { useState, useRef, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  BookOpen, Loader2, CheckCircle2, Circle, AlertCircle,
  ChevronDown, ChevronUp, FileText, PenLine, Search,
  Quote, Star, BookMarked, Send, Zap,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface APEvent {
  stage: string;
  label: string;
  content: string;
  data?: { stage_num?: number; total?: number };
}

// ── SSE stream helper ─────────────────────────────────────────────────────────

async function streamPost(
  url: string,
  body: object,
  onChunk: (ev: APEvent) => void,
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

const APIE_STAGES = [
  { key: 'source_discovery',       label: 'Source Discovery',        icon: Search },
  { key: 'argument_architecture',  label: 'Argument Architecture',   icon: PenLine },
  { key: 'structural_outline',     label: 'Structural Outline',      icon: FileText },
  { key: 'draft_synthesis',        label: 'Draft Synthesis',         icon: BookOpen },
  { key: 'evidence_weaving',       label: 'Evidence & Citation',     icon: Quote },
  { key: 'peer_review_simulation', label: 'Peer Review',             icon: Star },
  { key: 'revision_intelligence',  label: 'Revision Intelligence',   icon: PenLine },
  { key: 'integrity_audit',        label: 'Integrity Audit',         icon: BookMarked },
  { key: 'publication_readiness',  label: 'Publication Readiness',   icon: Send },
];

const GENRES = ['academic paper', 'thesis', 'book chapter', 'policy brief', 'literature review', 'essay'];
const CITATION_STYLES = ['APA', 'MLA', 'Chicago', 'IEEE', 'Harvard', 'Vancouver'];
const DOMAINS = ['science', 'law', 'religion', 'education', 'care', 'career', 'philosophy', 'history', 'economics'];

// ── Component ─────────────────────────────────────────────────────────────────

export const AuthorshipEngine: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [genre, setGenre] = useState('academic paper');
  const [domain, setDomain] = useState('science');
  const [audience, setAudience] = useState('academic peers');
  const [citationStyle, setCitationStyle] = useState('APA');
  const [wordCount, setWordCount] = useState('8000');
  const [running, setRunning] = useState(false);
  const [events, setEvents] = useState<APEvent[]>([]);
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);
  const feedRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (feedRef.current) feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [events]);

  const run = async () => {
    if (!topic.trim()) return;
    setRunning(true);
    setEvents([]);
    setError('');
    setExpanded(null);

    await streamPost(
      '/api/v1/intelligence/authorship',
      { topic, genre, domain, audience, citation_style: citationStyle, word_count: wordCount },
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
  const progress = Math.min(100, Math.round((currentStageNum / APIE_STAGES.length) * 100));

  return (
    <div className="space-y-10 pb-24">
      {/* Header */}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2">
          Intelligence Engine · APIE
        </p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Authorship Intelligence
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          9-stage Scholarship & Authorship pipeline — from source discovery through peer review simulation,
          revision intelligence, and publication readiness. Powered by Nine Cognitive Engines + MJM.
        </p>
      </header>

      {/* Stage tracker */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500">
            9-Stage Authorship Pipeline
          </h3>
          {running && (
            <span className="text-[10px] font-black text-aura uppercase tracking-widest animate-pulse">
              {progress}% Complete
            </span>
          )}
        </div>
        <div className="flex gap-2 flex-wrap">
          {APIE_STAGES.map(({ key, label, icon: Icon }, i) => {
            const done = i < currentStageNum;
            const active = i === currentStageNum && running;
            return (
              <div
                key={key}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-wider border transition-all ${
                  done
                    ? 'bg-aura/10 text-aura border-aura/20'
                    : active
                    ? 'bg-highlight/10 text-highlight border-highlight/30 animate-pulse'
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
                className="h-full bg-aura transition-all duration-700 ease-out"
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
            Topic / Thesis / Research Question
          </label>
          <textarea
            value={topic}
            onChange={e => setTopic(e.target.value)}
            placeholder="State your scholarly topic, thesis, or central research question in detail..."
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-aura/50 resize-none"
          />
        </div>

        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-6">
          {/* Genre */}
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Genre
            </label>
            <div className="flex flex-wrap gap-2">
              {GENRES.map(g => (
                <button
                  key={g}
                  type="button"
                  onClick={() => setGenre(g)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    genre === g
                      ? 'bg-aura/20 text-aura border border-aura/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
          </div>

          {/* Citation style */}
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Citation Style
            </label>
            <div className="flex flex-wrap gap-2">
              {CITATION_STYLES.map(cs => (
                <button
                  key={cs}
                  type="button"
                  onClick={() => setCitationStyle(cs)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    citationStyle === cs
                      ? 'bg-aura/20 text-aura border border-aura/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {cs}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Domain + extras */}
        <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-6">
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
                  className={`px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all ${
                    domain === d
                      ? 'bg-aura/20 text-aura border border-aura/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Target Audience
            </label>
            <input
              value={audience}
              onChange={e => setAudience(e.target.value)}
              placeholder="e.g. academic peers, policymakers..."
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-aura/50"
            />
          </div>

          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
              Target Word Count
            </label>
            <input
              value={wordCount}
              onChange={e => setWordCount(e.target.value)}
              placeholder="e.g. 8000"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-aura/50"
            />
          </div>
        </div>

        <div className="flex items-center gap-4 pt-2">
          <Button
            onClick={run}
            disabled={running || !topic.trim()}
            className="flex items-center gap-2 bg-aura text-sovereign"
          >
            {running ? <Loader2 size={16} className="animate-spin" /> : <BookOpen size={16} />}
            {running ? 'Running Authorship Pipeline...' : 'Run APIE — 9 Stages'}
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
              Pipeline Output — {stageEvents.length} of {APIE_STAGES.length} Stages
            </h3>
            {stageEvents.length > 0 && (
              <button
                type="button"
                onClick={() => setExpanded(expanded === null ? 0 : null)}
                className="text-[9px] font-black uppercase text-slate-500 hover:text-aura tracking-widest transition-colors"
              >
                {expanded !== null ? 'Collapse All' : 'Expand All'}
              </button>
            )}
          </div>

          {stageEvents.map((ev, i) => {
            const stageInfo = APIE_STAGES[i];
            const StageIcon = stageInfo?.icon ?? FileText;
            return (
              <Card key={i} className="p-0 overflow-hidden border-slate-800/80">
                <button
                  type="button"
                  onClick={() => setExpanded(expanded === i ? null : i)}
                  className="w-full flex items-center justify-between p-5 text-left hover:bg-slate-800/30 transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-aura/10 flex items-center justify-center shrink-0">
                      <StageIcon size={14} className="text-aura" />
                    </div>
                    <div>
                      <p className="font-black text-white text-sm">{ev.label}</p>
                      <p className="text-[9px] font-bold uppercase text-slate-500 mt-0.5">
                        Stage {i + 1} of {APIE_STAGES.length}
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
                    <div className="mt-4 prose prose-invert prose-sm max-w-none">
                      <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
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
            <Card className="p-6 border-aura/30 bg-aura/5">
              <div className="flex items-center gap-3 mb-3">
                <Zap size={18} className="text-aura" />
                <h3 className="font-black text-aura uppercase tracking-widest text-sm">
                  Authorship Pipeline Complete
                </h3>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                {completeEvent.content} — {(completeEvent.data as any)?.genre ?? genre} ·{' '}
                {(completeEvent.data as any)?.citation_style ?? citationStyle}
              </p>
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
