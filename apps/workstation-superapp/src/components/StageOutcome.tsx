import React from 'react';
import { CheckCircle2, CircleDashed, XCircle } from 'lucide-react';
import { provenanceBadge } from '../lib/api';

// W479 (FU-121) — ONE rule for every intelligence-pipeline stage card (Intelligence Lab, Authorship,
// Design & Dev, Synthesis Nexus). The four pages ticked every stage green: a failed stage, a floor
// scaffold and a model-served stage all looked the same, and the pages counted framing events
// ('config', '*_start') as stages ("Stage 10 of 9"). A stage's outcome now comes from the provenance
// the backend puts on its event: failed (red) · floor scaffold (neutral) · model-served (green).
// Unknown provenance is treated as the floor: it is never green.

export interface StageData {
  stage_num?: number;
  total?: number;
  served_by?: string | null;
  is_external?: boolean;
  failed?: boolean;
}

export type StageOutcomeKind = 'failed' | 'floor' | 'model' | 'external';

export const stageOutcome = (d?: StageData | null): StageOutcomeKind =>
  d?.failed ? 'failed' : (d?.served_by && d.served_by !== 'native') ? (d.is_external ? 'external' : 'model') : 'floor';

// A stage RESULT event carries a stage number; framing events (init, config, *_start, routing, complete) do not.
export const isStageResult = (ev: { data?: unknown }): boolean =>
  typeof (ev.data as StageData | undefined)?.stage_num === 'number';

// (W479 refutation) how many stage results RAN: a failed stage is a result, never output.
export const ranCount = (evs: Array<{ data?: unknown }>): number =>
  evs.filter(ev => stageOutcome(ev.data as StageData) !== 'failed').length;

export const FLOOR_STAGE_NOTE =
  'Scaffold from the structured floor: headings built from your request. No model analysed it, and no review, audit or check was performed.';

export const StageMark: React.FC<{ data?: StageData | null; size?: number; className?: string }> = ({ data, size = 14, className = '' }) => {
  const k = stageOutcome(data);
  if (k === 'failed') return <XCircle size={size} className={`text-vital shrink-0 ${className}`} aria-label="stage did not run" />;
  if (k === 'floor') return <CircleDashed size={size} className={`text-slate-500 shrink-0 ${className}`} aria-label="structured floor scaffold" />;
  if (k === 'external') return <CheckCircle2 size={size} className={`text-amber-400 shrink-0 ${className}`} aria-label="served by an external accelerant (opt-in)" />;
  return <CheckCircle2 size={size} className={`text-emerald-400 shrink-0 ${className}`} aria-label="served by a model" />;
};

export const StageBadge: React.FC<{ data?: StageData | null }> = ({ data }) => {
  if (stageOutcome(data) === 'failed') {
    return <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-vital/15 text-vital">did not run</span>;
  }
  const b = provenanceBadge(data?.served_by, data?.is_external);
  return <span title={b.title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`}>{b.label}</span>;
};

// The run summary the backend puts on a pipeline's 'complete' event.
export interface RunSummary {
  stages_total?: number;
  stages_completed?: number;
  floor_calls?: number;
  failed_calls?: number;
  model_calls?: number;
  served_by?: Record<string, number>;
  any_external?: boolean;
}
