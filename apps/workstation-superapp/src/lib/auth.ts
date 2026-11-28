// §14 (W296) — the front door's token layer. Honest semantics:
//  - AUTH OFF (default single-user mode): everything works with no token; the UI says so plainly.
//  - AUTH ON: the stored bearer token rides on EVERY /api call (fetch + axios) without touching
//    the dozens of existing call sites; 401s surface as a redirect to /login.
//  - W1253: a 401 first renews the session once with the stored refresh token; only one it cannot renew goes to
//    /login, which says the session ended and sends the person back to the page they were on.
// Registration stays Owner-curated (the backend's /register is admin-only by design) — the login
// page never pretends self-serve signup exists.
import { silenceIsRight } from '../components/ReadFailures';   // W961 (FU-1181)
import axios from 'axios';
import type { AxiosResponse, InternalAxiosRequestConfig } from 'axios';   // W1253 - an axios call sent again
import { bodyOrNull } from './api';   // W960 (FU-1181)
import { bodyDetail } from './api';   // W1013 - a refusal's reason, in the one reading

const KEY = 'workstation_token';
//  W1253 - the refresh token the sign-in hands out beside the access token (lib/auth.ts renews a session with it)
const REFRESH_KEY = 'workstation_refresh';

// §9 (W352) — "My Work" and prefs are a PER-BROWSER store (localStorage). On a shared browser that
// would leak one user's history to the next, contradicting the §9 "personalised to each user's
// history" intent. Clearing the local history+prefs on every identity change (login AND logout)
// closes that at a single choke point covering all call sites. (A durable per-USER server-side
// store is the larger follow-up, tracked in the backlog — this is the honest minimum.)
function _clearLocalUserData(): void {
  try {
    //  W1253 - and the last sign-in's refresh token: it renews only the session it was handed out with
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem('ws_output_history_v1');
    localStorage.removeItem('ws_user_prefs_v1');
    window.dispatchEvent(new CustomEvent('ws:output-history'));
    window.dispatchEvent(new CustomEvent('ws:user-prefs'));
    //  W1076 - and whatever a page holds for the person who was signed in: the avatar's conversation set it aside
    window.dispatchEvent(new CustomEvent('ws:identity'));
  } catch { silenceIsRight('with no browser storage there is nothing to clear at sign-out')(); }
}

export const getToken = (): string | null => localStorage.getItem(KEY);
export const setToken = (t: string): void => { _clearLocalUserData(); localStorage.setItem(KEY, t); };
export const clearToken = (): void => { localStorage.removeItem(KEY); _clearLocalUserData(); };

//  W1253 - the refresh token, stored after setToken (which clears the last sign-in's) and replaced at each renewal; a
//  sign-in that handed out none stores none, and then a session that runs out ends as it did before
export const getRefreshToken = (): string | null => localStorage.getItem(REFRESH_KEY);
export const setRefreshToken = (r: string | null | undefined): void => {
  if (r) localStorage.setItem(REFRESH_KEY, r);
  else localStorage.removeItem(REFRESH_KEY);
};

/** W1253 - the page a sign-in sends the person back to: a path on this site, or '/' for anything else. The sign-in page
 *  reads it from its own address (?next=), which anyone can write in a link, so it is never an address on another site
 *  (an open redirect): it starts with one '/', holds no backslash or control character, resolves to this page's own
 *  origin to a path that does not start with '//', and is not the sign-in page itself. */
export function returnPath(raw: string | null | undefined): string {
  if (!raw || !raw.startsWith('/') || raw.startsWith('//') || raw.includes('\\')) return '/';
  if ([...raw].some(c => c.charCodeAt(0) < 32 || c.charCodeAt(0) === 127)) return '/';
  const origin = window.location.origin;
  let u: URL;
  try { u = new URL(raw, origin); } catch { return '/'; }
  const path = u.pathname + u.search + u.hash;
  if (u.origin !== origin || path.startsWith('//') || u.pathname.replace(/\/+$/, '') === '/login') return '/';
  return path;
}

/** W1253 - the sign-in page's address, from the page the person is on: ?session=ended when a session they held ended,
 *  so the sign-in page says so, and ?next= with the page they were on (not the home page), so a sign-in sends them
 *  back to it. */
export function signInAddress(ended: boolean): string {
  const here = window.location;
  const back = returnPath(`${here.pathname}${here.search ?? ''}${here.hash ?? ''}`);
  const q = new URLSearchParams();
  if (ended) q.set('session', 'ended');
  if (back !== '/') q.set('next', back);
  const s = q.toString();
  return s ? `/login?${s}` : '/login';
}

/** W1233, W1253 - the page goes to the sign-in page, from anywhere but that page. A token still held is one the server
 *  no longer takes, so it is cleared; what the person was typing is kept (lib/drafts.ts). `ended` says a session they
 *  held has ended, and the sign-in page says so. */
