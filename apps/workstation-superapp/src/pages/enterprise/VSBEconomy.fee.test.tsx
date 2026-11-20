// W1125 (FU-1057 part 2, P5.16 clauses 3 and 4) — a cycle on the VSB Economy page says the platform's fee and what the
// entity's split was over, in the cycle's own words, and the board pack the fee the books carry.
//
// P5.16's ACCEPT asks that the cycle's answer and the entity's page show profit, fee and the base the split used. The
// page is mounted against what its routes answered on a fresh store (VSBEconomy.fee.fixture.json, captured by
// w1125_capture.py): on the apex, which pays no fee, and on a made-up registered entity opened by its id in the address,
// whose cycle posts a quarter of its profit. The cycle is run by the page's own button, with the page's own defaults;
// the two reads the page makes again after a cycle are served as they answered then. Virtual WST; nothing is charged.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBEconomy.fee.fixture.json';
import { VSBEconomy } from './VSBEconomy';

type Answer = { status: number; body: any; request?: unknown };
type Case = { vsb_id: string; opening: Record<string, Answer>; cycle: Answer; after: Record<string, Answer> };
const apex = captured.apex as unknown as Case;
const entity = captured.entity as unknown as Case;

//  each read as its route answered it; the press of the cycle as the route answered it; and after the cycle, the two
//  reads the page makes again as they answered then. What the page asked the cycle for is kept, to be read.
function serve(c: Case) {
  const asked: unknown[] = [];
  let ran = false;
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    let a: Answer | undefined;
    if (url === '/api/v1/economy/cycle' && init?.method === 'POST') {
      asked.push(JSON.parse(String(init.body)));
      ran = true;
      a = c.cycle;
    } else {
      a = (ran ? c.after[url] : undefined) ?? c.opening[url];
    }
    if (!a) return { ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) };
    const got = a;
    return { ok: got.status < 400, status: got.status, statusText: '', json: async () => got.body };
  }));
  return asked;
}

//  a Metric draws its value above its label
function metric(label: string): string | null {
  return screen.getByText(label, { selector: 'p' }).previousElementSibling?.textContent ?? null;
}

async function runCycle() {
  fireEvent.click(await screen.findByRole('button', { name: /Run Metabolic Cycle/ }));
}

describe('VSBEconomy, a cycle and the platform fee (P5.16)', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('on the apex, the cycle says it pays no fee and its split is over the whole profit, in the cycle\'s own words', async () => {
    const asked = serve(apex);
    render(<MemoryRouter><VSBEconomy /></MemoryRouter>);
    await runCycle();
    const cy = apex.cycle.body.cycle;
    expect([cy.platform_fee.fee_wst, cy.platform_fee.exempt, cy.split_base_wst]).toEqual([0, 'apex', cy.distributable_profit]);
    await waitFor(() => expect(screen.getByTestId('cycle-platform-fee').textContent).toBe(`Platform fee: ${cy.platform_fee.basis}.`));
    expect([metric('Distributable'), metric('Platform fee'), metric('Split over')]).toEqual(
      [cy.distributable_profit, 0, cy.split_base_wst].map((n: number) => n.toLocaleString()));
    expect(asked).toEqual([apex.cycle.request]);
  });

  it('on a registered entity, the cycle says the fee it took first and what the split was over, and the pack carries it', async () => {
    const asked = serve(entity);
    render(<MemoryRouter initialEntries={[`/economy?vsb=${entity.vsb_id}`]}><VSBEconomy /></MemoryRouter>);
    await runCycle();
    const cy = entity.cycle.body.cycle;
    expect([cy.platform_fee.posted, cy.platform_fee.fee_wst * 4, cy.split_base_wst + cy.platform_fee.fee_wst])
      .toEqual([true, cy.distributable_profit, cy.distributable_profit]);
    await waitFor(() => expect(screen.getByTestId('cycle-platform-fee').textContent).toBe(`Platform fee: ${cy.platform_fee.basis}.`));
    expect([metric('Distributable'), metric('Platform fee'), metric('Split over')]).toEqual(
      [cy.distributable_profit, cy.platform_fee.fee_wst, cy.split_base_wst].map((n: number) => n.toLocaleString()));
    const pl = entity.after[`/api/v1/economy/board-pack?vsb_id=${entity.vsb_id}&entity_type=waqf_ltd_hybrid`].body.profit_and_loss;
    expect(pl.total_platform_fee_wst).toBe(cy.platform_fee.fee_wst);
    await waitFor(() => expect(metric('Platform fee (cumulative)')).toBe(`${Number(pl.total_platform_fee_wst).toLocaleString()} WST`));
    expect(screen.getByTestId('pack-platform-fee').textContent).toBe(`Platform fee: ${pl.total_platform_fee_wst_basis}.`);
    expect(asked).toEqual([entity.cycle.request]);
  });
});
