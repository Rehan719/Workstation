// W1041 (FU-399 part 62) — the Synthesis Nexus, rendered against its route's own stream.
//
// The Nexus runs four layers over a challenge, each passed to the next: the six cognitive lenses (one prompt), MJM (one
// prompt), a primary engine (one prompt per stage) chosen by a model or defaulted, and a synthesis (one prompt). This
// mounts the real page against what its route streamed on a fresh store with no model installed
// (SynthesisNexus.fixture.json, captured by w1041_capture.py: Auto, so no model chose the engine and BDP ran by default,
// and the route's refusal of a request with no challenge), played back as a stream, and has the server be unreachable.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './SynthesisNexus.fixture.json';
import { SynthesisNexus } from './SynthesisNexus';

type Reply = { status: number; body?: unknown; stream?: string; unreachable?: boolean };
type Ev = { stage: string; label: string; content: string; data?: Record<string, any> };
const ROUTE = '/api/v1/intelligence/nexus';

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

//  the page asks what the capture asked: its challenge, domain and activity (Auto, the page's own default)
function run() {
  render(<SynthesisNexus />);
  fireEvent.change(screen.getByPlaceholderText(/^Describe what you want to synthesise/), { target: { value: captured.ask.challenge } });
  fireEvent.click(screen.getByRole('button', { name: captured.ask.domain }));
  fireEvent.click(screen.getByRole('button', { name: /Activate Synthesis Nexus/ }));
}

const events = captured.nexus.stream.split('\n').filter(l => l.startsWith('data: ') && l.slice(6).trim() !== '[DONE]')
  .map(l => JSON.parse(l.slice(6)) as Ev);
const engineStages = events.filter(ev => typeof ev.data?.stage_num === 'number');
const selected = events.find(ev => ev.stage === 'engine_selected') as Ev;
const cognitive = events.find(ev => ev.stage === 'cognitive_complete') as Ev;
const mjm = events.find(ev => ev.stage === 'mjm_complete') as Ev;
const nexus = events.find(ev => ev.stage === 'nexus_complete') as Ev;

//  a layer's text as its open card shows it: the paragraph whose text is the layer's, line breaks and all
const shown = (content: string) => screen.queryAllByText((_, el) => el?.tagName === 'P' && el.textContent === content);

describe('SynthesisNexus, rendered against its route\'s own stream', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('asks what was chosen, and streams the four layers, the engine stages counted from the stream', async () => {
    serve({ status: 200, stream: captured.nexus.stream });
    run();
    const ran = engineStages.filter(ev => !ev.data?.failed).length;
    expect(await screen.findByText(`Layer 3 · BDP Pipeline — ${ran} of ${engineStages.length} stages ran`)).toBeTruthy();
    expect(asked).toEqual([captured.ask]);
    expect(engineStages).toHaveLength(8);
    await waitFor(() => expect(screen.getByText(/^Layer 4 · one prompt/).textContent).toContain('layers ran'));
    expect(screen.getByText(/^Layer 4 · one prompt/).textContent)
      .toContain(`${nexus.data?.layers_completed} of ${nexus.data?.layers_total} layers ran`);
  });

  it('says that no model chose the engine, and why, in words that read as a sentence', async () => {
    serve({ status: 200, stream: captured.nexus.stream });
    run();
    await waitFor(() => expect(screen.getByText(/^Not selected: defaulted to/).textContent)
      .toBe(`Not selected: defaulted to BDP because ${selected.data?.decision?.reason}`));
  });

  it('says the engine a model chose, and its reason, in words that read as a sentence', async () => {
    //  written here: with no model installed the route never decides, so the captured stream's choice is re-said as
    //  one a model made, the rest of the stream as captured
    const decided = captured.nexus.stream.split('\n').map(l => {
      if (!l.startsWith('data: ') || l.slice(6).trim() === '[DONE]') return l;
      const ev = JSON.parse(l.slice(6)) as Ev;
      if (ev.stage !== 'engine_selected') return l;
      return `data: ${JSON.stringify({ ...ev, data: { ...ev.data, decision: { decided: true, by: 'gateway', reason: 'W1041 made up: the challenge reads as a venture' } } })}`;
    }).join('\n');
    serve({ status: 200, stream: decided });
    run();
    await waitFor(() => expect(screen.getByText(/^Primary engine:/).textContent)
      .toBe('Primary engine: BDP (W1041 made up: the challenge reads as a venture)'));
  });

  it('opens each layer\'s card to that layer\'s own text, one at a time', async () => {
    serve({ status: 200, stream: captured.nexus.stream });
    run();
    await waitFor(() => expect(screen.getByText(/^Layer 4 · one prompt/).textContent).toContain('layers ran'));
    expect(shown(cognitive.content)).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: /^Cognitive Lenses/ }));
    expect(shown(cognitive.content)).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: /^MJM Meta-Assessment/ }));
    expect(shown(mjm.content)).toHaveLength(1);
    expect(shown(cognitive.content)).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${engineStages[0].label}`) }));
    expect(shown(engineStages[0].content)).toHaveLength(1);
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
});
