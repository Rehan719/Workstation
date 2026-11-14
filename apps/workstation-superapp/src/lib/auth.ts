// §14 (W296) — the front door's token layer. Honest semantics:
//  - AUTH OFF (default single-user mode): everything works with no token; the UI says so plainly.
//  - AUTH ON: the stored bearer token rides on EVERY /api call (fetch + axios) without touching
//    the dozens of existing call sites; 401s surface as a redirect to /login.
// Registration stays Owner-curated (the backend's /register is admin-only by design) — the login
// page never pretends self-serve signup exists.
import { silenceIsRight } from '../components/ReadFailures';   // W961 (FU-1181)
import axios from 'axios';
import { bodyOrNull } from './api';   // W960 (FU-1181)
import { bodyDetail } from './api';   // W1013 - a refusal's reason, in the one reading

const KEY = 'workstation_token';

// §9 (W352) — "My Work" and prefs are a PER-BROWSER store (localStorage). On a shared browser that
// would leak one user's history to the next, contradicting the §9 "personalised to each user's
// history" intent. Clearing the local history+prefs on every identity change (login AND logout)
// closes that at a single choke point covering all call sites. (A durable per-USER server-side
// store is the larger follow-up, tracked in the backlog — this is the honest minimum.)
function _clearLocalUserData(): void {
  try {
    localStorage.removeItem('ws_output_history_v1');
    localStorage.removeItem('ws_user_prefs_v1');
    window.dispatchEvent(new CustomEvent('ws:output-history'));
    window.dispatchEvent(new CustomEvent('ws:user-prefs'));
  } catch { silenceIsRight('with no browser storage there is nothing to clear at sign-out')(); }
}

export const getToken = (): string | null => localStorage.getItem(KEY);
export const setToken = (t: string): void => { _clearLocalUserData(); localStorage.setItem(KEY, t); };
export const clearToken = (): void => { localStorage.removeItem(KEY); _clearLocalUserData(); };

let installed = false;

/** Install the token onto every /api call (fetch + axios). Idempotent; call once at app boot. */
export function installAuth(): void {
  if (installed) return;
  installed = true;
  // §14 (W317) — the documented 401→/login redirect is REAL now: a session that expires (or a
  // token that was revoked) lands the user on the login page instead of an app full of silently
  // failing calls. Only fires for a session that HELD a token — auth-off mode (no token) never
  // redirects; the login page itself is exempt so its own error text keeps working.
  const on401 = () => {
    if (getToken() && window.location.pathname !== '/login') {
      clearToken();
      window.location.assign('/login');
    }
  };
  axios.interceptors.request.use(cfg => {
    const t = getToken();
    if (t && (cfg.url ?? '').startsWith('/api')) {
      cfg.headers = cfg.headers ?? {};
      (cfg.headers as Record<string, string>)['Authorization'] = `Bearer ${t}`;
    }
    return cfg;
  });
  axios.interceptors.response.use(
    r => r,
    err => {
      if (err?.response?.status === 401) on401();
      return Promise.reject(err);
    },
  );
  const origFetch = window.fetch.bind(window);
  window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
    const t = getToken();
    if (t && url.startsWith('/api')) {
      init = init ?? {};
      init.headers = { ...(init.headers as Record<string, string> ?? {}), Authorization: `Bearer ${t}` };
    }
    const res = await origFetch(input, init);
    if (res.status === 401 && url.startsWith('/api') && !url.includes('/auth/')) on401();
    return res;
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
