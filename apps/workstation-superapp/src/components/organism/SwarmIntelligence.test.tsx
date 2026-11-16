// W1063 (FU-399 part 77) — the organism's Swarm Intelligence hub, rendered against its routes' own answers.
//
// The hub runs an org cascade for a mission (Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order), grounded
// in a chosen entity's living plan, lists the cascades that ran with a way to accept an entity's delivery, and lists
// the completed delegate runs. This mounts the real hub against what each route answered on a fresh store with no
// model installed (SwarmIntelligence.fixture.json, captured by w1063_capture.py: every read on opening a store
// holding one entity established through Genesis, that entity's plan, a cascade for a made-up mission scoped to it,
// the two run lists after it, the delivery accepted and the route's refusals of an acceptance, and each run list's
// own 500). Rendering found the hub drawing every tier of the delivery cut, unmarked (the Build-to-Order delivery at
// 1,400 of its 2,088 characters, each officer's at 700), saying the cascade history as empty before it was read,
// saying a refused acceptance as a history it could not read (the list it had read was taken off the page), offering
// no objective from a plan it could not read without saying so, and a refresh that read the delegate runs alone.
// Fixed in this round.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './SwarmIntelligence.fixture.json';
import SwarmIntelligence from './SwarmIntelligence';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const VID = captured.vsb_id;
const ENTITY = captured.entities.body.entities[0];
const RUNS = '/api/v1/swarm/runs';
const HISTORY = '/api/v1/swarm/cascade/runs';
const ENTITIES = '/api/v1/vsb';
const PLAN = `/api/v1/business-plan?scope=${encodeURIComponent(VID)}`;
const CASCADE = '/api/v1/swarm/cascade';
const RUN = captured.cascade_runs_after.body.runs[0];
const ACCEPT = `/api/v1/swarm/cascade/runs/${RUN.run_id}/accept`;
const DELIVERY = captured.cascade.body;

const refusal = (a: Answer) => Object.assign(new Error(`Request failed with status code ${a.status}`),
  { isAxiosError: true, response: { status: a.status, data: a.body } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  each route as it answered; a case replaces an answer or holds one back. Each read of the cascade history takes
//  the next answer in `history` (the last one stays), and each acceptance the next in `accept`
function serve(plan: { runs?: Reply; history?: Reply[]; plan?: Reply; accept?: Reply[] } = {}) {
  const history = [...(plan.history ?? [captured.cascade_runs, captured.cascade_runs_after])];
  const accepts = [...(plan.accept ?? [captured.accepted])];
  const calls: { method: string; url: string; body?: unknown }[] = [];
  const answer = async (r: Reply) => {
    const a = await r;
    if (a === 'unreachable') throw unreached();
    if (a.status >= 400) throw refusal(a);
    return { status: a.status, data: a.body };
  };
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    calls.push({ method: 'GET', url });
    if (url === RUNS) return answer(plan.runs ?? captured.runs) as never;
    if (url === HISTORY) return answer(history.length > 1 ? history.shift()! : history[0]) as never;
    if (url === ENTITIES) return answer(captured.entities) as never;
    if (url === PLAN) return answer(plan.plan ?? captured.plan) as never;
    throw refusal({ status: 404, body: { detail: `not served here: ${url}` } });
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string, body?: unknown) => {
    calls.push({ method: 'POST', url, body });
    if (url === ACCEPT) return answer(accepts.length > 1 ? accepts.shift()! : accepts[0]) as never;
    throw refusal({ status: 404, body: { detail: `not served here: ${url}` } });
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    calls.push({ method: init?.method ?? 'GET', url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    if (url === CASCADE) return { ok: true, status: 200, json: async () => captured.cascade.body } as unknown as Response;
    return { ok: false, status: 404, json: async () => ({ detail: `not served here: ${url}` }) } as unknown as Response;
  }));
  return calls;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const mount = () => render(<SwarmIntelligence />);
//  the living plan to ground the cascade in, once the entities are read
async function chooseEntityPlan() {
  await waitFor(() => expect(screen.getByRole('option', { name: ENTITY.name })).toBeTruthy());
  fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: VID } });
}
const preUnder = (label: string) => screen.getByText(label).closest('details')!.querySelector('pre')!;

