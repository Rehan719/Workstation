import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { ClipboardCheck, Loader2 } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

// W690 — THE REVIEW CELL'S RECORDS, ON A PAGE (Owner ruling 2026-10-12). Every record of a review, whether it
// counts and why not, and the one form that records one. EVERY SENTENCE ABOUT A RECORD IS THE SERVER'S: the
// label a tool carries, why a record does not count, that a credential is unverified, and each refusal. The
// page decides nothing about a record - the route does, and what it answers is what is shown.

interface Rec {
  record_id: string; tool: string; tier: string; date: string; counts: boolean; why_not: string | null;
  entered_by?: string; entered_at?: string; name?: string; credential_as_stated?: string; lapses_on?: string;
  rule?: string; test?: string; checklist?: string; model?: string; agent?: string;
}
interface Listing { records: Rec[]; total: number; counted: number; tools: Record<string, string>; credential_basis: string; basis: string }

const TIERS: { id: string; fields: string[] }[] = [
  { id: 'checked_by_rule', fields: ['rule', 'test'] },
  { id: 'reviewed_by_workstation_agent', fields: ['agent', 'checklist', 'sources_read', 'model', 'could_not_check'] },
  { id: 'signed_by_a_qualified_person', fields: ['name', 'credential_as_stated', 'reviewed', 'lapses_on'] },
];
const FIELD_LABEL: Record<string, string> = {
  agent: 'The agent that reviewed (its calibration is read from its recorded run)',
  rule: 'The rule', test: 'The test that runs it', checklist: 'The checklist used', sources_read: 'Sources read (comma-separated ids)',
  model: 'The model that reviewed', could_not_check: 'What it could not check', name: 'The person’s name',
  credential_as_stated: 'Their credential, as they state it', reviewed: 'What was reviewed', lapses_on: 'Lapses on (YYYY-MM-DD)',
};
const inputCls = 'text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300';

export const ReviewRecords: React.FC = () => {
  const [listing, setListing] = useState<Listing | null>(null);
  const [loadErr, setLoadErr] = useState('');
  const [err, setErr] = useState('');
  const [said, setSaid] = useState('');
  const [busy, setBusy] = useState(false);
  const [tool, setTool] = useState('');
  const [tier, setTier] = useState(TIERS[0].id);
  const [date, setDate] = useState('');
  const [values, setValues] = useState<Record<string, string>>({});

  const load = () => apiJson<Listing>('/api/v1/review/records')
    .then(d => { setListing(d); setLoadErr(''); })
    .catch(e => { setListing(null); setLoadErr(errorMessage(e)); });
  useEffect(() => { load(); }, []);

  const record = async () => {
    setBusy(true); setErr(''); setSaid('');
    const fields = TIERS.find(t => t.id === tier)?.fields ?? [];
    const body: Record<string, unknown> = { tool: tool.trim(), tier, date: date.trim() };
    for (const f of fields) {
      const v = (values[f] ?? '').trim();
      if (!v) continue;
      body[f] = f === 'sources_read' ? v.split(',').map(s => s.trim()).filter(Boolean) : v;
    }
    try {
      const d = await apiJson<any>('/api/v1/review/record', { method: 'POST', body });
      setSaid(`Recorded. ${d.tool_now_says?.label ?? ''} — ${d.tool_now_says?.basis ?? ''}${d.kept_basis ? ` (${d.kept_basis})` : ''}`);
      await load();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy(false);
  };

  const fields = TIERS.find(t => t.id === tier)?.fields ?? [];
  return (
    <div className="space-y-4" data-testid="review-records">
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><ClipboardCheck size={14} /> Records of review</h3>
        {loadErr && <p data-testid="review-records-unread" className="text-[10px] text-vital">{loadErr}</p>}
        {listing && (
          <>
            <p data-testid="review-records-basis" className="text-[9px] text-slate-500 leading-relaxed">{listing.basis}.</p>
            <p data-testid="review-records-credential" className="text-[9px] text-amber-300/90 leading-relaxed mb-2">{listing.credential_basis}.</p>
            <p data-testid="review-records-count" className="text-[9px] text-slate-500 mb-2">{listing.counted} of {listing.total} record(s) count.</p>
            <div className="flex flex-wrap gap-1.5 mb-3">
              {Object.entries(listing.tools).map(([t, label]) => (
                <span key={t} data-testid={`review-tool-${t}`} className="text-[9px] px-2 py-1 rounded-lg border border-slate-800 text-slate-300">{t} · {label}</span>
              ))}
            </div>
            <div className="space-y-1.5">
              {listing.records.map(r => (
                <div key={r.record_id} data-testid={`review-record-${r.record_id}`} className="p-2 rounded-lg border border-slate-900">
                  <p className="text-[10px] text-slate-300">
                    <span className="font-mono">{r.tool}</span> · {r.tier.replace(/_/g, ' ')} · {r.date}
                    {r.name ? ` · ${r.name}, ${r.credential_as_stated ?? ''} (as stated), until ${r.lapses_on ?? ''}` : ''}
                    {r.test ? ` · ${r.test}` : ''}{r.agent ? ` · ${r.agent}` : ''}{r.model ? ` · ${r.model}` : ''}
                  </p>
                  {!r.counts && r.why_not && (
                    <p data-testid={`review-record-why-not-${r.record_id}`} className="text-[9px] text-amber-400">Does not count: {r.why_not}.</p>
                  )}
                  <p className="text-[9px] text-slate-600">entered by {r.entered_by ?? 'not recorded'}{r.entered_at ? `, ${r.entered_at}` : ''}</p>
                </div>
              ))}
              {listing.total === 0 && <p data-testid="review-records-none" className="text-[10px] text-slate-500">No review has been recorded for any tool.</p>}
            </div>
          </>
        )}
      </Card>

      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Record a review</h3>
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <input aria-label="Tool" value={tool} onChange={e => setTool(e.target.value)} placeholder="the tool, e.g. care_risk_assess" className={`${inputCls} w-56`} />
          <select aria-label="Tier" value={tier} onChange={e => setTier(e.target.value)} className={inputCls}>
            {TIERS.map(t => <option key={t.id} value={t.id}>{t.id.replace(/_/g, ' ')}</option>)}
          </select>
          <input aria-label="Date" value={date} onChange={e => setDate(e.target.value)} placeholder="YYYY-MM-DD" className={`${inputCls} w-28`} />
        </div>
        <div className="grid sm:grid-cols-2 gap-2 mb-2">
          {fields.map(f => (
            <input key={f} aria-label={FIELD_LABEL[f]} value={values[f] ?? ''} placeholder={FIELD_LABEL[f]}
              onChange={e => setValues({ ...values, [f]: e.target.value })} className={inputCls} />
          ))}
        </div>
        <Button onClick={record} disabled={busy || !tool.trim() || !date.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
          {busy ? <Loader2 size={11} className="animate-spin" /> : <ClipboardCheck size={11} />} Record
        </Button>
        {err && <p data-testid="review-record-refused" className="text-[10px] text-vital mt-2">{err}</p>}
        {said && <p data-testid="review-record-said" className="text-[10px] text-slate-300 mt-2">{said}</p>}
      </Card>
    </div>
  );
};
