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
  axios.interceptors.request.use(cfg => {
    const t = getToken();
    if (t && (cfg.url ?? '').startsWith('/api')) {
      cfg.headers = cfg.headers ?? {};
      (cfg.headers as Record<string, string>)['Authorization'] = `Bearer ${t}`;
    }
    return cfg;
  });
  const origFetch = window.fetch.bind(window);
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
    const t = getToken();
    if (t && url.startsWith('/api')) {
      init = init ?? {};
      init.headers = { ...(init.headers as Record<string, string> ?? {}), Authorization: `Bearer ${t}` };
    }
    return origFetch(input, init);
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
