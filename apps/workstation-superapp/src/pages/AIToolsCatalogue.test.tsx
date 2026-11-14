// W1018 (FU-399 part 45) — the AI tools catalogue, rendered against the tool registry and the serving status.
//
// The catalogue lists every domain tool from the one registry (lib/toolRegistry.ts), each card a link to its tool on
// its domain's page, and says before any form what this machine can serve, from GET /api/v1/native-ai/status
// (AIToolsCatalogue.fixture.json, captured by w1018_capture.py on a fresh store with no model installed). A status
// that cannot be read is said as not known. The status is read once per page load, so each case loads the page anew.
import { render, screen, within } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './AIToolsCatalogue.fixture.json';
import { TOOL_REGISTRY, TOOL_TOTAL } from '../lib/toolRegistry';
import { servingSentence } from '../components/ServingNow';

const STATUS = '/api/v1/native-ai/status';

async function mount(reply: { status: number; body: unknown }) {
  vi.resetModules();                                     // the status is read once per page load
  vi.stubGlobal('fetch', vi.fn(async (url: string) => (url === STATUS
    ? { ok: reply.status < 400, status: reply.status, json: async () => reply.body }
    : { ok: false, status: 404, json: async () => ({ detail: `not served in this test: ${url}` }) })));
  const { AIToolsCatalogue } = await import('./AIToolsCatalogue');
  render(<MemoryRouter><AIToolsCatalogue /></MemoryRouter>);
}

describe('AIToolsCatalogue, rendered against the registry and the serving status', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('lists every tool the registry holds, each a link to its tool on its domain\'s page', async () => {
    await mount({ status: 200, body: captured.status });
    expect(screen.getByText(new RegExp(`^${TOOL_TOTAL} tools across ${TOOL_REGISTRY.length} domains`))).toBeTruthy();
    for (const d of TOOL_REGISTRY) {
      const section = screen.getByRole('heading', { name: d.name }).closest('section') as HTMLElement;
      expect(within(section).getByText(`${d.tools.length} tools`)).toBeTruthy();
      const links = within(section).getAllByRole('link');
      expect(links.map(a => a.getAttribute('href'))).toEqual(d.tools.map(t => `${d.route}?tab=${t.tab}`));
    }
  });

  it('says what serves as the server says it, before any form', async () => {
    await mount({ status: 200, body: captured.status });
    const said = await screen.findAllByTestId('serving-now');
    expect(said).toHaveLength(TOOL_REGISTRY.length + 1);   // the page's, and one over each domain's tools
    for (const p of said) expect(p.textContent).toBe(servingSentence(captured.status));
    expect(captured.status.is_real_model).toBe(false);
  });

  it('a status that cannot be read is said as not known, never as a model serving', async () => {
    await mount({ status: 503, body: { detail: 'the model register could not be read' } });
    const said = await screen.findAllByTestId('serving-now');
    for (const p of said) {
      expect(p.textContent).toBe('What is serving on this deployment could not be read just now, so nothing is claimed about it.');
    }
  });
});
