import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Loader2, Send, Cpu, RefreshCw, Zap, ChevronDown, ChevronUp } from 'lucide-react';

interface SwarmRun {
  run_id: string;
  task: string;
  agents_engaged?: string[];
  agent_ids?: string[];           // fallback
  ceo_synthesis?: string;
  result?: string;                // fallback
  duration_ms?: number;
  fitness?: number;
  status?: string;
  created_at?: string;
}

const STATUS_COLOR: Record<string, string> = {
  STABLE:   'border-green-400  text-green-400',
  EVOLVING: 'border-yellow-400 text-yellow-400',
  COMPLETE: 'border-blue-400   text-blue-400',
  default:  'border-white/20   text-white/40',
};

function RunCard({ run }: { run: SwarmRun }) {
  const [open, setOpen] = useState(false);
  const agents = run.agents_engaged ?? run.agent_ids ?? [];
  const synthesis = run.ceo_synthesis ?? run.result;
  const statusKey = run.status ?? 'COMPLETE';
  const colorCls = STATUS_COLOR[statusKey] ?? STATUS_COLOR.default;
  const fitness = run.fitness ?? (run.duration_ms ? Math.max(0.7, 1 - run.duration_ms / 30000) : null);

  return (
    <div className={`p-2.5 bg-[#111] mb-2 rounded-md border-l-[3px] ${colorCls.split(' ')[0]} cursor-pointer`} onClick={() => setOpen(o => !o)}>
      <div className="flex justify-between items-start">
        <div>
          <div className="text-xs font-bold text-white truncate max-w-[200px]">{run.task.slice(0, 50)}{run.task.length > 50 ? '…' : ''}</div>
          <div className="text-[10px] text-[#666] mt-0.5">
            {agents.length > 0 ? `${agents.join(', ')}` : 'Swarm'} · {run.run_id.slice(-8)}
          </div>
        </div>
        <div className="text-right shrink-0 ml-2">
          {fitness !== null && <div className="text-xs text-[#00d4ff]">{(fitness * 100).toFixed(1)}%</div>}
          <div className={`text-[9px] ${colorCls.split(' ')[1] ?? 'text-white/40'}`}>{statusKey}</div>
          {open ? <ChevronUp size={10} className="ml-auto text-white/30 mt-1" /> : <ChevronDown size={10} className="ml-auto text-white/30 mt-1" />}
        </div>
      </div>
      {open && synthesis && (
        <pre className="mt-2 text-[9px] text-white/50 font-mono whitespace-pre-wrap leading-relaxed max-h-40 overflow-y-auto border-t border-white/8 pt-2">
          {synthesis.slice(0, 800)}{synthesis.length > 800 ? '\n…' : ''}
        </pre>
      )}
    </div>
  );
}

