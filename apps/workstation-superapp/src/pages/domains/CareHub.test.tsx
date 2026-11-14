// W976 (FU-399 part 10) — the Care page, rendered against the Care routes' own answers.
//
// What a person reads on the Care page is about care: where each tool's standard comes from, which hazards of the tools
// are guarded and which are not, and a risk score computed from the published chart before any narrative. Six guards
// read the page's source. This mounts the real page against the answers the Care routes gave on a fresh store
// (CareHub.fixture.json, captured by w976_capture.py from made-up observations), reads each claim in the DOM, and has
// the server refuse the two reads the page makes itself.
import { fireEvent, render, screen, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './CareHub.fixture.json';
import { CareHub } from './CareHub';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (detail: string): Reply => ({ status: 503, body: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: { tools?: Reply; hazards?: Reply } = {}) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const reply = ({ status, body }: Reply) => ({ ok: status < 400, status, statusText: '', json: async () => body });
    if (url === '/api/v1/care/tools') return reply(a.tools ?? ok(captured.tools));
    if (url === '/api/v1/care/hazards') return reply(a.hazards ?? ok(captured.hazards));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/handover')) return reply(ok(captured.review_handover));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/risk-assess')) return reply(ok(captured.review_risk));
    if (url === '/api/v1/native-ai/status') return reply(ok(captured.status));
    return reply({ status: 404, body: { detail: `not served in this test: ${url}` } });
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <AdaptiveUIProvider>
        <CareHub />
      </AdaptiveUIProvider>
    </MemoryRouter>,
  );
}

const tools = captured.tools.tools;
const OBSERVED_FULL = { resp_rate: '22', spo2: '93', oxygen: 'air', systolic_bp: '105', pulse: '112', temp: '38.4',
                        consciousness: 'alert' };
const FULL = Object.entries(OBSERVED_FULL).map(([k, v]) => `${k}: ${v}`).join('\n');

// the risk tab, the observations typed as a person types them (the made-up ones the capture sent), and Assess
async function assess(observations: string) {
  await screen.findAllByTestId('care-source-tool');
  fireEvent.click(screen.getByRole('button', { name: 'Risk Assess' }));
  fireEvent.change(await screen.findByLabelText('Observations / data (key: value per line)'), { target: { value: observations } });
  fireEvent.click(screen.getByRole('button', { name: /Assess risk/ }));
}
const runnable = tools.filter(t => t.type !== 'withheld' && t.type !== 'retired');

