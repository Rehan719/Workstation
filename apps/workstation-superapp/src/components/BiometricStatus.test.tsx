// W1078 (FU-399 part 89) — the shell's vitals, rendered with the real hook against their route's own answers.
//
// The vitals chrome (BiometricStatus, fed by useWorkstationBiometrics) reads one route every few seconds. This mounts
// the real chrome with the real hook against what the route answered on a fresh store (BiometricStatus.fixture.json,
// captured by w1078_capture.py): a live reading of the capturing machine, and the route's own 503 for a host it could
// not read. Every figure is read back from the fixture. Rendering found: the window the CPU figure covers, and the
// load and communication readings' own bases, dropped by the hook, so the chrome said its fallback instead of the
// server's words; a first read that failed titled with the hook's default headroom (100%) and labelled Idle; and a
// refused read kept the last figures as though current, without the route's reason. Fixed here.
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './BiometricStatus.fixture.json';
import { BiometricStatus } from './BiometricStatus';
import { useWorkstationBiometrics } from '../hooks/useWorkstationBiometrics';

type Answer = { status: number; body: any };
const L = captured.live.body;
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

function Vitals({ every }: { every: number }) {
  const b = useWorkstationBiometrics(every);
  return <BiometricStatus biometrics={b} />;
}

//  the route's answers in the order they are read; the last one stays
function serve(answers: (Answer | 'unreachable')[]) {
  const reads = vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/biometrics/status') throw Object.assign(new Error('not served here'), { isAxiosError: true });
    const a = answers.length > 1 ? answers.shift()! : answers[0];
    if (a === 'unreachable') throw unreached();
    return { status: a.status, data: a.body };   // the hook reads every status itself (validateStatus)
  });
  return reads;
}

const cardio = () => screen.getAllByTitle(/^Cardiovascular/)[0].getAttribute('title');
const load = () => screen.getAllByTitle(/^Load state/)[0].getAttribute('title');
const comm = () => screen.getAllByTitle(/^Communication/)[0].getAttribute('title');
const label = () => screen.getAllByText(/^(Work|Comm|Rest|Maint|Idle|Unread)$/)[0].textContent;

describe('BiometricStatus with useWorkstationBiometrics, rendered against the route\'s own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('says a live reading in the route\'s own words: the headroom with its window, and each basis', async () => {
    serve([captured.live]);
    render(<Vitals every={60000} />);
    await waitFor(() => expect(cardio()).toContain(`host CPU headroom ${Math.round(L.cardiovascular.resource_flow)}%`));
    expect(cardio()).toContain(`(CPU sampled over ${L.cardiovascular.host_cpu_window_seconds} s)`);
    expect(load()).toBe(`Load state — ${L.cognition.basis}`);
    expect(comm()).toBe(`Communication — ${L.communication.basis}`);
    expect(label()).toBe(L.workload.platform_busy ? 'Work' : 'Idle');
  });

  it('says a host it could not read on the first reading as not read, with the route\'s reason, and claims no state', async () => {
    serve([captured.refused]);
    render(<Vitals every={60000} />);
    await waitFor(() => expect(cardio()).toBe(`Cardiovascular — host CPU headroom not read: ${captured.refused.body.detail}`));
    expect(cardio()).not.toMatch(/\d+%/);
    expect(label()).toBe('Unread');
  });

  it('says a refused reading after a live one as the last reading, not live now, with the reason', async () => {
    const reads = serve([captured.live, captured.refused]);
    render(<Vitals every={30} />);
    await waitFor(() => expect(reads.mock.calls.length).toBeGreaterThanOrEqual(2));
    await waitFor(() => expect(cardio()).toContain(`— the last reading, not live now: ${captured.refused.body.detail}`));
    expect(cardio()).toContain(`host CPU headroom ${Math.round(L.cardiovascular.resource_flow)}%`);
    expect(load()).toContain('— the last reading, not live now: ');
    expect(label()).toBe('Unread');
  });

  it('says a route it could not reach on the first reading as not read, never as the host\'s figures', async () => {
    serve(['unreachable']);
    render(<Vitals every={60000} />);
    await waitFor(() => expect(cardio()).toBe('Cardiovascular — host CPU headroom not read: Failed — backend unreachable.'));
    expect(comm()).toBe('Communication — not read: Failed — backend unreachable.');
    expect(label()).toBe('Unread');
  });
});
