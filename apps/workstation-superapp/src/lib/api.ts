// Round-11 ledger cluster 2 — the CLASS-KILL for HTTP-status blindness.
// The recurring defect: `setState(await r.json())` with no `r.ok` check, so a FastAPI error body
// ({detail: ...}) renders as a result (blank panes, crashed detail views, fabricated success).
// One shared helper ends the class: it throws ApiError on !ok with the parsed detail, so every
// caller's catch shows the REAL reason — and a success path is only ever entered on 2xx.
//
// Usage:
//   try { setThing(await apiJson('/api/v1/x', { method: 'POST', body: {...} })); }
//   catch (e) { setError(errorMessage(e)); }

export class ApiError extends Error {
  status: number;
  detail: string;
  constructor(status: number, detail: string) {
    super(`HTTP ${status}: ${detail}`);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

export interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  /** JSON-serialised automatically; Content-Type set for you. */
  body?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
}

/** fetch → checked JSON. Throws ApiError (with the backend's own `detail`) on any non-2xx,
 *  and TypeError on network failure — never lets an error body flow into a success path. */
export async function apiJson<T = any>(url: string, opts: ApiOptions = {}): Promise<T> {
  const { method = 'GET', body, headers, signal } = opts;
  const res = await fetch(url, {
    method,
    signal,
    headers: body !== undefined ? { 'Content-Type': 'application/json', ...headers } : headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    let detail = res.statusText || 'request failed';
    try {
      const j = await res.json();
      if (j && typeof j === 'object' && 'detail' in j) {
        detail = typeof j.detail === 'string' ? j.detail : JSON.stringify(j.detail);
      }
    } catch { /* non-JSON error body — keep the status text */ }
    throw new ApiError(res.status, detail.slice(0, 300));
  }
  return res.json() as Promise<T>;
}

/** An AXIOS error's `detail`, always as a string a page can render.
 *
 *  A route may raise `HTTPException(detail={...})` — seven already do — and axios hands that object to the
 *  caller unchanged. `setError(obj)` then puts an object where React expects a child, and React THROWS: the
 *  surface crashes rather than showing a bad message. Twenty-two call sites read `e?.response?.data?.detail`
 *  straight into error state, so this is a class and not a site.
 *
 *  A structured detail is rendered by its `message` when it has one, because that is the sentence written
 *  for a reader; otherwise by its JSON, which is ugly but TRUE and far better than a blank panel claiming
 *  the backend is unavailable when it in fact refused and gave a reason.
 *
 *  `errorMessage` above does the same job for the fetch path. The two now agree.
 */
export function axiosDetail(e: any, fallback: string): string {
  const d = e?.response?.data?.detail;
  if (typeof d === 'string' && d) return d;
  // A 422 carries a LIST of {loc, msg} — FastAPI's validation shape — and rendering that as JSON tells a
  // reader nothing they can act on, while rendering it as an array child throws just as an object does.
  // VSBCockpit.tsx already unpacks it this way; the helper takes that over so one place knows how.
  if (Array.isArray(d)) {
    const reasons = d.map((x: any) => {
      if (typeof x === 'string') return x;
      if (!x?.msg) return '';
      const field = Array.isArray(x.loc) && x.loc.length ? `${x.loc[x.loc.length - 1]}: ` : '';
      return `${field}${x.msg}`;
    }).filter(Boolean).join('; ');
    return reasons || fallback;
  }
  if (d && typeof d === 'object') {
    const m = (d as Record<string, unknown>).message ?? (d as Record<string, unknown>).error
              ?? (d as Record<string, unknown>).note;
    if (typeof m === 'string' && m) return m;
    try { return JSON.stringify(d); } catch { return fallback; }
  }
  return fallback;
}

/** Honest, user-facing message for anything a failed call can throw. */
export function errorMessage(e: unknown): string {
  if (e instanceof ApiError) return e.status === 401
    ? 'Not signed in — your session may have expired.'
    : `Failed (HTTP ${e.status}): ${e.detail}`;
  if (e instanceof Error && e.name === 'AbortError') return 'Cancelled.';
  return 'Failed — backend unreachable.';
}

// W439 — the deterministic floor must never wear the green in-house badge: it composes structured
// output from the REQUEST (not model inference), and eight separate renderers were labelling it
// "in-house · native" in green. One helper, every badge; the class dies here.
// W495 (FU-127, S4.2) - the two badge helpers now call each other (a map reaching the string helper is
// routed to the map one), so both need a declared return type: TypeScript cannot infer through the cycle.
export type ProvBadge = { label: string; cls: string; title?: string };

export const provenanceBadge = (servedBy: string | Record<string, number> | null | undefined,
                                isExternal?: boolean): ProvBadge => {
  // W495 (FU-127, S4.2) - a COUNT MAP reached here and fell through every string arm to the emerald
  // `in-house · ${sb}` branch, which rendered as "in-house · [object Object]" over output the
  // deterministic floor served (served_by {native: 4}). The parameter was typed `string`, so nothing
  // failed; TypeScript did not see it because the caller held `any`. Any non-string is routed to the
  // map helper, which counts the keys — so no shape can reach the emerald arm by falling through.
  if (servedBy !== null && servedBy !== undefined && typeof servedBy !== 'string') {
    return provenanceMapBadge(servedBy as Record<string, number>, isExternal);
  }
  // W490 (refutation) — THE THIRD STATE. `servedBy ?? 'native'` turned "no call is recorded as having
  // served this" into the positive claim "structured floor — not model analysis". Two surfaces this
  // round added hit exactly that: a transformation assessment whose call RAISED (served_by: null), and
  // the synthesis fallback endpoint, which records no provenance at all. `provenanceLine` has said
  // "not recorded for this output" since W485; the badge was the half that still guessed.
  if (servedBy === null || servedBy === undefined || servedBy === '') {
    return { label: 'provenance not recorded', cls: 'bg-slate-800 text-slate-400',
      title: 'no call is recorded as having served this output — neither a model nor the floor is claimed' };
  }
  const sb = servedBy;
  if (isExternal) return { label: `via ${sb}`, cls: 'bg-amber-500/20 text-amber-400',
    title: 'served by an external accelerant (opt-in)' };
  if (sb === 'native' || sb === 'template') return { label: 'structured floor — not model analysis', cls: 'bg-amber-500/20 text-amber-400',
    title: 'the deterministic native floor composes structured output from the prompt it is given — it is not model inference' };
  // W490 (refutation) — `verbatim-ingest` means the CALLER supplied this text and declared no origin.
  // The platform composed nothing, so the emerald "in-house · verbatim-ingest" was a composition claim
  // over someone else's words — and it contradicted the exported file, which now says so correctly.
  if (sb === 'verbatim-ingest') return { label: 'supplied verbatim by the caller', cls: 'bg-slate-800 text-slate-400',
    title: 'the platform did not compose this text and records no origin for it' };
  // W495 (FU-123, S11.3) - the emerald `in-house · <sb>` arm caught every token that is not 'native',
  // 'template', 'verbatim-ingest' or external - and the backend writes several NON-MODEL PLACEHOLDERS
  // into served_by: 'real-engine' (a fabric run that completed with no AI call recorded), 'none' (a
  // failed board call), 'unavailable' (a failed business-plan Chief) and '' (an ensemble whose members
  // reported none). Each rendered as the in-house MODEL badge this helper exists to withhold from floor
  // or failed output, on every surface that calls it. They are named for what they are.
  if (sb === 'real-engine') return { label: 'engine ran · no model call recorded', cls: 'bg-slate-800 text-slate-400',
    title: 'a resource ran to completion and recorded no AI call, so nothing here is model output' };
  if (sb === 'none') return { label: 'no call served this', cls: 'bg-slate-800 text-slate-400',
    title: 'the run recorded no serving call at all - neither a model nor the floor is claimed' };
  if (sb === 'unavailable') return { label: 'the serving call FAILED', cls: 'bg-vital/20 text-vital',
    title: 'the resource that should have served this raised, so there is no output to attribute' };
  return { label: `in-house · ${sb}`, cls: 'bg-emerald-500/20 text-emerald-400', title: undefined };
};

// W453 (delivery-plan P1.5, ledger 1.5) — the same class-kill for provenance MAPS: a run that
// records {served_by: {native: 3, 'ollama:x': 1}, any_external} was chipped green 'in-house' by
// five renderers when every call was the floor. One helper, every map chip: all-floor → amber
// with the floor label; any external → amber 'via'; otherwise emerald with the models named.
// refuter F1 — the swarm / tree / composition responses carry a per-step TRACE, not a count map: derive
// the map from what was actually served (an undefined map would have read as 'floor' even when the
// owned model served every step)
// W455 (P1.7) — a §11 verdict has THREE colours: fail (red) · review (amber) · pass (emerald). Ten
// chips coloured by `compliant` (= not fail) painted every 'review' green.
// W460 — emerald only for an explicit 'pass'; anything unscreened or unknown is neutral, never green
export const complianceCls = (overall: string | null | undefined) =>
  overall === 'fail' ? 'bg-vital/15 text-vital' : overall === 'review' ? 'bg-amber-500/15 text-amber-400'
    : overall === 'pass' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-500';
// W483 (ledger v5 R1.1 / sweep S3.6) — ONE rule for every §11 chip on every page. The chip used to
// read a bare "COMPLIANCE: PASS" in emerald with a tooltip listing framework statuses, on a verdict
// whose frameworks had mostly assessed nothing. A pass is now only ever shown as the pass of what
// actually assessed the subject, and the areas nothing assessed are named in the chip itself.
// W485 (sweep S7.8) — ONE provenance line for text that LEAVES the platform. A download or a copy
// carries no DOM, so a badge rendered beside the text is not a label on the text: a whole Genesis
// journey, every call floor-served, left as a .md saying nothing about what composed it. Every export
// surface prepends this. `servedBy` accepts the orchestrator's string or a provenance count map.
const NO_SERVED_CALL_LINE = '> Provenance: no call is recorded as having served this output.\n\n';
export const provenanceLine = (
  servedBy: string | Record<string, number> | null | undefined,
  isExternal?: boolean,
  savedAt?: number,
): string => {
  if (servedBy === undefined || servedBy === null) return '> Provenance: not recorded for this output.\n\n';
  // W485 (refutation) — an empty map means no call served this output; saying 'floor' about it is
  // a positive claim about a run that produced nothing.
  if (typeof servedBy === 'object' && !Object.entries(servedBy).some(([, n]) => (n || 0) > 0)) {
    return NO_SERVED_CALL_LINE;
  }
  const map = typeof servedBy === 'object';
  const b = map ? provenanceMapBadge(servedBy as Record<string, number>, isExternal)
                : provenanceBadge(servedBy as string, isExternal);
  // W485 (refutation) — `.every` on an EMPTY map is vacuously true, so a provenance map with no
  // served calls was labelled 'composed by the deterministic native structured engine' — a positive
  // claim about a run that served nothing. And the backend's non-model set is {native, template},
  // not {native}: a template-served output was being labelled as though a model had composed it.
  const NON_MODEL = ['native', 'template'];
  const served = map
    ? Object.entries(servedBy as Record<string, number>).filter(([, n]) => (n || 0) > 0)
    : [];
  const floor = map
    ? served.length > 0 && served.every(([k]) => NON_MODEL.includes(k))
    : NON_MODEL.includes(String(servedBy));
  return `> Provenance: ${b.label}${floor
    ? ' — composed by the deterministic native structured engine, not by a model. It arranges the'
      + ' headings it was asked for; it does not supply analysis.'
    : ''}\n> ${savedAt ? 'Saved' : 'Exported'} ${new Date(savedAt ?? Date.now()).toISOString()} from Workstation.\n\n`;
};
export type ComplianceVerdictRow = { framework?: string; status?: string; coverage?: string; escalate?: string[] };
export type ComplianceRecord = {
  overall?: string | null; verdicts?: ComplianceVerdictRow[] | null;
  coverage_gaps?: string[] | null; assessed_by?: string[] | null; basis?: string | null;
  // tri-state: false = a row refused it · true = every area assessed and passed · null = not established
  compliant?: boolean | null;
  // W485 — false when the screen could not assess the subject (a pending board pack).
  assessable?: boolean;
};
export const complianceChip = (c: ComplianceRecord | null | undefined) => {
  // W485 — a record that says it could not be assessed is never rendered as a verdict, whatever
  // else it carries.
  const overall = c?.assessable === false ? null : (c?.overall ?? null);
  const rows = c?.verdicts ?? [];
  // W483 (refutation) — a record written BEFORE this round carries no coverage fields at all, and
  // deriving from their absence asserted "nothing assessed this" about a verdict that predates the
  // question. `legacy` is that case: the chip says the record is older than the rule instead of
  // making a claim about it. A record with rows that DO carry coverage is read normally.
  const hasCoverage = c?.coverage_gaps !== undefined || c?.assessed_by !== undefined
    || rows.some(v => v?.coverage !== undefined);
  const legacy = !!overall && !hasCoverage;
  const gaps = c?.coverage_gaps ?? rows.filter(v => v?.coverage === 'none' || v?.coverage === 'screen'
    || v?.status === 'not_assessed' || v?.status === 'not_checked').map(v => v?.framework || '?');
  const assessedBy = c?.assessed_by ?? rows.filter(v => v?.coverage === 'engine'
    && v?.status && !['not_assessed', 'not_checked', 'error'].includes(v.status)).map(v => v?.framework || '?');
  const escalated = rows.flatMap(v => (v?.escalate ?? []).map(d => `${v?.framework}:${d}`));
  const qualifier = legacy ? ' (recorded before W483)'
    : overall === 'pass' && !assessedBy.length ? ' (screen only)'
    : overall === 'pass' && gaps.length ? ` (${assessedBy.join(' · ')} only)` : '';
  // A pass nothing assessed is never emerald — nor is a pass we cannot interrogate.
  const cls = (overall === 'pass' && (legacy || !assessedBy.length))
    ? 'bg-slate-800 text-slate-400' : complianceCls(overall);
  const detail = rows.map(v => `${v?.framework}:${v?.status}${v?.coverage ? ` [${v.coverage}]` : ''}`).join(' · ');
  // W576 (FU-318) — A DIMENSION-LEVEL GAP REACHES THE READER. This derived everything from
  // framework-level status and coverage, so the ethical engine's four inner dimensions were
  // invisible: a reader saw THAT the framework was assessed, never that one of its dimensions was
  // not. The compliance layer now carries them, and an unassessed dimension is named here — at
  // framework level the row can still read "assessed" while a dimension inside it assessed nothing.
  const dimGaps = rows.flatMap(v => ((v as any)?.dimensions_not_assessed ?? [])
    .map((d: string) => `${v?.framework}:${d}`));
  return {
    cls,
    label: `compliance: ${overall ?? 'not screened'}${qualifier}`,
    title: `§11 live compliance — ${detail || 'no framework detail recorded'}`
      + (legacy
        ? '\nThis verdict was recorded before the rule that a screen can refuse but never clear, so what it assessed was not recorded.'
        : (assessedBy.length ? `\nASSESSED by: ${assessedBy.join(' · ')}` : '\nNOTHING here assessed this subject')
          + (gaps.length ? `\nNOT assessed: ${gaps.join(' · ')} — a keyword screen can refuse a subject, not clear one` : '')
          + (dimGaps.length ? `\nDIMENSIONS not assessed: ${dimGaps.join(' · ')} — the framework ran and these dimensions inside it assessed nothing` : ''))
      + (escalated.length ? `\nESCALATED for a human: ${escalated.join(' · ')}` : '')
      + (c?.compliant === null || c?.compliant === undefined ? '' : `\ncompliant: ${c.compliant}`),
  };
};
export const provenanceMapFromTrace = (steps: Array<{ served_by?: string | null }> | null | undefined): Record<string, number> => {
  const m: Record<string, number> = {};
  for (const s of steps ?? []) { const k = s?.served_by || 'native'; m[k] = (m[k] || 0) + 1; }
  return m;
};
export const provenanceMapBadge = (servedBy: Record<string, number> | null | undefined, anyExternal?: boolean): ProvBadge => {
  const keys = Object.entries(servedBy ?? {}).filter(([, n]) => (n || 0) > 0).map(([k]) => k);
  // refuter F4 — an external run still lists the owned model in its map; 'via' names only the accelerant
  if (anyExternal) return { label: `via ${keys.filter(k => k !== 'native' && !k.startsWith('ollama:')).join(' · ') || 'external'}`, cls: 'bg-amber-500/20 text-amber-400',
    title: 'served by an external accelerant (opt-in)' };
  // W490 (refutation) — an EMPTY map is not the floor: it is the absence of any record, and this
  // returned the floor's positive claim for it (the same shape W485 fixed in provenanceLine).
  if (!keys.length) return provenanceBadge(null);
  if (keys.every(k => k === 'native')) return provenanceBadge('native');
  // W495 (FU-123, S11.3) - the map variant had the same defect as the single-token one: every key that
  // is not 'native' was counted as a MODEL, so the backend's non-model placeholders ('real-engine',
  // 'none', 'unavailable', '') inflated modelCalls and could carry the map to the emerald in-house arm.
  // They are counted apart and named, never as model calls.
  const NON_MODEL = new Set(['native', 'template', 'real-engine', 'none', 'unavailable', '']);
  const models = keys.filter(k => !NON_MODEL.has(k));
  const placeholders = keys.filter(k => k !== 'native' && NON_MODEL.has(k));
  const floorCalls = servedBy?.['native'] || 0;
  const modelCalls = models.reduce((n, k) => n + (servedBy?.[k] || 0), 0);
  const placeholderCalls = placeholders.reduce((n, k) => n + (servedBy?.[k] || 0), 0);
  if (!models.length) return { label: `no model call recorded${placeholderCalls ? ` · ${placeholders.join(' · ')}` : ''}`,
    cls: 'bg-slate-800 text-slate-400',
    title: `this run records ${floorCalls} floor call(s)${placeholderCalls ? ` and ${placeholderCalls} call(s) that served nothing (${placeholders.join(', ')})` : ''} and no model call, so nothing here is model output` };
  // W479 (refutation 3) — the counts decide: a run the floor served mostly is not an in-house model run,
  // and the tooltip states the split instead of assuming the model served most calls
  if (floorCalls >= modelCalls) return { label: `mostly structured floor · ${floorCalls} of ${floorCalls + modelCalls} calls (+${models.join(' · ')})`,
    cls: 'bg-amber-500/20 text-amber-400',
    title: `the deterministic floor served ${floorCalls} of ${floorCalls + modelCalls} calls (structured output, not model analysis); the owned model served ${modelCalls}` };
  return { label: `in-house · ${models.join(' · ')}${floorCalls ? ` (+${floorCalls} floor)` : ''}`, cls: 'bg-emerald-500/20 text-emerald-400',
    title: floorCalls ? `a mix: the owned model served ${modelCalls} of ${floorCalls + modelCalls} calls; the deterministic floor served the rest` : undefined };
};

// W449 (delivery-plan P1.1, ledger 1.1) — the living-QMS gate has THREE honest states: pass · fail ·
// NOT ASSESSABLE (null — the deterministic floor served the content, and the gate cannot measure floor
// output: the floor emits the caller's own headings, so coverage cannot fail by construction). Twenty
// renderers branched on truthiness or `typeof === 'boolean'`, so a null verdict would have painted
// amber "flagged" on DomainTool and vanished everywhere else. One helper, every chip; a guard test
// (test_w449_qms_chip_renders_through_one_helper) fails on any inline `qms_gate_passed ?` ternary.
export type QmsQuality = {
  qms_gate_passed?: boolean | null; qms_basis?: string | null;
  delivery_coverage?: number | null; document_controlled?: boolean | null;
} | null | undefined;
export const qmsChip = (q: QmsQuality, prefix = 'QMS') => {
  if (!q || q.qms_gate_passed === undefined) return null;   // no gate ran (or a gate error) — no chip
  const v = q.qms_gate_passed;
  const cov = typeof q.delivery_coverage === 'number' ? ` · cov ${Math.round(q.delivery_coverage * 100)}%` : '';
  const doc = q.document_controlled ? ' · doc-controlled' : '';
  if (v === null) return { verdict: 'not assessable' as const, label: `${prefix} —`, cls: 'bg-slate-800 text-slate-500',
    title: q.qms_basis || 'not assessable — floor-served: the floor emits the requested headings, so the gate cannot measure it' };
  if (v) return { verdict: 'pass' as const, label: `${prefix} pass${cov}${doc}`, cls: 'bg-emerald-500/15 text-emerald-400',
    title: q.qms_basis || 'living-QMS gate passed on real coverage/stub metrics' };
  return { verdict: 'fail' as const, label: `${prefix} fail${cov}${doc}`, cls: 'bg-vital/15 text-vital',
    title: q.qms_basis || 'living-QMS gate failed on real coverage/stub metrics' };
};

/**
 * W506 (FU-160 S3.8) — what the biomimetic record actually SAYS about the layers.
 *
 * Both tooltips read `7 biomimetic layers · {self}` — a flat count of what is DECLARED, over a chip reporting
 * one layer's health. The record says how many CONTRIBUTED, and since W506 it also says which layers hold code
 * that nothing calls. Two readers asserting a claim its writer has stopped making is how an untruth survives a
 * fix, so both now read the same fields through this one helper.
 */
/**
 * W658 (Owner ruling 2026-10-10) - the immune figure, said with what it rests on. The sensor hears failures; with
 * no call observed in its window "no failure" is not a reading, and seven places printed it as 100%.
 * A record stored before the count existed carries no count: its figure is printed as it was, since nothing can
 * say now how many calls stood behind it.
 */
export const immuneReading = (imm: { health?: number | null; observations_in_window?: number | null } | null | undefined): string => {
  if (!imm || imm.health === null || imm.health === undefined) return 'not read';
  if (imm.observations_in_window === 0) return 'nothing observed';
  return `${Math.round(imm.health * 100)}%`;
};

export const layerTitle = (bio: {
  layers?: string[];
  layers_declared?: string[];
  layer_states?: Record<string, string>;
  self?: string;
} | null | undefined): string => {
  if (!bio) return 'no biomimetic record was returned for this run';
  const declared = bio.layers_declared?.length ?? 0;
  const contributed = bio.layers ?? [];
  const states = bio.layer_states ?? {};
  const unreached = Object.keys(states).filter(k => states[k] === 'code_exists_unreached');
  const parts = [
    declared
      ? `${contributed.length} of ${declared} declared layers contributed a value${contributed.length ? `: ${contributed.join(', ')}` : ''}`
      : `${contributed.length} layer(s) contributed a value`,
  ];
  if (unreached.length) {
    parts.push(`code exists but nothing calls it: ${unreached.join(', ')}`);
  }
  if (bio.self) parts.push(bio.self);
  return parts.join(' · ');
};

/**
 * W506 (P2.4/FU-248) — the provenance line, rendered so the TARGET FORMAT can carry it.
 *
 * `provenanceLine` emits a markdown blockquote, which is right for a .md or .txt download and wrong for
 * everything else: prepending `> Provenance: ...` to a .py file is a syntax error and to a .json file is
 * corruption. Generator.tsx exports eight formats and CreatorStudio saves a canvas as JSON, so both were left
 * unlabelled rather than broken — an understandable choice, and still a file leaving the platform with no
 * statement of what produced it.
 *
 * Returns '' for formats with no comment syntax (json). Those callers must put the provenance IN the document —
 * a key on the object — because a corrupted download is worse than an unlabelled one.
 */
const COMMENT_SYNTAX: Record<string, [string, string]> = {
  python: ['# ', ''],
  yaml: ['# ', ''],
  toml: ['# ', ''],
  typescript: ['// ', ''],
  javascript: ['// ', ''],
  sql: ['-- ', ''],
  html: ['<!-- ', ' -->'],
  markdown: ['> ', ''],
  text: ['# ', ''],
};

export const provenanceComment = (
  format: string,
  servedBy: string | Record<string, number> | null | undefined,
  isExternal?: boolean,
): string => {
  const syntax = COMMENT_SYNTAX[(format || '').toLowerCase()];
  if (!syntax) return '';            // json and anything else with no comment form — the caller adds a key
  const [open, close] = syntax;
  // reuse provenanceLine's RULES, not its punctuation: strip its markdown and its blank lines
  const body = provenanceLine(servedBy, isExternal).replace(/^>\s*/gm, '').trim();
  return body.split('\n').map(l => `${open}${l}${close}`).join('\n') + '\n\n';
};

/**
 * W506 (P2.4/FU-248) — the provenance as a VALUE, for formats that cannot hold a comment.
 * A caller merges this into the object it is about to stringify.
 */
export const provenanceField = (
  servedBy: string | Record<string, number> | null | undefined,
  isExternal?: boolean,
): Record<string, string> => ({
  _provenance: provenanceLine(servedBy, isExternal).replace(/^>\s*/gm, '').trim(),
});

/**
 * W506 (P2.7(7)) — what a venture "position" actually is, for the figure beside it.
 *
 * MEASURED: a cycle records positions against NAMED living VSBs and no investee is ever credited —
 * `_record_positions_locked` writes the investor's holdings and nothing else, while the board pack rendered
 * "Venture portfolio (§6) 105 WST · 5 positions" with those names, as if capital had been deployed. The
 * criterion P2.7(7) is explicit that the label belongs on the figure a reader sees, not only in the payload.
 *
 * The wording is the SERVER's (`funding_basis`), never restated here: a helper that mirrors a rule instead of
 * carrying it becomes the second writer that drifts. When the server says nothing, this says that — it does
 * not assume the funded case, because an older response that predates the field is not evidence of funding.
 */
export const fundingLabel = (
  fundingState: string | null | undefined,
  fundingBasis?: string | null,
): { short: string; full: string; unfunded: boolean } => {
  if (fundingState === 'recorded_unfunded') {
    return {
      short: 'recorded, unfunded',
      full: fundingBasis || 'recorded, unfunded — the investee is not credited.',
      unfunded: true,
    };
  }
  if (!fundingState) {
    return {
      short: 'funding not stated',
      full: 'this response does not say whether the investee was credited, so nothing here establishes that it was.',
      unfunded: false,
    };
  }
  return { short: fundingState, full: fundingBasis || fundingState, unfunded: false };
};
