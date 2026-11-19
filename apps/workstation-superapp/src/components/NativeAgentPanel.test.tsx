// W1064 (FU-399 part 78) — the shell's in-house assistant, rendered against its routes' own answers.
//
// The panel in the shell's fourth column reads which owned model resources exist and sends the conversation, flattened
// into one prompt, to the native orchestrator; every reply is stamped with the resource that served it. This mounts the
// real panel against what each route answered on a fresh store with no model installed (NativeAgentPanel.fixture.json,
// captured by w1064_capture.py: the owned model list, a first message and a second turn, each asked exactly as the
// panel builds it, and the model list's own 500). Rendering found a reply, and a failure, that came back after the
// conversation was cleared said in the cleared conversation, under no question. Fixed in this round.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import captured from './NativeAgentPanel.fixture.json';
import { NativeAgentPanel } from './NativeAgentPanel';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const MODELS = '/api/v1/native-ai/models';
const COMPLETE = '/api/v1/native-ai/complete';
const FIRST = captured.first_reply.body;
const SECOND = captured.second_reply.body;

//  each route as it answered; each completion asked takes the next answer in `replies`
function serve(plan: { models?: Reply; replies?: Reply[] } = {}) {
  const replies = [...(plan.replies ?? [captured.first_reply, captured.second_reply])];
  const asked: unknown[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    let r: Reply;
    if (url === MODELS) r = plan.models ?? captured.models;
    else if (url === COMPLETE && init?.method === 'POST') {
      asked.push(JSON.parse(String(init.body)));
      r = replies.length > 1 ? replies.shift()! : replies[0];
    } else r = { status: 404, body: { detail: `not served here: ${url}` } };
    const a = await r;
    if (a === 'unreachable') throw new TypeError('Failed to fetch');
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return asked;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const mount = () => render(<NativeAgentPanel />);
const box = () => screen.getByPlaceholderText('Ask the in-house assistant… (Enter to send)');
function say(text: string) {
  fireEvent.change(box(), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: 'Send message' }));
}
const stamps = () => screen.queryAllByText(/^served by /).map(s => s.textContent);

describe('NativeAgentPanel, rendered against its routes\' own answers', () => {
  beforeAll(() => {
    //  jsdom has no layout: the panel scrolls its last message into view
    Element.prototype.scrollIntoView = () => undefined;
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('offers only the owned resources the route lists, and says no local model is installed', async () => {
    serve();
    mount();
    const tiers = captured.models.body.tiers;
    await waitFor(() => expect((screen.getByLabelText('Owned model resource') as HTMLSelectElement).disabled).toBe(false));
    expect(screen.getAllByRole('option').map(o => o.textContent)).toEqual(tiers.map(t => t.label));
    expect(captured.models.body.local_models).toEqual([]);
    expect(screen.getByText('No local model is installed on this host — answers come from the deterministic native floor.')).toBeTruthy();
  });

  it('says a model list it could not read with the route\'s reason', async () => {
    serve({ models: captured.models_failed });
    mount();
    await waitFor(() => expect(screen.getByText(
      `Could not read the owned model list: Failed (HTTP 500): ${captured.models_failed.body.detail}`)).toBeTruthy());
  });

  it('asks what the person said, with the conversation so far, and stamps each reply with what served it', async () => {
    const asked = serve();
    mount();
    await waitFor(() => expect((screen.getByLabelText('Owned model resource') as HTMLSelectElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole('button', { name: captured.first }));
    expect((box() as HTMLTextAreaElement).value).toBe(captured.first);
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }));
    await waitFor(() => expect(screen.getByText(FIRST.output, { normalizer: s => s })).toBeTruthy());
    expect(stamps()).toEqual([`served by ${FIRST.served_by}`]);
    say(captured.second);
    await waitFor(() => expect(stamps()).toHaveLength(2));
    expect(stamps()).toEqual([`served by ${FIRST.served_by}`, `served by ${SECOND.served_by}`]);
    expect(asked).toEqual([captured.ask_first, captured.ask_second]);
  });

  it('says a message that reached no server as a failure, never as a reply', async () => {
    serve({ replies: ['unreachable'] });
    mount();
    say(captured.first);
    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe('Failed — backend unreachable.'));
    expect(stamps()).toEqual([]);
    expect(screen.getByText(captured.first)).toBeTruthy();
  });

  it('never says a reply, or a failure, that comes after the conversation was cleared', async () => {
    for (const late of [captured.first_reply, 'unreachable' as const]) {
      const reply = held(late);
      serve({ replies: [reply.reply] });
      const { unmount } = mount();
      say(captured.first);
      await waitFor(() => expect(screen.getByRole('button', { name: 'Clear conversation' })).toBeTruthy());
      fireEvent.click(screen.getByRole('button', { name: 'Clear conversation' }));
      await act(async () => { reply.letGo(); });
      await act(async () => { await Promise.resolve(); });
      expect(stamps()).toEqual([]);
      expect(screen.queryByRole('alert')).toBeNull();
      expect(screen.queryAllByText('You')).toHaveLength(0);
      //  and the cleared conversation is ready to be asked again: nothing is left being answered
      expect(screen.queryByText('thinking')).toBeNull();
      unmount();
      vi.unstubAllGlobals();
    }
  });
});
