// W976 (FU-399 part 10) — the Care page, rendered against the Care routes' own answers.
//
// What a person reads on the Care page is about care: where each tool's standard comes from, which hazards of the tools
// are guarded and which are not, and a risk score computed from the published chart before any narrative. Six guards
// read the page's source. This mounts the real page against the answers the Care routes gave on a fresh store
// (CareHub.fixture.json, captured by w976_capture.py from made-up observations), reads each claim in the DOM, and has
// the server refuse the two reads the page makes itself.
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './CareHub.fixture.json';
import { CareHub } from './CareHub';
import { toolsFor } from '../../lib/toolRegistry';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (detail: string): Reply => ({ status: 503, body: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: { tools?: Reply; hazards?: Reply; review_handover?: Reply; review_risk?: Reply; review_care_plan?: Reply;
                    review_safeguarding?: Reply } = {}) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const reply = ({ status, body }: Reply) => ({ ok: status < 400, status, statusText: '', json: async () => body });
    if (url === '/api/v1/care/tools') return reply(a.tools ?? ok(captured.tools));
    if (url === '/api/v1/care/hazards') return reply(a.hazards ?? ok(captured.hazards));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/handover')) return reply(a.review_handover ?? ok(captured.review_handover));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/risk-assess')) return reply(a.review_risk ?? ok(captured.review_risk));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/care-plan')) return reply(a.review_care_plan ?? ok(captured.review_care_plan));
    if (url === '/api/v1/review-options?endpoint=' + encodeURIComponent('/api/v1/care/safeguarding')) return reply(a.review_safeguarding ?? ok(captured.review_safeguarding));
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

  // W1098 (FU-1275) - the chart's owner allows its reuse provided the stated acknowledgement is given; the score is
  // where its points, band and response wording are read, so the acknowledgement is said there, as the route gives it
  it('a NEWS2 score gives its owner\'s acknowledgement, whole, under the score', async () => {
    serve();
    vi.spyOn(axios, 'post').mockResolvedValue({ data: captured.news2 } as never);
    mount();
    await assess(FULL);
    const score = await screen.findByTestId('care-score');
    expect(captured.news2.score.acknowledgement).toMatch(/^Reproduced from: Royal College of Physicians\./);
    expect(within(score).getByTestId('care-score-acknowledgement').textContent).toBe(captured.news2.score.acknowledgement);
  });

  it('a partial NEWS2 gives the acknowledgement too: its points are still the chart\'s', async () => {
    serve();
    vi.spyOn(axios, 'post').mockResolvedValue({ data: captured.news2_partial } as never);
    mount();
    await assess('resp_rate: 22\nskin_colour: pale');
    const score = await screen.findByTestId('care-score');
    expect(within(score).getByTestId('care-score-acknowledgement').textContent).toBe(captured.news2_partial.score.acknowledgement);
  });

  // W1102 (FU-399 part 91) - the tier of review where a person reads it: in the options before the form, and in the
  // line under the answer, each in the route's own sentence, with an uncalibrated agent's review labelled (W1101)
  it('an uncalibrated agent\'s review of the handover is labelled before the form and under the answer', async () => {
    serve({ review_handover: ok(captured.review_handover_uncalibrated) });
    const post = vi.spyOn(axios, 'post').mockResolvedValue({ data: captured.handover_uncalibrated } as never);
    mount();
    const label = "an agent's review of this tool exists and does not raise its tier: w1102-made-up-reviewer has not been calibrated";
    const options = captured.review_handover_uncalibrated.review;
    const tier = await screen.findByTestId('review-option-tier');
    expect(tier.textContent).toBe(`Review reached: ${options.label} — ${options.basis}.`);
    expect(options.basis).toContain(label);
    fireEvent.change(screen.getByLabelText('Patient summary'), { target: { value: 'w-care 84F' } });
    fireEvent.change(screen.getByLabelText('Current situation'), { target: { value: 'fell at 0300' } });
    fireEvent.click(screen.getByRole('button', { name: /Compose handover/ }));
    const line = await screen.findByTestId('domain-review-tier');
    const review = captured.handover_uncalibrated.ai_provenance.review;
    expect(line.textContent).toBe(`Review: ${review.label} — ${review.basis}.`);
    expect(review.basis).toContain(label);
    expect(post.mock.calls[0][0]).toBe('/api/v1/care/handover');
  });

  // W1183 (FU-1054 part 5) - the Care reviewer agent's calibration, before every Care form, in the server's own
  // statement: UNCALIBRATED with no rates while it has no run of its own, and its two rates once a run exists
  it('the handover form says the reviewer agent is uncalibrated, with no rates, before anything is typed', async () => {
    serve();
    mount();
    const r = captured.review_handover.reviewer;
    await screen.findByTestId('review-option-reviewer');
    await waitFor(() => expect(screen.getByTestId('review-option-reviewer').textContent).toBe(
      `Reviewer agent (${r.agent}): ${r.label} — ${r.basis}.`));
    expect(r.label).toBe('Uncalibrated');
    expect(r.rates).toBeNull();
    expect(screen.queryByTestId('review-option-reviewer-rates')).toBeNull();
  });

  it('once the reviewer has a run of its own, the risk form gives its two rates with their counts', async () => {
    serve({ review_risk: ok(captured.review_risk_made_up_run) });
    mount();
    await screen.findAllByTestId('care-source-tool');
    fireEvent.click(screen.getByRole('button', { name: 'Risk Assess' }));
    const r = captured.review_risk_made_up_run.reviewer;
    await waitFor(() => expect(screen.getByTestId('review-option-reviewer').textContent).toBe(
      `Reviewer agent (${r.agent}): ${r.label} — ${r.basis}.`));
    await waitFor(() => expect(screen.getByTestId('review-option-reviewer-rates').textContent).toBe(`${r.rates.basis}.`));
    expect(r.label).toBe('Uncalibrated');
  });

  // W1185 (FU-1823, P5.15) - every Care tool's tier of review in one place: the four together, each line its tool's
  // answer from the options route in the server's words, and a failed read said on its own tool's line
  const TIERS = [['clinical', 'review_handover'], ['care-plan', 'review_care_plan'], ['risk', 'review_risk'],
                 ['safeguarding', 'review_safeguarding']] as const;
  const T = toolsFor('/care');

  it('the page states the tier each of the four Care tools has reached, together, in the server\'s words', async () => {
    serve();
    mount();
    const card = await screen.findByTestId('care-tiers');
    await waitFor(() => expect(within(card).getAllByTestId('care-tier-review')).toHaveLength(TIERS.length));
    const lines = within(card).getAllByTestId('care-tier');
    expect(lines).toHaveLength(TIERS.length);
    TIERS.forEach(([tab, key], i) => {
      const a = captured[key];
      expect(within(lines[i]).getByTestId('care-tier-tool').textContent).toBe(`${T[tab].title} · ${a.tool}`);
      expect(within(lines[i]).getByTestId('care-tier-review').textContent).toBe(`Review reached: ${a.review.label} — ${a.review.basis}.`);
      expect(within(lines[i]).getByTestId('care-tier-reviewer').textContent).toBe(
        `Reviewer agent (${a.reviewer.agent}): ${a.reviewer.label} — ${a.reviewer.basis}.`);
      expect(within(lines[i]).queryByTestId('care-tier-reviewer-rates')).toBeNull();
      expect(within(lines[i]).queryByTestId('care-tier-refusal')).toBeNull();
    });
    expect(new Set(TIERS.map(([, key]) => captured[key].tool)).size).toBe(TIERS.length);
    // ...the card says its heading and the four lines, and nothing else
    expect(card.textContent).toBe('The review each tool has reached' + TIERS.map(([tab, key]) => {
      const a = captured[key];
      return `${T[tab].title} · ${a.tool}Review reached: ${a.review.label} — ${a.review.basis}.`
        + `Reviewer agent (${a.reviewer.agent}): ${a.reviewer.label} — ${a.reviewer.basis}.`;
    }).join(''));
    // ...and it stays, its four lines whole, whichever tool's tab is open
    for (const name of ['Care Plan', 'Risk Assess', 'Safeguarding']) {
      fireEvent.click(screen.getByRole('button', { name }));
      expect(within(screen.getByTestId('care-tiers')).getAllByTestId('care-tier-review')).toHaveLength(TIERS.length);
    }
  });

  it('once the reviewer has a run of its own, its two rates with their counts are on that tool\'s line', async () => {
    serve({ review_risk: ok(captured.review_risk_made_up_run) });
    mount();
    const card = await screen.findByTestId('care-tiers');
    const r = captured.review_risk_made_up_run.reviewer;
    await waitFor(() => expect(within(card).getByTestId('care-tier-reviewer-rates').textContent).toBe(`${r.rates.basis}.`));
    const risk = within(card).getAllByTestId('care-tier')[TIERS.findIndex(([tab]) => tab === 'risk')];
    expect(within(risk).getByTestId('care-tier-reviewer').textContent).toBe(`Reviewer agent (${r.agent}): ${r.label} — ${r.basis}.`);
    expect(within(risk).getByTestId('care-tier-reviewer-rates').textContent).toBe(`${r.rates.basis}.`);
    expect(r.label).toBe('Uncalibrated');
  });

  for (const [tab, key] of TIERS) {
    it(`a refused read of the ${tab} tool's tier is said on its own line, and no tier is shown there`, async () => {
      const over: NonNullable<Parameters<typeof serve>[0]> = {};
      over[key] = refused(`w1185 the options of ${tab} could not be read`);
      serve(over);
      mount();
      const card = await screen.findByTestId('care-tiers');
      await waitFor(() => {
        expect(within(card).getAllByTestId('care-tier-refusal')).toHaveLength(1);
        expect(within(card).getAllByTestId('care-tier-review')).toHaveLength(TIERS.length - 1);
      });
      const lines = within(card).getAllByTestId('care-tier');
      TIERS.forEach(([other, k], i) => {
        if (other === tab) {
          expect(within(lines[i]).getByTestId('care-tier-refusal').textContent).toBe(
            `The tier of review this tool has reached could not be read, so none is shown: Failed (HTTP 503): w1185 the options of ${tab} could not be read`);
          expect(within(lines[i]).getByTestId('care-tier-tool').textContent).toBe(T[tab].title);
          expect(within(lines[i]).queryByTestId('care-tier-review')).toBeNull();
          expect(within(lines[i]).queryByTestId('care-tier-reviewer')).toBeNull();
        } else {
          expect(within(lines[i]).getByTestId('care-tier-review').textContent).toBe(
            `Review reached: ${captured[k].review.label} — ${captured[k].review.basis}.`);
        }
      });
    });
  }

  it('an answer that carries no tier is said on its line as one, and never shown as a tier', async () => {
    serve({ review_care_plan: ok({ ...captured.review_care_plan, review: null }) });
    mount();
    const card = await screen.findByTestId('care-tiers');
    await waitFor(() => expect(within(card).getByTestId('care-tier-refusal').textContent).toBe(
      'The tier of review this tool has reached could not be read, so none is shown: the answer carried no tier of review'));
    const plan = within(card).getAllByTestId('care-tier')[TIERS.findIndex(([tab]) => tab === 'care-plan')];
    expect(within(plan).queryByTestId('care-tier-review')).toBeNull();
    expect(within(plan).queryByTestId('care-tier-reviewer')).toBeNull();
  });

  // W1185 (FU-1823) - the answer to a concern about a child or young person says the safeguarding tool's tier under
  // it, as every other Care answer says its tool's; the emergency line and the children's route are as they were, and
  // nothing composed it
  it('a concern about a child gets the children\'s route, with the safeguarding tool\'s tier under it', async () => {
    serve();
    const got = captured.safeguarding_child;
    const post = vi.spyOn(axios, 'post').mockResolvedValue({ data: got } as never);
    mount();
    await screen.findAllByTestId('care-source-tool');
    fireEvent.click(screen.getByRole('button', { name: 'Safeguarding' }));
    fireEvent.change(await screen.findByLabelText('Who is the concern about?'), { target: { value: 'a child or young person' } });
    fireEvent.change(screen.getByLabelText('Safeguarding concern'), { target: { value: 'w1185 a worker is worried about bruising on a child' } });
    fireEvent.click(screen.getByRole('button', { name: /Set out the process/ }));
    const review = got.ai_provenance.review;
    await waitFor(() => expect(screen.getByTestId('domain-review-tier').textContent).toBe(`Review: ${review.label} — ${review.basis}.`));
    expect(review).toEqual(captured.review_safeguarding.review);
    expect(post.mock.calls[0][0]).toBe('/api/v1/care/safeguarding');
    expect((post.mock.calls[0][1] as { concern_about: string }).concern_about).toBe('a child or young person');
    expect(screen.getByText((_, el) => el?.tagName === 'PRE' && el.textContent === got.guidance)).toBeTruthy();
    expect(screen.getByText(got.disclaimer)).toBeTruthy();
    // the gap: with served_by null the badge says 'provenance not recorded', not 'no call served this'; W1186 gives it "none"
    expect(screen.getByText('provenance not recorded')).toBeTruthy();
    expect(screen.queryByTestId('domain-served-identity')).toBeNull();
    expect(screen.queryByTestId('domain-floor-note')).toBeNull();
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
