// W1076 (FU-399 part 88) — the avatar session, rendered against its routes' own answers.
//
// The avatar session (useAvatarSession) is the one conversation the shell's footer, its header and its voice
// controls share. This mounts it with the footer's real conversation panel, voice controls and avatar against what
// each route answered on a fresh store with no model installed (useAvatarSession.fixture.json, captured by
// w1076_capture.py; every message, entity name and mission made up). Rendering found: a reply that did not come
// said in the avatar's own voice; a second message sent with Enter while the first was answered; a cleared
// conversation's late reply said in the new one, and its session continued; the person's entity read once per page
// load, so a newer entity was never the one grounded; the previous person's conversation left on screen after a
// change of who is signed in; a voice message sent as the session stood when the recording started; and the rewind
// offered for a reply the browser spoke. Fixed here.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './useAvatarSession.fixture.json';
import { useAvatarSession } from './useAvatarSession';
import { AvatarWidget } from '../components/avatar/AvatarWidget';
import { ConversationPanel } from '../components/avatar/ConversationPanel';
import { VoiceVisualizer } from '../components/avatar/VoiceVisualizer';
import { clearToken } from '../lib/auth';

type Answer = { status: number; body: any };
type Held = { answer: Answer; held: Promise<void>; letGo: () => void };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  an answer the test lets go when it chooses
function hold(answer: Answer): Held {
  let letGo: () => void = () => undefined;
  const held = new Promise<void>(go => { letGo = go; });
  return { answer, held, letGo: () => letGo() };
}

//  the footer as the shell lays it out: one session, three views of it
function Footer() {
  const avatar = useAvatarSession();
  return (<>
    <ConversationPanel avatar={avatar} />
    <VoiceVisualizer avatar={avatar} />
    <AvatarWidget avatar={avatar} />
  </>);
}

