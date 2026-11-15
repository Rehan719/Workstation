// W1069 (FU-399 part 82) — the Quran platform's scholar review panel, rendered against its routes' own answers.
//
// The panel reads the scholar-review gate's status and its queue, adds a named scholar to the roster, and enters a
// scholar's decision on an item that awaits review; above the queue it mounts the children's approval pack, handed
// the roster. This mounts the real panel against what each route answered on a fresh store
// (ScholarReviewPanel.fixture.json, captured by w1069_capture.py): the status and the queue empty; one item in the
// queue whose text is a made-up placeholder (the gate's compose was replaced, so no composed religious text is kept);
// a made-up reviewer added; that reviewer's rejection of the placeholder; the route's 409 for a reviewer not on the
// roster; and the status and queue routes' own 500s. Nothing in it was approved, and no Arabic is in it. The pack is a
// stand-in here that says what it was handed (its own answer is not kept). Rendering found the roster and the queue
// said as empty before their reads answered and when they failed, one refused read taking the other's answer down,
// and the pack told "No scholar is on the roster" of a roster nobody had read. Fixed here.
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ScholarReviewPanel.fixture.json';
import ScholarReviewPanel from './ScholarReviewPanel';

vi.mock('./ChildrenApprovalPack', () => ({
  ChildrenApprovalPack: ({ roster, chosen }: { roster: [string, { name: string }][] | null; chosen: string }) => (
    <p>{`pack stand-in: ${roster === null ? 'roster unread' : `roster of ${roster.length}`}${chosen ? `, for ${chosen}` : ''}`}</p>
  ),
}));

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const STATUS = '/api/v1/scholar-review/status';
const QUEUE = '/api/v1/scholar-review/queue';
const ROSTER = '/api/v1/scholar-review/roster';
const DECIDE = '/api/v1/scholar-review/decide';
const NOBODY = 'No scholar is recorded, so nothing can be approved and every item stays withheld.';
const NOTHING = 'Nothing has been composed and submitted for review.';
const SCHOLAR = captured.scholar_ask;
const ITEM = captured.queue_one.body.items[0];

