// W992 (FU-399 part 24) — the Sovereign Evolution page, rendered against its routes' own answers.
//
// The page shows the evolution roadmap a curation cycle leaves, says whether a cycle also runs on the heartbeat, and
// runs a cycle. This mounts the real page against the answers its three routes gave on a fresh store
// (SovereignEvolution.fixture.json, captured by w992_capture.py: no cycle, then one), and has the server refuse each.
// A refusal says the server's reason, not yet read is not "could not be read", and no cycle run is said.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { provenanceMapBadge } from '../../lib/api';
import captured from './SovereignEvolution.fixture.json';
import { SovereignEvolution } from './SovereignEvolution';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const ROADMAP = '/api/v1/sovereign-evolution/roadmap';
const HEARTBEAT = '/api/v1/heartbeat/status';
const CYCLE = '/api/v1/sovereign-evolution/cycle';

//  a reply held back until the test lets it go, to see the page while a read is under way
function held(r: Reply) {
  let release: () => void = () => undefined;
  const gate = new Promise<void>(res => { release = res; });
  return { reply: r, gate, release: () => release() };
}

function serve(over: Record<string, Reply> = {}, wait: Record<string, Promise<void>> = {}) {
  const base: Record<string, Reply> = {
    [ROADMAP]: ok(captured.roadmap_none), [HEARTBEAT]: ok(captured.heartbeat), [CYCLE]: ok(captured.cycle),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url in wait) await wait[url];
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const basis = () => screen.getByTestId('evolution-autonomy-basis').textContent;

describe('SovereignEvolution, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('no cycle run is said, and the levers are said as the heartbeat reports them', async () => {
    serve();
    render(<SovereignEvolution />);
    await waitFor(() => expect(screen.getByTestId('evolution-no-cycle').textContent?.trim()).toBe(
      'No evolution cycle has run yet, so there is no roadmap to show. Run one above.'));
    expect(captured.heartbeat.auto_evolve).toBe(false);
    await waitFor(() => expect(basis()).toBe(
      'Running on the beat is OFF (the Self-evolve lever on the heartbeat), so a cycle happens only when you press the button below.'));
  });

  it('the levers are not said unread while they are being read', async () => {
    const h = held(ok(captured.heartbeat));
    serve({}, { [HEARTBEAT]: h.gate });
    render(<SovereignEvolution />);
    expect(basis()).toBe('Reading whether a cycle also runs on the beat…');
    h.release();
    await waitFor(() => expect(basis()).toMatch(/^Running on the beat is OFF/));
  });

  it('a refused read of the levers is said with its reason', async () => {
    serve({ [HEARTBEAT]: refused(503, 'the heartbeat is restarting') });
    render(<SovereignEvolution />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure').map(e => e.textContent)).toContain(
      'Could not read the heartbeat\'s levers — Failed (HTTP 503): the heartbeat is restarting'));
    expect(basis()).toBe('Whether a cycle also runs on the beat could not be read.');
  });

  it('a cycle that runs replaces "no cycle" with its roadmap', async () => {
    serve();
    render(<SovereignEvolution />);
    await screen.findByTestId('evolution-no-cycle');
    fireEvent.click(screen.getByRole('button', { name: /Run a Curation Cycle Now/ }));
    await waitFor(() => expect(screen.queryByTestId('evolution-no-cycle')).toBeNull());
    expect(screen.queryByTestId('evolution-error')).toBeNull();
  });

  // W1110 (FU-399 part 99) - the roadmap a cycle returns says, in its own words, when its readings were taken, what
  // served it, who curated it, where each directive came from and whether it carries a verdict, and the cycle before
  it('a cycle\'s roadmap says when it read, what served it, who curated it, each directive\'s source and verdict, and the cycle before', async () => {
    serve();
    render(<SovereignEvolution />);
    await screen.findByTestId('evolution-no-cycle');
    fireEvent.click(screen.getByRole('button', { name: /Run a Curation Cycle Now/ }));
    const c = captured.cycle;
    await waitFor(() => expect(screen.getByTestId('introspection-as-of').textContent).toBe(
      `cycle ${c.cycle_id} · ${c.duration_ms}ms · run ${c.created_at}`));
    expect(screen.getByTestId('introspection-staleness').textContent).toBe(
      'These are the readings that cycle took, not live values. Run a cycle to refresh them.');
    //  the cycle's answer carries no record of what served it, and the badge says that state, not a server
    expect(['served_by', 'any_external'].filter(k => k in c)).toEqual([]);
    const b = provenanceMapBadge(undefined, undefined);
    expect(screen.getByTestId('cycle-provenance').textContent).toBe(b.label);
    expect(screen.getByTestId('cycle-provenance').getAttribute('title')).toBe(b.title);
    expect(screen.getByTestId('evolution-curated-by').textContent).toBe(c.curated_by.join(' → '));
    expect(screen.getByTestId('evolution-curated-by').getAttribute('title')).toBe(c.curated_by_basis);
    const [d] = c.ceo_directives;
    expect([d.source, d.verdict]).toEqual(['default', null]);
    expect(screen.getByTestId('directive-defaulted').textContent).toBe(d.source_basis);
    expect(screen.getByTestId('directive-no-verdict').textContent).toBe('no C-Suite verdict');
    expect(screen.getByTestId('directive-no-verdict').getAttribute('title')).toBe(d.verdict_source);
    expect(c.previous_cycle.directives).toEqual([]);
    expect(screen.getByTestId('evolution-previous-cycle').querySelector('h3')?.textContent).toBe('What the previous cycle did');
    expect(screen.getByTestId('evolution-previous-basis').textContent).toBe(c.previous_cycle.basis);
  });

  it('a refused cycle says the server\'s reason', async () => {
    serve({ [CYCLE]: refused(503, 'the introspection could not be read') });
    render(<SovereignEvolution />);
    await screen.findByTestId('evolution-no-cycle');
    fireEvent.click(screen.getByRole('button', { name: /Run a Curation Cycle Now/ }));
    await waitFor(() => expect(screen.getByTestId('evolution-error').textContent).toBe(
      ' The cycle was not run: Failed (HTTP 503): the introspection could not be read'));
    expect(screen.getByTestId('evolution-no-cycle')).toBeTruthy();
  });
});
