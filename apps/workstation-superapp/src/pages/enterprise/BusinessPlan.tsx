import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { Target, Loader2, Sparkles, Plus, CheckCircle2, Clock, AlertCircle, Crown } from 'lucide-react';

interface Objective { id: string; title: string; kpi: string; timeline: string; owner_role: string; progress_pct: number; status: string }
interface RoadmapPhase { timeline: string; progress_pct: number; complete: boolean; count: number; objectives: { title: string }[] }
interface Roadmap { living: boolean; phases: RoadmapPhase[]; overall_progress_pct: number; current_phase: string | null; next_milestone: { phase: string; title: string } | null; note?: string }
interface Plan { scope: string; owner: string; executive_summary: string; concept: string; mission: string; vision: string; strategy: string; aims: string[]; objectives: Objective[]; roadmap?: Roadmap; updated_at: string | null }

const STATUS_TONE: Record<string, string> = { done: 'text-emerald-400', in_progress: 'text-highlight', blocked: 'text-vital', planned: 'text-slate-500' };

export const BusinessPlan: React.FC = () => {
  const [plan, setPlan] = useState<Plan | null>(null);
  const [busy, setBusy] = useState(false);
  const [newObj, setNewObj] = useState({ title: '', kpi: '', timeline: '', owner_role: 'AI CEO' });
  const [orchestrating, setOrchestrating] = useState('');
  const [orchResult, setOrchResult] = useState<Record<string, any>>({});

  const load = () => fetch('/api/v1/business-plan?scope=workstation').then(r => r.json()).then(setPlan).catch(() => {});
  useEffect(() => { load(); }, []);

  const generate = async () => {
    setBusy(true);
    try { await fetch('/api/v1/business-plan/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scope: 'workstation' }) }); await load(); } catch {}
    setBusy(false);
  };
  const addObjective = async () => {
    if (!newObj.title.trim()) return;
    setBusy(true);
    try { await fetch('/api/v1/business-plan/objective', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scope: 'workstation', ...newObj }) }); setNewObj({ title: '', kpi: '', timeline: '', owner_role: 'AI CEO' }); await load(); } catch {}
    setBusy(false);
  };
  const review = async (oid: string, progress_pct: number, status: string) => {
    await fetch(`/api/v1/business-plan/objective/${oid}/review`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scope: 'workstation', progress_pct, status }) });
    load();
  };
  const orchestrate = async (oid: string) => {
    setOrchestrating(oid);
    try {
      const r = await fetch(`/api/v1/business-plan/objective/${oid}/orchestrate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scope: 'workstation' }) });
      const data = await r.json();
      if (r.ok && data?.tree) setOrchResult(m => ({ ...m, [oid]: data.tree }));
      await load();
    } catch { /* leave result unset; the run is best-effort */ }
    setOrchestrating('');
  };

  const overall = plan && plan.objectives.length ? Math.round(plan.objectives.reduce((s, o) => s + o.progress_pct, 0) / plan.objectives.length) : 0;

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">VSB · Living Business Plan</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Business Plan</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The living plan owned by your <span className="text-highlight">Chief</span> (your digital twin) and the Board —
          opening with <span className="text-highlight">Executive Summary · Concept · Vision</span>, then mission, strategy,
          and timelined objectives with KPIs, reviewed for progress. You set direction; the org delivers.
        </p>
      </header>

      {plan && (
        <>
          {(plan.executive_summary || plan.concept || plan.vision) && (
            <Card className="p-8 border-highlight/40 bg-gradient-to-br from-highlight/10 to-transparent">
              <div className="flex items-center gap-3 mb-4">
                <Crown size={18} className="text-highlight" />
                <h3 className="text-sm font-black text-white uppercase tracking-wide">Chief's Opening — Executive Summary · Concept · Vision</h3>
              </div>
              {plan.executive_summary && <Field label="Executive Summary" value={plan.executive_summary} />}
              {plan.concept && <Field label="Concept" value={plan.concept} />}
              {plan.vision && <Field label="Vision" value={plan.vision} />}
            </Card>
          )}

          <Card className="p-8 border-highlight/30 bg-highlight/5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3"><Crown size={18} className="text-highlight" /><h3 className="text-sm font-black text-white uppercase tracking-wide">Strategic Layer</h3></div>
              <Button onClick={generate} disabled={busy} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
                {busy ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} Chief: AI-Generate
              </Button>
            </div>
            {plan.mission && <Field label="Mission" value={plan.mission} />}
            {plan.strategy && <Field label="Strategy" value={plan.strategy} />}
            {plan.aims?.length > 0 && (
              <div className="mt-3">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mb-1">Aims</p>
                <div className="flex flex-wrap gap-2">{plan.aims.map((a, i) => <span key={i} className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 text-[10px] font-bold">{a}</span>)}</div>
              </div>
            )}
            <div className="flex items-end gap-3 mt-5 pt-4 border-t border-highlight/20">
              <span className="text-3xl font-black text-emerald-400">{overall}%</span>
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1.5">overall objective progress · {plan.objectives.length} objectives</span>
            </div>
          </Card>

          {plan.roadmap && plan.roadmap.phases.length > 0 && (
            <Card className="p-6 border-highlight/30">
              <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
                <h3 className="text-[10px] font-black uppercase tracking-widest text-highlight flex items-center gap-2"><Target size={14} /> Living roadmap</h3>
                <span className="text-[9px] font-black uppercase text-slate-500">overall {plan.roadmap.overall_progress_pct}% · current: {plan.roadmap.current_phase ?? '—'}</span>
              </div>
              <div className="space-y-3">
                {plan.roadmap.phases.map((ph, i) => (
                  <div key={i} className={`p-3 rounded-xl border ${ph.timeline === plan.roadmap!.current_phase ? 'bg-highlight/5 border-highlight/40' : 'bg-slate-900 border-slate-800'}`}>
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-[11px] font-black uppercase tracking-wider text-white">{ph.timeline}</p>
                      <span className="text-[9px] font-black text-highlight">{ph.progress_pct}% · {ph.count} obj{ph.complete ? ' ✓' : ''}</span>
                    </div>
                    <div className="mt-2 h-1.5 rounded-full bg-slate-800 overflow-hidden"><div className="h-full bg-highlight" style={{ width: `${ph.progress_pct}%` }} /></div>
                    <div className="mt-2 flex flex-wrap gap-x-3 gap-y-0.5">{ph.objectives.map((o, j) => <span key={j} className="text-[9px] text-slate-400">· {o.title}</span>)}</div>
                  </div>
                ))}
              </div>
              {plan.roadmap.next_milestone && <p className="text-[10px] text-slate-500 mt-3">Next milestone: <span className="text-white font-bold">{plan.roadmap.next_milestone.title}</span> ({plan.roadmap.next_milestone.phase})</p>}
            </Card>
          )}

          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Target size={14} /> Objectives</h3>
            <div className="space-y-3">
              {plan.objectives.map(o => (
                <Card key={o.id} className="p-5">
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="min-w-0">
                      <p className="font-black text-white text-sm">{o.title}</p>
                      <p className="text-[10px] text-slate-500 mt-0.5">{o.kpi && `KPI: ${o.kpi} · `}{o.timeline && `${o.timeline} · `}owner {o.owner_role}</p>
                    </div>
                    <span className={`text-[10px] font-black uppercase shrink-0 ${STATUS_TONE[o.status] ?? 'text-slate-500'}`}>{o.progress_pct}% · {o.status.replace('_', ' ')}</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden mb-3"><div className="h-full bg-highlight transition-all" style={{ width: `${o.progress_pct}%` }} /></div>
                  <div className="flex gap-2 flex-wrap">
                    <button type="button" onClick={() => review(o.id, Math.min(100, o.progress_pct + 25), o.progress_pct + 25 >= 100 ? 'done' : 'in_progress')} className="text-[9px] font-black uppercase text-highlight border border-highlight/30 px-2 py-1 rounded">+25% progress</button>
                    <button type="button" onClick={() => review(o.id, o.progress_pct, 'blocked')} className="text-[9px] font-black uppercase text-vital border border-vital/30 px-2 py-1 rounded">Mark blocked</button>
                    <button type="button" onClick={() => orchestrate(o.id)} disabled={orchestrating === o.id} className="text-[9px] font-black uppercase text-aura border border-aura/30 px-2 py-1 rounded flex items-center gap-1 disabled:opacity-50">
                      {orchestrating === o.id ? <Loader2 size={10} className="animate-spin" /> : <Crown size={10} />} Chief: deliver via tree
                    </button>
                  </div>
                  {orchResult[o.id] && (
                    <div className="mt-3 p-3 rounded-xl bg-aura/5 border border-aura/20">
                      <div className="flex items-center flex-wrap gap-2 mb-1.5">
                        <span className="text-[8px] font-black uppercase tracking-widest text-aura">Chief workflow-tree</span>
                        <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-highlight/15 text-highlight">decision: {orchResult[o.id].decision?.recommendation ?? '—'}</span>
                        <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${orchResult[o.id].consensus?.choice === 'proceed' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>consensus: {orchResult[o.id].consensus?.choice ?? 'none'}</span>
                        <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{orchResult[o.id].node_count} nodes</span>
                        {orchResult[o.id].ueg_hash && <span className="text-[8px] font-mono text-slate-600" title={orchResult[o.id].ueg_hash}>UEG {orchResult[o.id].ueg_hash.slice(0, 12)}…</span>}
                      </div>
                      <p className="text-[10px] text-slate-400 whitespace-pre-wrap line-clamp-4">{orchResult[o.id].final}</p>
                    </div>
                  )}
                </Card>
              ))}
            </div>
          </div>

          <Card className="p-6">
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Plus size={14} /> Add Objective</h3>
            <div className="grid grid-cols-1 @[560px]:grid-cols-4 gap-2 mb-3">
              <input value={newObj.title} onChange={e => setNewObj({ ...newObj, title: e.target.value })} placeholder="Objective" className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white @[560px]:col-span-2" />
              <input value={newObj.kpi} onChange={e => setNewObj({ ...newObj, kpi: e.target.value })} placeholder="KPI" className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white" />
              <input value={newObj.timeline} onChange={e => setNewObj({ ...newObj, timeline: e.target.value })} placeholder="Timeline" className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white" />
            </div>
            <Button onClick={addObjective} disabled={busy || !newObj.title.trim()} className="bg-highlight text-sovereign text-xs flex items-center gap-2"><Plus size={13} /> Add</Button>
          </Card>
        </>
      )}
    </div>
  );
};

const Field: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="mb-3">
    <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mb-1">{label}</p>
    <p className="text-sm text-slate-300 leading-relaxed">{value}</p>
  </div>
);
