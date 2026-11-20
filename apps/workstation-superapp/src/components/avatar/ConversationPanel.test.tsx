// W1146 (FU-399 part 111, FU-1293) — THE FOOTER'S CONVERSATION PANEL, rendered against the avatar's own answers.
//
// Under each reply the panel says what the server could not do. The hook's rendered test (W1076) reads its grounding
// line and its send error; nothing read the rest. This mounts the real panel on the real hook, against what the avatar
// route answered for made-up messages (ConversationPanel.fixture.json, captured by w1146_capture.py): a reply from the
// structured floor, the same asked for in Arabic, with an image attached, with a saved profile, and with that profile's
// file cut short. Each line is read in the route's own words.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './ConversationPanel.fixture.json';
import { ConversationPanel } from './ConversationPanel';
import { useAvatarSession } from '../../hooks/useAvatarSession';
import { clearPrefs, setPrefs } from '../../lib/userPrefs';

type Answer = { status: number; body: any; request?: any };
const cases = (captured as any).cases as Record<string, { reply: Answer }>;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

function Footer() {
  const avatar = useAvatarSession();
  return <ConversationPanel avatar={avatar} />;
}
function Where() {
  return <p data-testid="where-now">{useLocation().pathname}</p>;
}

//  the avatar's status, its chat as it answered, and the person's entities as the hook reads them
function serve(reply: Answer) {
  const sent: any[] = [];
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/avatar/status') return { status: captured.status.status, data: captured.status.body };
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string, body?: any) => {
    if (url !== '/api/v1/avatar/chat') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    sent.push(body);
    return { status: reply.status, data: reply.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const a = url === '/api/v1/vsb' ? captured.vsb : { status: 404, body: { detail: `not served here: ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return sent;
}

const mount = () => render(
  <MemoryRouter initialEntries={['/']}><Footer /><Where /></MemoryRouter>);
async function say(text: string) {
  fireEvent.change(screen.getByPlaceholderText('Message the avatar…'), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: 'Send message to avatar' }));
}
const said = (id: string) => screen.getByTestId(id).textContent;

describe('ConversationPanel, what each reply could not do, rendered against the avatar\'s own answers', () => {
  beforeEach(() => {
    Element.prototype.scrollIntoView = vi.fn();   // jsdom lays nothing out
  });
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    clearPrefs();
  });

  it('a reply from the floor says the grounding it did not use, that it was not cleared, and the areas it matched', async () => {
    const c = cases.floor.reply;
    const b = c.body;
    const sent = serve(c);
    mount();
    await say(c.request.message);
    await waitFor(() => expect(said('avatar-grounding-unused')).toBe(`${b.grounded_in}: ${b.grounding_basis}`));
    expect(sent).toEqual([c.request]);
    expect(said('avatar-not-cleared')).toBe(`not cleared: ${b.clearance_reason}`);
    expect(said('suggested-areas-basis')).toBe(b.suggested_areas_basis);
    for (const a of b.suggested_areas) expect(screen.getByTitle(a.because).textContent).toBe(` ${a.label} →`);
    expect(screen.queryByTestId('image-not-read')).toBeNull();
    expect(screen.queryByTestId('language-not-honoured')).toBeNull();
    const plan = b.suggested_areas.find((a: any) => a.route === '/business-plan');
    fireEvent.click(screen.getByTitle(plan.because));
    await waitFor(() => expect(said('where-now')).toBe('/business-plan'));
  });

  it('a reply asked for in Arabic says the floor\'s own note on the language, with what to do', async () => {
    const c = cases.language.reply;
    setPrefs({ language: 'ar' });
    const sent = serve(c);
    mount();
    await say(c.request.message);
    await waitFor(() => expect(said('language-not-honoured')).toBe(c.body.language_note));
    expect(c.body.language).toBeNull();
    expect(sent).toEqual([c.request]);
  });

  it('an image no model could read is said with the route\'s measured reason, and the image went with the message', async () => {
    const c = cases.image.reply;
    const sent = serve(c);
    mount();
    const bytes = Uint8Array.from(atob(c.request.image_base64), ch => ch.charCodeAt(0));
    fireEvent.change(screen.getByLabelText('Attach image', { selector: 'input' }),
      { target: { files: [new File([bytes], 'pixel.png', { type: 'image/png' })] } });
    await waitFor(() => expect(screen.getByAltText('Pending attachment')).toBeTruthy());
    await say(c.request.message);
    await waitFor(() => expect(said('image-not-read')).toBe(
      `The image was received but not read, so this reply is not based on what is in it. ${c.body.image_refusal}`));
    expect(c.body.image_status).toBe('no_vision_model');
    expect(sent).toEqual([c.request]);
  });

  it('a saved profile the floor cannot use is said as not usable, never as no profile', async () => {
    const c = cases.profile.reply;
    serve(c);
    mount();
    await say(c.request.message);
    await waitFor(() => expect(said('profile-not-usable')).toBe(
      'profile: not usable by the floor — the structured floor answered this, and it does not read your profile. '
      + 'Set up the owned model and ask again.'));
    expect(c.body.profile_state).toBe('not_usable_by_floor');
    expect(screen.queryByTestId('profile-unreadable')).toBeNull();
  });

  it('a profile that could not be read is said with the route\'s reason', async () => {
    const c = cases.unreadable.reply;
    serve(c);
    mount();
    await say(c.request.message);
    await waitFor(() => expect(said('profile-unreadable')).toBe(`profile: NOT applied — ${c.body.profile_basis}.`));
    expect(c.body.profile_state).toBe('unreadable');
    expect(screen.queryByTestId('profile-not-usable')).toBeNull();
  });
});
