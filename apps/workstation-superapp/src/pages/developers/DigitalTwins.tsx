import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Boxes, Loader2, Activity, ChevronRight } from 'lucide-react';

// W481 (FU-122, sweep S8.1) — the transformation cascade writes a PROJECTION (arithmetic over two live
// readings), never a simulation; records written before W481 carry the old `simulations` shape and its
// 'stable-and-improving' verdict, which was impossible by construction. Both are rendered as projections.
interface Projection { of?: string; formula?: string; projected?: number; current?: number; note?: string;
  compared_with_current?: string }
interface Simulation { scenario?: string; verdict?: string; projected_realisation?: number; time_horizon?: string;
  // W831 (FU-747) - a scenario composed through /twin/simulate is stored in the same list. It carries its own id and
  // its statement of how its text was produced; its text is returned when asked and is not stored.
  simulation_id?: string; scenario_name?: string; run_at?: string;
  composition?: { basis?: string; served_by?: string; computed?: boolean } | null }

// W831 (FU-747) - ModelRequest's documented values; `complexity` selects the route's own specification text
const MODEL_TYPES = ['process', 'biological', 'economic', 'physical', 'organisational'];
const COMPLEXITIES = ['simple', 'standard', 'complex'];
const FIELD = 'w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-white';
interface TwinModel {
  model_id: string;
  system_name: string;
  system_description?: string;
  domain?: string;
  model_type?: string;
  complexity?: string;
  model_spec?: string;
  simulations?: Simulation[];          // legacy records only
  projections?: Projection[];
  trained?: boolean;
  template_note?: string;
  // P3.30 r6 - how this record's text was produced, as the route recorded it (absent on older records)
  composition?: { kind?: string; computed?: boolean; served_by?: string; basis?: string } | null;
  created_at?: string;
}

