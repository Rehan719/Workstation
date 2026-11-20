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
import { DomainTool, KEEPS_NOTHING, OWN_MATTER_SURFACES } from './DomainTool';

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

// W1104 (FU-399 part 93) — WHAT THE FLOOR DID AND DID NOT DO, SAID UNDER THE ANSWER, against the care plan route's own
// answers (DomainTool.fixture.json, captured by w1104_capture.py on a fresh store with no model, asked as the Care page
// asks: its five fields, as CareHub.tsx declares them). One answer is for a reader whose language is Welsh, with a
// made-up profile on record; one names a gambling support group among the care needs. Each note is the server's own
// sentence, under the answer it belongs to, and a note the answer does not call for is not drawn.
describe('DomainTool, what the floor did and did not do, said under the answer, rendered', () => {
  const ENDPOINT = '/api/v1/care/care-plan';
  type Captured = { asked: { patient_profile: Record<string, string>; care_needs: string[] }; body: unknown };

  function serve() {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      const r = (status: number, body: unknown) => ({ ok: status < 400, status, statusText: '', json: async () => body });
      if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent(ENDPOINT)) {
        return r(captured.review_care_plan.status, captured.review_care_plan.body);
      }
      if (url === '/api/v1/native-ai/status') return r(200, captured.status);
      return r(599, { detail: `the test served nothing for ${url}` });
    }));
  }

  //  the Care page's care plan tool, its fields as CareHub.tsx declares them; the reader's language as the page keeps it
  async function ask(answer: Captured, language: string) {
    localStorage.setItem('ws_user_prefs_v1', JSON.stringify({ language }));
    const post = vi.spyOn(axios, 'post').mockResolvedValue({ data: answer.body } as never);
    render(
      <MemoryRouter>
        <DomainTool title="Care plan" description="what it does" endpoint={ENDPOINT} resultKey="care_plan"
          submitLabel="Build care plan"
          fields={[
            { name: 'patient_profile', label: 'Patient profile (key: value per line)', type: 'keyvalue', default: 'age: \ncondition: \nmobility: ' },
            { name: 'care_needs', label: 'Care needs (one per line)', type: 'list', placeholder: 'breathlessness management\nfalls prevention' },
            { name: 'setting', label: 'Setting', type: 'select', options: ['community', 'hospital', 'care_home', 'mental_health'], default: 'community' },
            { name: 'duration_weeks', label: 'Duration (weeks)', type: 'text', default: '4' },
            { name: 'care_model', label: 'Care model', type: 'text', default: 'person_centred' },
          ]} />
      </MemoryRouter>,
    );
    //  said once, for every tool, before anything is typed: what "own AI" delivers depends on what is serving
    expect(screen.getByTestId('tool-serving-note').textContent).toBe(
      '"Own AI" means an owned model when one is serving. When none is, the result is a structured frame built from '
      + 'what you typed, not model-written work, and the result says which it was.');
    fireEvent.change(screen.getByLabelText('Patient profile (key: value per line)'), { target: { value:
      Object.entries(answer.asked.patient_profile).map(([k, v]) => `${k}: ${v}`).join('\n') } });
    fireEvent.change(screen.getByLabelText('Care needs (one per line)'), { target: { value: answer.asked.care_needs.join('\n') } });
    fireEvent.click(screen.getByRole('button', { name: /Build care plan/ }));
    await waitFor(() => expect(post).toHaveBeenCalledTimes(1));
    const [url, body, config] = post.mock.calls[0] as unknown as [string, unknown, { headers: Record<string, string> }];
    expect(url).toBe(ENDPOINT);
    expect(body).toEqual(answer.asked);
    expect(config.headers['Accept-Language']).toBe(language);
  }

  afterEach(() => {
    localStorage.removeItem('ws_user_prefs_v1');
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('an answer composed in English for a Welsh reader says so, and that the saved profile did not shape it', async () => {
    const answer = captured.care_plan_welsh;
    const prov = answer.body.ai_provenance;
    serve();
    await ask(answer, answer.language);
    await waitFor(() => expect(screen.getByTestId('tool-language-note').textContent).toBe(prov.language_basis));
    expect(screen.getByTestId('tool-language-note').getAttribute('title')).toBe(prov.language_basis);
    expect(prov.language_basis.startsWith('NOT DELIVERED IN CY: ')).toBe(true);
    expect(screen.getByTestId('domain-profile-not-usable').textContent).toBe(`profile: ${prov.profile_basis}`);
    expect(screen.getByTestId('domain-floor-note').textContent).toBe(prov.floor_note);
    //  the screen could not clear it, and its REVIEW is not the echo's: no reason of the echo's is said
    expect(prov.quality_assurance.compliance_echo_only).toBe(false);
    expect(screen.getByTestId('domain-compliance-chip').textContent).toBe('§11 compliance REVIEW — the screen could not clear this output');
    expect(screen.queryByTestId('domain-compliance-echo')).toBeNull();
    //  the floor names no model, so no model is said to have answered
    expect(prov.served_identity.model).toBeNull();
    expect(screen.queryByTestId('domain-served-identity')).toBeNull();
  });

  it('a REVIEW that came only from the person\'s own words says the server\'s reason inside the verdict', async () => {
    const answer = captured.care_plan_echo;
    const prov = answer.body.ai_provenance;
    const qa = prov.quality_assurance;
    serve();
    await ask(answer, answer.language);
    await waitFor(() => expect(screen.getByTestId('domain-compliance-echo').textContent).toBe(qa.compliance_basis));
    expect(qa.compliance_echo_only).toBe(true);
    expect(screen.getByTestId('domain-compliance-chip').textContent).toBe(
      `§11 compliance REVIEW — the screen could not clear this output${qa.compliance_basis}`);
    expect(screen.getByTestId('domain-floor-note').textContent).toBe(prov.floor_note);
    //  asked in English and answered in English: no language note; no profile on record: no profile note
    expect([prov.language_requested, prov.language_delivered]).toEqual(['en', 'en']);
    expect(screen.queryByTestId('tool-language-note')).toBeNull();
    expect(prov.profile_state).toBe('none_written');
    expect(screen.queryByTestId('domain-profile-not-usable')).toBeNull();
  });
});