describe('CareHub, rendered against the Care routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('each tool says where its standard comes from, row by row, and a tool with no row says so', async () => {
    serve();
    mount();
    const card = await screen.findByTestId('care-sources');
    const rows = await within(card).findAllByTestId('care-source-tool');
    expect(rows).toHaveLength(tools.length);
    expect(within(card).getByText(captured.tools.sources_basis)).toBeTruthy();
    rows.forEach((row, i) => {
      const t = tools[i];
      expect(row.textContent).toContain(`${t.name}: ${t.standard}`);
      const sources = within(row).queryAllByTestId('care-source-row');
      expect(sources).toHaveLength((t.sources ?? []).length);
      (t.sources ?? []).forEach((s, j) => expect(sources[j].textContent).toBe(`${s.id} · ${s.status_said}`));
      if ((t.sources ?? []).length === 0) expect(row.textContent).toContain('no row of the register is named for this entry.');
    });
  });

  it('a refused read of the tools is said in the server\'s words, and no standard is claimed', async () => {
    serve({ tools: refused('The register of sources could not be read (OSError).') });
    mount();
    const said = await screen.findByTestId('care-sources-refusal');
    expect(said.textContent).toBe(
      'The tools and their sources could not be read: Failed (HTTP 503): The register of sources could not be read (OSError).');
    expect(screen.queryAllByTestId('care-source-tool')).toHaveLength(0);
  });

  it('the open hazard log lists each hazard with its guard, or says it is unguarded, and what it does not cover', async () => {
    serve();
    mount();
    const log = await screen.findByTestId('care-hazard-log');
    expect(within(log).getByText(captured.hazards.basis)).toBeTruthy();
    const rows = within(log).getAllByTestId('care-hazard');
    expect(rows).toHaveLength(captured.hazards.hazards.length);
    rows.forEach((row, i) => {
      const h = captured.hazards.hazards[i];
      expect(row.textContent).toContain(`${h.id} · ${h.tool} · ${h.hazard}`);
      expect(row.textContent).toContain(h.guarded ? `guarded: ${h.how}` : String(h.how));
      if (!h.guarded) expect(row.textContent).not.toContain('guarded:');
      if (h.residual) expect(row.textContent).toContain(`Not covered: ${h.residual}.`);
    });
    expect(screen.queryByTestId('care-hazard-refusal')).toBeNull();
  });

  it('a hazard whose guard is gone from the code is said to be missing its guard, by name', async () => {
    const h = clone(captured.hazards);
    const g = h.hazards.find((x: { guarded: boolean }) => x.guarded);
    g.guarded = false;
    g.guard_present = false;
    serve({ hazards: ok(h) });
    mount();
    const rows = await screen.findAllByTestId('care-hazard');
    const row = rows.find(r => r.textContent?.startsWith(g.id));
    expect(row?.textContent).toContain(`GUARD MISSING (${g.guard}): ${g.how}`);
  });

  it('a refused read of the hazard log is said in its place, never as a page with no log', async () => {
    serve({ hazards: refused('the hazard log could not be resolved') });
    mount();
    const said = await screen.findByTestId('care-hazard-refusal');
    expect(within(said).getByRole('alert').textContent).toBe(
      'The open hazard log could not be read: Failed (HTTP 503): the hazard log could not be resolved');
    expect(screen.queryByTestId('care-hazard-log')).toBeNull();
    expect(await screen.findByTestId('care-sources')).toBeTruthy();
  });

  it('the risk tool names each runnable instrument as the server names it, and offers no withheld or retired one', async () => {
    serve();
    mount();
    await screen.findAllByTestId('care-source-tool');
    fireEvent.click(screen.getByRole('button', { name: 'Risk Assess' }));
    const select = await screen.findByLabelText(/^Tool \(news2 computes a score/) as HTMLSelectElement;
    const labels = Array.from(select.options).map(o => o.textContent);
    expect(labels).toEqual(runnable.map(t => t.name));
    for (const t of tools.filter(x => x.type === 'withheld' || x.type === 'retired')) expect(labels).not.toContain(t.name);
  });

  it('a NEWS2 assessment shows the computed score first, its band and response, then the components', async () => {
    serve();
    const post = vi.spyOn(axios, 'post').mockResolvedValue({ data: captured.news2 } as never);
    mount();
    await assess(FULL);
    expect(post.mock.calls[0][0]).toBe('/api/v1/care/risk-assess');
    expect((post.mock.calls[0][1] as { patient_data: Record<string, string> }).patient_data).toEqual(OBSERVED_FULL);
    const score = await screen.findByTestId('care-score');
    const s = captured.news2.score;
    expect(score.textContent).toContain(String(s.total));
    expect(score.textContent).toContain(s.response);
    expect(score.textContent).toContain(`${s.table} · ${s.basis}`);
    expect(within(score).queryByTestId('care-keys-not-read')).toBeNull();
    expect(score.textContent).not.toContain('Incomplete');
  });

  it('a partial NEWS2 says what is missing, that the total is a lower bound, and which keys it did not read', async () => {
    serve();
    vi.spyOn(axios, 'post').mockResolvedValue({ data: captured.news2_partial } as never);
    mount();
    await assess('resp_rate: 22\nskin_colour: pale');
    const score = await screen.findByTestId('care-score');
    const s = captured.news2_partial.score;
    expect(score.textContent).toContain(`Incomplete — missing: ${s.missing.join(' · ')}. The total is a lower bound`);
    expect(within(score).getByTestId('care-keys-not-read').textContent).toContain(
      `Not read: ${s.keys_not_read.join(' · ')} — these are not part of this instrument, so they did not affect the result.`);
  });
});
