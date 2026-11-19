// W1048 (FU-399 part 67) — the Native AI page, rendered against its routes' own answers.
//
// On opening, the page reads the fabric's status and thirteen more records of the owned estate; it offers a completion,
// an ensemble, a quick swarm and a workflow tree. This mounts the real page against what each route answered on a fresh
// store with no model installed (NativeAI.fixture.json, captured by w1048_capture.py: every read on opening, one
// completion of the page's own default prompt, and the status route's own 500 when its read fails inside). Rendering
// found two defects, fixed in this round: every action's failure was said in one line under the header, far above its
// button, and kept on screen after a later success; and a failed read of the status dropped the route's reason.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './NativeAI.fixture.json';
import { NativeAI } from './NativeAI';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
type Outcome = 'answered' | 'unreachable' | 'no reason';
const reply = (a: Answer) => ({ ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body });

//  each read as its route answered it; each action's outcomes, in the order it is pressed
function serve(o: { statusFailed?: boolean; complete?: Outcome[]; swarm?: Outcome; tree?: Outcome } = {}) {
  const complete = [...(o.complete ?? ['answered'])];
  const posted: unknown[] = [];
  const outcome = (x: Outcome | undefined, answered: Answer | null) => {
    if (x === 'unreachable') throw new TypeError('Failed to fetch');
    if (x === 'no reason' || !answered) return reply({ status: 500, body: {} });
    return reply(answered);
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string; body?: string }) => {
    if ((init?.method ?? 'GET') === 'GET') {
      const a = o.statusFailed && url === '/api/v1/native-ai/status' ? captured.status_failed : answers[url];
      return a ? reply(a) : reply({ status: 404, body: { detail: `not served here: ${url}` } });
    }
    posted.push([url, JSON.parse(init?.body ?? 'null')]);
    if (url === '/api/v1/native-ai/complete') return outcome(complete.shift(), captured.completed);
    if (url === '/api/v1/native-ai/swarm') return outcome(o.swarm, null);
    if (url === '/api/v1/native-ai/tree') return outcome(o.tree, null);
    return reply({ status: 404, body: { detail: `not served here: ${url}` } });
  }));
  return posted;
}

describe('NativeAI, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('opens on what each read answered: the floor serves, and no failure is said', async () => {
    serve();
    render(<NativeAI />);
    expect(await screen.findByText('Deterministic floor active')).toBeTruthy();
    expect(screen.queryByTestId('native-status-error')).toBeNull();
  });

  it('a failed read of the fabric\'s status says the route\'s own reason', async () => {
    serve({ statusFailed: true });
    render(<NativeAI />);
    await waitFor(() => expect(screen.getByTestId('native-status-error').textContent).toBe(
      `The fabric's status could not be read: Failed (HTTP 500): ${captured.status_failed.body.detail}`));
  });

  it('a completion that reached no server is said beside its button, and a later one that is answered clears it', async () => {
    const posted = serve({ complete: ['unreachable', 'answered'] });
    render(<NativeAI />);
    fireEvent.click(await screen.findByRole('button', { name: /Run completion/ }));
    await waitFor(() => expect(screen.getByTestId('native-complete-error').textContent).toBe('Failed — backend unreachable.'));
    expect(screen.queryByTestId('native-status-error')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: /Run completion/ }));
    await waitFor(() => expect(screen.getByTestId('native-complete-tokens').textContent).toContain('tokens:'));
    expect(screen.queryByTestId('native-complete-error')).toBeNull();
    //  asked what the capture asked: the page's own default prompt and tier
    expect(posted[1]).toEqual(['/api/v1/native-ai/complete', captured.ask]);
  });

  it('the swarm and the tree each say their failure beside their own button', async () => {
    serve({ swarm: 'unreachable', tree: 'no reason' });
    render(<NativeAI />);
    fireEvent.click(await screen.findByRole('button', { name: /Run quick swarm/ }));
    await waitFor(() => expect(screen.getByTestId('native-swarm-error').textContent).toBe('Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: /Plan \+ run workflow tree/ }));
    await waitFor(() => expect(screen.getByTestId('native-tree-error').textContent).toBe('Workflow-tree run failed (HTTP 500).'));
    expect(screen.getByTestId('native-swarm-error').textContent).toBe('Failed — backend unreachable.');
    expect(screen.queryByTestId('native-status-error')).toBeNull();
  });
});
