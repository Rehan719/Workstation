// W991 (FU-399 part 23) — the Compliance page, rendered against the compliance routes' own answers.
//
// The page lists the frameworks the federated screen covers, each with what it checks, and runs the screen on a
// subject: an overall verdict, what assessed it and what did not, and each framework's verdict with its reason. This
// mounts the real page against the answers its two routes gave on a fresh store (ComplianceChecker.fixture.json,
// captured by w991_capture.py: the page's own placeholder example), and has the server refuse each. A refusal says the
// server's reason, an unread list of frameworks is not an empty card, and every status the screen gives has its tone.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ComplianceChecker.fixture.json';
import { ComplianceChecker } from './ComplianceChecker';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const FRAMEWORKS = '/api/v1/compliance/frameworks';
const CHECK = '/api/v1/compliance/check';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = { [FRAMEWORKS]: ok(captured.frameworks), [CHECK]: ok(captured.check) };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

async function runTheCheck() {
  fireEvent.change(screen.getByPlaceholderText(/^Describe a product, intent, or content to check/),
    { target: { value: captured.check.subject } });
  fireEvent.click(screen.getByRole('button', { name: /Run Compliance Check/ }));
}

describe('ComplianceChecker, rendered against the compliance routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the frameworks and a check are the routes\' own, and every status has its tone', async () => {
    serve();
    render(<ComplianceChecker />);
    for (const f of captured.frameworks.frameworks) expect(await screen.findByText(f.name)).toBeTruthy();
    await runTheCheck();
    expect((await screen.findByTestId('compliance-coverage-line')).textContent).toContain(
      'NOTHING here assessed this subject.');
    expect(captured.check.assessed_by).toEqual([]);
    for (const v of captured.check.verdicts) {
      const reason = screen.getByText(v.reason);
      const icon = reason.closest('div.flex')?.querySelector('svg');
      expect(icon?.getAttribute('class') ?? '').not.toContain('undefined');
    }
    expect(captured.check.verdicts.some(v => v.status === 'not_assessed')).toBe(true);
  });

  it('a refused check says the server\'s reason', async () => {
    serve({ [CHECK]: refused(503, 'the word lists could not be loaded') });
    render(<ComplianceChecker />);
    await screen.findByText(captured.frameworks.frameworks[0].name);
    await runTheCheck();
    expect((await screen.findByTestId('compliance-error')).textContent).toBe(
      ' The check was not run: Failed (HTTP 503): the word lists could not be loaded');
  });

  it('a check the backend never answered is said as that', async () => {
    serve();
    render(<ComplianceChecker />);
    await screen.findByText(captured.frameworks.frameworks[0].name);
    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('Failed to fetch'); }));
    await runTheCheck();
    expect((await screen.findByTestId('compliance-error')).textContent).toBe(
      ' The check was not run: Failed — backend unreachable.');
  });

  it('an unread list of frameworks is not an empty card', async () => {
    serve({ [FRAMEWORKS]: refused(502, 'the framework registry did not answer') });
    render(<ComplianceChecker />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure').map(e => e.textContent)).toContain(
      'Could not read the frameworks — Failed (HTTP 502): the framework registry did not answer'));
    expect(screen.getByTestId('frameworks-unread').textContent?.trim()).toBe(
      'The frameworks could not be read, so this is not a list of none.');
  });
});
