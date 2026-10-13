import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Loader2, Send } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

// W697 — THE APPRAISAL CELL, ON A PAGE (Owner ruling 2026-10-13). The cell's readings over a scope, what
// becomes of an appraisal, and what its findings recommend. A person may send ONE recommendation to Change
// Control with the button beside it. EVERY SENTENCE HERE IS THE SERVER'S: each reading's basis, each
// recommendation and each refusal. The page composes none of them, and sending approves and applies nothing.

interface Recommendation {
  id: string; from_faculty: string; count: number; recommendation: string; rests_on: string;
  affected_systems: string[];
}
interface Appraisal {
  scope: string;
  faculties: Record<string, { basis?: string | null; limits?: string | null; state?: string | null }>;
  hand_off: { statement: string; kept_basis: string; authorises_basis: string; not_established: string } | null;
  recommendations: Recommendation[];
  recommendations_basis: string;
  this_cell_never_says: string;
}

export const MethodAppraisal: React.FC = () => {
  const [scope, setScope] = useState('');
  const [asked, setAsked] = useState('');
  const [data, setData] = useState<Appraisal | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const [sending, setSending] = useState('');
  const [sent, setSent] = useState<Record<string, string>>({});
  const [sendErr, setSendErr] = useState<Record<string, string>>({});

  const load = (s: string) => {
    setBusy(true); setErr(''); setSent({}); setSendErr({});
    const q = s.trim() ? `?scope=${encodeURIComponent(s.trim())}` : '';
    return apiJson<Appraisal>(`/api/v1/method/appraise${q}`)
      .then(d => { setData(d); setAsked(s.trim()); })
      .catch(e => { setData(null); setErr(errorMessage(e)); })
      .finally(() => setBusy(false));
  };
  useEffect(() => { load(''); }, []);

  const send = async (id: string) => {
    setSending(id);
    setSendErr(p => ({ ...p, [id]: '' }));
    try {
      const d = await apiJson<any>('/api/v1/method/appraise/recommend', {
        method: 'POST', body: { scope: asked || null, recommendation_id: id },
      });
      setSent(p => ({ ...p, [id]: `Change record ${d.change_control?.cca_id} filed (${d.change_control?.status}). ${d.basis}` }));
    } catch (e) {
      setSendErr(p => ({ ...p, [id]: errorMessage(e) }));
    } finally { setSending(''); }
  };

  return (
    <div className="space-y-4" data-testid="method-appraisal">
      <Card className="p-4 bg-slate-950/60 border-slate-900">
        <h2 className="text-sm font-black text-slate-100">Appraisal</h2>
        <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
          Readings of the plan and the register over a scope, made when this page asks. A scope is a phase
          (P3), an item (P3.30), or empty for the whole plan.
        </p>
        <div className="flex gap-2 mt-3">
          <input
            data-testid="appraisal-scope" value={scope} onChange={e => setScope(e.target.value)}
            placeholder="e.g. P3.30 — empty for the whole plan" aria-label="Scope to appraise"
            className="flex-1 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300"
          />
          <Button type="button" data-testid="appraisal-run" disabled={busy} onClick={() => load(scope)}>
            {busy ? <Loader2 size={14} className="animate-spin" /> : 'Appraise'}
          </Button>
        </div>
        {err && <p className="text-[11px] text-rose-400 mt-2" data-testid="appraisal-unavailable">The appraisal could not be read: {err}</p>}
      </Card>

      {data && (
        <>
          <Card className="p-4 bg-slate-950/60 border-slate-900" data-testid="appraisal-recommendations">
            <h3 className="text-xs font-black uppercase tracking-widest text-slate-300">
              What the readings recommend · {data.scope}
            </h3>
            <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">{data.recommendations_basis}</p>
            {data.recommendations.length === 0 ? (
              <p className="text-[11px] text-slate-400 mt-3" data-testid="appraisal-no-recommendations">
                No counted finding in this scope calls for an act. That is what these readings count, not a
                statement that the scope is sound.
              </p>
            ) : (
              <ul className="mt-3 space-y-3">
                {data.recommendations.map(r => (
                  <li key={r.id} className="border border-slate-900 rounded-lg p-3" data-testid={`recommendation-${r.id}`}>
                    <p className="text-[11px] text-slate-200 leading-relaxed">{r.recommendation}</p>
                    <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                      <span className="font-black uppercase tracking-widest">From {r.from_faculty} · </span>{r.rests_on}
                    </p>
                    <div className="mt-2 flex items-center gap-2">
                      <Button type="button" data-testid={`send-${r.id}`} disabled={sending === r.id || !!sent[r.id]} onClick={() => send(r.id)}>
                        {sending === r.id ? <Loader2 size={12} className="animate-spin" /> : <Send size={12} />}
                        <span className="ml-1">Send to Change Control</span>
                      </Button>
                      <span className="text-[10px] text-slate-500">Files one record for a person to decide. Applies nothing.</span>
                    </div>
                    {sent[r.id] && <p className="text-[10px] text-emerald-400 mt-2" data-testid={`sent-${r.id}`}>{sent[r.id]}</p>}
                    {sendErr[r.id] && <p className="text-[10px] text-rose-400 mt-2" data-testid={`send-refused-${r.id}`}>Not sent: {sendErr[r.id]}</p>}
                  </li>
                ))}
              </ul>
            )}
          </Card>

          {data.hand_off && (
            <Card className="p-4 bg-slate-950/60 border-slate-900" data-testid="appraisal-hand-off">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-300">What becomes of an appraisal</h3>
              <p className="text-[11px] text-slate-300 mt-2 leading-relaxed">{data.hand_off.statement}</p>
              <p className="text-[10px] text-slate-500 mt-2 leading-relaxed">{data.hand_off.kept_basis}. {data.hand_off.authorises_basis}.</p>
              <p className="text-[10px] text-amber-400/90 mt-2 leading-relaxed">
                <span className="font-black uppercase tracking-widest">Not established · </span>{data.hand_off.not_established}
              </p>
            </Card>
          )}

          <Card className="p-4 bg-slate-950/60 border-slate-900" data-testid="appraisal-readings">
            <h3 className="text-xs font-black uppercase tracking-widest text-slate-300">The readings</h3>
            <ul className="mt-2 space-y-2">
              {Object.entries(data.faculties).map(([name, f]) => (
                <li key={name} className="text-[11px] leading-relaxed">
                  <span className="font-black uppercase tracking-widest text-slate-400">{name}{f.state ? ` · ${f.state}` : ''} · </span>
                  <span className="text-slate-300">{f.basis || 'this reading states no basis'}</span>
                  {f.limits && <span className="text-slate-500"> Limits: {f.limits}</span>}
                </li>
              ))}
            </ul>
            <p className="text-[10px] text-amber-400/90 mt-3 leading-relaxed">
              <span className="font-black uppercase tracking-widest">This cell never says · </span>{data.this_cell_never_says}
            </p>
          </Card>
        </>
      )}
    </div>
  );
};