//  the chat's answers in the order messages are sent (a held one waits until it is let go); the entities as the
//  listing stands when it is read
function serve(chats: (Answer | Held)[], listing: { now: Answer }) {
  const sent: any[] = [];
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/avatar/status') return { status: captured.status.status, data: captured.status.body };
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string, body?: any) => {
    if (url !== '/api/v1/avatar/chat') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    sent.push(body);
    const x = chats.shift();
    if (!x) throw axiosRefusal(500, { detail: 'no answer was planned for this message' });
    let a: Answer;
    if ('letGo' in x) { await x.held; a = x.answer; } else a = x;
    if (a.status >= 400) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const closed = vi.spyOn(axios, 'delete').mockImplementation(async () => ({ status: captured.deleted.status, data: captured.deleted.body }));
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const a: Answer = url === '/api/v1/vsb' ? listing.now : { status: 404, body: { detail: `not served here: ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return { sent, closed };
}

const mount = () => render(<MemoryRouter initialEntries={['/']}><Footer /></MemoryRouter>);
const box = () => screen.getByPlaceholderText('Message the avatar…') as HTMLTextAreaElement;
async function say(text: string) {
  fireEvent.change(box(), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: 'Send message to avatar' }));
}
const replies = () => screen.queryAllByText('Avatar').length;
const sid1 = captured.reply_1.body.session_id;

describe('useAvatarSession, rendered against its routes\' own answers (made-up messages and entities)', () => {
  beforeEach(() => {
    Element.prototype.scrollIntoView = vi.fn();   // jsdom lays nothing out
  });
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    delete (window as any).SpeechRecognition;
    delete (window as any).speechSynthesis;
    delete (window as any).SpeechSynthesisUtterance;
    localStorage.clear();
  });

  it('grounds each message in the person\'s most recent entity as listed when it is sent, on the session the first opened', async () => {
    const listing = { now: captured.vsb_one as Answer };
    const { sent } = serve([captured.reply_1, captured.reply_2], listing);
    mount();
    await say(captured.ask_1.message);
    await waitFor(() => expect(replies()).toBe(1));
    expect(sent[0]).toEqual(captured.ask_1);
    expect(screen.getByTestId('avatar-grounded-in').textContent).toContain(captured.reply_1.body.grounded_in);
    listing.now = captured.vsb_two;   // a newer entity, listed first
    await say(captured.ask_2.message);
    await waitFor(() => expect(replies()).toBe(2));
    expect(sent[1]).toEqual(captured.ask_2);
  });

  it('says a reply that did not come as that, beside the input, never in the avatar\'s voice', async () => {
    serve([captured.not_theirs], { now: captured.vsb_none });
    mount();
    await say('W1076 made up: a question that is not answered');
    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe(`No reply came: ${captured.not_theirs.body.detail}`));
    expect(replies()).toBe(0);
  });

  it('answers one message at a time: Enter while one is answered sends nothing, and keeps the words', async () => {
    const first = hold(captured.reply_1);
    const { sent } = serve([first, captured.reply_2], { now: captured.vsb_one });
    mount();
    await say(captured.ask_1.message);
    await waitFor(() => expect(sent.length).toBe(1));
    fireEvent.change(box(), { target: { value: captured.ask_2.message } });
    fireEvent.keyDown(box(), { key: 'Enter' });
    await act(async () => { await new Promise(r => setTimeout(r, 20)); });
    expect(sent.length).toBe(1);
    expect(box().value).toBe(captured.ask_2.message);
    await act(async () => { first.letGo(); });
    await waitFor(() => expect(replies()).toBe(1));
    fireEvent.keyDown(box(), { key: 'Enter' });
    await waitFor(() => expect(sent.length).toBe(2));
    expect(sent[1].session_id).toBe(sid1);
  });

  it('drops a reply for a conversation cleared while it was on its way, and closes the session it opened', async () => {
    const first = hold(captured.reply_1);
    const { sent, closed } = serve([first, captured.reply_2], { now: captured.vsb_one });
    mount();
    await say(captured.ask_1.message);
    await waitFor(() => expect(sent.length).toBe(1));
    fireEvent.click(screen.getByRole('button', { name: 'Clear chat history' }));
    await act(async () => { first.letGo(); });
    await waitFor(() => expect(closed).toHaveBeenCalledWith(`/api/v1/avatar/session/${sid1}`));
    expect(replies()).toBe(0);
    await say(captured.ask_2.message);
    await waitFor(() => expect(sent.length).toBe(2));
    expect(sent[1].session_id).toBeNull();
  });

  it('sets the conversation aside when who is signed in changes', async () => {
    const { sent } = serve([captured.reply_1, captured.reply_2], { now: captured.vsb_one });
    mount();
    await say(captured.ask_1.message);
    await waitFor(() => expect(replies()).toBe(1));
    act(() => { clearToken(); });
    await waitFor(() => expect(replies()).toBe(0));
    expect(screen.queryByText(captured.ask_1.message)).toBeNull();
    await say(captured.ask_2.message);
    await waitFor(() => expect(sent.length).toBe(2));
    expect(sent[1].session_id).toBeNull();
  });

  it('sends a voice message on the session as it stands when the words are heard', async () => {
    const first = hold(captured.reply_1);
    const { sent } = serve([first, captured.reply_2], { now: captured.vsb_one });
    let heard: any = null;
    (window as any).SpeechRecognition = class {
      lang = ''; interimResults = false; maxAlternatives = 1;
      onresult: any = null; onerror: any = null; onend: any = null;
      constructor() { heard = this; }
      start() { /* the browser listens */ }
      stop() { this.onend?.(); }
    };
    mount();
    await say(captured.ask_1.message);
    await waitFor(() => expect(sent.length).toBe(1));
    fireEvent.click(screen.getByRole('button', { name: 'Start voice message to avatar' }));
    expect(heard).not.toBeNull();
    await act(async () => { first.letGo(); });
    await waitFor(() => expect(replies()).toBe(1));
    act(() => { heard.onresult({ results: [[{ transcript: captured.ask_2.message }]] }); });
    await waitFor(() => expect(sent.length).toBe(2));
    expect(sent[1].session_id).toBe(sid1);
    expect(sent[1].message).toBe(captured.ask_2.message);
  });

  it('offers the rewind only for a reply it can rewind, never for one the browser spoke', async () => {
    const spoken: string[] = [];
    (window as any).speechSynthesis = { speak: (u: { text: string }) => { spoken.push(u.text); }, cancel: () => undefined };
    (window as any).SpeechSynthesisUtterance = class { text: string; volume = 1; onend: any = null; onerror: any = null;
      constructor(t: string) { this.text = t; } };
    serve([captured.reply_1], { now: captured.vsb_one });
    mount();
    const rewind = screen.getByRole('button', { name: "Rewind avatar's last reply 5 seconds" }) as HTMLButtonElement;
    expect(rewind.disabled).toBe(true);
    fireEvent.click(screen.getByRole('button', { name: 'Enable spoken replies' }));
    await say(captured.ask_1.message);
    await waitFor(() => expect(spoken.length).toBe(1));
    expect(spoken[0]).toBe(captured.reply_1.body.response.slice(0, 1200));
    expect(rewind.disabled).toBe(true);
  });
});
