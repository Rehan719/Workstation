// W965 (FU-1190) — the sha256 of a text, in lowercase hexadecimal: how a claim names an answer without sending it.
// The browser computes it only on a secure connection (https, or this machine); elsewhere it is not available, and
// the caller says so rather than send anything in its place.
export async function sha256Hex(text: string): Promise<string> {
  const subtle = globalThis.crypto?.subtle;
  if (!subtle) throw new Error('fingerprint unavailable');
  const digest = await subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
}