//  each route as it answered; each read of the status or the queue takes the next answer in its list (the last
//  one stays), each roster or decision post the next in its own
function serve(plan: { status?: Reply[]; queue?: Reply[]; roster?: Reply[]; decide?: Reply[] } = {}) {
  const lists = {
    status: [...(plan.status ?? [captured.status])],
    queue: [...(plan.queue ?? [captured.queue])],
    roster: [...(plan.roster ?? [captured.scholar_added])],
    decide: [...(plan.decide ?? [captured.decided])],
  };
  const next = (list: Reply[]) => (list.length > 1 ? list.shift()! : list[0]);
  const sent: { url: string; method: string; body?: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    sent.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    let r: Reply;
    if (method === 'GET' && url === STATUS) r = next(lists.status);
    else if (method === 'GET' && url === QUEUE) r = next(lists.queue);
    else if (method === 'POST' && url === ROSTER) r = next(lists.roster);
    else if (method === 'POST' && url === DECIDE) r = next(lists.decide);
    else r = { status: 404, body: { detail: `not served here: ${method} ${url}` } };
    const a = await r;
    if (a === 'unreachable') throw new TypeError('Failed to fetch');
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return sent;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const item = () => screen.getByTestId('scholar-item');
//  what the pack's stand-in was handed (it is found by its own words: the app declares no test id for it)
const pack = () => screen.getByText(/^pack stand-in: /).textContent;

describe('ScholarReviewPanel, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('says nothing of the roster or the queue before each is read, then what each read answered', async () => {
    const status = held(captured.status);
    const queue = held(captured.queue);
    serve({ status: [status.reply], queue: [queue.reply] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(screen.getByText('Reading the roster…')).toBeTruthy());
    expect(screen.getByText('Reading the review queue…')).toBeTruthy();
    expect(screen.queryByText(NOBODY)).toBeNull();
    expect(screen.queryByText(NOTHING)).toBeNull();
    expect(pack()).toBe('pack stand-in: roster unread');
    await act(async () => { status.letGo(); queue.letGo(); });
    await waitFor(() => expect(screen.getByText(NOBODY)).toBeTruthy());
    expect(screen.getByText(NOTHING)).toBeTruthy();
    expect(pack()).toBe('pack stand-in: roster of 0');
    expect(screen.getByTestId('scholar-footing').textContent).toBe(
      `Authentication is off. Who adds a scholar: ${captured.status.body.footing.who_adds_a_scholar}. Who decides: ${captured.status.body.footing.who_decides}.`);
  });

  it('says a status it could not read with its reason, and the queue it did read', async () => {
    serve({ status: [captured.status_failed], queue: [captured.queue_held] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(screen.getByTestId('scholar-status-unread').textContent).toBe(
      `The scholar review status could not be read: Failed (HTTP 500): ${captured.status_failed.body.detail}`));
    expect(screen.getByTestId('scholar-roster-unread')).toBeTruthy();
    expect(screen.queryByText(NOBODY)).toBeNull();
    await waitFor(() => expect(within(item()).getByText(ITEM.body)).toBeTruthy());
    expect(pack()).toBe('pack stand-in: roster unread');
  });

  it('says a queue it could not read with its reason, and the roster it did read', async () => {
    serve({ status: [captured.status_one], queue: [captured.queue_failed] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(screen.getByTestId('scholar-queue-unread').textContent).toBe(
      `The review queue could not be read: Failed (HTTP 500): ${captured.queue_failed.body.detail}`));
    expect(screen.queryByText(NOTHING)).toBeNull();
    expect(screen.getAllByText(SCHOLAR.name).length).toBe(2);   // its row, and the choice of who decides
    expect(pack()).toBe('pack stand-in: roster of 1');
  });

  it('adds a scholar as the panel asks, says what was recorded, and reads the roster again', async () => {
    const sent = serve({ status: [captured.status, captured.status_one], queue: [captured.queue] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(screen.getByText(NOBODY)).toBeTruthy());
    fireEvent.change(screen.getByLabelText('Scholar id'), { target: { value: SCHOLAR.scholar_id } });
    fireEvent.change(screen.getByLabelText('Scholar name'), { target: { value: SCHOLAR.name } });
    fireEvent.change(screen.getByLabelText('Stated credential'), { target: { value: SCHOLAR.credential } });
    fireEvent.click(screen.getByRole('button', { name: 'Add scholar' }));
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe(
      `Recorded ${SCHOLAR.name}. The credential is stored as stated; nothing here verified it.`));
    expect(sent.find(s => s.url === ROSTER)).toEqual({ url: ROSTER, method: 'POST', body: SCHOLAR });
    await waitFor(() => expect(screen.getAllByText(SCHOLAR.name).length).toBe(2));
    expect(pack()).toBe('pack stand-in: roster of 1');
  });

  it('enters a rejection for the chosen scholar, and says the decision the queue then records', async () => {
    const sent = serve({ status: [captured.status_one], queue: [captured.queue_one, captured.queue_decided] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(within(item()).getByText(ITEM.body)).toBeTruthy());
    expect((within(item()).getByRole('button', { name: 'Reject' }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(screen.getByLabelText('Scholar deciding'), { target: { value: SCHOLAR.scholar_id } });
    fireEvent.click(within(item()).getByRole('button', { name: 'Reject' }));
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe('Rejection recorded.'));
    expect(sent.find(s => s.url === DECIDE)).toEqual({ url: DECIDE, method: 'POST', body: captured.decide_ask });
    const decided = captured.queue_decided.body.items[0];
    await waitFor(() => expect(screen.getByTestId('scholar-decision').textContent).toBe(
      `${decided.state} for ${SCHOLAR.name} on ${String(decided.reviewed_at).slice(0, 10)} — ${decided.attestation}`));
  });

  it('says a decision the route refused by its reason', async () => {
    serve({ status: [captured.status_one], queue: [captured.queue_one], decide: [captured.decide_unknown] });
    render(<ScholarReviewPanel />);
    await waitFor(() => expect(within(item()).getByText(ITEM.body)).toBeTruthy());
    fireEvent.change(screen.getByLabelText('Scholar deciding'), { target: { value: SCHOLAR.scholar_id } });
    fireEvent.click(within(item()).getByRole('button', { name: 'Reject' }));
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe(
      `Not decided. Failed (HTTP 409): ${captured.decide_unknown.body.detail}`));
  });
});
