// W1055 (FU-399 part 73) — the cockpit's chief tab, rendered against its routes' own answers.
//
// The tab shows an entity's review gates, assembles its Board Pack and reads the pack's history, and passes an
// instruction to the entity's Chief. This mounts the real cockpit on the tab against what each route answered for two
// entities established through Genesis on a fresh store with no model installed (VSBCockpit.chief.fixture.json,
// captured by w1055_capture.py: every read on opening either, the Board Pack assembled for the one the cockpit opens
// on and the pack's reads after it, and that entity's Chief instructed with a made-up instruction as the tab sends
// it). Rendering found the Chief's answer tied to no entity: an answer that came after another entity was opened was
// said under that entity's Chief, and an answer or a failure stood under every entity opened after it; and a failure
// was said with nothing to say what had failed. Fixed in this round.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.chief.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const OTHER = captured.other_id;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });
type Outcome = 'answered' | 'refused' | 'unreachable' | 'held';

//  each read as its route answered it, the pack's two the ones after an assembly once one is answered; each press of
//  the Chief's button answered in turn. 'held' keeps the answer back until the test lets it go.
function serve(o: { instruct?: Outcome[] } = {}) {
  let assembled = false;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = assembled && key === `/api/v1/vsb/${VID}/board-packs` ? captured.packs_after
      : assembled && key === `/api/v1/vsb/${VID}/board-pack` ? captured.pack_after
      : answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const instruct = [...(o.instruct ?? [])];
  let letGo: () => void = () => undefined;
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url === `/api/v1/vsb/${VID}/board-pack`) { assembled = true; return { status: captured.assembled.status, data: captured.assembled.body }; }
    if (url !== '/api/v1/board/chief/instruct') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    const x = instruct.shift();
    if (x === 'unreachable') throw unreached();
    if (x === 'refused') throw axiosRefusal(captured.instruct_refused.status, captured.instruct_refused.body);
    if (x === 'held') await new Promise<void>(go => { letGo = go; });
    return { status: captured.instructed.status, data: captured.instructed.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return { post, letGo: () => letGo() };
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit?tab=chief']}><VSBCockpit /></MemoryRouter>);
const box = () => screen.getByPlaceholderText(/^Give the Chief an instruction/) as HTMLTextAreaElement;
const issue = () => screen.getByRole('button', { name: /Issue instruction/ });
const instruct = () => {
  fireEvent.change(box(), { target: { value: captured.ask.instruction } });
  fireEvent.click(issue());
};
const open = (id: string) => fireEvent.change(screen.getByLabelText('Select VSB'), { target: { value: id } });
const said = (b: unknown, k: string) => String((b as Record<string, unknown>)[k]);

describe('VSBCockpit\'s chief tab, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('assembles the Board Pack as the tab asks for it, and its history then holds the one assembly', async () => {
    const { post } = serve();
    mount();
    await waitFor(() => expect(screen.getByTestId('cockpit-pack-none').textContent).toBe('No board pack has been assembled for this entity.'));
    expect(screen.queryByTestId('cockpit-pack-message')).toBeNull();   // the 404 is "none assembled yet", not a failure
    fireEvent.click(screen.getByTestId('cockpit-pack-assemble'));
    const pack = captured.assembled.body as { version: number; generated_at: string };
    await waitFor(() => expect(screen.getByTestId('cockpit-pack-latest').textContent).toContain(
      `Version ${pack.version} · assembled ${pack.generated_at}`));
    await waitFor(() => expect(screen.getByTestId('cockpit-pack-history').textContent).toMatch(/^History — 1 assembly, 1 distinct ve/));
    expect(post).toHaveBeenCalledWith(`/api/v1/vsb/${VID}/board-pack`);
  });

  it('instructs the Chief as the tab sends it, and says what composed the answer', async () => {
    const { post } = serve({ instruct: ['answered'] });
    mount();
    await screen.findByTestId('cockpit-pack-none');
    instruct();
    const b = captured.instructed.body;
    await waitFor(() => expect(screen.getByTestId('cockpit-objectives-fallback').textContent).toBe(
      'your instruction was recorded as ONE objective in place of a plan'));
    expect(post).toHaveBeenCalledWith('/api/v1/board/chief/instruct', captured.ask);
    expect(screen.getByTestId('cockpit-directive-reason').textContent).toBe(said(b, 'directive_reason'));
    expect(screen.getByTestId('cockpit-ceo-plan-reason').textContent).toBe(said(b, 'ceo_plan_reason'));
    expect(box().value).toBe('');
  });

  it('an instruction that reached no server or was refused says it was not passed, and why', async () => {
    serve({ instruct: ['unreachable', 'refused'] });
    mount();
    await screen.findByTestId('cockpit-pack-none');
    instruct();
    await waitFor(() => expect(screen.getByTestId('cockpit-chief-error').textContent).toBe('Not instructed: Failed — backend unreachable.'));
    fireEvent.click(issue());
    await waitFor(() => expect(screen.getByTestId('cockpit-chief-error').textContent).toBe('Not instructed: instruction: Field required'));
    expect(box().value).toBe(captured.ask.instruction);   // a failed instruction is kept to send again
  });

  it('the Chief\'s answer stays with the entity it was issued for, and nothing of it under another entity\'s Chief', async () => {
    const { letGo } = serve({ instruct: ['answered', 'held'] });
    mount();
    await screen.findByTestId('cockpit-pack-none');
    instruct();
    await screen.findByTestId('cockpit-objectives-fallback');
    //  another entity opened: the first's answer is not said under its Chief
    open(OTHER);
    await waitFor(() => expect(screen.getByRole('heading', { name: /Instruct this entity's Chief/ })).toBeTruthy());
    await waitFor(() => expect(screen.queryByTestId('cockpit-objectives-fallback')).toBeNull());
    //  an answer that comes after another entity is opened is not said there; what was typed for the first is not
    //  left in the other's box, and the other's button is not left busy with the first's call
    open(VID);
    await screen.findByTestId('cockpit-pack-none');
    instruct();
    open(OTHER);
    await waitFor(() => expect(box().value).toBe(''));
    fireEvent.change(box(), { target: { value: 'W1055 made up: open on the first Saturday' } });
    expect((issue() as HTMLButtonElement).disabled).toBe(false);
    letGo();
    await new Promise(r => setTimeout(r, 50));
    expect(screen.queryByTestId('cockpit-objectives-fallback')).toBeNull();
    expect(box().value).toBe('W1055 made up: open on the first Saturday');
  });
});
