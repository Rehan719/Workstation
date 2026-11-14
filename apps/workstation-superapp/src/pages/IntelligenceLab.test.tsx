// W1008 (FU-399 part 38) — the Intelligence Lab, rendered against its route's own stream.
//
// The Lab runs the Business Development Process or Scientific Process Intelligence over a challenge, eight stages each
// through the in-house gateway, and shows each stage as it streams in with what served it. This mounts the real page
// against what its route streamed on a fresh store with no model installed (IntelligenceLab.fixture.json, captured by
// w1008_capture.py: the stream as the server sent it, and the route's refusal of a request with no challenge), played
// back as a stream, and has the server be unreachable. A refusal says the server's reason, a field check by its field.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './IntelligenceLab.fixture.json';
import { IntelligenceLab } from './IntelligenceLab';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
const BDP = '/api/v1/intelligence/bdp';

//  the captured stream, played back in two pieces cut mid-frame, as a network delivers it
function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({
    start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); },
  });
}

function serve(reply: Reply) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== BDP) return { ok: false, status: 404, statusText: '', body: null, json: async () => ({ detail: `not served: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return {
      ok: reply.status < 400, status: reply.status, statusText: '',
      body: reply.stream !== undefined ? streamOf(reply.stream) : null,
      json: async () => reply.body,
    };
  }));
}

function run() {
  render(<MemoryRouter><IntelligenceLab /></MemoryRouter>);
  fireEvent.change(screen.getByPlaceholderText('Describe your business challenge, opportunity, or venture concept...'),
    { target: { value: 'W1008 made up: a delivery cooperative for village bakeries' } });
  fireEvent.click(screen.getByRole('button', { name: /Run BDP Engine/ }));
}

const stages = captured.bdp.stream.split('\n').filter(l => l.startsWith('data: ') && l.slice(6).trim() !== '[DONE]')
  .map(l => JSON.parse(l.slice(6)) as { data?: { stage_num?: number; failed?: boolean } })
  .filter(ev => typeof ev.data?.stage_num === 'number');

describe('IntelligenceLab, rendered against its route\'s own stream', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the stream is shown stage by stage, the count of stages that ran the stream\'s own', async () => {
    serve({ status: 200, stream: captured.bdp.stream });
    run();
    const ran = stages.filter(ev => !ev.data?.failed).length;
    expect(await screen.findByText(`Analysis Results — ${ran} of 8 stages ran`)).toBeTruthy();
    expect(stages).toHaveLength(8);
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, body: captured.refused.body });
    run();
    expect(await screen.findByText('Failed (HTTP 422): challenge: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, unreachable: true });
    run();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });

  it('an answer that carries no stream is said, not taken for a run that showed nothing', async () => {
    //  written here: the route has not been seen to answer without a stream
    serve({ status: 200 });
    run();
    expect(await screen.findByText('The server answered without a stream, so nothing ran here.')).toBeTruthy();
  });
});
