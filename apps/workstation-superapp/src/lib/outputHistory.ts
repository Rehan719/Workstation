// §9 — "My Work": the user's history of AI tool/journey outputs.
//
// Storage is now two-tier and honest about which tier is in play:
//   • SIGNED IN  → the server-side per-user workspace (/api/v1/user/workspace). The history follows
//     the USER across devices and browsers; localStorage acts as an offline-capable mirror.
//   • AUTH OFF   → localStorage only, exactly as before (single-user mode, no server profile).
// Round 10 (W352) cleared local history on every identity change to stop a shared browser leaking
// one user's work to the next — the honest minimum. This is the real fix: the workspace lives with
// the user. Nothing here fabricates: a failed sync leaves local data intact and is reported.

export interface OutputRecord {
  id: string;
  kind: 'domain-tool' | 'genesis';
  title: string;
  domain?: string;
  endpoint?: string;
  input?: string;      // a short excerpt of what the user asked
  output: string;      // the result text (capped)
  provenance?: { served_by?: string; is_external?: boolean } | null;
  vsb_id?: string;    // W303 - links a genesis record to its living entity
  // §3A (W337) — refinement HISTORY: `output` is always the latest text; each refine pushes the
  // prior text here, so 'version n+1 persisted' is structural and no draft is ever lost.
  versions?: { output: string; refinedAt: number }[];
  refineCount?: number;
  ts: number;
}

const KEY = 'ws_output_history_v1';
const MAX_ENTRIES = 50;
const MAX_OUTPUT_CHARS = 24_000;
const MAX_INPUT_CHARS = 400;

function read(): OutputRecord[] {
  try {
    const raw = localStorage.getItem(KEY);
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch { return []; }
}

function write(records: OutputRecord[]) {
  try { localStorage.setItem(KEY, JSON.stringify(records.slice(0, MAX_ENTRIES))); } catch { /* quota/full — ignore */ }
  // §9 — mirror every local change up to the user's server workspace (no-op when signed out)
  scheduleWorkspacePush();
}

export function listOutputs(): OutputRecord[] {
  return read().sort((a, b) => b.ts - a.ts);
}

export function saveOutput(rec: Omit<OutputRecord, 'id' | 'ts'> & { id?: string; ts?: number }): OutputRecord {
  const record: OutputRecord = {
    id: rec.id ?? `out-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    ts: rec.ts ?? Date.now(),
    kind: rec.kind,
    vsb_id: rec.vsb_id,
    title: rec.title,
    domain: rec.domain,
    endpoint: rec.endpoint,
    input: rec.input ? rec.input.slice(0, MAX_INPUT_CHARS) : undefined,
    output: (rec.output || '').slice(0, MAX_OUTPUT_CHARS),
    provenance: rec.provenance ?? null,
    // W337 — cap version history (latest 5 priors, each output-capped) so quota stays sane
    versions: (rec.versions ?? []).slice(-5).map(v => ({
      output: (v.output || '').slice(0, MAX_OUTPUT_CHARS), refinedAt: v.refinedAt })),
    refineCount: rec.refineCount ?? 0,
  };
  const next = [record, ...read().filter(r => r.id !== record.id)].slice(0, MAX_ENTRIES);
  write(next);
  try { window.dispatchEvent(new CustomEvent('ws:output-history')); } catch { /* ignore */ }
  return record;
}

export function removeOutput(id: string) {
  write(read().filter(r => r.id !== id));
  try { window.dispatchEvent(new CustomEvent('ws:output-history')); } catch { /* ignore */ }
}

export function clearOutputs() {
  write([]);
  try { window.dispatchEvent(new CustomEvent('ws:output-history')); } catch { /* ignore */ }
}

// ── Server sync (§9) ─────────────────────────────────────────────────────────────────────────
// Only active when the user is signed in (a bearer token exists). Auth-off keeps the pure-local
// behaviour, so single-user mode is untouched.

import { getToken } from './auth';
import { getPrefs, setPrefs } from './userPrefs';

const WORKSPACE_URL = '/api/v1/user/workspace';
let _pushTimer: ReturnType<typeof setTimeout> | null = null;
let _lastSyncError = '';

/** The most recent sync failure, for surfacing honestly in the UI ('' when healthy). */
export function lastSyncError(): string { return _lastSyncError; }

function signedIn(): boolean {
  try { return !!getToken(); } catch { return false; }
}

/** Push the local workspace to the server (debounced). No-op when signed out. */
export function scheduleWorkspacePush(): void {
  if (!signedIn()) return;
  if (_pushTimer) clearTimeout(_pushTimer);
  _pushTimer = setTimeout(async () => {
    try {
      const res = await fetch(WORKSPACE_URL, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ history: read(), prefs: getPrefs() }),
      });
      _lastSyncError = res.ok ? '' : `Sync failed (HTTP ${res.status}) — your work is still saved in this browser.`;
    } catch {
      _lastSyncError = 'Sync failed — offline. Your work is still saved in this browser.';
    }
    try { window.dispatchEvent(new CustomEvent('ws:output-history')); } catch { /* ignore */ }
  }, 1200);
}

/** Pull the server workspace and adopt it locally. Call at boot and right after a login.
 *  Returns the number of records adopted, or null when signed out / unavailable. */
export async function syncWorkspaceFromServer(): Promise<number | null> {
  if (!signedIn()) return null;
  try {
    const res = await fetch(WORKSPACE_URL);
    if (!res.ok) {
      _lastSyncError = `Could not load your saved work (HTTP ${res.status}).`;
      return null;
    }
    const doc = await res.json();
    const serverHistory: OutputRecord[] = Array.isArray(doc.history) ? doc.history : [];
    // Union by id, newest first — a record made offline on this device is never dropped.
    const merged = [...serverHistory, ...read()]
      .filter((r, i, arr) => r && r.id && arr.findIndex(x => x.id === r.id) === i)
      .sort((a, b) => (b.ts ?? 0) - (a.ts ?? 0))
      .slice(0, MAX_ENTRIES);
    write(merged);
    if (doc.prefs && typeof doc.prefs === 'object' && Object.keys(doc.prefs).length) {
      setPrefs({ ...doc.prefs, ...getPrefs() });   // local edits win over the stored copy
    }
    _lastSyncError = '';
    try { window.dispatchEvent(new CustomEvent('ws:output-history')); } catch { /* ignore */ }
    if (merged.length !== serverHistory.length) scheduleWorkspacePush();   // push what the server lacked
    return merged.length;
  } catch {
    _lastSyncError = 'Could not reach the server — showing the work saved in this browser.';
    return null;
  }
}

/** Clear the server-side copy too (the Settings 'Clear preferences & history' control). */
export async function clearWorkspaceEverywhere(): Promise<void> {
  clearOutputs();
  if (!signedIn()) return;
  try {
    const res = await fetch(WORKSPACE_URL, { method: 'DELETE' });
    _lastSyncError = res.ok ? '' : `Server copy not cleared (HTTP ${res.status}).`;
  } catch { _lastSyncError = 'Server copy not cleared — offline.'; }
}
