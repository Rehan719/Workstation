// W1074 (FU-399 part 87) — the children's approval pack, rendered against its routes' own answers.
//
// The pack shows, as one thing a scholar decides as a whole, the rules every children's tool keeps, each tool as a
// child would meet it, and the learner-facing text awaiting a decision; one decision covers the pack and is bound to
// the fingerprint the scholar read. This mounts the real pack against what each route answered on a fresh store
// (ChildrenApprovalPack.fixture.json, captured by w1074_capture.py). THE PACK'S OWN WORDS ARE NOT IN THE FIXTURE:
// every rule, tool name, who runs a tool, what a child sees, step, wording, question and answer was replaced by
// made-up words when it was captured; the structure, the counts, the fingerprint, the state and the platform's own
// sentences about the state are as the route answered them. The only decision in it is a return with made-up notes
// by a made-up reviewer: nothing is approved. Rendering found a pack that could not be read again left on the page
// under "could not be read", and a decision refused because the pack had changed said over the old pack with nothing
// that read it again. Fixed here.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ChildrenApprovalPack.fixture.json';
import { ChildrenApprovalPack } from './ChildrenApprovalPack';

type Answer = { status: number; body: unknown };
const PACK = '/api/v1/scholar-review/pack';
const DECIDE = '/api/v1/scholar-review/pack/decide';
const SCHOLAR = captured.scholar_ask;
const ROSTER: [string, { name: string }][] = [[SCHOLAR.scholar_id, { name: SCHOLAR.name }]];
const P = captured.pack.body;

//  each route as it answered; each read of the pack takes the next answer in `packs` (the last one stays), each
//  decision the next in `decisions`
function serve(plan: { packs?: Answer[]; decisions?: Answer[] } = {}) {
  const packs = [...(plan.packs ?? [captured.pack, captured.pack_after])];
  const decisions = [...(plan.decisions ?? [captured.returned])];
  const next = (list: Answer[]) => (list.length > 1 ? list.shift()! : list[0]);
  const sent: { url: string; method: string; body?: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    sent.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    let a: Answer;
    if (method === 'GET' && url === PACK) a = next(packs);
    else if (method === 'POST' && url === DECIDE) a = next(decisions);
    else a = { status: 404, body: { detail: `not served here: ${method} ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return sent;
}

const state = () => screen.getByTestId('pack-state').textContent;
const reads = (sent: { url: string; method: string }[]) => sent.filter(s => s.method === 'GET' && s.url === PACK).length;

describe('ChildrenApprovalPack, rendered against its routes\' own answers (made-up words for the pack\'s own)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows the pack as one: its rules, its tools as a child would meet them, and its state', async () => {
    serve();
    render(<ChildrenApprovalPack roster={ROSTER} chosen="" />);
    await waitFor(() => expect(state()).toBe(`State: ${P.state.replace(/_/g, ' ')} — ${P.basis}. ${P.whole}.`));
    for (const r of P.sections.rules) expect(screen.getByText(r.rule)).toBeTruthy();
    expect(screen.getAllByTestId('pack-tool').length).toBe(P.sections.tools.length);
    expect(screen.getByText(P.sections.tools[0].what_a_child_sees)).toBeTruthy();
    expect(screen.getByTestId('pack-gate').textContent).toBe(`Children's tools: ${P.children_tools.basis}`);
    expect(screen.getByText('Choose the scholar the decision is entered for, below.')).toBeTruthy();
  });

  it('says a roster not yet read apart from a roster with nobody on it', async () => {
    serve();
    const view = render(<ChildrenApprovalPack roster={null} chosen="" />);
    await waitFor(() => expect(screen.getByTestId('pack-roster-unread')).toBeTruthy());
    expect(screen.queryByTestId('pack-no-scholar')).toBeNull();
    view.rerender(<ChildrenApprovalPack roster={[]} chosen="" />);
    expect(screen.getByTestId('pack-no-scholar')).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Return with notes' })).toBeNull();
  });

  it('returns the pack with notes for the chosen scholar, bound to the fingerprint read, and reads it again', async () => {
    const sent = serve();
    render(<ChildrenApprovalPack roster={ROSTER} chosen={SCHOLAR.scholar_id} />);
    await waitFor(() => expect(state()).toMatch(/^State: awaiting review/));
    fireEvent.change(screen.getByLabelText('Notes on the pack'), { target: { value: captured.return_ask.notes } });
    fireEvent.click(screen.getByRole('button', { name: 'Return with notes' }));
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe('The pack is recorded as returned, with your notes.'));
    expect(sent.find(s => s.url === DECIDE)!.body).toEqual({ ...captured.return_ask, decision: 'return' });
    await waitFor(() => expect(state()).toBe(
      `State: returned — ${captured.pack_after.body.basis}. ${captured.pack_after.body.whole}.`));
  });

  it('reads the pack again when a decision is refused because the pack changed', async () => {
    const sent = serve({ packs: [captured.pack, captured.pack_after], decisions: [captured.stale_decide] });
    render(<ChildrenApprovalPack roster={ROSTER} chosen={SCHOLAR.scholar_id} />);
    await waitFor(() => expect(state()).toMatch(/^State: awaiting review/));
    fireEvent.click(screen.getByRole('button', { name: 'Return with notes' }));
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe(
      `Not recorded. Failed (HTTP 409): ${captured.stale_decide.body.detail}`));
    await waitFor(() => expect(reads(sent)).toBe(2));
    await waitFor(() => expect(state()).toMatch(/^State: returned/));
  });

  it('takes a pack it could not read again off the page', async () => {
    serve({ packs: [captured.pack, captured.pack_failed] });
    render(<ChildrenApprovalPack roster={ROSTER} chosen={SCHOLAR.scholar_id} />);
    await waitFor(() => expect(state()).toMatch(/^State: awaiting review/));
    fireEvent.click(screen.getByRole('button', { name: 'Return with notes' }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe(
      `The approval pack could not be read. Failed (HTTP 500): ${captured.pack_failed.body.detail}`));
    expect(screen.queryByTestId('pack-state')).toBeNull();
    expect(screen.queryByText(P.sections.rules[0].rule)).toBeNull();
  });

  it('says a pack it could not read on opening by its reason', async () => {
    serve({ packs: [captured.pack_failed] });
    render(<ChildrenApprovalPack roster={ROSTER} chosen="" />);
    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe(
      `The approval pack could not be read. Failed (HTTP 500): ${captured.pack_failed.body.detail}`));
    expect(screen.queryByTestId('pack-state')).toBeNull();
  });
});
