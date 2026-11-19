// W1044 (FU-399 part 64) — the Projects hub, rendered against its routes' own answers.
//
// The hub lists projects, creates one, runs its stage as a stream and proposes its advance. This mounts the real page
// against what the routes answered on a fresh store with no model installed (ProjectsHub.fixture.json, captured by
// w1044_capture.py: a made-up project created on the subject and area the form opens on; its concept stage run, which
// the native engine composed; the proposal to advance it and the refusal of a second; and the list route's own 500
// when its read fails inside). Rendering found four defects, fixed in this round: the page rendered again without end
// while its list was unread, which here kept the list's own read from ever arriving, so every case hung; a failed read
// of the list was one fixed sentence asking whether the backend was running; three fallbacks said nothing of what
// happened, one of them that the project was not ready yet; and a run that completed was said as failed when the
// project could not be read again afterwards, the project marked as in error over a saved output.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ProjectsHub.fixture.json';
import { ProjectsHub } from './ProjectsHub';

type Answer = { status: number; body: unknown };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });
const PID = captured.created.body.id;
const answered = (a: Answer) => {
  if (a.status >= 400) throw axiosRefusal(a.status, a.body);
  return { status: a.status, data: a.body };
};

//  the stream as the route sent it, in two pieces cut mid-frame, as a network delivers it
function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({
    start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); },
  });
}

//  what the stream says, as its frames say it: the tokens joined, each escaped line break a line break
const streamed = captured.stream.text.split('\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)))
  .filter(f => f.token !== undefined).map(f => String(f.token).replace(/\\n/g, '\n')).join('');

type Serve = { list?: Answer; create?: 'unreachable'; reread?: 'unreachable'; propose?: 'unreachable' };

//  each route as it answered; a call that reaches no server is said as one
function serve(s: Serve = {}) {
  let proposals = 0;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/projects/') return answered(s.list ?? captured.empty);
    if (url === `/api/v1/projects/${PID}`) {
      if (s.reread === 'unreachable') throw unreached();
      return answered(proposals > 0 ? captured.waiting : captured.ran);
    }
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url === '/api/v1/projects/') {
      if (s.create === 'unreachable') throw unreached();
      return answered(captured.created);
    }
    if (url === `/api/v1/projects/${PID}/propose-advance`) {
      if (s.propose === 'unreachable') throw unreached();
      return answered(proposals++ === 0 ? captured.proposed : captured.again);
    }
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  const del = vi.spyOn(axios, 'delete').mockImplementation(async () => { throw unreached(); });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== `/api/v1/projects/${PID}/run`) return { ok: false, status: 404, statusText: '', body: null, json: async () => ({ detail: `not served: ${url}` }) };
    return { ok: true, status: captured.stream.status, statusText: '', body: streamOf(captured.stream.text) };
  }));
  return { post, del };
}

