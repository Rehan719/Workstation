// W1118 (FU-399 part 107) — THE ARCHIVE SEARCH, rendered against the route's own answers.
//
// The Horizon Companion's search panel looks for an exact word in the explicit inbox's index and shows each located
// passage with its document and line, the counts with what was omitted, how a passage can be cited, and the files the
// search could not look inside. No rendered test read it. This mounts the real panel against what the route answered
// on a fresh store (ArchiveSearchPanel.fixture.json, captured by w1118_capture.py) after four made-up files were put
// in the inbox and scanned: two text files that use the word, a PDF this module does not read, and a file excluded by
// its name before any byte was read. No scan writes a passage without a line, so the not-citable list is not drawn.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ArchiveSearchPanel.fixture.json';
import ArchiveSearchPanel from './ArchiveSearchPanel';

type Answer = { status: number; body: unknown };
type Passage = { path: string; line: number; text: string };
type Searched = { passages_matched: number; shown_files: number; matched_files: number; file_hits_basis: string;
                  passages: Passage[]; citation_basis: string; not_citable: unknown[]; not_searched: string[] };

//  each search answers what the route answered for its address, or fails as a server out of reach does while
//  `down` says so; what was asked is kept in order
function serve(answers: Record<string, Answer>, down: { now: boolean } = { now: false }) {
  const sent: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    sent.push(url);
    if (down.now) throw new TypeError('Failed to fetch');
    const a = answers[url] ?? { status: 599, body: { detail: `the test served nothing for ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
  return sent;
}

const box = () => screen.getByPlaceholderText('search the indexed files (exact words)');
const search = (term: string) => {
  fireEvent.change(box(), { target: { value: term } });
  fireEvent.click(screen.getByRole('button', { name: 'Search' }));
};
//  the counts line, as the route's answer states its parts
const counts = (r: Searched) =>
  `${r.passages_matched} passage(s) matched · ${r.shown_files} of ${r.matched_files} file(s) shown · ${r.file_hits_basis}`;

describe('ArchiveSearchPanel, the archive search, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('nothing is searched until a word is typed, and spaces are not a word', () => {
    const sent = serve({});
    render(<ArchiveSearchPanel />);
    expect(screen.getByTestId('archive-search-panel')).toBeTruthy();
    const go = screen.getByRole('button', { name: 'Search' }) as HTMLButtonElement;
    expect(go.disabled).toBe(true);
    fireEvent.change(box(), { target: { value: '   ' } });
    expect(go.disabled).toBe(true);
    expect(sent).toEqual([]);
  });

  it('a word two indexed files use: each passage with its document and line, the counts, and what was not searched', async () => {
    const f = captured.found.body as Searched;
    const sent = serve({ [captured.found.url]: captured.found });
    render(<ArchiveSearchPanel />);
    search('orchard');
    await waitFor(() => expect(screen.getByTestId('archive-search-counts').textContent).toBe(counts(f)));
    expect(sent).toEqual([captured.found.url]);
    expect(f.passages.length).toBe(4);
    expect([...screen.getByTestId('archive-search-passages').querySelectorAll('li')].map(e => e.textContent)).toEqual(
      f.passages.map(p => `${p.path}:${p.line} — ${p.text}`));
    expect(screen.getByTestId('archive-search-citation-basis').textContent).toBe(f.citation_basis);
    expect(f.not_citable).toEqual([]);
    expect(screen.queryByTestId('archive-search-not-citable')).toBeNull();
    expect(screen.getByTestId('archive-search-not-searched').textContent).toBe(
      `Not searched (not read into the index): ${f.not_searched.join(', ')}`);
  });

  it('a word no indexed file uses: none matched, said as none, and what was not searched is still said', async () => {
    const n = captured.none.body as Searched;
    serve({ [captured.none.url]: captured.none });
    render(<ArchiveSearchPanel />);
    search('quince');
    await waitFor(() => expect(screen.getByTestId('archive-search-counts').textContent).toBe(counts(n)));
    expect(n.passages_matched).toBe(0);
    expect(screen.getByTestId('archive-search-passages').querySelectorAll('li').length).toBe(0);
    expect(screen.getByTestId('archive-search-citation-basis').textContent).toBe(n.citation_basis);
    expect(screen.getByTestId('archive-search-not-searched').textContent).toBe(
      `Not searched (not read into the index): ${n.not_searched.join(', ')}`);
  });

  it('a search that fails is said, and the result before it is taken away', async () => {
    const f = captured.found.body as Searched;
    const down = { now: false };
    serve({ [captured.found.url]: captured.found }, down);
    render(<ArchiveSearchPanel />);
    search('orchard');
    await waitFor(() => expect(screen.getByTestId('archive-search-counts').textContent).toBe(counts(f)));
    down.now = true;
    search('orchard');
    await waitFor(() => expect(screen.getByText('Search failed: Failed — backend unreachable.')).toBeTruthy());
    expect(screen.queryByTestId('archive-search-counts')).toBeNull();
    expect(screen.queryByTestId('archive-search-passages')).toBeNull();
  });
});
