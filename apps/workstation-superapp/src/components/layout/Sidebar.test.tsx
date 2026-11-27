// W1237 - the sidebar's profile block follows a sign-in and a sign-out made in the page, without a remount.
//
// Found on the live site with sign-in on: after signing in, the sidebar's bottom-left still offered "Sign in", and the
// Owner had to click it. The sidebar read the session once on mount, and the sign-in form signs in and goes to the
// home page with no reload, so the sidebar kept the signed-out answer. It now reads the session again on every
// 'ws:identity', which setToken and clearToken dispatch, and on every 'storage' event for the token, which is how a
// sign-in or a sign-out in another tab reaches this one. This mounts the real sidebar against what the session route
// answered on a fresh store with sign-in on (Sidebar.fixture.json, captured by w1237_capture.py: the session with no
// token, and the session of a made-up account signed in). The route is answered by the token stored when it is
// asked, as the server answers by the token the request carries.
import { act, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Sidebar.fixture.json';
import { Sidebar } from './Sidebar';
import { clearToken, setToken } from '../../lib/auth';

type Answer = { status: number; body: unknown };
const ME = '/api/v1/auth/me';
const TOKEN = 'w1237-made-up-token';
const NAME = captured.me_signed_in.body.username;
const SIGN_IN = 'Sign in →';
const SIGN_OUT = 'Sign out';

//  the session route answers by the token stored when it is asked; an answer can be held back until the test lets it go
function serve(held: Promise<Answer>[] = []) {
  const asked: (string | null)[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== ME) return { ok: false, status: 404, json: async () => ({ detail: `not served in this test: ${url}` }) };
    const token = localStorage.getItem('workstation_token');
    asked.push(token);
    const a: Answer = held.length ? await held.shift()! : token === TOKEN ? captured.me_signed_in : captured.me_signed_out;
    return { ok: a.status < 400, status: a.status, json: async () => a.body };
  }));
  return asked;
}

function held(a: Answer) {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const mount = () => render(<MemoryRouter><Sidebar activeTab="dashboard" setActiveTab={() => undefined} /></MemoryRouter>);

describe('Sidebar, its profile block against the session route\'s own answers (W1237)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    localStorage.clear();
  });

  it('offers "Sign in" signed out, the name and "Sign out" once signed in, and "Sign in" again once signed out, with no remount', async () => {
    const asked = serve();
    const { container } = mount();
    const aside = container.querySelector('aside');
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    expect(screen.queryByRole('button', { name: SIGN_OUT })).toBeNull();

    act(() => setToken(TOKEN));
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument());
    expect(screen.getByText(NAME)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: SIGN_IN })).toBeNull();

    act(() => clearToken());
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    expect(screen.queryByRole('button', { name: SIGN_OUT })).toBeNull();
    expect(screen.queryByText(NAME)).toBeNull();

    expect(container.querySelector('aside')).toBe(aside);
    //  the read after the sign-in asked with the token stored, not before it was stored
    expect(asked).toEqual([null, TOKEN, null]);
  });

  it('says the session is being read while it is read again', async () => {
    const later = held(captured.me_signed_in);
    serve([Promise.resolve(captured.me_signed_out), later.reply]);
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    act(() => setToken(TOKEN));
    await waitFor(() => expect(screen.getByTestId('session-not-known').textContent).toBe('Reading the session…'));
    expect(screen.queryByRole('button', { name: SIGN_IN })).toBeNull();
    await act(async () => later.letGo());
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument());
  });

  it('never lets an earlier answer replace a later one', async () => {
    const first = held(captured.me_signed_out);
    serve([first.reply, Promise.resolve(captured.me_signed_in)]);
    mount();
    act(() => setToken(TOKEN));
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument());
    await act(async () => first.letGo());
    expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: SIGN_IN })).toBeNull();
  });

  it('reads the session again when another tab signs in or signs out, and not when another key changes', async () => {
    const asked = serve();
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    //  another tab stores the token: this tab hears a 'storage' event, never 'ws:identity'
    localStorage.setItem('workstation_token', TOKEN);
    act(() => { window.dispatchEvent(new StorageEvent('storage', { key: 'workstation_token', newValue: TOKEN })); });
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument());
    expect(screen.getByText(NAME)).toBeInTheDocument();
    //  another tab's preferences changing is no sign-in or sign-out
    await act(async () => { window.dispatchEvent(new StorageEvent('storage', { key: 'ws_user_prefs_v1', newValue: null })); });
    expect(screen.getByRole('button', { name: SIGN_OUT })).toBeInTheDocument();
    //  another tab clears the whole store: the event names no key
    localStorage.clear();
    act(() => { window.dispatchEvent(new StorageEvent('storage', { key: null })); });
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    expect(screen.queryByText(NAME)).toBeNull();
    expect(asked).toEqual([null, TOKEN, null]);
  });

  it('stops listening once unmounted', async () => {
    const asked = serve();
    const removed = vi.spyOn(window, 'removeEventListener');
    const { unmount } = mount();
    await waitFor(() => expect(screen.getByRole('button', { name: SIGN_IN })).toBeInTheDocument());
    unmount();
    expect(removed.mock.calls.filter(c => c[0] === 'ws:identity')).toHaveLength(1);
    expect(removed.mock.calls.filter(c => c[0] === 'storage')).toHaveLength(1);
    await act(async () => setToken(TOKEN));
    await act(async () => { window.dispatchEvent(new StorageEvent('storage', { key: 'workstation_token', newValue: TOKEN })); });
    expect(asked).toEqual([null]);
  });
});
