// W979 (FU-399 part 12) — the Forge page, rendered against the forge routes' own answers.
//
// A person composes a pipeline of the IDBO's digital resources here, configures each stage, runs it, reads what the
// framing, each stage and the integration produced and what served each one, and can run it again with the same
// configuration. Six guards read the page's source. This mounts the real page against the answers the routes gave on
// a fresh store (ForgePipeline.fixture.json, captured by w979_capture.py: the stages, one run of a made-up objective
// with a configured stage, its rerun, and two refusals), drives it as a person would, and reads each claim in the DOM.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ForgePipeline.fixture.json';
import { ForgePipeline } from './ForgePipeline';

// a reply: a JSON body, or `text` for a body that is not JSON (a proxy's error page)
type Reply = { status: number; body?: unknown; text?: string };
const ok = (body: unknown): Reply => ({ status: 200, body });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: { resources?: Reply; run?: Reply; rerun?: Reply } = {}) {
  const calls: { url: string; init?: RequestInit }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    const reply = (r: Reply) => ({
      ok: r.status < 400, status: r.status, statusText: '',
      json: async () => {
        if (r.text !== undefined) throw new SyntaxError(`Unexpected token '<', "${r.text.slice(0, 8)}"... is not valid JSON`);
        return r.body;
      },
    });
    if (url === '/api/v1/forge/resources') return reply(a.resources ?? ok(captured.resources));
    if (url === '/api/v1/forge/run') return reply(a.run ?? ok(captured.run));
    if (url.endsWith('/rerun')) return reply(a.rerun ?? ok(captured.rerun));
    return reply({ status: 404, body: { detail: `not served in this test: ${url}` } });
  }));
  return calls;
}

function mount() {
  return render(
    <MemoryRouter>
      <ForgePipeline />
    </MemoryRouter>,
  );
}

const resource = (id: string) => {
  const r = captured.resources.resources.find(x => x.id === id);
  if (!r) throw new Error(`the fixture holds no ${id} stage`);
  return r;
};
const declaredLine = (id: string) =>
  `declares ${Object.entries(resource(id).params).map(([k, t]) => `${k} (${t})`).join(', ')}`;
// the stages the page selects before anything is clicked
const DEFAULT = ['petri_dish', 'laboratory', 'factory'];

async function runIt() {
  fireEvent.change(screen.getByPlaceholderText(/Objective to forge/), { target: { value: captured.run.objective } });
  fireEvent.click(screen.getByRole('button', { name: 'Run Forge Pipeline' }));
}

