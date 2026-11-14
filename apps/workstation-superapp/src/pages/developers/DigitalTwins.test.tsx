// W993 (FU-399 part 25) — the Digital Twins page, rendered against the twin routes' own answers.
//
// The page composes a twin model of a system, lists the models, opens one with its specification, its scenarios and
// what composed it, and asks it a scenario or an optimisation. This mounts the real page against the answers its
// routes gave on a fresh store (DigitalTwins.fixture.json, captured by w993_capture.py: no model, then one made-up
// system with one scenario), and has the server refuse each read and each action. A refusal is shown, with the
// server's status and reason, never written where nothing reads it.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DigitalTwins.fixture.json';
import { DigitalTwins } from './DigitalTwins';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const id = captured.composed.model_id;
const URL = {
  models: '/api/v1/twin/models', model: `/api/v1/twin/models/${id}`, compose: '/api/v1/twin/model',
  simulate: '/api/v1/twin/simulate', optimise: '/api/v1/twin/optimise',
};

//  each route answers its captured reply; a list is answered in order, its last reply kept
function serve(over: Record<string, Reply | Reply[]> = {}) {
  const base: Record<string, Reply> = {
    [URL.models]: ok(captured.models), [URL.model]: ok(captured.model), [URL.compose]: ok(captured.composed),
    [URL.simulate]: ok(captured.scenario),
  };
  const queues: Record<string, Reply[]> = Object.fromEntries(
    Object.entries(over).map(([u, r]) => [u, Array.isArray(r) ? [...r] : [r]]));
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const q = queues[url];
    const r = (q ? (q.length > 1 ? q.shift()! : q[0]) : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const name = captured.composed.system_name;
async function openTheModel() {
  fireEvent.click(await screen.findByText(name, { selector: 'p.truncate' }));
}

describe('DigitalTwins, rendered against the twin routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a model opens with the scenarios the route lists', async () => {
    serve({ [URL.model]: ok(captured.model_after) });
    render(<DigitalTwins />);
    await openTheModel();
    expect(await screen.findAllByTestId('twin-scenario-row')).toHaveLength(captured.model_after.simulations.length);
    expect(screen.queryByTestId('twin-load-error')).toBeNull();
  });

  it('a refused read of a model is shown, with the server\'s reason', async () => {
    serve({ [URL.model]: captured.missing });
    render(<DigitalTwins />);
    await openTheModel();
    expect((await screen.findByTestId('twin-load-error')).textContent?.trim()).toBe(
      `This model could not be read: Failed (HTTP ${captured.missing.status}): ${captured.missing.body.detail} — showing the summary row only.`);
  });

  it('a refused compose says the server\'s status and reason', async () => {
    serve({ [URL.compose]: refused(422, 'system_description: the description is empty') });
    render(<DigitalTwins />);
    fireEvent.change(await screen.findByPlaceholderText('System name'), { target: { value: 'A system' } });
    fireEvent.change(screen.getByPlaceholderText('What the system is and does'), { target: { value: 'It does a thing.' } });
    fireEvent.click(screen.getByRole('button', { name: /Compose the model text/ }));
    expect((await screen.findByTestId('twin-action-error')).textContent).toBe(
      'The model was not composed: Failed (HTTP 422): system_description: the description is empty');
  });

  it('a refused scenario says the server\'s status and reason', async () => {
    serve({ [URL.simulate]: refused(404, `Model ${id} not found.`) });
    render(<DigitalTwins />);
    await openTheModel();
    fireEvent.change(await screen.findByPlaceholderText('Scenario name'), { target: { value: 'Twice' } });
    fireEvent.change(screen.getByPlaceholderText('What changes in this scenario'), { target: { value: 'Doubles.' } });
    fireEvent.click(screen.getByRole('button', { name: /Compose the scenario text/ }));
    expect((await screen.findByTestId('twin-action-error')).textContent).toBe(
      `The scenario was not run: Failed (HTTP 404): Model ${id} not found.`);
  });

  it('a scenario that ran, and a model that could not then be read again, is said', async () => {
    serve({ [URL.model]: [ok(captured.model), refused(503, 'the twin store is locked')] });
    render(<DigitalTwins />);
    await openTheModel();
    await waitFor(() => expect(screen.queryByTestId('twin-load-error')).toBeNull());
    fireEvent.change(await screen.findByPlaceholderText('Scenario name'), { target: { value: 'Twice' } });
    fireEvent.change(screen.getByPlaceholderText('What changes in this scenario'), { target: { value: 'Doubles.' } });
    fireEvent.click(screen.getByRole('button', { name: /Compose the scenario text/ }));
    expect((await screen.findByTestId('twin-load-error')).textContent?.trim()).toBe(
      'This model could not be read: Failed (HTTP 503): the twin store is locked — the list of scenarios is the one read before this one ran.');
    expect(screen.queryByTestId('twin-action-error')).toBeNull();
  });
});
