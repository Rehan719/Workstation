// W1027 (FU-399 part 53) — the Religion hub, rendered against its one read's own answers.
//
// The hub's first tab lists the schools of jurisprudence from /api/v1/religion/schools (ReligionHub.fixture.json,
// captured on a fresh store: the route's answer, and the server's own 500 when the route fails inside, which names
// the failure's class and says its cause is not established). Its other
// tabs are tools that each have a rendered test of their own, so each is stood in for by a stub here, as are the
// Quran platform's panels on its QEP tab. Read here: the schools as the route lists them, the tab the address names, a
// tab it does not have, choosing a tab, and a failed read.
//
// Rendering found two defects, fixed in this round: the hub read ?tab= once, when it mounted, and never wrote it; and
// every failed read of the schools, a server's refusal included, was said as "Backend unreachable".
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('../../components/DomainTool', () => ({
  DomainTool: (p: { title: string; endpoint: string }) => <p>stub: tool {p.title} at {p.endpoint}</p>,
}));
vi.mock('../../components/QEPStudio', () => ({ QEPStudio: () => <p>stub: the Quran studio</p> }));
vi.mock('../../components/QEPFlagshipFeatures', () => ({ QEPFlagshipFeatures: () => <p>stub: the roadmap</p> }));
vi.mock('../../components/LearnTeachModule', () => ({ LearnTeachModule: () => <p>stub: learn and teach</p> }));

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import { toolsFor } from '../../lib/toolRegistry';
import captured from './ReligionHub.fixture.json';
import { ReligionHub } from './ReligionHub';

const T = toolsFor('/religion');
const SCHOOLS = '/api/v1/religion/schools';
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

function serve(read: 'answered' | 'failed' | 'unreached') {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url !== SCHOOLS) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (read === 'failed') throw axiosRefusal(captured.schools_failed.status, captured.schools_failed.body);
    if (read === 'unreached') throw Object.assign(new Error('Network Error'), { isAxiosError: true });
    return { status: 200, data: captured.schools } as never;
  });
}

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at: string) {
  render(
    <MemoryRouter initialEntries={[at]}>
      <AdaptiveUIProvider>
        <ReligionHub />
      </AdaptiveUIProvider>
      <Where />
    </MemoryRouter>,
  );
}

const at = () => screen.getByText(/^at: /).textContent;

describe('ReligionHub, rendered against its read\'s own answers', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('opens on the schools of jurisprudence, each as the route lists it', async () => {
    serve('answered');
    mount('/religion');
    const [first] = captured.schools.madhabs;
    await waitFor(() => expect(screen.getByText(first.name).textContent).toBe(first.name));
    for (const m of captured.schools.madhabs) {
      expect(screen.getByText(m.name)).toBeTruthy();
      expect(screen.getByText(m.region)).toBeTruthy();
      expect(screen.getByText(m.founder)).toBeTruthy();
    }
    expect(screen.queryByText(/^stub: tool /)).toBeNull();
  });

  it('a tab named by the address opens its tool, and a tab the hub does not have opens the schools', async () => {
    serve('answered');
    mount('/religion?tab=hadith');
    expect(screen.getByText(`stub: tool ${T.hadith.title} at /api/v1/religion/hadith-study`)).toBeTruthy();
    mount('/religion?tab=not-a-tab');
    const [first] = captured.schools.madhabs;
    await waitFor(() => expect(screen.getByText(first.name).textContent).toBe(first.name));
    mount('/religion?tab=qep');
    expect(screen.getByText('stub: the roadmap')).toBeTruthy();
  });

  it('choosing a tab writes it into the address, and the first tab clears it', async () => {
    serve('answered');
    mount('/religion');
    fireEvent.click(screen.getByRole('button', { name: 'Tafsir' }));
    await waitFor(() => expect(at()).toBe('at: /religion?tab=tafsir'));
    expect(screen.getByText(`stub: tool ${T.tafsir.title} at /api/v1/religion/quran-tafsir`)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Wisdom' }));
    await waitFor(() => expect(at()).toBe('at: /religion'));
  });

  it('says a failed read by what it was, and a server that answered is not said as unreachable', async () => {
    serve('failed');
    mount('/religion');
    await waitFor(() => expect(screen.getByTestId('religion-schools-failed').textContent).toBe(
      `The schools of jurisprudence could not be read: Failed (HTTP ${captured.schools_failed.status}): ${captured.schools_failed.body.detail}`));
    expect(screen.queryByText(/Backend unreachable/)).toBeNull();
    expect(screen.queryByText(/Loading jurisprudential traditions/)).toBeNull();
  });

  it('says a read that reached no server as one', async () => {
    serve('unreached');
    mount('/religion');
    await waitFor(() => expect(screen.getByTestId('religion-schools-failed').textContent).toBe(
      'The schools of jurisprudence could not be read: Failed — backend unreachable.'));
  });
});
