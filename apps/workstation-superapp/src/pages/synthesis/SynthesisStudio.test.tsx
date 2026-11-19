// W1021 (FU-399 part 48) — the synthesis studio, rendered against its routes' own answers.
//
// The studio reads the knowledge base and the history, and asks for one output per type chosen: a document or a
// website from the stream, every structured output from /generate. Until now it was read only as source text. This
// mounts the real studio against the routes' answers (SynthesisStudio.fixture.json, captured on a fresh store with
// no model installed): one made-up note in the knowledge base, /generate's answer for each structured type, the
// stream's frames for a report, played back as a network delivers them, the history after them, and a request the
// route refuses.
//
// Rendering found these defects, fixed in this round:
// - the stream handed every structured output over as text, and each display that parses its output drew nothing;
//   each is now composed whole by /generate, and /stream refuses it;
// - an output the model did not return drew an empty panel, and a deck of none was "1 slides · player can open this";
// - every failed generation, a refusal included, was said as "check the API server is running";
// - an unread knowledge base read "No files ingested yet", and an unread history "No synthesis runs yet";
// - a streamed result's text was read back off the page, so it could miss the last frames.
//
// W1028 - a refused delete is said by its status and reason, and one whose answer gave no reason is never said as an
// unreachable server: the delete's fallback was "backend unreachable".
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './SynthesisStudio.fixture.json';
import ingest from '../../components/employment/ApplicationStudio.fixture.json';   // W1028 - the ingest route's own refusal
import { SynthesisStudio } from './SynthesisStudio';

const FILE = captured.files[0];
const answers = captured.generate as Record<string, { content: string; served_by: string | null }>;
const COMPOSED = ['simulation', 'business_model', 'audiobook', 'app', 'presentation'];
const LABELS: Record<string, string> = {
  report: 'Report', simulation: 'Simulation', business_model: 'Business Model', audiobook: 'Audiobook',
  app: 'App', presentation: 'Presentation',
};

const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  the captured stream, played back in two pieces cut mid-frame, as a network delivers it
function streamOf(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  const cut = Math.floor(bytes.length / 2);
  return new ReadableStream({ start(c) { c.enqueue(bytes.slice(0, cut)); c.enqueue(bytes.slice(cut)); c.close(); } });
}

