// W925 (P5.15, RELEASE — the Owner's ruling of 2026-10-12) — BOTH OPTIONS, before a tool's form, rendered against the
// API's own answers.
//
// Where a tool is offered, a person reads two things before typing into it: the tier of review the tool has reached,
// and the option of a qualified person with when one is warranted (and what release would leave with a person). This
// mounts the real DomainTool against answers GET /api/v1/review-options gave on a fresh store
// (DomainTool.fixture.json, captured by w925_capture.py): an unreviewed Care tool, a Religion tool the ruling keeps
// with a scholar, a Science tool after a person's signature was recorded, and an engine that declares no tool.
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DomainTool.fixture.json';
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
