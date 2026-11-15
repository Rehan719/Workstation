// W1086 (P5.18 clause 3, FU-1267) — the one list of what waits on you, rendered against its route's own answers.
//
// The panel shows what GET /api/v1/waiting (W1085) answered on a fresh store (WaitingPanel.fixture.json, captured by
// w1086_capture.py beside the agreements panel's fixture): with sign-in off, which keeps nothing; then, signed in as a
// made-up person, the list with two obligations falling due (one past its date) and two not confirmed, the list after
// one was confirmed, the list once the agreement's end was recorded, and the route's own 503 when the agreement store
// cannot be read whole. Every party, obligation and agreement is made up, and nothing is legal advice.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './WaitingPanel.fixture.json';
import WaitingPanel from './WaitingPanel';

const C: any = captured;
type Answer = { status: number; body: any };

function serve(answers: Answer[]) {
  const list = [...answers];
  const asked: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    asked.push(url);
    const a = url === '/api/v1/waiting' ? (list.length > 1 ? list.shift()! : list[0])
      : { status: 404, body: { detail: `not served in this test: ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return asked;
}

const items = () => screen.getAllByTestId('waiting-item').map(li => li.textContent);
const clause = (s: string) => s.replace(/\s*\.\s*$/, '');
const line = (i: any) => `${i.what} (${i.clause}, on ${i.agreement_title}): ${clause(i.said)}${i.kind === 'falls_due' && !i.confirmed ? '; not confirmed by a person yet' : ''}.`;

describe('WaitingPanel, rendered against its route\'s own answers (made-up obligations)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('with sign-in off says nothing is kept, by the route\'s reason', async () => {
    serve([C.waiting_off]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-not-kept').textContent).toBe(C.waiting_off.body.said));
    expect(screen.queryByTestId('waiting-item')).toBeNull();
  });

  it('says what falls due soonest first, then what waits for a confirmation, each with its clause and agreement', async () => {
    serve([C.waiting]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getAllByTestId('waiting-item')).toHaveLength(C.waiting.body.items.length));
    expect(items()).toEqual(C.waiting.body.items.map(line));
    expect(C.waiting.body.items[0].said).toMatch(/^fell due 3 days ago$/);
    expect(items().every(t => !t?.includes('..'))).toBe(true);   // a sentence ends once
    const r = C.waiting.body;
    expect(screen.getByTestId('waiting-reads').textContent).toBe(
      `This list reads ${r.reads.join('; ')}. It does not read yet: ${r.not_read_yet.join('; ')}. ${r.date_basis}`);
  });

  it('reads the list again when asked: a confirmed obligation no longer waits for a confirmation', async () => {
    const asked = serve([C.waiting, C.waiting_after]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getAllByTestId('waiting-item')).toHaveLength(C.waiting.body.items.length));
    fireEvent.click(screen.getByRole('button', { name: 'Read it again' }));
    await waitFor(() => expect(screen.getAllByTestId('waiting-item')).toHaveLength(C.waiting_after.body.items.length));
    expect(items()).toEqual(C.waiting_after.body.items.map(line));
    expect(asked).toEqual(['/api/v1/waiting', '/api/v1/waiting']);
  });

  it('says nothing waits only as the route says it, once the agreement has ended', async () => {
    serve([C.waiting_ended]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-none').textContent).toBe(C.waiting_ended.body.said));
    expect(C.waiting_ended.body.items).toEqual([]);
  });

  it('a failed read says its reason, and says nothing waiting', async () => {
    serve([C.waiting_unread]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-unread').textContent).toBe(
      `What waits on you could not be read (Failed (HTTP ${C.waiting_unread.status}): ${C.waiting_unread.body.detail}), so nothing is said about it here.`));
    expect(screen.queryByTestId('waiting-none')).toBeNull();
    expect(screen.queryByTestId('waiting-reads')).toBeNull();
  });
});
