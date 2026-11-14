// W925 (P5.15, RELEASE — the Owner's ruling of 2026-10-12) — BOTH OPTIONS, before a tool's form, rendered against the
// API's own answers.
//
// Where a tool is offered, a person reads two things before typing into it: the tier of review the tool has reached,
// and the option of a qualified person with when one is warranted (and what release would leave with a person). This
// mounts the real DomainTool against answers GET /api/v1/review-options gave on a fresh store
// (DomainTool.fixture.json, captured by w925_capture.py): an unreviewed Care tool, a Religion tool the ruling keeps
// with a scholar, a Science tool after a person's signature was recorded, and an engine that declares no tool.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DomainTool.fixture.json';
import claimed from './SupportClaims.fixture.json';   // W965 - the claim route's own answers
import { DomainTool } from './DomainTool';

type Reply = { status: number; body: unknown };

function serve(answers: Record<string, Reply>) {
  const asked: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const reply = (status: number, body: unknown) => ({ ok: status < 400, status, statusText: '', json: async () => body });
    if (url.startsWith('/api/v1/review-options?endpoint=')) {
      const endpoint = decodeURIComponent(url.slice('/api/v1/review-options?endpoint='.length));
      asked.push(endpoint);
      const a = answers[endpoint];
      return a ? reply(a.status, a.body) : reply(599, { detail: `the test served nothing for ${endpoint}` });
    }
    if (url === '/api/v1/native-ai/status') return reply(200, captured.status);       // ServingNow's own read
    return reply(200, {});
  }));
  return asked;
}

function mount(endpoint: string) {
  render(
    <MemoryRouter>
      <DomainTool title="A tool" description="what it does" endpoint={endpoint} resultKey="plan"
        fields={[{ name: 'notes', label: 'Notes', type: 'textarea' }]} />
    </MemoryRouter>,
  );
}

const text = (id: string) => screen.getByTestId(id).textContent;

describe('DomainTool, both options before the form, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('an unreviewed Care tool: the tier and the person, in the server\'s words, before anything can be typed', async () => {
    const o = captured.care.body;
    const asked = serve({ [captured.care.endpoint]: captured.care });
    mount(captured.care.endpoint);
    await screen.findByTestId('review-option-tier');
    expect(asked).toEqual([captured.care.endpoint]);
    expect(text('review-option-tier')).toBe(`Review reached: ${o.review.label} — ${o.review.basis}.`);
    expect(o.review.tier).toBe('unreviewed');
    expect(text('review-option-person')).toBe(`A qualified person — ${o.person.option} ${o.person.warranted_when}`);
    expect(text('review-option-release')).toBe(o.person.release);
    //  BEFORE the form: the options precede the first field and the button that runs the tool
    const options = screen.getByTestId('review-options');
    for (const later of [screen.getByLabelText('Notes'), screen.getByRole('button', { name: /Generate/ })]) {
      expect(options.compareDocumentPosition(later) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    }
  });

  it('a Religion tool the ruling keeps with a scholar says so, as well as when to ask one', async () => {
    const o = captured.religion.body;
    serve({ [captured.religion.endpoint]: captured.religion });
    mount(captured.religion.endpoint);
    await screen.findByTestId('review-option-release');
    expect(o.person.kept_by_the_ruling).toBeTruthy();
    expect(text('review-option-release')).toBe(o.person.release);
    expect(text('review-option-warranted')).toBe(` ${o.person.warranted_when}`);
    expect(screen.getByTestId('review-option-person').getAttribute('title')).toBe(o.person.basis);
  });

  it('a signed review is the tier shown, with the person\'s credential as they stated it', async () => {
    const o = captured.signed.body;
    serve({ [captured.signed.endpoint]: captured.signed });
    mount(captured.signed.endpoint);
    await screen.findByTestId('review-option-tier');
    expect(o.review.tier).toBe('signed_by_a_qualified_person');
    expect(text('review-option-tier')).toBe(`Review reached: ${o.review.label} — ${o.review.basis}.`);
  });

  it('an engine that declares no tool shows the server\'s sentence, and no tier', async () => {
    serve({ [captured.none.endpoint]: captured.none });
    mount(captured.none.endpoint);
    await screen.findByTestId('review-options-none');
    expect(text('review-options-none')).toBe((captured.none.body as { detail: string }).detail);
    expect(screen.queryByTestId('review-option-tier')).toBeNull();
    expect(screen.queryByTestId('review-options-error')).toBeNull();
  });

  it('a failure to read is said, and is never shown as a tier', async () => {
    serve({ [captured.care.endpoint]: { status: 500, body: { detail: 'the store could not be read' } } });
    mount(captured.care.endpoint);
    await screen.findByTestId('review-options-error');
    expect(text('review-options-error')).toContain('Failed (HTTP 500): the store could not be read');
    expect(screen.queryByTestId('review-option-tier')).toBeNull();
  });

  it('an answer that carries no tier is not shown as one', async () => {
    serve({ [captured.care.endpoint]: { status: 200, body: {} } });
    mount(captured.care.endpoint);
    await screen.findByTestId('review-options-error');
    expect(screen.queryByTestId('review-option-tier')).toBeNull();
    expect(screen.queryByTestId('review-option-person')).toBeNull();
  });

  it('a discipline with no statement of when a person is warranted says that, and guesses nothing', async () => {
    const body = JSON.parse(JSON.stringify(captured.care.body));
    body.person.warranted_when = null;
    body.person.basis = 'no statement of when a qualified person is warranted exists for the unnamed discipline, so none is given here';
    serve({ [captured.care.endpoint]: { status: 200, body } });
    mount(captured.care.endpoint);
    await screen.findByTestId('review-option-not-stated');
    expect(text('review-option-not-stated')).toBe(` ${body.person.basis}`);
    expect(screen.queryByTestId('review-option-warranted')).toBeNull();
  });
});

