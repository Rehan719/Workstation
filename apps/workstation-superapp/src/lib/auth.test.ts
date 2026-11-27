// W930 — whoami says the session as the server answers it. "Auth off" is the server's own word (GET /api/v1/auth/me
// answers { auth_enabled: false } when sign-in is off); a refusal, an unreachable server, or an answer that says
// neither is 'unknown', with its reason. It used to be 'auth-off' for all of them.
// W1233 - with sign-in on, a signed-out visitor is sent to /login: by the boot probe on an 'anonymous' session, and by a
// 401 from an /api data call with no token held. Auth off, an unknown session and a sign-in call's 401 never redirect.
import { afterEach, describe, expect, it, vi } from 'vitest';

import { whoami } from './auth';

const reply = (status: number, body: unknown) => ({ ok: status < 400, status, json: async () => body });
const serve = (r: unknown) => vi.stubGlobal('fetch', vi.fn(async () => r));

describe('whoami, the session as the server answers it', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('is auth off only when the server says sign-in is off', async () => {
    serve(reply(200, { auth_enabled: false, message: 'Single-user mode — no auth required.' }));
    expect(await whoami()).toEqual({ mode: 'auth-off' });
  });

  it('names a signed-in person as the server names them', async () => {
    serve(reply(200, { user: { username: 'ada', role: 'admin' } }));
    expect(await whoami()).toEqual({ mode: 'authenticated', username: 'ada', role: 'admin' });
  });

  it('is anonymous on a 401', async () => {
    serve(reply(401, { detail: 'Not authenticated' }));
    expect(await whoami()).toEqual({ mode: 'anonymous' });
  });

  it('is not known when the read is refused, with the server\'s reason, never auth off', async () => {
    serve(reply(503, { detail: 'the account store could not be read' }));
    expect(await whoami()).toEqual({ mode: 'unknown', basis: 'Failed (HTTP 503): the account store could not be read' });
  });

  it('is not known when the server cannot be reached', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('Failed to fetch'); }));
    expect(await whoami()).toEqual({ mode: 'unknown', basis: 'the server could not be reached' });
  });

  it('is not known when the answer names no user and does not say sign-in is off', async () => {
    serve(reply(200, {}));
    expect(await whoami()).toEqual({ mode: 'unknown', basis: 'the session answer named no user and did not say sign-in is off' });
  });
});

//  W1233 - the page's address, with assign recorded instead of followed
const at = (pathname: string) => {
  const assign = vi.fn();
  vi.stubGlobal('location', { ...window.location, pathname, assign });
  return assign;
};

describe('a signed-out visitor is sent to the sign-in page (W1233)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    localStorage.clear();
  });

  it('sends an anonymous visitor at / to /login', async () => {
    const assign = at('/');
    serve(reply(401, { detail: 'Not authenticated' }));
    const { sendSignedOutToLogin } = await import('./auth');
    await sendSignedOutToLogin();
    expect(assign).toHaveBeenCalledWith('/login');
  });

  it('leaves an anonymous visitor on /login where they are', async () => {
    const assign = at('/login');
    serve(reply(401, { detail: 'Not authenticated' }));
    const { sendSignedOutToLogin } = await import('./auth');
    await sendSignedOutToLogin();
    expect(assign).not.toHaveBeenCalled();
  });

  it('never redirects with sign-in off', async () => {
    const assign = at('/');
    serve(reply(200, { auth_enabled: false }));
    const { sendSignedOutToLogin } = await import('./auth');
    await sendSignedOutToLogin();
    expect(assign).not.toHaveBeenCalled();
  });

  it('never redirects a session that is not known: a refusal or an unreachable server', async () => {
    const assign = at('/');
    serve(reply(503, { detail: 'the account store could not be read' }));
    const { sendSignedOutToLogin } = await import('./auth');
    await sendSignedOutToLogin();
    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('Failed to fetch'); }));
    await sendSignedOutToLogin();
    expect(assign).not.toHaveBeenCalled();
  });

  it('sends a visitor with no token to /login on a 401 from an /api data call', async () => {
    const assign = at('/');
    serve(reply(401, { detail: 'Not authenticated' }));
    vi.resetModules();
    const { installAuth, getToken } = await import('./auth');
    installAuth();
    expect(getToken()).toBeNull();
    await window.fetch('/api/v1/dashboard/summary');
    expect(assign).toHaveBeenCalledWith('/login');
  });

  it('does not redirect on a 401 from a sign-in call', async () => {
    const assign = at('/');
    serve(reply(401, { detail: 'Incorrect username or password' }));
    vi.resetModules();
    const { installAuth } = await import('./auth');
    installAuth();
    await window.fetch('/api/v1/auth/token');
    expect(assign).not.toHaveBeenCalled();
  });
});
