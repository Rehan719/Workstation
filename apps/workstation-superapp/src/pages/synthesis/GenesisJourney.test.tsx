// W924 (FU-399 part 6) — a Genesis journey's stage rail and its rank stage, rendered against the API's own answer.
//
// What each stage did is a claim about what a founder SEES (W573): a stage the journey never reached says "not run"
// with the journey's reason; a stage with no verification entry says "not known"; the rank stage says "not ranked"
// when the server found its candidates are not alternatives (W436), shows a vetoed candidate as vetoed (W485), and
// says when the journey stopped at the section 11 screen. This mounts the real page, runs one journey against the
// answer the journey route gave (GenesisJourney.fixture.json, captured on the native floor), and reads the rail and
// the rank stage in the DOM, then the same answer changed the ways the server changes it.
import { fireEvent, render, screen, within, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { PRODUCTS, PRODUCT_LABELS } from '../../lib/taxonomy';
import captured from './GenesisJourney.fixture.json';
import { GenesisJourney } from './GenesisJourney';

// W1242b - with every call floor-served the page says first, in the route's plain words, that no model answered, what
// was saved and how a model is added; folds the fallback's frames, each behind its own toggle; and keeps the technical
// labels in closed disclosures. A model-served answer (no_model null) folds nothing.
// the rail's six tiles, in order, and the verification entry each reads (the rank tile reads its candidates)
const RAIL: (string | null)[] = ['concept', 'research', null, 'design', 'operations', 'commercialisation'];

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function serve(edit?: (j: any) => void) {
  const journey = JSON.parse(JSON.stringify(captured.journey));
  if (edit) edit(journey);
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const reply = (status: number, body: unknown) => ({ ok: status < 400, status, json: async () => body });
    if (url === '/api/v1/genesis/journey' && init?.method === 'POST') return reply(200, journey);
    if (url === '/api/v1/economy/entity-types') return reply(200, captured.entity_types);
    if (url === '/api/v1/genesis/price') return reply(200, captured.price);          // the price panel's own read
    return reply(200, {});
  }));
  return journey;
}

async function runJourney() {
  render(
    <MemoryRouter>
      <GenesisJourney />
    </MemoryRouter>,
  );
  fireEvent.change(screen.getByPlaceholderText(/Describe the problem to solve/), { target: { value: captured.request.problem } });
  fireEvent.click(screen.getByText('Launch Genesis Journey'));
  await screen.findByTestId(`rail-state-${1}`);          // the rail's ids are built per tile, as the page builds them
}

const chip = (i: number) => screen.getByTestId(`rail-state-${i}`).textContent;
const why = (i: number) => screen.getByTestId(`rail-why-${i}`).textContent;

