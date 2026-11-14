// W1007 (FU-399 part 37) — the cognition page, rendered against the cognition routes' own answers.
//
// The page shows how the cognitive tiers are wired, the knowledge sources and the engines, runs the cognitive cascade
// over a problem, and reads the alignment of the platform's pillars as a dry run. This mounts the real page against the
// answers its routes gave on a fresh store with no model installed (CognitionIntegration.fixture.json, captured by
// w1007_capture.py), and has the server refuse each action. A refused action is said as that action's, where it was
// run, and a failure is taken off once the same action succeeds.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './CognitionIntegration.fixture.json';
import { CognitionIntegration } from './CognitionIntegration';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const SOLVE = 'POST /api/v1/intelligence/solve';
const ALIGN = 'POST /api/v1/cognition/align';

//  each route answers its captured reply; a list is answered in order, its last reply kept
function serve(over: Record<string, Reply | Reply[]> = {}) {
  const base: Record<string, Reply> = {
    '/api/v1/cognition/wiring': ok(captured.wiring), '/api/v1/cognition/knowledge': ok(captured.knowledge),
    '/api/v1/intelligence/cognitive-engines': ok(captured.engines), '/api/v1/heartbeat/status': ok(captured.heartbeat),
    [SOLVE]: ok(captured.solved), [ALIGN]: ok(captured.aligned),
  };
  const queues: Record<string, Reply[]> = Object.fromEntries(
    Object.entries(over).map(([u, r]) => [u, Array.isArray(r) ? [...r] : [r]]));
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const key = init?.method === 'POST' ? `POST ${url}` : url;
    const q = queues[key];
    const r = (q ? (q.length > 1 ? q.shift()! : q[0]) : base[key]) ?? refused(404, `not served in this test: ${key}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

function mount() {
  render(<MemoryRouter><CognitionIntegration /></MemoryRouter>);
}

const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);

function runCascade() {
  fireEvent.change(screen.getByPlaceholderText('Describe a problem to analyse through the cognitive engines…'),
    { target: { value: 'W1007 made up: how should a small bakery cooperative schedule its morning deliveries?' } });
  fireEvent.click(screen.getByRole('button', { name: /Run cascade/ }));
}

describe('CognitionIntegration, rendered against the cognition routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('every read answered: the wiring is the server\'s count, and nothing is said to have failed', async () => {
    serve();
    mount();
    const w = captured.wiring as { routes_mounted?: number; connected: number; total: number };
    expect((await screen.findByTestId('wiring-count')).textContent).toBe(
      `${w.routes_mounted ?? w.connected}/${w.total} tiers have a route mounted`);
    expect(failures()).toEqual([]);
  });

  it('a cascade the server refuses is said as the cascade\'s, where it is run', async () => {
    serve({ [SOLVE]: refused(503, 'the cascade is held while the engines are rebuilt') });
    mount();
    await screen.findByTestId('wiring-count');
    runCascade();
    expect((await screen.findByTestId('solve-error')).textContent).toBe(
      'The cascade did not run: Failed (HTTP 503): the cascade is held while the engines are rebuilt');
    expect(screen.queryByTestId('align-error')).toBeNull();
  });

  it('an alignment the server refuses is said as the alignment\'s', async () => {
    serve({ [ALIGN]: refused(502, 'the pillar register did not answer') });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: /Route Gaps/ }));
    expect((await screen.findByTestId('align-error')).textContent).toBe(
      'The alignment could not be read: Failed (HTTP 502): the pillar register did not answer');
    expect(screen.queryByTestId('solve-error')).toBeNull();
  });

  it('a failure is taken off once the same action succeeds', async () => {
    serve({ [ALIGN]: [refused(502, 'the pillar register did not answer'), ok(captured.aligned)] });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: /Route Gaps/ }));
    await screen.findByTestId('align-error');
    fireEvent.click(screen.getByRole('button', { name: /Route Gaps/ }));
    await waitFor(() => expect(screen.queryByTestId('align-error')).toBeNull());
  });

  it('a refused read of the engines is said by what was being read', async () => {
    serve({ '/api/v1/intelligence/cognitive-engines': refused(503, 'the engine registry is locked') });
    mount();
    await waitFor(() => expect(failures()).toEqual([
      'Could not read the cognitive engines — Failed (HTTP 503): the engine registry is locked']));
  });
});