// W1169 (P5.11 clause 9) — ON THE ADVICE SURFACE A PERSON'S OWN MATTER WAITS FOR SIGN-IN. A Law form, signed out, keeps
// nothing typed and no answer in this browser, hands nothing to another page, and says so before the form; signed in,
// it keeps its work as before; a form off the advice surface keeps its work as before.
describe('DomainTool on the advice surface keeps nothing typed until a person is signed in', () => {
  const ANSWER = { analysis: 'w1169 the answer as it was shown', ai_provenance: { served_by: 'native' } };
  const kept = () => [localStorage, sessionStorage].flatMap(s =>
    Array.from({ length: s.length }, (_, i) => `${s.key(i)}=${s.getItem(s.key(i)!) ?? ''}`)).join('\n');

  async function run(endpoint: string) {
    vi.spyOn(axios, 'post').mockResolvedValue({ data: ANSWER } as never);
    serve({});
    render(
      <MemoryRouter>
        <DomainTool title="A tool" description="what it does" endpoint={endpoint} resultKey="analysis"
          fields={[{ name: 'question', label: 'Question', type: 'textarea' }]} />
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText('Question'), { target: { value: 'w1169 what the person typed' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate/ }));
    await screen.findByText(ANSWER.analysis);
  }

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    localStorage.clear();
    sessionStorage.clear();
  });

  it('a Law form, signed out: the sentence is said before the form, and nothing typed and no answer is kept', async () => {
    await run('/api/v1/law/research');
    const note = screen.getByTestId('tool-keeps-nothing');
    expect(note.textContent).toBe(KEEPS_NOTHING);
    expect(note.compareDocumentPosition(screen.getByLabelText('Question')) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(kept()).not.toContain('w1169 what the person typed');
    expect(kept()).not.toContain(ANSWER.analysis);
    expect(screen.queryByRole('button', { name: /Commercialise via Genesis/ })).toBeNull();
  });

  it('a Law form, signed in: the work is kept, as before', async () => {
    localStorage.setItem('workstation_token', 'w1169-a-token');
    await run('/api/v1/law/research');
    expect(screen.queryByTestId('tool-keeps-nothing')).toBeNull();
    expect(kept()).toContain('w1169 what the person typed');
  });

  it('a form off the advice surface keeps its work, as before', async () => {
    await run('/api/v1/science/methodology');
    expect(screen.queryByTestId('tool-keeps-nothing')).toBeNull();
    expect(kept()).toContain('w1169 what the person typed');
  });
});

