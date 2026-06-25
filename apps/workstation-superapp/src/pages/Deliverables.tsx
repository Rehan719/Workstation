import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { FileText, Loader2, Sparkles, RefreshCw, Layers, Download } from 'lucide-react';

interface DType { id: string; sections: string[] }
interface DeliverableSummary {
  id: string; type: string; title: string; vsb_id?: string;
  versions: number; served_by?: string; updated_at?: string; qms_gate_passed?: boolean | null;
}
interface QualityAssurance {
  quality?: { qms_gate_passed?: boolean; delivery_coverage?: number; bar?: string[];
    qms_non_conformance_rate?: number };
  biomimetic?: { immune?: { health?: number }; circadian?: string; layers?: string[]; self?: string };
}
interface Deliverable {
  id: string; type: string; title: string; brief: string; sections: string[];
  content: string; ai_provenance: { posture: string; served_by: string; is_external: boolean };
  quality_assurance?: QualityAssurance;
  versions: { created_at: string }[];
}

export const Deliverables: React.FC = () => {
  const [types, setTypes] = useState<DType[]>([]);
  const [list, setList] = useState<DeliverableSummary[]>([]);
  const [type, setType] = useState('report');
  const [title, setTitle] = useState('');
  const [brief, setBrief] = useState('a halal, zero-waste community meal service for elderly Londoners');
  const [producing, setProducing] = useState(false);
  const [selected, setSelected] = useState<Deliverable | null>(null);
  const [regenBrief, setRegenBrief] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [dlFormat, setDlFormat] = useState('md');   // §4.9 — selectable in-house export format
  // The live export formats are fetched from the backend so the selector reflects REAL capability
  // (e.g. PDF appears only when the in-house renderer is available). Falls back to the always-on set.
  const [formats, setFormats] = useState<{ id: string; label: string }[]>([
    { id: 'md', label: 'Markdown (.md)' }, { id: 'html', label: 'HTML document (.html)' },
    { id: 'slides', label: 'Presentation (.html)' }, { id: 'txt', label: 'Plain text (.txt)' },
    { id: 'json', label: 'JSON (.json)' },
  ]);

  const loadList = () =>
    fetch('/api/v1/deliverables').then(r => r.json()).then(d => setList(d.deliverables || [])).catch(() => {});

  useEffect(() => {
    fetch('/api/v1/deliverables/types').then(r => r.json()).then(d => setTypes(d.types || [])).catch(() => setError('Failed to load types'));
    fetch('/api/v1/deliverables/output-formats').then(r => r.json())
      .then(d => { if (Array.isArray(d.live) && d.live.length) setFormats(d.live.map((f: any) => ({ id: f.id, label: f.label }))); })
      .catch(() => {});
    loadList().finally(() => setLoading(false));
  }, []);

  const produce = async () => {
    if (!brief.trim()) return;
    setProducing(true); setError('');
    try {
      const r = await fetch('/api/v1/deliverables/produce', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, title, brief }),
      });
      const d = await r.json();
      setSelected(d);
      await loadList();
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setProducing(false);
  };

  const open = async (id: string) => {
    try { setSelected(await fetch(`/api/v1/deliverables/${id}`).then(r => r.json())); } catch { /* */ }
  };

  const regenerate = async () => {
    if (!selected) return;
    setBusy(true);
    try {
      const r = await fetch(`/api/v1/deliverables/${selected.id}/regenerate`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brief: regenBrief || undefined }),
      });
      setSelected(await r.json());
      setRegenBrief('');
      await loadList();
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setBusy(false);
  };

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Living Deliverables</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">Living Deliverables</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Reports · presentations · websites · apps · services — produced on Workstation's <span className="text-highlight">own</span> AI
          fabric and kept <span className="text-highlight">living</span>: re-generate and reconfigure any deliverable at any time, with full
          version history and in-house provenance.
        </p>
      </header>

      {error && <p className="text-vital text-xs font-bold">{error}</p>}

      {/* Produce */}
      <Card className="p-6 border-aura/30">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-aura mb-3 flex items-center gap-2"><Sparkles size={14} /> Produce a deliverable</h3>
        <div className="flex flex-wrap gap-2 mb-3">
          {types.map(t => (
            <button key={t.id} onClick={() => setType(t.id)}
              className={`text-[10px] font-black uppercase px-3 py-1.5 rounded-lg ${type === t.id ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-400'}`}>
              {t.id}
            </button>
          ))}
        </div>
        <input value={title} onChange={e => setTitle(e.target.value)}
          className="w-full text-xs font-bold bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-white mb-2"
          placeholder="Title (optional)…" />
        <textarea value={brief} onChange={e => setBrief(e.target.value)} rows={2}
          className="w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300 mb-3"
          placeholder="Brief — what should this deliverable cover?" />
        <Button onClick={produce} disabled={producing || !brief.trim()} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
          {producing ? <Loader2 size={13} className="animate-spin" /> : <FileText size={13} />} Produce {type}
        </Button>
      </Card>

      <div className="grid grid-cols-1 @[900px]:grid-cols-[280px_1fr] gap-6">
        {/* List */}
        <div>
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Layers size={14} /> Deliverables ({list.length})</h3>
          <div className="space-y-2">
            {loading && <p className="text-[11px] text-slate-600">Loading…</p>}
            {!loading && list.length === 0 && <p className="text-[11px] text-slate-600">None yet — produce one above.</p>}
            {list.map(d => (
              <button key={d.id} onClick={() => open(d.id)}
                className={`w-full text-left p-3 rounded-xl border ${selected?.id === d.id ? 'border-aura/50 bg-aura/5' : 'border-slate-900 bg-slate-950'}`}>
                <p className="text-xs font-black text-white truncate">{d.title}</p>
                <p className="text-[9px] font-bold uppercase text-slate-600 mt-0.5 flex items-center gap-1.5">
                  {d.type} · v{d.versions} · {d.served_by}
                  {typeof d.qms_gate_passed === 'boolean' && (
                    <span className={d.qms_gate_passed ? 'text-emerald-400' : 'text-vital'} title={`Living-QMS gate: ${d.qms_gate_passed ? 'pass' : 'fail'}`}>● QMS</span>
                  )}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Detail */}
        <div>
          {!selected && <p className="text-[11px] text-slate-600">Select or produce a deliverable to view it.</p>}
          {selected && (
            <Card className="p-6">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <p className="text-[9px] font-black uppercase tracking-widest text-highlight">{selected.type} · v{selected.versions.length}</p>
                  <h3 className="text-lg font-black text-white">{selected.title}</h3>
                </div>
                <span className={`text-[8px] font-black uppercase px-2 py-1 rounded ${selected.ai_provenance.is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                  {selected.ai_provenance.is_external ? `via ${selected.ai_provenance.served_by}` : `in-house · ${selected.ai_provenance.served_by}`}
                </span>
              </div>
              {/* Continual operational delivery within the living QMS — §10 bar + §8 organism */}
              {selected.quality_assurance?.quality && (
                <div className="flex flex-wrap items-center gap-1.5 mb-3">
                  {typeof selected.quality_assurance.quality.qms_gate_passed === 'boolean' && (
                    <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${selected.quality_assurance.quality.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-vital/15 text-vital'}`}
                      title={`§10 Solution-Quality Bar: ${(selected.quality_assurance.quality.bar || []).join(' · ')}`}>
                      Living-QMS gate: {selected.quality_assurance.quality.qms_gate_passed ? 'pass' : 'fail'} · cov {Math.round((selected.quality_assurance.quality.delivery_coverage || 0) * 100)}%
                    </span>
                  )}
                  {selected.quality_assurance.biomimetic?.immune && (
                    <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-violet-500/15 text-violet-300"
                      title={`7 biomimetic layers · ${selected.quality_assurance.biomimetic.self || ''}`}>
                      organism: immune {Math.round((selected.quality_assurance.biomimetic.immune.health ?? 0) * 100)}% · {selected.quality_assurance.biomimetic.circadian}
                    </span>
                  )}
                </div>
              )}
              <pre className="text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 border border-slate-900 rounded-xl p-4 max-h-[420px] overflow-y-auto">{selected.content}</pre>
              <div className="mt-3 flex items-end gap-2">
                <input value={regenBrief} onChange={e => setRegenBrief(e.target.value)}
                  className="flex-1 text-[11px] bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-slate-300"
                  placeholder="Reconfigure the brief, then regenerate (blank = re-run as-is)…" />
                <Button onClick={regenerate} disabled={busy} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[11px]">
                  {busy ? <Loader2 size={12} className="animate-spin" /> : <RefreshCw size={12} />} Regenerate
                </Button>
                <select value={dlFormat} onChange={e => setDlFormat(e.target.value)} aria-label="Export format"
                  className="text-[11px] bg-slate-950 border border-slate-800 rounded-xl p-2 text-slate-300">
                  {formats.map(f => <option key={f.id} value={f.id}>{f.label}</option>)}
                </select>
                <a href={`/api/v1/deliverables/${selected.id}/export?format=${dlFormat}`} download
                  className="flex items-center gap-1.5 bg-aura text-sovereign text-[11px] font-bold px-3 py-2 rounded-xl hover:opacity-90">
                  <Download size={12} /> Download
                </a>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
