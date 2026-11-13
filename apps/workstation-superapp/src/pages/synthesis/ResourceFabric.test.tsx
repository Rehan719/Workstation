// W917 (FU-609, last part) — a saved composition's lifecycle, rendered: its state, its expiry, the runs the history
// keeps, the beat's record of an expiry, and why a state is not known.
//
// W915 derives the state on each read and refuses a run past a declared expiry; W916 records an expiry once, on the
// beat. Both are claims about what a person SEES on the Resource Fabric page, the kind FU-399 converts. This mounts
// the real page against the API's own answers, captured from the app's routes after three compositions were saved
// (one with an expiry, never run; one run, with no expiry; one run, then expired and recorded by a real beat), and
// reads each card in the DOM. The capture keeps each composition's fields the page reads: its QA record is left out
// and its model keeps only unset_params (scratchpad w917_capture.py, the round's own record of how it was taken).
import { fireEvent, render, screen, within } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ResourceFabric.fixture.json';
import { ResourceFabric } from './ResourceFabric';

type Comp = (typeof captured.compositions.compositions)[number];

function byState(state: string): Comp {
  const c = captured.compositions.compositions.find(x => x.lifecycle.state === state);
  if (!c) throw new Error(`the fixture holds no ${state} composition`);
  return c;
}

// answer the page's reads with the captured answers; `edit` changes the compositions answer for one case, and `put`
// answers an update
function serve(edit?: (comps: Comp[]) => void, put?: { status: number; body: unknown }) {
  const comps = JSON.parse(JSON.stringify(captured.compositions));
  if (edit) edit(comps.compositions);
  const calls: { url: string; init?: RequestInit }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    const reply = (status: number, body: unknown) => ({ ok: status < 400, status, json: async () => body });
    if (init?.method === 'PUT' && put) return reply(put.status, put.body);
    if (url === '/api/v1/resources/compositions') return reply(200, comps);
    if (url.startsWith('/api/v1/resources/compositions/runs')) return reply(200, { runs: [], listing_is_incomplete: false });
    if (url.startsWith('/api/v1/resources?')) return reply(200, captured.resources);
    //  the instrument panel on the same page reads these two on mount
    if (url === '/api/v1/resources/cell/availability') return reply(200, captured.cell_availability);
    if (url === '/api/v1/resources/specifications') return reply(200, captured.specifications);
    return reply(200, {});
  }));
  return { comps: comps.compositions as Comp[], calls };
}

function mount() {
  return render(
    <MemoryRouter>
      <ResourceFabric />
    </MemoryRouter>,
  );
}

describe('ResourceFabric, each saved composition\'s lifecycle, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('every card shows the state the API derived, with its basis on hover', async () => {
    const { comps } = serve();
    mount();
    for (const c of comps) {
      const card = await screen.findByTestId(`comp-lifecycle-${c.id}`);
      expect(within(card).getByTestId('comp-state').textContent).toBe(c.lifecycle.state);
      expect(card.getAttribute('title')).toBe(c.lifecycle.basis);
    }
    expect(new Set(comps.map(c => c.lifecycle.state))).toEqual(new Set(['provisioned', 'operating', 'expired']));
  });

  it('an expired composition says when it expired and who recorded it, and it cannot be run', async () => {
    serve();
    const c = byState('expired');
    expect(c.lifecycle.expiry_recorded).not.toBeNull();
    mount();
    const card = await screen.findByTestId(`comp-lifecycle-${c.id}`);
    expect(within(card).getByTestId('comp-expiry').textContent).toBe(`expired at ${c.lifecycle.expires_at}`);
    const rec = within(card).getByTestId('comp-expiry-recorded').textContent ?? '';
    expect(rec).toContain(c.lifecycle.expiry_recorded!.recorded_by);
    expect(rec).toContain(c.lifecycle.expiry_recorded!.recorded_at);
    expect((screen.getByTestId(`comp-run-${c.id}`) as HTMLButtonElement).disabled).toBe(true);
  });

  it('a runnable composition says when it expires and how many runs are kept, and it can be run', async () => {
    serve();
    const fresh = byState('provisioned');
    const used = byState('operating');
    mount();
    const a = await screen.findByTestId(`comp-lifecycle-${fresh.id}`);
    expect(within(a).getByTestId('comp-expiry').textContent).toBe(`expires at ${fresh.lifecycle.expires_at}`);
    expect(within(a).getByTestId('comp-runs-kept').textContent).toBe('0 runs kept');
    expect(within(a).queryByTestId('comp-expiry-recorded')).toBeNull();
    const b = screen.getByTestId(`comp-lifecycle-${used.id}`);
    expect(within(b).queryByTestId('comp-expiry')).toBeNull();
    expect(within(b).getByTestId('comp-runs-kept').textContent).toBe(`1 run kept, last ${used.lifecycle.last_run_at}`);
    for (const c of [fresh, used]) {
      expect((screen.getByTestId(`comp-run-${c.id}`) as HTMLButtonElement).disabled).toBe(false);
    }
  });

  it('a state the stores cannot settle says why, and claims no count', async () => {
    const why = 'the run history could not be read (the store is not valid JSON)';
    const used = byState('operating');
    serve(comps => {
      const c = comps.find(x => x.id === used.id)!;
      Object.assign(c.lifecycle, { state: 'not known', runs_kept: null, last_run_at: null, not_known_because: why });
    });
    mount();
    const card = await screen.findByTestId(`comp-lifecycle-${used.id}`);
    expect(within(card).getByTestId('comp-state').textContent).toBe('not known');
    expect(within(card).getByTestId('comp-not-known').textContent).toBe(why);
    expect(within(card).queryByTestId('comp-runs-kept')).toBeNull();
  });

  it('a refused renewal shows the API\'s own sentence, and the time typed is kept', async () => {
    const said = "expires_at '2020-01-01T00:00:00.000Z' has already passed, so the composition could never run. "
      + 'Give a later time, or leave expires_at out for a composition that does not expire. Nothing was saved.';
    const fresh = byState('provisioned');
    const { calls } = serve(undefined, { status: 422, body: { detail: said } });
    mount();
    const row = await screen.findByTestId(`comp-renew-${fresh.id}`);
    const input = within(row).getByLabelText(`New expiry for ${fresh.name}`) as HTMLInputElement;
    fireEvent.change(input, { target: { value: '2020-01-01T00:00' } });
    fireEvent.click(within(row).getByText('Renew'));
    expect(await screen.findByText(said)).toBeTruthy();
    expect(input.value).toBe('2020-01-01T00:00');
    const sent = calls.find(c => c.init?.method === 'PUT');
    expect(sent?.url).toBe(`/api/v1/resources/compositions/${fresh.id}`);
    expect(JSON.parse(String(sent?.init?.body)).expires_at).toBe(new Date('2020-01-01T00:00').toISOString());
  });
});
