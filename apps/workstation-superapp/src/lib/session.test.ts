// W1253 — a session that runs out is renewed in place, once; only a renewal that fails sends the person to sign in,
// and the sign-in page is told why and which page to send them back to.
//
// The access token lasts ACCESS_TOKEN_TTL (60 minutes by default). When it ran out, the next /api call answered 401 and
// the page cleared the token and went to /login with nothing said, and what the person was typing was lost, though the
// sign-in had handed out a refresh token the page never kept. Each case here drives installAuth()'s fetch and axios
// paths against a server stood in for by one function, answering as the routes answer: a data route takes only the
// access token now current, and POST /api/v1/auth/refresh takes { refresh_token } and answers { access_token,
// refresh_token, token_type, expires_in }, or 401 when it refuses. Every token is a made-up string.
import type { AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { afterEach, describe, expect, it, vi } from 'vitest';

const OLD = 'w1253-made-up-access-old';
const NEW = 'w1253-made-up-access-new';
const REFRESH = 'w1253-made-up-refresh-1';
const REFRESH2 = 'w1253-made-up-refresh-2';
const DATA = '/api/v1/dashboard/summary';
const SLOW = '/api/v1/w1253-made-up-slow-read';
const ME = '/api/v1/auth/me';
const RENEW = '/api/v1/auth/refresh';
const EXPIRED = { detail: 'Invalid or expired token: Signature has expired.' };

type Call = { url: string; auth: string | null; body: string | null };
type Answer = { status: number; body: unknown };

//  the server. `renew`: whether the refresh route renews or refuses; `takes`: the one access token a data route takes
function server(renew: 'renews' | 'refuses', takes = NEW) {
  const calls: Call[] = [];
  const answer = async (url: string, auth: string | null, body: string | null): Promise<Answer> => {
    calls.push({ url, auth, body });
    //  a call sent again and again would never end: past twenty the stand-in stops answering 401, so the case ends red
    if (calls.length > 20) return { status: 503, body: { detail: 'W1253 stand-in: a call was sent again and again' } };
    if (url === RENEW) {
      await new Promise(r => setTimeout(r, 5));   // out for a moment, so the 401s that come meanwhile wait for it
      return renew === 'renews'
        ? { status: 200, body: { access_token: NEW, refresh_token: REFRESH2, token_type: 'bearer', expires_in: 3600 } }
        : { status: 401, body: EXPIRED };
    }
    if (url === SLOW) await new Promise(r => setTimeout(r, 40));   // answers after the renewal is done
    if (auth !== `Bearer ${takes}`) return { status: 401, body: EXPIRED };
    return { status: 200, body: url === ME ? { user: { username: 'w1253-made-up-name', role: 'user' } } : { read: url } };
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const auth = (init?.headers as Record<string, string> | undefined)?.Authorization ?? null;
    const a = await answer(url, auth, typeof init?.body === 'string' ? init.body : null);
    return { ok: a.status < 400, status: a.status, json: async () => a.body };
  }));
  return { calls, answer };
}

//  the page's address, with assign recorded instead of followed
function at(pathname: string, search = '', hash = '') {
  const assign = vi.fn();
  vi.stubGlobal('location', { ...window.location, pathname, search, hash, assign });
  return assign;
}

//  signed in: an access token that has run out and the refresh token the same sign-in handed out, then the token
//  layer installed fresh (its axios is the one the test drives)
let putBack: (() => void) | null = null;
async function signedIn() {
  vi.resetModules();
  const auth = await import('./auth');
  const ax = (await import('axios')).default;
  ax.interceptors.request.clear();
  ax.interceptors.response.clear();
  const before = ax.defaults.adapter;
  putBack = () => { ax.defaults.adapter = before; };
  localStorage.setItem('workstation_token', OLD);
  localStorage.setItem('workstation_refresh', REFRESH);
  auth.installAuth();
  return { auth, ax };
}

//  axios answered by the same server
function adapter(answer: (url: string, auth: string | null, body: string | null) => Promise<Answer>) {
  return async (config: InternalAxiosRequestConfig): Promise<AxiosResponse> => {
    const auth = (config.headers as unknown as Record<string, string | undefined>).Authorization ?? null;
    const a = await answer(String(config.url), auth, null);
    const response = { data: a.body, status: a.status, statusText: '', headers: {}, config, request: {} } as AxiosResponse;
    const ok = config.validateStatus ? config.validateStatus(a.status) : a.status < 400;
    if (!ok) throw Object.assign(new Error(`Request failed with status code ${a.status}`), { isAxiosError: true, config, response });
    return response;
  };
}

