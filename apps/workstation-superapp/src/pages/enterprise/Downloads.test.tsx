// W1054 — no failure is said in a browser alert: the cockpit's export and the Projects hub's download, rendered.
//
// A census of alert() in the app found two left, both a failed download: the cockpit's export of a deliverable and the
// Projects hub's download of a saved output. An alert is a box that is gone once it is dismissed, and says nothing on
// the page about which row failed. This mounts both pages against their routes' own answers: the cockpit on the list
// VSBCockpit.deliverables.fixture.json read after its production, the hub on the project ProjectsHub.fixture.json read
// after its run, and each file route's own refusal and own file (Downloads.fixture.json, captured by w1054_capture.py:
// the two rows asked of a store that does not hold their records, and the same two asked of records made there as the
// fixtures made theirs). Each failure is said under its own row, and cleared when that row is downloaded again.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import files from './Downloads.fixture.json';
import cockpit from './VSBCockpit.deliverables.fixture.json';
import hub from '../projects/ProjectsHub.fixture.json';
import { VSBCockpit } from './VSBCockpit';
import { ProjectsHub } from '../projects/ProjectsHub';

type Answer = { status: number; body: unknown };
type Press = 'unreachable' | 'refused' | 'answered';
type Refusal = { url: string; status: number; body: { detail: string } };
type File = { url: string; status: number; content_disposition: string; content_type: string; text: string };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  the file route as it answered each press: a call that reached no server, its refusal, or the file it sent; what the
//  browser was handed to save is kept by name
function fileRoute(refused: Refusal, file: File, presses: Press[]) {
  const saved: string[] = [];
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) { saved.push(this.download); });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== refused.url) return { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) };
    const press = presses.shift();
    if (press === 'unreachable') throw new TypeError('Failed to fetch');
    if (press === 'refused') return { ok: false, status: refused.status, statusText: '', json: async () => refused.body };
    return {
      ok: true, status: file.status,
      headers: new Headers({ 'Content-Disposition': file.content_disposition, 'Content-Type': file.content_type }),
      blob: async () => new Blob([file.text], { type: file.content_type }),
    };
  }));
  return saved;
}
const nameIn = (f: File) => /filename="?([^";]+)"?/.exec(f.content_disposition)?.[1];

//  the cockpit's reads as their routes answered them, its list the one read after the production
function serveTheCockpit() {
  const answers = cockpit.answers as Record<string, Answer>;
  const list = `/api/v1/deliverables?vsb_id=${cockpit.vsb_id}`;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = key === list ? cockpit.after : answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
}

//  the hub's list and its project as they were read after the run
function serveTheHub() {
  const pid = hub.ran.body.id;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/projects/') return { status: 200, data: [hub.ran.body] };
    if (url === `/api/v1/projects/${pid}`) return { status: hub.ran.status, data: hub.ran.body };
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
}

describe('the two downloads, rendered against their routes\' own answers', () => {
  beforeAll(() => {
    //  jsdom has no object URLs; the page makes one of what it fetched and hands it to the browser to save
    Object.defineProperty(URL, 'createObjectURL', { configurable: true, value: () => 'blob:w1054' });
    Object.defineProperty(URL, 'revokeObjectURL', { configurable: true, value: () => undefined });
  });
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('the cockpit says a refused export under its row, never in an alert, and clears it when the row is exported again', async () => {
    const alerted = vi.spyOn(window, 'alert').mockImplementation(() => {});
    serveTheCockpit();
    const saved = fileRoute(files.export_refused, files.exported, ['refused', 'answered']);
    render(<MemoryRouter initialEntries={['/cockpit?tab=deliverables']}><VSBCockpit /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText(/^Outputs \(/).textContent).toBe('Outputs (1)'));
    fireEvent.click(screen.getByRole('button', { name: /^Export$/ }));
    await waitFor(() => expect(screen.getByTestId('cockpit-export-error').textContent).toBe(
      `Export failed (HTTP ${files.export_refused.status}): ${files.export_refused.body.detail}`));
    fireEvent.click(screen.getByRole('button', { name: /^Export$/ }));
    await waitFor(() => expect(saved).toEqual([nameIn(files.exported)]));
    expect(screen.queryByTestId('cockpit-export-error')).toBeNull();
    expect(alerted).not.toHaveBeenCalled();
  });

  it('the hub says a download that reached no server or was refused under its output, never in an alert, and clears it when it is downloaded', async () => {
    const alerted = vi.spyOn(window, 'alert').mockImplementation(() => {});
    serveTheHub();
    const saved = fileRoute(files.download_refused, files.downloaded, ['unreachable', 'refused', 'answered']);
    const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    render(<QueryClientProvider client={qc}><MemoryRouter><ProjectsHub /></MemoryRouter></QueryClientProvider>);
    fireEvent.click(await screen.findByRole('button', { name: new RegExp(`^${hub.ask.title}`) }));
    fireEvent.click(await screen.findByRole('button', { name: /^Download$/ }));
    await waitFor(() => expect(screen.getByTestId('project-download-error').textContent).toBe('Failed — backend unreachable.'));
    fireEvent.click(screen.getByRole('button', { name: /^Download$/ }));
    await waitFor(() => expect(screen.getByTestId('project-download-error').textContent).toBe(
      `Export failed (HTTP ${files.download_refused.status}): ${files.download_refused.body.detail}`));
    fireEvent.click(screen.getByRole('button', { name: /^Download$/ }));
    await waitFor(() => expect(saved).toEqual([nameIn(files.downloaded)]));
    expect(screen.queryByTestId('project-download-error')).toBeNull();
    expect(alerted).not.toHaveBeenCalled();
  });
});
