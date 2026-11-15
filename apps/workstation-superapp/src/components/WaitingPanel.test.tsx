// W1086 (P5.18 clause 3, FU-1267); W1087 (P5.14 clause 4, FU-1269) — the one list of what waits on you, rendered
// against its route's own answers.
//
// The panel shows what GET /api/v1/waiting answered on a fresh store (WaitingPanel.fixture.json, captured by
// w1087_capture.py): with sign-in off, a made-up project waiting on a decision on its proposal and a made-up change in
// Change Control's queue, with the route's sentence that agreement and asset records are kept only after sign-in;
// signed in as a made-up person, the list over their made-up agreement, asset and project; the list after one
// obligation was confirmed; the list when the agreement store could not be read whole; the route's own 400; and a
// second made-up person's list, on which nothing waits. Everything in it is made up, and nothing is legal advice.
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
const line = (i: any) => `${i.what} (${i.ref ? `${i.ref}, ` : ''}on ${i.on}): ${clause(i.said)}${
  i.kind === 'falls_due' && !i.confirmed ? '; not confirmed by a person yet' : ''}. It is acted on in ${i.where}.`;
const reads = (r: any) => `This list reads ${r.reads.join('; ')}.${
  r.not_read_yet.length ? ` It does not read yet: ${r.not_read_yet.join('; ')}.` : ''} ${r.date_basis}`;

describe('WaitingPanel, rendered against its route\'s own answers (made-up records)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('with sign-in off says why agreement and asset records are not on it, and lists what the other stores hold', async () => {
    serve([C.waiting_off]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-not-kept').textContent).toBe(C.waiting_off.body.not_kept));
    expect(items()).toEqual(C.waiting_off.body.items.map(line));
    expect(C.waiting_off.body.items.map((i: any) => i.source)).toEqual(['project', 'change']);
  });

  it('says what waits soonest first, each with the record it is on and where it is acted on', async () => {
    serve([C.waiting]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getAllByTestId('waiting-item')).toHaveLength(C.waiting.body.items.length));
    expect(items()).toEqual(C.waiting.body.items.map(line));
    expect(C.waiting.body.items.map((i: any) => i.source)).toEqual(
      ['agreement', 'asset', 'asset', 'agreement', 'project', 'agreement', 'agreement']);
    expect(items().every(t => !t?.includes('..'))).toBe(true);   // a sentence ends once
    expect(screen.getByTestId('waiting-reads').textContent).toBe(reads(C.waiting.body));
    expect(screen.queryByTestId('waiting-not-kept')).toBeNull();
    expect(screen.queryByTestId('waiting-store-unread')).toBeNull();
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

  it('a store that could not be read is said in its place, and what the other stores hold still stands', async () => {
    serve([C.waiting_store_unread]);
    render(<WaitingPanel />);
    const b = C.waiting_store_unread.body;
    await waitFor(() => expect(screen.getAllByTestId('waiting-store-unread').map(p => p.textContent)).toEqual(
      b.unread.map((u: any) => u.said)));
    expect(items()).toEqual(b.items.map(line));
    expect(b.items.some((i: any) => i.source === 'agreement')).toBe(false);
    expect(screen.queryByTestId('waiting-none')).toBeNull();
  });

  it('says nothing waits only as the route says it', async () => {
    serve([C.waiting_none]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-none').textContent).toBe(C.waiting_none.body.said));
    expect(C.waiting_none.body.items).toEqual([]);
  });

  it('a refused read says its reason, and says nothing waiting', async () => {
    serve([C.waiting_refused]);
    render(<WaitingPanel />);
    await waitFor(() => expect(screen.getByTestId('waiting-unread').textContent).toBe(
      `What waits on you could not be read (Failed (HTTP ${C.waiting_refused.status}): ${C.waiting_refused.body.detail}), so nothing is said about it here.`));
    expect(screen.queryByTestId('waiting-none')).toBeNull();
    expect(screen.queryByTestId('waiting-reads')).toBeNull();
  });
});
