// W1056 (FU-399 part 74) — the cockpit's organisation tab, rendered against its routes' own answers.
//
// The tab lists the sections of an entity's body that are not written, each with a box for the founder's own words,
// and edits the entity's delivery cascade. This mounts the real cockpit on the tab against what each route answered
// for two entities established through Genesis on a fresh store with no model installed (VSBCockpit.org.fixture.json,
// captured by w1056_capture.py: every read on opening either, each one's cascade as the editor reads it, the opened
// entity's cascade saved with one instruction edited and a section written in its founder's words, the route's
// refusal of a section too short to be one, and the cascade route's refusals for a cascade it does not hold).
// Rendering found the cascade editor bound to no entity: opened on one entity, it stayed open with that entity's
// stages when another was opened, and its Save then wrote them over the other entity's cascade; and its failures were
// said as a bare reason, with nothing to say whether the cascade had not been read or not been saved. Fixed here.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.org.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
type Swarm = { cascade_id: string; name: string };
type Stage = { role: string; instruction: string };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const OTHER = captured.other_id;
const NOT_HELD = 'swarm-w1056-not-held';
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const swarmOf = (id: string) => (answers[`/api/v1/vsb/${id}`].body as { native_swarm: Swarm }).native_swarm;
const stagesOf = (cid: string) => (answers[`/api/v1/resources/swarm/${cid}`].body as { stages: Stage[] }).stages;

//  each read as its route answered it, the opened entity's record the one after a save once one is answered (re-said
//  here, when asked, as naming a cascade the store does not hold); the section route and the cascade route as they
//  answered, a save that reached no server when asked. What was put to the cascade route is kept.
function serve(o: { notHeld?: boolean; save?: 'answered' | 'unreachable' } = {}) {
  let after: Answer | null = null;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    let a = key === `/api/v1/vsb/${VID}` && after ? after : answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (key === `/api/v1/vsb/${VID}` && o.notHeld) {
      //  written here: the record re-said as naming a cascade the store does not hold
      const body = a.body as { native_swarm: Swarm };
      a = { ...a, body: { ...body, native_swarm: { ...body.native_swarm, cascade_id: NOT_HELD } } };
    }
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url === `/api/v1/vsb/${VID}/body/design`) { after = captured.after_body; return { status: captured.body_saved.status, data: captured.body_saved.body }; }
    if (url === `/api/v1/vsb/${VID}/body/operations`) throw axiosRefusal(captured.body_refused.status, captured.body_refused.body);
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  const puts: { url: string; body: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string; body?: string }) => {
    const answer = (a: Answer) => ({ ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body });
    if (init?.method === 'PUT') {
      puts.push({ url, body: JSON.parse(String(init.body)) });
      if (o.save === 'unreachable') throw new TypeError('Failed to fetch');
      after = captured.after_save;
      return answer(captured.saved);
    }
    if (url === `/api/v1/resources/swarm/${NOT_HELD}`) return answer(captured.read_refused);
    return answer(answers[url] ?? { status: 404, body: { detail: `not served here: ${url}` } });
  }));
  return { puts };
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit']}><VSBCockpit /></MemoryRouter>);
const open = (id: string) => fireEvent.change(screen.getByLabelText('Select VSB'), { target: { value: id } });
const instructions = () => screen.getAllByPlaceholderText('instruction') as HTMLInputElement[];
const editFirst = (value: string) => fireEvent.change(instructions()[0], { target: { value } });

describe('VSBCockpit\'s organisation tab, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('records a section in the founder\'s own words, and then lists only what is left', async () => {
    serve();
    mount();
    fireEvent.change(await screen.findByLabelText('Your own words for design'), { target: { value: captured.body_ask.text } });
    fireEvent.click(screen.getByRole('button', { name: 'Record my design' }));
    const b = captured.body_saved.body as { status: string; status_basis: string };
    await waitFor(() => expect(screen.getByTestId('cockpit-body-message').textContent).toBe(
      `design: recorded as your own words. The entity now reads "${b.status}" — ${b.status_basis}.`));
    await waitFor(() => expect(screen.queryByLabelText('Your own words for design')).toBeNull());
    expect(screen.getByLabelText('Your own words for operations')).toBeTruthy();
  });

  it('a section the route refuses says it was not recorded, and the route\'s reason', async () => {
    serve();
    mount();
    fireEvent.change(await screen.findByLabelText('Your own words for operations'), { target: { value: 'seeds' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record my operations' }));
    await waitFor(() => expect(screen.getByTestId('cockpit-body-message').textContent).toBe(
      `operations: NOT recorded — ${String((captured.body_refused.body as { detail: string }).detail)}`));
  });

  it('the cascade editor reads the entity\'s own cascade, and saves an edit to it as the route was asked', async () => {
    const { puts } = serve({ save: 'answered' });
    mount();
    fireEvent.click(await screen.findByTestId('cascade-edit-open'));
    await waitFor(() => expect(instructions()[0].value).toBe(stagesOf(captured.cascade_id)[0].instruction));
    editFirst(captured.save_ask.stages[0].instruction);
    fireEvent.click(screen.getByTestId('cascade-edit-save'));
    await waitFor(() => expect(screen.getByTestId('cascade-edit-saved').textContent).toBe(
      `Saved ${(captured.saved.body as { stages: Stage[] }).stages.length} stages. The next run of this cascade re-reads them — nothing further to apply.`));
    expect(puts).toEqual([{ url: `/api/v1/resources/swarm/${captured.cascade_id}`, body: captured.save_ask }]);
  });

  it('an open editor closes when another entity is opened, so one entity\'s stages are never saved over another\'s', async () => {
    const { puts } = serve({ save: 'answered' });
    mount();
    fireEvent.click(await screen.findByTestId('cascade-edit-open'));
    await waitFor(() => expect(instructions()[0].value).toBe(stagesOf(captured.cascade_id)[0].instruction));
    editFirst(captured.save_ask.stages[0].instruction);
    open(OTHER);
    await waitFor(() => expect(screen.getByTestId('vsb-swarm-template-note').textContent).toContain(swarmOf(OTHER).name));
    expect(screen.queryByTestId('cascade-edit')).toBeNull();
    //  opened again, it reads the other entity's own cascade
    fireEvent.click(screen.getByTestId('cascade-edit-open'));
    await waitFor(() => expect(instructions()[0].value).toBe(stagesOf(swarmOf(OTHER).cascade_id)[0].instruction));
    expect(puts).toEqual([]);
  });

  it('a cascade that could not be read or could not be saved says which, and why', async () => {
    serve({ notHeld: true });
    const { unmount } = mount();
    fireEvent.click(await screen.findByTestId('cascade-edit-open'));
    await waitFor(() => expect(screen.getByTestId('cascade-edit-error').textContent).toBe(
      `The cascade could not be read: ${String((captured.read_refused.body as { detail: string }).detail)}`));
    unmount();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    serve({ save: 'unreachable' });
    mount();
    fireEvent.click(await screen.findByTestId('cascade-edit-open'));
    await waitFor(() => expect(instructions()[0].value).toBe(stagesOf(captured.cascade_id)[0].instruction));
    fireEvent.click(screen.getByTestId('cascade-edit-save'));
    await waitFor(() => expect(screen.getByTestId('cascade-edit-error').textContent).toBe('The cascade was not saved: Failed — backend unreachable.'));
  });
});