export const DigitalTwins: React.FC = () => {
  const [models, setModels] = useState<TwinModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<TwinModel | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  //  W831 (FU-747) - composing a model, and asking a selected model for a scenario or an optimisation
  const [form, setForm] = useState({ system_name: '', system_description: '', domain: 'general',
                                     model_type: 'process', complexity: 'standard' });
  const [composing, setComposing] = useState(false);
  const [scenario, setScenario] = useState({ scenario_name: '', scenario_description: '', time_horizon: '90 days' });
  const [objective, setObjective] = useState('');
  const [constraints, setConstraints] = useState('');
  const [asking, setAsking] = useState(false);
  const [actionError, setActionError] = useState('');
  const [answer, setAnswer] = useState<{ kind: 'scenario' | 'optimisation'; title: string; text: string;
                                          basis?: string } | null>(null);

  const loadModels = () => fetch('/api/v1/twin/models')
    .then(r => r.json())
    .then(d => setModels(d.models ?? (Array.isArray(d) ? d : [])))
    .catch(() => {});

  useEffect(() => {
    loadModels().finally(() => setLoading(false));
  }, []);

  const post = async (url: string, body: any) => {
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                                 body: JSON.stringify(body) });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(typeof d?.detail === 'string' ? d.detail : `HTTP ${r.status}`);
    return d;
  };

  const compose = async () => {
    setComposing(true); setActionError('');
    try {
      const d = await post('/api/v1/twin/model', form);
      await loadModels();
      await open({ model_id: d.model_id, system_name: d.system_name } as TwinModel);
      setForm(f => ({ ...f, system_name: '', system_description: '' }));
    } catch (e: any) { setActionError(e?.message ?? String(e)); }
    setComposing(false);
  };

  const ask = async (kind: 'scenario' | 'optimisation') => {
    if (!selected) return;
    setAsking(true); setActionError(''); setAnswer(null);
    try {
      const d = kind === 'scenario'
        ? await post('/api/v1/twin/simulate', { model_id: selected.model_id, ...scenario })
        : await post('/api/v1/twin/optimise', { model_id: selected.model_id, optimisation_objective: objective,
            constraints: constraints.split('\n').map(s => s.trim()).filter(Boolean) });
      setAnswer({ kind, title: (kind === 'scenario' ? d.scenario_name : d.objective) ?? '', text: d.result ?? '',
                  basis: d.composition?.basis });
      if (kind === 'scenario') {        // the stored model now lists this scenario
        const r = await fetch(`/api/v1/twin/models/${selected.model_id}`);
        if (r.ok) setSelected(await r.json());
      }
    } catch (e: any) { setActionError(e?.message ?? String(e)); }
    setAsking(false);
  };

  const open = async (m: TwinModel) => {
    setAnswer(null);
    setLoadingDetail(true); setSelected(m);
    try {
      const r = await fetch(`/api/v1/twin/models/${m.model_id}`);
      if (r.ok) setSelected(await r.json());
      else setSelected({ ...m, _load_error: `HTTP ${r.status} — showing the summary row only` } as any);   // W329
    } catch { setSelected({ ...m, _load_error: 'backend unreachable — showing the summary row only' } as any); }
    setLoadingDetail(false);
  };

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Digital Resources</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Digital Twins</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Living digital-twin models generated across the organism — including the VSB organisational
          twins produced by each transformation orchestration. Select a model to inspect its structure
          and projections. Nothing here is a trained model, and the transformation cascade's figure is a
          projection (arithmetic over live readings), not a simulation. A model, a scenario or an optimisation
          composed on this page is text written by whatever served it; nothing is computed, and each answer says so.
        </p>
      </header>

      {/* W831 (FU-747) - the page could only read twins: the three routes that compose text had no caller here */}
      <Card className="p-6" data-testid="twin-compose">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2">
          <Boxes size={14} /> Compose a twin model (text)
        </h3>
        <div className="grid grid-cols-1 @[640px]:grid-cols-2 gap-2 mb-2">
          <input value={form.system_name} onChange={e => setForm({ ...form, system_name: e.target.value })}
            placeholder="System name" className={FIELD} />
          <input value={form.domain} onChange={e => setForm({ ...form, domain: e.target.value })}
            placeholder="Domain" className={FIELD} />
          <select value={form.model_type} onChange={e => setForm({ ...form, model_type: e.target.value })}
            className={FIELD} aria-label="Model type">
            {MODEL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <select value={form.complexity} onChange={e => setForm({ ...form, complexity: e.target.value })}
            className={FIELD} aria-label="Complexity">
            {COMPLEXITIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <textarea value={form.system_description} onChange={e => setForm({ ...form, system_description: e.target.value })}
          rows={2} placeholder="What the system is and does" className={`${FIELD} mb-3`} />
        <Button onClick={compose} disabled={composing || !form.system_name.trim() || !form.system_description.trim()}
          className="flex items-center gap-2 text-xs">
          {composing ? <Loader2 size={13} className="animate-spin" /> : <Boxes size={13} />} Compose the model text
        </Button>
        {actionError && <p className="text-vital text-xs font-bold mt-2" data-testid="twin-action-error">{actionError}</p>}
      </Card>

      <div className="grid grid-cols-1 @[900px]:grid-cols-2 gap-6">
        {/* List */}
        <Card className="p-6">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2">
            <Boxes size={14} /> Twin Models ({models.length})
          </h3>
          {loading ? (
            <p className="text-slate-600 text-xs py-6 text-center"><Loader2 size={14} className="animate-spin inline" /> Loading…</p>
          ) : models.length === 0 ? (
            <p className="text-slate-600 text-xs py-6 text-center uppercase tracking-widest font-bold">
              No twins yet. Run a transformation orchestration to generate one.
            </p>
          ) : (
            <div className="space-y-2">
              {models.map(m => (
                <div key={m.model_id} onClick={() => open(m)}
                  className={`flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all ${
                    selected?.model_id === m.model_id ? 'bg-highlight/10 border-highlight/30' : 'bg-slate-950/60 border-slate-900 hover:border-highlight/20'
                  }`}>
                  <div className="min-w-0">
                    <p className="text-xs font-black text-white truncate">{m.system_name}</p>
                    <p className="text-[9px] text-slate-600 uppercase">{m.model_type} · {m.created_at ? new Date(m.created_at).toLocaleDateString() : ''}</p>
                  </div>
                  <ChevronRight size={14} className="text-slate-700 shrink-0" />
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Detail */}
        <Card className="p-6">
          {!selected ? (
            <p className="text-slate-600 text-xs py-10 text-center uppercase tracking-widest font-bold">Select a twin model</p>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-black text-white">{selected.system_name}</h3>
                {loadingDetail && <Loader2 size={13} className="animate-spin text-highlight" />}
              </div>
              {selected.trained === false && selected.template_note ? (
                <p className="text-[10px] text-amber-400/90 font-semibold mb-3 leading-relaxed">{selected.template_note}</p>
              ) : selected.trained === undefined && (selected.simulations?.some(s => !s.simulation_id) || /vision_realisation|owner twin/i.test(selected.model_spec || '')) ? (
                /* W481 — records written before this round claim an owner twin and a 'vision_realisation' state
                   variable; nothing here is trained, and that is said on the record itself */
                <p className="text-[10px] text-amber-400/90 font-semibold mb-3 leading-relaxed">
                  recorded before W481: a structural template, not a trained model. Its components name an
                  "owner twin" and its state variable is called vision_realisation — that figure is API-surface
                  coverage, not delivery, and no twin was trained.
                </p>
              ) : null}
              {selected.projections && selected.projections.length > 0 && (
                <div className="mb-4 space-y-2">
                  {selected.projections.map((p, i) => (
                    <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <p className="text-[10px] font-bold text-slate-300 flex items-center gap-1.5"><Activity size={11} className="text-slate-400" /> Projection of {p.of ?? 'a live reading'}</p>
                      <p className="text-[9px] text-slate-600">{String(p.projected ?? '—')} from {String(p.current ?? '—')} · {p.formula} · {p.compared_with_current}</p>
                      {p.note && <p className="text-[9px] text-amber-400/80 mt-1 leading-relaxed">{p.note}</p>}
                    </div>
                  ))}
                </div>
              )}
              {selected.simulations && selected.simulations.length > 0 && (
                <div className="mb-4 space-y-2">
                  {selected.simulations.map((s, i) => s.simulation_id ? (
                    /* W831 (FU-747) - a scenario composed through /twin/simulate, not a pre-W481 record */
                    <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-900" data-testid="twin-scenario-row">
                      <p className="text-[10px] font-bold text-slate-300 flex items-center gap-1.5"><Activity size={11} className="text-slate-400" /> Scenario · {s.scenario_name}</p>
                      <p className="text-[9px] text-slate-600">horizon {s.time_horizon ?? 'not stated'}{s.run_at ? ` · ${s.run_at}` : ''} · its text was returned when it was asked for and is not stored</p>
                      <p className="text-[9px] text-amber-400/80 mt-1 leading-relaxed">{s.composition?.basis ?? 'This scenario row does not say how its text was produced.'}</p>
                    </div>
                  ) : (
                    <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <p className="text-[10px] font-bold text-slate-300 flex items-center gap-1.5"><Activity size={11} className="text-slate-400" /> {s.scenario ?? 'Recorded before W481'}</p>
                      {s.projected_realisation != null && (
                        <p className="text-[9px] text-slate-600">projected {Math.round((s.projected_realisation || 0) * 100)}% · horizon {s.time_horizon}</p>
                      )}
                      <p className="text-[9px] text-amber-400/80 mt-1 leading-relaxed">a pre-W481 record: this figure is arithmetic over two live readings (coverage × health), not a simulation{/improving/i.test(s.verdict || '') ? `, and its stored verdict (${s.verdict}) was reached whenever immune health was 1.0 — the projection could never exceed the current figure` : s.verdict ? `, and its stored verdict was ${s.verdict}` : ''}</p>
                    </div>
                  ))}
                </div>
              )}
              {/* P3.30 r6 (ledger v16 R4.11) - the record's own statement of how its text was produced, above the
                  text. A record that carries none says that, rather than nothing. */}
              <p className="text-[10px] text-amber-400/90 leading-relaxed mb-2" data-testid="twin-composition-basis">
                {selected.composition?.basis
                  ?? 'This record does not say how its text was produced.'}
              </p>
              <pre className="text-[10px] text-slate-400 leading-relaxed whitespace-pre-wrap font-mono bg-slate-950 rounded-xl p-4 max-h-[460px] overflow-auto border border-slate-900">{selected.model_spec ?? 'No model spec.'}</pre>

              {/* W831 (FU-747) - ask this model for a scenario or an optimisation; both answers are text */}
              <div className="mt-4 grid grid-cols-1 gap-3" data-testid="twin-ask">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-900 space-y-2">
                  <p className="text-[10px] font-black uppercase tracking-widest text-slate-400">Compose a scenario narrative</p>
                  <input value={scenario.scenario_name} onChange={e => setScenario({ ...scenario, scenario_name: e.target.value })}
                    placeholder="Scenario name" className={FIELD} />
                  <textarea value={scenario.scenario_description} onChange={e => setScenario({ ...scenario, scenario_description: e.target.value })}
                    rows={2} placeholder="What changes in this scenario" className={FIELD} />
                  <input value={scenario.time_horizon} onChange={e => setScenario({ ...scenario, time_horizon: e.target.value })}
                    placeholder="Time horizon" className={FIELD} />
                  <Button onClick={() => ask('scenario')} className="flex items-center gap-2 text-xs"
                    disabled={asking || !scenario.scenario_name.trim() || !scenario.scenario_description.trim()}>
                    {asking ? <Loader2 size={13} className="animate-spin" /> : <Activity size={13} />} Compose the scenario text
                  </Button>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-900 space-y-2">
                  <p className="text-[10px] font-black uppercase tracking-widest text-slate-400">Ask for an optimisation</p>
                  <input value={objective} onChange={e => setObjective(e.target.value)} placeholder="Objective" className={FIELD} />
                  <textarea value={constraints} onChange={e => setConstraints(e.target.value)} rows={2}
                    placeholder="Constraints, one per line (optional)" className={FIELD} />
                  <Button onClick={() => ask('optimisation')} disabled={asking || !objective.trim()}
                    className="flex items-center gap-2 text-xs">
                    {asking ? <Loader2 size={13} className="animate-spin" /> : <Activity size={13} />} Compose the optimisation text
                  </Button>
                </div>
              </div>
              {answer && (
                <div className="mt-4" data-testid="twin-answer">
                  <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1">
                    {answer.kind === 'scenario' ? 'Scenario' : 'Optimisation'}{answer.title ? ` · ${answer.title}` : ''}
                  </p>
                  <p className="text-[10px] text-amber-400/90 leading-relaxed mb-2" data-testid="twin-answer-basis">
                    {answer.basis ?? 'This answer does not say how its text was produced.'}
                  </p>
                  <pre className="text-[10px] text-slate-400 leading-relaxed whitespace-pre-wrap font-mono bg-slate-950 rounded-xl p-4 max-h-[460px] overflow-auto border border-slate-900">{answer.text || 'The answer carried no text.'}</pre>
                </div>
              )}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
