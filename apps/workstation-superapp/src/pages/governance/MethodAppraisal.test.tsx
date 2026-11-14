// W1003 (FU-399 part 33) — the appraisal page, rendered against the method routes' own answers.
//
// The page shows the method cell's readings over a scope (the whole plan, a phase or an item): what the readings
// recommend, what becomes of an appraisal, and each reading with how it was read. A person may send one
// recommendation to Change Control. This mounts the real page against the answers its routes gave on a fresh store
// (MethodAppraisal.fixture.json, captured by w1003_capture.py: the whole plan, one phase, a recommendation sent, and
// one the readings do not make), and has the server refuse an appraisal. Every reading says how it was read, and a
// refused send is said by its reason, not as its JSON.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './MethodAppraisal.fixture.json';
import { MethodAppraisal } from './MethodAppraisal';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: unknown): Reply => ({ status, body: { detail } });

const WHOLE = '/api/v1/method/appraise';
const PHASE = '/api/v1/method/appraise?scope=P3';
const SEND = 'POST /api/v1/method/appraise/recommend';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = { [WHOLE]: ok(captured.whole), [PHASE]: ok(captured.phase), [SEND]: ok(captured.sent) };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const key = init?.method === 'POST' ? `POST ${url}` : url;
    const r = (key in over ? over[key] : base[key]) ?? refused(404, `not served in this test: ${key}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const first = captured.whole.recommendations[0];

describe('MethodAppraisal, rendered against the method routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the whole plan: every reading says how it was read', async () => {
    serve();
    render(<MethodAppraisal />);
    const readings = await screen.findByTestId('appraisal-readings');
    expect(readings.textContent).not.toContain('this reading states no basis');
    expect(readings.textContent).toContain(`retrospection · ${captured.whole.faculties.retrospection.state} · `
      + captured.whole.faculties.retrospection.basis);
    expect(Object.keys(captured.whole.faculties)).toHaveLength(11);
  });

  it('a recommendation sent is said in the server\'s words', async () => {
    serve();
    render(<MethodAppraisal />);
    fireEvent.click(await screen.findByTestId(`send-${first.id}`));
    await waitFor(() => expect(screen.getByTestId(`sent-${first.id}`).textContent).toBe(
      `Change record ${captured.sent.change_control.cca_id} filed (${captured.sent.change_control.status}). `
      + captured.sent.basis));
  });

  it('a refused send is said by its reason, not as its JSON', async () => {
    serve({ [SEND]: { status: captured.refused_send.status, body: captured.refused_send.body } });
    render(<MethodAppraisal />);
    fireEvent.click(await screen.findByTestId(`send-${first.id}`));
    await waitFor(() => expect(screen.getByTestId(`send-refused-${first.id}`).textContent).toBe(
      `Not sent: Failed (HTTP 409): ${captured.refused_send.body.detail.message}`));
    expect(screen.queryByTestId(`sent-${first.id}`)).toBeNull();
  });

  it('a phase is appraised as the phase it names', async () => {
    serve();
    render(<MethodAppraisal />);
    await screen.findByTestId('appraisal-readings');
    fireEvent.change(screen.getByLabelText('Scope to appraise'), { target: { value: 'P3' } });
    fireEvent.click(screen.getByTestId('appraisal-run'));
    expect((await screen.findByText(`What the readings recommend · ${captured.phase.scope}`))).toBeTruthy();
  });

  it('a refused appraisal is said, and no reading of an earlier scope is left standing', async () => {
    serve({ [PHASE]: refused(503, 'the register could not be read') });
    render(<MethodAppraisal />);
    await screen.findByTestId('appraisal-readings');
    fireEvent.change(screen.getByLabelText('Scope to appraise'), { target: { value: 'P3' } });
    fireEvent.click(screen.getByTestId('appraisal-run'));
    await waitFor(() => expect(screen.getByTestId('appraisal-unavailable').textContent).toBe(
      'The appraisal could not be read: Failed (HTTP 503): the register could not be read'));
    expect(screen.queryByTestId('appraisal-readings')).toBeNull();
  });
});
