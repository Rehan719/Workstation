// W1253 — Genesis's idea box keeps what was typed across a sign-in, for that account only, and lets it go once the
// journey ran.
//
// Found on the live site: a session that ran out sent the page to the sign-in page, a whole new page load, and the idea
// typed into the box was lost. This mounts the real page against the answers its routes gave (GenesisJourney.fixture
// .json), types a made-up idea, and opens the page again: as the same account, as another, and after a session that
// ended while the journey was being sent, through the real token layer. Every token is a made-up one, shaped as the
// server's are (its middle part the claims, with the account's id).
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { installAuth } from '../../lib/auth';
import captured from './GenesisJourney.fixture.json';
import { GenesisJourney } from './GenesisJourney';

const IDEA = 'W1253 made up: a tool-lending library for one street, with a reminder when a tool is due back';
const KEPT = 'ws_draft_genesis-idea';
const SAID = 'What you typed here before is back in the box. It is kept in this browser tab until the journey runs. '
  + 'Run it when you are ready, or clear the box to start again.';
const tokenFor = (uid: string) => {
  const claims = btoa(JSON.stringify({ sub: 'w1253-made-up-name', uid, type: 'access' }))
    .replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `w1253-made-up-head.${claims}.w1253-made-up-signature`;
};

//  the routes as they answered; `journey`: the journey route's answer to the launch
function serve(journey: 'answers' | 'session ran out' = 'answers') {
  const fetched = vi.fn(async (url: string, init?: RequestInit) => {
    const reply = (status: number, body: unknown) => ({ ok: status < 400, status, json: async () => body });
    if (url === '/api/v1/genesis/journey' && init?.method === 'POST') {
      return journey === 'answers' ? reply(200, captured.journey)
        : reply(401, { detail: 'Invalid or expired token: Signature has expired.' });
    }
    if (url === '/api/v1/auth/refresh') return reply(401, { detail: 'Invalid or expired token: Signature has expired.' });
    if (url === '/api/v1/economy/entity-types') return reply(200, captured.entity_types);
    if (url === '/api/v1/genesis/price') return reply(200, captured.price);
    return reply(200, {});
  });
  vi.stubGlobal('fetch', fetched);
  return fetched;
}

const box = () => screen.getByPlaceholderText(/Describe the problem to solve/) as HTMLTextAreaElement;
const mount = () => render(<MemoryRouter initialEntries={['/genesis']}><GenesisJourney /></MemoryRouter>);

describe('GenesisJourney\'s idea box keeps what was typed across a sign-in (W1253)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    localStorage.clear();
    sessionStorage.clear();
  });

  it('puts the idea back when the page opens again, says so, and lets it go once the journey ran', async () => {
    serve();
    mount();
    fireEvent.change(box(), { target: { value: IDEA } });
    cleanup();
    mount();
    expect(box().value).toBe(IDEA);
    await waitFor(() => expect(screen.getByTestId('genesis-draft-restored').textContent).toBe(SAID));
    fireEvent.click(screen.getByText('Launch Genesis Journey'));
    await screen.findByTestId(`rail-state-${1}`);   // the rail's ids are built per tile, as the page builds them
    expect(screen.queryByTestId('genesis-draft-restored')).toBeNull();
    expect(sessionStorage.getItem(KEPT)).toBeNull();
    cleanup();
    mount();
    expect(box().value).toBe('');
  }, 15000);   // a whole page, mounted more than once: more than the default five seconds on a loaded runner

  it('never shows one account\'s idea to another: it is dropped unread', async () => {
    serve();
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-a'));
    mount();
    fireEvent.change(box(), { target: { value: IDEA } });
    cleanup();
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-b'));
    mount();
    expect(box().value).toBe('');
    expect(screen.queryByTestId('genesis-draft-restored')).toBeNull();
    expect(sessionStorage.getItem(KEPT)).toBeNull();
  }, 15000);   // a whole page, mounted more than once: more than the default five seconds on a loaded runner

  it('keeps the idea when the session ends as the journey is sent, and puts it back once the same person signs in again', async () => {
    const assign = vi.fn();
    vi.stubGlobal('location', { ...window.location, pathname: '/genesis', search: '', hash: '', assign });
    serve('session ran out');
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-a'));
    localStorage.setItem('workstation_refresh', 'w1253-made-up-refresh');
    installAuth();   // the real token layer, over the routes above (the last case here: it stays installed)
    mount();
    fireEvent.change(box(), { target: { value: IDEA } });
    fireEvent.click(screen.getByText('Launch Genesis Journey'));
    await waitFor(() => expect(assign).toHaveBeenCalledWith('/login?session=ended&next=%2Fgenesis'));
    expect(localStorage.getItem('workstation_token')).toBeNull();
    cleanup();
    localStorage.setItem('workstation_token', tokenFor('w1253-made-up-uid-a'));   // signed in again
    mount();
    expect(box().value).toBe(IDEA);
    await waitFor(() => expect(screen.getByTestId('genesis-draft-restored').textContent).toBe(SAID));
  }, 15000);   // a whole page, mounted more than once: more than the default five seconds on a loaded runner
});