describe('SwarmIntelligence, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('says on opening what each read answered: no delegate run, no cascade yet, and the entity to ground one in', async () => {
    serve();
    mount();
    await waitFor(() => expect(screen.getByTestId('cascade-runs-empty').textContent).toBe('No persisted cascade runs yet.'));
    expect(screen.getByTestId('swarm-runs-panel-empty')).toBeTruthy();
    expect(screen.getByTestId('swarm-runs-empty')).toBeTruthy();
    await waitFor(() => expect(screen.getByRole('option', { name: ENTITY.name })).toBeTruthy());
    expect(screen.queryByTestId('read-failures')).toBeNull();
  });

  it('never says the cascade history is empty before it has been read', async () => {
    const first = held(captured.cascade_runs);
    serve({ history: [first.reply] });
    mount();
    await waitFor(() => expect(screen.getByTestId('swarm-runs-panel-empty')).toBeTruthy());
    expect(screen.queryByTestId('cascade-runs-empty')).toBeNull();
    await act(async () => { first.letGo(); });
    await waitFor(() => expect(screen.getByTestId('cascade-runs-empty')).toBeTruthy());
  });

  it('offers the open objectives of the entity whose plan is chosen', async () => {
    serve();
    mount();
    await chooseEntityPlan();
    for (const o of captured.plan.body.objectives.filter(x => x.status !== 'done')) {
      await waitFor(() => expect(screen.getByRole('option', { name: `[${o.status}] ${o.title}` })).toBeTruthy());
    }
  });

  it('says a plan whose objectives could not be read, rather than offering none', async () => {
    serve({ plan: 'unreachable' });
    mount();
    await chooseEntityPlan();
    await waitFor(() => expect(screen.getByTestId('read-failures').textContent).toBe(
      "Could not read the living plan's objectives — Failed — backend unreachable."));
    expect(screen.getAllByRole('option').filter(o => (o.textContent ?? '').startsWith('['))).toHaveLength(0);
  });

  it('runs the cascade the person asked for, in the chosen plan, and draws every tier of its delivery whole', async () => {
    const calls = serve();
    mount();
    await chooseEntityPlan();
    fireEvent.change(screen.getByPlaceholderText('Describe the mission for the agent swarm...'), { target: { value: captured.mission } });
    fireEvent.click(screen.getByRole('button', { name: 'Cascade' }));
    await waitFor(() => expect(screen.getByText('Build-to-Order — operational delivery')).toBeTruthy());
    expect(calls.find(c => c.url === CASCADE)!.body).toEqual(captured.ask);
    const tiers: [string, string][] = [
      ['Chief of the Board (the founder\'s standing charter — no twin model is trained)', DELIVERY.level_0_chief_of_board],
      ['Board of Directors — action plan', DELIVERY.level_0b_board_resolution],
      ['AI CEO — directive', DELIVERY.level_1_ceo_directive],
      ['Business Transformation Office', DELIVERY.level_4_business_transformation_office],
      ['Build-to-Order — operational delivery', DELIVERY.level_5_build_to_order],
      ['Products & Services catalogue', DELIVERY.products_services_catalogue],
    ];
    expect(DELIVERY.level_5_build_to_order.length).toBeGreaterThan(1400);
    for (const [label, text] of tiers) expect(preUnder(label).textContent).toBe(text);
    const officers = screen.getByText(/C-Suite → Centres of Excellence/).closest('details')!;
    const csuite = DELIVERY.level_2_csuite as Record<string, string>;
    const coe = DELIVERY.level_3_coe as Record<string, string>;
    for (const role of DELIVERY.csuite_roster.engaged) {
      const pres = Array.from(officers.querySelectorAll('pre')).map(p => p.textContent);
      expect(pres).toContain(csuite[role]);
      expect(pres).toContain(`↳ CoE — ${coe[`${role} CoE`]}`);
    }
    const appraisal = screen.getByTestId('cascade-appraisal-heading').closest('details')!;
    const appraised = Array.from(appraisal.querySelectorAll('pre')).map(p => p.textContent);
    for (const v of Object.values(DELIVERY.appraisals as Record<string, string>)) expect(appraised).toContain(v);
    //  and the history read after it lists the run, with the way to accept the entity's delivery
    await waitFor(() => expect(screen.getByTestId('cascade-run-accept')).toBeTruthy());
  });

  it('says who accepted a delivery, and which version', async () => {
    const calls = serve({ history: [captured.cascade_runs_after, captured.cascade_runs_accepted] });
    mount();
    await waitFor(() => expect(screen.getByTestId('cascade-run-accept')).toBeTruthy());
    fireEvent.click(screen.getByTestId('cascade-run-accept'));
    const acc = captured.cascade_runs_accepted.body.runs[0].acceptance!;
    await waitFor(() => expect(screen.getByTestId('cascade-run-accepted').textContent).toBe(
      `accepted by ${acc.accepted_by} (not verified) at ${acc.at} — version ${acc.delivery_sha256.slice(0, 12)} — earned nothing by itself`));
    expect(calls.find(c => c.url === ACCEPT)!.body).toEqual({ delivery_sha256: RUN.delivery_sha256 });
  });

  it('says a refused acceptance beside its button, and the history it had read stays on the page', async () => {
    serve({ history: [captured.cascade_runs_after], accept: [captured.accept_again] });
    mount();
    await waitFor(() => expect(screen.getByTestId('cascade-run-accept')).toBeTruthy());
    fireEvent.click(screen.getByTestId('cascade-run-accept'));
    await waitFor(() => expect(screen.getByTestId('cascade-run-accept-error').textContent).toBe(
      `Not accepted: Failed (HTTP 409): ${captured.accept_again.body.detail}`));
    expect(screen.queryByTestId('cascade-runs-unreadable')).toBeNull();
    expect(screen.getByText(RUN.mission)).toBeTruthy();
  });

  it('says a run list it could not read with the route\'s reason, and reads both lists again when asked', async () => {
    serve({ runs: captured.runs_failed, history: [captured.cascade_runs_failed, captured.cascade_runs] });
    mount();
    await waitFor(() => expect(screen.getByTestId('cascade-runs-unreadable').textContent).toBe(
      `The cascade history could not be read (Failed (HTTP 500): ${captured.cascade_runs_failed.body.detail}) — whether any cascade ran is unknown.`));
    expect(screen.getByTestId('swarm-runs-panel-unreadable').textContent).toBe(
      `The run list could not be read (Failed (HTTP 500): ${captured.runs_failed.body.detail}) — whether any run exists is unknown.`);
    fireEvent.click(screen.getByRole('button', { name: 'Read the run lists again' }));
    await waitFor(() => expect(screen.getByTestId('cascade-runs-empty')).toBeTruthy());
    expect(screen.queryByTestId('cascade-runs-unreadable')).toBeNull();
  });

  // W1109 (FU-399 part 98) - the chips and headings the hub draws, read against the routes' own answers
  it('on opening, the axis the cascade runs on, the delegate runs heading and the QMS chart\'s caption are said', async () => {
    serve();
    mount();
    const ask = captured.ask;
    await waitFor(() => expect(screen.getByTestId('cascade-axis-fixed').textContent).toBe(
      `runs as domain ${ask.domain} · realm ${ask.realm} — fixed on this tab whatever the mission says; no CoE specialism is sent`));
    expect(screen.getByTestId('emergence-heading').textContent).toBe('Completed delegate runs (most recent first)');
    expect(screen.getByTestId('pareto-title').textContent).toBe('QMS coverage vs run duration (gate-assessed runs only)');
  });

  it('a cascade\'s chips say the run\'s own figures: its axis, the intent gate, BMS, EMS, what operated, and the fabric', async () => {
    serve();
    mount();
    await chooseEntityPlan();
    fireEvent.change(screen.getByPlaceholderText('Describe the mission for the agent swarm...'), { target: { value: captured.mission } });
    fireEvent.click(screen.getByRole('button', { name: 'Cascade' }));
    const ask = captured.ask;
    await waitFor(() => expect(screen.getByTestId('cascade-axis').textContent).toBe(`run as: ${ask.domain} / ${ask.realm}`));
    const gov = DELIVERY.governance;
    expect(gov.content_screened).toBe(true);
    expect(screen.getByTestId('cascade-gov-chip').textContent).toBe(`intent gate: ${gov.status}`);
    expect(screen.getByTestId('cascade-gov-chip').getAttribute('title')).toBe(gov.scope);
    const ms = DELIVERY.management_systems;
    expect(screen.getByTestId('bms-chip').textContent).toBe(
      `BMS ${ms.bms.status.replace(/_/g, ' ')} · $${ms.bms.cost_per_insight_usd}/insight (sim)`);
    expect(screen.getByTestId('bms-chip').getAttribute('title')).toBe(ms.bms.status_basis);
    expect(screen.getByTestId('ems-chip').textContent).toBe(
      `EMS · CO₂ this run ${ms.ems.co2_kg_this_run}kg (est.) · process total ${ms.ems.process_total_co2_kg}kg`
      + ` · efficiency ${ms.ems.efficiency_gain_constant} (constant, not measured)`);
    expect(screen.getByTestId('ems-chip').getAttribute('title')).toBe(ms.ems.caveat);
    expect(screen.getByTestId('mgmt-operated-chip').textContent).toBe(`mgmt operated: ${ms.operated_this_run.join('·')}`);
    expect(screen.getByTestId('mgmt-operated-chip').getAttribute('title')).toBe(ms.operated_basis);
    const fr = DELIVERY.fabric_requisitions;
    const fs = DELIVERY.fabric_requisitions_summary;
    expect('records_queried' in fs).toBe(false);
    const queried = fr.filter(f => f.kind === 'query').length;
    expect(screen.getByTestId('fabric-requisitions-heading').textContent).toBe(
      `§7 fabric requisitioned (${fr.length}) — ${fs.facilities_ran} ran, ${fs.state_read + queried} read only`);
  });

  it('the delegate runs panel says a run list it could not read as unknown, with the route\'s reason', async () => {
    serve({ runs: captured.runs_failed, history: [captured.cascade_runs_failed, captured.cascade_runs] });
    mount();
    await waitFor(() => expect(screen.getByTestId('swarm-runs-unreadable').textContent).toBe(
      `[--:--:--] UNREADABLE: the swarm run list could not be read (Failed (HTTP 500): ${captured.runs_failed.body.detail})`
      + ' — whether any run exists is unknown.'));
  });
});
