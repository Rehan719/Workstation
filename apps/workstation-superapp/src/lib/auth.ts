// §14 (W296) — the front door's token layer. Honest semantics:
//  - AUTH OFF (default single-user mode): everything works with no token; the UI says so plainly.
//  - AUTH ON: the stored bearer token rides on EVERY /api call (fetch + axios) without touching
//    the dozens of existing call sites; 401s surface as a redirect to /login.
// Registration stays Owner-curated (the backend's /register is admin-only by design) — the login
// page never pretends self-serve signup exists.
import axios from 'axios';

const KEY = 'workstation_token';

export const getToken = (): string | null => localStorage.getItem(KEY);
export const setToken = (t: string): void => localStorage.setItem(KEY, t);
export const clearToken = (): void => localStorage.removeItem(KEY);

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

export interface WhoAmI { mode: 'auth-off' | 'authenticated' | 'anonymous'; username?: string; role?: string }

/** Honest identity probe: distinguishes auth-off single-user mode from a real session. */
export async function whoami(): Promise<WhoAmI> {
  try {
    const r = await fetch('/api/v1/auth/me');
    if (r.status === 401) return { mode: 'anonymous' };
    const d = await r.json();
    const u = d?.user ?? d;
    if (u?.username) return { mode: 'authenticated', username: u.username, role: u.role };
    return { mode: 'auth-off' };
  } catch {
    return { mode: 'auth-off' };
  }
}