export function goToSignIn(ended: boolean): void {
  if (window.location.pathname === '/login') return;
  if (getToken() || getRefreshToken()) clearToken();
  window.location.assign(signInAddress(ended));
}

//  W1253 - ONE SILENT REFRESH. The access token lasts ACCESS_TOKEN_TTL (60 minutes by default). When it ran out, the
//  next /api call answered 401 and the page cleared the token and went to /login with nothing said, and what the person
//  was typing was lost, though the sign-in had handed out a refresh token (REFRESH_TOKEN_TTL, 7 days by default) that
//  the page never kept. Now a 401 to a call that carried the sign-in renews it with the stored refresh token (POST
//  /api/v1/auth/refresh), once, and sends that call again, once:
//  - every 401 that comes while the exchange is out waits for that same exchange (renewing), and one that comes after
//    it is sent again with the token it gave (renewed): concurrent 401s share one refresh;
//  - the exchange and the call sent again go out on the browser's own fetch, past this layer, and an axios call sent
//    again is marked so, so neither can start another: it never loops;
//  - a renewal is the same person: the tokens are replaced in place, and nothing of theirs is cleared;
//  - the routes that hand out tokens are never renewed: their 401 is their answer;
//  - only when the exchange fails, or the call sent again is refused again, is the person sent to sign in.
let sendRaw: typeof window.fetch | null = null;
let renewing: Promise<string | null> | null = null;
let renewed: { from: string; to: string } | null = null;
const handsOutTokens = (url: string) =>
  ['/api/v1/auth/token', '/api/v1/auth/refresh', '/api/v1/auth/signup'].includes(url.split('?')[0]);
const fires401 = (url: string) => url.startsWith('/api') && !url.includes('/auth/');

async function exchange(): Promise<string | null> {
  const held = getRefreshToken();
  const from = getToken();
  if (!held || !from || !sendRaw) return null;
  let r: Response;
  try {
    r = await sendRaw('/api/v1/auth/refresh', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh_token: held }),
    });
  } catch { return null; }
  //  signed in or out while the exchange was out: what it answered belongs to a session that is gone
  if (getRefreshToken() !== held || getToken() !== from) return null;
  const d = r.ok ? await bodyOrNull<{ access_token?: string; refresh_token?: string }>(r) : null;
  if (!d?.access_token) {
    localStorage.removeItem(REFRESH_KEY);   // refused (run out, or its account removed): it renews nothing now
    return null;
  }
  localStorage.setItem(KEY, d.access_token);
  setRefreshToken(d.refresh_token ?? held);
  renewed = { from, to: d.access_token };
  return d.access_token;
}

/** W1253 - the token to send a call the server refused (401) again with, or null when it is not sent again: it carried
 *  no sign-in, it went to a route that hands out tokens, the sign-in changed while it was out, or the exchange failed. */
async function retryToken(sentWith: string | null | undefined, url: string): Promise<string | null> {
  if (!sentWith || handsOutTokens(url)) return null;
  const now = getToken();
  if (renewed && renewed.from === sentWith && now === renewed.to) return now;   // renewed while this call was out
  if (now !== sentWith) return null;
  if (!renewing) renewing = exchange().finally(() => { renewing = null; });
  return renewing;
}

/** W1253 - a 401 nothing renewed: the session the call was sent under has ended, and the page goes to sign in, saying
 *  so when the call carried a sign-in. A call sent under an earlier sign-in (the one held changed while it was out)
 *  ends nothing, and a sign-in call (/auth/ in the url) never sends the page anywhere: its own page says why. */
function ended401(sentWith: string | null | undefined, url: string): void {
  if (!fires401(url) || getToken() !== (sentWith ?? null)) return;
  goToSignIn(!!sentWith);
}

let installed = false;

