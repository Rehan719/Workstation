import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { ShieldCheck, FileCheck2, Coins, Leaf, Network, Loader2, Play, Wrench, RotateCcw } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';

// W440 — the VBS management systems (QMS · DCMS · BMS · EMS · Mycelial backbone), audited then
// wired. These engines were already honest (real gates, persistent defects, SHA3-512 seals with a
// recomputed integrity fraction); the audit's residue was disclosure — an undisclosed $0.50/insight
// constant inside "ROI", a "latency_p95" that is neither a p95 nor measured, and in-memory accruals
// with no scope — all fixed. This panel renders the real/simulated split as first-class content.

interface SystemRow { id: string; name: string; owned: boolean; real: string[]; simulated: string[]; owns?: string[]; owned_by?: string }
interface DefectRow { id: string; label: string; status: string; opened_at: string; correction?: string | null; meta?: { coverage?: number; stubs_found?: boolean }; reverify_basis?: string }
interface DefectSummary { gates_run: number; defects_total: number; gate_failures: number; open?: number; corrected?: number; closed?: number; non_conformance_rate: number }

function Chip({ tone, children, title }: { tone: 'ok' | 'warn' | 'dim'; children: React.ReactNode; title?: string }) {
  const cls = tone === 'ok' ? 'bg-emerald-500/15 text-emerald-400' : tone === 'warn' ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400';
  return <span title={title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cls}`}>{children}</span>;
}

export const VBSSystemsPanel: React.FC = () => {
  const [systems, setSystems] = useState<SystemRow[] | null>(null);
  const [defects, setDefects] = useState<{ summary: DefectSummary; defects: DefectRow[] } | null>(null);
  const [docCtl, setDocCtl] = useState<any>(null);
  const [bbHealth, setBbHealth] = useState<any>(null);
  const [err, setErr] = useState('');
  const [loadErrs, setLoadErrs] = useState<string[]>([]);
  const [busy, setBusy] = useState('');

  const getJson = (url: string, set: (d: any) => void) =>
    fetch(url)
      .then(r => (r.ok ? r.json() : Promise.reject(new Error(`${url} → HTTP ${r.status}`))))
      .then(set)
      .catch(e => setLoadErrs(errs => [...errs, String(e?.message ?? e)]));

  const loadAll = () => {
    setLoadErrs([]);
    getJson('/api/v1/vbs/systems', d => setSystems(d.systems || []));
    getJson('/api/v1/vbs/qms/defects', setDefects);
    getJson('/api/v1/vbs/qms/document-control', setDocCtl);
    getJson('/api/v1/vbs/backbone/health', setBbHealth);
  };
  useEffect(loadAll, []);

  // ── QMS gate runner ──
  const [gateCov, setGateCov] = useState(0.97);
  const [gateStubs, setGateStubs] = useState(false);
  const [gateRes, setGateRes] = useState<{ passed: boolean; min_coverage: number; non_conformance_rate: number } | null>(null);
  const runGate = async () => {
    setBusy('gate'); setErr('');
    try {
      setGateRes(await apiJson('/api/v1/vbs/qms/gate', { method: 'POST', body: { coverage: gateCov, stubs_found: gateStubs } }));
      loadAll();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── defect correct → reverify loop ──
  const [selDefect, setSelDefect] = useState<string | null>(null);
  const [correction, setCorrection] = useState('');
  const [reverifyContent, setReverifyContent] = useState('');
  const [loopResult, setLoopResult] = useState('');
  const correctDefect = async () => {
    if (!selDefect) return;
    setBusy('correct'); setErr(''); setLoopResult('');
    try {
      await apiJson(`/api/v1/vbs/qms/defects/${selDefect}/correct`, { method: 'POST', body: { correction } });
      setLoopResult('correction recorded — closure still requires re-verification (a correction alone never closes a defect)');
      loadAll();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  const reverifyDefect = async () => {
    if (!selDefect) return;
    setBusy('reverify'); setErr(''); setLoopResult('');
    try {
      const d = await apiJson(`/api/v1/vbs/qms/defects/${selDefect}/reverify`, { method: 'POST', body: { content: reverifyContent } });
      setLoopResult(d.passed
        ? 'closed — the corrected delivery PASSED the same gate, measured from the content itself'
        : 'REOPENED — the correction did not hold (the failed re-verification also raises the non-conformance rate)');
      loadAll();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── DCMS commit ──
  const [artifactId, setArtifactId] = useState('cockpit-demo');
  const [artifactText, setArtifactText] = useState('First controlled revision of this artifact.');
  const [commitRes, setCommitRes] = useState<{ hash: string; version: number; audit_integrity: number } | null>(null);
  const commitArtifact = async () => {
    setBusy('commit'); setErr('');
    try {
      setCommitRes(await apiJson('/api/v1/vbs/dcms/commit', { method: 'POST', body: { artifact_id: artifactId, content: { text: artifactText } } }));
      loadAll();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── BMS economics / EMS efficiency ──
  const [insights, setInsights] = useState(10);
  const [wh, setWh] = useState(50);
  const [econ, setEcon] = useState<any>(null);
  const runEcon = async () => {
    setBusy('econ'); setErr('');
    try { setEcon(await apiJson('/api/v1/vbs/bms/economics', { method: 'POST', body: { insights_count: insights, wh_consumed: wh } })); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  const [eff, setEff] = useState<any>(null);
  const runEff = async () => {
    setBusy('eff'); setErr('');
    try { setEff(await apiJson('/api/v1/vbs/ems/efficiency', { method: 'POST', body: { energy_wh: wh } })); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── backbone register ──
  const [agentId, setAgentId] = useState('cockpit-agent');
  const registerAgent = async () => {
    setBusy('register'); setErr('');
    try {
      await apiJson('/api/v1/vbs/backbone/register', { method: 'POST', body: { agent_id: agentId, capabilities: ['demo'] } });
      loadAll();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  const selRow = (defects?.defects ?? []).find(d => d.id === selDefect);

  return (
    <div className="space-y-4">
      {err && <p className="text-vital text-xs font-bold">{err}</p>}
      {loadErrs.length > 0 && <p className="text-amber-400 text-[10px] font-bold">{loadErrs.length} section(s) failed to load — {loadErrs.slice(0, 2).join(' · ')}</p>}

      {/* catalogue: the real-vs-simulated split IS the content */}
      {systems && (
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-2">
          {systems.map(s => (
            <div key={s.id} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <p className="text-[11px] font-black text-white mb-1">{s.name} {s.owned_by && <span className="text-slate-600">(owned by {s.owned_by.toUpperCase()})</span>}</p>
              {s.real.map((r, i) => <p key={i} className="text-[9px] text-emerald-400/80">✓ {r}</p>)}
              {s.simulated.map((r, i) => <p key={i} className="text-[9px] text-amber-400/80">≈ simulated: {r}</p>)}
              {s.simulated.length === 0 && <p className="text-[9px] text-slate-600 italic">nothing simulated</p>}
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 @[900px]:grid-cols-2 gap-4">
        {/* QMS — gates + the defect loop */}
        <Card className="p-5">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-2"><ShieldCheck size={14} /> QMS — quality gates + the §8.7/§10.2 defect loop</h4>
          {defects && (
            <div className="flex items-center gap-1.5 flex-wrap mb-3">
              <Chip tone="dim">{defects.summary.gates_run} gates run</Chip>
              <Chip tone={defects.summary.gate_failures > 0 ? 'warn' : 'ok'}>{defects.summary.gate_failures} failures</Chip>
              <Chip tone="dim" title="gate failures / gates run — a real rate, 0.0 with no history">
                non-conformance {Math.round(defects.summary.non_conformance_rate * 100)}%
              </Chip>
              <Chip tone={(defects.summary.open ?? 0) > 0 ? 'warn' : 'ok'}>{defects.summary.open ?? 0} open</Chip>
              <Chip tone="dim">{defects.summary.closed ?? 0} closed</Chip>
            </div>
          )}
          <div className="flex items-center gap-2 flex-wrap mb-3">
            <span className="text-[9px] font-black uppercase text-slate-500">run a gate:</span>
            <input type="number" step="0.01" min={0} max={1} value={gateCov} onChange={e => setGateCov(Number(e.target.value))}
              className="w-20 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300" aria-label="coverage" />
            <label className="text-[9px] text-slate-500 flex items-center gap-1">
              <input type="checkbox" checked={gateStubs} onChange={e => setGateStubs(e.target.checked)} /> stubs found
            </label>
            <Button onClick={runGate} disabled={!!busy} className="flex items-center gap-1.5 bg-aura text-sovereign text-[10px]">
              {busy === 'gate' ? <Loader2 size={11} className="animate-spin" /> : <Play size={11} />} Gate
            </Button>
            {gateRes && <Chip tone={gateRes.passed ? 'ok' : 'warn'}>{gateRes.passed ? 'PASSED' : `FAILED (min ${gateRes.min_coverage})`}</Chip>}
          </div>
          <div className="max-h-40 overflow-y-auto space-y-1 mb-2">
            {(defects?.defects ?? []).map(d => (
              <button key={d.id} type="button" onClick={() => { setSelDefect(d.id); setLoopResult(''); }}
                className={`w-full text-left p-2 rounded-lg border text-[10px] transition-colors ${selDefect === d.id ? 'border-aura/40 bg-aura/5' : 'border-slate-900 bg-slate-950 hover:border-slate-700'}`}>
                <span className="font-mono text-slate-400">{d.id}</span> · {d.label} ·{' '}
                <span className={d.status === 'open' ? 'text-amber-400' : d.status === 'closed' ? 'text-emerald-400' : 'text-sky-300'}>{d.status}</span>
              </button>
            ))}
            {defects && defects.defects.length === 0 && <p className="text-[10px] text-slate-600 italic">no defects recorded — failed gates open them automatically</p>}
          </div>
          {selRow && (
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900 space-y-2">
              <p className="text-[9px] text-slate-500">
                {selRow.id} · {selRow.status} · coverage {selRow.meta?.coverage ?? '—'}
                {selRow.reverify_basis && <> · reverified via <span className={selRow.reverify_basis === 'measured_from_content' ? 'text-emerald-400' : 'text-amber-400'}>{selRow.reverify_basis}</span></>}
              </p>
              {selRow.status === 'open' && (
                <div className="flex items-center gap-2">
                  <input value={correction} onChange={e => setCorrection(e.target.value)}
                    className="flex-1 text-[11px] bg-slate-900 border border-slate-800 rounded-lg p-2 text-slate-300" placeholder="what was corrected…" />
                  <Button onClick={correctDefect} disabled={!!busy || !correction.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
                    {busy === 'correct' ? <Loader2 size={11} className="animate-spin" /> : <Wrench size={11} />} Correct
                  </Button>
                </div>
              )}
              {selRow.status === 'corrected' && (
                <div>
                  <textarea value={reverifyContent} onChange={e => setReverifyContent(e.target.value)} rows={2}
                    className="w-full text-[11px] bg-slate-900 border border-slate-800 rounded-lg p-2 text-slate-300 mb-1.5"
                    placeholder="paste the CORRECTED delivery — the platform measures it (section requirements when the defect stores them; length + stub instruments otherwise — the basis says which)" />
                  <Button onClick={reverifyDefect} disabled={!!busy || !reverifyContent.trim()} className="flex items-center gap-1.5 bg-aura text-sovereign text-[10px]">
                    {busy === 'reverify' ? <Loader2 size={11} className="animate-spin" /> : <RotateCcw size={11} />} Re-verify (measured)
                  </Button>
                </div>
              )}
              {loopResult && <p className="text-[10px] text-slate-300">{loopResult}</p>}
            </div>
          )}
        </Card>

        {/* DCMS — versioned seals with a recomputed integrity fraction */}
        <Card className="p-5">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-2"><FileCheck2 size={14} /> DCMS — SHA3-512 document control (owned by the QMS)</h4>
          {docCtl && (
            <div className="flex items-center gap-1.5 flex-wrap mb-3">
              <Chip tone={docCtl.qms_owns_dcms ? 'ok' : 'warn'}>QMS owns DCMS: {String(docCtl.qms_owns_dcms)}</Chip>
              <Chip tone="dim">{docCtl.registered_artifacts} artifacts (persistent)</Chip>
              <Chip tone="dim" title="the RECOMPUTED fraction of stored seals that still match — 0.0 with no verifiable history, never a constant">
                audit integrity {Math.round((docCtl.audit_integrity ?? 0) * 100)}%
              </Chip>
            </div>
          )}
          <div className="space-y-2">
            <input value={artifactId} onChange={e => setArtifactId(e.target.value)}
              className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="artifact id" />
            <textarea value={artifactText} onChange={e => setArtifactText(e.target.value)} rows={2}
              className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="artifact content…" />
            <Button onClick={commitArtifact} disabled={!!busy || !artifactId.trim()} className="flex items-center gap-1.5 bg-aura text-sovereign text-[10px]">
              {busy === 'commit' ? <Loader2 size={11} className="animate-spin" /> : <FileCheck2 size={11} />} Commit version
            </Button>
            {commitRes && (
              <p className="text-[9px] text-slate-500 font-mono break-all">
                v{commitRes.version} · sha3_512 {commitRes.hash.slice(0, 32)}… · integrity {Math.round((commitRes.audit_integrity ?? 0) * 100)}%
              </p>
            )}
          </div>
        </Card>

        {/* BMS + EMS — real arithmetic, simulated constants DISCLOSED */}
        <Card className="p-5">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-2"><Coins size={14} /> BMS economics · <Leaf size={14} /> EMS efficiency</h4>
          <div className="flex items-center gap-2 flex-wrap mb-2">
            <input type="number" min={1} value={insights} onChange={e => setInsights(Number(e.target.value))}
              className="w-20 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300" aria-label="insights" />
            <span className="text-[9px] text-slate-600">insights</span>
            <input type="number" min={0} value={wh} onChange={e => setWh(Number(e.target.value))}
              className="w-20 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300" aria-label="wh" />
            <span className="text-[9px] text-slate-600">Wh</span>
            <Button onClick={runEcon} disabled={!!busy} className="bg-slate-900 text-aura text-[10px]">Economics</Button>
            <Button onClick={runEff} disabled={!!busy} className="bg-slate-900 text-aura text-[10px]">Efficiency</Button>
          </div>
          {econ && (
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-900 mb-2">
              <p className="text-[11px] text-slate-300">
                cost/insight ${Number(econ.cost_per_insight).toFixed(6)} · {econ.status} ·{' '}
                roi {econ.roi === null ? <span className="text-slate-500">null — {econ.roi_basis}</span> : Number(econ.roi).toFixed(2)}
              </p>
              <p className="text-[8px] text-amber-400/70 mt-1">simulated: {(econ.simulated || []).join(' · ')}</p>
            </div>
          )}
          {eff && (
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-900">
              <p className="text-[11px] text-slate-300">CO2 total {Number(eff.total_co2_kg).toFixed(5)} kg <span className="text-slate-600">({eff.scope})</span></p>
              <p className="text-[8px] text-amber-400/70 mt-1">simulated: {(eff.simulated || []).join(' · ')} — the CO2 accrual is the real part</p>
            </div>
          )}
        </Card>

        {/* Mycelial backbone — honest names for simulated figures */}
        <Card className="p-5">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-2"><Network size={14} /> Mycelial backbone</h4>
          {bbHealth && (
            <div className="flex items-center gap-1.5 flex-wrap mb-3">
              <Chip tone="dim">{bbHealth.active_nodes} nodes</Chip>
              <Chip tone="warn" title={bbHealth.latency_note}>latency EWMA {bbHealth.latency_ewma_ms}ms (simulated)</Chip>
              <Chip tone="dim" title={bbHealth.failure_rate_basis}>
                failure rate {bbHealth.failure_rate === null ? 'null — nothing measured' : `${Math.round(bbHealth.failure_rate * 100)}%`}
              </Chip>
              <Chip tone="dim" title={bbHealth.scope}>per-process</Chip>
            </div>
          )}
          <div className="flex items-center gap-2">
            <input value={agentId} onChange={e => setAgentId(e.target.value)}
              className="flex-1 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="agent id" />
            <Button onClick={registerAgent} disabled={!!busy || !agentId.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
              {busy === 'register' ? <Loader2 size={11} className="animate-spin" /> : <Network size={11} />} Register DID
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};
