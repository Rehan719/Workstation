// W1061 (FU-399 part 76) — the Resource Fabric's instrument cell, rendered against its routes' own answers.
//
// The cell shows which resources the fabric can run, proposes the smallest available set for an objective, keeps a
// proposal as a specification and lists the kept ones. This mounts the real panel against what each route answered on
// a fresh store with no model installed (InstrumentCellPanel.fixture.json, captured by w1061_capture.py: every read on
// opening, a proposal for a made-up objective with no capability stated and then with its first suggestion stated,
// that proposal kept, the list read again, a second proposal kept beside it, and the availability route's own 500).
// Rendering found the panel saying a
// list before it was read as empty ("No specification has been kept." while the list was still being read), a failed
// availability read taken away by the next proposal asked, a proposal that was not made said away from its button
// with the one before it still drawn as its answer, and a list that was not read after a keep said as a bare failure
// under "Kept as". Fixed in this round.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './InstrumentCellPanel.fixture.json';
import { InstrumentCellPanel } from './InstrumentCellPanel';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const AVAIL = '/api/v1/resources/cell/availability';
const RUNS = '/api/v1/resources/compositions/runs?limit=10';
const SPECS = '/api/v1/resources/specifications';
const PROPOSE = '/api/v1/resources/cell/propose';
const OBJECTIVE = captured.objective;
const STATED = String(captured.first_suggestion);
const SECOND = String(captured.second_suggestion);
const KEPT = captured.kept.body;
const UNLISTED = 'The kept specifications were not listed: Failed — backend unreachable.';
const NONE_KEPT = 'No specification has been kept.';
const NO_RUN = 'No recorded run is listed, so there is nothing to check yet.';

