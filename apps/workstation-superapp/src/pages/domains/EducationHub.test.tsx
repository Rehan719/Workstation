// W1004 (FU-399 part 34) — the Education hub, rendered against the education routes' own answers.
//
// The hub offers its forms (lessons, curriculum, assessment, marking), says before each what it does on this machine
// now, and fills the curriculum's framework select from the frameworks the API lists, each by its name. This mounts
// the real page against the answers its reads gave on a fresh store (EducationHub.fixture.json, captured by
// w1004_capture.py), and has the server refuse each read and answer the framework list empty. A refusal says the
// server's reason, and an empty list is said as empty, not as unread.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './EducationHub.fixture.json';
import { EducationHub } from './EducationHub';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const FRAMEWORKS = '/api/v1/education/frameworks';
const TOOLS = '/api/v1/education/tools';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [FRAMEWORKS]: ok(captured.frameworks), [TOOLS]: ok(captured.tools), '/api/v1/native-ai/status': ok(captured.serving),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <AdaptiveUIProvider>
        <EducationHub />
      </AdaptiveUIProvider>
    </MemoryRouter>,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Curriculum' }));
}

const offered = () => Array.from((screen.getByLabelText('Framework') as HTMLSelectElement).options)
  .map(o => [o.value, o.textContent]);

describe('EducationHub, rendered against the education routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the frameworks offered are the server\'s by name, and the form says what it does on this machine now', async () => {
    serve();
    mount();
    await waitFor(() => expect(offered()).toEqual(captured.frameworks.frameworks.map(f => [f.id, f.name])));
    const form = captured.tools.forms.find(f => f.id === 'curriculum');
    await waitFor(() => expect(screen.getByTestId('education-form-says').textContent).toContain(form?.does ?? 'no such form'));
    expect(screen.queryByTestId('education-frameworks-note')).toBeNull();
  });

  it('a refused read of the frameworks says the server\'s reason', async () => {
    serve({ [FRAMEWORKS]: refused(502, 'the framework register did not answer') });
    mount();
    await waitFor(() => expect(screen.getByTestId('education-frameworks-note').textContent).toBe(
      'The framework list could not be read (Failed (HTTP 502): the framework register did not answer), so only the '
      + 'default framework is offered below.'));
  });

  it('an empty list of frameworks is said as empty, not as unread', async () => {
    serve({ [FRAMEWORKS]: ok({ ...captured.frameworks, frameworks: [] }) });
    mount();
    await waitFor(() => expect(screen.getByTestId('education-frameworks-note').textContent).toBe(
      'The server lists no frameworks, so only the default framework is offered below.'));
  });

  it('a refused read of what each form does is said with its reason, and no form claims it', async () => {
    serve({ [TOOLS]: refused(503, 'the form register is locked') });
    mount();
    await waitFor(() => expect(screen.getByTestId('education-form-not-read').textContent).toContain(
      'Failed (HTTP 503): the form register is locked'));
    expect(screen.queryByTestId('education-form-says')).toBeNull();
  });
});
