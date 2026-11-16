// W987 (FU-399 part 19) — the Transformation Dashboard, rendered against its routes' own answers.
//
// The page shows the vision's pillars with their presence checks, the transformation plan, the orchestration cascade
// and its run history, and the delivery plan read live from the follow-up register. This mounts the real page against
// the answers its six routes gave on a fresh store (TransformationDashboard.fixture.json, captured by w987_capture.py:
// the register's lists cut to two entries, and one run record that cannot be parsed), has the server refuse each read
// and each action, and follows an action that fails and then succeeds.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { provenanceBadge } from '../lib/api';
import captured from './TransformationDashboard.fixture.json';
import { TransformationDashboard } from './TransformationDashboard';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const URL = {
  picture: '/api/v1/transformation', runs: '/api/v1/transformation/orchestrate/runs',
  followups: '/api/v1/plan/followups', tick: '/api/v1/transformation/tick',
  assess: '/api/v1/transformation/assess', orchestrate: '/api/v1/transformation/orchestrate',
};

//  each route answers its captured reply; `over` replaces one, and a list is answered in order, its last reply kept
function serve(over: Record<string, Reply | Reply[]> = {}) {
  const base: Record<string, Reply> = {
    [URL.picture]: ok(captured.picture), [URL.runs]: ok(captured.runs), [URL.followups]: ok(captured.followups),
    [URL.tick]: ok(captured.tick), [URL.assess]: ok(captured.assess), [URL.orchestrate]: ok(captured.orchestrate),
  };
  const queues: Record<string, Reply[]> = Object.fromEntries(
    Object.entries(over).map(([u, r]) => [u, Array.isArray(r) ? [...r] : [r]]));
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const q = queues[url];
    const r = (q ? (q.length > 1 ? q.shift()! : q[0]) : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const button = (name: string) => screen.getByRole('button', { name: new RegExp(name) });

describe('TransformationDashboard, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the picture, the runs and the plan are the routes\' own', async () => {
    serve();
    render(<TransformationDashboard />);
    const p = captured.picture;
    await screen.findByText(p.vision_summary);
    expect(screen.getByText(`${Math.round(p.realisation.overall_realisation * 100)}%`)).toBeTruthy();
    expect(screen.getByTestId('route-census').textContent).toBe(`Route census: ${p.realisation.route_census.basis}`);
    const checks = screen.getAllByTestId('pillar-checks');
    expect(checks).toHaveLength(p.realisation.pillars.length);
    p.realisation.pillars.forEach((pl, i) => expect(checks[i].textContent).toBe(
      `${pl.checks_met} of ${pl.checks_assessed} checks present · coverage, not delivery`));
    expect(screen.getByTestId('immediate-gaps-basis').textContent).toBe(p.transformation_plan.immediate_gaps_basis);
    expect(screen.getByTestId('plan-lists-basis').textContent).toBe(p.transformation_plan.plan_lists_basis);
    //  the run that was read is listed, and the record that could not be read is said, by its name
    expect(await screen.findAllByTestId('orchestration-run')).toHaveLength(captured.runs.runs.length);
    const u = captured.runs.unreadable_records[0];
    expect(screen.getByTestId('runs-unreadable').textContent).toBe(
      `1 run record could not be read, so it is not listed: ${u.record} (${u.error})`);
    expect(await screen.findByTestId('followups-card')).toBeTruthy();
    expect(screen.getByTestId('plan-live-stamp').textContent).toMatch(
      /^Read from the delivery plan and the follow-up register at .+ · refreshes every minute$/);
  });

  it('a refused read of the picture is said by what it was reading, and the runs are still shown', async () => {
    serve({ [URL.picture]: refused(503, 'the route census could not be built') });
    render(<TransformationDashboard />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure').map(e => e.textContent)).toContain(
      'Could not read the realisation picture — Failed (HTTP 503): the route census could not be built'));
    expect(screen.queryByText('Failed to load')).toBeNull();
    expect(await screen.findAllByTestId('orchestration-run')).toHaveLength(captured.runs.runs.length);
    expect(screen.getByTestId('runs-unreadable')).toBeTruthy();
    expect(await screen.findByTestId('followups-card')).toBeTruthy();
  });

  it('a refused re-read of the picture after a tick is said, and the next read clears it', async () => {
    serve({ [URL.picture]: [ok(captured.picture), refused(502, 'the census timed out'), ok(captured.picture)] });
    render(<TransformationDashboard />);
    await screen.findByText(captured.picture.vision_summary);
    fireEvent.click(button('Tick'));
    await waitFor(() => expect(screen.getAllByTestId('read-failure').map(e => e.textContent)).toContain(
      'Could not read the realisation picture — Failed (HTTP 502): the census timed out'));
    //  the picture as last read stays on the page
    expect(screen.getByText(captured.picture.vision_summary)).toBeTruthy();
    fireEvent.click(button('Tick'));
    await waitFor(() => expect(screen.queryAllByTestId('read-failure').map(e => e.textContent)).not.toContain(
      'Could not read the realisation picture — Failed (HTTP 502): the census timed out'));
  });

  it('a refused tick is said with its reason, and a tick that then succeeds clears it', async () => {
    serve({ [URL.tick]: [refused(503, 'the heartbeat is paused'), ok(captured.tick)] });
    render(<TransformationDashboard />);
    await screen.findByText(captured.picture.vision_summary);
    fireEvent.click(button('Tick'));
    await waitFor(() => expect(screen.getByTestId('action-error').textContent).toBe(' Failed (HTTP 503): the heartbeat is paused'));
    fireEvent.click(button('Tick'));
    await waitFor(() => expect(screen.queryByTestId('action-error')).toBeNull());
  });

  it('a refused orchestration is said, and one that then runs shows its cascade and clears it', async () => {
    serve({ [URL.orchestrate]: [refused(500, 'the board did not answer'), ok(captured.orchestrate)] });
    render(<TransformationDashboard />);
    await screen.findByText(captured.picture.vision_summary);
    fireEvent.click(button('Orchestrate'));
    await waitFor(() => expect(screen.getByTestId('action-error').textContent).toBe(' Failed (HTTP 500): the board did not answer'));
    fireEvent.click(button('Orchestrate'));
    await screen.findByText('Transformation Cascade · Chief → Build-to-Order', { exact: false });
    expect(screen.queryByTestId('action-error')).toBeNull();
    const v = captured.orchestrate.validation;
    expect(v.validated).toBeNull();
    //  the cascade's own verdict, and the run's in the history: neither is called validated
    expect(screen.getAllByText('NOT ASSESSABLE').length).toBeGreaterThanOrEqual(2);
    expect(screen.queryByText('VALIDATED')).toBeNull();
    expect(screen.getByText(v.report)).toBeTruthy();
  });

  it('an assessment says what composed it', async () => {
    serve();
    render(<TransformationDashboard />);
    await screen.findByText(captured.picture.vision_summary);
    fireEvent.click(button('Assess'));
    const a = captured.assess.ai_provenance;
    //  the shared helper's badge, whole: its label, its colour and its title (W453: never a label alone)
    const badge = provenanceBadge(a.served_by, a.is_external);
    const el = await screen.findByTestId('assessment-provenance');
    expect(el.textContent).toBe(badge.label);
    expect(el.className).toContain(badge.cls);
    expect(el.getAttribute('title')).toBe(badge.title ?? null);
  });

  it('the register not shipped is said as the route says it, and a refused read keeps its reason', async () => {
    serve({ [URL.followups]: ok(captured.followups_unavailable) });
    const { unmount } = render(<TransformationDashboard />);
    await waitFor(() => expect(screen.getByTestId('followups-card').textContent).toContain(captured.followups_unavailable.reason));
    expect(screen.getByTestId('plan-live-stamp').textContent).toBe(
      'The delivery plan has not been read yet · retrying every minute');
    unmount();
    serve({ [URL.followups]: refused(500, 'the register is locked') });
    render(<TransformationDashboard />);
    await waitFor(() => expect(screen.getByTestId('followups-card').textContent).toContain(
      'The follow-up register could not be loaded (Failed (HTTP 500): the register is locked).'));
  });

  // W1107 (FU-399 part 96) - the delivery plan says the register's own figures: where it is going, in rounds and
  // never a date, the plan's own completion, the next bundle, what is done and next, and how the rows are ordered
  it('the delivery plan\'s pace, completion, next bundle, next item and priority are the register\'s own figures', async () => {
    serve();
    render(<TransformationDashboard />);
    const f = captured.followups;
    const fc = f.forecast;
    const rounds = (n: number) => `${n} round${n === 1 ? '' : 's'}`;
    //  the state this answer is in, which decides what the page draws
    expect(fc.assessable).toBe(true);
    expect(fc.next_item.rounds_projected).not.toBeNull();
    expect(fc.items_rounds_projected).not.toBeNull();
    expect(fc.items_open_unmarked).toEqual([]);
    await waitFor(() => expect(screen.getByTestId('plan-pace').querySelectorAll('p')[1].textContent).toBe(
      `~${rounds(fc.next_item.rounds_projected)} to finish ${fc.next_item.slot} (${fc.next_item.open_rows} open rows) · `
      + `~${rounds(fc.all_rows_rounds_projected)} for all ${fc.open_rows} open rows`));
    expect(screen.getByTestId('plan-completion-pace').textContent).toBe(
      `~${rounds(fc.items_rounds_projected)} for the ${fc.items_open_build} open BUILD plan items`
      + ` · ${fc.items_open_owner_switch} the Owner flips (${fc.items_owner_switch_slots.join(', ')}) — not projected`);
    const bn = f.bundles.bundles[0];
    expect([bn.component_size > bn.size, bn.also_touching.length > 0, bn.above_measured_ceiling, bn.possibly_under_connected])
      .toEqual([true, true, false, false]);
    expect(screen.getByTestId('next-bundle').textContent).toBe(
      `NEXT BUNDLE: ${bn.slot} — one subsystem, ${bn.size} rows across ${bn.files_count} files`
      + ` · cut from a ${bn.component_size}-row component`
      + ` · advances ${bn.also_touching.join(', ')} (advances — their own ACCEPT criteria close them)`);
    expect(screen.getByTestId('plan-completion-basis').textContent).toBe(
      `At ${fc.item_build_rate_per_round} plan items per round — a rate measured entirely on ${fc.item_rate_phases.join(', ')},`
      + ' so it is the rate THAT work closed at, applied to phases whose work differs.'
      + ` Coverage: ${fc.items_sized_build} of ${fc.items_open_build} build items carry a registered row; the other`
      + ` ${fc.items_open_build - fc.items_sized_build} have never been sized, so this is the weakest figure on this page.`);
    expect(screen.getByTestId('plan-now').querySelector('p')?.textContent).toBe(
      `Done ${f.plan.done} of ${f.plan.total} items — ${f.plan.phases.map(p => `${p.phase} ${p.done}/${p.total}`).join(' · ')}`);
    expect(f.plan.next.followups).toBe(0);
    expect(screen.getByTestId('plan-next').textContent).toBe(`Next: ${f.plan.next.slot} ${f.plan.next.title} — no follow-ups ride it`);
    const pr = f.priority;
    const gp = pr.completion.by_phase[pr.gate_phase as keyof typeof pr.completion.by_phase];
    expect(pr.config_problems).toEqual([]);
    expect(screen.getByTestId('plan-priority').textContent).toBe(
      'Rows run highest priority first (vision area × truth tier × reach × criticality × breadth × effort; weights in '
      + `${pr.config}) · follow-up completion weighted by priority — ${pr.gate_phase}: ${gp.weighted_pct}% of its rows' priority`
      + ` closed (${gp.rows_closed} of ${gp.rows_closed + gp.rows_open} rows)`);
  });
});
