// E3 — "My Work": a lightweight, honest, per-browser history of the user's AI tool/journey outputs.
// Stored in localStorage (local to this browser — no server, no fabrication). Lets users revisit, copy,
// download and remove past results that were previously lost on navigation. (§9 "personalised to each
// user's history" foundation; E5 builds on this.)

export interface OutputRecord {
  id: string;
  kind: 'domain-tool' | 'genesis';
  title: string;
  domain?: string;
  endpoint?: string;
  input?: string;      // a short excerpt of what the user asked
  output: string;      // the result text (capped)
  provenance?: { served_by?: string; is_external?: boolean } | null;
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
}

export function listOutputs(): OutputRecord[] {
  return read().sort((a, b) => b.ts - a.ts);
}

export function saveOutput(rec: Omit<OutputRecord, 'id' | 'ts'> & { id?: string; ts?: number }): OutputRecord {
  const record: OutputRecord = {
    id: rec.id ?? `out-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    ts: rec.ts ?? Date.now(),
    kind: rec.kind,
    title: rec.title,
    domain: rec.domain,
    endpoint: rec.endpoint,
    input: rec.input ? rec.input.slice(0, MAX_INPUT_CHARS) : undefined,
    output: (rec.output || '').slice(0, MAX_OUTPUT_CHARS),
    provenance: rec.provenance ?? null,
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