function mount() {
  //  retry is off, as the knowledge hub's test has it: a failed read is said at once rather than after the retry
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter>
        <ProjectsHub />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

//  the page asks what the capture asked: the title and description typed, the subject and area it opens on
function fillTheForm() {
  fireEvent.click(screen.getByRole('button', { name: 'New project' }));
  fireEvent.change(screen.getByPlaceholderText('e.g. AI-powered legal research assistant'), { target: { value: captured.ask.title } });
  fireEvent.change(screen.getByPlaceholderText('What does this project do, for whom, and why does it matter?'), { target: { value: captured.ask.description } });
  fireEvent.click(screen.getByRole('button', { name: /Create Project/ }));
}

const listed = (a: Answer) => ({ status: 200, body: [a.body] });
const open = async () => fireEvent.click(await screen.findByRole('button', { name: new RegExp(`^${captured.ask.title}`) }));

describe('ProjectsHub, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('creates what was typed, runs its stage as streamed, and proposes its advance once', async () => {
    const { post } = serve();
    const { container } = mount();
    expect(await screen.findByText(/^No projects yet/)).toBeTruthy();
    fillTheForm();
    await waitFor(() => expect(post).toHaveBeenCalledWith('/api/v1/projects/', captured.ask));
    fireEvent.click(await screen.findByRole('button', { name: /^Run concept$/ }));
    //  the stream's text as its frames said it, labelled with what composed it, and the output the server saved
    await waitFor(() => expect(screen.getByTestId('project-stream-provenance').textContent).toBe('structured floor — not model analysis'));
    expect(container.querySelector('pre')?.textContent).toBe(streamed);
    expect(captured.ran.body.outputs.map(o => o.served_by)).toEqual(['native']);
    await waitFor(() => expect(screen.getByText(/^Saved Outputs/).textContent).toBe('Saved Outputs (1)'));
    fireEvent.click(screen.getByRole('button', { name: /Propose Advance/ }));
    await waitFor(() => expect(screen.getByTestId('project-message').textContent).toBe('✓ Proposal submitted — go to Governance Hub to approve or reject.'));
    await waitFor(() => expect(screen.getByTestId('project-waiting-on-person').textContent).toMatch(
      /^Waiting on a person: a decision on the proposal to move it from 'concept' to 'prototype', raised .+\. It is decided in the Governance Hub's proposals\.$/));
    //  a second proposal for the same step is the route's refusal, by its reason
    fireEvent.click(screen.getByRole('button', { name: /Propose Advance/ }));
    await waitFor(() => expect(screen.getByTestId('project-message').textContent).toBe((captured.again.body as { detail: string }).detail));
  });

  it('a failed read of the list says its reason, and never that there are no projects', async () => {
    serve({ list: captured.list_failed });
    mount();
    await waitFor(() => expect(screen.getByTestId('projects-unread').textContent).toBe(
      `The projects could not be read, so the list is not what is there: Failed (HTTP 500): ${captured.list_failed.body.detail}`));
    expect(screen.queryByText(/^No projects yet/)).toBeNull();
  });

  it('a run that completed is said as completed when the project cannot be read again, and stays done', async () => {
    serve({ list: listed(captured.created), reread: 'unreachable' });
    mount();
    await open();
    fireEvent.click(await screen.findByRole('button', { name: /^Run concept$/ }));
    await waitFor(() => expect(screen.getByTestId('project-message').textContent).toBe(
      'The run completed and its output was saved, but the project could not be read again to show it: Failed — backend unreachable.'));
    //  in the list and in the panel
    expect(screen.getAllByLabelText('status: done')).toHaveLength(2);
    expect(screen.queryByLabelText('status: error')).toBeNull();
  });

  it('a proposal or a delete that reached no server says so, and never that the project is not ready', async () => {
    const { del } = serve({ list: listed(captured.ran), propose: 'unreachable' });
    mount();
    await open();
    fireEvent.click(await screen.findByRole('button', { name: /Propose Advance/ }));
    await waitFor(() => expect(screen.getByTestId('project-message').textContent).toBe(
      'Could not propose the advance: Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: 'Delete project' }));
    fireEvent.change(screen.getByTestId('ask-type-back'), { target: { value: captured.ask.title } });
    fireEvent.click(screen.getByRole('button', { name: 'Delete the project' }));
    await waitFor(() => expect(screen.getByTestId('project-message').textContent).toBe('Delete failed: Failed — backend unreachable.'));
    expect(del).toHaveBeenCalledWith(`/api/v1/projects/${PID}`, { params: { confirm_title: captured.ask.title } });
  });

  it('a project that could not be created says what happened', async () => {
    serve({ create: 'unreachable' });
    mount();
    expect(await screen.findByText(/^No projects yet/)).toBeTruthy();
    fillTheForm();
    await waitFor(() => expect(screen.getByTestId('project-create-error').textContent).toBe(
      'Could not create the project: Failed — backend unreachable.'));
  });
});
