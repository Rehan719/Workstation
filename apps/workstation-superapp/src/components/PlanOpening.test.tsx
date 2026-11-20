// W1144 (FU-399 part 110, FU-1291) — THE PLAN'S OPENING, rendered against the plan routes' own answers.
//
// The opening (components/PlanOpening.tsx, W505) heads the Business Plan page and the cockpit's plan tab. A text scan
// held it, and BusinessPlan's rendered test reached only its refused edit. This mounts the real component against what
// the routes answered for made-up entities and scopes (PlanOpening.fixture.json, captured by w1144_capture.py): an
// opening of templates, one holding the Owner's own concept, one a model composed (the owned model stood in as
// test_w471 stands it in), an edit made through the component's own form, an edit refused, and a plan with no opening.
// What each field's mark says is read from the field's own source in the plan, never from the date of an old edit.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './PlanOpening.fixture.json';
import PlanOpening from './PlanOpening';

type Answer = { status: number; body: any; request?: unknown };
const cases = captured.cases as any;
const ALL = ['executive_summary', 'concept', 'vision', 'mission', 'strategy'];
const ABOVE = ['executive_summary', 'concept', 'vision'];

//  the owner-edit route as it answered, each body posted kept; nothing else is served
function serveSet(answer: Answer) {
  const posted: unknown[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    if (url === '/api/v1/business-plan/set' && init?.method === 'POST') {
      posted.push(JSON.parse(String(init.body)));
      return { ok: answer.status < 400, status: answer.status, statusText: '', json: async () => answer.body };
    }
    return { ok: false, status: 599, statusText: '', json: async () => ({ detail: `the test served nothing for ${url}` }) };
  }));
  return posted;
}

function mount(plan: any, fields?: string[]) {
  const onSaved = vi.fn();
  const onError = vi.fn();
  const view = render(<PlanOpening plan={plan} scope={plan.scope} onSaved={onSaved} onError={onError} fields={fields} />);
  return { onSaved, onError, view };
}
const heading = () => screen.getByTestId('plan-opening-heading').textContent;
//  a field's mark, by the id the component builds for it (plan-<kind>-<field>)
const markEl = (kind: string, k: string) => screen.queryByTestId(`plan-${kind}-${k}`);
const mark = (kind: string, k: string) => markEl(kind, k)?.textContent ?? null;
const sentence = () => screen.getByTestId('plan-opening-written-by').textContent;

describe('PlanOpening, the plan\'s opening rendered against the plan routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('an opening of templates is headed as one, each field marked a template, under the sentence that says so', () => {
    const plan = cases.templated.plan.body;
    expect(ABOVE.map(k => plan.provenance.field_sources[k])).toEqual(ABOVE.map(() => 'establish_template'));
    mount(plan);
    expect(heading()).toBe('Plan opening — generated from your establish answers');
    expect(ABOVE.map(k => mark('templated', k))).toEqual(ABOVE.map(() => 'template'));
    expect(sentence()).toBe(plan.provenance.opening_written_by);
  });

  it('an opening holding the Owner\'s own concept is not headed as the Chief\'s, and the concept is marked the Owner\'s words', () => {
    const plan = cases.owner_concept.plan.body;
    expect(plan.provenance.field_sources.concept).toBe('owner_supplied');
    expect(plan.owner_edits?.concept).toBeFalsy();
    mount(plan);
    expect(heading()).toBe('Plan opening');
    expect(mark('owner-supplied', 'concept')).toBe('the Owner’s words');
    expect(mark('owner-edited', 'concept')).toBeNull();
    expect(['executive_summary', 'vision'].map(k => mark('templated', k))).toEqual(['template', 'template']);
    expect(sentence()).toBe(plan.provenance.opening_written_by);
  });

  it('an opening a model composed is the Chief\'s, and each field says in words who wrote it', () => {
    const plan = cases.composed.plan.body;
    const fs = plan.provenance.field_sources;
    expect(ABOVE.map(k => fs[k])).toEqual(['model_composed', 'model_composed', 'owner_supplied']);
    mount(plan);
    expect(heading()).toBe('Chief’s Opening');
    expect(['executive_summary', 'concept'].map(k => mark('source', k))).toEqual(['composed by a model', 'composed by a model']);
    expect(mark('owner-edited', 'concept')).toBeNull();
    expect(mark('owner-edited', 'vision')).toBe('owner-edited');
    expect(markEl('owner-edited', 'vision')?.getAttribute('title'))
      .toBe(`set by ${plan.owner_edits_by.vision} at ${plan.owner_edits.vision}`);
    expect(sentence()).toBe(plan.provenance.opening_written_by);
  });

  it('an edit made through the form sends what changed and the field emptied, and the plan read again marks the Owner\'s field', async () => {
    const c = cases.edit;
    const before = cases.templated.plan.body;
    const posted = serveSet(c.set);
    const { onSaved, onError, view } = mount(before, ALL);
    fireEvent.click(screen.getByTestId('plan-owner-edit-open'));
    fireEvent.change(screen.getByLabelText('Vision'), { target: { value: c.fields.vision } });
    fireEvent.change(screen.getByLabelText('Mission'), { target: { value: c.fields.mission } });
    fireEvent.click(screen.getByTestId('plan-owner-edit-save'));
    await waitFor(() => expect(onSaved).toHaveBeenCalledTimes(1));
    expect(posted).toEqual([c.set.request]);
    expect(onError).not.toHaveBeenCalled();
    expect(screen.queryByTestId('plan-owner-edit')).toBeNull();
    const after = c.plan_after.body;
    view.rerender(<PlanOpening plan={after} scope={after.scope} onSaved={onSaved} onError={onError} fields={ALL} />);
    expect(mark('owner-edited', 'vision')).toBe('owner-edited');
    expect(after.mission).toBe('');
    expect(mark('templated', 'mission')).toBeNull();
    expect(heading()).toBe('Plan opening');
    expect(sentence()).toBe(after.provenance.opening_written_by);
  });

  it('a refused edit says the field the server refused, keeps the typed words, and reads the plan again', async () => {
    const c = cases.refused;
    const plan = cases.owner_concept.plan.body;
    const posted = serveSet(c.set);
    const { onSaved, onError } = mount(plan, ALL);
    fireEvent.click(screen.getByTestId('plan-owner-edit-open'));
    fireEvent.change(screen.getByLabelText('Mission'), { target: { value: c.fields.mission } });
    fireEvent.click(screen.getByTestId('plan-owner-edit-save'));
    await waitFor(() => expect(onError).toHaveBeenCalledWith(
      `The owner edit was NOT saved: Failed (HTTP ${c.set.status}): ${c.set.body.detail}`));
    expect(posted).toEqual([c.set.request]);
    expect((screen.getByLabelText('Mission') as HTMLTextAreaElement).value).toBe(c.fields.mission);
    expect(onSaved).toHaveBeenCalledTimes(1);
  });

  it('a plan with no opening says none is recorded and still offers the edit', () => {
    const plan = cases.none.plan.body;
    expect(ALL.map(k => plan[k])).toEqual(ALL.map(() => ''));
    mount(plan);
    expect(screen.getByText('No opening recorded yet — nothing here is the Chief’s framing until the owned model '
      + 'composes it or you set it.')).toBeTruthy();
    expect(screen.queryByTestId('plan-opening-heading')).toBeNull();
    expect(screen.getByTestId('plan-owner-edit-open')).toBeTruthy();
  });
});
