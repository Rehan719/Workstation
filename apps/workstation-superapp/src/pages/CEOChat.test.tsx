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
// W1238 - a reply is rendered as formatted text (components/RichText.tsx): the floor's reply shows its headings and
// list items with no markdown marker left, and the badge and the grounding chip are as they were.
// W1239 - with no model connected the route streams a fixed notice in place of the floor's frame (the fixture is
// recaptured from the patched route), and the greeting no longer says a record is held.
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
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

//  W1238 - the structured floor's reply as captured for W1024 (the earlier CEOChat.fixture.json), with the terminal
//  frame it came with: the chat renders it as formatted text, and the badge and the grounding chip are as they were
const FLOOR_REPLY = [
  '_[Workstation native structured engine — owned, no external dependency]_',
  '',
  "_Role the prompt asked for: AI CEO of this Workstation IDBO enterprise. The native floor takes no role - what follows is a frame, not that role's work._",
  '',
  '## Assessment',
  'Subject: W1024 made up: should the bakery cooperative buy a third van? (domain: WITHHELD — no domain was declared for this call).',
  'Structured frame over the terms most frequent in the request (a term count, not an analysis):',
  '- bakery cooperative', '- cooperative buy', '- buy third', '- third van', '- made',
  '',
  '## Priorities',
  "Native structured frame for 'Priorities' over: W1024 made up: should the bakery cooperative buy a third van? (domain: WITHHELD — no domain was declared for this call). The list below is the request's most frequent terms, not findings about them.",
  '- bakery cooperative', '- cooperative buy', '- buy third', '- third van', '- made',
  '',
  '## Next actions',
  '- Validate the structured outputs above against the stated objective.',
  '- Route richer generation to a model resource (local-first; external only if enabled).',
  "- Iterate via the orchestrator's cascade for WITHHELD — no domain was declared for this call; record outcomes to memory/UEG.",
].join('\n');
const FLOOR_DONE = {
  content: '', done: true, served_by: 'native', is_external: false, guardrail_passed: true, profile_applied: false,
  grounding: { scope: 'workstation', directives: 0, objectives: 0, plan_score: 0.3, debate_entries: 0,
    cited: { directives: 0, objectives: 0 },
    cited_basis: 'handed 0 directive(s) and 0 objective(s); the answer names 0 and 0 of them. A record handed in and not named was not answered from' },
  grounding_conflicts: [],
};
const FLOOR_STREAM = [FLOOR_REPLY.slice(0, 200), FLOOR_REPLY.slice(200, 700), FLOOR_REPLY.slice(700)]
  .map(c => `data: ${JSON.stringify({ content: c, done: false })}\n\n`).join('') + `data: ${JSON.stringify(FLOOR_DONE)}\n\n`;

//  W1238 - a line of the answer as the renderer shows it: its heading hashes, its list marker and a whole-line italic's
//  underscores are not shown
const shownLine = (line: string) => line.trim().replace(/^#{1,6} +/, '').replace(/^- /, '').replace(/^_(.*)_$/, '$1');
const lastMessage = () => screen.getAllByTestId('ceo-message').at(-1) as HTMLElement;

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
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    const lines = said.split('\n').filter(l => l.trim());
    expect(lines.length).toBeGreaterThan(0);
    for (const line of lines) expect(lastMessage().textContent).toContain(shownLine(line));
    expect(screen.queryByText('AI Offline')).toBeNull();
  });

  it('renders the floor\'s reply as formatted text: headings and list items, no marker left, the chips as they were', async () => {
    serve({ stream: FLOOR_STREAM });
    ask(captured.ask);
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    const box = lastMessage();
    expect(within(box).getAllByRole('heading').map(h => h.textContent)).toEqual(['Assessment', 'Priorities', 'Next actions']);
    expect(within(box).getAllByRole('list').length).toBe(3);
    expect(within(box).getAllByRole('listitem').length).toBe(13);
    expect(within(box).getByText('[Workstation native structured engine — owned, no external dependency]').tagName).toBe('EM');
    expect(box.textContent).not.toContain('##');
    expect(box.textContent).not.toContain('_[');
    for (const el of box.querySelectorAll('p, li, h3, h4, h5, h6')) expect(el.textContent?.startsWith('- ')).toBe(false);
    expect(screen.getByTestId('ceo-grounding-cited').textContent).toBe(
      'handed 0 directives · 0 objectives · the answer names 0 and 0 · scope workstation');
    expect(screen.queryAllByTestId('ceo-grounding-conflict')).toHaveLength(0);
  });

  it('says that no model is connected, and the greeting claims no record', async () => {
    serve({ stream: captured.stream });
    ask(captured.ask);
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    const box = lastMessage();
    expect(box.textContent).toContain('No AI model is connected on this server, so this is not an answer to your question.');
    expect(box.textContent).toContain('What the CEO holds from its records: none recorded on this server');
    expect(box.textContent).toContain('each is the Owner\'s decision');
    expect(box.textContent).not.toContain('Assessment');
    expect(box.textContent).not.toContain('WITHHELD');
    const greeting = screen.getAllByTestId('ceo-message')[0].textContent ?? '';
    expect(greeting).toContain('which on a new server may be nothing');
    expect(greeting).not.toContain('handed the record for this scope');
  });

  it('shows the person\'s own words as typed', async () => {
    serve({ stream: FLOOR_STREAM });
    ask('W1238 made up: ## not a heading - **not bold**');
    await waitFor(() => expect(screen.getAllByText('structured floor — not model analysis').length).toBeGreaterThan(0));
    const mine = screen.getAllByTestId('ceo-message').find(el => el.textContent === 'W1238 made up: ## not a heading - **not bold**');
    expect(mine).toBeTruthy();
    expect(within(mine as HTMLElement).queryByRole('heading')).toBeNull();
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
