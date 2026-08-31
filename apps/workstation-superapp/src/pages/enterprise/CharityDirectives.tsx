/**
 * §5 — the Owner's charity directives (W397).
 *
 * GET/POST /api/v1/economy/charity/directives existed with no UI, so the directives were visible
 * only to code: priorities, exclusions and the 100%-donation rule sat at their defaults (recorded as
 * a 2026-06-21 Owner directive) with no way to read or revise them in the product. Charity is a stage
 * of the §4 profit waterfall, so these values govern where a real share of distributable profit goes.
 *
 * Honesty notes:
 *   • This sets ALLOCATION POLICY for virtual WST. It moves no real money. Real-money and live
 *     charity rails remain gated behind the Owner's authorisation and a compliance review, and
 *     nothing here touches them.
 *   • `source` and `updated_at` are shown as the backend reports them, so "still on defaults" is
 *     visibly different from "the Owner set this".
 *   • A failed save is reported. It never silently keeps the edited values on screen as if saved.
 */

import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { HeartHandshake, Loader2, AlertTriangle } from 'lucide-react';
import { apiJson, errorMessage } from '../../lib/api';

interface Directives {
  priorities: string[];
  exclusions: string[];
  require_100pct: boolean;
  source?: string;
  updated_at?: string | null;
}

const toList = (s: string) =>
  s.split(',').map(x => x.trim()).filter(Boolean);

export const CharityDirectives: React.FC = () => {
  const [loaded, setLoaded] = useState<Directives | null>(null);
  const [priorities, setPriorities] = useState('');
  const [exclusions, setExclusions] = useState('');
  const [require100, setRequire100] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const apply = (d: Directives) => {
    setLoaded(d);
    setPriorities((d.priorities || []).join(', '));
    setExclusions((d.exclusions || []).join(', '));
    setRequire100(d.require_100pct !== false);
  };

  const load = () =>
    apiJson<Directives>('/api/v1/economy/charity/directives')
      .then(d => { apply(d); setError(''); })
      .catch(e => setError(errorMessage(e)));

  useEffect(() => { load(); }, []);

  const save = async () => {
    setSaving(true); setError(''); setNotice('');
    try {
      const res = await apiJson<Directives>('/api/v1/economy/charity/directives', {
        method: 'POST',
        body: {
          priorities: toList(priorities),
          exclusions: toList(exclusions),
          require_100pct: require100,
        },
      });
      apply(res);
      setNotice('Directives saved — honoured by allocations from the next metabolic cycle.');
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setSaving(false);
    }
  };

  const dirty =
    !!loaded &&
    (priorities !== (loaded.priorities || []).join(', ')
      || exclusions !== (loaded.exclusions || []).join(', ')
      || require100 !== (loaded.require_100pct !== false));

  return (
    <Card className="p-5 space-y-4">
      <div>
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
          <HeartHandshake size={14} /> §5 · Charity directives
        </h3>
        <p className="text-slate-500 text-xs font-semibold mt-2 leading-relaxed max-w-3xl">
          Where the charity stage of the profit waterfall is directed, and what it must never fund.
          These govern allocation of <span className="text-slate-400">virtual WST</span> — no real
          money moves, and live charity rails stay gated behind your authorisation and a compliance
          review.
        </p>
        {loaded && (
          <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mt-2">
            {loaded.updated_at
              ? `set by you · ${loaded.updated_at}`
              : `still on defaults${loaded.source ? ` · ${loaded.source}` : ''}`}
          </p>
        )}
      </div>

      <label className="flex flex-col gap-1">
        <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Priorities (comma-separated)</span>
        <input value={priorities} onChange={e => setPriorities(e.target.value)}
          aria-label="Charity priorities"
          placeholder="clean_water, orphan_sponsorship, …"
          className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
      </label>

      <label className="flex flex-col gap-1">
        <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">Exclusions — never funded (comma-separated)</span>
        <input value={exclusions} onChange={e => setExclusions(e.target.value)}
          aria-label="Charity exclusions"
          placeholder="none set"
          className="bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
      </label>

      <label className="flex items-center gap-2 cursor-pointer">
        <input type="checkbox" checked={require100} onChange={e => setRequire100(e.target.checked)}
          aria-label="Require 100% of the charity allocation to reach the cause"
          className="accent-aura" />
        <span className="text-[10px] font-bold text-slate-400">
          Require 100% of the charity allocation to reach the cause (no deductions)
        </span>
      </label>

      {error && (
        <div role="alert" className="flex items-start gap-2 rounded-xl border border-vital/30 bg-vital/10 px-3 py-2">
          <AlertTriangle size={12} className="text-vital shrink-0 mt-0.5" />
          <p className="text-[10px] font-bold text-vital leading-relaxed">{error}</p>
        </div>
      )}
      {notice && (
        <div role="status" className="rounded-xl border border-aura/30 bg-aura/10 px-3 py-2">
          <p className="text-[10px] font-bold text-aura leading-relaxed">{notice}</p>
        </div>
      )}

      <Button type="button" onClick={save} disabled={saving || !dirty}>
        {saving ? <Loader2 size={13} className="animate-spin" /> : dirty ? 'Save directives' : 'No changes'}
      </Button>
    </Card>
  );
};
