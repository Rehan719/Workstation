// W1018 (FU-399 part 46) — the domains hub, rendered against the tool registry and the serving status.
//
// The hub shows the six domains, each with the count and the titles of its tools from the one registry
// (lib/toolRegistry.ts), opens a domain when its card is chosen, and says what this machine can serve, from
// GET /api/v1/native-ai/status (DomainsHub.fixture.json, captured by w1018_capture.py on a fresh store with no
// model installed). A status that cannot be read is said as not known. Each case loads the page anew.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DomainsHub.fixture.json';
import { TOOL_REGISTRY, TOOL_TOTAL } from '../../lib/toolRegistry';
import { servingSentence } from '../../components/ServingNow';

const STATUS = '/api/v1/native-ai/status';

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}</p>;
}

async function mount(reply: { status: number; body: unknown }) {
  vi.resetModules();                                     // the status is read once per page load
  vi.stubGlobal('fetch', vi.fn(async (url: string) => (url === STATUS
    ? { ok: reply.status < 400, status: reply.status, json: async () => reply.body }
    : { ok: false, status: 404, json: async () => ({ detail: `not served in this test: ${url}` }) })));
  const { DomainsHub } = await import('./DomainsHub');
  render(<MemoryRouter initialEntries={['/domains']}><DomainsHub /><Where /></MemoryRouter>);
}

describe('DomainsHub, rendered against the registry and the serving status', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows each domain with the count and the titles of its tools, and opens it when chosen', async () => {
    await mount({ status: 200, body: captured.status });
    expect(screen.getByText(new RegExp(`${TOOL_TOTAL} tools across ${TOOL_REGISTRY.length} domains`))).toBeTruthy();
    //  the cards' counts, in the order the cards stand, are the registry's
    expect(screen.getAllByText(/^\d+ tools$/, { selector: 'span' }).map(s => s.textContent))
      .toEqual(TOOL_REGISTRY.map(d => `${d.tools.length} tools`));
    for (const d of TOOL_REGISTRY) expect(screen.getByText(d.tools.map(t => t.title).join(' · ') + '.')).toBeTruthy();
    const law = TOOL_REGISTRY.find(d => d.route === '/law')!;
    fireEvent.click(screen.getByText(law.tools.map(t => t.title).join(' · ') + '.'));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /law'));
  });

  it('says what serves as the server says it', async () => {
    await mount({ status: 200, body: captured.status });
    await waitFor(() => expect(screen.getByTestId('serving-now').textContent).toBe(servingSentence(captured.status)));
  });

  it('a status that cannot be read is said as not known, never as a model serving', async () => {
    await mount({ status: 503, body: { detail: 'the model register could not be read' } });
    await waitFor(() => expect(screen.getByTestId('serving-now').textContent).toBe(
      'What is serving on this deployment could not be read just now, so nothing is claimed about it.'));
  });
});