//  the text the stream's frames carry, read as the SSE protocol gives it: each token frame's text, in order
function framesText(sse: string): string {
  return sse.split('\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)))
    .filter(ev => ev.token !== undefined).map(ev => String(ev.token).replace(/\\n/g, '\n')).join('');
}

type Read = { ok: true } | { refused: number; body: unknown };
function serve(opts: { files?: Read; history?: Read; generate?: Read } = {}) {
  const get = vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    const r = url === '/api/v1/ingest/list' ? opts.files : url === '/api/v1/synthesis/history' ? opts.history : undefined;
    if (r && 'refused' in r) throw axiosRefusal(r.refused, r.body);
    if (url === '/api/v1/ingest/list') return { status: 200, data: captured.files } as never;
    if (url === '/api/v1/synthesis/history') return { status: 200, data: captured.history } as never;
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  const post = vi.spyOn(axios, 'post').mockImplementation(async (url: string, body: any) => {
    if (url !== '/api/v1/synthesis/generate') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (opts.generate && 'refused' in opts.generate) throw axiosRefusal(opts.generate.refused, opts.generate.body);
    return { status: 200, data: answers[body.output_type] } as never;
  });
  const fetchMock = vi.fn(async (url: string, init?: { body?: string }) => {
    if (url !== '/api/v1/synthesis/stream') return { ok: false, status: 404, body: null, json: async () => ({}) };
    if (opts.generate && 'refused' in opts.generate) {
      return { ok: false, status: opts.generate.refused, body: null, json: async () => opts.generate };
    }
    const type = JSON.parse(init?.body ?? '{}').output_type;
    if (type !== 'report') throw new Error(`the studio streamed ${type}, which is composed whole`);
    return { ok: true, status: 200, body: streamOf(captured.stream_report), json: async () => ({}) };
  });
  vi.stubGlobal('fetch', fetchMock);
  return { get, post, fetchMock };
}

function mount() {
  return render(<MemoryRouter><SynthesisStudio /></MemoryRouter>);
}

async function generate(types: string[]) {
  await waitFor(() => expect(screen.getByText(FILE.filename)).toBeTruthy());
  fireEvent.click(screen.getByText(FILE.filename));
  for (const t of types) fireEvent.click(screen.getByText(LABELS[t], { selector: 'span' }));
  fireEvent.click(screen.getByRole('button', { name: /^Generate/ }));
}

//  each result's card, by its type's label in the card's header
function card(label: string): HTMLElement {
  const header = screen.getAllByText(label, { selector: 'p span, p' }).map(el => el.closest('.rounded-2xl') as HTMLElement)
    .find(el => el && el.querySelector('[data-testid="synthesis-result-provenance"]'));
  if (!header) throw new Error(`no result card for ${label}`);
  return header;
}

describe('SynthesisStudio, rendered against the routes it reads', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    // jsdom has no layout and so no ResizeObserver, which the simulation's chart container needs to mount
    vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('streams the report and asks /generate for every structured output, each saying the model returned none', async () => {
    const { post, fetchMock } = serve();
    mount();
    await generate(COMPOSED);                                 // the report is chosen when the studio opens
    await waitFor(() => expect(screen.getByText(`${COMPOSED.length + 1} Outputs Generated`)).toBeTruthy());
    expect(fetchMock.mock.calls.map(c => JSON.parse((c[1] as { body: string }).body).output_type)).toEqual(['report']);
    expect(post.mock.calls.map(c => (c[1] as { output_type: string }).output_type).sort()).toEqual([...COMPOSED].sort());

    // the report is open first: its text is the text the stream's frames carried, whole
    const report = card('Report');
    expect(within(report).getByTestId('studio-result-content').textContent).toBe(framesText(captured.stream_report));
    expect(within(report).getByTestId('synthesis-result-provenance').textContent).toBe('structured floor — not model analysis');

    for (const t of ['business_model', 'audiobook', 'app', 'presentation']) {
      const c = card(LABELS[t]);
      fireEvent.click(c.firstElementChild as HTMLElement);  // open it
      const said = JSON.parse(answers[t].content);
      const detail = (Array.isArray(said) ? said[0] : said);
      await waitFor(() => expect(within(c).getByTestId('studio-not-generated').textContent)
        .toBe(detail.detail ?? detail.content));
    }
    const deck = card('Presentation');
    expect(within(deck).getByTestId('studio-player-line').textContent).toBe('no slide data in this result · the player has nothing to open');
    expect((within(deck).getByTestId('studio-launch-player') as HTMLButtonElement).disabled).toBe(true);

    // the simulation's dashboard says its own, under the result's own badge
    const sim = card('Simulation');
    fireEvent.click(sim.firstElementChild as HTMLElement);
    await waitFor(() => expect(within(sim).getByTestId('model-provenance').textContent).toBe('structured floor — not model analysis'));
    expect(within(sim).getByRole('status').textContent).toBe(JSON.parse(answers.simulation.content).detail);
    expect(within(sim).queryByTestId('studio-not-generated')).toBeNull();
  });

  it('says a refused generation by its reason, never as a server that is not running', async () => {
    serve({ generate: { refused: captured.refused.status, body: captured.refused.body } });
    mount();
    await generate([]);
    const said = `Generation failed for report: Failed (HTTP 409): ${captured.refused.body.detail.message}`;
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain(said));
    expect(screen.getByRole('alert').textContent).not.toContain('check the API server is running');
  });

  it('says a refused delete by its status and reason, and one with no reason never as an unreachable server', async () => {
    serve();
    //  the ingest route's own refusal of a file it no longer holds (captured by W1026), then a proxy's answer in front
    //  of the server, made up for this test: a 429 whose body is a page, so it carries no reason
    const del = vi.spyOn(axios, 'delete')
      .mockImplementationOnce(async () => { throw axiosRefusal(ingest.delete_refused.status, ingest.delete_refused.body); })
      .mockImplementationOnce(async () => { throw axiosRefusal(429, '<html><body>W1028 made up: too many requests</body></html>'); });
    mount();
    const remove = await waitFor(() => screen.getByRole('button', { name: `Remove ${FILE.filename} from knowledge base` }));
    fireEvent.click(remove);
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain(
      `Delete failed: Failed (HTTP 404): ${ingest.delete_refused.body.detail}`));
    fireEvent.click(remove);
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('Delete failed: Failed (HTTP 429): no reason given'));
    expect(screen.getByRole('alert').textContent).not.toMatch(/unreachable/);
    expect(del).toHaveBeenCalledTimes(2);
    expect(screen.getAllByText(FILE.filename).length).toBeGreaterThan(0);
  });

  it('says an unread knowledge base as unread, never as empty', async () => {
    serve({ files: { refused: 503, body: { detail: 'W1021 made up: the registry could not be read whole' } } });
    mount();
    await waitFor(() => expect(screen.getByTestId('studio-files-unread').textContent).toBe(
      'The knowledge base could not be read (Failed (HTTP 503): W1021 made up: the registry could not be read whole), '
      + 'so whether it holds any file is not known.'));
    expect(screen.queryByText(/No files ingested yet/)).toBeNull();
  });

  it('lists the history it read, and says an unread history as unread', async () => {
    serve();
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'History' }));
    await waitFor(() => expect(screen.getAllByText(captured.history[0].metadata.title).length).toBeGreaterThan(0));
    expect(screen.queryByTestId('studio-history-unread')).toBeNull();

    vi.restoreAllMocks();
    serve({ history: { refused: 503, body: { detail: 'W1021 made up: the history could not be read' } } });
    fireEvent.click(screen.getByRole('button', { name: 'History' }));   // closed
    fireEvent.click(screen.getByRole('button', { name: 'History' }));   // opened again, read again
    await waitFor(() => expect(screen.getByTestId('studio-history-unread').textContent).toBe(
      'The history could not be read (Failed (HTTP 503): W1021 made up: the history could not be read), '
      + 'so whether this session has any run is not known.'));
    expect(screen.queryByText('No synthesis runs yet this session.')).toBeNull();
  });
});
