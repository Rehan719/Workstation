// W1053 (FU-399 part 72) — the cockpit's operating panel, its life cycle and its restore, rendered against the routes'
// own answers.
//
// The panel moves an entity along its life cycle and proposes the restore of a retired one. This mounts the real
// cockpit on its transformation tab against what each route answered for an entity established through Genesis on a
// fresh store with no model installed (VSBCockpit.lifecycle.fixture.json, captured by w1053_capture.py: every read on
// opening, the entity made dormant, the refusal of its retirement and the refusal of a restore for an entity that is
// not retired). Rendering found both actions with no catch, so a call that reached no server did nothing visible, and
// a refused life-cycle change written into the roster's own line; fixed in this round.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.lifecycle.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const ROSTER = '/api/v1/economy/living-vsbs';
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });
type Outcome = 'answered' | 'refused' | 'unreachable';

//  each read as its route answered it (the roster's row re-said as retired when the restore is to be offered); each
//  action's outcomes in the order it is pressed. A refused change is the route's own refusal, as it words one.
function serve(o: { retired?: boolean; lifecycle?: Outcome[]; restore?: Outcome[] } = {}) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    let a = answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (key === ROSTER && o.retired) {
      //  written here: a fresh store has no retired entity, so the captured row is re-said as one
      const body = a.body as { living_vsbs: Record<string, unknown>[] };
      a = { ...a, body: { ...body, living_vsbs: body.living_vsbs.map(v => v.vsb_id === VID ? { ...v, lifecycle_state: 'retired' } : v) } };
    }
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const lifecycle = [...(o.lifecycle ?? [])];
  const restore = [...(o.restore ?? [])];
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    const x = url.endsWith('/lifecycle') ? lifecycle.shift() : url.endsWith('/propose-restore') ? restore.shift() : undefined;
    if (x === 'unreachable') throw unreached();
    if (x === 'answered') return { status: captured.dormant.status, data: captured.dormant.body };
    if (x === 'refused') {
      const r = url.endsWith('/lifecycle') ? captured.retire_refused : captured.restore_refused;
      return { status: r.status, data: r.body };
    }
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit?tab=transform']}><VSBCockpit /></MemoryRouter>);
const basis = (a: { body: unknown }) => String((a.body as { detail: { basis: string } }).detail.basis);

describe('VSBCockpit\'s life cycle and restore, rendered against the routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('a change that reached no server is said beside the toggle; a refusal there too; an answer moves the entity', async () => {
    serve({ lifecycle: ['unreachable', 'refused', 'answered'] });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Make dormant' }));
    await waitFor(() => expect(screen.getByTestId('cockpit-lifecycle-error').textContent).toBe(
      'The life-cycle change was not made: Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: 'Make dormant' }));
    await waitFor(() => expect(screen.getByTestId('cockpit-lifecycle-error').textContent).toBe(
      `The life-cycle change was refused (HTTP 409): ${basis(captured.retire_refused)}`));
    expect(screen.queryByTestId('cockpit-operating-unavailable')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Make dormant' }));
    expect(await screen.findByRole('button', { name: 'Wake' })).toBeTruthy();
    expect(screen.queryByTestId('cockpit-lifecycle-error')).toBeNull();
  });

  it('a restore that reached no server says so; a refused one says the route\'s reason', async () => {
    serve({ retired: true, restore: ['unreachable', 'refused'] });
    mount();
    fireEvent.change(await screen.findByPlaceholderText('Why restore it?'), { target: { value: 'W1053 made up: the scheme has a new organiser' } });
    fireEvent.click(screen.getByTestId('cockpit-restore-propose'));
    await waitFor(() => expect(screen.getByTestId('cockpit-restore-note').textContent).toBe('The restore was not filed: Failed — backend unreachable.'));
    fireEvent.click(screen.getByTestId('cockpit-restore-propose'));
    await waitFor(() => expect(screen.getByTestId('cockpit-restore-note').textContent).toBe(
      `The restore was not filed (HTTP 409): ${basis(captured.restore_refused)}`));
  });
});
