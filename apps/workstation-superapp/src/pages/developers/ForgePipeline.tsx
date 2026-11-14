import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { Hammer, Loader2, AlertCircle, Check, ChevronDown, ChevronUp, Rocket, FlaskConical } from 'lucide-react';
import { FabricLink } from '../../components/FabricLink';
import { provenanceMapBadge, apiJson, bodyOrNull, bodyDetail } from '../../lib/api';
import { ReadFailures, useReadFailures } from '../../components/ReadFailures';   // W929

//  W979 (FU-399 part 12) - `params` names the keys each stage declares, with their type (GET /forge/resources)
interface Resource { id: string; name: string; role: string; biomimetic: string; params?: Record<string, string> }
// W805 (FU-823) - each stage now says what served it, and what kind of stage it is
interface StageOutput { resource: string; name: string; biomimetic: string; output: string;
  served_by?: string | null; kind?: string; kind_basis?: string }
// W490 (sweep S8.12, C7) — the run's ai_provenance was returned and never rendered: each stage card is
// named for a fabric engine (Petri Dish / Laboratory / Factory) with a biomimetic subtitle, and every
// one is in fact a persona prompt through the gateway. On the floor all five calls compose scaffolds.
// W494 (FU-130 refutation) — forge's `governance` became the shared intent-gate object (status +
// scope + content_screened); it was typed `string` here and rendered directly as a JSX child, which
// throws "Objects are not valid as a React child". The pre-gate "ungated" string is still possible, so
// both shapes are accepted and the qualifier is shown when the object carries it.
type IntentGate = { status: string; scope?: string; content_screened?: boolean; checkpoint?: string; node?: string };
interface RunResult { run_id: string; pipeline: string[]; ceo_framing: string; stage_outputs: StageOutput[]; integrated_deliverable: string;
  governance: string | IntentGate;
  ai_provenance?: { served_by?: Record<string, number>; any_external?: boolean };
  //  W979 - what served the framing and the integration: null when the call failed, absent on a record from before
  ceo_served_by?: string | null; integration_served_by?: string | null }

//  W979 - what served one call, as the record has it: a record from before W979 never said, and null is a failed call
const servedBy = (v: string | null | undefined): string =>
  v === undefined ? 'not recorded' : (v ?? 'nothing — the call failed');

