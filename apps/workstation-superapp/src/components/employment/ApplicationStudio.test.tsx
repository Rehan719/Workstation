// W1026 (FU-399 part 51) — the Employment application studio, rendered against its routes' own answers.
//
// The studio reads the uploads, generates application documents from them, and synthesises example job listings it
// says are not a live board. Until now it was read only as source text. This mounts the real studio against the
// routes' answers (ApplicationStudio.fixture.json, captured on a fresh store with no model installed): one made-up
// CV in the knowledge base, the floor's job search, two replies made up for the capture and run through the route (one
// with a whole listing and one that leaves out its employer and its location, one in prose with no listing in it), and
// the refusals the routes give.
//
// Rendering found four defects, fixed in this round:
// - six failures were said as fixed sentences, five through alert(), each dropping the reason;
// - a listing with no location read "Remote", and one with no employer read "Company";
// - a search that parsed no listing gave a bare zero, and the page said "Try broadening your terms";
// - the CV the studio offers as "CV" came back titled "Cv".
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './ApplicationStudio.fixture.json';
import { ApplicationStudio } from './ApplicationStudio';

type Answer = { status: number; data: unknown };
const ok = (data: unknown): Answer => ({ status: 200, data });
const refused = (r: { status: number; body: unknown }): Answer => ({ status: r.status, data: r.body });
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

function serve(post: Record<string, Answer | 'unreached'>, del?: Answer) {
  //  the uploads list as the route answered it, and as it answered once a listing was attached
  let attached = false;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/ingest/list') return { status: 200, data: attached ? captured.uploads_after_use : captured.uploads } as never;
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    const a = post[url];
    if (a === 'unreached') throw unreached();
    if (!a) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (a.status >= 400) throw axiosRefusal(a.status, a.data);
    if (url === '/api/v1/career/job-search/use') attached = true;
    return a as never;
  });
  vi.spyOn(axios, 'delete').mockImplementation(async (url: string) => {
    if (!del) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (del.status >= 400) throw axiosRefusal(del.status, del.data);
    return del as never;
  });
  //  the three tools' options, as the review-options route answered them
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const ep = decodeURIComponent(String(url).split('endpoint=')[1] ?? '');
    const body = (captured.review_options as Record<string, unknown>)[ep];
    return body === undefined
      ? { ok: false, status: 404, statusText: '', json: async () => ({ detail: `not served here: ${url}` }) }
      : { ok: true, status: 200, json: async () => body };
  }));
}

const CV = captured.uploads[0].filename;
const partialTitle = () => captured.job_search_model.results[1].title;

async function mount() {
  render(<ApplicationStudio title="W1026 made up: Application Studio" />);
  await waitFor(() => expect(screen.getAllByText(CV).length).toBeGreaterThan(0));
}

function search() {
  const box = screen.getByPlaceholderText('Optional: override search terms (e.g. remote senior react developer)');
  fireEvent.change(box, { target: { value: 'W1026 made up: delivery coordinator' } });
  fireEvent.keyDown(box, { key: 'Enter' });
}

//  a listing's employer and place are said on one line, "employer · place"
const said = (text: string) => screen.queryAllByText((_, el) =>
  el?.tagName === 'P' && (el.textContent ?? '').replace(/\s+/g, ' ').trim() === text);

