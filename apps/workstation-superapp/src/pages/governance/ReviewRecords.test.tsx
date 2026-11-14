// W922 (FU-399 part 5) — the review cell's records, and the one form that records a review, rendered.
//
// Every sentence the governance page says about a record is the server's: whether it counts and why not, that a
// credential is as stated and not verified, and each refusal at the door. Those are claims about what a person SEES,
// the kind FU-399 converts. This mounts the real page against the API's own answer, captured from the record route
// after four records were made (a rule check and a signature that count, an uncalibrated agent's whole review that
// is kept and not counted, and an agent's review stored before clause 2), and drives the form against the door.
import { fireEvent, render, screen, within, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ReviewRecords.fixture.json';
import { ReviewRecords } from './ReviewRecords';

// answer the page's read with the captured listing (or a refusal), and its POST with `post`
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function serve(listing: any, post?: { status: number; body: unknown }) {
  const sent: { url: string; init?: RequestInit }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    sent.push({ url, init });
    const reply = (status: number, body: unknown) =>
      ({ ok: status < 400, status, statusText: '', json: async () => body });
    if (init?.method === 'POST' && post) return reply(post.status, post.body);
    if ('status' in listing) return reply(listing.status, { detail: listing.detail });
    return reply(200, listing);
  }));
  return sent;
}

describe('ReviewRecords, the records and the form, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('every record is shown, and one that does not count says why in the server\'s words', async () => {
    const listing = captured.records;
    serve(listing);
    render(<ReviewRecords />);
    await waitFor(() => expect(screen.getByTestId('review-records-count').textContent).toBe(`${listing.counted} of ${listing.total} record(s) count.`));
    expect(screen.getByTestId('review-records-basis').textContent).toBe(`${listing.basis}.`);
    expect(screen.getByTestId('review-records-credential').textContent).toBe(`${listing.credential_basis}.`);
    for (const r of listing.records) {
      const row = screen.getByTestId(`review-record-${r.record_id}`);
      const why = within(row).queryByTestId(`review-record-why-not-${r.record_id}`);
      if (r.counts) expect(why).toBeNull();
      else expect(why?.textContent).toBe(`Does not count: ${r.why_not}.`);
    }
    expect(listing.records.some(r => !r.counts) && listing.records.some(r => r.counts)).toBe(true);
  });

  it('an agent\'s review is sent as clause 2 asks, and the door\'s refusal is shown in its own words', async () => {
    const said = "Not recorded: the source 'rcp-news2' does not say which page or section was read. A record is stored "
      + 'only when it meets the rule of the tier it claims.';
    const sent = serve(captured.records, { status: 422, body: { detail: said } });
    render(<ReviewRecords />);
    await screen.findByTestId('review-records-count');
    fireEvent.change(screen.getByLabelText('Tier'), { target: { value: 'reviewed_by_workstation_agent' } });
    fireEvent.change(screen.getByLabelText('Tool'), { target: { value: 'care_risk_assess' } });
    fireEvent.change(screen.getByLabelText('Date'), { target: { value: '2026-11-13' } });
    const fill: Record<string, string> = {
      'The agent that reviewed (its calibration is read from its recorded run)': 'care-reviewer',
      'The checklist used': 'care checklist v2',
      'The version of the tool it reviewed': 'care_risk_assess as built today',
      'Sources read, one per line: register id | page or section | date read (YYYY-MM-DD)':
        'nice-ng249 | recommendations 1.1 | 2026-11-13\nrcp-news2 |  | 2026-11-12',
      'The model that reviewed': 'local-model',
      'What it could not check ("nothing" if so)': 'nothing',
    };
    for (const [label, value] of Object.entries(fill)) fireEvent.change(screen.getByLabelText(label), { target: { value } });
    fireEvent.click(screen.getByText('Record'));
    //  the status and the door's own sentence, as the shared helper words every refusal (errorMessage)
    await waitFor(() => expect(screen.getByTestId('review-record-refused').textContent).toBe(`Failed (HTTP 422): ${said}`));
    const post = sent.find(s => s.init?.method === 'POST');
    const body = JSON.parse(String(post?.init?.body));
    expect(post?.url).toBe('/api/v1/review/record');
    expect(body.tool_version).toBe('care_risk_assess as built today');
    expect(body.sources_read).toEqual([
      { source: 'nice-ng249', page: 'recommendations 1.1', read_on: '2026-11-13' },
      { source: 'rcp-news2', page: '', read_on: '2026-11-12' },
    ]);
    expect(screen.queryByTestId('review-record-said')).toBeNull();
  });

  it('with no record, the page says none has been recorded', async () => {
    serve({ ...captured.records, records: [], total: 0, counted: 0, tools: {} });
    render(<ReviewRecords />);
    await waitFor(() => expect(screen.getByTestId('review-records-none').textContent).toBe('No review has been recorded for any tool.'));
  });

  it('a record store that cannot be read is said, and never shown as empty', async () => {
    const detail = 'The record of reviews exists and could not be read whole. Nothing is shown from it, and no tool is '
      + 'treated as reviewed.';
    serve({ status: 503, detail });
    render(<ReviewRecords />);
    await waitFor(() => expect(screen.getByTestId('review-records-unread').textContent).toBe(`Failed (HTTP 503): ${detail}`));
    expect(screen.queryByTestId('review-records-none')).toBeNull();
    expect(screen.queryByTestId('review-records-count')).toBeNull();
  });
});
