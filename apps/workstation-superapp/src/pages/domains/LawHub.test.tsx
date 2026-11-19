// W996 (FU-399 part 28) — the Law hub, rendered against the Law routes' own answers.
//
// The hub says what this machine does in Law before any form: the tools that call no model come first, then each
// form's sentence for what it returns with no model, then the template list with the one it holds for a qualified
// read. This mounts the real page against the answers its reads gave on a fresh store (LawHub.fixture.json, captured
// by w996_capture.py), and has the server refuse each read. A refusal says the server's reason, and a count on the
// page is the server's.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './LawHub.fixture.json';
import { LawHub } from './LawHub';

type Reply = { status: number; body: unknown; notJson?: boolean };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const TEMPLATES = '/api/v1/law/templates';
const TOOLS = '/api/v1/law/tools';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [TEMPLATES]: ok(captured.templates), [TOOLS]: ok(captured.tools),
    '/api/v1/native-ai/status': ok(captured.serving), '/api/v1/law/help': ok(captured.help),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return {
      ok: r.status < 400, status: r.status, statusText: '',
      json: async () => { if (r.notJson) throw new SyntaxError('Unexpected token < in JSON at position 0'); return r.body; },
    };
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <AdaptiveUIProvider>
        <LawHub />
      </AdaptiveUIProvider>
    </MemoryRouter>,
  );
}

describe('LawHub, rendered against the Law routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('what runs here is the server\'s, and the count of forms that need a model is its list\'s', async () => {
    serve();
    mount();
    const noModel = captured.tools.needs_no_model;
    expect(await screen.findAllByTestId('law-no-model-tool')).toHaveLength(noModel.length);
    const n = captured.tools.needs_a_model.length;
    expect(screen.getByTestId('law-forms-need-a-model').textContent).toMatch(
      new RegExp(`^The ${n === 1 ? 'one form' : `${n} forms`} further down need${n === 1 ? 's' : ''} a model\\.`));
  });

  it('a list with a different number of forms is counted as the server lists them', async () => {
    const one = { ...captured.tools, needs_a_model: captured.tools.needs_a_model.slice(0, 1) };
    serve({ [TOOLS]: ok(one) });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-forms-need-a-model').textContent).toMatch(/^The one form further down needs a model\./));
  });

  it('a refused read of the tools says the server\'s reason', async () => {
    serve({ [TOOLS]: refused(503, 'the tools register is being rebuilt') });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-tools-note').textContent).toBe(
      'What each Law tool does could not be read (Failed (HTTP 503): the tools register is being rebuilt), so nothing is said about it here. Each answer still says what composed it.'));
  });

  it('a refused read of the templates says the server\'s reason on the draft tab', async () => {
    serve({ [TEMPLATES]: refused(502, 'the template store did not answer') });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    await waitFor(() => expect(screen.getByTestId('law-templates-note').textContent).toMatch(
      /^The template list could not be read \(Failed \(HTTP 502\): the template store did not answer\), so the templates typed/));
  });

  it('an answer that is not JSON is said by its status, not by the parser', async () => {
    serve({ [TOOLS]: { status: 502, body: null, notJson: true } });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-tools-note').textContent)
      .toMatch(/^What each Law tool does could not be read \(Failed \(HTTP 502\): /));
    expect(screen.getByTestId('law-tools-note').textContent).not.toContain('Unexpected token');   // once it has settled
  });

  it('the templates held for a qualified read are said on the draft tab', async () => {
    serve();
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    const held = captured.templates.held;
    await waitFor(() => expect(screen.getByTestId('law-templates-held').textContent).toContain(held.reason));
  });
});