//  each route as it answered; a case replaces one answer, or holds it back until the test lets it go. Each read of
//  the specifications takes the next answer in `specs` (the last one stays), each proposal asked the next in
//  `propose`, and by default a proposal is the route's own for what was asked
function serve(plan: { avail?: Reply; runs?: Reply; specs?: Reply[]; propose?: Reply[]; keep?: Reply } = {}) {
  const calls: { method: string; url: string; body?: unknown }[] = [];
  const specs = [...(plan.specs ?? [captured.specifications, captured.specifications_after])];
  const proposals = [...(plan.propose ?? [])];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    const body = init?.body ? JSON.parse(String(init.body)) : undefined;
    calls.push({ method, url, body });
    let r: Reply;
    if (method === 'GET' && url === AVAIL) r = plan.avail ?? captured.availability;
    else if (method === 'GET' && url === RUNS) r = plan.runs ?? captured.runs;
    else if (method === 'GET' && url === SPECS) r = specs.length > 1 ? specs.shift()! : specs[0];
    else if (method === 'POST' && url === PROPOSE) {
      r = proposals.shift() ?? ((body?.required_capabilities ?? []).length ? captured.proposed_stated : captured.proposed_open);
    } else if (method === 'POST' && url === SPECS) r = plan.keep ?? captured.kept;
    else r = { status: 404, body: { detail: `not served here: ${method} ${url}` } };
    const a = await r;
    if (a === 'unreachable') throw new TypeError('Failed to fetch');
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return calls;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const mount = () => render(<InstrumentCellPanel />);
const type = (label: string, value: string) => fireEvent.change(screen.getByLabelText(label), { target: { value } });
const press = (name: string) => fireEvent.click(screen.getByRole('button', { name }));
//  a proposal for a stated capability, drawn with its keep section
async function proposeStated(caps = STATED) {
  type('Objective', OBJECTIVE);
  type('Required capabilities', caps);
  press('Propose a set');
  await waitFor(() => expect(screen.getByTestId('cell-keep')).toBeTruthy());
}
const keptSaid = (k: { id: string; version: number; digest: string }) =>
  `Kept as ${k.id}, version ${k.version}, digest ${k.digest.slice(0, 12)}. Nothing was run.`;

describe('InstrumentCellPanel, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('says on opening what each read answered: what the fabric can run, what it cannot and why, and that nothing is kept or run', async () => {
    serve();
    mount();
    const a = captured.availability.body;
    await waitFor(() => expect(screen.getByTestId('cell-availability').textContent).toContain(
      `${a.counts.available} fabric can run it · ${a.counts.prompt_stage_only} prompt stage only — engine not run — of ${a.total} registered.`));
    const cannot = a.resources.filter(r => r.state !== 'available');
    expect(cannot.length).toBe(a.counts.prompt_stage_only);
    for (const r of cannot) {
      expect(screen.getByText(r.name).closest('li')!.textContent).toBe(`${r.name} — prompt stage only — engine not run. ${r.reason}`);
    }
    const unmet = a.resources.filter(r => r.needs_state === 'unmet');
    expect(unmet.length).toBe(a.needs_counts.unmet);
    expect(screen.getByTestId('cell-needs-unmet').textContent).toBe(unmet.map(r => `${r.name} — unavailable. ${r.needs_basis}`).join(''));
    expect(screen.getByTestId('cell-available-without-engine').textContent).toBe(
      `${a.available_without_engine.length} of the available run no engine when composed: ${a.available_without_engine.join(', ')}.`);
    await waitFor(() => expect(screen.getByText(NONE_KEPT)).toBeTruthy());
    expect(screen.getByText(NO_RUN)).toBeTruthy();
  });

  it('says no list is empty before it has been read', async () => {
    const specs = held(captured.specifications);
    const runs = held(captured.runs);
    serve({ specs: [specs.reply], runs: runs.reply });
    mount();
    await waitFor(() => expect(screen.getByTestId('cell-availability')).toBeTruthy());
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
    expect(screen.queryByText(NO_RUN)).toBeNull();
    await act(async () => { specs.letGo(); runs.letGo(); });
    await waitFor(() => expect(screen.getByText(NONE_KEPT)).toBeTruthy());
    expect(screen.getByText(NO_RUN)).toBeTruthy();
  });

  it('says a failed availability read in its place, with what was not read, and a proposal asked after it does not take it away', async () => {
    serve({ avail: captured.availability_failed });
    mount();
    const said = `Which resources the fabric can run was not read: Failed (HTTP 500): ${captured.availability_failed.body.detail.replace(/\.$/, '')}.`;
    await waitFor(() => expect(screen.getByTestId('cell-availability-error').textContent).toBe(said));
    expect(screen.queryByTestId('cell-availability')).toBeNull();
    type('Objective', OBJECTIVE);
    press('Suggest requirements');
    await waitFor(() => expect(screen.getByTestId('cell-proposal').textContent).toContain(captured.proposed_open.body.what_this_is));
    expect(screen.getByTestId('cell-availability-error').textContent).toBe(said);
  });

  it('draws a proposal as the route answered it, the suggestions and then the set for what was stated, and sends what was asked', async () => {
    const calls = serve();
    mount();
    await waitFor(() => expect(screen.getByTestId('cell-availability')).toBeTruthy());
    type('Objective', OBJECTIVE);
    press('Suggest requirements');
    const open = captured.proposed_open.body;
    await waitFor(() => expect(screen.getByTestId('cell-proposal').textContent).toContain(open.suggestion_basis));
    for (const s of open.suggested_requirements) expect(screen.getByRole('button', { name: `+ ${s.capability}` })).toBeTruthy();
    press(`+ ${STATED}`);
    expect((screen.getByLabelText('Required capabilities') as HTMLInputElement).value).toBe(STATED);
    press('Propose a set');
    await waitFor(() => expect(screen.getByTestId('cell-keep')).toBeTruthy());
    const sel = captured.proposed_stated.body.selection;
    for (const s of sel.selected) {
      expect(screen.getByText(s.name).closest('li')!.textContent).toContain(
        `${s.name} — covers ${s.covers.join(', ')}. ${s.contract.when_run}.What it persists: ${s.contract.persists_basis}`);
    }
    expect(calls.filter(c => c.url === PROPOSE).map(c => c.body)).toEqual([captured.ask_open, captured.ask_stated]);
  });

  it('says a proposal that was not made beside its button, and the one before it is no longer drawn as its answer', async () => {
    serve({ propose: [captured.proposed_stated, 'unreachable'] });
    mount();
    await proposeStated();
    type('Required capabilities', `${STATED}, risk`);
    press('Propose a set');
    await waitFor(() => expect(screen.getByTestId('cell-propose-error').textContent).toBe(
      'No proposal was made: Failed — backend unreachable.'));
    expect(screen.queryByTestId('cell-proposal')).toBeNull();
    expect(screen.queryByTestId('cell-keep')).toBeNull();
  });

  it('keeps the proposal on screen as the route kept it, says so, and lists it', async () => {
    const calls = serve();
    mount();
    await waitFor(() => expect(screen.getByText(NONE_KEPT)).toBeTruthy());
    await proposeStated();
    press('Keep as a new specification');
    await waitFor(() => expect(screen.getByTestId('cell-spec-message').textContent).toBe(keptSaid(KEPT)));
    await waitFor(() => expect(screen.getByRole('button', { name: KEPT.id })).toBeTruthy());
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
    expect(calls.find(c => c.method === 'POST' && c.url === SPECS)!.body).toEqual(captured.keep_ask);
  });

  it('says a list that was not read, never as none, and keeps saying it until a read of it answers', async () => {
    const keep = held(captured.kept);
    serve({ specs: ['unreachable', captured.specifications_after], keep: keep.reply });
    mount();
    await waitFor(() => expect(screen.getByTestId('cell-specs-unlisted').textContent).toBe(UNLISTED));
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
    await proposeStated();
    press('Keep as a new specification');
    //  a keep asked is not a read of the list: what was not read is still said while it is asked
    expect(screen.getByTestId('cell-specs-unlisted').textContent).toBe(UNLISTED);
    await act(async () => { keep.letGo(); });
    await waitFor(() => expect(screen.getByRole('button', { name: KEPT.id })).toBeTruthy());
    expect(screen.queryByTestId('cell-specs-unlisted')).toBeNull();
  });

  //  W1062 - the store's own refusal of the list is longer than the 300 characters the shared helper kept
  it('says the store\'s own refusal of the list whole', async () => {
    const why = captured.specifications_failed.body.detail;
    expect(why.length).toBeGreaterThan(300);
    serve({ specs: [captured.specifications_failed] });
    mount();
    await waitFor(() => expect(screen.getByTestId('cell-specs-unlisted').textContent).toBe(
      `The kept specifications were not listed: Failed (HTTP 503): ${why.replace(/\.$/, '')}.`));
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
  });

  it('says a keep that was made, and that the list read after it was not, apart, and draws no list it did not read', async () => {
    serve({ specs: [captured.specifications_after, 'unreachable'], propose: [captured.proposed_second], keep: captured.kept_second });
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: KEPT.id })).toBeTruthy());
    await proposeStated(SECOND);
    press('Keep as a new specification');
    await waitFor(() => expect(screen.getByTestId('cell-spec-message').textContent).toBe(keptSaid(captured.kept_second.body)));
    await waitFor(() => expect(screen.getByTestId('cell-specs-unlisted').textContent).toBe(UNLISTED));
    expect(screen.queryByTestId('cell-spec-error')).toBeNull();
    //  what the read before it listed is not the list now
    expect(screen.queryByRole('button', { name: KEPT.id })).toBeNull();
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
  });

  it('never lets a read of the list that answers late replace the one read after a keep', async () => {
    const first = held(captured.specifications);
    serve({ specs: [first.reply, captured.specifications_after] });
    mount();
    await waitFor(() => expect(screen.getByTestId('cell-availability')).toBeTruthy());
    await proposeStated();
    press('Keep as a new specification');
    await waitFor(() => expect(screen.getByRole('button', { name: KEPT.id })).toBeTruthy());
    await act(async () => { first.letGo(); });
    await act(async () => { await Promise.resolve(); });
    expect(screen.getByRole('button', { name: KEPT.id })).toBeTruthy();
    expect(screen.queryByText(NONE_KEPT)).toBeNull();
  });

  // W1116 (FU-399 part 105) - what the cell draws and no test read: what it is, what each need was checked against,
  // the kept specifications' and the run check's sections, and each proposed resource's need narrowed here
  it('says what each need was checked against, and what each proposed resource cannot do here, in the routes\' own words', async () => {
    serve();
    mount();
    const a = captured.availability.body;
    const word: Record<string, string> = { available: 'available', unavailable: 'unavailable', not_checked: 'not checked' };
    await waitFor(() => expect(screen.getByTestId('cell-checked').textContent).toBe(
      `Checked against what each declares it needs: ${Object.entries(a.checked_counts).map(([k, v]) => `${v} ${word[k] ?? k}`).join(' · ')}.`
      + a.needs_basis));
    expect(screen.getByTestId('instrument-cell').querySelector('h2')?.textContent).toBe('Instrument Cell');
    expect(screen.getByTestId('cell-specifications').querySelector('p')?.textContent).toBe('Kept specifications');
    const verify = screen.getByTestId('cell-verify').querySelectorAll('p');
    expect([verify[0].textContent, verify[1].textContent]).toEqual([
      'Check a recorded run against stated criteria',
      'This reads a run that already happened; it runs nothing. A criterion nothing here can read ends as not assessed,'
      + ' and not assessed never counts as met.']);
    //  a set proposed as the capture asked: each selected resource's need narrowed here, in the route's words
    type('Objective', OBJECTIVE);
    press('Suggest requirements');
    await waitFor(() => expect(screen.getByTestId('cell-proposal').textContent).toContain(captured.proposed_open.body.suggestion_basis));
    press(`+ ${STATED}`);
    press('Propose a set');
    await waitFor(() => expect(screen.getByTestId('cell-keep')).toBeTruthy());
    type Narrowed = { availability: { needs_narrowed?: { needs: string; why: string }[] } };
    const narrowed = (captured.proposed_stated.body.selection.selected as Narrowed[])
      .flatMap(s => (s.availability.needs_narrowed ?? []).map(n => `Here, without ${n.needs}: ${n.why}`));
    expect(narrowed.length).toBeGreaterThan(0);
    expect(screen.getAllByTestId('cell-needs-narrowed').map(e => e.textContent)).toEqual(narrowed);
  });
});
