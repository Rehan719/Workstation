// W994 (FU-399 part 26) — the Self Vision page (Introspection), rendered against the biometrics route's own answer.
//
// The page shows the organism's vitals, read from GET /api/v1/biometrics/status every ten seconds. This mounts the real
// page against the route's answer on a fresh store with one made-up six-minute run recorded
// (Introspection.fixture.json, captured by w994_capture.py: the work budget at 90%, `efficiency` at 95%), and has the
// server refuse a read, first and after a good one. A bar draws the figure its label names, and a refusal says its
// reason.
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Introspection.fixture.json';
import { Introspection } from './Introspection';

type Reply = { status: number; data: unknown };
const ok = (data: unknown): Reply => ({ status: 200, data });
const refused = (status: number, detail: string): Reply => ({ status, data: { detail } });

//  the page reads through axios with validateStatus () => true, so a refusal is an answer, not a throw
function serve(...replies: Reply[]) {
  const q = [...replies];
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/biometrics/status') throw new Error(`not served in this test: ${url}`);
    return q.length > 1 ? q.shift()! : q[0];
  });
}

const bar = (label: string) => {
  const row = screen.getAllByTestId('load-visual').find(e => e.textContent?.startsWith(label));
  return row?.querySelector('span.text-white')?.textContent;
};

describe('Introspection (Self Vision), rendered against the biometrics route\'s own answer', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('the work budget\'s bar draws the work budget, not another figure', async () => {
    serve(ok(captured.status));
    render(<Introspection />);
    await screen.findByText('Self Vision');
    const m = captured.status.metabolic;
    expect(m.energy_ratio).not.toBe(m.efficiency);
    expect(bar('Work budget left')).toBe(`${Math.round(m.energy_ratio * 100)}%`);
  });

  it('a work budget not known draws no figure', async () => {
    serve(ok({ ...captured.status, metabolic: { ...captured.status.metabolic, energy_ratio: null } }));
    render(<Introspection />);
    await screen.findByText('Self Vision');
    expect(bar('Work budget left')).toBe('not measured');
  });

  it('a refused read says the server\'s reason, and that none was received', async () => {
    serve(refused(503, 'the immune sensor is restarting'));
    render(<Introspection />);
    expect((await screen.findByRole('alert')).textContent?.trim()).toBe(
      'The organism is not reporting (HTTP 503: the immune sensor is restarting). No vitals are shown, because none were received.');
  });

  it('a refused read after a good one does not say none was received', async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    serve(ok(captured.status), refused(502, 'the organism did not answer'));
    render(<Introspection />);
    await screen.findByText('Self Vision');
    await vi.advanceTimersByTimeAsync(10_000);
    await waitFor(() => expect(screen.getByRole('alert').textContent?.trim()).toBe(
      'The organism is not reporting (HTTP 502: the organism did not answer). The last reading is not shown, because it may no longer be current.'));
  });
});
