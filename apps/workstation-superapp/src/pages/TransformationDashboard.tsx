import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import {
  Target, Activity, GitBranch, CheckCircle2, Circle, Loader2,
  Sparkles, HeartPulse, AlertCircle, Eye, Map,
} from 'lucide-react';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Evidence { label: string; met: boolean }
interface Pillar { id: string; pillar: string; realisation: number; status: string; evidence: Evidence[] }
interface Picture {
  vision_summary: string;
  realisation: { overall_realisation: number; pillars: Pillar[]; evidence_counts: Record<string, any> };
  transformation_plan: { immediate_gaps: { pillar: string; realisation: number; missing: string[] }[]; short_term: string[]; long_term: string[] };
}

function tone(status: string) {
  return status === 'realised' ? 'text-emerald-400' : status === 'partial' ? 'text-amber-400' : 'text-slate-500';
}
function barColor(status: string) {
  return status === 'realised' ? 'bg-emerald-400' : status === 'partial' ? 'bg-amber-400' : 'bg-slate-600';
}

// ── Component ─────────────────────────────────────────────────────────────────

export const TransformationDashboard: React.FC = () => {
  const [pic, setPic] = useState<Picture | null>(null);
  const [assessing, setAssessing] = useState(false);
  const [ticking, setTicking] = useState(false);
  const [assessment, setAssessment] = useState('');
  const [error, setError] = useState('');

  const load = () => fetch('/api/v1/transformation').then(r => r.json()).then(setPic).catch(() => setError('Failed to load'));
  useEffect(() => { load(); }, []);

  const tick = async () => {
    setTicking(true);
    try { await fetch('/api/v1/transformation/tick', { method: 'POST' }); await load(); } catch {}
    setTicking(false);
  };
  const assess = async () => {
    setAssessing(true); setAssessment('');
    try {
      const r = await fetch('/api/v1/transformation/assess', { method: 'POST' });
      const d = await r.json(); setAssessment(d.assessment ?? '');
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setAssessing(false);
  };

  const overall = pic ? Math.round(pic.realisation.overall_realisation * 100) : 0;

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Living Alignment</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Vision · Realisation · Transformation</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          One living picture, computed from the live organism: <span className="text-highlight">your vision</span>, how far the
          <span className="text-highlight"> current state realises it</span>, and the <span className="text-highlight">transformation plan</span> to close the gap.
          Continuously self-introspecting.
        </p>
      </header>

      {error && <p className="text-vital text-xs font-bold flex items-center gap-2"><AlertCircle size={14} /> {error}</p>}

      {pic && (
        <>
          {/* Overall realisation */}
          <Card className="p-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3"><Eye size={18} className="text-highlight" /><h3 className="text-sm font-black text-white uppercase tracking-wide">Vision Realisation</h3></div>
              <div className="flex gap-2">
                <Button onClick={tick} disabled={ticking} className="flex items-center gap-2 bg-slate-800 text-white text-xs">
                  {ticking ? <Loader2 size={14} className="animate-spin" /> : <HeartPulse size={14} />} Tick
                </Button>
                <Button onClick={assess} disabled={assessing} className="flex items-center gap-2 bg-highlight text-sovereign text-xs">
                  {assessing ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} AI Assess
                </Button>
              </div>
            </div>
            <p className="text-slate-400 text-sm font-bold leading-relaxed mb-4">{pic.vision_summary}</p>
            <div className="flex items-end gap-3 mb-2">
              <span className="text-5xl font-black text-emerald-400">{overall}%</span>
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2">overall realised</span>
            </div>
            <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-emerald-400 to-highlight transition-all duration-700" style={{ width: `${overall}%` }} />
            </div>
            {assessment && (
              <div className="mt-5 p-4 rounded-2xl bg-slate-950 border border-highlight/20">
                <p className="text-[10px] font-black uppercase tracking-widest text-highlight mb-2">AI Assessment</p>
                <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{assessment}</p>
              </div>
            )}
          </Card>

          {/* Pillars — vision mapped to live evidence */}
          <div>
            <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Target size={14} /> Vision Pillars (computed from live evidence)</h3>
            <div className="space-y-3">
              {pic.realisation.pillars.map(p => (
                <Card key={p.id} className="p-5">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-black text-white text-sm">{p.pillar}</p>
                    <span className={`text-[10px] font-black uppercase ${tone(p.status)}`}>{Math.round(p.realisation * 100)}% · {p.status}</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden mb-3">
                    <div className={`h-full ${barColor(p.status)} transition-all duration-500`} style={{ width: `${p.realisation * 100}%` }} />
                  </div>
                  <div className="flex flex-wrap gap-x-4 gap-y-1">
                    {p.evidence.map((e, i) => (
                      <span key={i} className="flex items-center gap-1.5 text-[10px] font-bold">
                        {e.met ? <CheckCircle2 size={11} className="text-emerald-400" /> : <Circle size={11} className="text-slate-600" />}
                        <span className={e.met ? 'text-slate-400' : 'text-slate-600'}>{e.label}</span>
                      </span>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Transformation plan */}
          <Card className="p-6 border-highlight/30 bg-highlight/5">
            <h3 className="font-black text-highlight uppercase tracking-widest text-sm mb-4 flex items-center gap-2"><GitBranch size={16} /> Transformation Plan (gap → action)</h3>
            {pic.transformation_plan.immediate_gaps.length > 0 && (
              <div className="mb-4">
                <p className="text-[10px] font-black uppercase tracking-widest text-amber-400 mb-2">Immediate gaps</p>
                <div className="space-y-2">
                  {pic.transformation_plan.immediate_gaps.map((g, i) => (
                    <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <p className="text-sm text-slate-300 font-bold">{g.pillar} <span className="text-amber-400 text-[10px]">({Math.round(g.realisation * 100)}%)</span></p>
                      <p className="text-[10px] text-slate-600 mt-0.5">missing: {g.missing.join(' · ')}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-4">
              <PlanList title="Short term" items={pic.transformation_plan.short_term} icon={Map} />
              <PlanList title="Long term" items={pic.transformation_plan.long_term} icon={Map} />
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

const PlanList: React.FC<{ title: string; items: string[]; icon: React.ComponentType<any> }> = ({ title, items, icon: Icon }) => (
  <div>
    <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 flex items-center gap-1.5"><Icon size={12} /> {title}</p>
    <ul className="space-y-1.5">
      {items.map((it, i) => <li key={i} className="text-[11px] text-slate-500 leading-relaxed flex gap-2"><span className="text-slate-700">›</span>{it}</li>)}
    </ul>
  </div>
);
