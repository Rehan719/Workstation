import React, { useEffect, useState } from 'react';
import { Card } from '@workstation/ui';
import { Boxes, Loader2, Activity, ChevronRight } from 'lucide-react';

// W481 (FU-122, sweep S8.1) — the transformation cascade writes a PROJECTION (arithmetic over two live
// readings), never a simulation; records written before W481 carry the old `simulations` shape and its
// 'stable-and-improving' verdict, which was impossible by construction. Both are rendered as projections.
interface Projection { of?: string; formula?: string; projected?: number; current?: number; note?: string;
  compared_with_current?: string }
interface Simulation { scenario?: string; verdict?: string; projected_realisation?: number; time_horizon?: string }
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
  created_at?: string;
}

export const DigitalTwins: React.FC = () => {
  const [models, setModels] = useState<TwinModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<TwinModel | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    fetch('/api/v1/twin/models')
      .then(r => r.json())
      .then(d => setModels(d.models ?? (Array.isArray(d) ? d : [])))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const open = async (m: TwinModel) => {
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
          projection (arithmetic over live readings), not a simulation.
        </p>
      </header>

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
              ) : selected.trained === undefined && (selected.simulations?.length || /vision_realisation|owner twin/i.test(selected.model_spec || '')) ? (
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
                  {selected.simulations.map((s, i) => (
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
              <pre className="text-[10px] text-slate-400 leading-relaxed whitespace-pre-wrap font-mono bg-slate-950 rounded-xl p-4 max-h-[460px] overflow-auto border border-slate-900">{selected.model_spec ?? 'No model spec.'}</pre>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
