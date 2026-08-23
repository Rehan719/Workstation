import React, { useState, useRef, useCallback } from 'react';
import { WORKSPACE_DOMAINS } from '../../lib/taxonomy';
import { useSearchParams } from 'react-router-dom';
import { Button } from '@workstation/ui';
import { Play, Square, Terminal, Zap, Bug, Share2, Download, Loader2, CheckCircle2 } from 'lucide-react';

const DOMAINS = WORKSPACE_DOMAINS;   // §17.1 (W321) — one shared workspace list
type Domain = typeof DOMAINS[number];

interface Param { label: string; key: string; active: boolean }

const DEFAULT_PARAMS: Param[] = [
  { label: 'Article 1095 Logic',   key: 'article_1095',   active: true  },
  { label: 'Latency Stress Test',  key: 'latency_stress', active: false },
  { label: 'Byzantine Fault Mode', key: 'byzantine',      active: false },
  // W314 — the fabricated 'PQC Enforced' chip removed: no PQC implementation exists.
  { label: 'In-House Fabric',      key: 'inhouse_fabric', active: true  },
];

export const DigitalReactor: React.FC = () => {
  const [searchParams] = useSearchParams();
  const urlDomain = searchParams.get('domain') as Domain | null;
  const [isRunning,   setIsRunning]   = useState(false);
  const [isDone,      setIsDone]      = useState(false);
  const [domain,      setDomain]      = useState<Domain>(
    urlDomain && (DOMAINS as readonly string[]).includes(urlDomain) ? urlDomain : 'general'
  );
  const [params,      setParams]      = useState<Param[]>(DEFAULT_PARAMS);
  const [log,         setLog]         = useState<string[]>([]);
  const [runId,       setRunId]       = useState('');
  const [durationMs,  setDurationMs]  = useState(0);
  const logRef  = useRef<HTMLDivElement>(null);
  const readerRef = useRef<ReadableStreamDefaultReader<Uint8Array> | null>(null);

  const toggleParam = (key: string) =>
    setParams(ps => ps.map(p => p.key === key ? { ...p, active: !p.active } : p));

  const appendLog = useCallback((line: string) => {
    setLog(prev => {
      const next = [...prev, line];
      requestAnimationFrame(() => logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: 'smooth' }));
      return next;
    });
  }, []);

  const handleLaunch = async () => {
    if (isRunning) {
      // Stop
      readerRef.current?.cancel();
      setIsRunning(false);
      appendLog('[SYSTEM] Simulation stopped by user.');
      return;
    }

    setLog([]);
    setIsDone(false);
    setIsRunning(true);
    appendLog(`[SYSTEM] Launching ${domain.toUpperCase()} reactor…`);

    const activeParams: Record<string, boolean> = {};
    params.filter(p => p.active).forEach(p => { activeParams[p.key] = true; });

    try {
      const response = await fetch('/api/v1/reactor/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain, params: activeParams, label: `${domain} simulation` }),
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
              setIsDone(true);
              appendLog(`\n[SYSTEM] ✓ Simulation complete — run ${ev.run_id} (${ev.duration_ms}ms)`);
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
    const content = log.join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reactor-trace-${runId || Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const activeParamCount = params.filter(p => p.active).length;

  return (
    <div className="space-y-8 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-aura break-words uppercase tracking-tighter">Digital Reactor</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Real AI Domain Simulation · Layer A5</p>
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
          <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Simulation Parameters</h3>
          <div className="space-y-5 flex-1">
            {params.map(p => (
              <label
                key={p.key}
                className={`w-full flex justify-between items-center group cursor-pointer ${isRunning ? 'opacity-50 pointer-events-none' : ''}`}
              >
                <span className="text-xs font-bold text-slate-400 group-hover:text-white transition-colors text-left">{p.label}</span>
                <input
                  type="checkbox"
                  checked={p.active}
                  onChange={() => toggleParam(p.key)}
                  disabled={isRunning}
                  className="sr-only"
                />
                <div className={`w-9 h-5 rounded-full transition-all relative shrink-0 ml-4 ${p.active ? 'bg-aura' : 'bg-slate-800'}`} aria-hidden="true">
                  <div className={`absolute top-1 w-3 h-3 rounded-full bg-white transition-all ${p.active ? 'left-5' : 'left-1'}`} />
                </div>
              </label>
            ))}
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-900 flex items-center gap-3">
            <Bug size={18} className={activeParamCount > 2 ? 'text-yellow-500' : 'text-emerald-500'} />
            <p className="text-[9px] font-bold text-slate-400 leading-relaxed">
              {activeParamCount} parameter{activeParamCount !== 1 ? 's' : ''} active.{' '}
              {activeParamCount > 2 ? 'High-complexity run.' : 'Standard configuration.'}
            </p>
          </div>
        </aside>

        {/* Main: console */}
        <main className="@[440px]:col-span-2 rounded-[2rem] bg-slate-950/70 border border-aura/20 flex flex-col overflow-hidden">
          <div className="flex items-center gap-2 px-5 py-3 border-b border-slate-800 shrink-0">
            <Terminal size={12} className="text-aura" />
            <span className="text-[9px] font-black uppercase tracking-widest text-aura">Reactor Console</span>
            {isRunning && <Loader2 size={10} className="text-aura animate-spin ml-auto" />}
            {isDone && <CheckCircle2 size={10} className="text-emerald-500 ml-auto" />}
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
