// W988 (FU-399 part 20) — the Business Plan page, rendered against the plan routes' own answers.
//
// The page shows a scope's living plan: its opening with the Owner's edits, the strategic layer and the action plan,
// the living cadence, the roadmap, and the objectives with their reviews. This mounts the real page against the
// answers its routes gave on a fresh store (BusinessPlan.fixture.json, captured by w988_capture.py: an empty plan,
// then one made-up objective reviewed once), and has the server refuse each action and the plan's own read. A mean
// over no objective is not a measurement, and a refusal is said with the server's reason.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './BusinessPlan.fixture.json';
import { BusinessPlan } from './BusinessPlan';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });

const PLAN = '/api/v1/business-plan?scope=workstation';
const CADENCE = '/api/v1/organism/cadence?scope=workstation';
const OBJECTIVE = '/api/v1/business-plan/objective';
const SET = '/api/v1/business-plan/set';
const one = captured.plan_one.objectives[0];
const REVIEW = `/api/v1/business-plan/objective/${one.id}/review`;

function serve(plan: Reply, over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [PLAN]: plan, [CADENCE]: ok(captured.cadence), [OBJECTIVE]: ok(captured.objective), [REVIEW]: ok(captured.review),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? { status: 404, body: { detail: `not served in this test: ${url}` } };
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const mount = () => render(<MemoryRouter><BusinessPlan /></MemoryRouter>);
//  what apiJson keeps of a refusal's reason
const said = (r: { status: number; body: { detail: string } }) => `Failed (HTTP ${r.status}): ${r.body.detail.slice(0, 300)}`;

describe('BusinessPlan, rendered against the plan routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('an empty plan: no objective, and no progress figure over none', async () => {
    serve(ok(captured.plan_empty));
    mount();
    expect(captured.plan_empty.objectives).toHaveLength(0);
    expect((await screen.findByTestId('plan-overall')).textContent).toBe(
      'No objective is recorded on this plan yet, so there is no progress to measure.');
    expect(screen.queryByText('0%')).toBeNull();
  });

  it('one objective, reviewed once: the figure and the roadmap are the plan\'s own', async () => {
    serve(ok(captured.plan_one));
    mount();
    expect((await screen.findByTestId('plan-overall')).textContent).toBe(
      `${one.progress_pct}%overall objective progress · 1 objective`);
    //  the objective's card, and the roadmap's next milestone, which names it
    expect(screen.getAllByText(one.title).length).toBeGreaterThanOrEqual(1);
    const rm = captured.plan_one.roadmap;
    expect(screen.getByText(`overall ${rm.overall_progress_pct}% · current: ${rm.current_phase}`)).toBeTruthy();
  });

  it('a refused objective says the server\'s reason, and the typed objective is kept', async () => {
    serve(ok(captured.plan_empty), { [OBJECTIVE]: captured.objective_refused });
    mount();
    const title = await screen.findByPlaceholderText('Objective');
    fireEvent.change(title, { target: { value: 'An objective the server will refuse' } });
    fireEvent.click(screen.getByRole('button', { name: /Add/ }));
    expect((await screen.findByTestId('plan-action-error')).textContent).toBe(
      `The objective was NOT saved: ${said(captured.objective_refused)}`);
    expect((screen.getByPlaceholderText('Objective') as HTMLInputElement).value).toBe('An objective the server will refuse');
  });

  it('a refused review says the server\'s reason', async () => {
    serve(ok(captured.plan_one), { [REVIEW]: captured.review_refused });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: '+25% progress' }));
    expect((await screen.findByTestId('plan-action-error')).textContent).toBe(
      `The review was NOT recorded: ${said(captured.review_refused)}`);
  });

  it('a refused owner edit says the field the server refused', async () => {
    serve(ok(captured.plan_one), { [SET]: captured.set_refused });
    mount();
    fireEvent.click((await screen.findAllByTestId('plan-owner-edit-open'))[0]);
    fireEvent.change(screen.getByLabelText('Mission'), { target: { value: 'A mission the server will refuse' } });
    fireEvent.click(screen.getByTestId('plan-owner-edit-save'));
    await waitFor(() => expect(screen.getByTestId('plan-action-error').textContent).toBe(
      `The owner edit was NOT saved: ${said(captured.set_refused)}`));
  });

  it('a plan that cannot be read is said with its file, and nothing written is said once', async () => {
    const r = captured.plan_unreadable;
    serve(r);
    mount();
    expect((await screen.findByTestId('plan-unreadable')).textContent).toContain(r.body.detail);
    expect(r.body.detail.match(/nothing was written/g)).toHaveLength(1);
    expect(screen.queryByTestId('plan-overall')).toBeNull();
  });
});
