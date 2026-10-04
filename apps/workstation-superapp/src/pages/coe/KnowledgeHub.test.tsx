// W579 (FU-352) — THE FIRST RENDERED PAGE GUARD IN THIS REPOSITORY.
//
// Every page assertion in the Python suite is a text scan: 81 tests read a .tsx file and match
// substrings, and 295 `data-testid` attributes existed for a renderer that did not exist. A scan can
// show that a line of source is present; it cannot show that a person looking at the page sees
// anything. P2.18 clause (b) is that an instrument proves what it claims.
//
// The subject is FU-323's crash path, chosen because it is the row where the difference matters most:
// `intelligence_insights` used to return an empty list when its computation raised, and an empty list
// renders as "Create projects to generate portfolio insights" — a failure shown to the founder as the
// statement that they have no projects. W576 moved the failure INSIDE `insights` so the empty branch
// cannot be reached by a crash at all. This mounts the real component against the real crash shape and
// reads the DOM.
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { KnowledgeHub } from './KnowledgeHub';

// the exact shape agentic_core/api/products.py returns from its except branch (W576), including the
// first insight that carries the failure and says what was NOT measured
const CRASH_PAYLOAD = {
  insights: [
    {
      id: 'i-err',
      type: 'Unavailable',
      title: 'Portfolio insights could not be computed',
      detail:
        'The computation failed, so this is NOT a statement that you have no projects: nothing was ' +
        'counted. Reason: boom',
      score: 0,
      score_basis: 'no score was assigned — nothing was measured',
    },
  ],
  computed_at: 1,
  total_projects: null,
  error: 'RuntimeError: boom',
  score_meaning: 'no insight was produced, so no score was assigned and there is nothing here for a score to mean',
};

const HEALTHY_PAYLOAD = {
  insights: [
    { id: 'i-1', type: 'Enterprise', title: 'Portfolio concentration', detail: 'Three of four projects sit in one domain.', score: 0.82, score_basis: 'salience weight: a fixed constant for this insight type, not a measurement' },
  ],
  computed_at: 2,
  total_projects: 4,
  error: null,
  score_meaning: "every insight's `score` is a SALIENCE WEIGHT used to order the list; three of the four are fixed constants per insight type and the fourth scales with the project count. None of them measures the subject the insight names.",
};

function mount() {
  // retry MUST be off: react-query would otherwise swallow the first render and this test would time
  // out rather than fail, which reads as a broken runner instead of a broken page
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter>
        <KnowledgeHub />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe('KnowledgeHub, rendered', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders the failure, and never the you-have-no-projects sentence (FU-323)', async () => {
    vi.spyOn(axios, 'get').mockResolvedValue({ data: CRASH_PAYLOAD } as never);
    mount();

    // THE FAILURE REACHES THE DOM AS A CARD, NOT AS THE EMPTY-STATE CHIP — and finding that out is
    // what this runner is for. W576 moved the failure INSIDE `insights`, so the list is non-empty and
    // the `insights-error` branch (which only renders when there are NO insights) is unreachable on a
    // crash; the page's own comment says so. The first draft of this test asserted that chip and failed,
    // which then showed that the list rendered an insight's TITLE and never its DETAIL — so the clause
    // that refuses the wrong reading reached nobody. A text scan would have found the string present in
    // the source and concluded the opposite.
    const detail = await screen.findByTestId('insight-detail');
    expect(detail.textContent).toMatch(/NOT a statement that you have no projects/i);
    expect(detail.textContent).toMatch(/nothing was counted/i);
    expect(screen.queryByTestId('insights-error')).toBeNull();

    // the empty-state sentence must be absent: it is what a crash used to render as
    expect(screen.queryByText(/Create projects to generate portfolio insights/i)).toBeNull();

    // W578 (FU-394) — null is NOT zero. The crash branch counted nothing, so the provenance chip must
    // say so rather than rendering "Derived from 0 projects", which reads as "you have no projects".
    expect(await screen.findByTestId('insights-provenance-unknown')).toBeInTheDocument();
    expect(screen.queryByTestId('insights-provenance')).toBeNull();
  });

  it('renders the count and the score meaning on a healthy payload (FU-394)', async () => {
    vi.spyOn(axios, 'get').mockResolvedValue({ data: HEALTHY_PAYLOAD } as never);
    mount();

    const prov = await screen.findByTestId('insights-provenance');
    expect(prov.textContent).toMatch(/Derived from 4 projects/i);
    expect(screen.queryByTestId('insights-provenance-unknown')).toBeNull();
    expect(screen.queryByTestId('insights-error')).toBeNull();

    // the response-level statement about what every score MEANS — the aggregate fact no per-insight
    // basis carries, which is that the ORDER of the list is not a ranking of anything measured
    const meaning = await screen.findByTestId('insights-score-meaning');
    expect(meaning.textContent).toMatch(/SALIENCE WEIGHT/i);
  });
});
