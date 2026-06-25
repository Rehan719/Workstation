import React, { useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { BarChart3, LineChart, ScatterChart, Loader2, Sparkles } from 'lucide-react';

// ── Types ───────────────────────────────────────────────────────────────────
interface StudioPoint { label: string; value: number; z?: number | null }
interface StudioResult {
  title: string; domain: string; chart_type: string; dimensions: number;
  series: StudioPoint[];
  analytics: { count: number; total: number; mean: number; range: number;
    min: { label: string; value: number }; max: { label: string; value: number } };
  insight: string;
  ai_provenance: { any_external: boolean; served_by: Record<string, number> };
  quality_assurance?: { quality?: { qms_gate_passed?: boolean; document_controlled?: boolean;
    compliance?: { overall?: string; compliant?: boolean; verdicts?: { framework: string; status: string }[] } } };
}

// Parse "label, value[, z]" per line into points (real user data — never invented).
function parseSeries(text: string): StudioPoint[] {
  return text.split('\n').map(l => l.trim()).filter(Boolean).map(line => {
    const parts = line.split(/[,|]/).map(p => p.trim());
    const value = parseFloat(parts[1]);
    const z = parts[2] !== undefined && parts[2] !== '' ? parseFloat(parts[2]) : null;
    return { label: parts[0] || '?', value: isNaN(value) ? 0 : value, z: z != null && !isNaN(z) ? z : null };
  }).filter(p => p.label);
}

const CHARTS = [
  { id: 'bar', name: 'Bar', icon: BarChart3 },
  { id: 'line', name: 'Line', icon: LineChart },
  { id: 'scatter', name: 'Scatter (+z)', icon: ScatterChart },
];

// ── Chart renderer (real SVG; no fabricated data) ─────────────────────────────
const W = 640, H = 280, PAD = 40;
const Chart: React.FC<{ result: StudioResult }> = ({ result }) => {
  const pts = result.series;
  const vals = pts.map(p => p.value);
  const vmax = Math.max(...vals, 0), vmin = Math.min(...vals, 0);
  const span = vmax - vmin || 1;
  const x = (i: number) => PAD + (pts.length === 1 ? (W - 2 * PAD) / 2 : (i * (W - 2 * PAD)) / (pts.length - 1));
  const y = (v: number) => H - PAD - ((v - vmin) / span) * (H - 2 * PAD);
  const zs = pts.map(p => p.z ?? 0); const zmax = Math.max(...zs, 1);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={`${result.chart_type} chart`}>
      {/* baseline + axis labels */}
      <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} className="stroke-slate-700" strokeWidth={1} />
      <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} className="stroke-slate-700" strokeWidth={1} />
      <text x={PAD - 6} y={y(vmax) + 4} textAnchor="end" className="fill-slate-500 text-[9px]">{vmax}</text>
      <text x={PAD - 6} y={H - PAD + 4} textAnchor="end" className="fill-slate-500 text-[9px]">{vmin}</text>

      {result.chart_type === 'bar' && pts.map((p, i) => {
        const bw = Math.max(8, (W - 2 * PAD) / pts.length * 0.6);
        const bx = PAD + (i + 0.5) * ((W - 2 * PAD) / pts.length) - bw / 2;
        return <rect key={i} x={bx} y={y(p.value)} width={bw} height={(H - PAD) - y(p.value)}
          className="fill-current text-highlight" rx={2} />;
      })}

      {result.chart_type === 'line' && (
        <polyline fill="none" className="stroke-current text-highlight" strokeWidth={2}
          points={pts.map((p, i) => `${x(i)},${y(p.value)}`).join(' ')} />
      )}
      {result.chart_type === 'line' && pts.map((p, i) =>
        <circle key={i} cx={x(i)} cy={y(p.value)} r={3} className="fill-current text-highlight" />)}

      {result.chart_type === 'scatter' && pts.map((p, i) => {
        const bx = PAD + (i + 0.5) * ((W - 2 * PAD) / pts.length);
        const r = result.dimensions === 3 ? 4 + ((p.z ?? 0) / zmax) * 16 : 6;
        return <circle key={i} cx={bx} cy={y(p.value)} r={r} className="fill-current text-aura/70" />;
      })}

      {/* point labels */}
      {pts.map((p, i) => {
        const lx = result.chart_type === 'line' ? x(i) : PAD + (i + 0.5) * ((W - 2 * PAD) / pts.length);
        return <text key={i} x={lx} y={H - PAD + 14} textAnchor="middle" className="fill-slate-400 text-[9px]">{p.label}</text>;
      })}
    </svg>
  );
};

