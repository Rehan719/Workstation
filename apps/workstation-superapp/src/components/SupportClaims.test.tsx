// W942 (P5.3 part 2) — claims that an output is wrong, on the support page, rendered against the claim routes' own
// answers (SupportClaims.fixture.json, captured by w942_capture.py on a fresh store): before any claim, a claim OPEN,
// the same claim ANSWERED by a person with its decision in the ledger, and the routes' refusals.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './SupportClaims.fixture.json';
import { SupportClaims } from './SupportClaims';

type Reply = { status: number; body: unknown };
type Claimed = { claim_id: string; state: string; state_basis: string; what_is_wrong: string;
  answer_logged_basis?: string; artefact: { title: string; version: number } };
const ok = (body: unknown): Reply => ({ status: 200, body });
const claims = (a: { claims: unknown }) => a.claims as Claimed[];

//  the claims and the deliverables each answer in turn (the last one repeats); writes answer in turn
function serve(cl: Reply[], dl: Reply[], writes: Reply[] = []) {
  const sent: { url: string; body: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const post = init?.method === 'POST';
    if (post) sent.push({ url, body: JSON.parse(String(init?.body ?? 'null')) });
    const take = (q: Reply[]) => (q.length > 1 ? q.shift()! : q[0]);
    const r = post ? (writes.shift() ?? ok({})) : url === '/api/v1/support/claims' ? take(cl) : take(dl);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
  return sent;
}

const text = (id: string) => screen.getByTestId(id).textContent;

describe("SupportClaims, rendered against the claim routes' own answers", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('with no claim raised, it says so, with the rule in the server\'s words', async () => {
    serve([ok(captured.empty)], [ok(captured.deliverables)]);
    render(<SupportClaims />);
    await waitFor(() => expect(screen.getByTestId('claims-basis').textContent).toBe(captured.empty.basis));
    expect(text('claims-open')).toBe('0 open of 0');
    expect(screen.getByTestId('claims-none')).toBeTruthy();
  });

  it('a claim is sent as what it is about and what is wrong, read again, and shown OPEN in the server\'s words', async () => {
    const sent = serve([ok(captured.empty), ok(captured.after_raise)], [ok(captured.deliverables)], [ok(captured.raised)]);
    render(<SupportClaims />);
    await screen.findByTestId('claims-basis');
    const q = captured.raise_request;
    fireEvent.change(screen.getByLabelText('Deliverable the claim is about'), { target: { value: q.artefact_id } });
    fireEvent.change(screen.getByLabelText('What is wrong'), { target: { value: q.what_is_wrong } });
    fireEvent.click(screen.getByText('Raise a claim'));
    const [c] = claims(captured.after_raise);
    const row = await screen.findByTestId(`claim-${c.claim_id}`);
    expect(row.textContent).toContain(`OPEN — ${c.artefact.title} (version ${c.artefact.version})`);
    expect(row.textContent).toContain(`${c.state_basis}.`);
    expect(screen.queryByTestId(`claim-logged-${c.claim_id}`)).toBeNull();
    expect(sent).toEqual([{ url: '/api/v1/support/claims', body: captured.raise_request }]);
    expect(text('claims-done')).toBe(`Raised: ${captured.raised.claim_id} — ${captured.raised.state}.`);
    expect(text('claims-open')).toBe('1 open of 1');
  });

  it('a claim a person answered says so, with whether the decision reached the ledger', async () => {
    serve([ok(captured.after_answer)], [ok(captured.deliverables)]);
    render(<SupportClaims />);
    const [c] = claims(captured.after_answer);
    await waitFor(() => expect(screen.getByTestId(`claim-${c.claim_id}`).textContent).toContain(`ANSWERED — ${c.artefact.title}`));
    expect(text(`claim-logged-${c.claim_id}`)).toBe(`${c.answer_logged_basis}.`);
    expect(text('claims-open')).toBe('0 open of 1');
  });

  //  W964 (FU-1190): a claim against an answer that was never saved names its tool, what served it and its
  //  fingerprint, with the server's sentence on what the claim holds
  it('a claim against an answer names its tool, what served it and its fingerprint, in the server\'s words', async () => {
    serve([ok(captured.answer_claims)], [ok(captured.deliverables)]);
    render(<SupportClaims />);
    const [c] = captured.answer_claims.claims;
    const row = await screen.findByTestId(`claim-${c.claim_id}`);
    expect(row.textContent).toContain(
      `OPEN — an answer from ${c.artefact.tool}, served by ${c.artefact.served_by_as_reported} (sha256 ${c.artefact_id.slice(0, 12)})`);
    expect(text(`claim-answer-${c.claim_id}`)).toBe(c.artefact.basis);
    expect(row.textContent).not.toContain('version');
    expect(text('claims-open')).toBe('1 open of 1');
  });

  it("a claim the server refuses is shown in its own words", async () => {
    serve([ok(captured.empty)], [ok(captured.deliverables)], [{ status: 422, body: { detail: captured.refused_blank } }]);
    render(<SupportClaims />);
    await screen.findByTestId('claims-basis');
    fireEvent.change(screen.getByLabelText('Deliverable the claim is about'), { target: { value: captured.raise_request.artefact_id } });
    fireEvent.click(screen.getByText('Raise a claim'));
    await waitFor(() => expect(screen.getByTestId('claims-refused').textContent).toBe(`Failed (HTTP 422): ${captured.refused_blank}`));
    expect(screen.queryByTestId('claims-done')).toBeNull();
  });

  it('with no deliverable to name, nothing can be raised', async () => {
    serve([ok(captured.empty)], [ok(captured.deliverables_empty)]);
    render(<SupportClaims />);
    expect(await screen.findByTestId('claims-no-deliverable')).toBeTruthy();
    expect(screen.queryByText('Raise a claim')).toBeNull();
  });

  it('a refused read is said, and never drawn as no claims', async () => {
    serve([{ status: 503, body: { detail: captured.unreadable } }], [ok(captured.deliverables)]);
    render(<SupportClaims />);
    await waitFor(() => expect(screen.getByTestId('claims-unread').textContent).toBe(
      `Could not read the claims — Failed (HTTP 503): ${captured.unreadable}`));
    expect(screen.queryByTestId('claims-none')).toBeNull();
    expect(screen.queryByTestId('claims-open')).toBeNull();
  });
});
