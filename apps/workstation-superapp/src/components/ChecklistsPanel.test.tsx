// W1168 (P5.11 clause 8) — what to gather, rendered against the route's own answer
// (ChecklistsPanel.fixture.json is what GET /api/v1/law/checklists gave on a fresh store, taken by w1168_capture.py; the
// suite holds it equal to what the route returns). Every item is in the words of the page that gives it.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ChecklistsPanel.fixture.json';
import ChecklistsPanel from './ChecklistsPanel';

type Reply = { status: number; body: unknown };

function serve(reply: Reply) {
  const urls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    urls.push(url);
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
  return urls;
}

const texts = (box: Element, id: string) => Array.from(box.querySelectorAll(`[data-testid="${id}"]`)).map(e => e.textContent);

describe("ChecklistsPanel, rendered against the route's own answer", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('each list is the page\'s own words, with the part of the page, its nations and the day it was read', async () => {
    const urls = serve({ status: 200, body: captured.checklists });
    render(<ChecklistsPanel />);
    const box = await screen.findByTestId('law-checklists');
    await screen.findAllByTestId('checklist');
    const lists = captured.checklists.checklists;
    expect(texts(box, 'checklist-subject')).toEqual(lists.map(c => c.subject));
    expect(texts(box, 'checklist-nations')).toEqual(['For England, Wales and Scotland.', 'For England and Wales.']);
    expect(texts(box, 'checklist-elsewhere')).toEqual(lists.filter(c => c.elsewhere).map(c => c.elsewhere));
    expect(texts(box, 'checklist-heading')).toEqual(lists.flatMap(c => c.groups.map(g => `${g.heading} (the page's part "${g.part}")`)));
    expect(texts(box, 'checklist-lead')).toEqual(lists.flatMap(c => c.groups.filter(g => g.lead).map(g => g.lead)));
    expect(texts(box, 'checklist-item')).toEqual(lists.flatMap(c => c.groups.flatMap(g => g.items)));
    expect(texts(box, 'checklist-read')).toEqual(lists.map(c => `Read: ${c.sources.map(s => `${s.name}, ${s.checked}`).join('; ')}.`));
    expect(texts(box, 'checklist-here')).toEqual(lists.filter(c => c.here).map(c => c.here));
    expect(screen.getByTestId('law-checklists-basis').textContent).toBe(captured.checklists.basis);
    expect(urls).toEqual(['/api/v1/law/checklists']);
  });

  it('lists that could not be read are said in their place, never as none', async () => {
    serve({ status: 503, body: { detail: 'the register of sources could not be read' } });
    render(<ChecklistsPanel />);
    await waitFor(() => expect(screen.getByTestId('law-checklists-note').textContent).toBe(
      'What to gather could not be read (Failed (HTTP 503): the register of sources could not be read).'));
    expect(screen.queryByTestId('law-checklists-none')).toBeNull();
    expect(screen.queryAllByTestId('checklist')).toHaveLength(0);
  });

  it('a list of no subject is said as none, not as a failure', async () => {
    serve({ status: 200, body: { checklists: [], basis: captured.checklists.basis } });
    render(<ChecklistsPanel />);
    await waitFor(() => expect(screen.getByTestId('law-checklists-none').textContent).toBe('The server lists no subject.'));
    expect(screen.queryByTestId('law-checklists-note')).toBeNull();
  });
});