// W1171 (P5.12's and P5.13's boundaries) — THE EDUCATION AND CARE FORMS KEEP NOTHING TYPED BEFORE SIGN-IN, as the Law
// forms do (W1169). Signed out, an Education form and a Care form keep nothing typed and no answer in this browser,
// hand nothing to another page, and say so before the form; signed in, each keeps its work as before. A claim raised
// against an answer kept nowhere still names it by the fingerprint of the text the copy and every download carry.
describe('DomainTool on the Education and Care forms keeps nothing typed until a person is signed in', () => {
  //  W965's answer and the sha256 of `${plan}\n\n_${disclaimer}_`, computed apart from the page when W965 was written
  const ANSWER = { plan: 'w965 the plan as it was shown', disclaimer: 'w965 a disclaimer that travels with it',
    ai_provenance: { served_by: 'native' } };
  const EXPORTED_SHA256 = '1842c10de0336bfbb6b2ec30d863a929114d3bd67cfa9784f75816c54b7c903f';
  const [claim] = claimed.answer_claims.claims;
  const sent: { url: string; body: any }[] = [];
  const kept = () => [localStorage, sessionStorage].flatMap(s =>
    Array.from({ length: s.length }, (_, i) => `${s.key(i)}=${s.getItem(s.key(i)!) ?? ''}`)).join('\n');

  async function run(endpoint: string) {
    sent.length = 0;
    vi.spyOn(axios, 'post').mockResolvedValue({ data: ANSWER } as never);
    vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
      const r = (status: number, body: unknown) => ({ ok: status < 400, status, statusText: '', json: async () => body });
      if (init?.method === 'POST') {
        sent.push({ url, body: JSON.parse(String(init.body ?? 'null')) });
        return r(200, { ...claim, state: 'OPEN' });
      }
      if (url.startsWith('/api/v1/review-options?endpoint=')) return r(599, { detail: 'the test served nothing here' });
      if (url === '/api/v1/native-ai/status') return r(200, captured.status);
      return r(200, {});
    }));
    render(
      <MemoryRouter>
        <DomainTool title="A tool" description="what it does" endpoint={endpoint} resultKey="plan" claimable
          fields={[{ name: 'notes', label: 'Notes', type: 'textarea' }]} />
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText('Notes'), { target: { value: 'w1171 what the person typed' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate/ }));
    await screen.findByText(ANSWER.plan);
  }

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    localStorage.clear();
    sessionStorage.clear();
  });

  it('the forms that keep nothing before sign-in are the Law, Education and Care forms', () => {
    expect(OWN_MATTER_SURFACES).toEqual(['/api/v1/law/', '/api/v1/education/', '/api/v1/care/']);
  });

  for (const endpoint of ['/api/v1/education/lesson-plan', '/api/v1/care/care-plan']) {
    it(`${endpoint}, signed out: the sentence is said before the form, and nothing typed and no answer is kept`, async () => {
      await run(endpoint);
      const note = screen.getByTestId('tool-keeps-nothing');
      expect(note.textContent).toBe(KEEPS_NOTHING);
      expect(note.compareDocumentPosition(screen.getByLabelText('Notes')) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      expect(kept()).not.toContain('w1171 what the person typed');
      expect(kept()).not.toContain(ANSWER.plan);
      expect(screen.queryByRole('button', { name: /Commercialise via Genesis/ })).toBeNull();
    });

    it(`${endpoint}, signed in: the work is kept, as before`, async () => {
      localStorage.setItem('workstation_token', 'w1171-a-token');
      await run(endpoint);
      expect(screen.queryByTestId('tool-keeps-nothing')).toBeNull();
      expect(kept()).toContain('w1171 what the person typed');
    });
  }

  it('a claim against a Care answer kept nowhere still names it by its fingerprint, never its text', async () => {
    await run('/api/v1/care/care-plan');
    fireEvent.change(screen.getByLabelText('What is wrong with this answer'), { target: { value: 'w1171 it leaves out the evening dose' } });
    fireEvent.click(screen.getByRole('button', { name: 'Raise a claim about this answer' }));
    await waitFor(() => expect(screen.getByTestId('domain-claim-done').textContent).toBe(`Raised: ${claim.claim_id} — OPEN.`));
    expect(sent).toEqual([{ url: '/api/v1/support/claims', body: {
      artefact_kind: 'answer', artefact_id: EXPORTED_SHA256,
      endpoint: '/api/v1/care/care-plan', served_by: 'native', what_is_wrong: 'w1171 it leaves out the evening dose' } }]);
    expect(kept()).not.toContain(ANSWER.plan);
    expect(JSON.stringify(sent)).not.toContain(ANSWER.plan);
  });
});
