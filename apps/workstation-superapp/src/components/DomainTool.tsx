import React, { useState } from 'react';
import axios from 'axios';
import { Card, Button } from '@workstation/ui';
import { Loader2, Sparkles } from 'lucide-react';

export interface DomainField {
  name: string;
  label: string;
  type?: 'text' | 'textarea' | 'select' | 'keyvalue' | 'list';
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

  const run = async () => {
    setBusy(true); setError(''); setResult(null);
    try {
      const body: Record<string, any> = {};
      for (const f of fields) {
        body[f.name] = f.type === 'keyvalue' ? parseKeyValue(form[f.name])
          : f.type === 'list' ? parseList(form[f.name])
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
          ) : (f.type === 'textarea' || f.type === 'keyvalue' || f.type === 'list') ? (
            <textarea aria-label={f.label} value={form[f.name]} onChange={e => setForm({ ...form, [f.name]: e.target.value })} rows={3}
              placeholder={f.placeholder || (f.type === 'keyvalue' ? 'one per line — key: value' : f.type === 'list' ? 'one item per line' : undefined)}
              className={`block w-full mt-1 text-xs bg-slate-950 border border-slate-900 rounded-2xl p-3 text-slate-300 ${(f.type === 'keyvalue' || f.type === 'list') ? 'font-mono' : ''}`} />
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
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-black text-white uppercase tracking-wide">Result</h4>
            {prov && (
              <span className={`text-[8px] font-black uppercase px-2 py-1 rounded ${prov.is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                {prov.is_external ? `via ${prov.served_by}` : `in-house · ${prov.served_by ?? 'native'}`}
              </span>
            )}
          </div>
          <pre className="text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 border border-slate-900 rounded-xl p-4 max-h-[420px] overflow-y-auto">
            {String(result[resultKey] ?? result.deliverable ?? JSON.stringify(result, null, 2))}
          </pre>
          {result.disclaimer && <p className="text-[10px] text-slate-600 italic leading-relaxed">{result.disclaimer}</p>}
        </Card>
      )}
    </div>
  );
};
