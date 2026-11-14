// W978 (FU-399 part 11) — the Horizon Companion page, rendered against the horizon routes' own answers.
//
// What a person reads here is each request as it was recorded: what was asked, what the platform understood, what it
// did not evaluate, what the run consumed, and what the owned knowledge index holds. Every field is three-state, and
// the middle state is the one that matters. Three guards read the page's source. This mounts the real page against the
// answers the three routes gave on a fresh store (HorizonCompanion.fixture.json, captured by w978_capture.py from one
// made-up request and three planted inbox files), reads each claim in the DOM, and has the server refuse each read.
import { render, screen, within, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './HorizonCompanion.fixture.json';
import { HorizonCompanion } from './HorizonCompanion';

type Reply = { status: number; data: unknown };
const ok = (data: unknown): Reply => ({ status: 200, data });
const refused = (detail: string): Reply => ({ status: 503, data: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: { records?: Reply; consumption?: Reply; archive?: Reply } = {}) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/horizon/records?limit=25') return (a.records ?? ok(captured.records)) as never;
    if (url === '/api/v1/horizon/consumption?limit=100') return (a.consumption ?? ok(captured.consumption)) as never;
    if (url === '/api/v1/horizon/archive') return (a.archive ?? ok(captured.archive_scanned)) as never;
    return { status: 404, data: { detail: `not served in this test: ${url}` } } as never;
  });
}

const records = captured.records.records;
const joined = new Set(captured.consumption.records.map(c => c.intent_id));

