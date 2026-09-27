import React, { useState, useRef, useCallback } from 'react';
import { WORKSPACE_DOMAINS } from '../../lib/taxonomy';
import { useSearchParams } from 'react-router-dom';
import { Button } from '@workstation/ui';
import { Play, Square, Terminal, Zap, Bug, Share2, Download, Loader2, CheckCircle2 } from 'lucide-react';
import { provenanceBadge, provenanceLine } from '../../lib/api';

const DOMAINS = WORKSPACE_DOMAINS;   // §17.1 (W321) — one shared workspace list
type Domain = typeof DOMAINS[number];

// W495 (FU-127, S8.7) — THE FOUR SIMULATION-PARAMETER TOGGLES ARE GONE. They were switches wired
// to nothing: a repo-wide grep for their keys hit only this file. They were serialised into a prompt,
// so no latency was injected, no fault was simulated, the fabric switch changed nothing when off, and
// one of them named a clause with no referent anywhere in the codebase. This is the class W314 removed
// with the fabricated post-quantum chip. Their names are deliberately not repeated here: a guard
// forbids them in this file, and a comment quoting them would keep them alive in it.
// In their place is the ONE parameter /api/v1/reactor/run really honours: which owned tier serves the
// run (orchestrator.complete's `prefer` — native | local | auto).
interface ServingChoice { label: string; value: string; note: string }

const SERVING: ServingChoice[] = [
  { label: 'In-house first (auto)', value: 'auto',
    note: 'the local owned model if it is up, else the deterministic floor' },
  { label: 'Deterministic floor only', value: 'native',
    note: 'the native floor composes the trace from your request — fast, free, reproducible, and not model analysis' },
  { label: 'Local owned model', value: 'local',
    note: 'requires the local model (Ollama); falls back to the floor if it cannot serve, and the badge will say so' },
];

