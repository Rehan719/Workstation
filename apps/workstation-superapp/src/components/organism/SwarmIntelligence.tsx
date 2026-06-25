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

const CSUITE_POOL = ['CSO', 'CFO', 'CTO', 'CPO', 'COO', 'CIO', 'CLO', 'Forecasting', 'Policy'];

const SwarmIntelligence: React.FC = () => {
  const [runs, setRuns] = useState<SwarmRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [task, setTask] = useState('');
  const [delegating, setDelegating] = useState(false);
  const [streamOutput, setStreamOutput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [cascade, setCascade] = useState<any>(null);   // full org-cascade delivery (Chief → Build-to-Order)
  // §5 user design-control: choose which specialist C-Suite officers run (each drives its own CoE).
  const [csuiteSel, setCsuiteSel] = useState<string[]>(['CSO', 'CFO', 'CTO', 'COO', 'CLO']);
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
      // Run the FULL org cascade (Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order →
      // Products) on Workstation's OWN native fabric. The endpoint returns the structured delivery as
      // JSON (every tier + the integrated living management systems + arms-length governance + the
      // UEG provenance seal) — render it, don't treat it as a stream.
      setStreaming(true); setCascade(null); setStreamOutput('');
      const response = await fetch('/api/v1/swarm/cascade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mission: task, domain: 'enterprise', realm: 'enterprise', csuite_roles: csuiteSel }),
      });
      if (response.ok) {
        setCascade(await response.json());
      } else {
        const res = await axios.post('/api/v1/swarm/delegate', { task, n_agents: 3 });
        setStreamOutput(JSON.stringify(res.data, null, 2));
      }
      setStreaming(false);
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

        {/* §5 user design-control — choose which specialist C-Suite officers run (each drives its own CoE) */}
        <div className="mt-2 flex flex-wrap items-center gap-1">
          <span className="text-[8px] font-black uppercase tracking-widest text-white/30 mr-1">C-Suite</span>
          {CSUITE_POOL.map(role => {
            const on = csuiteSel.includes(role);
            return (
              <button key={role} type="button" disabled={delegating}
                onClick={() => setCsuiteSel(s => on ? s.filter(x => x !== role) : [...s, role])}
                className={`text-[8px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded border transition-colors disabled:opacity-50 ${on ? 'bg-fuchsia-500/15 text-fuchsia-300 border-fuchsia-500/40' : 'bg-white/5 text-white/30 border-white/10 hover:text-white/60'}`}>
                {role}
              </button>
            );
          })}
        </div>

        {streaming && !cascade && (
          <div className="mt-3 flex items-center gap-2 text-[10px] text-white/40"><Loader2 size={12} className="animate-spin" /> The living organisation is delivering — Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order…</div>
        )}
        {streamOutput && (
          <div ref={outputRef} className="mt-3 max-h-48 overflow-y-auto font-mono text-[9px] text-green-400 bg-black/40 rounded-lg p-3 leading-relaxed whitespace-pre-wrap border border-white/5">
            {streamOutput}
            {streaming && <span className="animate-pulse">█</span>}
          </div>
        )}
        {cascade && (
          <div className="mt-3 space-y-2">
            {/* §5↔§6 — the living organisation's delivery, in-house + governed + provenance-sealed */}
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-[8px] font-black uppercase tracking-widest text-fuchsia-400">Living-Organisation delivery</span>
              <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cascade.ai_provenance && !cascade.ai_provenance.any_external ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                {cascade.ai_provenance && !cascade.ai_provenance.any_external ? 'in-house' : 'external used'}
              </span>
              {cascade.governance && <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cascade.governance.status === 'allowed' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>gov: {cascade.governance.status}{cascade.governance.arms_length ? ' · arms-length' : ''}</span>}
              {Array.isArray(cascade.management_systems?.integrated) && cascade.management_systems.integrated.length > 0 && (
                <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300">mgmt: {cascade.management_systems.integrated.join('·')}</span>
              )}
              {cascade.quality && typeof cascade.quality.qms_gate_passed === 'boolean' && (
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cascade.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                  title={`§10 quality bar: ${(cascade.quality.bar || []).join(' · ')}${cascade.quality.quality_record_hash ? `\nDocument-controlled under the QMS (DCMS) · record ${String(cascade.quality.quality_record_hash).slice(0, 16)}…` : ''}`}>
                  QMS gate: {cascade.quality.qms_gate_passed ? 'pass' : 'fail'} · cov {Math.round((cascade.quality.delivery_coverage || 0) * 100)}%{cascade.quality.document_controlled ? ' · doc-controlled' : ''}
                </span>
              )}
              {cascade.biomimetic?.immune && (
                <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-violet-500/15 text-violet-300" title={`7 biomimetic layers · ${cascade.biomimetic.self}`}>
                  organism: immune {Math.round((cascade.biomimetic.immune.health ?? 0) * 100)}% · {cascade.biomimetic.circadian}
                </span>
              )}
              {cascade.quality?.compliance && (
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cascade.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                  title={`§11 live compliance — ${(cascade.quality.compliance.verdicts || []).map((v: any) => `${v.framework}:${v.status}`).join(' · ')}`}>
                  compliance: {cascade.quality.compliance.overall}
                </span>
              )}
              {cascade.ueg_hash && <span className="text-[8px] font-mono text-white/30" title={cascade.ueg_hash}>UEG {String(cascade.ueg_hash).slice(0, 12)}…</span>}
            </div>
            {([
              ['Chief of the Board (founder digital twin)', cascade.level_0_chief_of_board],
              ['Board of Directors — action plan', cascade.level_0b_board_resolution],
              ['AI CEO — directive', cascade.level_1_ceo_directive],
              ['Business Transformation Office', cascade.level_4_business_transformation_office],
              ['Build-to-Order — operational delivery', cascade.level_5_build_to_order],
              ['Products & Services catalogue', cascade.products_services_catalogue],
            ] as [string, string][]).filter(([, v]) => v).map(([label, text]) => (
              <details key={label} className="bg-black/40 rounded-lg border border-white/5">
                <summary className="text-[9px] font-black uppercase tracking-widest text-white/60 px-3 py-2 cursor-pointer">{label}</summary>
                <pre className="text-[9px] text-white/50 font-mono whitespace-pre-wrap leading-relaxed max-h-44 overflow-y-auto px-3 pb-3">{String(text).slice(0, 1400)}</pre>
              </details>
            ))}
            {/* §5 — the specialist C-Suite, each officer driving its own Centre of Excellence */}
            {Array.isArray(cascade.csuite_roster?.engaged) && cascade.csuite_roster.engaged.length > 0 && (
              <details className="bg-black/40 rounded-lg border border-white/5">
                <summary className="text-[9px] font-black uppercase tracking-widest text-white/60 px-3 py-2 cursor-pointer">
                  C-Suite → Centres of Excellence ({cascade.csuite_roster.engaged.length} officers, each drives a CoE)
                </summary>
                <div className="px-3 pb-3 space-y-2">
                  {cascade.csuite_roster.engaged.map((role: string) => (
                    <div key={role} className="border-t border-white/5 pt-2">
                      <p className="text-[9px] font-black uppercase tracking-widest text-fuchsia-300">{role}</p>
                      <pre className="text-[9px] text-white/45 font-mono whitespace-pre-wrap leading-relaxed max-h-28 overflow-y-auto">{String(cascade.level_2_csuite?.[role] || '').slice(0, 700)}</pre>
                      {cascade.level_3_coe?.[`${role} CoE`] && (
                        <pre className="mt-1 text-[9px] text-sky-300/50 font-mono whitespace-pre-wrap leading-relaxed max-h-24 overflow-y-auto border-l border-sky-500/20 pl-2">↳ CoE — {String(cascade.level_3_coe[`${role} CoE`]).slice(0, 500)}</pre>
                      )}
                    </div>
                  ))}
                </div>
              </details>
            )}
            {/* §5 — each tier manages, appraises and develops the tier below (arms-length upward pass) */}
            {cascade.appraisals && Object.keys(cascade.appraisals).length > 0 && (
              <details className="bg-black/40 rounded-lg border border-white/5">
                <summary className="text-[9px] font-black uppercase tracking-widest text-white/60 px-3 py-2 cursor-pointer">
                  Management appraisal &amp; development (each tier develops the one below)
                </summary>
                <div className="px-3 pb-3 space-y-2">
                  {Object.entries(cascade.appraisals).map(([k, v]: any) => (
                    <div key={k} className="border-t border-white/5 pt-2">
                      <p className="text-[9px] font-black uppercase tracking-widest text-amber-300/80">{String(k).replace(/_/g, ' ')}</p>
                      <pre className="text-[9px] text-white/45 font-mono whitespace-pre-wrap leading-relaxed max-h-28 overflow-y-auto">{String(v).slice(0, 600)}</pre>
                    </div>
                  ))}
                </div>
              </details>
            )}
            {cascade.management_systems?.document_control && Object.keys(cascade.management_systems.document_control).length > 0 && (
              <p className="text-[8px] text-white/30 leading-relaxed">Document-controlled (DCMS, SHA3-512): {Object.entries(cascade.management_systems.document_control).map(([k, v]: any) => `${k} ${String(v).slice(0, 8)}…`).join('  ·  ')}</p>
            )}
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
