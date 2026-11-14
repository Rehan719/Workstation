// W1051 (FU-399 part 70) — the cockpit's actions, rendered on their tabs against its routes' own answers.
//
// The cockpit opens an entity on the reads W1049 captured (VSBCockpit.fixture.json: an entity established through
// Genesis on a fresh store with no model installed). On its plan tab the Chief delivers an objective, on its economy tab
// a cycle runs, and on its transformation tab the transformation runs and a build is configured. Each action here
// fails as a call can fail, unreached or answered with no reason. Rendering found every one of those failures said in
// one line above the entity picker, away from the tab the action is on, and three of the four never cleared it. Each
// is said beside its own button now, fixed in this round.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
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
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });
type Outcome = 'unreachable' | 'no reason' | 'no tree';

//  each read as its route answered it; each action's outcomes in the order it is pressed
function serve(acts: Record<string, Outcome[]>) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    const route = Object.keys(acts).find(r => url.startsWith(r));
    const x = route ? acts[route].shift() : undefined;
    if (x === 'unreachable') throw unreached();
    if (x === 'no tree') return { status: 200, data: { tree: null } };
    throw axiosRefusal(x === 'no reason' ? 500 : 404, x === 'no reason' ? {} : { detail: `not served here: ${url}` });
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
}

const mount = (tab: string) => render(<MemoryRouter initialEntries={[`/cockpit?tab=${tab}`]}><VSBCockpit /></MemoryRouter>);

describe('VSBCockpit\'s actions, each said beside its own button', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('the transformation and the build configuration each say their failure beside their button', async () => {
    serve({ '/api/v1/transformation/orchestrate': ['unreachable'], '/api/v1/bto/configure': ['no reason'] });
    mount('transform');
    fireEvent.click(await screen.findByRole('button', { name: /Run transformation/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-transformation-error').textContent).toBe(
      'The transformation failed: Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: /^Configure build/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-configuration-error').textContent).toBe(
      'The configuration failed: Failed (HTTP 500): no reason given'));
    expect(screen.getByTestId('cockpit-transformation-error').textContent).toBe('The transformation failed: Failed — backend unreachable.');
  });

  it('a cycle that was answered with no reason says so beside its button', async () => {
    serve({ '/api/v1/economy/cycle': ['no reason'] });
    mount('economy');
    fireEvent.click(await screen.findByRole('button', { name: /Run economic cycle/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-cycle-error').textContent).toBe(
      'The cycle failed (HTTP 500): no reason given.'));
  });

  it('an objective the Chief could not deliver says so under that objective, and again when pressed again', async () => {
    serve({ [`/api/v1/business-plan/objective/`]: ['no reason', 'no tree'] });
    mount('plan');
    const plan = answers[`/api/v1/business-plan?scope=${VID}`].body as { objectives: { id: string }[] };
    expect(plan.objectives.length).toBeGreaterThan(1);
    const delivers = await screen.findAllByRole('button', { name: /Chief: deliver via tree/ });
    fireEvent.click(delivers[0]);
    await waitFor(() => expect(screen.getByTestId('cockpit-orchestration-error').textContent).toBe(
      'Orchestration failed: Failed (HTTP 500): no reason given'));
    fireEvent.click(delivers[0]);
    await waitFor(() => expect(screen.getByTestId('cockpit-orchestration-error').textContent).toBe(
      'Orchestration ran but returned no delivery tree.'));
    expect(screen.getAllByTestId('cockpit-orchestration-error')).toHaveLength(1);
  });
});
