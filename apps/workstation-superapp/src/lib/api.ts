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
