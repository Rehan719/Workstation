// W1079 (FU-399 part 90) — the Quran platform's hub, rendered against its route's own answers.
//
// The hub's first tab shows one verse retrieved from its source (GET /api/v1/qep/ayah/2/1), every label derived from
// the answer, with no copy of its own to fall back on; recitation is never scored. This mounts the real hub against
// what the route answered on a fresh store (QEPReligionHub.fixture.json, captured by w1079_capture.py): the route's own
// 503 while its source cannot be reached, and its answer with the platform's Quran cache planted with a made-up
// placeholder (Latin words, a made-up surah name). No Quran text is kept and nothing is scored. The hub's other cards
// (the studio, the intelligence layer, the donor statement, the scholar review) each have a rendered test of their
// own; here each is a stand-in that says what it is. Rendering found the route's sentence on whether a prefix was
// separated from the verse shown only when one was: its "not checked" never reached the reader. Fixed here.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './QEPReligionHub.fixture.json';

vi.mock('../../components/QEPStudio', () => ({ QEPStudio: () => <p>studio stand-in</p> }));
vi.mock('../../components/qep/QEPIntelligence', () => ({ default: () => <p>intelligence stand-in</p> }));
vi.mock('../../components/QepDonorStatement', () => ({ default: () => <p>donor statement stand-in</p> }));
vi.mock('../../components/qep/ScholarReviewPanel', () => ({ default: () => <p>scholar review stand-in</p> }));

import { QEPReligionHub } from './QEPReligionHub';

type Answer = { status: number; body: any };
const V = captured.verse.body;

function serve(a: Answer) {
  const asked: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    asked.push(url);
    const r = url === '/api/v1/qep/ayah/2/1' ? a : { status: 404, body: { detail: `not served here: ${url}` } };
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body } as unknown as Response;
  }));
  return asked;
}

const mount = (at = '/qep') => render(<MemoryRouter initialEntries={[at]}><QEPReligionHub /></MemoryRouter>);

describe('QEPReligionHub, rendered against its route\'s own answers (a made-up placeholder for the verse)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows the verse its source returned, under the reference, name and source the source returned', async () => {
    serve(captured.verse);
    mount();
    await waitFor(() => expect(screen.getByText(V.text_arabic)).toBeTruthy());
    //  the badge is the source's reference and its own name for the surah, as one label
    expect(screen.getAllByText((_, el) => el?.textContent === `${V.ref} · ${V.surah_name}`).length).toBeGreaterThan(0);
    expect(screen.getAllByText(V.source).length).toBeGreaterThan(0);
    await waitFor(() => expect(screen.getByTestId('coach-provenance').textContent).toBe(
      `edition ${V.edition ?? 'not stated'} · ${V.riwayah ? `riwayah ${V.riwayah}` : 'riwayah not declared'}`));
    expect(screen.getByText(`The text above was retrieved from ${V.source} at ${V.ref}: it is not stored in this page and is never generated.`, { exact: false })).toBeTruthy();
    expect(screen.getByText('Recitation assessment unavailable')).toBeTruthy();
    //  the route's own sentence on the prefix, whatever it found (here: not checked, so no boundary asserted)
    expect(screen.getByTestId('coach-basmala-basis').textContent).toBe(V.basmala_basis);
  });

  it('shows no verse when its source cannot be reached, and says why by the route\'s reason', async () => {
    serve(captured.unavailable);
    mount();
    await waitFor(() => expect(screen.getByText(
      `No verse is shown: the sourced text could not be retrieved — Failed (HTTP 503): ${captured.unavailable.body.detail}`)).toBeTruthy());
    expect(screen.getByText('verse unavailable')).toBeTruthy();
    expect(screen.getByText(/keeps no copy of the Qur’an to fall back on/)).toBeTruthy();
    expect(screen.queryByTestId('coach-provenance')).toBeNull();
  });

  it('opens the tab its address names, and the donor statement is on every tab', async () => {
    const asked = serve(captured.verse);
    mount('/qep?tab=review');
    expect(screen.getByText('scholar review stand-in')).toBeTruthy();
    expect(screen.getByText('donor statement stand-in')).toBeTruthy();
    expect(asked).toEqual([]);   // the coach is not on this tab, so no verse is asked for
    fireEvent.click(screen.getByRole('button', { name: /Memorization/ }));
    expect(screen.getByText('studio stand-in')).toBeTruthy();
    expect(screen.getByText('donor statement stand-in')).toBeTruthy();
  });

  it('offers no machine-scored recitation contest: it is refused, by ruling', () => {
    serve(captured.verse);
    mount('/qep?tab=comp');
    expect(screen.getByText('Machine-scored recitation contests')).toBeTruthy();
    expect(screen.getByText('REFUSED (A.9.1)')).toBeTruthy();
  });
});
