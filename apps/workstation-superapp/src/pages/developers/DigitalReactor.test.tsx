// W1009 (FU-399 part 39) — the Digital Reactor, rendered against its route's own stream.
//
// The Reactor asks the serving resource to narrate a domain's pipeline as a streamed log, and executes nothing; the
// log ends with the run, how long it took to write, and what wrote it. This mounts the real page against what its
// route streamed on a fresh store with no model installed (DigitalReactor.fixture.json, captured by w1009_capture.py:
// the stream as the server sent it, and the route's refusal of a request with no body), played back as a stream, and
// has the server be unreachable. A refusal says the server's reason, a field check by its field.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './DigitalReactor.fixture.json';
import { DigitalReactor } from './DigitalReactor';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
const RUN = '/api/v1/reactor/run';

function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({ start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); } });
}

function serve(reply: Reply) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== RUN) return { ok: false, status: 404, statusText: '', body: null, json: async () => ({ detail: `not served: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return { ok: reply.status < 400, status: reply.status, statusText: '',
             body: reply.stream !== undefined ? streamOf(reply.stream) : null, json: async () => reply.body };
  }));
}

function launch() {
  render(<MemoryRouter><DigitalReactor /></MemoryRouter>);
  fireEvent.click(screen.getByRole('button', { name: /Launch Reactor/ }));
}

const done = captured.narrated.stream.split('\n').filter(l => l.startsWith('data: '))
  .map(l => JSON.parse(l.slice(6)) as { done?: boolean; run_id?: string; duration_ms?: number; served_by?: string })
  .find(ev => ev.done);

describe('DigitalReactor, rendered against its route\'s own stream', () => {
  beforeEach(() => {
    //  the log scrolls itself after each piece; jsdom draws nothing, so there is nothing to scroll
    Element.prototype.scrollTo = () => undefined;
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the narrative streams in as a log, ending with the run and what wrote it', async () => {
    serve({ status: 200, stream: captured.narrated.stream });
    launch();
    expect(await screen.findByText(new RegExp(`Narrative complete — run ${done?.run_id}, written in ${done?.duration_ms}ms by ${done?.served_by}\\.`))).toBeTruthy();
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, body: captured.refused.body });
    launch();
    expect(await screen.findByText('[ERROR] Failed (HTTP 422): body: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, unreachable: true });
    launch();
    expect(await screen.findByText('[ERROR] Failed — backend unreachable.')).toBeTruthy();
  });
});