// W965 (FU-1190) — SAY THIS ANSWER IS WRONG, under the answer, against the claim route's own answers
// (SupportClaims.fixture.json, captured by w964_capture.py). The tool runs (its POST is axios's, answered here); the
// claim is raised with the sha256 of the one composition the copy and every download carry, the tool's route and what
// served it, and never the text. What was raised, what the claim holds and a refusal are the server's words.
describe('DomainTool, a claim that an answer is wrong, rendered', () => {
  const ENDPOINT = '/api/v1/care/care-plan';
  const ANSWER = { plan: 'w965 the plan as it was shown', disclaimer: 'w965 a disclaimer that travels with it',
    ai_provenance: { served_by: 'native' } };
  //  the sha256 of `${ANSWER.plan}\n\n_${ANSWER.disclaimer}_` - the text the copy and every download carry - computed
  //  apart from the page (Python's hashlib, when this test was written), so the page's own hashing is checked too
  const EXPORTED_SHA256 = '1842c10de0336bfbb6b2ec30d863a929114d3bd67cfa9784f75816c54b7c903f';
  const [claim] = claimed.answer_claims.claims;
  const sent: { url: string; body: any }[] = [];

  function claimServe(reply: { status: number; body: unknown }) {
    sent.length = 0;
    vi.spyOn(axios, 'post').mockResolvedValue({ data: ANSWER } as any);
    vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
      const r = (status: number, body: unknown) => ({ ok: status < 400, status, statusText: '', json: async () => body });
      if (init?.method === 'POST') {
        sent.push({ url, body: JSON.parse(String(init.body ?? 'null')) });
        return r(reply.status, reply.body);
      }
      if (url.startsWith('/api/v1/review-options?endpoint=')) return r(captured.care.status, captured.care.body);
      if (url === '/api/v1/native-ai/status') return r(200, captured.status);
      return r(200, {});
    }));
  }

  async function runThenClaim(claimable = true) {
    render(
      <MemoryRouter>
        <DomainTool title="A tool" description="what it does" endpoint={ENDPOINT} resultKey="plan" claimable={claimable}
          fields={[{ name: 'notes', label: 'Notes', type: 'textarea' }]} />
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText('Notes'), { target: { value: 'w965 what the person typed' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate/ }));
    await screen.findByText(ANSWER.plan);
  }

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('a claim is raised with the fingerprint of the answer as it is kept, its route and what served it, never its text', async () => {
    claimServe({ status: 200, body: { ...claim, state: 'OPEN' } });
    await runThenClaim();
    fireEvent.change(screen.getByLabelText('What is wrong with this answer'), { target: { value: 'w965 it leaves out the evening dose' } });
    fireEvent.click(screen.getByRole('button', { name: 'Raise a claim about this answer' }));
    await waitFor(() => expect(screen.getByTestId('domain-claim-done').textContent).toBe(`Raised: ${claim.claim_id} — OPEN.`));
    expect(text('domain-claim-basis')).toBe(claim.artefact.basis);
    expect(sent).toEqual([{ url: '/api/v1/support/claims', body: {
      artefact_kind: 'answer', artefact_id: EXPORTED_SHA256,
      endpoint: ENDPOINT, served_by: 'native', what_is_wrong: 'w965 it leaves out the evening dose' } }]);
    expect(JSON.stringify(sent)).not.toContain(ANSWER.plan);
  });

  it('a claim the server refuses is shown in its own words, and nothing is said to be raised', async () => {
    const detail = 'Not raised: a claim says what is wrong.';
    claimServe({ status: 422, body: { detail } });
    await runThenClaim();
    fireEvent.change(screen.getByLabelText('What is wrong with this answer'), { target: { value: 'w965 something' } });
    fireEvent.click(screen.getByRole('button', { name: 'Raise a claim about this answer' }));
    await waitFor(() => expect(screen.getByTestId('domain-claim-refused').textContent).toBe(`Failed (HTTP 422): ${detail}`));
    expect(screen.queryByTestId('domain-claim-done')).toBeNull();
  });

  it('where the route declares no tool, no claim is offered', async () => {
    claimServe({ status: 200, body: {} });
    await runThenClaim(false);
    expect(screen.queryByTestId('domain-claim')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Raise a claim about this answer' })).toBeNull();
  });
});
