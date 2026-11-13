// W975 (FU-399 part 9) — the Horizon Guardrails page, rendered against the guardrails and seam routes' own answers.
//
// The page's most dangerous field is the human distress route: a person in distress might act on what it shows, so an
// unfilled field must read as unfilled, a stale route as stale, and a route for one place as covering that place only.
// It also says that the seam in front of the domain routes observes and does not gate, and that no gate certifies a
// subject was absent. Six guards read the page's source. This mounts the real page against the answers the routes gave
// on a fresh store (HorizonGuardrails.fixture.json, captured by w975_capture.py from TEST RECORDS that name no service
// and reach no one), reads each claim in the DOM, and has the server refuse each read.
import { render, screen, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './HorizonGuardrails.fixture.json';
import { HorizonGuardrails } from './HorizonGuardrails';

type Reply = { status: number; data: unknown } | Error;
const ok = (data: unknown): Reply => ({ status: 200, data });

function serve(guardrails: Reply, seam: Reply = ok(captured.seam)) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    const r = url === '/api/v1/horizon/guardrails' ? guardrails : url === '/api/v1/horizon/seam' ? seam
      : { status: 404, data: { detail: `not served in this test: ${url}` } };
    if (r instanceof Error) throw r;
    return r as never;
  });
}

const field = () => screen.findByTestId('horizon-distress-routes');
// The page chooses each route row's id by the route's freshness (horizon-route-row or horizon-route-stale-row), so
// those two ids are not literal attributes in its source; they are queried through template literals, as per-item ids
// are, and test_w975 holds that the page names both.

