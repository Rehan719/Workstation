// W1009 (FU-399 part 39) — the Factory, rendered against its route's own stream.
//
// The Factory runs production lines: each line is one product (a name, a type, a domain and a description) written by
// the serving resource and streamed back as it is written, with what wrote it. This mounts the real page against what
// its route streamed on a fresh store with no model installed (Factory.fixture.json, captured by w1009_capture.py: the
// stream as the server sent it, and the route's refusal of a request with no body), played back as a stream, and has
// the server be unreachable. A refusal says the server's reason, a field check by its field.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Factory.fixture.json';
import { Factory } from './Factory';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
const PRODUCE = '/api/v1/factory/produce';

function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({ start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); } });
}

function serve(reply: Reply) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== PRODUCE) return { ok: false, status: 404, statusText: '', body: null, json: async () => ({ detail: `not served: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return { ok: reply.status < 400, status: reply.status, statusText: '',
             body: reply.stream !== undefined ? streamOf(reply.stream) : null, json: async () => reply.body };
  }));
}

async function produce() {
  render(<MemoryRouter><Factory /></MemoryRouter>);
  fireEvent.click(screen.getByRole('button', { name: /New Production Line/ }));
  fireEvent.change(await screen.findByLabelText('Production line name'), { target: { value: 'W1009 made-up order tracker' } });
  fireEvent.change(screen.getByLabelText('Production line description'),
    { target: { value: 'W1009 made up: a page where a bakery cooperative tracks the morning\'s orders' } });
  fireEvent.click(screen.getByRole('button', { name: 'Create Production Line' }));
  fireEvent.click(await screen.findByRole('button', { name: /Produce/ }));
}

const written = captured.produced.stream.split('\n').filter(l => l.startsWith('data: '))
  .map(l => JSON.parse(l.slice(6)) as { token?: string })
  .filter(ev => ev.token).map(ev => (ev.token as string).replace(/\\n/g, '\n')).join('');

describe('Factory, rendered against its route\'s own stream', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a product is written as the server streams it', async () => {
    serve({ status: 200, stream: captured.produced.stream });
    await produce();
    expect(await screen.findByText((_, el) => el?.tagName === 'PRE' && el.textContent === written)).toBeTruthy();
    expect(written.length).toBeGreaterThan(0);
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, body: captured.refused.body });
    await produce();
    expect(await screen.findByText('[ERROR] Failed (HTTP 422): body: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, unreachable: true });
    await produce();
    expect(await screen.findByText('[ERROR] Failed — backend unreachable.')).toBeTruthy();
  });
});
