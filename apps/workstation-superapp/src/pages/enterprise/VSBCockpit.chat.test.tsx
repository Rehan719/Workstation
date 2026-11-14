// W1052 (FU-399 part 71) — the cockpit's chat tab, rendered against its routes' own answers.
//
// The tab puts a person's message to the entity's avatar. This mounts the real cockpit on the tab against what each
// route answered for an entity established through Genesis on a fresh store with no model installed
// (VSBCockpit.chat.fixture.json, captured by w1052_capture.py: every read on opening, the avatar's answer to a made-up
// message as the tab sends it, and the route's field check of a message left out). Rendering found a reply that did
// not come put into the conversation in the avatar's own voice, one fixed sentence whatever the failure was; it is
// said beside the input as what it was, fixed in this round.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.chat.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  each read as its route answered it; the chat's outcomes in the order messages are sent
function serve(chat: ('answered' | 'unreachable' | 'refused')[]) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/avatar/chat') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    const x = chat.shift();
    if (x === 'unreachable') throw unreached();
    if (x === 'refused') throw axiosRefusal(captured.refused.status, captured.refused.body);
    return { status: captured.answered.status, data: captured.answered.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return post;
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit?tab=chat']}><VSBCockpit /></MemoryRouter>);
async function say(text: string) {
  fireEvent.change(await screen.findByPlaceholderText('Ask about this enterprise…'), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: /^Send$/ }));
}

describe('VSBCockpit\'s chat tab, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('a message is put as the tab sends it, and the avatar\'s answer says what composed it', async () => {
    const post = serve(['answered']);
    mount();
    await say(captured.ask.message);
    expect(await screen.findByText('structured floor — not model analysis')).toBeTruthy();
    expect(post).toHaveBeenCalledWith('/api/v1/avatar/chat', captured.ask);
    expect(screen.queryByTestId('cockpit-chat-error')).toBeNull();
  });

  it('a reply that did not come is said beside the input as what it was, never in the avatar\'s voice', async () => {
    serve(['unreachable', 'refused', 'answered']);
    mount();
    await say(captured.ask.message);
    await waitFor(() => expect(screen.getByTestId('cockpit-chat-error').textContent).toBe('No reply came: Failed — backend unreachable.'));
    expect(screen.queryByText(/avatar is unavailable/)).toBeNull();
    await say(captured.ask.message);
    await waitFor(() => expect(screen.getByTestId('cockpit-chat-error').textContent).toBe('No reply came: Failed (HTTP 422): message: Field required'));
    //  and cleared when a message is answered
    await say(captured.ask.message);
    expect(await screen.findByText('structured floor — not model analysis')).toBeTruthy();
    expect(screen.queryByTestId('cockpit-chat-error')).toBeNull();
  });
});
