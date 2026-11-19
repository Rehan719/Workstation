// W1047 (FU-399 part 66) — the VSB Economy page, rendered against its routes' own answers.
//
// On opening, the page reads the entity forms, the living entities, the apex's owner payments, its board pack and its
// waterfall, and its panels read the ventures, the transfers, the charity directives and the service contracts. This
// mounts the real page against what each route answered on a fresh store (VSBEconomy.fixture.json, captured by
// w1047_capture.py; nothing was posted), and against the living entities' route's own 500. Rendering found four reads
// whose failure was a fixed sentence, fixed in this round: the living entities' dropped every refusal's reason, and the
// owner payments', the board pack's and the waterfall's said nothing of a call that reached no server.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBEconomy.fixture.json';
import { VSBEconomy } from './VSBEconomy';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;

//  each read as its route answered it; a path given as unreached throws as fetch does when no server answers, and the
//  living entities can be given their route's own 500
function serve(o: { livingFailed?: boolean; unreached?: string[] } = {}) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if ((o.unreached ?? []).some(p => url.startsWith(p))) throw new TypeError('Failed to fetch');
    const a = o.livingFailed && url === '/api/v1/economy/living-vsbs' ? captured.living_failed : answers[url];
    if (!a) return { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
}

function mount() {
  return render(<MemoryRouter><VSBEconomy /></MemoryRouter>);
}

const FAILURES = ['living-error', 'owner-payments-error', 'board-pack-error', 'waterfall-error'];

describe('VSBEconomy, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  // W1112 (FU-399 part 101) - what the answers say, read where the page draws it: that the books are a simulation's,
  // who a payout would go to, the charity pot's label, the P&L's basis and result before distributions, and the
  // organism's posture beside the pack
  it('says the simulation, the payee, the charity label, the P&L\'s basis and the organism\'s posture in the answers\' own words', async () => {
    serve();
    mount();
    type Pack = {
      registration: string; registration_basis: string; charitable_giving: { label: string; basis: string };
      statements: { profit_and_loss: { net_profit_basis: string; operating_result_before_distributions_wst: number; distributions_wst: number } };
      organism_posture: { energy_ratio: number; composite_health: number; composite_health_measured_only: number | null; composite_health_basis: string };
    };
    type Payments = { owner: string | null; owner_recorded: boolean; owner_basis: string; account_name: string | null; simulated: boolean };
    const bp = answers['/api/v1/economy/board-pack?vsb_id=workstation-idbo&entity_type=waqf_ltd_hybrid'].body as Pack;
    const pay = answers['/api/v1/economy/owner-payments?vsb_id=workstation-idbo'].body as Payments;
    expect([bp.registration, pay.simulated]).toEqual(['UNREGISTERED', false]);
    await waitFor(() => expect(screen.getByTestId('economy-simulation-notice').textContent).toBe(
      `SIMULATION — ${bp.registration_basis} Its funds are not transferred or invested into registered entities,`
      + ' and it pays nothing into the shared capital fund.'));
    expect([pay.owner_recorded, pay.account_name]).toEqual([false, null]);
    const governed = screen.getByTestId('owner-payout-governed');
    expect(governed.textContent).toBe(
      'Every payout is held at Change Control for the decision of a person, whatever its amount. A request pays nothing;'
      + ' once it is approved there, request the same amount again to apply it. The payee is the owner the entity\'s'
      + ' record names, not the name stored on the account: none - the entity has no owner record.');
    expect(governed.querySelector('span')?.getAttribute('title')).toBe(pay.owner_basis);
    expect(screen.getByTestId('pack-charity-label').textContent).toBe(bp.charitable_giving.label);
    expect(screen.getByTestId('pack-charity-label').getAttribute('title')).toBe(bp.charitable_giving.basis);
    const pnl = bp.statements.profit_and_loss;
    expect(screen.getByTestId('pnl-net-basis').textContent).toBe(pnl.net_profit_basis);
    expect(screen.getByTestId('pnl-operating').textContent).toBe(
      `before distributions: ${pnl.operating_result_before_distributions_wst.toLocaleString()} WST`
      + ` · distributed ${pnl.distributions_wst.toLocaleString()} WST`);
    const po = bp.organism_posture;
    expect(po.composite_health_measured_only).toBeNull();
    expect(screen.getByTestId('vsb-organism-posture').textContent).toBe(
      `work budget left ${Math.round(po.energy_ratio * 100)}% · health not measured · blended ${Math.round(po.composite_health * 100)}%`);
    expect(screen.getByTestId('vsb-organism-posture').getAttribute('title')).toBe(po.composite_health_basis);
  });

  it('opens on what each read answered, and says no failure', async () => {
    serve();
    mount();
    expect(await screen.findByTestId('owner-share-reconciliation')).toBeTruthy();
    expect(await screen.findByTestId('form-in-force')).toBeTruthy();
    for (const id of FAILURES) expect(screen.queryByTestId(id)).toBeNull();
  });

  it('a failed read of the living entities says the route\'s own reason', async () => {
    serve({ livingFailed: true });
    mount();
    await waitFor(() => expect(screen.getByTestId('living-error').textContent).toBe(
      `Could not load the living entities, so nothing is shown rather than stale figures: Failed (HTTP 500): ${captured.living_failed.body.detail}`));
  });

  it('a read that reached no server says so, and what it leaves empty', async () => {
    serve({ unreached: ['/api/v1/economy/owner-payments', '/api/v1/economy/board-pack', '/api/v1/economy/waterfall'] });
    mount();
    await waitFor(() => expect(screen.getByTestId('owner-payments-error').textContent).toBe(
      'Could not load the owner payments, so nothing is shown rather than zero balances: Failed — backend unreachable.'));
    await waitFor(() => expect(screen.getByTestId('board-pack-error').textContent).toBe(
      'Could not load the board pack, so nothing is shown rather than stale figures: Failed — backend unreachable.'));
    await waitFor(() => expect(screen.getByTestId('waterfall-error').textContent).toBe(
      "Could not load the waterfall, so nothing is shown rather than another entity's split: Failed — backend unreachable."));
  });
});
