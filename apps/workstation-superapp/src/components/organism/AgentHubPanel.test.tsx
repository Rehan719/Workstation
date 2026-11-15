// W1066 (FU-399 part 79) — the organism's Agent Collaboration Hub, rendered against its routes' own answers.
//
// The panel shows the hub's participants, its message bus (with a live stream) and its work-order letterbox, posts to
// the general channel as USER, and moves a work-order's status. This mounts the real panel against what each route
// answered on a fresh store (AgentHubPanel.fixture.json, captured by w1066_capture.py: an empty hub, a message posted
// as the panel posts it, a made-up work-order filed through the hub's own route and moved as the panel moves it, the
// route's refusal of a work-order it does not hold, and the two list routes' own 500s). jsdom has no EventSource, so
// the stream is a stand-in the test opens or fails. Rendering found the panel saying each list as empty before it was
// read, a failed read without its reason, a refused status change away from its work-order, and the hub stamping a
// work-order a person claimed as "claimed by an executor", which the panel itself says does not exist. Fixed here.
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './AgentHubPanel.fixture.json';
import AgentHubPanel from './AgentHubPanel';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const AGENTS = '/api/v1/hub/agents';
const MESSAGES = '/api/v1/hub/messages?limit=30';
const HANDOFFS = '/api/v1/hub/handoffs?limit=20';
const POST = '/api/v1/hub/message';
const HANDOFF = captured.handoffs_after.body.handoffs[0];
const MOVE = `/api/v1/hub/handoffs/${HANDOFF.handoff_id}/status`;
const QUIET = 'no messages — the bus is real, and currently quiet';
const NOBODY = 'none — no external agent session has registered on the hub';

//  the live stream, as a stand-in the test opens or fails
class Stream {
  static last: Stream | null = null;
  onopen: (() => void) | null = null;
  onerror: (() => void) | null = null;
  onmessage: ((e: { data: string }) => void) | null = null;
  closed = false;
  constructor(public url: string) { Stream.last = this; }
  close() { this.closed = true; }
}

