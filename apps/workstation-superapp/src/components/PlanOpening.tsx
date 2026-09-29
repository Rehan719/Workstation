/**
 * W505 (FU-074, FU-158) — THE PLAN'S OPENING, ONE COMPONENT, TWO PAGES.
 *
 * FU-074: W471 wired the owner-edit form (POST /business-plan/set, with `clear`) and the owner-edited marks
 * into BusinessPlan.tsx only. VSBCockpit's plan tab showed the same Chief's Opening with its provenance badge
 * and pending list, and the founder could not set or clear a single field there, nor see which fields they had
 * already set. The register row asks for one component shared by both pages rather than a second copy of the
 * form, because a second copy is the same defect waiting to drift.
 *
 * FU-158 (S1.24 + S3.13): both pages head this block "Chief's Opening" over text that is, on the establish
 * path, CODE TEMPLATES filled from the problem statement — an f-string, composed by neither the Chief nor any
 * model. The heading claimed authorship the provenance badge could not support, because `served_by` describes
 * the ENTITY's serving resource and is null on that path. The backend now records `field_sources` and
 * `opening_written_by`, and this component prints them: a templated field is marked as such, next to its own
 * text, where the reader meets it.
 *
 * The heading is no longer an unconditional claim either. It says "Chief's Opening" only when something other
 * than a template wrote the fields; otherwise it says what is there.
 */
import React, { useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Crown, PenLine, CheckCircle2, Loader2 } from 'lucide-react';
import { provenanceMapBadge } from '../lib/api';

export interface PlanProvenanceShape {
  served_by?: Record<string, number> | null;
  body_pending?: string[];
  /** W505 (FU-158) — per field: 'establish_template' | 'owner_supplied' | a model's name. */
  field_sources?: Record<string, string>;
  templated_fields?: string[];
  opening_written_by?: string;
}

export interface PlanOpeningShape {
  scope?: string;
  owner?: string;
  executive_summary?: string;
  concept?: string;
  vision?: string;
  mission?: string;
  strategy?: string;
  owner_edits?: Record<string, string>;
  owner_edits_by?: Record<string, string>;
  provenance?: PlanProvenanceShape | null;
}

const OPENING: [string, string][] = [
  ['executive_summary', 'Executive Summary'],
  ['concept', 'Concept'],
  ['vision', 'Vision'],
  ['mission', 'Mission'],
  ['strategy', 'Strategy'],
];

/** The five fields shown above the fold on both pages; mission and strategy sit in the strategic layer. */
const ABOVE_FOLD = ['executive_summary', 'concept', 'vision'];

interface Props {
  plan: PlanOpeningShape;
  scope: string;
  /** Called after a successful save so the page can reload the plan. */
  onSaved: () => void;
  /** Which fields to render. Defaults to the opening three; pass all five on a page with no strategic layer. */
  fields?: string[];
  /** Surfaced to the page so a failure is never silent (the W329 rule). */
  onError?: (message: string) => void;
}

