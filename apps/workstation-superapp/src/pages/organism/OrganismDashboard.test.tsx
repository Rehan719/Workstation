// W909 (FU-399 part 2) — the Metabolic card, rendered: the work budget left, its basis, and whether anything
// reads it.
//
// W902 (FU-1112, S18.1) replaced the card's simulated ATP ratio ("ATP ratio · simulated — cannot fall") with the
// figure the ruling says is DERIVED from the work budget. Every guard of that card in the Python suite reads the
// page's source, so none can say what a person looking at the card sees: a figure with its basis is a claim about
// what is RENDERED, the kind FU-399 converts. This mounts the real page against the API's own answers, captured
// from the app's routes (OrganismDashboard.fixture.json), and reads the card in the DOM.
import { render, screen, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './OrganismDashboard.fixture.json';
import { OrganismDashboard } from './OrganismDashboard';

type Metabolic = { energy_ratio: number | null; energy_acts: boolean; energy_basis: string };

// answer the page's three reads with the captured answers, the work budget's figure replaced where a case says so
function serve(metabolic?: Partial<Metabolic>) {
  const status = JSON.parse(JSON.stringify(captured.status));
  if (metabolic) Object.assign(status.systems.metabolic, metabolic);
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url.startsWith('/api/v1/organism/status')) return { status: 200, data: status } as never;
    if (url.startsWith('/api/v1/organism/signals')) return { status: 200, data: captured.signals } as never;
    if (url.startsWith('/api/v1/native-ai/homeostasis')) return { status: 200, data: captured.homeostasis } as never;
    return { status: 404, data: null } as never;
  });
  return status.systems.metabolic as Metabolic;
}

async function metabolicCard() {
  render(
    <MemoryRouter>
      <OrganismDashboard />
    </MemoryRouter>,
  );
  const figure = await screen.findByTestId('organism-work-budget-left');
  const card = figure.closest('.rounded-xl') as HTMLElement;
  expect(within(card).getByText('Metabolic')).toBeTruthy();       // the card the figure sits in, and no other
  return { figure, card };
}

describe('OrganismDashboard, the Metabolic card, rendered', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('shows the work budget left with its basis, and says nothing reads it while the budget is switched off', async () => {
    const m = serve();                                                // as the app answers on an empty store
    expect(m.energy_acts).toBe(false);
    const { figure, card } = await metabolicCard();
    expect(figure.textContent).toBe(`${Math.round((m.energy_ratio as number) * 100)}%`);
    const basis = within(card).getByText(/work budget left ·/);
    expect(basis.getAttribute('title')).toBe(m.energy_basis);        // the basis is on the figure's own line
    expect(basis.textContent).toContain('read by nothing while the budget is switched off');
    // the simulated ratio W902 retired is not what the card prints
    expect(card.textContent).not.toMatch(/ATP ratio/);
    expect(card.textContent).not.toMatch(/simulated/);
  });

  it('with the budget switched on and nine-tenths spent, shows 10% and says the energy thresholds read it', async () => {
    serve({
      energy_ratio: 0.1,
      energy_acts: true,
      energy_basis: '1 - 3240.0s spent / 3600s stated capacity this window (the capacity is a stated assumption)',
    });
    const { figure, card } = await metabolicCard();
    expect(figure.textContent).toBe('10%');
    const basis = within(card).getByText(/work budget left ·/);
    expect(basis.textContent).toContain('the energy thresholds read it');
    expect(basis.getAttribute('title')).toContain('3240.0s spent');
  });

  it('shows a dash, not a number, when the budget cannot be read', async () => {
    serve({ energy_ratio: null });
    const { figure } = await metabolicCard();
    expect(figure.textContent).toBe('—');
  });
});