export const DigitalReactor: React.FC = () => {
  const [searchParams] = useSearchParams();
  const urlDomain = searchParams.get('domain') as Domain | null;
  const [isRunning,   setIsRunning]   = useState(false);
  const [isDone,      setIsDone]      = useState(false);
  const [domain,      setDomain]      = useState<Domain>(
    urlDomain && (DOMAINS as readonly string[]).includes(urlDomain) ? urlDomain : 'general'
  );
  const [serving,     setServing]     = useState<string>('auto');
  const [servedBy,    setServedBy]    = useState<string | null>(null);
  const [isExternal,  setIsExternal]  = useState(false);
  const [log,         setLog]         = useState<string[]>([]);
  const [runId,       setRunId]       = useState('');
  const [durationMs,  setDurationMs]  = useState(0);
  const logRef  = useRef<HTMLDivElement>(null);
  const readerRef = useRef<ReadableStreamDefaultReader<Uint8Array> | null>(null);

  const appendLog = useCallback((line: string) => {
    setLog(prev => {
      const next = [...prev, line];
      requestAnimationFrame(() => logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: 'smooth' }));
      return next;
    });
  }, []);

  const servingLabel = SERVING.find(s => s.value === serving)?.label ?? serving;
  const servingNote = SERVING.find(s => s.value === serving)?.note ?? '';
  const provBadge = isDone ? provenanceBadge(servedBy, isExternal) : null;

  const handleLaunch = async () => {
    if (isRunning) {
      // Stop
      readerRef.current?.cancel();
      setIsRunning(false);
      appendLog('[SYSTEM] Stopped by user - the trace is incomplete.');
      return;
    }

    setLog([]);
    setIsDone(false);
    setIsRunning(true);
    setServedBy(null);
    setIsExternal(false);
    appendLog(`[SYSTEM] Asking the ${servingLabel.toLowerCase()} to narrate a ${domain.toUpperCase()} pipeline. Nothing is executed.`);

    try {
      const response = await fetch('/api/v1/reactor/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // W495 (FU-127, S8.7) — `model` is the one parameter this endpoint honours (it reaches
        // orchestrator.complete as `prefer`). `params` used to carry four switches nothing read.
        body: JSON.stringify({ domain, params: {}, label: `${domain} narrative`, model: serving }),
      });
      if (!response.ok || !response.body) throw new Error(`HTTP ${response.status}`);

      const reader = response.body.getReader();
      readerRef.current = reader;
      const dec = new TextDecoder();
      let buf = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop() ?? '';
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const ev = JSON.parse(line.slice(6));
            if (ev.token) {
              const text = ev.token.replace(/\\n/g, '\n');
              // Break token stream into log lines at actual newlines
              const parts = text.split('\n');
              parts.forEach((part: string, i: number) => {
                if (i === 0) {
                  setLog(prev => {
                    const next = [...prev];
                    if (next.length === 0) next.push(part);
                    else next[next.length - 1] += part;
                    return next;
                  });
                } else {
                  appendLog(part);
                }
              });
            } else if (ev.done) {
              setRunId(ev.run_id ?? '');
              setDurationMs(ev.duration_ms ?? 0);
              // W495 (FU-127, S8.7) — the done frame has carried served_by and is_external all along and
              // the page dropped both, so nothing named what produced the trace; and "Simulation
              // complete" described an execution that never happened. The duration is real — it is the
              // time taken to WRITE the trace, which is what it now says.
              setServedBy(ev.served_by ?? null);
              setIsExternal(Boolean(ev.is_external));
              setIsDone(true);
              appendLog(`\n[SYSTEM] Narrative complete — run ${ev.run_id}, written in ${ev.duration_ms}ms by ${ev.served_by ?? 'an unrecorded resource'}. Nothing was executed: no data entered a node, no latency was injected and no gate ran.`);
            } else if (ev.error) {
              appendLog(`[ERROR] ${ev.error}`);
            }
          } catch { /* malformed */ }
        }
        requestAnimationFrame(() => logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: 'smooth' }));
      }
    } catch (err: any) {
      appendLog(`[ERROR] ${err.message}`);
    } finally {
      setIsRunning(false);
      readerRef.current = null;
    }
  };

  const handleExport = () => {
    // W495 (FU-127, S8.7) — the exported trace left the platform with no provenance and no statement of
    // what it is, so a file on disk read as a record of an executed simulation.
    const content = provenanceLine(servedBy, isExternal)
      + `> This is a ${servedBy === 'native' ? 'floor-composed' : 'model-written'} NARRATIVE of a ${domain} pipeline.`
      + ` Nothing was executed: no data entered a node, no latency was injected, no fault was simulated`
      + ` and no quality gate ran. Any figure under [METRICS] is a description of what would be measured.\n\n`
      + log.join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reactor-trace-${runId || Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-aura break-words uppercase tracking-tighter">Digital Reactor</h1>
          {/* W495 (FU-127, S8.7) — the previous subtitle called this a real domain simulation, which
              describes an execution. The page asks an owned tier to WRITE how a pipeline would behave;
              nothing is simulated in the engineering sense. The old wording is not quoted here: a guard
              forbids it in this file. */}
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Written pipeline trace · nothing executed · Layer A5</p>
        </div>
        <div className="flex items-center gap-3 flex-wrap shrink-0">
          <select
            value={domain}
            onChange={e => setDomain(e.target.value as Domain)}
            aria-label="Select simulation domain"
            disabled={isRunning}
            className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-[10px] font-black uppercase text-white focus:outline-none focus:border-aura disabled:opacity-40"
          >
            {DOMAINS.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase()+d.slice(1)}</option>)}
          </select>
          <Button
            onClick={handleLaunch}
            className={isRunning ? 'bg-vital text-white' : 'bg-aura text-sovereign'}
          >
            {isRunning
              ? <><Square size={16} fill="currentColor" /> Stop</>
              : <><Play size={16} /> Launch Reactor</>}
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8 min-h-[560px]">
        {/* Left: params */}
        <aside className="p-6 rounded-[2rem] bg-slate-900/40 border border-slate-800 flex flex-col gap-6">
          <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Run Parameter</h3>
          <div className="space-y-4 flex-1">
            <div>
              <label htmlFor="reactor-serving" className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-2">Which owned tier serves the run</label>
              <select
                id="reactor-serving"
                value={serving}
                onChange={e => setServing(e.target.value)}
                disabled={isRunning}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-[10px] font-black uppercase text-white focus:outline-none focus:border-aura disabled:opacity-40"
              >
                {SERVING.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
              </select>
              <p className="text-[9px] text-slate-500 mt-2 leading-relaxed">{servingNote}</p>
            </div>
            <p className="text-[9px] text-slate-500 leading-relaxed border-t border-slate-800 pt-4">
              This is the only parameter the run honours. Four switches that used to sit here were wired
              to nothing — no code anywhere read them — and have been removed rather than left to imply
              behaviour that does not exist.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-900 flex items-start gap-3">
            <Bug size={18} className="text-slate-500 shrink-0 mt-0.5" />
            <p className="text-[9px] font-bold text-slate-400 leading-relaxed">
              The run produces a WRITTEN TRACE of how a {domain} pipeline would behave. No data enters a
              node, no latency is injected, no fault is simulated and no quality gate runs.
            </p>
          </div>
        </aside>

        {/* Main: console */}
        <main className="@[440px]:col-span-2 rounded-[2rem] bg-slate-950/70 border border-aura/20 flex flex-col overflow-hidden">
          <div className="flex items-center gap-2 px-5 py-3 border-b border-slate-800 shrink-0">
            <Terminal size={12} className="text-aura" />
            <span className="text-[9px] font-black uppercase tracking-widest text-aura">Reactor Console</span>
            {isRunning && <Loader2 size={10} className="text-aura animate-spin ml-auto" />}
            {isDone && (
              <span className="ml-auto flex items-center gap-2">
                {provBadge && (
                  <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${provBadge.cls}`} title={provBadge.title}>{provBadge.label}</span>
                )}
                <CheckCircle2 size={10} className="text-emerald-500" aria-label="the trace finished streaming" />
              </span>
            )}
          </div>

          <div
            ref={logRef}
            className="flex-1 overflow-y-auto p-5 font-mono text-[10px] leading-relaxed space-y-0.5"
          >
            {log.length === 0 && !isRunning ? (
              <div className="h-full flex flex-col items-center justify-center text-center gap-4 opacity-30 pointer-events-none">
                <Terminal size={40} />
                <p className="font-black uppercase tracking-widest text-xs">Select a domain and launch the reactor</p>
              </div>
            ) : (
              log.map((line, i) => {
                const cls = line.startsWith('[ERROR]') ? 'text-red-400'
                  : line.startsWith('[SYSTEM]') ? 'text-aura'
                  : line.includes('[INIT]') || line.includes('[PROCESS]') ? 'text-highlight'
                  : line.includes('[VALIDATE]') ? 'text-yellow-400'
                  : line.includes('[OUTPUT]') || line.includes('[METRICS]') ? 'text-emerald-400'
                  : 'text-slate-400';
                return <p key={i} className={cls}>{line}</p>;
              })
            )}
            {isRunning && (
              <p className="text-aura animate-pulse">▌</p>
            )}
          </div>

          {(isDone || log.length > 0) && (
            <div className="p-4 bg-slate-900/80 border-t border-slate-800 flex justify-between items-center shrink-0 flex-wrap gap-3">
              <div className="flex gap-3 text-[8px] font-black uppercase text-slate-500">
                {runId && <span>Run: {runId}</span>}
                {durationMs > 0 && <span>{durationMs}ms</span>}
              </div>
              <button
                type="button"
                onClick={handleExport}
                className="flex items-center gap-2 px-3 py-1.5 border border-slate-700 rounded-xl text-[9px] font-black text-slate-400 hover:text-white hover:border-aura/50 transition-all uppercase tracking-widest"
              >
                <Download size={11} /> Export Trace
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
