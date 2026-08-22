import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Button } from '@workstation/ui';
import { Loader2, Sparkles, Copy, Download, Check, Rocket } from 'lucide-react';
import { AttachDocument, appendDocBlock } from './AttachDocument';
import { DictateButton } from './DictateButton';
import { saveOutput } from '../lib/outputHistory';
import { getPrefs } from '../lib/userPrefs';

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
  const navigate = useNavigate();
  const [form, setForm] = useState<Record<string, string>>(() =>
    Object.fromEntries(fields.map(f => [f.name, f.default ?? ''])));
  // Offering-1 -> Offering-2 bridge (WHOLE_VISION §3A): the domain segment is the endpoint's 4th part
  // (/api/v1/<domain>/...), used to deep-link a seeded Genesis Concept->Commercialisation journey.
  const domainSeed = endpoint.match(/\/api\/v1\/([a-z0-9-]+)\//)?.[1] ?? '';
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Record<string, any> | null>(null);
  const [error, setError] = useState('');

  const primary = fields.find(f => f.type === 'textarea')?.name ?? fields[0]?.name;
  const canSubmit = !primary || (form[primary] || '').trim().length > 0;

  // §9/§4.1 multimodal "bring your own data" — attach a text document; its content is inserted into the
  // primary field (via the shared AttachDocument control), so it flows into the tool within the contract.
  const primaryField = fields.find(f => f.name === primary);
  const canAttach = !!primary && (primaryField?.type === undefined || primaryField?.type === 'text' || primaryField?.type === 'textarea');

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
      // E3 — save to "My Work" history so the output is revisitable (not lost on navigate).
      try {
        const text = String(r.data?.[resultKey] ?? r.data?.deliverable ?? JSON.stringify(r.data, null, 2));
        saveOutput({ kind: 'domain-tool', title, domain: domainSeed, endpoint,
          input: primary ? form[primary] : undefined, output: text, provenance: r.data?.ai_provenance ?? null });
      } catch { /* history is best-effort */ }
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
  // E4 — output-format selection (§4.9): export the result in any real, in-house-producible text format.
  const downloadAs = (fmt: 'md' | 'txt' | 'html' | 'json') => {
    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'result';
    let content = displayText, mime = 'text/plain';
    if (fmt === 'md') { mime = 'text/markdown'; }
    else if (fmt === 'html') {
      mime = 'text/html';
      const esc = displayText.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      content = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>body{font:16px/1.6 system-ui,-apple-system,sans-serif;max-width:48rem;margin:2rem auto;padding:0 1rem;color:#0f172a}h1{font-size:1.4rem}pre{white-space:pre-wrap;word-wrap:break-word;font-family:inherit}</style></head><body><h1>${title}</h1><pre>${esc}</pre></body></html>`;
    } else if (fmt === 'json') {
      mime = 'application/json';
      content = JSON.stringify({ title, output: displayText, provenance: effectiveProv ?? null, generated_at: new Date().toISOString() }, null, 2);
    }
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${slug}.${fmt}`;
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

      {canAttach && primary && (
        <div className="flex items-start gap-2 flex-wrap">
          <AttachDocument
            hint="your own data — research, reviews, notes (read in-browser, stays with this request)"
            onText={block => setForm(prev => ({ ...prev, [primary]: appendDocBlock(prev[primary], block) }))} />
          <DictateButton lang={getPrefs().language || 'en-US'} onTranscript={text => setForm(prev => ({ ...prev, [primary]: (prev[primary] ? prev[primary] + ' ' : '') + text }))} />
        </div>
      )}

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
              {/* §10×§11 (W308) — every Offering-1 response carries its real QMS + compliance posture */}
              {effectiveProv?.quality_assurance && (
                <span title={`coverage ${effectiveProv.quality_assurance.delivery_coverage} · compliance ${effectiveProv.quality_assurance.compliance_overall ?? 'n/a'}`}
                  className={`text-[8px] font-black uppercase px-2 py-1 rounded ${effectiveProv.quality_assurance.qms_gate_passed ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
                  QMS {effectiveProv.quality_assurance.qms_gate_passed ? 'pass' : 'flagged'}
                </span>
              )}
              <button type="button" onClick={copyResult} aria-label="Copy result"
                className="text-[8px] font-black uppercase px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1">
                {copied ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />} {copied ? 'Copied' : 'Copy'}
              </button>
              <span className="inline-flex items-center rounded bg-slate-800 overflow-hidden">
                <span className="text-[8px] font-black uppercase px-1.5 text-slate-500 flex items-center"><Download size={10} /></span>
                {(['md', 'txt', 'html', 'json'] as const).map(fmt => (
                  <button key={fmt} type="button" onClick={() => downloadAs(fmt)} aria-label={`Download as ${fmt.toUpperCase()}`}
                    className="text-[8px] font-black uppercase px-1.5 py-1 text-slate-300 hover:text-white hover:bg-slate-700">
                    {fmt}
                  </button>
                ))}
              </span>
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

          {/* Offering 1 -> Offering 2 (§3A): take this work end-to-end into a living VSB IDBO enterprise */}
          {primary && (form[primary] || '').trim() && (
            <div className="pt-3 border-t border-slate-800/60 flex items-center justify-between gap-3 flex-wrap">
              <p className="text-[10px] text-slate-500 leading-relaxed max-w-sm">
                Want to take this further? Commercialise it end-to-end into your own self-running <span className="text-highlight font-bold">VSB IDBO enterprise</span>.
              </p>
              <Button type="button"
                onClick={() => { const sid = `seed_${Date.now().toString(36)}`; try { sessionStorage.setItem(`ws_genesis_${sid}`, JSON.stringify({ title, domain: domainSeed, input: primary ? form[primary] : '', output: String(result?.[resultKey] ?? result?.deliverable ?? '') })); } catch { /* seed best-effort */ } navigate(`/genesis?seed=${sid}${domainSeed ? `&domain=${encodeURIComponent(domainSeed)}` : ''}`); }}
                className="bg-highlight text-sovereign flex items-center gap-2 text-xs shrink-0">
                <Rocket size={14} /> Commercialise via Genesis
              </Button>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};