export const ForgePipeline: React.FC = () => {
  const { failures: readFailures, note: noteRead, clear: clearRead } = useReadFailures();   // W929 - a read that fails is said
  const [resources, setResources] = useState<Resource[]>([]);
  const [selected, setSelected] = useState<string[]>(['petri_dish', 'laboratory', 'factory']);
  const [objective, setObjective] = useState('');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<RunResult | null>(null);
  const [open, setOpen] = useState<string>('deliverable');
  // W508 (P2.8(4)) — PER-STAGE CONFIG. StageConfig has carried a `config` field all along and _execute feeds
  // it into each stage's prompt, so the reconfigurable half of a "reconfigurable resource" existed in the API
  // and had no surface. Held as the raw text the user typed, per stage id.
  const [stageConfig, setStageConfig] = useState<Record<string, string>>({});
  const [rerunning, setRerunning] = useState(false);

  // key=value per line. Free-form on purpose: the API takes any key, so the page passes what was typed rather than
  // pretending to know the shape — and it REPORTS a line it could not read instead of dropping it.
  // W979 (FU-399 part 12) - each stage DECLARES its keys (`params` on GET /forge/resources), and the page names them
  // now: every stage's placeholder offered the Laboratory's key. A key its stage does not declare is still sent, as
  // typed, and the page says which.
  const parseConfig = (raw: string): { config: Record<string, string>; unreadable: string[] } => {
    const config: Record<string, string> = {};
    const unreadable: string[] = [];
    (raw || '').split('\n').map(l => l.trim()).filter(Boolean).forEach(line => {
      const i = line.indexOf('=');
      if (i <= 0) { unreadable.push(line); return; }
      config[line.slice(0, i).trim()] = line.slice(i + 1).trim();
    });
    return { config, unreadable };
  };
  const unreadableLines = selected.flatMap(id => parseConfig(stageConfig[id] || '').unreadable);
  //  W979 - the keys a stage declares, or null when the stages could not be read (then nothing is said of its keys)
  const declared = (id: string): Record<string, string> | null => resources.find(r => r.id === id)?.params ?? null;
  const undeclaredKeys = selected.flatMap(id => {
    const d = declared(id);
    return d ? Object.keys(parseConfig(stageConfig[id] || '').config).filter(k => !Object.keys(d).includes(k)).map(k => `${id}: ${k}`) : [];
  });

  useEffect(() => { apiJson('/api/v1/forge/resources').then(d => setResources(d.resources ?? [])).catch(noteRead('the Forge resources')); }, []);

  const toggle = (id: string) => setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id]);

  const run = async () => {
    if (!objective.trim()) return;
    setRunning(true); setError(''); setResult(null);
    try {
      const r = await fetch('/api/v1/forge/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ objective, stages: selected.map(t => ({ type: t, config: parseConfig(stageConfig[t] || '').config })) }) });
      // W805 (FU-823) - a refused pipeline says WHY: the route's sentence, not a bare status number
      if (!r.ok) {
        let _why = '';
        const _b = await bodyOrNull(r); _why = bodyDetail(_b, '');   // W960 (FU-1181); W1013 - a field check by its field
        setError(_why ? `HTTP ${r.status} — ${_why}` : `HTTP ${r.status}`); setRunning(false); return;
      }
      setResult(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-10 pb-24">
      <ReadFailures failures={readFailures} />
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Forge</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Digital Resource Forge</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Compose the IDBO's digital resources — Petri Dish · Incubator · Laboratory · Factory · Generator · Simulator · Reactor —
          into a <span className="text-highlight">swarm-orchestrated cascade pipeline</span> (AI CEO frames → resources process → CoE integrates),
          producing integrated multi-type outputs for Concept→Commercialisation.
        </p>
        <div className="mt-3"><FabricLink /></div>
      </header>

      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4">Select &amp; order resources</h3>
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-4 gap-2">
          {resources.map(r => {
            const sel = selected.includes(r.id);
            return (
              <button key={r.id} type="button" onClick={() => toggle(r.id)} className={`text-left p-3 rounded-xl border transition-all ${sel ? 'bg-highlight/10 border-highlight/50' : 'bg-slate-900 border-slate-800'}`}>
                <div className="flex items-center justify-between mb-1">
                  <FlaskConical size={13} className="text-highlight" />
                  {sel && <Check size={12} className="text-highlight" />}
                </div>
                <p className="text-[11px] font-black text-white">{r.name}</p>
                <p className="text-[8px] text-slate-600 italic">{r.biomimetic}</p>
              </button>
            );
          })}
        </div>
        {selected.length > 0 && <p className="text-[9px] font-mono text-highlight mt-3">pipeline: {selected.join(' → ')}</p>}
        {/* W508 (P2.8(4)) — each SELECTED stage can be configured, which is what makes these resources
            reconfigurable in practice rather than in their registry entry. */}
        {selected.length > 0 && (
          <div className="mt-4 space-y-2" data-testid="forge-stage-config">
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">
              Per-stage configuration · one key=value per line · reaches that stage's prompt
            </p>
            {selected.map(id => {
              const keys = declared(id);
              const first = keys ? Object.keys(keys)[0] : undefined;
              return (
                <div key={id} className="flex gap-2 items-start">
                  <div className="w-28 shrink-0 pt-2">
                    <span className="block text-[9px] font-mono text-slate-500">{id}</span>
                    <span className="block text-[8px] text-slate-600" data-testid="forge-stage-declared">
                      {keys === null ? 'its keys were not read'
                        : Object.keys(keys).length ? `declares ${Object.entries(keys).map(([k, t]) => `${k} (${t})`).join(', ')}`
                        : 'declares no key'}
                    </span>
                  </div>
                  <textarea
                    aria-label={`configuration of ${id}`}
                    value={stageConfig[id] || ''}
                    onChange={e => setStageConfig({ ...stageConfig, [id]: e.target.value })}
                    rows={2}
                    placeholder={first ? `${first}=…` : 'key=value'}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1.5 text-[10px] font-mono text-white placeholder:text-slate-700 focus:outline-none focus:border-highlight/40 resize-none"
                  />
                </div>
              );
            })}
            {unreadableLines.length > 0 && (
              <p className="text-[9px] font-bold text-amber-400" data-testid="forge-config-unreadable">
                these lines have no <span className="font-mono">=</span> and are NOT sent:{' '}
                <span className="font-mono">{unreadableLines.join(' · ')}</span>
              </p>
            )}
            {undeclaredKeys.length > 0 && (
              <p className="text-[9px] font-bold text-amber-400" data-testid="forge-config-undeclared">
                these keys are not ones their stage declares, and are sent as typed all the same:{' '}
                <span className="font-mono">{undeclaredKeys.join(' · ')}</span>
              </p>
            )}
          </div>
        )}
      </Card>

      <Card className="p-8 space-y-5">
        <textarea value={objective} onChange={e => setObjective(e.target.value)} rows={3} placeholder="Objective to forge — e.g. 'A halal meal-prep subscription for busy professionals'" className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none" />
        <div className="flex items-center gap-4">
          <Button onClick={run} disabled={running || !objective.trim() || selected.length === 0} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={16} className="animate-spin" /> : <Hammer size={16} />}
            {running ? 'Forging pipeline…' : 'Run Forge Pipeline'}
          </Button>
          {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}
        </div>
      </Card>

      {result && (
        <div className="space-y-3">
          <div className="text-[9px] font-mono text-slate-500 flex items-center gap-2 flex-wrap">
            <span>{result.run_id} · {result.pipeline.join(' → ')}</span>
          {/* W508 (P2.8(4)) — RERUN. POST /forge/runs/{id}/rerun has existed with no control to call it, and
              its backend dropped every per-stage config when rebuilding the pipeline, so a "rerun" ran
              something else. Both halves are fixed; the response states which stages carried a config. */}
          <button
            type="button"
            data-testid="forge-rerun"
            disabled={rerunning}
            onClick={async () => {
              setRerunning(true); setError('');
              try {
                const r = await fetch(`/api/v1/forge/runs/${result.run_id}/rerun`, { method: 'POST' });
                //  W979 (FU-399 part 12) - THE STATUS BEFORE THE BODY, as the run does. The body was parsed first, so a
                //  refusal whose body was not JSON (a proxy's error page) said a parse error and never its status.
                if (!r.ok) {
                  const _rb = await bodyOrNull(r);
                  const _rwhy = bodyDetail(_rb, '');   // W1013 - a field check by its field
                  throw new Error(_rwhy ? `HTTP ${r.status} — ${_rwhy}` : `HTTP ${r.status}`);
                }
                setResult(await r.json());
              } catch (e: any) { setError(e?.message ?? String(e)); }
              setRerunning(false);
            }}
            className="text-[9px] font-black uppercase tracking-widest text-highlight hover:text-white transition-colors disabled:opacity-40">
            {rerunning ? 'Rerunning…' : 'Rerun with the same configuration'}
          </button>
          {(result as any).rerun_basis && (
            <span className="text-[9px] text-slate-500" data-testid="forge-rerun-basis">{(result as any).rerun_basis}</span>
          )}
            {/* W494 — the verdict, and what it covers: the gate screens the intent label and a constant
                attestation sentence, never the pipeline's output. */}
            <span data-testid="forge-intent-gate"
                  title={typeof result.governance === 'string' ? undefined : result.governance?.scope}>
              {typeof result.governance === 'string'
                ? `governance ${result.governance}`
                : `intent gate: ${result.governance?.status}${result.governance?.content_screened === false ? ' · content not screened' : ''}`}
            </span>
            {(() => { const b = provenanceMapBadge(result.ai_provenance?.served_by, result.ai_provenance?.any_external);
              return <span data-testid="forge-provenance" className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`} title={b.title}>{b.label}</span>; })()}
          </div>
          {/* W979 (FU-399 part 12) - THE FRAMING. The run returns the AI CEO's framing of the objective, the stages
              run after it, and the page never showed it. What served it is kept with it now. */}
          <Card className="p-4 border-slate-800/80">
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mb-1">AI CEO framing</p>
            <p className="text-[9px] font-bold text-slate-600 mb-2" data-testid="forge-ceo-served-by">Served by: {servedBy(result.ceo_served_by)}.</p>
            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap" data-testid="forge-ceo-framing">{result.ceo_framing}</p>
          </Card>
          {result.stage_outputs.map((s, i) => (
            <Card key={i} className="p-0 overflow-hidden border-slate-800/80">
              <button type="button" data-testid="forge-stage-toggle" onClick={() => setOpen(open === String(i) ? '' : String(i))} className={`w-full flex items-center justify-between p-4 text-left ${open === String(i) ? 'bg-slate-800/30' : ''}`}>
                <div className="flex items-center gap-3"><FlaskConical size={13} className="text-highlight" /><p className="font-black text-white text-sm">{s.name}</p><span className="text-[9px] text-slate-600 italic">{s.biomimetic}</span></div>
                {open === String(i) ? <ChevronUp size={13} className="text-slate-500" /> : <ChevronDown size={13} className="text-slate-500" />}
              </button>
              {open === String(i) && <div className="px-4 pb-5 border-t border-slate-800/50 pt-3">
                {/* W490 (refutation) — each stage is a persona prompt through the gateway. W805 (FU-823): the API
                    now records what served EACH stage, so the card says it rather than pointing at the run badge. */}
                <p className="text-[9px] font-bold text-slate-600 mb-2" data-testid="forge-stage-scope">
                  Composed by a persona prompt through the gateway, served by {s.served_by ?? 'nothing — the call failed'}.
                  {/* W979 (FU-399 part 12) - what the stage is, in the server's words (W803's kind_basis), not typed here */}
                  {' '}What the stage is: <span data-testid="forge-stage-kind">{s.kind_basis ?? 'not stated by the server'}</span>.
                </p>
                <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{s.output}</p></div>}
            </Card>
          ))}
          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <div className="flex items-center gap-2 mb-3"><Rocket size={16} className="text-highlight" /><h3 className="font-black text-highlight uppercase tracking-widest text-sm">Integrated Deliverable</h3>
              {(() => { const b = provenanceMapBadge(result.ai_provenance?.served_by, result.ai_provenance?.any_external);
                //  W979 (FU-399 part 12) - the title said no stage's own provenance was recorded, untrue since W805
                return <span data-testid="forge-deliverable-provenance" className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`}
                  title={`${b.title ?? ''} — this counts every call in the run: the framing, each stage and the integration. What served each one is said where it is shown.`}>whole run: {b.label}</span>; })()}</div>
            <p className="text-[9px] font-bold text-slate-600 mb-2" data-testid="forge-integration-served-by">Served by: {servedBy(result.integration_served_by)}.</p>
            <p className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">{result.integrated_deliverable}</p>
            <p className="text-[10px] text-slate-500 mt-3">Next: establish this as a living VSB IDBO entity via Genesis.</p>
          </Card>
        </div>
      )}
    </div>
  );
};
