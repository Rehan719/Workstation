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

import captured from './GenesisJourney.fixture.json';
import { GenesisJourney } from './GenesisJourney';

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
