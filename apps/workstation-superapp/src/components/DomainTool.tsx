import React, { useState } from 'react';
import axios from 'axios';
import { Card, Button } from '@workstation/ui';
import { Loader2, Sparkles, Copy, Download, Check } from 'lucide-react';

export interface DomainField {
  name: string;
  label: string;
  type?: 'text' | 'textarea' | 'select' | 'keyvalue' | 'list' | 'claims';
  options?: string[];
  placeholder?: string;
  default?: string;
}

// A `keyvalue` field is edited as "key: value" lines and posted as an object under the field name.
function parseKeyValue(raw: string): Record<string, string> {
  const obj: Record<string, string> = {};
  (raw || '').split('\n').forEach((line) => {
    const i = line.indexOf(':');
    if (i > 0) {
      const k = line.slice(0, i).trim();
      if (k) obj[k] = line.slice(i + 1).trim();
    }
  });
  return obj;
}

// A `list` field is edited one-item-per-line and posted as an array of strings.
function parseList(raw: string): string[] {
  return (raw || '').split('\n').map((s) => s.trim()).filter(Boolean);
}

// A `claims` field is edited one-claim-per-line as "claim text | confidence | reputation" and posted
// as an array of {claim, confidence, reputation} objects (for the collective truth-consensus engine).
function parseClaims(raw: string): { claim: string; confidence: number; reputation: number }[] {
  return (raw || '').split('\n').map((line) => {
    const parts = line.split('|').map((p) => p.trim());
    const claim = parts[0] || '';
    const confidence = parts[1] !== undefined && parts[1] !== '' ? parseFloat(parts[1]) : 0.8;
    const reputation = parts[2] !== undefined && parts[2] !== '' ? parseFloat(parts[2]) : 1.0;
    return { claim, confidence: isNaN(confidence) ? 0.8 : confidence, reputation: isNaN(reputation) ? 1.0 : reputation };
  }).filter((c) => c.claim);
}

interface DomainToolProps {
  title: string;
  description: React.ReactNode;
  endpoint: string;          // e.g. /api/v1/science/synthesise
  fields: DomainField[];     // form fields -> POST body
  resultKey: string;         // response key holding the text result (falls back to JSON)
  submitLabel?: string;
}

/**
 * Reusable domain-tool form: renders fields, POSTs them to an in-house domain endpoint, and shows
 * the result with the in-house provenance badge (and any disclaimer). Used to make the solid
 * domain backends (Science/Care/Education/Law…) genuinely reachable by users — DRY across hubs.
 */
