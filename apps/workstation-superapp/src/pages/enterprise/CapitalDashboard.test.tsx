// W910 (FU-399 part 3) — the Capital Fund's figures, rendered with their bases.
//
// Ledger v17 FU-977: the page showed the pool as "the real capital fund" and HEALTHY, and dropped the API's own
// statements that most of the pool is an unfunded seed and that the health word is a ratio against it. The guard
// that fixed it (test_t2_the_capital_fund_page_prints_the_seed_split_and_the_health_basis) reads the page's source.
// What a person sees on the page is a claim about what is RENDERED, the kind FU-399 converts. This mounts the real
// page against the API's own answers, captured from the app's routes (CapitalDashboard.fixture.json), and reads the
// figures in the DOM: each basis beside its figure, and a chip that says so when the store could not be read whole.
import { render, screen } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './CapitalDashboard.fixture.json';
import { CapitalDashboard } from './CapitalDashboard';

type Fund = Record<string, unknown>;

// answer the page's four reads with the captured answers, the fund's fields replaced where a case says so
function serve(fund?: Fund) {
  const f = { ...JSON.parse(JSON.stringify(captured.fund)), ...(fund ?? {}) };
  const answers: Record<string, unknown> = {
    '/api/v1/fund/status': f,
    '/api/v1/heartbeat/status': captured.heartbeat,
    '/api/v1/cca': captured.cca,
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const data = answers[String(url)];
    return data === undefined
      ? { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: 'not served here' }) }
      : { ok: true, status: 200, statusText: 'OK', json: async () => data };
  }));
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => (
    url.startsWith('/api/v1/projects/stats/summary')
      ? { status: 200, data: captured.portfolio }
      : { status: 404, data: null }) as never);
  return f;
}

function mount() {
  return render(
    <MemoryRouter>
      <CapitalDashboard />
    </MemoryRouter>,
  );
}

describe('CapitalDashboard, the fund figures, rendered', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows the seed split and the health basis the API states, and no chip when the store was read whole', async () => {
    const f = serve();                                               // as the app answers on an empty store
    mount();
    expect((await screen.findByTestId('fund-capital-basis')).textContent).toBe(f.capital_basis);
    expect(screen.getByTestId('fund-health-basis').textContent).toBe(`${f.fund_health}: ${f.fund_health_basis}`);
    expect(screen.getByTestId('fund-contributed').textContent).toContain('contributed by cycles:');
    expect(screen.getByTestId('fund-set-aside').textContent).toBe(
      (f.set_aside_reconciliation as { basis: string }).basis);
    expect(screen.queryByTestId('fund-balances-incomplete')).toBeNull();
    expect(screen.queryByTestId('fund-health-incomplete')).toBeNull();
    // FU-977: the pool is not presented as the real capital fund
    expect(document.body.textContent).not.toMatch(/the real capital fund/i);
  });

  it('says on both figures when the fund store could not be read whole, each chip carrying its basis', async () => {
    serve({
      balances_are_incomplete: true,
      balances_basis: 'the fund store could not be read whole: 2 allocation rows were unreadable',
      fund_health_is_incomplete: true,
      fund_health_incomplete_basis: 'allocations are missing from this reading: 2 rows could not be read',
    });
    mount();
    const balances = await screen.findByTestId('fund-balances-incomplete');
    expect(balances.textContent).toContain('may be OVERSTATED');
    expect(balances.getAttribute('title')).toContain('could not be read whole');
    const health = screen.getByTestId('fund-health-incomplete');
    expect(health.textContent).toContain('OPTIMISTIC');
    expect(health.getAttribute('title')).toContain('allocations are missing');
  });

  it('prints no contributed line when the API states no contributed figure, rather than a zero', async () => {
    serve({ contributed_wst: null });
    mount();
    await screen.findByTestId('fund-capital-basis');
    expect(screen.queryByTestId('fund-contributed')).toBeNull();
  });
});
