// W1253 — an enterprise's Converse box keeps what was being written across a sign-in, for that account only, and lets
// it go once a reply came.
//
// Found on the live site: a session that ran out sent the page to the sign-in page, a whole new page load, and the
// message being written in the cockpit's Converse box was lost. This mounts the real cockpit on the tab against what
// each route answered (VSBCockpit.chat.fixture.json, as VSBCockpit.chat.test.tsx reads it), writes a made-up message,
// and opens the cockpit again: as the same account and as another. Every token is a made-up one, shaped as the
// server's are (its middle part the claims, with the account's id).
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.chat.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const MSG = 'W1253 made up: what would it take to open on Saturdays?';
const KEPT = `ws_draft_cockpit-converse:${captured.vsb_id}`;
const SAID = 'What you were writing to this enterprise before is back in the box. It is kept in this browser tab until a '
  + 'reply comes. Press Send when you are ready.';
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const tokenFor = (uid: string) => {
  const claims = btoa(JSON.stringify({ sub: 'w1253-made-up-name', uid, type: 'access' }))
    .replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `w1253-made-up-head.${claims}.w1253-made-up-signature`;
};

//  each read as its route answered it; the chat's outcomes in the order messages are sent
function serve(chat: ('answered' | 'refused')[]) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/avatar/chat') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (chat.shift() === 'refused') throw axiosRefusal(captured.refused.status, captured.refused.body);
    return { status: captured.answered.status, data: captured.answered.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return post;
}

const mount = () => render(<MemoryRouter initialEntries={['/vsb-cockpit?tab=chat']}><VSBCockpit /></MemoryRouter>);
const input = async () => (await screen.findByPlaceholderText('Ask about this enterprise…')) as HTMLInputElement;

describe('VSBCockpit\'s Converse box keeps what was being written across a sign-in (W1253)', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    localStorage.clear();
    sessionStorage.clear();
  });

  it('puts the message back when the enterprise opens again, says so, and lets it go once a reply came', async () => {
    const post = serve(['answered']);
    mount();
    fireEvent.change(await input(), { target: { value: MSG } });
    cleanup();
    mount();
    await waitFor(() => expect(screen.getByTestId('cockpit-draft-restored').textContent).toBe(SAID));
    expect((await input()).value).toBe(MSG);
    fireEvent.click(screen.getByRole('button', { name: /^Send$/ }));
    expect(await screen.findByText('structured floor — not model analysis')).toBeTruthy();
    expect(post).toHaveBeenCalledWith('/api/v1/avatar/chat', { ...captured.ask, message: MSG });
    expect(sessionStorage.getItem(KEPT)).toBeNull();
    expect(screen.queryByTestId('cockpit-draft-restored')).toBeNull();
  }, 15000);   // a whole page, mounted more than once: more than the default five seconds on a loaded runner

  it('keeps a message no reply came for, and never shows it to another account: it is dropped unread', async () => {
    serve(['refused']);
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-a'));
    mount();
    fireEvent.change(await input(), { target: { value: MSG } });
    fireEvent.click(screen.getByRole('button', { name: /^Send$/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-chat-error').textContent).toBe('No reply came: Failed (HTTP 422): message: Field required'));
    expect(JSON.parse(String(sessionStorage.getItem(KEPT))).text).toBe(MSG);
    cleanup();
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-b'));
    mount();
    expect((await input()).value).toBe('');
    expect(screen.queryByTestId('cockpit-draft-restored')).toBeNull();
    expect(sessionStorage.getItem(KEPT)).toBeNull();
  }, 15000);   // a whole page, mounted more than once: more than the default five seconds on a loaded runner
});
