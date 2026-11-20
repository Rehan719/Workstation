// W1142 (FU-399 part 109) — THE MATTER BUNDLE, ASSEMBLED WITH PROVENANCE, rendered against the Law routes' own answers.
//
// The Law page's matter panel reads the one named folder's state and, on its button, assembles a draft from it: every
// particular shows the document and line it came from, or is a BLANK; every authority is resolved or REFUSED; the
// checks that did not resolve are listed on the page; and the not-legal-advice statement is shown where the work is
// read. A text scan held it (test_w610); no rendered test read it. This mounts the real panel against what the routes
// answered on a fresh store (MatterAssemblyPanel.fixture.json, captured by w1142_capture.py), with a made-up folder named
// by LEGAL_BUNDLE_DIR, the only way a test process reads one: first empty, then holding one made-up letter. Each draft is
// asked for as a person asks, by the panel's three fields and its button. Nothing about a real matter is read.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './MatterAssemblyPanel.fixture.json';
import MatterAssemblyPanel from './MatterAssemblyPanel';

type Answer = { status: number; body: any; request?: unknown };
type Fields = { particular: string; words: string; authority: string };
type Case = { fields: Fields; bundle: Answer; assemble: Answer };
const { empty, letter } = captured.cases as unknown as { empty: Case; letter: Case };
const unreached = () => new TypeError('Failed to fetch');

//  the folder's read and the draft as the routes answered them, or failing as a server out of reach does; each draft
//  asked for is kept
function serve(c: Case, fail: { bundle?: boolean; assemble?: boolean } = {}) {
  const posted: unknown[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const reply = (a: Answer) => ({ ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body });
    if (url === '/api/v1/law/bundle' && (init?.method ?? 'GET') === 'GET') {
      if (fail.bundle) throw unreached();
      return reply(c.bundle);
    }
    if (url === '/api/v1/law/matter/assemble' && init?.method === 'POST') {
      posted.push(JSON.parse(String(init.body)));
      if (fail.assemble) throw unreached();
      return reply(c.assemble);
    }
    return reply({ status: 599, body: { detail: `the test served nothing for ${url}` } });
  }));
  return posted;
}

//  a draft asked for as a person asks: the three fields, then the button
function assemble(f: Fields) {
  fireEvent.change(screen.getByPlaceholderText('particular, e.g. date of dismissal'), { target: { value: f.particular } });
  fireEvent.change(screen.getByPlaceholderText('words to find, comma-separated'), { target: { value: f.words } });
  fireEvent.change(screen.getByPlaceholderText('an authority, e.g. Equality Act 2010'), { target: { value: f.authority } });
  fireEvent.click(screen.getByRole('button', { name: 'Assemble draft' }));
}

const items = (id: string) => [...screen.getByTestId(id).querySelectorAll('li')].map(li => li.textContent);
const folderLine = (b: any) =>
  `Folder: ${b.folder_state} · ${b.document_count === null ? 'no documents can be counted' : `${b.document_count} document(s)`} · ${b.bundle_indexing_basis}`;

describe('MatterAssemblyPanel, the matter bundle assembled with provenance, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('before a draft, the folder\'s state is read and the panel says nothing here is legal advice', async () => {
    const posted = serve(empty);
    render(<MatterAssemblyPanel />);
    expect(empty.bundle.body.document_count).toBe(0);
    await waitFor(() => expect(screen.getByTestId('matter-bundle-state').textContent).toBe(folderLine(empty.bundle.body)));
    expect(screen.getByTestId('matter-not-legal-advice').textContent).toBe(
      'Nothing here is legal advice. This platform assembles and cites as a clerk would; it is never counsel, and it'
      + ' never forecasts an outcome.');
    expect(screen.queryByTestId('matter-artefact')).toBeNull();
    expect(posted).toEqual([]);
  });

  it('from an empty folder, the particular is a BLANK and the authority REFUSED, and the unresolved line names it', async () => {
    const a = empty.assemble.body;
    const posted = serve(empty);
    render(<MatterAssemblyPanel />);
    await waitFor(() => expect(screen.getByTestId('matter-bundle-state').textContent).toBe(folderLine(empty.bundle.body)));
    assemble(empty.fields);
    await waitFor(() => expect(items('matter-particulars')).toEqual(
      a.particulars.map((p: any) => `${p.particular}: ${p.rendered}`)));
    expect(a.particulars.map((p: any) => [p.found, p.rendered.startsWith('[BLANK:')])).toEqual([[false, true]]);
    expect(items('matter-authorities')).toEqual(a.authorities.map((x: any) => `${x.authority}: REFUSED — ${x.basis}`));
    expect(a.authorities_refused).toEqual([empty.fields.authority]);
    expect(screen.getByTestId('matter-unresolved-checks').textContent).toBe(
      `Unresolved: ${empty.fields.authority} (authority refused)`);
    expect(screen.getByTestId('matter-artefact').querySelector('p')?.textContent).toBe(`${a.status} · ${a.face}`);
    expect(screen.getByTestId('matter-not-legal-advice').textContent).toBe(a.not_legal_advice);
    expect(screen.getByText('Filing-shaped: this stays a draft until the Owner records an approval.')).toBeTruthy();
    expect(posted).toEqual([empty.assemble.request]);
  });

  it('from the made-up letter, the particular comes with its document and line, re-verified, and the authority is resolved', async () => {
    const a = letter.assemble.body;
    const posted = serve(letter);
    render(<MatterAssemblyPanel />);
    await waitFor(() => expect(screen.getByTestId('matter-bundle-state').textContent).toBe(folderLine(letter.bundle.body)));
    expect(letter.bundle.body.document_count).toBe(1);
    assemble(letter.fields);
    const p = a.particulars[0];
    expect([p.found, p.document, p.line, p.verification.verdict]).toEqual([true, 'dismissal_letter.txt', 2, 'MET']);
    await waitFor(() => expect(items('matter-particulars')).toEqual(
      [`${p.particular}: ${p.rendered} — ${p.document}:${p.line} (${p.verification.verdict})`]));
    expect(items('matter-authorities')).toEqual(a.authorities.map((x: any) => `${x.authority}: resolved — ${x.basis}`));
    expect(screen.getByTestId('matter-authorities-held').textContent).toBe(a.authorities_held.basis);
    expect(screen.getByTestId('matter-unresolved-checks').textContent).toBe('No unresolved check.');
    expect(posted).toEqual([letter.assemble.request]);
  });

  it('a folder that could not be read, and a draft that was not assembled, each say so', async () => {
    serve(letter, { bundle: true, assemble: true });
    render(<MatterAssemblyPanel />);
    await waitFor(() => expect(screen.getByText('The matter folder could not be read: Failed — backend unreachable.')).toBeTruthy());
    expect(screen.queryByTestId('matter-bundle-state')).toBeNull();
    assemble(letter.fields);
    await waitFor(() => expect(screen.getByText('Not assembled: Failed — backend unreachable.')).toBeTruthy());
    expect(screen.queryByTestId('matter-artefact')).toBeNull();
  });
});
