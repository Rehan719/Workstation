// W1068 (FU-399 part 81) — the Religion hub's Learn and Teach module, rendered against its routes' own answers.
//
// The module reads the scholar roster when it opens and asks the scholar-review gate for a study-plan frame, which a
// learner sees only once a scholar on the roster has approved that exact text (P3.10). This mounts the real module
// against what each route answered on a fresh store (LearnTeachModule.fixture.json, captured by w1068_capture.py:
// the roster with no scholar on it, the gate's answer to the module's own request then, the roster with a made-up
// reviewer on it and the gate's answer then, and each route's own 500). Every gate answer kept is withheld: no
// composed religious text is in the fixture, and nothing was approved. Rendering found a roster it could not read
// said without its reason, and a withheld plan headed "withheld — withheld". Fixed here.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './LearnTeachModule.fixture.json';
import { LearnTeachModule } from './LearnTeachModule';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const STATUS = '/api/v1/scholar-review/status';
const PLAN = '/api/v1/qep/curriculum';
const ASK = 'Generate a study-plan frame';
const NONE_ON_ROSTER = /^No scholars are verified on this deployment — the roster holds none\./;
const UNREAD_ROSTER = /^Whether any scholar is on the roster could not be read here, so nothing is said about who reviews\./;

//  each route as it answered; each request for a plan takes the next answer in `plans` (the last one stays)
function serve(plan: { status?: Reply; plans?: Reply[] } = {}) {
  const plans = [...(plan.plans ?? [captured.plan_empty_roster])];
  const sent: { url: string; method: string; body?: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    sent.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    let r: Reply;
    if (method === 'GET' && url === STATUS) r = plan.status ?? captured.status;
    else if (method === 'POST' && url === PLAN) r = plans.length > 1 ? plans.shift()! : plans[0];
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

const mount = () => render(<MemoryRouter><LearnTeachModule /></MemoryRouter>);
const board = () => screen.getByTestId('learnteach-scholar-board').textContent ?? '';

describe('LearnTeachModule, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('reads the roster on opening, and says it holds no scholar only once read', async () => {
    const status = held(captured.status);
    serve({ status: status.reply });
    mount();
    expect(board()).toBe('Reading the scholar roster…');
    await act(async () => { status.letGo(); });
    await waitFor(() => expect(board()).toMatch(NONE_ON_ROSTER));
    expect(screen.queryByTestId('learnteach-roster-unread')).toBeNull();
  });

  it('says a roster it could not read with the route\'s reason', async () => {
    serve({ status: captured.status_failed });
    mount();
    await waitFor(() => expect(board()).toMatch(UNREAD_ROSTER));
    expect(screen.getByTestId('learnteach-roster-unread').textContent).toBe(
      `The roster could not be read: Failed (HTTP 500): ${captured.status_failed.body.detail}`);
  });

  it('asks the gate as the module asks, and says a withheld plan once, with the gate\'s reason', async () => {
    const sent = serve();
    mount();
    await waitFor(() => expect(board()).toMatch(NONE_ON_ROSTER));
    fireEvent.click(screen.getByRole('button', { name: ASK }));
    await waitFor(() => expect(screen.getByTestId('learnteach-review-note').textContent).toBe(
      captured.plan_empty_roster.body.review_note));
    expect(sent.find(s => s.url === PLAN)).toEqual({ url: PLAN, method: 'POST', body: captured.plan_ask });
    expect(screen.getByTestId('learnteach-review-heading').textContent).toBe('withheld');
    //  nothing is shown in a withheld plan's place: no frame, no badge, no caption
    expect(screen.queryByTestId('qep-studyframe-provenance')).toBeNull();
    expect(screen.queryByTestId('learnteach-plan-caption')).toBeNull();
  });

  it('says the scholars on the roster as the route counts them, and a plan awaiting their review', async () => {
    serve({ status: captured.status_one, plans: [captured.plan_awaiting] });
    mount();
    await waitFor(() => expect(board()).toMatch(
      /^1 scholar is on the roster, each entered by the Owner on the scholar's behalf — attested, not verified\./));
    fireEvent.click(screen.getByRole('button', { name: ASK }));
    await waitFor(() => expect(screen.getByTestId('learnteach-review-note').textContent).toBe(
      captured.plan_awaiting.body.review_note));
    expect(screen.getByTestId('learnteach-review-heading').textContent).toBe('withheld');
  });

  it('says a request for a plan that failed by its reason, with nothing withheld or shown', async () => {
    serve({ plans: [captured.plan_failed] });
    mount();
    await waitFor(() => expect(board()).toMatch(NONE_ON_ROSTER));
    fireEvent.click(screen.getByRole('button', { name: ASK }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe(
      `Failed (HTTP 500): ${captured.plan_failed.body.detail}`));
    expect(screen.queryByTestId('learnteach-review-state')).toBeNull();
    expect(screen.queryByTestId('learnteach-plan-caption')).toBeNull();
    expect((screen.getByRole('button', { name: ASK }) as HTMLButtonElement).disabled).toBe(false);
  });

  it('takes the gate\'s own count over a roster it could not read, and clears that failure', async () => {
    serve({ status: captured.status_failed });
    mount();
    await waitFor(() => expect(screen.getByTestId('learnteach-roster-unread')).toBeTruthy());
    fireEvent.click(screen.getByRole('button', { name: ASK }));
    await waitFor(() => expect(board()).toMatch(NONE_ON_ROSTER));
    expect(screen.queryByTestId('learnteach-roster-unread')).toBeNull();
    expect(screen.getByTestId('learnteach-review-heading').textContent).toBe('withheld');
  });
});