describe('GenesisJourney, the stage rail and the rank stage, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  // W1111 (FU-399 part 100) - what a floor journey produced and what served it, in the journey's own words: the product
  // chosen and how it is recorded, the heading, the two stages' subtitles, the calls and what served them, and the gate
  it('a floor journey says what it produced, what served it, the product it recorded and the gate it passed', async () => {
    const j = serve();
    render(
      <MemoryRouter>
        <GenesisJourney />
      </MemoryRouter>,
    );
    const picker = screen.getByTestId('genesis-product-picker');
    expect(Array.from(picker.querySelectorAll('button')).map(b => b.getAttribute('title'))).toEqual(PRODUCTS.map(p => PRODUCT_LABELS[p]));
    expect(screen.getByTestId('genesis-product-record-only').textContent).toBe(
      'Recorded only: the product is saved with this journey and its entity, but no stage runs differently by product yet.');
    fireEvent.click(within(picker).getByTitle(PRODUCT_LABELS[captured.request.product]));
    fireEvent.change(screen.getByPlaceholderText(/Describe the problem to solve/), { target: { value: captured.request.problem } });
    fireEvent.click(screen.getByText('Launch Genesis Journey'));
    expect([j.status, j.enterprise_established]).toEqual(['complete', false]);
    await waitFor(() => expect(screen.getByTestId('journey-complete-heading').textContent).toBe(
      'Journey Complete — Record Only (no enterprise established)'));
    const post = vi.mocked(fetch).mock.calls.find(([u, i]) => u === '/api/v1/genesis/journey' && i?.method === 'POST');
    const posted = JSON.parse(String(post?.[1]?.body));
    expect([posted.problem, posted.product]).toEqual([captured.request.problem, captured.request.product]);
    expect(screen.getByTestId('journey-product').textContent).toBe(`Product: ${j.product_label} — ${j.product_source}`);
    expect([j.stage_verifications.research.floor_served, j.stage_verifications.operations.floor_served]).toEqual([true, true]);
    expect(screen.getByTestId('genesis-research-subtitle').textContent).toBe(
      'The structured floor served this stage, not a model: what follows is a frame built from your own words under the'
      + ' requested headings. No approach was found, researched or compared.');
    expect(screen.getByTestId('genesis-operations-subtitle').textContent).toBe(
      'The structured floor served this stage, not a model: the headings below name deliverability, compliance and'
      + ' operability, and nothing under them assessed any of the three.'
      + ' The §11 screen below reads the design and commercialisation text — a keyword and vocabulary screen, not a certification.');
    expect(screen.getByTestId('journey-engines-basis').textContent).toBe(j.engines_used_basis);
    const sb = j.ai_provenance.served_by;
    expect(Object.keys(sb)).toEqual(['native']);
    expect(screen.getByTestId('engines-used-basis').textContent).toBe(
      `These are the calls this journey made, not engines that reasoned: all ${sb.native} of its AI calls were served by`
      + ' the deterministic floor, which answers each with a structured frame. gaas.v5 is the intent gate.');
    const g = j.governance;
    expect(g.content_screened).toBe(false);
    expect(screen.getByTestId('journey-intent-gate').textContent).toBe(
      `intent gate: ${g.status} · content not screened · checkpoint ${g.checkpoint}`);
    expect(screen.getByTestId('journey-intent-gate').getAttribute('title')).toBe(g.scope);
  });

  it('a floor journey: each stage says it ran with the journey\'s own reason, and the rank stage says not ranked', async () => {
    const j = serve();
    await runJourney();
    RAIL.forEach((key, n) => {
      if (!key) return;
      const v = j.stage_verifications[key];
      expect(v.ran === false || v.verified === true).toBe(false);          // the floor runs every stage, verifies none
      expect([chip(n + 1), why(n + 1)]).toEqual(['ran', v.basis]);
    });
    const r5 = j.stage_5_model_simulate_rank;
    expect(r5.candidates_are_alternatives).toBe(false);
    expect(chip(3)).toBe('not ranked');
    expect(why(3)).toContain(`${r5.candidates.length} candidate text(s) were produced and they are not alternatives`);
    expect(screen.getByTestId('rank-not-alternatives').textContent).toBe(r5.comparison_note);
    expect(screen.queryByTestId(`rank-candidate-${r5.candidates[0].id}`)).toBeNull();
    expect(screen.getByTestId('rank-selection-basis').textContent)
      .toBe(`${r5.selection_basis} — that one text is carried into Design; nothing was chosen over anything.`);
  });

  it('ranked alternatives: the winner is chipped selected and carried into Design, and a verified stage says so', async () => {
    const j = serve(x => {
      const r5 = x.stage_5_model_simulate_rank;
      r5.candidates_are_alternatives = true;
      r5.candidates.forEach((c: { rank: number; score: number }, i: number) => { c.rank = i + 1; c.score = 0.9 - i / 10; });
      r5.selected = r5.candidates[0].id;
      x.stage_verifications.concept = { ...x.stage_verifications.concept, verified: true, basis: 'the concept met its own checks' };
    });
    await runJourney();
    const r5 = j.stage_5_model_simulate_rank;
    expect([chip(3), why(3)]).toEqual(['ran',
      `${r5.candidates.length} candidate(s) were modelled and ranked. This stage carries no §10 verification entry, so nothing has been verified about it.`]);
    expect([chip(1), why(1)]).toEqual(['verified', 'the concept met its own checks']);
    expect(within(screen.getByTestId(`rank-candidate-${r5.selected}`)).getByTestId('rank-selected')).toBeTruthy();
    expect(screen.queryByTestId('rank-not-alternatives')).toBeNull();
    expect(screen.getByTestId('rank-selection-basis').textContent).toBe(`${r5.selection_basis} — the winner is carried into Design.`);
  });

  it('a journey the section 11 screen stopped: the stages it never reached say not run, and every candidate is vetoed', async () => {
    const stop = 'not reached: the section 11 screen vetoed every candidate, so the journey stopped after ranking';
    const j = serve(x => {
      const r5 = x.stage_5_model_simulate_rank;
      r5.candidates_are_alternatives = true;
      r5.blocked_by_screen = true;
      r5.vetoed = r5.candidates.map((c: { id: string }) => c.id);
      r5.selected = null;
      r5.blocked_reason = 'Every candidate failed the section 11 screen, so no approach was selected.';
      for (const k of ['design', 'operations', 'commercialisation']) x.stage_verifications[k] = { ran: false, basis: stop };
    });
    await runJourney();
    for (const n of [4, 5, 6]) expect([chip(n), why(n)]).toEqual(['not run', stop]);
    expect(screen.getByTestId('rank-blocked').textContent).toContain(j.stage_5_model_simulate_rank.blocked_reason);
    for (const c of j.stage_5_model_simulate_rank.candidates) {
      expect(within(screen.getByTestId(`rank-candidate-${c.id}`)).getByTestId('rank-vetoed')).toBeTruthy();
    }
    expect(screen.getByTestId('rank-selection-basis').textContent)
      .toBe(`${j.stage_5_model_simulate_rank.selection_basis} — nothing is carried into Design: the journey stops here.`);
  });

  it('a journey no model answered says so first, in plain words, and folds what the fallback produced', async () => {
    const j = serve();
    await runJourney();
    const nm = j.no_model;
    expect(Object.keys(j.ai_provenance.served_by)).toEqual(['native']);
    expect(nm.all_calls_floor_served).toBe(j.ai_provenance.served_by.native);
    expect(screen.getByTestId('genesis-no-model-said').textContent).toBe(nm.said);
    expect(nm.said.startsWith('No AI model is connected, so these steps could not write anything.')).toBe(true);
    expect(screen.getByTestId('genesis-no-model-saved').textContent).toBe(nm.saved);
    expect(screen.getByTestId('genesis-no-model-how').textContent).toBe(nm.how);
    // near the top: before the export card, the technical disclosure and every stage
    const notice = screen.getByTestId('genesis-no-model');
    for (const later of [screen.getByText('Export the journey (§4.9) as a deliverable'), screen.getByTestId('genesis-technical-details'),
      screen.getByText('Phase 1 · Conceptualisation')]) {
      expect(notice.compareDocumentPosition(later) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    }
    // folded: phase 1's three sections, research and operations each have a toggle, and no frame is drawn
    const toggles = screen.getAllByTestId('floor-fold-toggle');
    expect(toggles.map(t => t.textContent)).toEqual(Array(5).fill('Show what the fallback produced'));
    expect(screen.queryAllByTestId('floor-fold-text')).toHaveLength(0);
    expect(document.body.textContent).not.toContain(j.phase_1_conceptualisation.cognitive_cascade.trim().slice(0, 80));
    fireEvent.click(toggles[0]);
    expect(screen.getByTestId('floor-fold-text').textContent).toBe(j.phase_1_conceptualisation.cognitive_cascade);
    expect(toggles[0].textContent).toBe('Hide what the fallback produced');
    expect(screen.getAllByTestId('floor-fold-text')).toHaveLength(1);           // each heading opens on its own
    // the technical labels are kept, each in a closed disclosure
    for (const id of ['rail-why-1', 'genesis-technical-details', 'rank-method-details', 'rank-measured-details',
      'engines-used-basis', 'journey-intent-gate', 'journey-engines-basis']) {
      const d = screen.getByTestId(id).closest('details');
      expect(d).not.toBeNull();
      expect(d?.open).toBe(false);
    }
    expect(within(screen.getByTestId('genesis-technical-details')).getByText(/0\/0 verified/)).toBeTruthy();
    expect(screen.getByTestId('journey-intent-gate').textContent).toContain(`checkpoint ${j.governance.checkpoint}`);
  });

  it('a journey a model answered shows no notice and folds nothing', async () => {
    const j = serve(x => { x.no_model = null; x.ai_provenance.served_by = { 'ollama:w1242-local': 14 }; });
    await runJourney();
    expect(screen.queryByTestId('genesis-no-model')).toBeNull();
    expect(screen.queryAllByTestId('floor-fold-toggle')).toHaveLength(0);
    expect(document.body.textContent).toContain(j.phase_1_conceptualisation.concept.trim().slice(0, 80));
  });

  it('a stage the journey recorded no verification for says not known, never ran', async () => {
    serve(x => { delete x.stage_verifications.research; });
    await runJourney();
    expect([chip(2), why(2)]).toEqual(['not known',
      'the journey recorded no verification entry for "research", so whether this stage ran is not known']);
  });

  // W928 - a read the page needs and the server refuses is said where the page starts, with the server's reason
  it('a refused read of the entity types is said, with the server\'s reason', async () => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      const reply = (status: number, body: unknown) => ({ ok: status < 400, status, json: async () => body });
      if (url === '/api/v1/economy/entity-types') return reply(503, { detail: 'the entity type register could not be read' });
      if (url === '/api/v1/genesis/price') return reply(200, captured.price);
      return reply(200, {});
    }));
    render(
      <MemoryRouter>
        <GenesisJourney />
      </MemoryRouter>,
    );
    await waitFor(() => expect(screen.getByTestId('read-failure').textContent).toBe('Could not read the entity types — Failed (HTTP 503): the entity type register could not be read'));
  });
});
