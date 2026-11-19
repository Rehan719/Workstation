// W1017 (FU-399 part 41) — the governance centre, rendered: its tabs choose what is shown, and the address says which.
//
// GovernanceCenter is a row of tabs over pages that each have a rendered test of their own, so each page is stood in for by
// a stub here and only the hub's own work is read: which page it opens on, that the address names the tab shown,
// that a tab it does not have opens the first one, and that choosing a tab writes it into the address (the first
// tab clears it). Nothing is fetched by the hub itself.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

vi.mock('./GovernanceHub', () => ({ GovernanceHub: () => <p>stub: overview</p> }));
vi.mock('./ConstitutionalUI', () => ({ ConstitutionalUI: () => <p>stub: constitution</p> }));
vi.mock('./ComplianceChecker', () => ({ ComplianceChecker: () => <p>stub: compliance</p> }));
vi.mock('./DeliveryMethod', () => ({ DeliveryMethod: () => <p>stub: method</p> }));
vi.mock('./MethodAppraisal', () => ({ MethodAppraisal: () => <p>stub: appraisal</p> }));
vi.mock('./ReviewRecords', () => ({ ReviewRecords: () => <p>stub: review</p> }));

import { GovernanceCenter } from './GovernanceCenter';

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at: string) {
  render(<MemoryRouter initialEntries={[at]}><GovernanceCenter /><Where /></MemoryRouter>);
}

describe('GovernanceCenter, rendered: the tab shown is the tab the address names', () => {
  it('opens on its first tab, and a tab it does not have opens the first one', () => {
    mount('/');
    expect(screen.getByText('stub: overview')).toBeTruthy();
    mount('/?tab=not-a-tab');
    expect(screen.getAllByText('stub: overview')).toHaveLength(2);
  });

  it.each([
    ['overview', 'Governance'],
    ['constitution', 'Constitution'],
    ['compliance', 'Compliance'],
    ['method', 'Method'],
    ['appraisal', 'Appraisal'],
    ['review', 'Review'],
  ])('the address ?tab=%s shows that tab', (id, _name) => {
    mount(id === 'overview' ? '/' : `/?tab=${id}`);
    expect(screen.getByText(`stub: ${id}`)).toBeTruthy();
  });

  it('choosing a tab writes it into the address, and the first tab clears it', async () => {
    mount('/');
    fireEvent.click(screen.getByRole('button', { name: /Constitution/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /?tab=constitution'));
    expect(screen.getByText('stub: constitution')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /Governance/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /'));
    expect(screen.getByText('stub: overview')).toBeTruthy();
  });
});