describe('a session that runs out is renewed once, and only a renewal that fails sends the person to sign in (W1253)', () => {
  afterEach(() => {
    putBack?.();
    putBack = null;
    vi.unstubAllGlobals();
    localStorage.clear();
  });

  it('renews a 401 once with the stored refresh token and sends the call again, and the person stays on the page', async () => {
    const assign = at('/genesis');
    const { calls } = server('renews');
    const { auth } = await signedIn();
    const res = await window.fetch(DATA);
    expect(res.status).toBe(200);
    expect(calls.map(c => c.url)).toEqual([DATA, RENEW, DATA]);
    expect(JSON.parse(String(calls[1].body))).toEqual({ refresh_token: REFRESH });
    expect(calls[1].auth).toBeNull();
    expect([calls[0].auth, calls[2].auth]).toEqual([`Bearer ${OLD}`, `Bearer ${NEW}`]);
    expect([auth.getToken(), auth.getRefreshToken()]).toEqual([NEW, REFRESH2]);
    expect(assign).not.toHaveBeenCalled();
  });

  it('shares one renewal among 401s that come together, and sends one that comes after it with the token it gave', async () => {
    at('/');
    const { calls } = server('renews');
    await signedIn();
    const slow = window.fetch(SLOW);
    const together = await Promise.all([window.fetch(DATA), window.fetch('/api/v1/vsb'), window.fetch('/api/v1/plan')]);
    expect(together.map(r => r.status)).toEqual([200, 200, 200]);
    expect((await slow).status).toBe(200);
    expect(calls.filter(c => c.url === RENEW)).toHaveLength(1);
    expect(calls.filter(c => c.url === SLOW).map(c => c.auth)).toEqual([`Bearer ${OLD}`, `Bearer ${NEW}`]);
  });

  it('sends the person to sign in once when the renewal is refused, saying the session ended and where they were, and sends nothing again', async () => {
    const assign = at('/genesis', '?domain=science');
    const { calls } = server('refuses');
    const { auth } = await signedIn();
    const answered = await Promise.all([window.fetch(DATA), window.fetch('/api/v1/vsb'), window.fetch('/api/v1/plan')]);
    expect(answered.map(r => r.status)).toEqual([401, 401, 401]);
    expect(calls.map(c => c.url)).toEqual([DATA, '/api/v1/vsb', '/api/v1/plan', RENEW]);
    expect(assign).toHaveBeenCalledTimes(1);
    expect(assign).toHaveBeenCalledWith('/login?session=ended&next=%2Fgenesis%3Fdomain%3Dscience');
    expect([auth.getToken(), auth.getRefreshToken()]).toEqual([null, null]);
  });

  it('never sends a call a third time: one refused again after the renewal sends the person to sign in', async () => {
    const assign = at('/vsb-cockpit', '?tab=chat');
    const { calls } = server('renews', 'w1253-made-up-a-token-never-handed-out');
    await signedIn();
    const res = await window.fetch(DATA);
    expect(res.status).toBe(401);
    expect(calls.map(c => c.url)).toEqual([DATA, RENEW, DATA]);
    expect(assign).toHaveBeenCalledTimes(1);
    expect(assign).toHaveBeenCalledWith('/login?session=ended&next=%2Fvsb-cockpit%3Ftab%3Dchat');
  });

  it('renews an axios call that axios throws for on a 401, the same way and once', async () => {
    const assign = at('/');
    const { calls, answer } = server('renews');
    const { ax } = await signedIn();
    ax.defaults.adapter = adapter(answer);
    expect((await ax.get(DATA)).status).toBe(200);
    expect((await ax.get('/api/v1/vsb')).status).toBe(200);
    expect(calls.map(c => [c.url, c.auth])).toEqual([
      [DATA, `Bearer ${OLD}`], [RENEW, null], [DATA, `Bearer ${NEW}`], ['/api/v1/vsb', `Bearer ${NEW}`]]);
    expect(assign).not.toHaveBeenCalled();
  });

  it('renews an axios call whose caller takes every status, the same way and once', async () => {
    const assign = at('/');
    const { calls, answer } = server('renews');
    const { ax } = await signedIn();
    ax.defaults.adapter = adapter(answer);
    const r = await ax.get(DATA, { validateStatus: () => true });
    expect([r.status, r.data]).toEqual([200, { read: DATA }]);
    expect(calls.map(c => c.url)).toEqual([DATA, RENEW, DATA]);
    expect(assign).not.toHaveBeenCalled();
  });

  it('never sends an axios call a third time, and sends the person to sign in once', async () => {
    const assign = at('/');
    const { calls, answer } = server('renews', 'w1253-made-up-a-token-never-handed-out');
    const { ax } = await signedIn();
    ax.defaults.adapter = adapter(answer);
    await expect(ax.get(DATA)).rejects.toMatchObject({ response: { status: 401 } });
    expect(calls.map(c => c.url)).toEqual([DATA, RENEW, DATA]);
    expect(assign).toHaveBeenCalledTimes(1);
    expect(assign).toHaveBeenCalledWith('/login?session=ended');
  });

  it('renews nothing for a route that hands out tokens: its 401 is its answer, and the page stays', async () => {
    const assign = at('/');
    const { calls } = server('renews');
    await signedIn();
    const res = await window.fetch('/api/v1/auth/token', { method: 'POST' });
    expect(res.status).toBe(401);
    expect(calls.map(c => c.url)).toEqual(['/api/v1/auth/token']);
    expect(assign).not.toHaveBeenCalled();
  });

  it('the boot probe renews a session that ran out, and sends one it could not renew to sign in, saying it ended', async () => {
    let assign = at('/my-work');
    server('renews');
    let { auth } = await signedIn();
    await auth.sendSignedOutToLogin();
    expect(assign).not.toHaveBeenCalled();
    expect(auth.getToken()).toBe(NEW);
    vi.unstubAllGlobals();
    localStorage.clear();
    assign = at('/my-work');
    server('refuses');
    ({ auth } = await signedIn());
    await auth.sendSignedOutToLogin();
    expect(assign).toHaveBeenCalledWith('/login?session=ended&next=%2Fmy-work');
  });

  it('the sign-in page is never sent back to an address on another site, nor to itself', async () => {
    const { returnPath } = await import('./auth');
    for (const bad of ['//elsewhere', '//elsewhere/a-path', 'https://elsewhere/a-path', '/\\elsewhere', '/\telsewhere',
                       '/.//elsewhere', 'javascript:void(0)', 'elsewhere', '', null, undefined, '/login',
                       '/login?next=%2Fgenesis', '/login/']) {
      expect(returnPath(bad)).toBe('/');
    }
    expect(returnPath('/genesis')).toBe('/genesis');
    expect(returnPath('/vsb-cockpit?tab=chat#converse')).toBe('/vsb-cockpit?tab=chat#converse');
    expect(returnPath('/a-made-up-folder/../genesis')).toBe('/genesis');
  });
});
