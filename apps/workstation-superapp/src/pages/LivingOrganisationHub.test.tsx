// W1017 (FU-399 part 41) — the living organisation hub, rendered: its tabs choose what is shown, and the address says which.
//
// LivingOrganisationHub is a row of tabs over pages that each have a rendered test of their own, so each page is stood in for by
// a stub here and only the hub's own work is read: which page it opens on, that the address names the tab shown,
// that a tab it does not have opens the first one, and that choosing a tab writes it into the address (the first
// tab clears it). Nothing is fetched by the hub itself.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

vi.mock('./CEOChat', () => ({ CEOChat: () => <p>stub: ceo</p> }));
vi.mock('./enterprise/BoardOfDirectors', () => ({ BoardOfDirectors: () => <p>stub: board</p> }));
vi.mock('../components/organism/SwarmIntelligence', () => ({ default: () => <p>stub: swarm</p> }));
vi.mock('../components/organism/AgentHubPanel', () => ({ default: () => <p>stub: hub</p> }));

import { LivingOrganisationHub } from './LivingOrganisationHub';

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at: string) {
  render(<MemoryRouter initialEntries={[at]}><LivingOrganisationHub /><Where /></MemoryRouter>);
}

describe('LivingOrganisationHub, rendered: the tab shown is the tab the address names', () => {
  it('opens on its first tab, and a tab it does not have opens the first one', () => {
    mount('/');
    expect(screen.getByText('stub: ceo')).toBeTruthy();
    mount('/?tab=not-a-tab');
    expect(screen.getAllByText('stub: ceo')).toHaveLength(2);
  });

  it.each([
    ['ceo', 'AI CEO'],
    ['board', 'Board'],
    ['swarm', 'Swarm'],
    ['hub', 'Agent Hub'],
  ])('the address ?tab=%s shows that tab', (id, _name) => {
    mount(id === 'ceo' ? '/' : `/?tab=${id}`);
    expect(screen.getByText(`stub: ${id}`)).toBeTruthy();
  });

  it('choosing a tab writes it into the address, and the first tab clears it', async () => {
    mount('/');
    fireEvent.click(screen.getByRole('button', { name: /Board/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /?tab=board'));
    expect(screen.getByText('stub: board')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /AI CEO/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /'));
    expect(screen.getByText('stub: ceo')).toBeTruthy();
  });

  it('the composer it no longer holds is sent to the native designer, where it lives', async () => {
    //  read through the address alone: a route element in a test is counted as the app defining routes (W499)
    mount('/?tab=composer');
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /native-ai?focus=cascade-designer'));
  });
});
