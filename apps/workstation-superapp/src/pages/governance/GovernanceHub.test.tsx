// W990 (FU-399 part 22) — the Governance Hub's audit tab, rendered against the ledger and proposal routes' own answers.
//
// The audit tab shows the constitutional ledger (its chain recomputed, its newest events, each with what it is) and
// the stage proposals awaiting a vote. This mounts the real page against the answers its three reads gave on a fresh
// store (GovernanceHub.fixture.json, captured by w990_capture.py: one change filed, so the ledger holds its event; no
// proposal), and has the server refuse each read. One refused read does not hide the other, and an unread list of
// proposals is not a list of none.
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './GovernanceHub.fixture.json';
import { GovernanceHub } from './GovernanceHub';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const VERIFY = '/api/v1/gaas/ueg/verify';
const EVENTS = '/api/v1/gaas/ueg/events?limit=40';
const PROPOSALS = '/api/v1/projects/governance/proposals';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = { [VERIFY]: ok(captured.verify), [EVENTS]: ok(captured.events) };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
  //  the proposals are read through axios, which answers a refusal by throwing its own error
  const p = over[PROPOSALS] ?? ok(captured.proposals);
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url !== PROPOSALS) throw new Error(`not served in this test: ${url}`);
    if (p.status >= 400) {
      throw Object.assign(new Error(`Request failed with status code ${p.status}`),
        { isAxiosError: true, response: { status: p.status, data: p.body } });
    }
    return { data: p.body, status: p.status };
  });
}

const mount = () => render(<MemoryRouter><GovernanceHub /></MemoryRouter>);
//  a stat card: its label, then its figure
const stat = (label: string) => screen.getByText(label).parentElement?.querySelector('p.text-xl')?.textContent;
const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);
const ev = captured.events.events[0];
const eventRow = `${String(ev.data?.type ?? 'event')} · ${ev.id}`;

describe('GovernanceHub (audit), rendered against the ledger and proposal routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('the ledger and the proposals are the routes\' own', async () => {
    serve();
    mount();
    expect(await screen.findByText(eventRow)).toBeTruthy();
    expect(stat('UEG Events')).toBe(String(captured.verify.events));
    expect(stat('Chain Integrity')).toBe(captured.verify.anchor_checked ? 'VALID' : 'HASHES OK');
    expect(await screen.findByText('No proposals yet.')).toBeTruthy();
    expect(failures()).toEqual([]);
  });

  it('a refused verification is said by what it was reading, and the event log is still shown', async () => {
    serve({ [VERIFY]: refused(503, 'the ledger file is locked') });
    mount();
    await waitFor(() => expect(failures()).toContain(
      'Could not read the ledger\'s verification — Failed (HTTP 503): the ledger file is locked'));
    expect(await screen.findByText(eventRow)).toBeTruthy();
    expect(stat('UEG Events')).toBe('—');
    expect(screen.queryByText(/^Event log unavailable/)).toBeNull();
  });

  it('a refused event log is said, and the verification is still shown', async () => {
    serve({ [EVENTS]: refused(502, 'the event index did not answer') });
    mount();
    await waitFor(() => expect(failures()).toContain(
      'Could not read the event log — Failed (HTTP 502): the event index did not answer'));
    expect(await screen.findByText('Event log unavailable — it could not be read, so this is not a log of none.')).toBeTruthy();
    await waitFor(() => expect(stat('UEG Events')).toBe(String(captured.verify.events)));
  });

  it('a refused read of the proposals is not shown as none', async () => {
    serve({ [PROPOSALS]: refused(503, 'the proposals store could not be read') });
    mount();
    await waitFor(() => expect(screen.getByTestId('proposals-unread').textContent?.trim()).toBe(
      'The proposals could not be read (Failed (HTTP 503): the proposals store could not be read), so this is not a list of none.'));
    expect(screen.queryByText('No proposals yet.')).toBeNull();
  });
});
