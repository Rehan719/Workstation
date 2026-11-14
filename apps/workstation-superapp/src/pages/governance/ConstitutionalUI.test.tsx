// W985 (FU-399 part 17) — the Constitution page, rendered against its routes' own answers.
//
// The page says what governs the platform: the articles and what each records, whether the ledger's hash chain
// verifies, and the constitutional engine's live status. This mounts the real page against the answers its four routes
// gave on a fresh store (ConstitutionalUI.fixture.json, captured by w985_capture.py), and has the server refuse each
// read. An unread constitution must never be shown as an empty one.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ConstitutionalUI.fixture.json';
import { ConstitutionalUI } from './ConstitutionalUI';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    '/api/v1/gaas/ueg/verify': ok(captured.verify),
    '/api/v154/constitution/articles': ok(captured.articles),
    '/api/v1/gaas/status': ok(captured.status),
    '/api/v1/gaas/ueg/events?limit=40': ok(captured.events),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

function mount() {
  return render(
    <MemoryRouter>
      <ConstitutionalUI />
    </MemoryRouter>,
  );
}

const failures = async () => (await screen.findAllByTestId('read-failure')).map(p => p.textContent);

describe('ConstitutionalUI, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the articles are the route\'s own: their count, and each one by its number', async () => {
    serve();
    mount();
    const arts = captured.articles.articles;
    expect(await screen.findByText(`${arts.length} articles ·`, { exact: false })).toBeTruthy();
    for (const a of [arts[0], arts[arts.length - 1]]) {
      expect(screen.getByText(`Article ${a.id}`)).toBeTruthy();
      expect(screen.getAllByText(a.title, { exact: false }).length).toBeGreaterThan(0);
    }
    expect(screen.queryByTestId('articles-unread')).toBeNull();
  });

  it('the ledger\'s verdict is the route\'s', async () => {
    serve();
    mount();
    const v = captured.verify;
    expect(v.valid && v.anchor_checked).toBe(true);
    await waitFor(() => expect(screen.getByTestId('ledger-integrity-verdict').textContent).toBe('VERIFIED'));
  });

  it('an unread constitution is said, never shown as an empty one', async () => {
    serve({ '/api/v154/constitution/articles': refused(503, 'the canon could not be read') });
    mount();
    await waitFor(() => expect(screen.getByTestId('articles-unread').textContent).toContain(
      'The constitution\'s articles could not be read, so none is shown. This is not an empty constitution.'));
    expect(await failures()).toContain(
      'Could not read the constitution\'s articles — Failed (HTTP 503): the canon could not be read');
    expect(screen.queryByText('articles ·', { exact: false })).toBeNull();
  });

  it('a failed integrity check is said with the server\'s reason, and claims no verdict', async () => {
    serve({ '/api/v1/gaas/ueg/verify': refused(503, 'the ledger could not be opened') });
    mount();
    expect(await failures()).toContain(
      'Could not read the ledger\'s integrity check — Failed (HTTP 503): the ledger could not be opened');
    expect(screen.getByTestId('ledger-integrity-verdict').textContent).toBe('—');
  });

  it('the engine\'s status is the route\'s, and a refusal of it says the server\'s reason', async () => {
    serve();
    const a = mount();
    const s = captured.status;
    await waitFor(() => expect(screen.getByTestId('gaas-breaker-badge').textContent?.trim()).toBe(
      s.circuit_breaker.tripped ? 'BREAKER OPEN' : `${s.circuit_breaker_node ?? 'node'} BREAKER CLOSED`));
    a.unmount();

    serve({ '/api/v1/gaas/status': refused(503, 'the engine is restarting') });
    mount();
    expect(await failures()).toContain(
      'Could not read the constitutional engine\'s status — Failed (HTTP 503): the engine is restarting');
    expect(screen.getByTestId('gaas-breaker-badge').textContent?.trim()).toBe('UNAVAILABLE');
  });
});
