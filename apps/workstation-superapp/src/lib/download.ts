// §4.9 (W338/W343) — authenticated downloads: raw <a href> anchors bypass the bearer layer, so
// under AUTH_ENABLED every UI export format dead-ended with a 401 (audit-proven). Fetching via the
// patched window.fetch (auth.ts attaches the token) and handing the browser an object URL keeps
// every export working in BOTH modes. Failure surfaces to the caller — never a silent dead click.
import { bodyOrNull, bodyDetail } from './api';

//  W989 (FU-399 part 21) - A REFUSED EXPORT SAYS THE SERVER'S REASON. This said "Export failed (HTTP 404)" and
//  dropped what the server said (the deliverable it no longer holds, the format it does not serve) on every page that
//  exports. The status is checked by the caller below; the body is read only to say why.
async function refused(r: Response): Promise<Error> {
  const d = bodyDetail(await bodyOrNull(r), '');   // W1013 - a field check by its field (it said JSON)
  return new Error(`Export failed (HTTP ${r.status})${d ? `: ${d}` : ''}`);
}

export async function downloadExport(url: string, fallbackName: string): Promise<void> {
  const r = await fetch(url);
  if (!r.ok) throw await refused(r);
  const blob = await r.blob();
  const dispo = r.headers.get('Content-Disposition') || '';
  const m = /filename="?([^";]+)"?/.exec(dispo);
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = m?.[1] || fallbackName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
}

// Open an exported document in a new tab (HTML/slides) — same bearer-carrying path.
export async function openExport(url: string): Promise<void> {
  const r = await fetch(url);
  if (!r.ok) throw await refused(r);
  const blob = await r.blob();
  const objectUrl = URL.createObjectURL(new Blob([blob], { type: blob.type || 'text/html' }));
  window.open(objectUrl, '_blank');
  setTimeout(() => URL.revokeObjectURL(objectUrl), 60_000);
}
