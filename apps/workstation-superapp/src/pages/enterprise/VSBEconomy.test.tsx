// W1047 (FU-399 part 66) — the VSB Economy page, rendered against its routes' own answers.
//
// On opening, the page reads the entity forms, the living entities, the apex's owner payments, its board pack and its
// waterfall, and its panels read the ventures, the transfers, the charity directives and the service contracts. This
// mounts the real page against what each route answered on a fresh store (VSBEconomy.fixture.json, captured by
// w1047_capture.py; nothing was posted), and against the living entities' route's own 500. Rendering found four reads
// whose failure was a fixed sentence, fixed in this round: the living entities' dropped every refusal's reason, and the
// owner payments', the board pack's and the waterfall's said nothing of a call that reached no server.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBEconomy.fixture.json';
import { VSBEconomy } from './VSBEconomy';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;

//  each read as its route answered it; a path given as unreached throws as fetch does when no server answers, and the
//  living entities can be given their route's own 500
function serve(o: { livingFailed?: boolean; unreached?: string[] } = {}) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if ((o.unreached ?? []).some(p => url.startsWith(p))) throw new TypeError('Failed to fetch');
    const a = o.livingFailed && url === '/api/v1/economy/living-vsbs' ? captured.living_failed : answers[url];
    if (!a) return { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
}

function mount() {
  return render(<MemoryRouter><VSBEconomy /></MemoryRouter>);
}

const FAILURES = ['living-error', 'owner-payments-error', 'board-pack-error', 'waterfall-error'];

describe('VSBEconomy, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('opens on what each read answered, and says no failure', async () => {
    serve();
    mount();
    expect(await screen.findByTestId('owner-share-reconciliation')).toBeTruthy();
    expect(await screen.findByTestId('form-in-force')).toBeTruthy();
    for (const id of FAILURES) expect(screen.queryByTestId(id)).toBeNull();
  });

  it('a failed read of the living entities says the route\'s own reason', async () => {
    serve({ livingFailed: true });
    mount();
    await waitFor(() => expect(screen.getByTestId('living-error').textContent).toBe(
      `Could not load the living entities, so nothing is shown rather than stale figures: Failed (HTTP 500): ${captured.living_failed.body.detail}`));
  });

  it('a read that reached no server says so, and what it leaves empty', async () => {
    serve({ unreached: ['/api/v1/economy/owner-payments', '/api/v1/economy/board-pack', '/api/v1/economy/waterfall'] });
    mount();
    await waitFor(() => expect(screen.getByTestId('owner-payments-error').textContent).toBe(
      'Could not load the owner payments, so nothing is shown rather than zero balances: Failed — backend unreachable.'));
    await waitFor(() => expect(screen.getByTestId('board-pack-error').textContent).toBe(
      'Could not load the board pack, so nothing is shown rather than stale figures: Failed — backend unreachable.'));
    await waitFor(() => expect(screen.getByTestId('waterfall-error').textContent).toBe(
      "Could not load the waterfall, so nothing is shown rather than another entity's split: Failed — backend unreachable."));
  });
});
