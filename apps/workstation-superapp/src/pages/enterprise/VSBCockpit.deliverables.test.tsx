// W1050 (FU-399 part 69) — the cockpit's deliverables tab, rendered against its routes' own answers.
//
// The tab lists an entity's outputs and produces one from a brief. This mounts the real cockpit on the tab against what
// each route answered for an entity established through Genesis on a fresh store with no model installed
// (VSBCockpit.deliverables.fixture.json, captured by w1050_capture.py: every read on opening, a report produced from a
// made-up brief, the list read again after it, and the list route's own 500). Rendering found three defects, fixed in
// this round: a failed read of the list was said as a list of none; a failed production was said in the cockpit's
// one action line, away from its button; and a title taken from a brief was cut mid-word with nothing to say so.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.deliverables.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const LIST = `/api/v1/deliverables?vsb_id=${VID}`;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  each read as its route answered it; the list is the one read after a production once one is answered
function serve(o: { listFailed?: boolean; produce?: ('answered' | 'unreachable')[] } = {}) {
  const produce = [...(o.produce ?? ['answered'])];
  let produced = false;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = key === LIST && o.listFailed ? captured.list_failed
      : key === LIST && produced ? captured.after
      : answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/deliverables/produce') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (produce.shift() === 'unreachable') throw unreached();
    produced = true;
    return { status: captured.produced.status, data: captured.produced.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return post;
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit?tab=deliverables']}><VSBCockpit /></MemoryRouter>);
const outputs = () => screen.getByText(/^Outputs \(/).textContent;

describe('VSBCockpit\'s deliverables tab, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('produces what the brief asks, and lists it under a title cut between words', async () => {
    const post = serve();
    mount();
    await waitFor(() => expect(outputs()).toBe('Outputs (0)'));
    fireEvent.change(screen.getByPlaceholderText('Brief — what should it cover?'), { target: { value: captured.ask.brief } });
    fireEvent.click(screen.getByRole('button', { name: /^Produce$/ }));
    await waitFor(() => expect(outputs()).toBe('Outputs (1)'));
    expect(post).toHaveBeenCalledWith('/api/v1/deliverables/produce', captured.ask);
    const title = (captured.after.body as { deliverables: { title: string }[] }).deliverables[0].title;
    expect(title.endsWith('…')).toBe(true);
    expect(await screen.findByText(title)).toBeTruthy();
  });

  it('a failed read of the list is said as unread, never as none', async () => {
    serve({ listFailed: true });
    mount();
    await waitFor(() => expect(screen.getByTestId('cockpit-deliverables-unread').textContent).toBe(
      `This entity's deliverables could not be read, so the list is not what is there: Failed (HTTP 500): ${captured.list_failed.body.detail}`));
    expect(outputs()).toBe('Outputs (not read)');
    expect(screen.queryByText(/^No deliverables yet/)).toBeNull();
  });

  it('a production that reached no server is said beside its button, and cleared when it is pressed again', async () => {
    serve({ produce: ['unreachable', 'answered'] });
    mount();
    await waitFor(() => expect(outputs()).toBe('Outputs (0)'));
    fireEvent.change(screen.getByPlaceholderText('Brief — what should it cover?'), { target: { value: captured.ask.brief } });
    fireEvent.click(screen.getByRole('button', { name: /^Produce$/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-deliverable-error').textContent).toBe('Produce failed: Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: /^Produce$/ }));
    await waitFor(() => expect(outputs()).toBe('Outputs (1)'));
    expect(screen.queryByTestId('cockpit-deliverable-error')).toBeNull();
  });
});