//  each route as it answered; each read of the bus or the letterbox takes the next answer in its list (the last
//  stays), each status move the next in `moves`
function serve(plan: { agents?: Reply; messages?: Reply[]; handoffs?: Reply[]; post?: Reply; moves?: Reply[] } = {}) {
  const msgs = [...(plan.messages ?? [captured.messages, captured.messages_after])];
  const boxes = [...(plan.handoffs ?? [captured.handoffs_after, captured.handoffs_moved])];
  const moves = [...(plan.moves ?? [captured.moved])];
  const sent: { url: string; body: unknown }[] = [];
  const next = (list: Reply[]) => (list.length > 1 ? list.shift()! : list[0]);
  vi.stubGlobal('EventSource', Stream);
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    if (method === 'POST') sent.push({ url, body: JSON.parse(String(init?.body)) });
    let r: Reply;
    if (method === 'GET' && url === AGENTS) r = plan.agents ?? captured.agents;
    else if (method === 'GET' && url === MESSAGES) r = next(msgs);
    else if (method === 'GET' && url === HANDOFFS) r = next(boxes);
    else if (method === 'POST' && url === POST) r = plan.post ?? captured.posted;
    else if (method === 'POST' && url === MOVE) r = next(moves);
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

const mount = () => render(<AgentHubPanel />);
const row = () => screen.getByText(HANDOFF.task_title).closest('div.p-3') as HTMLElement;

describe('AgentHubPanel, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    Stream.last = null;
  });

  it('says on opening what each read answered: nobody registered, the roster, a quiet bus, and the letterbox', async () => {
    serve({ handoffs: [captured.handoffs] });
    mount();
    await waitFor(() => expect(screen.getByText(QUIET)).toBeTruthy());
    expect(screen.getByText(NOBODY)).toBeTruthy();
    for (const a of captured.agents.body.platform_roster) expect(screen.getAllByText(a.role).length).toBeGreaterThan(0);
    await waitFor(() => expect(screen.getByText('no work-orders filed')).toBeTruthy());
    expect(screen.getByText('connecting…')).toBeTruthy();
    await act(async () => { Stream.last!.onopen!(); });
    expect(screen.getByText('stream connected (SSE)')).toBeTruthy();
    expect(Stream.last!.url).toBe('/api/v1/hub/stream');
  });

  it('says no list is empty, or unavailable, before it has been read', async () => {
    const agents = held(captured.agents);
    const msgs = held(captured.messages);
    const box = held(captured.handoffs);
    serve({ agents: agents.reply, messages: [msgs.reply], handoffs: [box.reply] });
    mount();
    await waitFor(() => expect(screen.getByText('connecting…')).toBeTruthy());
    expect(screen.queryByText(QUIET)).toBeNull();
    expect(screen.queryByText(NOBODY)).toBeNull();
    expect(screen.queryByText(/^letterbox unavailable/)).toBeNull();
    expect(screen.queryByText('no work-orders filed')).toBeNull();
    await act(async () => { agents.letGo(); msgs.letGo(); box.letGo(); });
    await waitFor(() => expect(screen.getByText(QUIET)).toBeTruthy());
    expect(screen.getByText(NOBODY)).toBeTruthy();
    expect(screen.getByText('no work-orders filed')).toBeTruthy();
  });

  it('says each list it could not read with the route\'s reason', async () => {
    serve({ messages: [captured.messages_failed], handoffs: [captured.handoffs_failed] });
    mount();
    await waitFor(() => expect(screen.getByTestId('hub-messages-unread').textContent).toBe(
      `The message feed could not be read: Failed (HTTP 500): ${captured.messages_failed.body.detail} This is not a quiet bus.`));
    expect(screen.getByTestId('hub-handoffs-unread').textContent).toBe(
      `The letterbox could not be read: Failed (HTTP 500): ${captured.handoffs_failed.body.detail} No work-order is listed.`);
    expect(screen.queryByText(QUIET)).toBeNull();
    expect(screen.queryByText('no work-orders filed')).toBeNull();
  });

  it('posts what the person typed, says no live subscriber received it, and reads the bus again', async () => {
    const sent = serve();
    mount();
    await waitFor(() => expect(screen.getByText(QUIET)).toBeTruthy());
    fireEvent.change(screen.getByLabelText('hub message'), { target: { value: captured.post_ask.content } });
    fireEvent.click(screen.getByRole('button', { name: /Post/ }));
    await waitFor(() => expect(screen.getByText(/^Stored — no live subscribers received it/)).toBeTruthy());
    expect(sent.find(s => s.url === POST)!.body).toEqual(captured.post_ask);
    await waitFor(() => expect(screen.getByText(captured.post_ask.content)).toBeTruthy());
  });

  it('moves a work-order as asked, and says a refused move beside that work-order', async () => {
    const sent = serve({ moves: [captured.move_missing, captured.moved] });
    mount();
    await waitFor(() => expect(row()).toBeTruthy());
    expect(within(row()).getByText(HANDOFF.status)).toBeTruthy();
    fireEvent.click(within(row()).getByRole('button', { name: 'claim' }));
    await waitFor(() => expect(within(row()).getByTestId('hub-handoff-move-error').textContent).toBe(
      `Not moved: Failed (HTTP 404): ${captured.move_missing.body.detail}`));
    expect(sent.find(s => s.url === MOVE)!.body).toEqual({ status: 'in_progress' });
    fireEvent.click(within(row()).getByRole('button', { name: 'claim' }));
    await waitFor(() => expect(within(row()).getByText('in_progress')).toBeTruthy());
    expect(within(row()).queryByTestId('hub-handoff-move-error')).toBeNull();
    //  and the hub's note says who moved it: it said "claimed by an executor", and no executor is subscribed
    const moved = captured.handoffs_moved.body.handoffs[0];
    expect(moved.status_note).toBe('claimed by the operator of this single-user deployment');
    expect(within(row()).getByText(moved.status_note)).toBeTruthy();
    expect(row().textContent).not.toContain('executor');
  });
});