export const PlanOpening: React.FC<Props> = ({ plan, scope, onSaved, fields = ABOVE_FOLD, onError }) => {
  const [edit, setEdit] = useState<Record<string, string> | null>(null);
  const [saving, setSaving] = useState(false);

  const shown = OPENING.filter(([k]) => fields.includes(k));
  const sources = plan.provenance?.field_sources ?? {};
  const templated = new Set(plan.provenance?.templated_fields ?? []);
  const anyText = shown.some(([k]) => (plan as any)[k]);

  // W505 (FU-158) — the heading is CONDITIONAL. Calling this the Chief's Opening over five code templates is
  // the claim the sweep flagged; it is the Chief's only when something composed it.
  const allTemplated = shown.length > 0 && shown.every(([k]) => !(plan as any)[k] || templated.has(k));
  const heading = allTemplated
    ? 'Plan opening — generated from your establish answers'
    : 'Chief’s Opening';

  const openEdit = () =>
    setEdit(Object.fromEntries(OPENING.map(([k]) => [k, ((plan as any)[k] as string) || ''])));

  const save = async () => {
    if (!edit) return;
    setSaving(true);
    // only what the owner CHANGED is sent: an untouched template is never re-stamped as the owner's words
    const clear = OPENING.map(([k]) => k).filter(k => !edit[k].trim() && (plan as any)[k]);
    const body: Record<string, unknown> = { scope, owner: plan.owner ?? 'Rehan', clear };
    OPENING.forEach(([k]) => {
      const v = edit[k].trim();
      if (v && v !== (((plan as any)[k] as string) || '')) body[k] = v;
    });
    try {
      const r = await fetch('/api/v1/business-plan/set', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
      });
      if (!r.ok) onError?.(`Owner edit not saved (HTTP ${r.status})`);
      else setEdit(null);
    } catch {
      onError?.('Backend unreachable — the owner edit was NOT saved');
    }
    setSaving(false);
    onSaved();
  };

  return (
    <>
      {anyText && (
        <Card className="p-6 border-highlight/40 bg-gradient-to-br from-highlight/10 to-transparent">
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <Crown size={15} className="text-highlight" />
            <h4 className="text-[10px] font-black uppercase tracking-widest text-white" data-testid="plan-opening-heading">
              {heading}
            </h4>
            {(() => {
              const sb = plan.provenance?.served_by;
              if (!sb) return null;
              const b = provenanceMapBadge(sb);
              return (
                <span className={`text-[9px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded ${b.cls}`}
                      title={b.title} data-testid="plan-provenance">{b.label}</span>
              );
            })()}
            {(plan.provenance?.body_pending?.length ?? 0) > 0 && (
              <span className="text-[9px] text-amber-400/80" data-testid="plan-pending"
                    title="the deterministic floor served these; nothing was written — set them yourself, or generate once the owned model serves">
                pending the owned model: {plan.provenance!.body_pending!.join(' · ')}
              </span>
            )}
            <button type="button" onClick={openEdit}
                    className="ml-auto text-[9px] font-black uppercase tracking-widest text-highlight border border-highlight/40 rounded-lg px-2 py-1 flex items-center gap-1"
                    data-testid="plan-owner-edit-open"><PenLine size={10} /> Owner: edit</button>
          </div>

          {/* W505 (FU-158) — what wrote this, in a sentence, before the text it describes. */}
          {plan.provenance?.opening_written_by && templated.size > 0 && (
            <p className="text-[10px] text-amber-400/80 mb-3" data-testid="plan-opening-written-by">
              {plan.provenance.opening_written_by}
            </p>
          )}

          {shown.filter(([k]) => (plan as any)[k]).map(([k, label]) => (
            <div key={k} className="mb-3 last:mb-0">
              <p className="text-[9px] font-black uppercase tracking-widest text-highlight/70 mb-1 flex items-center gap-2">
                {label}
                {plan.owner_edits?.[k] && (
                  <span className="text-emerald-400/80 font-bold" data-testid={`plan-owner-edited-${k}`}
                        title={`set by ${plan.owner_edits_by?.[k] ?? 'the owner'} at ${plan.owner_edits[k]}`}>
                    owner-edited
                  </span>
                )}
                {!plan.owner_edits?.[k] && templated.has(k) && (
                  <span className="text-amber-400/70 font-bold" data-testid={`plan-templated-${k}`}
                        title="a code template filled from your establish answers — not written by the Chief or a model">
                    template
                  </span>
                )}
                {!plan.owner_edits?.[k] && !templated.has(k) && sources[k] && sources[k] !== 'owner_supplied' && (
                  <span className="text-slate-500 font-bold">{sources[k]}</span>
                )}
              </p>
              <p className="text-sm text-slate-300 leading-relaxed">{(plan as any)[k]}</p>
            </div>
          ))}
        </Card>
      )}

      {!anyText && (
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-2">
            <Crown size={15} className="text-highlight" />
            <h4 className="text-[10px] font-black uppercase tracking-widest text-white">Plan opening</h4>
            <button type="button" onClick={openEdit}
                    className="ml-auto text-[9px] font-black uppercase tracking-widest text-highlight border border-highlight/40 rounded-lg px-2 py-1 flex items-center gap-1"
                    data-testid="plan-owner-edit-open"><PenLine size={10} /> Owner: edit</button>
          </div>
          <p className="text-[11px] text-slate-500">
            No opening recorded yet — nothing here is the Chief&rsquo;s framing until the owned model composes it
            or you set it.
          </p>
        </Card>
      )}

      {edit && (
        <Card className="p-6 border-highlight/40" data-testid="plan-owner-edit">
          <div className="flex items-center gap-2 mb-3">
            <PenLine size={14} className="text-highlight" />
            <h3 className="text-[10px] font-black uppercase tracking-widest text-highlight">
              Owner edit — set or clear the opening and strategic layers
            </h3>
          </div>
          <p className="text-[10px] text-slate-500 mb-3">
            Your words replace whatever is there on save; an emptied field is cleared
            (POST /api/v1/business-plan/set). Each set field is marked owner-edited.
          </p>
          <div className="space-y-3">
            {OPENING.map(([k, label]) => (
              <label key={k} className="block">
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">{label}</span>
                <textarea value={edit[k]} onChange={e => setEdit({ ...edit, [k]: e.target.value })}
                          rows={k === 'vision' || k === 'mission' ? 1 : 3}
                          className="mt-1 w-full text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300"
                          data-testid={`plan-edit-${k}`} />
              </label>
            ))}
          </div>
          <div className="flex gap-2 mt-4">
            <Button onClick={save} disabled={saving}
                    className="bg-highlight text-sovereign text-xs flex items-center gap-2"
                    data-testid="plan-owner-edit-save">
              {saving ? <Loader2 size={13} className="animate-spin" /> : <CheckCircle2 size={13} />} Save
            </Button>
            <Button onClick={() => setEdit(null)} disabled={saving} className="bg-slate-900 text-slate-300 text-xs">
              Cancel
            </Button>
          </div>
        </Card>
      )}
    </>
  );
};

export default PlanOpening;
