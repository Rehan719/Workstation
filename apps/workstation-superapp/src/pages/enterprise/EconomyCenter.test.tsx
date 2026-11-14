// W1017 (FU-399 part 41) — the economy centre, rendered: its tabs choose what is shown, and the address says which.
//
// EconomyCenter is a row of tabs over pages that each have a rendered test of their own, so each page is stood in for by
// a stub here and only the hub's own work is read: which page it opens on, that the address names the tab shown,
// that a tab it does not have opens the first one, and that choosing a tab writes it into the address (the first
// tab clears it). Nothing is fetched by the hub itself.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

vi.mock('./VSBEconomy', () => ({ VSBEconomy: () => <p>stub: overview</p> }));
vi.mock('./CapitalDashboard', () => ({ CapitalDashboard: () => <p>stub: capital</p> }));
vi.mock('../profile/Wallet', () => ({ Wallet: () => <p>stub: wallet</p> }));

import { EconomyCenter } from './EconomyCenter';

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at: string) {
  render(<MemoryRouter initialEntries={[at]}><EconomyCenter /><Where /></MemoryRouter>);
}

describe('EconomyCenter, rendered: the tab shown is the tab the address names', () => {
  it('opens on its first tab, and a tab it does not have opens the first one', () => {
    mount('/');
    expect(screen.getByText('stub: overview')).toBeTruthy();
    mount('/?tab=not-a-tab');
    expect(screen.getAllByText('stub: overview')).toHaveLength(2);
  });

  it.each([
    ['overview', 'Economy'],
    ['capital', 'Capital Fund'],
    ['wallet', 'Wallet'],
  ])('the address ?tab=%s shows that tab', (id, _name) => {
    mount(id === 'overview' ? '/' : `/?tab=${id}`);
    expect(screen.getByText(`stub: ${id}`)).toBeTruthy();
  });

  it('choosing a tab writes it into the address, and the first tab clears it', async () => {
    mount('/');
    fireEvent.click(screen.getByRole('button', { name: /Capital Fund/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /?tab=capital'));
    expect(screen.getByText('stub: capital')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /Economy/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /'));
    expect(screen.getByText('stub: overview')).toBeTruthy();
  });
});
