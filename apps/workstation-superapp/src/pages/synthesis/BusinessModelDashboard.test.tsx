// W1019 (FU-399 part 47) — the business model dashboard, rendered against the simulation route's own answers.
//
// The synthesis studio draws a simulation with this dashboard: the simulation the result's content carries, parsed,
// beside the result's own provenance. Until now it was read only as source text. This mounts the real dashboard
// against POST /api/v1/synthesis/generate's answers (BusinessModelDashboard.fixture.json, captured on a fresh store):
// the floor's, which says no simulation came back, and two replies made up for the capture and run through the
// route, one whole and one without its simulation results. Each is drawn as the studio draws it: the content
// parsed, and the result's served_by and is_external handed in beside it.
//
// Rendering found three defects, fixed in this round:
// - the badge read served_by from the simulation, which never carries it, so it said "provenance not recorded"
//   over every simulation, the floor's included;
// - a "Market Size" card read a field the route never asks the model for, so it said "—" every time;
// - a "Download Strategy PDF" button downloaded nothing; it showed a toast promising a later release.
import { render, screen } from '@testing-library/react';
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './BusinessModelDashboard.fixture.json';
import { BusinessModelDashboard } from './BusinessModelDashboard';

type Answer = { content: string; served_by: string | null; is_external: boolean };

// as the studio draws a simulation: the result's content parsed, the result's own provenance beside it
function draw(answer: Answer) {
  return render(
    <BusinessModelDashboard data={JSON.parse(answer.content)} servedBy={answer.served_by} isExternal={answer.is_external} />,
  );
}

// a card's figure: the line under its label
const figure = (label: string) => screen.getByText(label).nextElementSibling?.textContent;

const NONE_CHARTED = 'The model returned no financial projections, so none are charted.';
const CHART = '.recharts-responsive-container';

describe('BusinessModelDashboard, a simulation drawn as the route answered it', () => {
  // jsdom has no layout and so no ResizeObserver, which the chart's container needs to mount. Its bars are not read
  // here (jsdom measures nothing); only whether a chart is offered, or the sentence that none is.
  beforeEach(() => {
    vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the floor: says no simulation came back, shows no figure, and wears the floor badge', () => {
    const { answer, simulation } = captured.floor;
    const { container } = draw(answer);
    expect(screen.getByTestId('model-provenance').textContent).toBe('structured floor — not model analysis');
    expect(screen.getByRole('status').textContent).toBe(simulation.detail);
    expect(figure('ROI Efficiency')).toBe('—');
    expect(figure('Swarm Multiplier')).toBe('—');
    expect(screen.getByText(NONE_CHARTED)).toBeTruthy();
    expect(container.querySelector(CHART)).toBeNull();
    expect(screen.getByTestId('no-market-strategy').textContent).toBe('The model returned no market summary, so none is shown.');
    expect(screen.getByTestId('no-sim-parameters').textContent).toContain(
      'No simulation parameters were returned — the model produced no simulation for this model.');
    // nothing the route never asks for, and nothing offered that does not do what it says
    expect(screen.queryByText('Market Size')).toBeNull();
    expect(screen.queryByRole('button')).toBeNull();
  });

  it('a whole reply: each figure the model gave, under its own label, and the badge names the model', () => {
    const { answer, simulation } = captured.model;
    const { container } = draw(answer);
    expect(screen.getByTestId('model-provenance').textContent).toBe(`in-house · ${answer.served_by}`);
    expect(screen.queryByRole('status')).toBeNull();                 // nothing is missing, so nothing is noted
    expect(figure('ROI Efficiency')).toBe('18%');
    expect(figure('Swarm Multiplier')).toBe('1.5x');
    expect(figure('ESE Adoption')).toBe('4%');
    expect(figure('ARO Efficiency')).toBe('18%');
    expect(figure('BTO Velocity')).toBe('1.5x');
    expect(figure('DRAD Resilience')).toBe('120ms');
    expect(screen.getByText(simulation.market_summary)).toBeTruthy();
    expect(screen.getByText(simulation.roi_analysis)).toBeTruthy();
    expect(screen.queryByText(NONE_CHARTED)).toBeNull();
    expect(container.querySelector(CHART)).not.toBeNull();
    expect(screen.queryByTestId('no-sim-parameters')).toBeNull();
    expect(screen.queryByTestId('no-market-strategy')).toBeNull();
  });

  it('a reply without simulation results: the route\'s note says so, and what the model did give is shown', () => {
    const { answer, simulation } = captured.partial;
    const { container } = draw(answer);
    expect(screen.getByRole('status').textContent).toBe(simulation.sim_results_note);
    expect(figure('ROI Efficiency')).toBe('—');
    expect(figure('Swarm Multiplier')).toBe('—');
    const none = screen.getByTestId('no-sim-parameters').textContent;
    expect(none).toContain('No simulation parameters were returned.');
    expect(none).not.toContain('the model produced no simulation');  // it did; only its results are missing
    expect(screen.queryByText(NONE_CHARTED)).toBeNull();                 // its projections came back
    expect(container.querySelector(CHART)).not.toBeNull();
    expect(screen.getByText(simulation.market_summary)).toBeTruthy();
  });

  it('reads the badge from the result alone: a simulation that names its own server is not believed', () => {
    const floor = captured.floor.answer;
    const claims = { ...JSON.parse(captured.model.answer.content), served_by: 'W1019 made up: a name in the reply', is_external: true };
    const { rerender } = render(
      <BusinessModelDashboard data={claims} servedBy={floor.served_by} isExternal={floor.is_external} />,
    );
    expect(screen.getByTestId('model-provenance').textContent).toBe('structured floor — not model analysis');
    rerender(<BusinessModelDashboard data={claims} />);              // a result that records nothing
    expect(screen.getByTestId('model-provenance').textContent).toBe('provenance not recorded');
  });
});