export const DomainTool: React.FC<DomainToolProps> = ({ title, description, endpoint, fields, resultKey, submitLabel = 'Generate' }) => {
  const [form, setForm] = useState<Record<string, string>>(() =>
    Object.fromEntries(fields.map(f => [f.name, f.default ?? ''])));
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Record<string, any> | null>(null);
  const [error, setError] = useState('');

  const primary = fields.find(f => f.type === 'textarea')?.name ?? fields[0]?.name;
  const canSubmit = !primary || (form[primary] || '').trim().length > 0;

  const [copied, setCopied] = useState(false);
  const [refineText, setRefineText] = useState('');
  const [refining, setRefining] = useState(false);
  const [refinedText, setRefinedText] = useState<string | null>(null);
  const [refineProv, setRefineProv] = useState<Record<string, any> | null>(null);
  const [refineCount, setRefineCount] = useState(0);

  const run = async () => {
    setBusy(true); setError(''); setResult(null);
    setRefinedText(null); setRefineProv(null); setRefineText(''); setRefineCount(0);
    try {
      const body: Record<string, any> = {};
      for (const f of fields) {
        body[f.name] = f.type === 'keyvalue' ? parseKeyValue(form[f.name])
          : f.type === 'list' ? parseList(form[f.name])
          : f.type === 'claims' ? parseClaims(form[f.name])
          : form[f.name];
      }
      const r = await axios.post(endpoint, body);
      setResult(r.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Request failed — the backend may be unavailable.');
    }
    setBusy(false);
  };

  const prov = result?.ai_provenance;
  const resultText = result ? String(result[resultKey] ?? result.deliverable ?? JSON.stringify(result, null, 2)) : '';
  // Iterative refinement: each refine builds on the currently-displayed text (in-house /api/v1/refine).
  const displayText = refinedText ?? resultText;
  const effectiveProv = refineProv ?? prov;

  const refine = async () => {
    if (!refineText.trim() || refining) return;
    setRefining(true);
    try {
      const r = await axios.post('/api/v1/refine', { previous: displayText, instruction: refineText, context: title });
      setRefinedText(String(r.data.refined ?? displayText));
      setRefineProv(r.data.ai_provenance ?? null);
      setRefineCount(c => c + 1);
      setRefineText('');
    } catch { /* keep current output */ }
    setRefining(false);
  };

  const copyResult = async () => {
    try { await navigator.clipboard.writeText(displayText); setCopied(true); setTimeout(() => setCopied(false), 1500); } catch { /* ignore */ }
  };
  const downloadResult = () => {
    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'result';
    const blob = new Blob([displayText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${slug}.md`;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-5">
      <div>
        <h4 className="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2"><Sparkles size={18} className="text-aura" /> {title}</h4>
        <p className="text-[11px] text-slate-500 font-bold mt-1 max-w-2xl leading-relaxed">{description}</p>
      </div>

      {fields.map(f => (
        <div key={f.name}>
          <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">{f.label}</label>
          {f.type === 'select' ? (
            <select aria-label={f.label} value={form[f.name]} onChange={e => setForm({ ...form, [f.name]: e.target.value })}
              className="block mt-1 text-[11px] font-black uppercase bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2">
              {(f.options || []).map(o => <option key={o} value={o}>{o}</option>)}
            </select>
          ) : (f.type === 'textarea' || f.type === 'keyvalue' || f.type === 'list' || f.type === 'claims') ? (
            <textarea aria-label={f.label} value={form[f.name]} onChange={e => setForm({ ...form, [f.name]: e.target.value })} rows={3}
              placeholder={f.placeholder || (f.type === 'keyvalue' ? 'one per line — key: value' : f.type === 'list' ? 'one item per line' : f.type === 'claims' ? 'one per line — claim | confidence | reputation' : undefined)}
              className={`block w-full mt-1 text-xs bg-slate-950 border border-slate-900 rounded-2xl p-3 text-slate-300 ${(f.type === 'keyvalue' || f.type === 'list' || f.type === 'claims') ? 'font-mono' : ''}`} />
          ) : (
            <input aria-label={f.label} value={form[f.name]} onChange={e => setForm({ ...form, [f.name]: e.target.value })}
              placeholder={f.placeholder}
              className="block w-full mt-1 text-xs bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-slate-300" />
          )}
        </div>
      ))}

      <Button type="button" onClick={run} disabled={busy || !canSubmit} className="bg-aura text-sovereign flex items-center gap-2 text-xs">
        {busy ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} {submitLabel}
      </Button>
      {error && <p className="text-vital text-xs font-bold">{error}</p>}

      {result && (
        <Card className="p-6 space-y-3">
          <div className="flex items-center justify-between gap-2 flex-wrap">
            <h4 className="text-sm font-black text-white uppercase tracking-wide">Result</h4>
            <div className="flex items-center gap-2">
              {refineCount > 0 && (
                <span className="text-[8px] font-black uppercase px-2 py-1 rounded bg-aura/15 text-aura">refined ×{refineCount}</span>
              )}
              {effectiveProv && (
                <span className={`text-[8px] font-black uppercase px-2 py-1 rounded ${effectiveProv.is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                  {effectiveProv.is_external ? `via ${effectiveProv.served_by}` : `in-house · ${effectiveProv.served_by ?? 'native'}`}
                </span>
              )}
              <button type="button" onClick={copyResult} aria-label="Copy result"
                className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1">
                {copied ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />} {copied ? 'Copied' : 'Copy'}
              </button>
              <button type="button" onClick={downloadResult} aria-label="Download result as Markdown"
                className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1">
                <Download size={11} /> .md
              </button>
            </div>
          </div>
          <pre className="text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 border border-slate-900 rounded-xl p-4 max-h-[420px] overflow-y-auto">
            {displayText}
          </pre>
          {result.disclaimer && <p className="text-[10px] text-slate-600 italic leading-relaxed">{result.disclaimer}</p>}

          {/* Iterative refinement — advance/develop/refine this output in-house, each step builds on the last */}
          <div className="pt-3 border-t border-slate-800/60 space-y-2">
            <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Refine this output</label>
            <div className="flex items-center gap-2 flex-wrap">
              <input aria-label="Refinement instruction" value={refineText} onChange={e => setRefineText(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') refine(); }}
                placeholder="e.g. make it more concise · add a risks section · adjust tone for a lay reader"
                className="flex-1 min-w-[220px] text-xs bg-slate-950 border border-slate-900 rounded-xl p-2.5 text-slate-300" />
              <Button type="button" onClick={refine} disabled={refining || !refineText.trim()} className="bg-slate-800 text-aura flex items-center gap-2 text-xs">
                {refining ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />} Refine
              </Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
