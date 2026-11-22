// W1117 (FU-399 part 106) — WHAT GENERATING AN ENTITY COSTS, rendered against the price route's own answers.
//
// The Genesis journey's price panel says the price the Owner set, that it is credited against the platform's fees,
// and that nothing is charged until three things exist, each said as existing or not. The Genesis page's test serves
// the price, so the panel was drawn there, but no test read what it said. This mounts the real panel against what the
// route answered on a fresh store (GenerationPrice.fixture.json, captured by w1117_capture.py): the standing price,
// and the route's own answer for an entity that distributes nothing, which is waived and credits nothing. The panel
// always asks for the standing price; the waived answer is served at its read to draw the branch kept for it.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './GenerationPrice.fixture.json';
import { GenerationPrice } from './GenerationPrice';

type Answer = { status: number; body: unknown };
type Condition = { condition: string; met: boolean; basis: string };

//  the panel's one read answers what the route answered, or fails as a server out of reach does; what was asked is kept
function serve(a: Answer | Error) {
  const sent: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    sent.push(url);
    if (a instanceof Error) throw a;
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
  return sent;
}

//  a condition, as the route states it: whether it exists, what it is, and how that was read
const said = (c: Condition) => `${c.met ? 'exists' : 'does not exist yet'} · ${c.condition} — ${c.basis}`;

describe('GenerationPrice, what generating an entity costs, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('the standing price: its basis, the credit, that nothing is charged and why, and each condition', async () => {
    const p = captured.standing.body;
    const sent = serve(captured.standing);
    render(<GenerationPrice />);
    await waitFor(() => expect(screen.getByTestId('generation-price-basis').textContent).toBe(`${p.price_basis}.`));
    expect(sent).toEqual([captured.standing.url]);
    expect(screen.getByTestId('generation-price').querySelector('p')?.textContent).toBe('what generating an entity costs');
    expect(p.credited_against_first_profit_share).toBe(true);
    expect(screen.getByTestId('generation-price-credit').textContent).toBe(`${p.credit_basis}.`);
    expect(p.waived).toBe(false);
    expect(screen.queryByTestId('generation-price-waived')).toBeNull();
    expect(p.charged_now).toBe(false);
    expect(screen.getByTestId('generation-price-not-charged').textContent).toBe(`${p.not_charged_basis}.`);
    expect(screen.getAllByTestId('generation-price-condition').map(e => e.textContent)).toEqual(
      (p.conditions as Condition[]).map(said));
    expect(screen.queryByTestId('generation-price-unread')).toBeNull();
  });

  it('an entity that distributes nothing: the price waived with its basis, and nothing credited, since nothing is owed', async () => {
    const w = captured.non_distributing.body;
    serve(captured.non_distributing);
    render(<GenerationPrice />);
    await waitFor(() => expect(screen.getByTestId('generation-price-waived').textContent).toBe(`${w.waived_basis}.`));
    expect(screen.getByTestId('generation-price-basis').textContent).toBe(`${w.price_basis}.`);
    expect(w.credited_against_first_profit_share).toBe(false);
    expect(screen.queryByTestId('generation-price-credit')).toBeNull();
    expect(screen.getByTestId('generation-price-not-charged').textContent).toBe(`${w.not_charged_basis}.`);
    expect(screen.getAllByTestId('generation-price-condition').map(e => e.textContent)).toEqual(
      (w.conditions as Condition[]).map(said));
  });

  it('a read that fails is said as unread, and no price is shown', async () => {
    serve(new TypeError('Failed to fetch'));
    render(<GenerationPrice />);
    await waitFor(() => expect(screen.getByTestId('generation-price-unread').textContent).toBe(
      'The price of generating an entity could not be read just now, so none is shown.'));
    expect(screen.queryByTestId('generation-price')).toBeNull();
    expect(screen.queryByTestId('generation-price-basis')).toBeNull();
  });
});
