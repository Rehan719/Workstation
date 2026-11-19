// W1049 (FU-399 part 68) — the entity cockpit, rendered against its routes' own answers.
//
// The cockpit lists the entities, opens one and reads its record, plan, ledger, repository, shipped body, roster and
// deliverables. This mounts the real page against what each route answered for an entity established through Genesis
// on a fresh store with no model installed (VSBCockpit.fixture.json, captured by w1049_capture.py), and against the
// list route's own 500 and the shipped body's own 500 (an unreadable manifest). Rendering found two reads whose failure
// was said as something else, fixed in this round: the list's failure was always a backend that could not be reached,
// and a failed read of the shipped body was dropped as an entity never shipped is.
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  each read as its route answered it, keyed as the capture keyed it: the path and the query its params make
function serve(o: { listFailed?: boolean; shipFailed?: boolean } = {}) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = o.listFailed && key === '/api/v1/vsb' ? captured.list_failed
      : o.shipFailed && key === `/api/v1/vsb/${VID}/repo/ship` ? captured.ship_failed
      : answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => { throw axiosRefusal(404, { detail: `not served here: ${url}` }); });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
}

function mount(tab?: string) {
  return render(<MemoryRouter initialEntries={[tab ? `/cockpit?tab=${tab}` : '/cockpit']}><VSBCockpit /></MemoryRouter>);
}

describe('VSBCockpit, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('opens the entity the list holds, on its organisation', async () => {
    serve();
    mount();
    expect((await screen.findAllByText((answers[`/api/v1/vsb/${VID}`].body as { name: string }).name)).some(e => e.tagName === 'H3')).toBe(true);
    expect(screen.queryByTestId('cockpit-list-error')).toBeNull();
  });

  it('a failed read of the list says what it was, and that the list is unknown', async () => {
    serve({ listFailed: true });
    mount();
    await waitFor(() => expect(screen.getByTestId('cockpit-list-error').textContent).toBe(
      `The VSB list could not be read, so this is not “no VSBs”: the list is unknown. Failed (HTTP 500): ${captured.list_failed.body.detail}`));
  });

  it('a shipped body that could not be read is said where its staleness is said', async () => {
    serve({ shipFailed: true });
    mount('transform');
    await waitFor(() => expect(screen.getByTestId('cockpit-ship-error').textContent).toBe(
      `Whether the shipped body is current could not be read: Failed (HTTP 500): ${captured.ship_failed.body.detail}`));
  });

  it('an entity never shipped shows nothing about its shipped body', async () => {
    serve();
    mount('transform');
    //  the tab is open on the entity once its operating state is read; the shipped body's read was issued before it
    expect(await screen.findByTestId('cockpit-cycle-counts')).toBeTruthy();
    expect(answers[`/api/v1/vsb/${VID}/repo/ship`].status).toBe(404);
    expect(screen.queryByTestId('cockpit-ship-error')).toBeNull();
    expect(screen.queryByText(/Shipped body is (STALE|current)/)).toBeNull();
  });
});