describe('HorizonGuardrails, rendered against the guardrails and seam routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('a route field with nothing it can show reads NOT SUPPLIED, as an alert, in the backend\'s own words', async () => {
    serve(ok(captured.refused));
    render(<HorizonGuardrails />);
    const f = await field();
    expect(f.getAttribute('data-route-state')).toBe('NOT_SUPPLIED');
    expect(f.getAttribute('role')).toBe('alert');
    expect(within(f).getByText('Not supplied')).toBeTruthy();
    expect(within(f).getByText(captured.refused.distress_routes_basis)).toBeTruthy();
    expect(f.textContent).toContain('REFUSED for want of a reviewer or a check date');
    expect(within(f).queryAllByTestId(`horizon-route-row`)).toHaveLength(0);
    expect(within(f).queryByTestId('horizon-routes-coverage')).toBeNull();
  });

  it('a fresh route is shown with its reviewer and check date, and says where it answers', async () => {
    serve(ok(captured.fresh));
    render(<HorizonGuardrails />);
    const f = await field();
    const r = captured.fresh.distress_routes[0];
    expect(f.getAttribute('data-route-state')).toBe('SUPPLIED_FRESH');
    expect(f.getAttribute('role')).toBeNull();
    const row = within(f).getByTestId(`horizon-route-row`);
    for (const part of [`route: ${r.route}`, `reviewed_by: ${r.reviewed_by}`, `checked_on: ${r.checked_on}`,
                        `jurisdiction: ${r.jurisdiction}`]) expect(row.textContent).toContain(part);
    expect(within(f).queryByTestId('horizon-routes-stale')).toBeNull();
    expect(within(f).queryByText('Not supplied')).toBeNull();
    const cover = within(f).getByTestId('horizon-routes-coverage');
    expect(cover.textContent).toContain('Reviewed as correct wherever the person is: it names no specific service.');
    expect(cover.textContent).toContain(captured.fresh.distress_routes_basis);
  });

  it('a stale route is shown as stale, beside the fresh one, and a route for named places covers those only', async () => {
    serve(ok(captured.stale));
    render(<HorizonGuardrails />);
    const f = await field();
    const s = captured.stale;
    expect(f.getAttribute('data-route-state')).toBe('SUPPLIED_STALE');
    expect(f.getAttribute('role')).toBe('alert');
    expect(within(f).getByTestId('horizon-routes-stale').textContent).toContain(
      `Last checked too long ago — ${s.distress_routes_stale_count} of ${s.distress_routes.length} route(s) may have ` +
      'changed since anyone confirmed them');
    const old = within(f).getAllByTestId(`horizon-route-stale-row`);
    expect(old).toHaveLength(1);
    expect(old[0].textContent).toContain(s.distress_routes.find(r => r.stale)!.route);
    expect(within(f).getAllByTestId(`horizon-route-row`)).toHaveLength(1);
    expect(within(f).getByTestId('horizon-routes-coverage').textContent).toContain(
      `Reviewed for ${s.distress_routes_jurisdictions.join(', ')} only — a person outside that is not covered by this route.`);
  });

  it('every gate refuses with the limit of what it looked at, and none certifies absence', async () => {
    serve(ok(captured.refused));
    render(<HorizonGuardrails />);
    await field();
    for (const g of captured.refused.gates) {
      expect(screen.getByText(`Refuses: ${g.refuses}`)).toBeTruthy();
    }
    expect(screen.getAllByText(`Did not look at: ${captured.refused.gates[0].limit}`)).toHaveLength(
      captured.refused.gates.length);
    expect(screen.getAllByText('certifies no absence')).toHaveLength(captured.refused.gates.length);
    expect(screen.queryByText('certifies absence')).toBeNull();
    expect(screen.getByText(`“${captured.refused.not_a_person_statement}”`)).toBeTruthy();
    for (const u of captured.refused.unchanged_refusals) expect(screen.getByText(`· ${u}`)).toBeTruthy();
    expect(screen.getByText(captured.refused.basis)).toBeTruthy();
  });

  it('the seam is said to observe and not gate, in its own sentences, with what it deliberately does not observe', async () => {
    serve(ok(captured.refused));
    render(<HorizonGuardrails />);
    const seam = await screen.findByTestId('horizon-seam');
    await within(seam).findByText('Observes · does not gate');
    for (const s of [captured.seam.gating_basis, captured.seam.decision_is_constant, captured.seam.body_basis,
                     captured.seam.basis]) expect(within(seam).getByText(s)).toBeTruthy();
    for (const k of Object.keys(captured.seam.not_observed_kinds)) expect(seam.textContent).toContain(k);
    expect(within(seam).queryByText('Gates requests')).toBeNull();
  });

  it('a refused guardrails read is said with the server\'s reason, shows no field, and the seam still says it does not gate', async () => {
    serve({ status: 503, data: { detail: 'the gate module could not be loaded' } });
    render(<HorizonGuardrails />);
    const said = await screen.findByText(/The guardrails are not reporting/);
    expect(said.textContent).toContain(
      'The guardrails are not reporting (HTTP 503: the gate module could not be loaded). Nothing is shown, because nothing was received.');
    expect(screen.queryByTestId('horizon-distress-routes')).toBeNull();
    expect(await screen.findByText('Observes · does not gate')).toBeTruthy();
  });

  it('a refused seam read is said with its reason, never as a seam that observed nothing; the guardrails still stand', async () => {
    serve(ok(captured.refused), { status: 500, data: { detail: 'the seam store could not be read' } });
    render(<HorizonGuardrails />);
    const seam = await screen.findByTestId('horizon-seam');
    const said = await within(seam).findByRole('alert');
    expect(said.textContent).toContain('The seam is not reporting (HTTP 500: the seam store could not be read).');
    expect(said.textContent).toContain('not that it observed nothing');
    expect(within(seam).queryByText('Observes · does not gate')).toBeNull();
    expect(await field()).toBeTruthy();
  });

  it('a read that never arrives says so, and a refusal with no reason is said by its status', async () => {
    serve(new Error('Network Error'), { status: 502, data: '<html>bad gateway</html>' });
    render(<HorizonGuardrails />);
    expect(await screen.findByText(/The guardrails could not be reached\./)).toBeTruthy();
    const seam = await screen.findByTestId('horizon-seam');
    expect((await within(seam).findByRole('alert')).textContent).toContain('The seam is not reporting (HTTP 502).');
  });
});
