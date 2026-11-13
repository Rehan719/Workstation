// W935 (P5.15 clauses 5 and 6; row FU-1178, its last part) — the review an entity's work has reached, rendered
// against the signature routes' own answers.
//
// What a founder reads here are claims about their entity's work: whether a qualified person has signed the current
// text of each deliverable, whose signature that is and on what credential as stated, and why a signature no longer
// counts. This mounts the real component against the answers GET/POST /api/v1/entity-specialists/{id}/signatures and
// .../sign gave on a fresh store (EntityWorkReview.fixture.json, captured by w935_capture.py): before a signature,
// after one, after the deliverable was run again, an entity with no specialist, and the routes' refusals.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './EntityWorkReview.fixture.json';
import { EntityWorkReview } from './EntityWorkReview';

type Reply = { status: number; body: unknown };
type Review = { label: string; basis: string; title: string; version: number };
type Signed = { signature_id: string; name: string; deliverable_title: string; version: number; reviewed: string;
  date: string; lapses_on: string; counts: boolean; why_not: string | null };
const ok = (body: unknown): Reply => ({ status: 200, body });
const did = captured.deliverable_id;
const review = (a: { deliverables: unknown }) => (a.deliverables as Record<string, Review>)[did];
const signatures = (a: { signatures: unknown }) => a.signatures as Signed[];

//  the signatures and the roster each answer in turn (the last one repeats); writes answer in turn
function serve(sigs: Reply[], roster: Reply[], writes: Reply[] = []) {
  const sent: { url: string; body: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const post = init?.method === 'POST';
    if (post) sent.push({ url, body: JSON.parse(String(init?.body ?? 'null')) });
    const take = (q: Reply[]) => (q.length > 1 ? q.shift()! : q[0]);
    const r = post ? (writes.shift() ?? ok({})) : url.endsWith('/signatures') ? take(sigs) : take(roster);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
  return sent;
}

const text = (id: string) => screen.getByTestId(id).textContent;

function fill() {
  const q = captured.sign_request;
  const [held] = captured.roster.active;
  fireEvent.change(screen.getByLabelText('Specialist who signs'), { target: { value: held.specialist_id } });
  fireEvent.change(screen.getByLabelText('Deliverable signed'), { target: { value: q.deliverable_id } });
  fireEvent.change(screen.getByLabelText('What in it they reviewed'), { target: { value: q.reviewed } });
  fireEvent.change(screen.getByLabelText('Date reviewed'), { target: { value: q.date } });
  fireEvent.change(screen.getByLabelText('Signature lapses on'), { target: { value: q.lapses_on } });
}

describe("EntityWorkReview, rendered against the signature routes' own answers", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("a deliverable nobody has signed shows the review it has reached in the server's words", async () => {
    serve([ok(captured.before)], [ok(captured.roster)]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    const r = review(captured.before);
    const row = await screen.findByTestId(`work-review-${did}`);
    expect(row.textContent).toContain(`${r.title} — version ${r.version}`);
    expect(row.textContent).toContain(`Review reached: ${r.label} — ${r.basis}.`);
    expect(text('work-review-basis')).toBe(captured.before.basis);
    expect(text('work-review-credential')).toBe(`Credentials: ${captured.before.credential_basis}.`);
    expect(screen.queryByTestId('work-review-no-specialist')).toBeNull();
  });

  it("a signature is sent as the person's record and nothing else, and the review is read again", async () => {
    const sent = serve([ok(captured.before), ok(captured.after)], [ok(captured.roster)], [ok(captured.signed)]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    await screen.findByTestId(`work-review-${did}`);
    fill();
    fireEvent.click(screen.getByText('Record the signature'));
    const [s] = signatures(captured.after);
    expect((await screen.findByTestId(`signature-${s.signature_id}`)).textContent).toBe(
      `${s.name} signed ${s.deliverable_title} (version ${s.version}) on ${s.date}, until ${s.lapses_on}: ${s.reviewed}. It counts.`);
    const [held] = captured.roster.active;
    expect(sent).toEqual([{ url: `/api/v1/entity-specialists/${captured.vsb_id}/${held.specialist_id}/sign`,
      body: captured.sign_request }]);
    const r = review(captured.after);
    expect(text(`work-review-${did}`)).toContain(`Review reached: ${r.label} — ${r.basis}.`);
    expect(text('work-review-done')).toBe(`Signed by ${captured.signed.signature.name}, for version ${captured.signed.signature.version}.`);
  });

  it("once the deliverable is run again, the signature is said not to count, with the server's reason", async () => {
    serve([ok(captured.rerun)], [ok(captured.roster)]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    const [s] = signatures(captured.rerun);
    expect((await screen.findByTestId(`signature-${s.signature_id}`)).textContent).toContain(` It does not count: ${s.why_not}.`);
    const r = review(captured.rerun);
    expect(text(`work-review-${did}`)).toContain(`Review reached: ${r.label} — ${r.basis}.`);
  });

  it("a signature the server refuses is shown in its own words, and nothing is drawn as signed", async () => {
    serve([ok(captured.before)], [ok(captured.roster)], [{ status: 422, body: { detail: captured.refused_empty } }]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    await screen.findByTestId(`work-review-${did}`);
    fill();
    fireEvent.click(screen.getByText('Record the signature'));
    expect((await screen.findByTestId('work-review-refused')).textContent).toBe(`Failed (HTTP 422): ${captured.refused_empty}`);
    expect(screen.queryByTestId('work-review-done')).toBeNull();
  });

  it('with no specialist holding a place, nothing can be signed, and an entity with no deliverable says so', async () => {
    serve([ok(captured.bare)], [ok(captured.bare_roster)]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    expect(await screen.findByTestId('work-review-no-specialist')).toBeTruthy();
    expect(screen.getByTestId('work-review-none')).toBeTruthy();
    expect(screen.queryByText('Record the signature')).toBeNull();
  });

  it('a refused read is said, and never drawn as nothing being signed', async () => {
    serve([{ status: 503, body: { detail: captured.unreadable } }], [ok(captured.roster)]);
    render(<EntityWorkReview vsbId={captured.vsb_id} />);
    expect((await screen.findByTestId('work-review-unread')).textContent).toBe(
      `Could not read the review of this entity's work — Failed (HTTP 503): ${captured.unreadable}`);
    expect(screen.queryByTestId('work-review-none')).toBeNull();
    expect(screen.queryByTestId(`work-review-${did}`)).toBeNull();
    expect(screen.queryByTestId('work-review-basis')).toBeNull();
  });
});
