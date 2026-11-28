// W1253 — the sign-in page after a session ended: it says so in plain words, keeps the refresh token the sign-in hands
// out, and sends the person back to the page they were on, never to an address on another site.
//
// The page is mounted on the address the token layer sends a person to when their session ends
// (/login?session=ended&next=...). The session and the signup setting are the answers Login.fixture.json captured; the
// sign-in's answer is written here in the shape POST /api/v1/auth/token answers (TokenResponse: access_token,
// refresh_token, token_type, expires_in), because the captured store has sign-in off. Every token is a made-up string.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Login.fixture.json';
import { Login } from './Login';

const SIGNED_IN = { access_token: 'w1253-made-up-access', refresh_token: 'w1253-made-up-refresh', token_type: 'bearer', expires_in: 3600 };
const ENDED = 'Your session ended. Sign in again to carry on.';
const BACK = 'Once you are signed in you will go back to the page you were on. What you were typing in the Genesis idea box '
  + 'or in an enterprise\'s Converse box is still there.';

function serve() {
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const r = init?.method === 'POST' && url === '/api/v1/auth/token' ? { status: 200, body: SIGNED_IN }
      : url === '/api/v1/auth/me' ? captured.me
      : url === '/api/v1/auth/config' ? captured.config
      : { status: 404, body: { detail: `not served in this test: ${url}` } };
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

//  where the sign-in sent the person, as the router holds it. It is drawn beside the page, not as a route of its own:
//  App.tsx is the one file that defines routes (test_w499 counts them through readme_figures.route_files)
const Where: React.FC = () => {
  const l = useLocation();
  return <p>{`W1253 stand-in for the page at ${l.pathname}${l.search}`}</p>;
};

function mount(address: string) {
  render(
    <MemoryRouter initialEntries={[address]}>
      <Login />
      <Where />
    </MemoryRouter>,
  );
}

function signIn() {
  fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'w1253-made-up-name' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'not-a-real-password' } });
  fireEvent.click(screen.getByRole('button', { name: /Sign in/ }));
}

describe('the sign-in page after a session ended (W1253)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    localStorage.clear();
  });

  it('says the session ended, keeps both tokens the sign-in hands out, and sends the person back to their page', async () => {
    serve();
    mount('/login?session=ended&next=%2Fgenesis%3Fdomain%3Dscience');
    await waitFor(() => expect(screen.getByTestId('session-ended').textContent).toContain(ENDED));
    expect(screen.getByTestId('session-ended-back').textContent).toBe(BACK);
    signIn();
    expect(await screen.findByText('W1253 stand-in for the page at /genesis?domain=science')).toBeTruthy();
    expect([localStorage.getItem('workstation_token'), localStorage.getItem('workstation_refresh')])
      .toEqual([SIGNED_IN.access_token, SIGNED_IN.refresh_token]);
  });

  it('never follows an address on another site: the sign-in lands on the home page, and nothing says a session ended', async () => {
    serve();
    mount('/login?next=%2F%2Felsewhere%2Fa-path');
    await waitFor(() => expect(screen.getByTestId('signup-state').textContent).toContain('Owner-curated'));
    expect(screen.queryByTestId('session-ended')).toBeNull();
    signIn();
    expect(await screen.findByText('W1253 stand-in for the page at /')).toBeTruthy();
  });

  it('says a session ended with no page to go back to only as that', async () => {
    serve();
    mount('/login?session=ended');
    await waitFor(() => expect(screen.getByTestId('session-ended').textContent).toBe(ENDED));
    expect(screen.queryByTestId('session-ended-back')).toBeNull();
  });
});
