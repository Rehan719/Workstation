// W986 (FU-399 part 18) — the Learning Loop page, rendered against the operations routes' own answers.
//
// The page shows the recorded outcomes of the platform's own runs: how many ran, how many a quality gate assessed and
// passed, how many were served in-house, the resources ranked, the failures and each model's health. This mounts the
// real page against the answers its five routes gave on a fresh store (OperationalExcellence.fixture.json, captured by
// w986_capture.py: an empty record, then three made-up runs), and has the server refuse each read. A rate over no run
// is not a zero, and one refused read does not hide the others.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './OperationalExcellence.fixture.json';
import { OperationalExcellence } from './OperationalExcellence';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const URL = {
  summary: '/api/v1/operations/summary', rankings: '/api/v1/operations/rankings',
  outcomes: '/api/v1/operations/outcomes?limit=40', models: '/api/v1/operations/model-health',
  failures: '/api/v1/operations/failures?limit=20',
};

function serve(state: 'empty' | 'runs', over: Record<string, Reply> = {}) {
  const pick = (k: keyof typeof URL) => (state === 'empty'
    ? (captured as Record<string, unknown>)[`${k}_empty`] : (captured as Record<string, unknown>)[k]);
  const base: Record<string, Reply> = Object.fromEntries(
    (Object.keys(URL) as (keyof typeof URL)[]).map(k => [URL[k], ok(pick(k))]));
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

// a stat card: its label, then its figure
const stat = (label: string) => screen.getByText(label).closest('div')?.parentElement?.querySelector('p.text-2xl')?.textContent;

describe('OperationalExcellence (the Learning Loop), rendered against the operations routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('an empty record: no run, and no rate printed as a zero', async () => {
    serve('empty');
    render(<OperationalExcellence />);
    await screen.findByText('Total runs');
    expect(stat('Total runs')).toBe('0');
    expect(stat('In-house rate')).toBe('not measured');
    expect(stat('Success rate (gate-assessed)')).toBe('not assessed');
    expect(screen.getByTestId('ops-in-house-basis').textContent).toBe(
      `In-house rate: ${captured.summary_empty.in_house_rate_basis}`);
    expect(screen.queryByText('0%')).toBeNull();
  });

  it('three runs: the figures and the ranking are the routes\' own', async () => {
    serve('runs');
    render(<OperationalExcellence />);
    await screen.findByText('Total runs');
    const s = captured.summary;
    expect(stat('Total runs')).toBe(String(s.total_runs));
    expect(stat('In-house rate')).toBe(`${Math.round(Number(s.in_house_rate) * 100)}%`);
    expect(stat('Resources')).toBe(String(s.distinct_resources));
    expect(await screen.findByTestId('rankings-basis')).toBeTruthy();
    expect(screen.getByTestId('rankings-basis').textContent).toBe(captured.rankings.basis);
    for (const r of captured.rankings.rankings) expect(screen.getAllByText(r.resource).length).toBeGreaterThan(0);
    expect(screen.getAllByTestId('outcome-mark')).toHaveLength(captured.outcomes.outcomes.length);
  });

  it('a refused read is said by what it was reading, and the other sections are still shown', async () => {
    serve('runs', { [URL.summary]: refused(503, 'the operations record could not be read') });
    render(<OperationalExcellence />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure').map(p => p.textContent)).toContain(
      'Could not read the summary — Failed (HTTP 503): the operations record could not be read'));
    //  the ranking and the outcomes were read, and are shown
    await waitFor(() => expect(screen.getByTestId('rankings-basis').textContent).toBe(captured.rankings.basis));
    expect(screen.getAllByTestId('outcome-mark')).toHaveLength(captured.outcomes.outcomes.length);
    expect(screen.queryByText('Failed to load operational metrics')).toBeNull();
    expect(screen.queryByText('Total runs')).toBeNull();
  });

  it('each read\'s refusal is said with its own reason', async () => {
    serve('runs', {
      [URL.rankings]: refused(503, 'the ranking could not be computed'),
      [URL.failures]: refused(502, 'the failures did not answer'),
    });
    render(<OperationalExcellence />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure')).toHaveLength(2));
    const said = screen.getAllByTestId('read-failure').map(p => p.textContent);
    expect(said).toEqual(expect.arrayContaining([
      'Could not read the rankings — Failed (HTTP 503): the ranking could not be computed',
      'Could not read the failures — Failed (HTTP 502): the failures did not answer',
    ]));
    expect(stat('Total runs')).toBe(String(captured.summary.total_runs));
  });

  it('no failure recorded is said as the route says it', async () => {
    serve('runs');
    render(<OperationalExcellence />);
    expect(captured.failures.state).toBe('none_recorded');
    expect(await screen.findByTestId('ops-failures')).toBeTruthy();
  });
});