describe('HorizonCompanion, rendered against the horizon routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('no request recorded is said as recorded, not as none made', async () => {
    serve({ records: ok(captured.records_empty) });
    render(<HorizonCompanion />);
    expect(await screen.findByText('No request has been recorded yet. That is not the same as none having been made.')).toBeTruthy();
    expect(screen.queryAllByTestId('companion-record')).toHaveLength(0);
    expect(screen.getByText(captured.records_empty.basis)).toBeTruthy();
  });

  it('each record says what was asked, that nothing compressed it, and what was not evaluated', async () => {
    serve();
    render(<HorizonCompanion />);
    const cards = await screen.findAllByTestId('companion-record');
    expect(cards).toHaveLength(records.length);
    cards.forEach((card, i) => {
      const r = records[i];
      expect(card.textContent).toContain(String(r.asked));
      expect(within(card).getByText('Not compressed')).toBeTruthy();
      expect(within(card).getByText(r.compression_basis)).toBeTruthy();
      expect(within(card).getByTestId(`field-domain`).textContent).toContain('Not evaluated — no compression produced this field');
      expect(within(card).getByTestId(`field-escalations`).textContent).toContain(
        'Not evaluated — nothing compressed this request, so no list exists. Its absence is not an absence of escalations.');
      expect(within(card).getByText(String(r.decision))).toBeTruthy();
      const terms = within(card).getAllByTestId('decision-term');
      expect(terms).toHaveLength((r.decision_terms ?? []).length);
      (r.decision_terms ?? []).forEach((t, j) => {
        expect(terms[j].textContent).toContain(t.fired === true ? 'FIRED' : t.fired === false ? 'did not fire' : 'Not evaluated');
        expect(terms[j].textContent).toContain(t.basis);
      });
      if (r.gated === false) expect(within(card).getByText(r.gating_basis)).toBeTruthy();
      expect(within(card).getByText('No station assigned')).toBeTruthy();
    });
  });

  it('a compressed record\'s lists are said as answered: none raised, or what was raised', async () => {
    const d = clone(captured.records);
    Object.assign(d.records[0], { compression: 'COMPRESSED', served_by: 'w978-model', escalations: [], missing: ['the patient\'s age'] });
    serve({ records: ok(d) });
    render(<HorizonCompanion />);
    const card = (await screen.findAllByTestId('companion-record'))[0];
    expect(within(card).getByText('Compressed by w978-model')).toBeTruthy();
    expect(within(card).getByTestId(`field-escalations`).textContent).toContain('None raised — the compression answered');
    expect(within(card).getByTestId(`field-missing-inputs`).textContent).toContain('the patient\'s age');
  });

  it('what a run consumed: measured figures, unmeasured ones never a zero, the owner\'s fields unfilled', async () => {
    serve();
    render(<HorizonCompanion />);
    const cards = await screen.findAllByTestId('companion-record');
    cards.forEach((card, i) => {
      const box = within(card).getByTestId('companion-consumption');
      const c = captured.consumption.records.find(x => x.intent_id === records[i].intent_id);
      if (!c) {
        expect(box.textContent).toContain('Not recorded');
        return;
      }
      const fields = within(box).getAllByTestId('consumption-field');
      expect(fields).toHaveLength(c.computed_fields.length);
      c.computed_fields.forEach((f, j) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const m = (c as any)[f];
        expect(fields[j].textContent).toContain(m.measured ? JSON.stringify(m.value) : 'Not measured');
        expect(fields[j].textContent).toContain(m.basis);
      });
      const owner = within(box).getAllByTestId('consumption-owner-field');
      expect(owner).toHaveLength(c.owner_fields.length);
      owner.forEach(o => expect(o.textContent).toContain('Not filled'));
    });
    expect(cards.some((_, i) => joined.has(records[i].intent_id))).toBe(true);
  });

  it('a failed read of what runs consumed is said on each card, never as a run nothing recorded', async () => {
    serve({ consumption: refused('the consumption store could not be read') });
    render(<HorizonCompanion />);
    const cards = await screen.findAllByTestId('companion-record');
    for (const card of cards) {
      const said = within(card).getByTestId('consumption-unread');
      expect(said.textContent).toContain(
        'What each run consumed could not be read (HTTP 503: the consumption store could not be read).');
      expect(within(card).getByTestId('companion-consumption').textContent).not.toContain('Not recorded');
    }
  });

  it('a refused read of the records is said with the server\'s reason, and shows no record', async () => {
    serve({ records: refused('the record store could not be read') });
    render(<HorizonCompanion />);
    const said = await screen.findByText(/The records are not reporting/);
    expect(said.textContent).toBe('The records are not reporting (HTTP 503: the record store could not be read). Nothing is ' +
      'shown, because nothing was received — not that nothing was recorded.');
    expect(screen.queryAllByTestId('companion-record')).toHaveLength(0);
  });

  it('a scanned index shows its counts, its recount, that no embedding is installed, its caps and what it did not read', async () => {
    serve();
    render(<HorizonCompanion />);
    const m = captured.archive_scanned.manifest;
    const panel = await screen.findByTestId('horizon-archive-index');
    expect((await within(panel).findByTestId('horizon-archive-counts')).textContent).toBe(
      `${m.counts.INDEXED} file(s) indexed · ${m.counts.NOT_READ} not read · ${m.counts.EXCLUDED} excluded by a secret rule.`);
    expect(within(panel).getByTestId('horizon-archive-recount').textContent).toBe(captured.archive_scanned.recount.basis);
    expect(within(panel).getByTestId('horizon-archive-embeddings').textContent).toBe('embeddings: none installed');
    expect(within(panel).getByTestId('horizon-archive-embeddings-basis').textContent).toBe(m.search_basis);
    expect(within(panel).getByTestId('horizon-archive-bounds').textContent).toContain(
      `Bounds: at most ${m.bounds.max_files} file(s), ${m.bounds.max_bytes} byte(s) per file, ` +
      `${m.bounds.max_passages_per_file} located passage(s) per document.`);
    const notRead = within(panel).getByTestId('horizon-archive-not-read').textContent ?? '';
    for (const f of m.files.filter(x => x.state !== 'INDEXED')) expect(notRead).toContain(`${f.path} (${f.state})`);
    expect(notRead).not.toContain('w978-notes.md');
  });

  it('an index never scanned says so, and prints no count nobody computed', async () => {
    serve({ archive: ok(captured.archive_unscanned) });
    render(<HorizonCompanion />);
    const said = await screen.findByTestId('horizon-archive-not-scanned');
    expect(said.textContent).toContain('No scan of the inbox is recorded, so nothing is indexed and no count is shown.');
    expect(said.textContent).toContain(captured.archive_unscanned.recount.basis);
    expect(screen.queryByTestId('horizon-archive-counts')).toBeNull();
    expect(screen.queryByText(/file\(s\) indexed/)).toBeNull();
  });

  it('an index that cannot be read is said to be unreachable, not empty', async () => {
    serve({ archive: refused('the index could not be read') });
    render(<HorizonCompanion />);
    await waitFor(() => expect(screen.getByTestId('horizon-archive-unavailable').textContent).toContain(
      'nothing here should be read as "the archive is empty"'));
    expect(screen.queryByTestId('horizon-archive-counts')).toBeNull();
  });
});
