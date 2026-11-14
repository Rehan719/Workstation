// W1004 (FU-399 part 34) — the Science hub, rendered against the science routes' own answers.
//
// The hub offers its research tools (synthesis, hypotheses, experiment design, literature), filling their methodology
// selects from the methodologies the API lists, each by its name. This mounts the real page against the answers its
// reads gave on a fresh store (ScienceHub.fixture.json, captured by w1004_capture.py), and has the server refuse the
// list and answer it empty. A refusal says the server's reason, and an empty list is said as empty, not as unread.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './ScienceHub.fixture.json';
import { ScienceHub } from './ScienceHub';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const METHODS = '/api/v1/science/methodologies';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = { [METHODS]: ok(captured.methodologies), '/api/v1/native-ai/status': ok(captured.serving) };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <AdaptiveUIProvider>
        <ScienceHub />
      </AdaptiveUIProvider>
    </MemoryRouter>,
  );
}

const offered = () => Array.from((screen.getByLabelText('Methodology') as HTMLSelectElement).options)
  .map(o => [o.value, o.textContent]);

describe('ScienceHub, rendered against the science routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the methodologies offered are the server\'s, each by its name', async () => {
    serve();
    mount();
    const listed = captured.methodologies.methodologies;
    await waitFor(() => expect(offered()).toEqual(listed.map(m => [m.id, m.name])));
    expect(screen.queryByTestId('science-methods-note')).toBeNull();
  });

  it('a refused read of the methodologies says the server\'s reason', async () => {
    serve({ [METHODS]: refused(503, 'the methodology register is locked') });
    mount();
    expect((await screen.findByTestId('science-methods-note')).textContent).toBe(
      'The methodology list could not be read (Failed (HTTP 503): the methodology register is locked), so only the '
      + 'methodologies typed on this page are offered.');
  });

  it('an empty list of methodologies is said as empty, not as unread', async () => {
    serve({ [METHODS]: ok({ ...captured.methodologies, methodologies: [] }) });
    mount();
    expect((await screen.findByTestId('science-methods-note')).textContent).toBe(
      'The server lists no methodologies, so only the methodologies typed on this page are offered.');
  });
});
