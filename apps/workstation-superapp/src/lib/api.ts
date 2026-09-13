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
export const provenanceBadge = (servedBy: string | null | undefined, isExternal?: boolean) => {
  const sb = servedBy ?? 'native';
  if (isExternal) return { label: `via ${sb}`, cls: 'bg-amber-500/20 text-amber-400',
    title: 'served by an external accelerant (opt-in)' };
  if (sb === 'native') return { label: 'structured floor — not model analysis', cls: 'bg-amber-500/20 text-amber-400',
    title: 'the deterministic native floor composes structured output from the request — it is not model inference' };
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
export const provenanceMapFromTrace = (steps: Array<{ served_by?: string | null }> | null | undefined): Record<string, number> => {
  const m: Record<string, number> = {};
  for (const s of steps ?? []) { const k = s?.served_by || 'native'; m[k] = (m[k] || 0) + 1; }
  return m;
};
export const provenanceMapBadge = (servedBy: Record<string, number> | null | undefined, anyExternal?: boolean) => {
  const keys = Object.entries(servedBy ?? {}).filter(([, n]) => (n || 0) > 0).map(([k]) => k);
  // refuter F4 — an external run still lists the owned model in its map; 'via' names only the accelerant
  if (anyExternal) return { label: `via ${keys.filter(k => k !== 'native' && !k.startsWith('ollama:')).join(' · ') || 'external'}`, cls: 'bg-amber-500/20 text-amber-400',
    title: 'served by an external accelerant (opt-in)' };
  if (!keys.length || keys.every(k => k === 'native')) return provenanceBadge('native');
  const models = keys.filter(k => k !== 'native');
  const floorCalls = servedBy?.['native'] || 0;
  return { label: `in-house · ${models.join(' · ')}${floorCalls ? ` (+${floorCalls} floor)` : ''}`, cls: 'bg-emerald-500/20 text-emerald-400',
    title: floorCalls ? 'a mix: the owned model served most calls; the deterministic floor served the rest' : undefined };
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