// ── Page ──────────────────────────────────────────────────────────────────────
export const ReactorStudio: React.FC = () => {
  const [title, setTitle] = useState('Quarterly halal-meal signups');
  const [domain, setDomain] = useState('enterprise');
  const [chartType, setChartType] = useState('bar');
  const [seriesText, setSeriesText] = useState('Q1, 120\nQ2, 180\nQ3, 150\nQ4, 240');
  const [result, setResult] = useState<StudioResult | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');

  const render = async () => {
    const series = parseSeries(seriesText);
    if (!series.length) { setError('Add at least one data point (label, value).'); return; }
    setRunning(true); setError(''); setResult(null);
    try {
      const r = await fetch('/api/v1/reactor/studio', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, domain, chart_type: chartType, series }),
      });
      if (!r.ok) { setError(`HTTP ${r.status}`); setRunning(false); return; }
      setResult(await r.json());
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setRunning(false);
  };

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Reactor · Studio</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Studio</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          The Reactor's <span className="text-highlight">2D/3D visual analytics &amp; insight</span> — render bar, line, or
          scatter charts over a <span className="text-highlight">real</span> data series, with computed statistics and an
          in-house insight narrative. Visualises the data you provide; never invents numbers.
        </p>
      </header>

      <Card className="p-6 space-y-4">
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-3">
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Chart title…"
            className="text-xs font-bold bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-white" />
          <input value={domain} onChange={e => setDomain(e.target.value)} placeholder="Domain…"
            className="text-xs bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-slate-300" />
        </div>
        <div className="flex flex-wrap gap-2">
          {CHARTS.map(c => (
            <button key={c.id} type="button" onClick={() => setChartType(c.id)}
              className={`flex items-center gap-1.5 text-[10px] font-black uppercase px-3 py-1.5 rounded-lg ${chartType === c.id ? 'bg-highlight text-sovereign' : 'bg-slate-900 text-slate-400'}`}>
              <c.icon size={12} /> {c.name}
            </button>
          ))}
        </div>
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-1 block">
            Data series — one per line: <span className="font-mono normal-case">label, value[, z]</span>
          </label>
          <textarea value={seriesText} onChange={e => setSeriesText(e.target.value)} rows={5}
            className="w-full text-xs font-mono bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300" />
        </div>
        <div className="flex items-center gap-3">
          <Button onClick={render} disabled={running} className="flex items-center gap-2 bg-highlight text-sovereign">
            {running ? <Loader2 size={15} className="animate-spin" /> : <Sparkles size={15} />} Render analytics
          </Button>
          {error && <p className="text-vital text-xs font-bold">{error}</p>}
        </div>
      </Card>

      {result && (
        <div className="grid grid-cols-1 @[900px]:grid-cols-[1fr_300px] gap-6">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-1">
              <h3 className="text-sm font-black text-white">{result.title}</h3>
              <span className="text-[9px] font-black uppercase text-slate-500">{result.dimensions}D · {result.chart_type}</span>
            </div>
            <Chart result={result} />
          </Card>
          <div className="space-y-4">
            <Card className="p-5">
              <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Analytics</h4>
              <dl className="space-y-1.5 text-[11px]">
                {[['Points', result.analytics.count], ['Total', result.analytics.total], ['Mean', result.analytics.mean],
                  ['Max', `${result.analytics.max.label} (${result.analytics.max.value})`],
                  ['Min', `${result.analytics.min.label} (${result.analytics.min.value})`],
                  ['Range', result.analytics.range]].map(([k, v]) => (
                  <div key={String(k)} className="flex justify-between"><dt className="text-slate-500">{k}</dt><dd className="text-white font-bold">{v}</dd></div>
                ))}
              </dl>
            </Card>
            <Card className="p-5">
              <div className="flex flex-wrap items-center gap-1.5 mb-2">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Insight</h4>
                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${!result.ai_provenance.any_external ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                  {!result.ai_provenance.any_external ? 'in-house' : 'external'}
                </span>
                {result.quality_assurance?.quality?.document_controlled && (
                  <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400">QMS · doc-controlled</span>
                )}
                {result.quality_assurance?.quality?.compliance && (
                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${result.quality_assurance.quality.compliance.compliant ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                    title={`§11 live compliance — ${(result.quality_assurance.quality.compliance.verdicts || []).map(v => `${v.framework}:${v.status}`).join(' · ')}`}>
                    compliance: {result.quality_assurance.quality.compliance.overall}
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-400 whitespace-pre-wrap leading-relaxed max-h-72 overflow-y-auto">{result.insight}</p>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};