const SwarmIntelligence: React.FC = () => {
  const [runs, setRuns] = useState<SwarmRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [task, setTask] = useState('');
  const [delegating, setDelegating] = useState(false);
  const [streamOutput, setStreamOutput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const outputRef = useRef<HTMLDivElement>(null);

  const loadRuns = async () => {
    try {
      const res = await axios.get('/api/v1/swarm/runs');
      setRuns(res.data.runs ?? []);
    } catch { /* empty state */ }
    finally { setLoading(false); }
  };

  useEffect(() => { loadRuns(); }, []);

  useEffect(() => {
    if (outputRef.current) outputRef.current.scrollTop = outputRef.current.scrollHeight;
  }, [streamOutput]);

  const delegate = async () => {
    if (!task.trim() || delegating) return;
    setDelegating(true);
    setStreamOutput('');
    setStreaming(false);

    try {
      // First try cascade (streaming)
      setStreaming(true);
      const response = await fetch('/api/v1/swarm/cascade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mission: task, domains: [], n_agents: 4 }),
      });

      if (!response.ok || !response.body) {
        // Fallback to delegate
        const res = await axios.post('/api/v1/swarm/delegate', { task, n_agents: 3 });
        setStreamOutput(JSON.stringify(res.data, null, 2));
        setStreaming(false);
      } else {
        const reader = response.body.getReader();
        const dec = new TextDecoder();
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = dec.decode(value, { stream: true });
          const lines = chunk.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.content) setStreamOutput(p => p + data.content);
                else if (data.stage) setStreamOutput(p => p + `\n[${data.stage}] `);
              } catch { setStreamOutput(p => p + line.slice(6)); }
            }
          }
        }
        setStreaming(false);
      }

      // Reload runs after completion
      await loadRuns();
      setTask('');
    } catch (e: any) {
      setStreamOutput(`Error: ${e?.response?.data?.detail ?? e.message}`);
      setStreaming(false);
    } finally {
      setDelegating(false);
    }
  };

  const paretoPoints: { x: number; y: number }[] = runs.length > 0
    ? runs.slice(0, 5).map((r, i) => ({ x: 10 + i * 18, y: r.fitness ?? 0.88 + i * 0.02 }))
    : [{ x: 10, y: 0.95 }, { x: 25, y: 0.98 }, { x: 50, y: 0.99 }];

  return (
    <div className="p-5 bg-[#050505] text-white rounded-2xl border border-[#1a1a1a]">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-fuchsia-500 text-lg font-bold uppercase">Swarm Intelligence Hub</h2>
        <button onClick={loadRuns} className="p-1.5 rounded hover:bg-white/5 text-white/30 hover:text-white/60">
          <RefreshCw size={13} />
        </button>
      </div>

      {/* Delegate panel */}
      <div className="mb-5 bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
        <h3 className="text-xs text-[#666] mb-3 uppercase tracking-widest flex items-center gap-1.5">
          <Cpu size={11} /> Delegate Mission to Swarm
        </h3>
        <div className="flex gap-2">
          <input
            value={task}
            onChange={e => setTask(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && delegate()}
            placeholder="Describe the mission for the agent swarm..."
            className="flex-1 bg-[#111] border border-[#222] rounded-lg px-3 py-2 text-xs text-white placeholder-[#444] focus:outline-none focus:border-fuchsia-800"
          />
          <button
            onClick={delegate}
            disabled={delegating || !task.trim()}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-fuchsia-900/40 hover:bg-fuchsia-900/60 text-fuchsia-400 border border-fuchsia-800/30 text-xs font-semibold disabled:opacity-50"
          >
            {delegating ? <Loader2 size={12} className="animate-spin" /> : <Send size={12} />}
            {delegating ? 'Cascading…' : 'Cascade'}
          </button>
        </div>

        {streamOutput && (
          <div ref={outputRef} className="mt-3 max-h-48 overflow-y-auto font-mono text-[9px] text-green-400 bg-black/40 rounded-lg p-3 leading-relaxed whitespace-pre-wrap border border-white/5">
            {streamOutput}
            {streaming && <span className="animate-pulse">█</span>}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-5">
        {/* Active Swarm Runs */}
        <div className="bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
          <h3 className="text-xs text-[#666] mb-4 uppercase tracking-widest flex items-center gap-1.5">
            <Zap size={10} /> Recent Swarm Runs
          </h3>
          {loading ? (
            <div className="flex items-center gap-2 text-white/30 text-xs">
              <Loader2 size={12} className="animate-spin" /> Loading…
            </div>
          ) : runs.length === 0 ? (
            <p className="text-[10px] text-[#444]">No swarm runs yet. Delegate a mission above.</p>
          ) : (
            <div className="max-h-60 overflow-y-auto">
              {runs.slice(0, 8).map(r => <RunCard key={r.run_id} run={r} />)}
            </div>
          )}
        </div>

        {/* Pareto Frontier */}
        <div className="bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
          <h3 className="text-xs text-[#666] mb-4 uppercase tracking-widest">Pareto: Accuracy vs Latency</h3>
          <svg viewBox="0 0 100 100" className="w-full h-[120px]" aria-label="Pareto frontier chart">
            <line x1="0" y1="100" x2="100" y2="100" stroke="#333" strokeWidth="0.5" />
            <line x1="0" y1="0" x2="0" y2="100" stroke="#333" strokeWidth="0.5" />
            {paretoPoints.map((p, i) => (
              <circle
                key={i}
                cx={p.x}
                cy={100 - (p.y - 0.85) * 666}
                r="2.5"
                fill="#ff00ff"
              />
            ))}
            <text x="95" y="99" fontSize="5" fill="#444" textAnchor="end">Latency</text>
            <text x="4" y="6" fontSize="5" fill="#444">Accuracy</text>
          </svg>
          {runs.length > 0 && (
            <div className="mt-2 space-y-1">
              {runs.slice(0, 3).map(r => (
                <div key={r.run_id} className="flex justify-between text-[9px] text-[#555]">
                  <span className="truncate max-w-[140px]">{r.task.slice(0, 30)}…</span>
                  <span className="text-fuchsia-500">{r.duration_ms ? `${r.duration_ms}ms` : '—'}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Emergence Feed */}
      <div className="mt-5 bg-[#0a0a0a] p-4 rounded-xl border border-[#111]">
        <h3 className="text-xs text-[#666] mb-2.5 uppercase tracking-widest">Emergence Event Stream</h3>
        <div className="font-mono text-[10px] text-green-400 space-y-1">
          {runs.length > 0 ? (
            runs.slice(0, 5).map(r => (
              <div key={r.run_id}>
                [{r.created_at ? new Date(r.created_at).toLocaleTimeString() : '--:--:--'}] SWARM_COMPLETE: {r.task.slice(0, 55)} · {(r.agents_engaged ?? r.agent_ids ?? []).length} agents
              </div>
            ))
          ) : (
            <>
              <div>[--:--:--] IDLE: No active swarm runs. Delegate a mission to see emergence events.</div>
              <div>[--:--:--] READY: Swarm intelligence online — waiting for orchestration signal.</div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SwarmIntelligence;
