// W1005 (FU-399 part 35) — the sign-in page, rendered against the auth routes' own answers.
//
// The page says whether sign-in is on, offers the sign-in form, offers self-serve signup only when the Owner turned it
// on, and offers an administrator the form that adds a user. This mounts the real page against the answers its routes
// gave on a fresh store with sign-in off, as shipped (Login.fixture.json, captured by w1005_capture.py: the session,
// the signup setting, a wrong password, a sign-in past the attempt limit, and a signup refused while sign-in is off).
// Signup turned on and an administrator's session cannot be read from that store, so the two answers that need them
// are written here, in the shape the routes answer, and say so. A refusal says the server's reason, and a setting
// that was not read is not shown as off.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Login.fixture.json';
import { Login } from './Login';

type Reply = { status: number; body: unknown; unreachable?: boolean };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: unknown): Reply => ({ status, body: { detail } });

const ME = '/api/v1/auth/me';
const CONFIG = '/api/v1/auth/config';
const TOKEN = 'POST /api/v1/auth/token';
const SIGNUP = 'POST /api/v1/auth/signup';
const REGISTER = 'POST /api/v1/auth/register';
//  written here, not captured: the shipped store has sign-in off, so neither can be read from it
const SIGNUP_ON = ok({ ...(captured.config.body as object), self_serve_signup_enabled: true });
const AN_ADMIN = ok({ user: { username: 'w1005-made-up-admin', role: 'admin' } });

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [ME]: captured.me, [CONFIG]: captured.config, [TOKEN]: captured.bad_signin, [SIGNUP]: captured.signup,
    [REGISTER]: captured.register,
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const key = init?.method === 'POST' ? `POST ${url}` : url;
    const r = (key in over ? over[key] : base[key]) ?? refused(404, `not served in this test: ${key}`);
    if (r.unreachable) throw new TypeError('Failed to fetch');
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

function mount() {
  render(<MemoryRouter><Login /></MemoryRouter>);
}

async function signIn() {
  fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'w1005-made-up-name' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'not-a-real-password' } });
  fireEvent.click(screen.getByRole('button', { name: /Sign in/ }));
}

describe('Login, rendered against the auth routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('sign-in off, as shipped: the page says so, and says signup is off as the server says', async () => {
    serve();
    mount();
    expect(await screen.findByText(/Single-user mode — authentication is currently OFF/)).toBeTruthy();
    //  W1013 - the element is there while the setting is read: wait for what it says once read (it raced on CI)
    await waitFor(() => expect(screen.getByTestId('signup-state').textContent).toMatch(/^Accounts are Owner-curated/));
    expect((captured.config.body as { self_serve_signup_enabled: boolean }).self_serve_signup_enabled).toBe(false);
  });

  it('a refused read of the signup setting is said, not shown as signup being off', async () => {
    serve({ [CONFIG]: refused(503, 'the account store is locked') });
    mount();
    await waitFor(() => expect(screen.getByTestId('signup-state').textContent).toBe(
      'Whether self-serve signup is on could not be read (Failed (HTTP 503): the account store is locked).'));
  });

  it('a wrong password is said as one', async () => {
    serve();
    mount();
    await signIn();
    expect(await screen.findByText('Invalid username or password.')).toBeTruthy();
    expect(captured.bad_signin.status).toBe(401);
  });

  it('a sign-in past the attempt limit says the server\'s reason, not its status alone', async () => {
    serve({ [TOKEN]: captured.too_many });
    mount();
    await signIn();
    const detail = (captured.too_many.body as { detail: string }).detail;
    expect(await screen.findByText(`Failed (HTTP 429): ${detail}`)).toBeTruthy();
  });

  it('a refused signup says the reason the server gave, never "[object Object]"', async () => {
    serve({ [CONFIG]: SIGNUP_ON, [SIGNUP]: refused(422, [{ loc: ['body', 'password'], msg: 'at least 8 characters' }]) });
    mount();
    fireEvent.change(await screen.findByPlaceholderText('Username (≥3 chars)'), { target: { value: 'w1005-made-up' } });
    fireEvent.change(screen.getByPlaceholderText('Password (≥8 chars)'), { target: { value: 'short' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
    expect(await screen.findByText('Failed (HTTP 422): password: at least 8 characters')).toBeTruthy();
  });

  it('a signup the server cannot be reached for is said, not left unanswered', async () => {
    serve({ [CONFIG]: SIGNUP_ON, [SIGNUP]: { status: 0, body: null, unreachable: true } });
    mount();
    fireEvent.change(await screen.findByPlaceholderText('Username (≥3 chars)'), { target: { value: 'w1005-made-up' } });
    fireEvent.change(screen.getByPlaceholderText('Password (≥8 chars)'), { target: { value: 'not-a-real-password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });

  it('a user the server refuses to add is said by its reason, never "[object Object]"', async () => {
    serve({ [ME]: AN_ADMIN, [REGISTER]: refused(409, { message: 'that username is taken' }) });
    mount();
    //  the sign-in form shows until the session is read; the administrator's form replaces it
    expect(await screen.findByText(/Add a user/)).toBeTruthy();
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'w1005-made-up-2' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'not-a-real-password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create user' }));
    expect(await screen.findByText('Failed (HTTP 409): that username is taken')).toBeTruthy();
    expect(captured.register.status).toBe(200);
  });
});
