// W1027 (FU-399 part 52) — the Employment hub, rendered: its tabs choose the tool shown, and the address says which.
//
// The hub is a row of tabs over tools that each have a rendered test of their own (DomainTool.test.tsx,
// ApplicationStudio.test.tsx), so each tool is stood in for by a stub here and only the hub's own work is read: it
// opens on the CV tools, the address names the tab shown, a tab it does not have opens the CV tools, choosing a tab
// writes it into the address (the first tab clears it, and the address keeps what else it carries), the header's two
// buttons open their tools, and an address that changes while the hub is open is followed. Nothing is fetched by the
// hub itself.
//
// Rendering found two defects, fixed in this round: the hub read ?tab= once, when it mounted, and never wrote it; and an
// address naming a tab it does not have showed "Select an engine to begin." with no tab chosen.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { Link, MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

vi.mock('../../components/DomainTool', () => ({
  DomainTool: (p: { title: string; endpoint: string }) => <p>stub: tool {p.title} at {p.endpoint}</p>,
}));
vi.mock('../../components/employment/ApplicationStudio', () => ({
  ApplicationStudio: (p: { title: string }) => <p>stub: studio {p.title}</p>,
}));

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import { toolsFor } from '../../lib/toolRegistry';
import { EmploymentHub } from './EmploymentHub';

const T = toolsFor('/employment');
const SHOWN: Record<string, string> = {
  studio: `stub: studio ${T.studio.title}`,
  cv: `stub: tool ${T.cv.title} at /api/v1/employment/cv`,
  cover: `stub: tool ${T.cover.title} at /api/v1/employment/cover-letter`,
  application: `stub: tool ${T.application.title} at /api/v1/employment/application`,
  interview: `stub: tool ${T.interview.title} at /api/v1/employment/interview-prep`,
  path: `stub: tool ${T.path.title} at /api/v1/employment/career-path`,
  salary: `stub: tool ${T.salary.title} at /api/v1/employment/salary-negotiation`,
};

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at: string) {
  render(
    <MemoryRouter initialEntries={[at]}>
      <AdaptiveUIProvider>
        <EmploymentHub />
      </AdaptiveUIProvider>
      <Where />
      <Link to="/employment?tab=salary">W1027 made up: a link to the salary tool</Link>
    </MemoryRouter>,
  );
}

const at = () => screen.getByText(/^at: /).textContent;

describe('EmploymentHub, rendered: the tool shown is the tab the address names', () => {
  it('opens on the CV tools, and a tab it does not have opens them too', () => {
    mount('/employment');
    expect(screen.getByText(SHOWN.cv)).toBeTruthy();
    mount('/employment?tab=not-a-tab');
    expect(screen.getAllByText(SHOWN.cv)).toHaveLength(2);
    expect(screen.queryByText(/Select an engine/)).toBeNull();
  });

  it.each(Object.keys(SHOWN))('the address ?tab=%s shows that tool', id => {
    mount(id === 'cv' ? '/employment' : `/employment?tab=${id}`);
    expect(screen.getByText(SHOWN[id])).toBeTruthy();
    expect(Object.values(SHOWN).filter(s => screen.queryByText(s)).length).toBe(1);
  });

  it('choosing a tab writes it into the address, the first tab clears it, and the rest of the address stays', async () => {
    mount('/employment?from=w1027');
    fireEvent.click(screen.getByRole('button', { name: 'Cover Letter' }));
    await waitFor(() => expect(at()).toBe('at: /employment?from=w1027&tab=cover'));
    expect(screen.getByText(SHOWN.cover)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'CV Tailor' }));
    await waitFor(() => expect(at()).toBe('at: /employment?from=w1027'));
    expect(screen.getByText(SHOWN.cv)).toBeTruthy();
  });

  it('the header\'s buttons open their tools, and the address says which', async () => {
    mount('/employment');
    const [header] = screen.getAllByRole('button', { name: /Career Path/ });
    fireEvent.click(header);
    await waitFor(() => expect(at()).toBe('at: /employment?tab=path'));
    expect(screen.getByText(SHOWN.path)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /New Opportunity/ }));
    await waitFor(() => expect(at()).toBe('at: /employment?tab=studio'));
    expect(screen.getByText(SHOWN.studio)).toBeTruthy();
  });

  it('an address that changes while the hub is open is followed', async () => {
    mount('/employment?tab=cover');
    expect(screen.getByText(SHOWN.cover)).toBeTruthy();
    fireEvent.click(screen.getByText('W1027 made up: a link to the salary tool'));
    await waitFor(() => expect(at()).toBe('at: /employment?tab=salary'));
    expect(screen.getByText(SHOWN.salary)).toBeTruthy();
    expect(screen.queryByText(SHOWN.cover)).toBeNull();
  });
});