describe('ApplicationStudio, rendered against its routes', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows a document the floor composed whole, titled as the studio names it', async () => {
    serve({ '/api/v1/career/generate': ok(captured.generate) });
    await mount();
    fireEvent.click(screen.getByText('CV', { selector: 'span' }));
    fireEvent.click(screen.getByRole('button', { name: /^Generate/ }));
    const [doc] = captured.generate.results;
    await waitFor(() => expect(screen.getAllByText((_, el) => el?.tagName === 'PRE' && el.textContent === doc.content).length).toBe(1));
    expect(doc.title).toBe('CV');
    expect(screen.getByText(doc.title, { selector: 'p' }).textContent).toContain('CV');
    expect(axios.post).toHaveBeenCalledWith('/api/v1/career/generate',
      expect.objectContaining({ output_types: ['cv'], file_ids: [captured.uploads[0].file_id] }));
    expect(screen.queryByTestId('studio-generate-failed')).toBeNull();
  });

  it('says a refused generation by its reason, beside the button, and never in an alert', async () => {
    const alert = vi.spyOn(window, 'alert').mockImplementation(() => {});
    serve({ '/api/v1/career/generate': refused(captured.generate_refused) });
    await mount();
    fireEvent.click(screen.getByText('CV', { selector: 'span' }));
    fireEvent.click(screen.getByRole('button', { name: /^Generate/ }));
    await waitFor(() => expect(screen.getByTestId('studio-generate-failed').textContent).toBe(
      `Nothing was generated: Failed (HTTP 400): ${captured.generate_refused.body.detail}`));
    expect(screen.queryByTestId('studio-files-failed')).toBeNull();
    expect(alert).not.toHaveBeenCalled();
  });

  it('says a refused removal by its reason, where the files are', async () => {
    const alert = vi.spyOn(window, 'alert').mockImplementation(() => {});
    serve({}, refused(captured.delete_refused));
    await mount();
    fireEvent.click(screen.getByRole('button', { name: `Remove ${CV}` }));
    await waitFor(() => expect(screen.getByTestId('studio-files-failed').textContent).toBe(
      `The file was not removed: Failed (HTTP 404): ${captured.delete_refused.body.detail}`));
    expect(alert).not.toHaveBeenCalled();
  });

  it('says why the floor\'s search has no listing, and names no cause it did not measure', async () => {
    serve({ '/api/v1/career/job-search': ok(captured.job_search) });
    await mount();
    search();
    await waitFor(() => expect(screen.getByTestId('job-search-none-basis').textContent).toBe(captured.job_search.none_basis));
    expect(captured.job_search.none_basis).toContain('this says nothing about whether such roles exist');
    expect(screen.getByTestId('job-search-floor').textContent).toContain('the deterministic native floor served this search');
    expect(screen.queryByText(/Try broadening your terms/)).toBeNull();
  });

  it('says why a reply in prose has no listing, and offers no cause for it', async () => {
    serve({ '/api/v1/career/job-search': ok(captured.job_search_prose) });
    await mount();
    search();
    await waitFor(() => expect(screen.getByTestId('job-search-none-basis').textContent).toBe(captured.job_search_prose.none_basis));
    expect(captured.job_search_prose.none_basis).toContain('Nothing came back in the shape a listing is asked for.');
    expect(screen.queryByText(/Try broadening your terms/)).toBeNull();
    expect(screen.queryByTestId('job-search-floor')).toBeNull();
  });

  it('says what a model\'s listing leaves out, and marks each one illustrative', async () => {
    serve({ '/api/v1/career/job-search': ok(captured.job_search_model) });
    await mount();
    search();
    const [whole, partial] = captured.job_search_model.results;
    await waitFor(() => expect(screen.getByText(partial.title as string).textContent).toBe(partial.title));
    expect([partial.company, partial.location]).toEqual([null, null]);
    expect(said(`${whole.company} · ${whole.location}`).length).toBe(1);
    expect(said('employer not stated · Not specified').length).toBe(1);
    expect(screen.getAllByText('illustrative · no live URL').length).toBe(2);
    expect(screen.queryByTestId('job-search-none-basis')).toBeNull();
  });

  it('attaches a listing as the target job ad, and the list read again holds it', async () => {
    serve({ '/api/v1/career/job-search': ok(captured.job_search_model),
            '/api/v1/career/job-search/use': ok(captured.use) });
    await mount();
    search();
    await waitFor(() => expect(screen.getAllByRole('button', { name: /Use as Target Job Ad/ }).length).toBe(2));
    fireEvent.click(screen.getAllByRole('button', { name: /Use as Target Job Ad/ })[0]);
    const ad = captured.uploads_after_use.find(u => u.category === 'job_ad');
    expect(ad).toBeTruthy();
    await waitFor(() => expect(screen.getByText(ad!.filename).textContent).toBe(ad!.filename));
    expect(screen.getAllByText(/Attached as Target Job Ad \(illustrative\)/).length).toBe(1);
    expect(screen.getAllByRole('button', { name: /Use as Target Job Ad/ }).length).toBe(1);
    expect(screen.queryByTestId('studio-listing-failed')).toBeNull();
  });

  it('says a refused attach by its reason, where the listings are', async () => {
    const alert = vi.spyOn(window, 'alert').mockImplementation(() => {});
    serve({ '/api/v1/career/job-search': ok(captured.job_search_model),
            '/api/v1/career/job-search/use': refused(captured.use_refused) });
    await mount();
    search();
    await waitFor(() => expect(screen.getAllByRole('button', { name: /Use as Target Job Ad/ }).length).toBe(2));
    fireEvent.click(screen.getAllByRole('button', { name: /Use as Target Job Ad/ })[1]);
    await waitFor(() => expect(screen.getByTestId('studio-listing-failed').textContent).toBe(
      `The listing was not attached as the Target Job Ad: Failed (HTTP 422): ${captured.use_refused.body.detail}`));
    //  what the listing does not give is posted as empty: the route refuses a null employer
    expect(axios.post).toHaveBeenCalledWith('/api/v1/career/job-search/use',
      expect.objectContaining({ title: partialTitle(), company: '', location: '' }));
    expect(screen.queryByText(/Attached as Target Job Ad/)).toBeNull();
    expect(alert).not.toHaveBeenCalled();
  });

  it('says a search that reached no server as one, not as a synthesis to try again', async () => {
    serve({ '/api/v1/career/job-search': 'unreached' });
    await mount();
    search();
    await waitFor(() => expect(screen.getByTestId('job-search-failed').textContent).toBe(
      'The example listings were not synthesised: Failed — backend unreachable.'));
    expect(screen.queryByText(/Try again/)).toBeNull();
  });
});
