// W1037 (FU-399 part 58) — Design & Dev Intelligence, rendered against its route's own stream.
//
// The page runs the Design & Development pipeline over a system, nine stages each through the in-house gateway, and
// shows each stage as it streams in with what served it. This mounts the real page against what its route streamed on
// a fresh store with no model installed (DesignDevEngine.fixture.json, captured by w1037_capture.py: the stream as the
// server sent it for a made-up system and stack, and the route's refusal of a request with no system), played back as
// a stream, and has the server be unreachable. Rendering found one defect, fixed in this round: the output's header
// said the form's stack, scale and target as they stood, so changing one after a run relabelled that run's stages.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DesignDevEngine.fixture.json';
import { DesignDevEngine } from './DesignDevEngine';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
type Ev = { stage: string; label: string; content: string; data?: { stage_num?: number; failed?: boolean } };
const ROUTE = '/api/v1/intelligence/design-dev';

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

const STACK = 'Or enter custom stack: e.g. Rust / Axum / SvelteKit / CockroachDB';

//  the page asks what the capture asked: its system, domain, a stack typed in, scale, target and rigor
function run() {
  render(<DesignDevEngine />);
  const ask = captured.ask;
  fireEvent.change(screen.getByPlaceholderText(/^Describe the system or product to design and build/), { target: { value: ask.system } });
  fireEvent.click(screen.getByRole('button', { name: ask.domain }));
  fireEvent.change(screen.getByPlaceholderText(STACK), { target: { value: ask.tech_stack } });
  fireEvent.click(screen.getByRole('button', { name: ask.scale }));
  fireEvent.click(screen.getByRole('button', { name: ask.deployment_target }));
  fireEvent.click(screen.getByRole('button', { name: ask.rigor }));
  fireEvent.click(screen.getByRole('button', { name: /Run DDPIE/ }));
}

const events = captured.design_dev.stream.split('\n').filter(l => l.startsWith('data: ') && l.slice(6).trim() !== '[DONE]')
  .map(l => JSON.parse(l.slice(6)) as Ev);
const stages = events.filter(ev => typeof ev.data?.stage_num === 'number');
const complete = events.find(ev => ev.stage === 'complete') as Ev;
const ranWith = `${captured.ask.tech_stack}·${captured.ask.scale}·${captured.ask.deployment_target}`;

describe('DesignDevEngine, rendered against its route\'s own stream', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('asks what was chosen, and shows the stream stage by stage, the count that ran the stream\'s own', async () => {
    serve({ status: 200, stream: captured.design_dev.stream });
    run();
    const ran = stages.filter(ev => !ev.data?.failed).length;
    expect(await screen.findByText(`Pipeline Output — ${ran} of 9 stages ran`)).toBeTruthy();
    expect(stages).toHaveLength(9);
    expect(asked).toEqual([captured.ask]);
    await waitFor(() => expect(screen.getByTestId('ddpie-ran-with').textContent).toBe(ranWith));
    //  the completion line is the stream's own, with the stack and scale the server ran
    await waitFor(() => expect(screen.getByText('Design & Development Pipeline Finished').textContent)
      .toBe('Design & Development Pipeline Finished'));
    expect(screen.getByText(complete.content)).toBeTruthy();
    expect(screen.getByText(`Stack: ${captured.ask.tech_stack}`)).toBeTruthy();
    expect(screen.getByText(`Scale: ${captured.ask.scale}`)).toBeTruthy();
  });

  it('a change to the form after a run leaves the run\'s output saying what it was run with', async () => {
    serve({ status: 200, stream: captured.design_dev.stream });
    run();
    await waitFor(() => expect(screen.getByTestId('ddpie-ran-with').textContent).toBe(ranWith));
    fireEvent.change(screen.getByPlaceholderText(STACK), { target: { value: 'W1037 changed after the run: Rust / Axum' } });
    fireEvent.click(screen.getByRole('button', { name: 'startup' }));
    fireEvent.click(screen.getByRole('button', { name: 'edge' }));
    expect(screen.getByText('→ W1037 changed after the run: Rust / Axum')).toBeTruthy();
    expect(screen.getByTestId('ddpie-ran-with').textContent).toBe(ranWith);
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, body: captured.refused.body });
    run();
    expect(await screen.findByText('Failed (HTTP 422): system: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, unreachable: true });
    run();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });
});
