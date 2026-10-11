import React, { useCallback, useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { apiJson, errorMessage } from '../../lib/api';

// W669 (FU-693, Owner ruling 2026-10-11) - THE REVIEWING HALF OF THE SCHOLAR GATE, ON A SCREEN.
// Religious teaching content is composed and WITHHELD until a named scholar approves it. Until this panel
// nothing could add a scholar, show what awaits review, or record a decision, so the gate could only withhold.
// With authentication off, the Owner adds named scholars and enters a scholar's decision on their behalf; every
// such decision is shown with its footing - attested, not verified - exactly as the server recorded it.

interface Scholar { name: string; credential: string; added_by: string; added_at: string }
interface Item {
  content_key: string; surface: string; reference: string; body: string; state: string;
  submitted_at?: string; reviewer_id?: string | null; reviewed_at?: string | null;
  decision_note?: string | null; entered_by?: string | null; attestation?: string | null;
}
interface Footing { authentication: string; who_adds_a_scholar: string; who_decides: string }
interface Status { scholars_on_roster: number; roster_is_empty: boolean; items: number; basis: string;
                   roster: Record<string, Scholar>; footing: Footing }

const ScholarReviewPanel: React.FC = () => {
  const [status, setStatus] = useState<Status | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [form, setForm] = useState({ scholar_id: '', name: '', credential: '' });
  const [chosen, setChosen] = useState('');
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    try {
      const [s, q] = await Promise.all([
        apiJson<Status>('/api/v1/scholar-review/status'),
        apiJson<{ items: Item[] }>('/api/v1/scholar-review/queue'),
      ]);
      setStatus(s); setItems(q.items || []); setErr('');
    } catch (e) { setErr(`The scholar review record could not be read. ${errorMessage(e)}`); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  const addScholar = async () => {
    setBusy(true); setMsg('');
    try {
      await apiJson('/api/v1/scholar-review/roster', { method: 'POST', body: form });
      setMsg(`Recorded ${form.name}. The credential is stored as stated; nothing here verified it.`);
      setForm({ scholar_id: '', name: '', credential: '' });
      await load();
    } catch (e) { setMsg(`Not recorded. ${errorMessage(e)}`); }
    setBusy(false);
  };

  const decide = async (content_key: string, approve: boolean) => {
    setBusy(true); setMsg('');
    try {
      await apiJson('/api/v1/scholar-review/decide', { method: 'POST', body: { content_key, scholar_id: chosen, approve } });
      setMsg(approve ? 'Approval recorded.' : 'Rejection recorded.');
      await load();
    } catch (e) { setMsg(`Not decided. ${errorMessage(e)}`); }
    setBusy(false);
  };

  const roster = Object.entries(status?.roster || {});
  return (
    <div className="space-y-6" data-testid="scholar-review-panel">
      <Card className="p-6 border-slate-800 bg-slate-900/40">
        <h3 className="text-xs font-black uppercase tracking-widest text-aura mb-2">Scholar review</h3>
        {err && <p role="alert" className="text-xs text-vital font-semibold mb-2">{err}</p>}
        <p className="text-[11px] text-slate-400 leading-relaxed">{status?.basis}</p>
        {status && (
          <p className="text-[11px] text-amber-400 font-semibold leading-relaxed mt-2" data-testid="scholar-footing">
            Authentication is {status.footing.authentication}. Who adds a scholar: {status.footing.who_adds_a_scholar}. Who decides: {status.footing.who_decides}.
          </p>
        )}
      </Card>

      <Card className="p-6 border-slate-800 bg-slate-900/40">
        <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Roster ({roster.length})</h4>
        {roster.length === 0
          ? <p className="text-[11px] text-slate-500" data-testid="scholar-roster-empty">No scholar is recorded, so nothing can be approved and every item stays withheld.</p>
          : roster.map(([id, s]) => (
            <p key={id} className="text-[11px] text-slate-300 mb-1">
              <span className="font-bold text-white">{s.name}</span> <span className="text-slate-500">({id})</span> — {s.credential}
              <span className="text-slate-600"> · credential as stated, not verified · added by {s.added_by} on {String(s.added_at).slice(0, 10)}</span>
            </p>
          ))}
        <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-2 mt-4">
          <input aria-label="Scholar id" placeholder="id (e.g. a short handle)" value={form.scholar_id} onChange={e => setForm({ ...form, scholar_id: e.target.value })} className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white" />
          <input aria-label="Scholar name" placeholder="full name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white" />
          <input aria-label="Stated credential" placeholder="stated credential" value={form.credential} onChange={e => setForm({ ...form, credential: e.target.value })} className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white" />
        </div>
        <Button type="button" onClick={addScholar} disabled={busy || !form.scholar_id.trim() || !form.name.trim() || !form.credential.trim()} className="mt-3 text-xs">Add scholar</Button>
      </Card>

      <Card className="p-6 border-slate-800 bg-slate-900/40">
        <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Awaiting or decided ({items.length})</h4>
        {roster.length > 0 && (
          <label className="block text-[10px] text-slate-500 mb-3">Decision entered for
            <select aria-label="Scholar deciding" value={chosen} onChange={e => setChosen(e.target.value)} className="ml-2 bg-slate-950 border border-slate-800 rounded-lg px-2 py-1 text-xs text-white">
              <option value="">— choose a scholar —</option>
              {roster.map(([id, s]) => <option key={id} value={id}>{s.name}</option>)}
            </select>
          </label>
        )}
        {items.length === 0 && <p className="text-[11px] text-slate-500">Nothing has been composed and submitted for review.</p>}
        {items.map(it => (
          <div key={it.content_key} className="p-3 rounded-xl bg-slate-950 border border-slate-900 mb-2" data-testid="scholar-item">
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">{it.surface} · {it.reference || it.content_key} · <span className="text-white">{it.state}</span></p>
            {/* REL — the key names the surface, the tool and the text's hash; shown when the line above shows the reference instead */}
            {it.reference && <p className="text-[9px] text-slate-600 break-all" data-testid="scholar-item-key">{it.content_key}</p>}
            <pre className="text-[11px] text-slate-300 whitespace-pre-wrap mt-2 max-h-48 overflow-auto">{it.body}</pre>
            {it.reviewer_id && (
              <p className="text-[10px] text-amber-400 mt-2" data-testid="scholar-decision">
                {it.state} for {status?.roster?.[it.reviewer_id]?.name || it.reviewer_id} on {String(it.reviewed_at).slice(0, 10)}
                {it.attestation ? ` — ${it.attestation}` : ''}{it.decision_note ? ` · note: ${it.decision_note}` : ''}
              </p>
            )}
            <div className="flex gap-2 mt-2">
              <Button type="button" disabled={busy || !chosen} onClick={() => decide(it.content_key, true)} className="text-xs">Approve</Button>
              <Button type="button" disabled={busy || !chosen} onClick={() => decide(it.content_key, false)} className="text-xs">Reject</Button>
            </div>
          </div>
        ))}
        {msg && <p role="status" className="text-[11px] text-slate-300 mt-3">{msg}</p>}
      </Card>
    </div>
  );
};

export default ScholarReviewPanel;
