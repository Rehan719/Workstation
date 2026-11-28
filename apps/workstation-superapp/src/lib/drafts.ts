// W1253 - what a person was typing is kept across a sign-in. When a session ends the page goes to the sign-in page, a
// whole new page load, and the text in Genesis's idea box or an enterprise's Converse box was lost with it. Each box
// keeps its text in this tab's sessionStorage as it is typed, under the account that typed it; puts it back when the
// page opens again for that same account (after a sign-in, a reload or a visit elsewhere); and drops it once it has
// done its work (the journey ran, the reply came). Text kept for one account is never shown to another: it is dropped
// unread. sessionStorage ends when the tab is closed, and nothing here is sent anywhere.
import { getToken } from './auth';

const PREFIX = 'ws_draft_';

/** The Genesis idea box. */
export const GENESIS_DRAFT = 'genesis-idea';
/** An enterprise's Converse box in the cockpit, one per enterprise. */
export const converseDraft = (vsbId: string): string => `cockpit-converse:${vsbId}`;

/** The account a draft belongs to: the id the stored sign-in was issued to (the token's uid, W1198b), '' with no
 *  sign-in (sign-in off), or null when the stored sign-in cannot be read, and then nothing is kept or put back. The
 *  token is read here, not checked: the server checks it on every call. */
export function draftOwner(): string | null {
  let t: string | null;
  try { t = getToken(); } catch { return null; }
  if (!t) return '';
  try {
    const part = (t.split('.')[1] ?? '').replace(/-/g, '+').replace(/_/g, '/');
    const claims = JSON.parse(atob(part.padEnd(Math.ceil(part.length / 4) * 4, '=')));
    const uid = claims?.uid ?? claims?.sub;
    return typeof uid === 'string' && uid ? uid : null;
  } catch { return null; }
}

/** Keep what is in a box as it is now; an empty box keeps nothing. Says whether it was kept. */
export function keepDraft(key: string, text: string): boolean {
  const by = draftOwner();
  try {
    if (by === null || !text.trim()) { sessionStorage.removeItem(PREFIX + key); return false; }
    sessionStorage.setItem(PREFIX + key, JSON.stringify({ by, text }));
    return true;
  } catch { return false; }
}

/** What was kept for a box, for the account signed in now, or '' when nothing was. Text kept for another account is
 *  dropped unread. Reading it leaves it kept: the box keeps it until it is used. */
export function takeDraft(key: string): string {
  try {
    const raw = sessionStorage.getItem(PREFIX + key);
    if (!raw) return '';
    const kept = JSON.parse(raw);
    const by = draftOwner();
    if (by !== null && kept?.by === by && typeof kept?.text === 'string') return kept.text;
    sessionStorage.removeItem(PREFIX + key);
    return '';
  } catch { return ''; }
}

/** Drop what was kept for a box once it has done its work. With `sent`, only when the box still keeps that text: what
 *  was typed while the work was out is kept. Says whether anything was dropped. */
export function dropDraft(key: string, sent?: string): boolean {
  try {
    const raw = sessionStorage.getItem(PREFIX + key);
    if (!raw) return false;
    if (sent !== undefined) {
      const kept = JSON.parse(raw);
      if (typeof kept?.text !== 'string' || kept.text.trim() !== sent.trim()) return false;
    }
    sessionStorage.removeItem(PREFIX + key);
    return true;
  } catch { return false; }
}
