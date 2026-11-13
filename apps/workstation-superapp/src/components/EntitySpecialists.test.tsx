// W933 (P5.15 clause 6 and its RELEASE clause; row FU-1178 part 2) — an entity's own specialists, rendered against
// the roster route's own answers.
//
// What a founder reads here are claims about their entity: whether Workstation recommends a specialist for it and
// what engaging one costs the entity, how many places are free, who holds one and who left and why, and what the
// server refused. This mounts the real component against the answers GET/POST /api/v1/entity-specialists gave on a
// fresh store (EntitySpecialists.fixture.json, captured by w933_capture.py): an entity the Genesis journey generated,
// one whose record names no generating door, a roster with a specialist in each state, and the route's refusals.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './EntitySpecialists.fixture.json';
import { EntitySpecialists } from './EntitySpecialists';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });

//  reads answer in turn (the last one repeats); writes answer in turn
function serve(reads: Reply[], writes: Reply[] = []) {
  const sent: { url: string; body: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const post = init?.method === 'POST';
    if (post) sent.push({ url, body: JSON.parse(String(init?.body ?? 'null')) });
    const r = post ? (writes.shift() ?? ok({})) : (reads.length > 1 ? reads.shift()! : reads[0]);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
  return sent;
}

const text = (id: string) => screen.getByTestId(id).textContent;

function fill(c: typeof captured.attach_request) {
  fireEvent.change(screen.getByLabelText("Specialist's name"), { target: { value: c.name } });
  fireEvent.change(screen.getByLabelText('Discipline'), { target: { value: c.discipline } });
  fireEvent.change(screen.getByLabelText('Credential as stated'), { target: { value: c.credential_as_stated } });
  fireEvent.change(screen.getByLabelText('What they review'), { target: { value: c.reviews } });
  fireEvent.change(screen.getByLabelText('Place lapses on'), { target: { value: c.lapses_on } });
}

describe("EntitySpecialists, rendered against the roster route's own answers", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("a generated entity is recommended a specialist, as a chargeable option, in the server's words", async () => {
    const r = captured.generated_empty;
    serve([ok(r)]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    expect((await screen.findByTestId('specialists-recommendation')).textContent).toBe(r.recommendation.said);
    expect(r.recommendation.recommended).toBe(true);
    expect(text('specialists-charge')).toBe(r.recommendation.charge);
    expect(text('specialists-when')).toBe(r.recommendation.when_warranted);
    expect(text('specialists-basis')).toBe(r.basis);
    expect(text('specialists-credential')).toBe(`Credentials: ${r.credential_basis}.`);
    expect(text('specialists-places')).toBe(`${r.places_left} of ${r.limit} places free`);
    expect(screen.getByTestId('specialists-none')).toBeTruthy();
  });

  it('an entity whose record names no generating door is told, by the server, that nothing is recommended', async () => {
    const r = captured.not_generated;
    serve([ok(r)]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    expect((await screen.findByTestId('specialists-recommendation')).textContent).toBe(r.recommendation.said);
    expect(r.recommendation.recommended).toBe(false);
    expect(text('specialists-recommendation')).not.toBe(captured.generated_empty.recommendation.said);
  });

  it('each specialist is shown by state: holding a place, lapsed, and retired with who, when and why', async () => {
    const r = captured.held;
    serve([ok(r)]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    const [a] = r.active;
    const held = await screen.findByTestId(`specialist-${a.specialist_id}`);
    expect(held.textContent).toContain(`${a.name} — ${a.discipline}`);
    expect(held.textContent).toContain(`Credential as stated: ${a.credential_as_stated}`);
    expect(held.textContent).toContain(`the place lapses on ${a.lapses_on}`);
    const [l] = r.lapsed;
    expect(text(`specialist-lapsed-${l.specialist_id}`)).toContain(`lapsed: the place ran to ${l.lapses_on}`);
    const [x] = r.retired;
    expect(text(`specialist-retired-${x.specialist_id}`)).toBe(
      `${x.name} — ${x.discipline} · retired ${x.retired_at} by ${x.retired_by}: ${x.retired_reason}`);
    expect(screen.queryByTestId(`specialist-${l.specialist_id}`)).toBeNull();
    expect(screen.queryByTestId(`specialist-${x.specialist_id}`)).toBeNull();
    expect(text('specialists-places')).toBe(`${r.places_left} of ${r.limit} places free`);
    expect(screen.queryByTestId('specialists-none')).toBeNull();
  });

  it('an attach sends the five things the clause names and nothing else, and the roster is read again', async () => {
    const sent = serve([ok(captured.generated_empty), ok(captured.after_attach)], [ok(captured.attached)]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    await screen.findByTestId('specialists-recommendation');
    fill(captured.attach_request);
    fireEvent.click(screen.getByText('Attach a specialist'));
    const s = captured.attached.specialist;
    expect(await screen.findByTestId(`specialist-${s.specialist_id}`)).toBeTruthy();
    expect(sent).toEqual([{ url: `/api/v1/entity-specialists/${captured.vsb_id}`, body: captured.attach_request }]);
    expect(text('specialists-done')).toBe(`Attached: ${s.name}.`);
    expect(screen.queryByTestId('specialists-refused')).toBeNull();
  });

  it("an attach the server refuses is shown in its own words, and nothing is drawn as attached", async () => {
    serve([ok(captured.held)], [{ status: 409, body: { detail: captured.refused_full } }]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    await screen.findByTestId('specialists-recommendation');
    fill(captured.attach_request);
    fireEvent.click(screen.getByText('Attach a specialist'));
    expect((await screen.findByTestId('specialists-refused')).textContent).toBe(`Failed (HTTP 409): ${captured.refused_full}`);
    expect(screen.queryByTestId('specialists-done')).toBeNull();
  });

  it("a retirement sends the reason typed for it, and a refused one is shown in the server's words", async () => {
    const [a] = captured.held.active;
    const sent = serve([ok(captured.held)], [{ status: 422, body: { detail: captured.refused_reason } }]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    await screen.findByTestId(`specialist-${a.specialist_id}`);
    fireEvent.change(screen.getByLabelText(`Reason for retiring ${a.name}`), { target: { value: 'the engagement ended' } });
    fireEvent.click(screen.getByText('Retire'));
    expect((await screen.findByTestId('specialists-refused')).textContent).toBe(`Failed (HTTP 422): ${captured.refused_reason}`);
    expect(sent).toEqual([{ url: `/api/v1/entity-specialists/${captured.vsb_id}/${a.specialist_id}/retire`,
      body: { reason: 'the engagement ended' } }]);
  });

  it('a refused read is said, and never drawn as an empty roster or a recommendation', async () => {
    serve([{ status: 503, body: { detail: captured.unreadable } }]);
    render(<EntitySpecialists vsbId={captured.vsb_id} />);
    expect((await screen.findByTestId('specialists-unread')).textContent).toBe(
      `Could not read this entity's roster — Failed (HTTP 503): ${captured.unreadable}`);
    expect(screen.queryByTestId('specialists-none')).toBeNull();
    expect(screen.queryByTestId('specialists-recommendation')).toBeNull();
    expect(screen.queryByTestId('specialists-places')).toBeNull();
  });
});
