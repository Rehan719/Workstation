// W984 (FU-399 part 16) — the Command Center (the home page, "/"), rendered against its routes' own answers.
//
// The home is the first page a person sees: what they are working on, this machine's figures, whether the organism
// runs itself, and its health. This mounts the real page against the answers its four routes gave on a fresh store
// (DashboardNew.fixture.json, captured by w984_capture.py: no project, then one made-up project), and has the server
// refuse each read, or not answer at all.
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DashboardNew.fixture.json';
import { DashboardNew } from './DashboardNew';

type Reply = { status: number; data: unknown } | 'unreachable';
const ok = (data: unknown): Reply => ({ status: 200, data });
const refused = (status: number, detail: string): Reply => ({ status, data: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    '/api/v1/projects/': ok(captured.projects_empty),
    '/api/v1/projects/stats/summary': ok(captured.stats),
    '/api/v1/heartbeat/status': ok(captured.heartbeat),
    '/api/v1/organism/status': ok(captured.organism),
  };
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    const r = url in a ? a[url] : base[url];
    if (r === 'unreachable') throw Object.assign(new Error('Network Error'), { isAxiosError: true });
    if (!r) throw Object.assign(new Error('not served in this test'), { isAxiosError: true, response: { status: 404, data: {} } });
    if (r.status >= 400) {
      throw Object.assign(new Error(`Request failed with status code ${r.status}`),
                          { isAxiosError: true, response: { status: r.status, data: r.data } });
    }
    return r as never;
  });
  //  the page's other components (what serves now) read through fetch: answered, not part of this test
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 404, statusText: '', json: async () => ({}) })));
}

function mount() {
  return render(
    <MemoryRouter>
      <DashboardNew />
    </MemoryRouter>,
  );
}

const UNREACHABLE = 'Backend unreachable — start the backend server to see live status';

describe('DashboardNew (the home), rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('no project yet is said as none, and a project made is listed by its title', async () => {
    serve();
    const a = mount();
    expect(await screen.findByText('No projects yet — start a Genesis or open a Domain tool')).toBeTruthy();
    a.unmount();
    vi.restoreAllMocks();

    serve({ '/api/v1/projects/': ok(captured.projects) });
    mount();
    expect(await screen.findByText(String(captured.projects[0].title))).toBeTruthy();
    expect(screen.queryByText('No projects yet — start a Genesis or open a Domain tool')).toBeNull();
  });

  it('a refused read of the projects is said with the server\'s reason, never as an unreachable server', async () => {
    serve({ '/api/v1/projects/': refused(500, 'the project store could not be read') });
    mount();
    expect(await screen.findByText(
      'Your projects could not be read (Failed (HTTP 500): the project store could not be read), so this is not a list of none.')).toBeTruthy();
    expect(screen.queryByText(UNREACHABLE)).toBeNull();
    expect(screen.queryByText('No projects yet — start a Genesis or open a Domain tool')).toBeNull();
  });

  it('a server that cannot be reached is said to be unreachable', async () => {
    serve({ '/api/v1/projects/': 'unreachable' });
    mount();
    expect(await screen.findByText(UNREACHABLE)).toBeTruthy();
  });

  it('the levers are the heartbeat\'s own: none on; one set while the heartbeat is stopped; and unread', async () => {
    const keys = ['auto_evolve', 'auto_economy', 'auto_align', 'auto_compliance', 'auto_ship'];
    serve();
    const a = mount();
    // before the heartbeat has answered, its levers are being read - not "could not be read"
    expect(screen.getByTestId('autonomy-levers').textContent).toBe('Reading the heartbeat levers…');
    await waitFor(() => expect(screen.getByTestId('autonomy-levers').textContent).toContain(
      `Self-running is a set of ${keys.length} heartbeat levers and none is on`));
    a.unmount();
    vi.restoreAllMocks();

    const one = clone(captured.heartbeat);
    one.auto_economy = true;
    one.running = false;
    serve({ '/api/v1/heartbeat/status': ok(one) });
    const b = mount();
    await waitFor(() => expect(screen.getByTestId('autonomy-levers').textContent).toContain(
      `1 of ${keys.length} heartbeat levers are set (economy), but the`));
    b.unmount();
    vi.restoreAllMocks();

    serve({ '/api/v1/heartbeat/status': refused(503, 'the heartbeat could not be read') });
    mount();
    await waitFor(() => expect(screen.getByTestId('autonomy-levers').textContent).toBe(
      'Self-running is a set of heartbeat levers; their state could not be read.'));
  });

  it('the health shown is the measured part only, and the blend is said as part unmeasured', async () => {
    serve();
    mount();
    const o = captured.organism as { composite_health: number; composite_health_measured_only: number | null;
      composite_health_terms: Record<string, { weight?: number; measured?: boolean }> };
    expect(o.composite_health_measured_only).toBeNull();
    const unmeasured = Object.entries(o.composite_health_terms).filter(([, t]) => t && t.measured === false);
    const share = unmeasured.reduce((s, [, t]) => s + (Number(t.weight) || 0), 0);
    const basis = await screen.findByTestId('home-composite-health-basis');
    expect(basis.textContent).toContain(
      `The blended composite is ${Math.round(o.composite_health * 100)}%, of which ${Math.round(share * 100)}% is not measured`);
    expect(screen.getAllByText(/not measured/).length).toBeGreaterThan(0);
  });

  it('a refused read of this machine\'s figures is said with the server\'s reason', async () => {
    serve({ '/api/v1/projects/stats/summary': refused(503, 'the host figures could not be read') });
    mount();
    expect((await screen.findAllByTestId('read-failure')).map(p => p.textContent)).toContain(
      'Could not read this machine\'s figures — Failed (HTTP 503): the host figures could not be read');
  });
});
