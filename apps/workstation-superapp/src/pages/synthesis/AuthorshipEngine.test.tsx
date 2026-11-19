// W1036 (FU-399 part 57) — Authorship Intelligence, rendered against its route's own stream.
//
// The page runs the Scholarship & Authorship pipeline over a topic, nine stages each through the in-house gateway,
// and shows each stage as it streams in with what served it. This mounts the real page against what its route
// streamed on a fresh store with no model installed (AuthorshipEngine.fixture.json, captured by w1036_capture.py: the
// stream as the server sent it for a made-up topic, and the route's refusal of a request with no topic), played back
// as a stream, and has the server be unreachable. Rendering found one defect, fixed in this round: "Expand All"
// opened the first stage's card and left the other eight shut. It opens every stage now, and "Collapse All" shuts them.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './AuthorshipEngine.fixture.json';
import { AuthorshipEngine } from './AuthorshipEngine';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
type Ev = { stage: string; label: string; content: string; data?: { stage_num?: number; failed?: boolean } };
const ROUTE = '/api/v1/intelligence/authorship';

//  the captured stream, played back in two pieces cut mid-frame, as a network delivers it
function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({
    start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); },
  });
}

const asked: unknown[] = [];
function serve(reply: Reply) {
  asked.length = 0;
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { body?: string }) => {
    if (url !== ROUTE) return { ok: false, status: 404, statusText: '', body: null, json: async () => ({ detail: `not served: ${url}` }) };
    asked.push(JSON.parse(init?.body ?? 'null'));
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return {
      ok: reply.status < 400, status: reply.status, statusText: '',
      body: reply.stream !== undefined ? streamOf(reply.stream) : null,
      json: async () => reply.body,
    };
  }));
}

//  the page asks what the capture asked: its topic, genre, domain, audience, citation style, length and rigor
function run() {
  render(<AuthorshipEngine />);
  const ask = captured.ask;
  fireEvent.change(screen.getByPlaceholderText('State your scholarly topic, thesis, or central research question in detail...'),
    { target: { value: ask.topic } });
  fireEvent.click(screen.getByRole('button', { name: ask.genre }));
  fireEvent.click(screen.getByRole('button', { name: ask.citation_style }));
  fireEvent.click(screen.getByRole('button', { name: ask.domain }));
  fireEvent.click(screen.getByRole('button', { name: ask.rigor }));
  fireEvent.change(screen.getByPlaceholderText('e.g. academic peers, policymakers...'), { target: { value: ask.audience } });
  fireEvent.change(screen.getByPlaceholderText('e.g. 8000'), { target: { value: ask.word_count } });
  fireEvent.click(screen.getByRole('button', { name: /Run APIE/ }));
}

const events = captured.authorship.stream.split('\n').filter(l => l.startsWith('data: ') && l.slice(6).trim() !== '[DONE]')
  .map(l => JSON.parse(l.slice(6)) as Ev);
const stages = events.filter(ev => typeof ev.data?.stage_num === 'number');
const complete = events.find(ev => ev.stage === 'complete') as Ev;

//  a stage's text as its open card shows it: the paragraph whose text is the stage's, line breaks and all
const shown = (content: string) => screen.queryAllByText((_, el) => el?.tagName === 'P' && el.textContent === content);

describe('AuthorshipEngine, rendered against its route\'s own stream', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('asks what was chosen, and shows the stream stage by stage, the count that ran the stream\'s own', async () => {
    serve({ status: 200, stream: captured.authorship.stream });
    run();
    const ran = stages.filter(ev => !ev.data?.failed).length;
    expect(await screen.findByText(`Pipeline Output — ${ran} of 9 stages ran`)).toBeTruthy();
    expect(stages).toHaveLength(9);
    expect(asked).toEqual([captured.ask]);
    //  the completion line is the stream's own, with the genre and citation style the server ran
    await waitFor(() => expect(screen.getByText('Authorship Pipeline Finished').textContent).toBe('Authorship Pipeline Finished'));
    expect(screen.getByText(`${complete.content} — ${captured.ask.genre} · ${captured.ask.citation_style}`)).toBeTruthy();
  });

  it('"Expand All" opens every stage, and "Collapse All" shuts them', async () => {
    serve({ status: 200, stream: captured.authorship.stream });
    run();
    await waitFor(() => expect(screen.getByText('Authorship Pipeline Finished').textContent).toBe('Authorship Pipeline Finished'));
    for (const ev of stages) expect(shown(ev.content)).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Expand All' }));
    for (const ev of stages) expect(shown(ev.content)).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: 'Collapse All' }));
    for (const ev of stages) expect(shown(ev.content)).toHaveLength(0);
  });

  it('a card opened by hand opens alone, and "Expand All" then opens the rest', async () => {
    serve({ status: 200, stream: captured.authorship.stream });
    run();
    await waitFor(() => expect(screen.getByText('Authorship Pipeline Finished').textContent).toBe('Authorship Pipeline Finished'));
    const second = screen.getByRole('button', { name: new RegExp(`^${stages[1].label}`) });
    fireEvent.click(second);
    expect(second.getAttribute('aria-expanded')).toBe('true');
    expect(stages.map(ev => shown(ev.content).length)).toEqual(stages.map((_, i) => (i === 1 ? 1 : 0)));
    fireEvent.click(screen.getByRole('button', { name: 'Expand All' }));
    expect(stages.map(ev => shown(ev.content).length)).toEqual(stages.map(() => 1));
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, body: captured.refused.body });
    run();
    expect(await screen.findByText('Failed (HTTP 422): topic: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, unreachable: true });
    run();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });
});