/** Install the token onto every /api call (fetch + axios). Idempotent; call once at app boot. */
export function installAuth(): void {
  if (installed) return;
  installed = true;
  // §14 (W317) — the documented 401→/login redirect is REAL now: a session that expires (or a
  // token that was revoked) lands the user on the login page instead of an app full of silently
  // failing calls. The login page itself is exempt so its own error text keeps working.
  // W1233 - it fires on a 401 from an /api call whether or not a token was held, and clears a held one first. It
  // used to fire only for a session that held a token, so a visitor who never signed in was shown the Command
  // Center with every read failing (HTTP 401) instead of the sign-in page. Sign-in calls (/auth/ in the url) never
  // fire it, on either path. Auth-off mode never answers 401, so it never redirects.
  // W1253 - and first, one silent refresh (retryToken); only a 401 it could not cure goes to sign in (ended401).
  type Sent = { _w1253SentWith?: string | null; _w1253Again?: boolean };
  axios.interceptors.request.use(cfg => {
    const t = getToken();
    if (t && (cfg.url ?? '').startsWith('/api')) {
      cfg.headers = cfg.headers ?? {};
      (cfg.headers as Record<string, string>)['Authorization'] = `Bearer ${t}`;
    }
    (cfg as typeof cfg & Sent)._w1253SentWith = t;   // W1253 - the sign-in this call carries
    return cfg;
  });
  //  W1253 - a refused axios call is renewed and sent again once (_w1253Again marks the second send), whether axios
  //  threw for it or the caller takes every status (validateStatus); the second send's own 401 comes back through here
  const again = async (cfg: (InternalAxiosRequestConfig & Sent) | undefined, url: string): Promise<AxiosResponse | null> => {
    if (!cfg || cfg._w1253Again) return null;
    const fresh = await retryToken(cfg._w1253SentWith, url);
    if (!fresh) return null;
    cfg._w1253Again = true;
    return axios.request(cfg);
  };
  axios.interceptors.response.use(
    async r => {
      const url = String(r?.config?.url ?? '');
      if (r?.status !== 401 || !url.startsWith('/api')) return r;
      const cfg = r.config as InternalAxiosRequestConfig & Sent;
      const second = await again(cfg, url);
      if (second) return second;
      ended401(cfg?._w1253SentWith, url);
      return r;
    },
    async err => {
      const url = String(err?.config?.url ?? '');
      if (err?.response?.status === 401 && url.startsWith('/api')) {
        const cfg = err.config as InternalAxiosRequestConfig & Sent;
        const second = await again(cfg, url);
        if (second) return second;
        ended401(cfg?._w1253SentWith, url);
      }
      return Promise.reject(err);
    },
  );
  const origFetch = window.fetch.bind(window);
  sendRaw = origFetch;
  window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
    const t = getToken();
    //  W1253 - a call that may be sent again keeps a copy of its Request, whose body the first send uses up
    const spare = t && url.startsWith('/api') && typeof Request !== 'undefined' && input instanceof Request ? input.clone() : input;
    if (t && url.startsWith('/api')) {
      init = init ?? {};
      init.headers = { ...(init.headers as Record<string, string> ?? {}), Authorization: `Bearer ${t}` };
    }
    const res = await origFetch(input, init);
    if (res.status !== 401 || !url.startsWith('/api')) return res;
    const fresh = await retryToken(t, url);
    if (!fresh) {
      ended401(t, url);
      return res;
    }
    const second = await origFetch(spare, {
      ...init, headers: { ...(init?.headers as Record<string, string> ?? {}), Authorization: `Bearer ${fresh}` },
    });
    if (second.status === 401) ended401(fresh, url);
    return second;
  };
}

export interface WhoAmI {
  mode: 'auth-off' | 'authenticated' | 'anonymous' | 'unknown';
  username?: string; role?: string;
  basis?: string;   // W930 - why the session is not known, when it is not
}

/** Honest identity probe: distinguishes auth-off single-user mode from a real session.
 *  W930 - "auth off" is the server's own word (auth_enabled: false), never what a failed read is taken to mean: a
 *  refusal, an unreachable server, or an answer that names no user and does not say sign-in is off is 'unknown',
 *  with its reason. It used to be 'auth-off', so a 503 told a signed-out person the platform needs no sign-in. */
export async function whoami(): Promise<WhoAmI> {
  let r: Response;
  try {
    r = await fetch('/api/v1/auth/me');
  } catch {
    return { mode: 'unknown', basis: 'the server could not be reached' };
  }
  if (r.status === 401) return { mode: 'anonymous' };
  let d: any = null;
  d = await bodyOrNull(r);              // W960 (FU-1181) - no body is said just below
  if (!r.ok) {
    return { mode: 'unknown', basis: `Failed (HTTP ${r.status}): ${bodyDetail(d, 'no reason given')}` };   // W1013 - a field check by its field
  }
  const u = d?.user ?? d;
  if (u?.username) return { mode: 'authenticated', username: u.username, role: u.role };
  if (d?.auth_enabled === false) return { mode: 'auth-off' };
  return { mode: 'unknown', basis: 'the session answer named no user and did not say sign-in is off' };
}

/** W1233 - the boot probe: a signed-out visitor is sent to the sign-in page before the shell's reads fail one by
 *  one. Only 'anonymous' (the server answered 401) redirects, and never from /login itself: 'auth-off' needs no
 *  sign-in, and 'unknown' (a refusal or an unreachable server) is not known to be signed out, so the page stays and
 *  says why. A token still held is one the server no longer takes, so it is cleared.
 *  W1253 - whoami's own call is renewed like any other, so 'anonymous' here is a session the refresh could not renew,
 *  or none: when one was held, the sign-in page says it ended. The page the visitor asked for goes with them as
 *  ?next=, now that the sign-in page reads it (goToSignIn). */
export async function sendSignedOutToLogin(): Promise<void> {
  const who = await whoami();
  if (who.mode === 'anonymous') goToSignIn(!!(getToken() || getRefreshToken()));
}
