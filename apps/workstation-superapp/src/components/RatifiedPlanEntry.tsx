import React, { useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { apiJson, errorMessage } from '../lib/api';

//  W726 (OWNER RULING 2026-10-14) - ONE ACTION ENTERS THE OWNER'S RATIFIED PLAN. The preview is shown first and
//  nothing is written until it is confirmed; the confirmation carries the fingerprint of the document that
//  was shown, so a document changed in between is refused. Nothing is fetched until asked for.
type Shown = {
  document: string; sha256: string; ratified_on: string | null;
  changed_since: { on: string; what: string } | null;
  fields: Record<string, string>; aims: string[];
  objectives: { title: string; plan_item: string; kpi: string; measure_as_ratified: string }[];
  not_entered: string[]; canvas: string; can_enter: boolean; cannot_because: string | null;
  already_entered: { entered_at: string; entered_by: string; basis: string } | null;
  edited_since?: string[]; edited_since_basis?: string;
};

export const RatifiedPlanEntry: React.FC<{ onEntered: () => void }> = ({ onEntered }) => {
  const [shown, setShown] = useState<Shown | null>(null);
  const [busy, setBusy] = useState('');
  const [said, setSaid] = useState('');
  const [refusal, setRefusal] = useState('');

  const preview = async () => {
    setBusy('preview'); setRefusal(''); setSaid('');
    try { setShown(await apiJson('/api/v1/business-plan/ratified/preview')); } catch (e) { setRefusal(errorMessage(e)); }
    setBusy('');
  };
  const enter = async () => {
    if (!shown) return;
    setBusy('enter'); setRefusal(''); setSaid('');
    try {
      const d = await apiJson('/api/v1/business-plan/ratified/enter', { method: 'POST', body: { sha256: shown.sha256 } });
      setSaid(`${d.stamp.basis}. ${d.objectives_added} objective(s) added.`);
      onEntered();
      setShown(await apiJson('/api/v1/business-plan/ratified/preview'));
    } catch (e) { setRefusal(errorMessage(e)); }
    setBusy('');
  };

  return (
    <Card className="p-5 border-slate-800" data-testid="ratified-plan-entry">
      <h3 className="text-[10px] font-black uppercase tracking-widest text-highlight">Enter my ratified plan</h3>
      <p className="text-[10px] text-slate-500 mt-1 mb-3">
        Reads the business plan document the Owner ratified and shows what would be entered here. Nothing is written until you confirm.
      </p>
      {!shown && (
        <Button onClick={preview} disabled={busy === 'preview'} className="bg-slate-900 text-aura text-[10px]" data-testid="ratified-preview">
          {busy === 'preview' ? 'Reading…' : 'Show what would be entered'}
        </Button>
      )}
      {refusal && <p data-testid="ratified-refusal" className="text-[11px] text-amber-300/90 mt-2">{refusal}</p>}
      {said && <p data-testid="ratified-said" className="text-[11px] text-emerald-300/90 mt-2">{said}</p>}
      {shown && (
        <div className="space-y-2 mt-2">
          <p data-testid="ratified-document" className="text-[10px] text-slate-400">
            {shown.document} · {shown.ratified_on ? `ratified by the Owner on ${shown.ratified_on}` : 'NOT ratified'}
            {shown.changed_since ? ` · changed on ${shown.changed_since.on}: ${shown.changed_since.what}` : ''}
          </p>
          {Object.entries(shown.fields).map(([k, v]) => (
            <div key={k} className="p-2 rounded-lg bg-slate-950 border border-slate-900">
              <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">{k.replace('_', ' ')}</p>
              <p className="text-[11px] text-slate-300 whitespace-pre-wrap">{v}</p>
            </div>
          ))}
          <p className="text-[10px] text-slate-400">{shown.aims.length} aim(s) · {shown.objectives.length} objective(s), each tied to a plan item.
            {' '}{shown.objectives.filter(o => !o.kpi).length} carry no measure, because the document says theirs is not measured.</p>
          <p data-testid="ratified-not-entered" className="text-[10px] text-amber-300/90">
            Not entered, because this plan has no place for them: {shown.not_entered.join(', ')}. Also, {shown.canvas}.
          </p>
          {shown.already_entered && (
            <p data-testid="ratified-already" className="text-[10px] text-slate-400">
              Entered {shown.already_entered.entered_at} by {shown.already_entered.entered_by}. {shown.already_entered.basis}.
              {shown.edited_since && shown.edited_since.length > 0 && ` Edited by hand since: ${shown.edited_since.join(', ')}.`}
            </p>
          )}
          {shown.can_enter
            ? <Button onClick={enter} disabled={busy === 'enter'} className="bg-highlight text-sovereign text-[10px]" data-testid="ratified-enter">
                {busy === 'enter' ? 'Entering…' : 'Enter this into the plan'}
              </Button>
            : <p data-testid="ratified-cannot" className="text-[11px] text-amber-300/90">Cannot be entered now: {shown.cannot_because}.</p>}
        </div>
      )}
    </Card>
  );
};
