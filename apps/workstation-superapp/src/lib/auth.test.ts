// W930 — whoami says the session as the server answers it. "Auth off" is the server's own word (GET /api/v1/auth/me
// answers { auth_enabled: false } when sign-in is off); a refusal, an unreachable server, or an answer that says
// neither is 'unknown', with its reason. It used to be 'auth-off' for all of them.
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
