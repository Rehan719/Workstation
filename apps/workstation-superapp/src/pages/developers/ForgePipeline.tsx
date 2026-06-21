import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { Hammer, Loader2, AlertCircle, Check, ChevronDown, ChevronUp, Rocket, FlaskConical } from 'lucide-react';

interface Resource { id: string; name: string; role: string; biomimetic: string }
interface StageOutput { resource: string; name: string; biomimetic: string; output: string }
interface RunResult { run_id: string; pipeline: string[]; ceo_framing: string; stage_outputs: StageOutput[]; integrated_deliverable: string; governance: string }

export const ForgePipeline: React.FC = () => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [selected, setSelected] = useState<string[]>(['petri_dish', 'laboratory', 'factory']);
  const [objective, setObjective] = useState('');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<RunResult | null>(null);
  const [open, setOpen] = useState<string>('deliverable');

  useEffect(() => { fetch('/api/v1/forge/resources').then(r => r.json()).then(d => setResources(d.resources ?? [])).catch(() => {}); }, []);

  const toggle = (id: string) => setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id]);

  const run = async () => {
    if (!objective.trim()) return;
    setRunning(true); setError(''); setResult(null);
    try {
      const r = await fetch('/api/v1/forge/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ objective, stages: selected.map(t => ({ type: t })) }) });
      if (!r.ok) { setError(`HTTP ${r.status}`); setRunning(false); return; }
      setResult(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Forge</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Digital Resource Forge</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Compose the IDBO's digital resources — Petri Dish · Incubator · Laboratory · Factory · Generator · Simulator · Reactor —
          into a <span className="text-highlight">swarm-orchestrated cascade pipeline</span> (AI CEO frames → resources process → CoE integrates),
          producing integrated multi-type outputs for Concept→Commercialisation.
        </p>
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
          <div className="text-[9px] font-mono text-slate-500">{result.run_id} · {result.pipeline.join(' → ')} · governance {result.governance}</div>
          {result.stage_outputs.map((s, i) => (
            <Card key={i} className="p-0 overflow-hidden border-slate-800/80">
              <button type="button" onClick={() => setOpen(open === s.resource ? '' : s.resource)} className={`w-full flex items-center justify-between p-4 text-left ${open === s.resource ? 'bg-slate-800/30' : ''}`}>
                <div className="flex items-center gap-3"><FlaskConical size={13} className="text-highlight" /><p className="font-black text-white text-sm">{s.name}</p><span className="text-[9px] text-slate-600 italic">{s.biomimetic}</span></div>
                {open === s.resource ? <ChevronUp size={13} className="text-slate-500" /> : <ChevronDown size={13} className="text-slate-500" />}
              </button>
              {open === s.resource && <div className="px-4 pb-5 border-t border-slate-800/50 pt-3"><p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{s.output}</p></div>}
            </Card>
          ))}
          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <div className="flex items-center gap-2 mb-3"><Rocket size={16} className="text-highlight" /><h3 className="font-black text-highlight uppercase tracking-widest text-sm">Integrated Deliverable</h3></div>
            <p className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">{result.integrated_deliverable}</p>
            <p className="text-[10px] text-slate-500 mt-3">Next: establish this as a living VSB IDBO entity via Genesis.</p>
          </Card>
        </div>
      )}
    </div>
  );
};
