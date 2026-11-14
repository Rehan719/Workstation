// W1024 (FU-399 part 50) — the AI CEO chat, rendered against its route's own answers.
//
// The chat POSTs /api/v138/ceo/chat and reads its stream. Until now it was read only as source text. This mounts the
// real chat against the route's answers (CEOChat.fixture.json, captured on a fresh store with no model installed):
// the stream's frames for a made-up question, played back as a network delivers them, and two refusals the route
// gives before any stream, a scope nothing holds (404) and a request with no message (422).
//
// Rendering found two defects, fixed in this round:
// - a refusal was said as an unreachable server ("The AI backend is currently unreachable"), and the pill turned to
//   "AI Offline" over a server that had answered;
// - the avatar's colour said a mood read off the person's own words ("fail" turned it frustrated red).
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './CEOChat.fixture.json';
import { CEOChat } from './CEOChat';

const CHAT = '/api/v138/ceo/chat';
type Reply = { stream?: string; status?: number; body?: unknown; unreachable?: boolean };

//  the captured stream, played back in two pieces cut mid-frame, as a network delivers it
function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({ start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); } });
}

//  the answer's text, read as the SSE protocol gives it: each frame's content, in order
function framesText(sse: string): string {
  return sse.split('\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)))
    .map(ev => String(ev.content ?? '')).join('');
}

function serve(reply: Reply) {
  const f = vi.fn(async (url: string) => {
    if (url !== CHAT) return { ok: false, status: 404, body: null, json: async () => ({ detail: `not served here: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    if (reply.stream !== undefined) return { ok: true, status: 200, body: streamOf(reply.stream), json: async () => ({}) };
    return { ok: false, status: reply.status, body: null, json: async () => reply.body };
  });
  vi.stubGlobal('fetch', f);
  return f;
}

function ask(text: string) {
  render(<MemoryRouter><CEOChat /></MemoryRouter>);
  fireEvent.change(screen.getByPlaceholderText('Ask the AI CEO — priorities, the plan, the C-Suite…'), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: 'Send message' }));
}

describe('CEOChat, rendered against its route', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('says the streamed answer whole, under the badge of what served it', async () => {
    serve({ stream: captured.stream });
    ask(captured.ask);
    const said = framesText(captured.stream);
    await waitFor(() => expect(screen.getAllByText((_, el) => el?.tagName === 'DIV' && el.textContent === said).length).toBe(1));
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    expect(screen.queryByText('AI Offline')).toBeNull();
  });

  it('says a refusal by its status and reason, and does not say the AI is offline over it', async () => {
    serve({ status: captured.scope_refused.status, body: captured.scope_refused.body });
    ask(captured.ask);
    await waitFor(() => expect(screen.getByText(`Not answered. Failed (HTTP 404): ${captured.scope_refused.body.detail}`)).toBeTruthy());
    expect(screen.queryByText(/currently unreachable/)).toBeNull();
    expect(screen.queryByText('AI Offline')).toBeNull();
  });

  it('says a field check by its field', async () => {
    serve({ status: captured.field_refused.status, body: captured.field_refused.body });
    ask(captured.ask);
    await waitFor(() => expect(screen.getByText('Not answered. Failed (HTTP 422): message: Field required')).toBeTruthy());
  });

  it('says a server it could not reach as one, and only then says the AI is offline', async () => {
    serve({ unreachable: true });
    ask(captured.ask);
    await waitFor(() => expect(screen.getByText(/The AI backend is currently unreachable/)).toBeTruthy());
    expect(screen.getByText('AI Offline')).toBeTruthy();
  });

  it('keeps the avatar one colour, whatever words the person uses', async () => {
    serve({ stream: captured.stream });
    ask('W1024 made up: why did the van booking fail? It is great otherwise.');
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    const icon = screen.getByTestId('ceo-avatar').querySelector('svg') as SVGElement;
    expect(icon.getAttribute('class')).toContain('text-aura');
    expect(icon.getAttribute('class')).not.toMatch(/text-(vital|emerald-400|highlight)/);
  });
});