describe('ForgePipeline, rendered against the forge routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the stages offered are the API\'s, and each selected stage names the keys it declares and offers its own', async () => {
    serve();
    mount();
    for (const r of captured.resources.resources) expect(await screen.findByText(r.name)).toBeTruthy();
    const declared = await screen.findAllByTestId('forge-stage-declared');
    await screen.findByText(declaredLine('petri_dish'));
    expect(declared.map(d => d.textContent)).toEqual(DEFAULT.map(declaredLine));
    for (const id of DEFAULT) {
      const first = Object.keys(resource(id).params)[0];
      expect(screen.getByLabelText(`configuration of ${id}`).getAttribute('placeholder')).toBe(`${first}=…`);
    }
  });

  it('a key its stage does not declare is said to be sent as typed, and a line with no = is said not to be sent', async () => {
    serve();
    mount();
    await screen.findByText(declaredLine('petri_dish'));
    expect(Object.keys(resource('petri_dish').params)).not.toContain('depth');
    expect(Object.keys(resource('laboratory').params)).toContain('depth');
    fireEvent.change(screen.getByLabelText('configuration of petri_dish'), { target: { value: 'depth=deep\nno equals sign' } });
    fireEvent.change(screen.getByLabelText('configuration of laboratory'), { target: { value: 'depth=deep' } });
    expect(screen.getByTestId('forge-config-undeclared').textContent).toBe(
      'these keys are not ones their stage declares, and are sent as typed all the same: petri_dish: depth');
    expect(screen.getByTestId('forge-config-unreadable').textContent).toContain('no equals sign');
  });

  it('each stage is sent with what was typed for it', async () => {
    const calls = serve();
    mount();
    await screen.findByText(declaredLine('petri_dish'));
    const sent = String((captured.run.stage_outputs[0].config as Record<string, unknown>).hypothesis);
    fireEvent.change(screen.getByLabelText('configuration of petri_dish'), { target: { value: `hypothesis=${sent}` } });
    await runIt();
    await screen.findByTestId('forge-ceo-framing');
    const post = calls.find(c => c.url === '/api/v1/forge/run');
    expect(JSON.parse(String(post?.init?.body)).stages).toEqual(
      captured.run.stage_outputs.map(s => ({ type: s.resource, config: s.config })));
  });

  it('a run shows the framing, what each stage is and what served it, and the whole run\'s badge as the whole run\'s', async () => {
    serve();
    mount();
    await runIt();
    const run = captured.run;
    await waitFor(() => expect(screen.getByTestId('forge-ceo-framing').textContent).toBe(run.ceo_framing));
    expect(screen.getByTestId('forge-ceo-served-by').textContent).toBe(`Served by: ${run.ceo_served_by}.`);
    const toggles = screen.getAllByTestId('forge-stage-toggle');
    expect(toggles).toHaveLength(run.stage_outputs.length);
    run.stage_outputs.forEach((s, i) => {
      fireEvent.click(toggles[i]);
      const scope = screen.getByTestId('forge-stage-scope');
      expect(scope.textContent).toContain(`served by ${s.served_by}.`);
      expect(screen.getByTestId('forge-stage-kind').textContent).toBe(s.kind_basis);
      expect(scope.parentElement?.textContent).toContain(s.output);
    });
    expect(screen.getByTestId('forge-integration-served-by').textContent).toBe(`Served by: ${run.integration_served_by}.`);
    expect(screen.getByText(run.integrated_deliverable, { normalizer: s => s })).toBeTruthy();
    const badge = screen.getByTestId('forge-deliverable-provenance');
    expect(badge.textContent).toContain('whole run:');
    expect(badge.getAttribute('title')).toContain(
      'this counts every call in the run: the framing, each stage and the integration. What served each one is said where it is shown.');
    expect(screen.getByTestId('forge-intent-gate').textContent).toBe(
      `intent gate: ${run.governance.status}${run.governance.content_screened === false ? ' · content not screened' : ''}`);
  });

  it('a call that failed is said as failed, and a record that never said what served it is said as not recorded', async () => {
    // each call is said for itself: the framing's call failed here and the integration's did not, and the other way
    const served = String(captured.run.integration_served_by);
    const failed = clone(captured.run);
    failed.ceo_served_by = null;
    failed.stage_outputs[0].served_by = null;
    serve({ run: ok(failed) });
    const first = mount();
    await runIt();
    await waitFor(() => expect(screen.getByTestId('forge-ceo-served-by').textContent).toBe('Served by: nothing — the call failed.'));
    expect(screen.getByTestId('forge-integration-served-by').textContent).toBe(`Served by: ${served}.`);
    fireEvent.click(screen.getAllByTestId('forge-stage-toggle')[0]);
    expect(screen.getByTestId('forge-stage-scope').textContent).toContain('served by nothing — the call failed.');
    first.unmount();

    const integrationFailed = clone(captured.run);
    integrationFailed.integration_served_by = null;
    serve({ run: ok(integrationFailed) });
    const second = mount();
    await runIt();
    await waitFor(() => expect(screen.getByTestId('forge-integration-served-by').textContent).toBe('Served by: nothing — the call failed.'));
    expect(screen.getByTestId('forge-ceo-served-by').textContent).toBe(`Served by: ${captured.run.ceo_served_by}.`);
    second.unmount();

    const before = clone(captured.run);
    delete before.integration_served_by;
    serve({ run: ok(before) });
    mount();
    await runIt();
    await waitFor(() => expect(screen.getByTestId('forge-integration-served-by').textContent).toBe('Served by: not recorded.'));
    expect(screen.getByTestId('forge-ceo-served-by').textContent).toBe(`Served by: ${captured.run.ceo_served_by}.`);
  });

  it('a refused run says the server\'s own sentence', async () => {
    serve({ run: { status: captured.refused_run.status, body: captured.refused_run.body } });
    mount();
    await runIt();
    expect(await screen.findByText(`HTTP ${captured.refused_run.status} — ${captured.refused_run.body.detail}`)).toBeTruthy();
    expect(screen.queryByTestId('forge-ceo-framing')).toBeNull();
  });

  it('a rerun shows its basis; a refused rerun says its status and reason; one whose body is not JSON says its status', async () => {
    serve();
    const a = mount();
    await runIt();
    fireEvent.click(await screen.findByTestId('forge-rerun'));
    await waitFor(() => expect(screen.getByTestId('forge-rerun-basis').textContent).toBe(captured.rerun.rerun_basis));
    a.unmount();

    serve({ rerun: { status: captured.refused_rerun.status, body: captured.refused_rerun.body } });
    const b = mount();
    await runIt();
    fireEvent.click(await screen.findByTestId('forge-rerun'));
    expect(await screen.findByText(`HTTP ${captured.refused_rerun.status} — ${captured.refused_rerun.body.detail}`)).toBeTruthy();
    b.unmount();

    serve({ rerun: { status: 502, text: '<html><body>Bad Gateway</body></html>' } });
    mount();
    await runIt();
    fireEvent.click(await screen.findByTestId('forge-rerun'));
    expect(await screen.findByText('HTTP 502')).toBeTruthy();
    expect(screen.queryByText(/not valid JSON/)).toBeNull();
  });

  it('a failed read of the stages is said, and no stage\'s keys are claimed', async () => {
    serve({ resources: { status: 503, body: { detail: 'the forge registry could not be read' } } });
    mount();
    await waitFor(() => expect(screen.getByTestId('read-failure').textContent).toBe(
      'Could not read the Forge resources — Failed (HTTP 503): the forge registry could not be read'));
    const declared = screen.getAllByTestId('forge-stage-declared');
    expect(declared).toHaveLength(DEFAULT.length);
    declared.forEach(d => expect(d.textContent).toBe('its keys were not read'));
    expect(screen.getByLabelText('configuration of petri_dish').getAttribute('placeholder')).toBe('key=value');
  });
});
