// W1045 (FU-399 part 65) — the Solutions Platform, rendered against its routes' own answers.
//
// The page asks the query route for a specification from a brief, records a deployment plan, and reads two routes for
// readiness. This mounts the real page against what the routes answered on a fresh store with no model installed
// (SolutionsPlatform.fixture.json, captured by w1045_capture.py: the specification the native engine composed for a
// made-up brief, the fabric's status and the constitutional ledger's verification). Rendering found three defects,
// fixed in this round: the specification was shown as generated with nothing saying what composed it; a failed request
// for one named a layer that had not answered when no reason came; and the Build phase's button said it built
// infrastructure for an action that records a plan.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './SolutionsPlatform.fixture.json';
import { SolutionsPlatform } from './SolutionsPlatform';

const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  the specification as the route answered it (or a failure), and the two readiness reads as they were answered
function serve(spec: 'answered' | 'unreachable' | 'no reason' = 'answered') {
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/ai/query') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (spec === 'unreachable') throw unreached();
    if (spec === 'no reason') throw axiosRefusal(500, {});
    return { status: captured.answered.status, data: captured.answered.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const a = url === '/api/v1/native-ai/status' ? captured.status : url === '/api/v1/gaas/ueg/verify' ? captured.verify : null;
    if (!a) return { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served: ${url}` }) };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
  return post;
}

//  the page is given the captured brief: its name, one domain, the description and one objective
function brief() {
  const b = captured.brief;
  render(<SolutionsPlatform />);
  fireEvent.change(screen.getByLabelText('Solution Name'), { target: { value: b.solution_name } });
  fireEvent.click(screen.getByRole('button', { name: b.domains[0] }));
  fireEvent.change(screen.getByLabelText('Solution Description'), { target: { value: b.description } });
  fireEvent.change(screen.getByLabelText('Add objective'), { target: { value: b.objectives[0] } });
  fireEvent.click(screen.getByRole('button', { name: 'Add' }));
  fireEvent.click(screen.getByRole('button', { name: /Generate Specification/ }));
}

describe('SolutionsPlatform, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('asks what the brief says; the specification says what composed it; the plan and the readiness say what they are', async () => {
    const post = serve();
    brief();
    await waitFor(() => expect(screen.getByTestId('spec-provenance').textContent).toBe('structured floor — not model analysis'));
    expect(post).toHaveBeenCalledWith('/api/v1/ai/query', captured.ask);
    expect(captured.answered.body.served_by).toBe('native');
    expect(screen.getByText(/^_\[Workstation native structured engine/).textContent).toBe(captured.answered.body.answer);
    //  each phase is shown once the one before it has finished leaving, so its controls are waited for
    fireEvent.click(screen.getByRole('button', { name: /Proceed to Build/ }));
    //  the button is named for what it does: it records a plan and provisions nothing
    fireEvent.click(await screen.findByRole('button', { name: /^Record the deployment plan$/ }));
    expect(await screen.findByText('PLAN ONLY — nothing provisioned')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /Proceed to Launch/ }));
    fireEvent.change(await screen.findByLabelText('Mission Name'), { target: { value: 'W1045 made up: TIMETABLE-001' } });
    fireEvent.click(screen.getByRole('button', { name: /Run readiness check/ }));
    expect(await screen.findByText('Native AI fabric: answering, but NO owned model is serving — mode deterministic_floor. '
      + 'Output would be composed by the deterministic floor, not generated.')).toBeTruthy();
    expect(await screen.findByText(`Constitutional ledger: chain VALID (${captured.verify.body.events} events), tail anchor matched.`)).toBeTruthy();
  });

  it('a request that reached no server says so, and the sentence ends once', async () => {
    serve('unreachable');
    brief();
    await waitFor(() => expect(screen.getByTestId('spec-error').textContent).toBe(
      'Specification generation failed: Failed — backend unreachable. Nothing was generated.'));
    expect(screen.queryByTestId('spec-provenance')).toBeNull();
  });

  it('a server that answered without a reason is said as one, never as a layer that did not respond', async () => {
    serve('no reason');
    brief();
    await waitFor(() => expect(screen.getByTestId('spec-error').textContent).toBe(
      'Specification generation failed: Failed (HTTP 500): no reason given. Nothing was generated.'));
  });
});
