// W1002 (FU-399 part 32) — the charity directives panel, rendered against the charity routes' own answers.
//
// The panel holds where the charity stage of the profit waterfall is directed, what it must never fund and whether all
// of a charity allocation must reach the cause, beside the ranked pool of causes those directives act on. This mounts
// the real component against the answers its routes gave on a fresh store (CharityDirectives.fixture.json, captured by
// w1002_capture.py: the defaults, the pool, and a save naming an exclusion that matches no cause), and has the server
// refuse each read and a save. A refused read is said as the read it was, the form shows nothing it did not read, and
// a refused save is said as a save that did not happen.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './CharityDirectives.fixture.json';
import { CharityDirectives } from './CharityDirectives';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const DIRECTIVES = '/api/v1/economy/charity/directives';
const SAVE = `POST ${DIRECTIVES}`;
const POOL = '/api/v1/economy/charity/candidates?top=12';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [DIRECTIVES]: ok(captured.directives), [POOL]: ok(captured.candidates), [SAVE]: ok(captured.saved),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const key = init?.method === 'POST' ? `POST ${url}` : url;
    const r = (key in over ? over[key] : base[key]) ?? refused(404, `not served in this test: ${key}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);
const field = (label: string) => screen.getByLabelText(label) as HTMLInputElement;

describe('CharityDirectives, rendered against the charity routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a fresh store: the defaults are said as defaults, and the pool is listed', async () => {
    serve();
    render(<CharityDirectives />);
    await waitFor(() => expect(screen.getByTestId('directives-provenance').textContent).toBe(
      `still on defaults · ${captured.directives.source}`));
    expect(field('Charity priorities').value).toBe(captured.directives.priorities.join(', '));
    expect(await screen.findByText(captured.candidates.candidates[0].cause)).toBeTruthy();
    expect(failures()).toEqual([]);
  });

  it('a refused read of the directives is said as that, and the form shows nothing it did not read', async () => {
    serve({ [DIRECTIVES]: refused(503, 'the directives store is locked') });
    render(<CharityDirectives />);
    await waitFor(() => expect(failures()).toEqual([
      'Could not read the charity directives — Failed (HTTP 503): the directives store is locked']));
    expect(field('Charity exclusions').placeholder).not.toBe('none set');
    expect(field('Charity exclusions').disabled).toBe(true);
    expect(field('Require 100% of the charity allocation to reach the cause').disabled).toBe(true);
    expect(screen.queryByText('No changes')).toBeNull();
  });

  it('a save the server refuses is said as a save that did not happen', async () => {
    serve({ [SAVE]: refused(400, 'priorities must name cause ids') });
    render(<CharityDirectives />);
    await screen.findByTestId('directives-provenance');
    fireEvent.change(field('Charity priorities'), { target: { value: 'clean_water' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save directives' }));
    await waitFor(() => expect(screen.getByTestId('directives-save-error').textContent).toBe(
      'The directives were not saved — Failed (HTTP 400): priorities must name cause ids'));
  });

  it('a refused read of the pool is said, and the ids typed are said to be unchecked', async () => {
    serve({ [POOL]: refused(502, 'the cause register did not answer') });
    render(<CharityDirectives />);
    await waitFor(() => expect(failures()).toEqual([
      'Could not read the charity candidates — Failed (HTTP 502): the cause register did not answer']));
    await waitFor(() => expect(screen.getByTestId('directives-ids-unchecked').textContent).toBe(
      'The ids typed here are not checked against the causes: the charity candidates could not be read.'));
  });

  it('a saved exclusion that matches no cause is answered with the server\'s own note', async () => {
    serve();
    render(<CharityDirectives />);
    await screen.findByTestId('directives-provenance');
    fireEvent.change(field('Charity exclusions'), { target: { value: 'w1002-no-such-cause' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save directives' }));
    expect((await screen.findByText(captured.saved.directives_match_note)).getAttribute('data-testid')).toBe(
      'directives-match-note');
    expect(screen.getByTestId('directives-provenance').textContent).toMatch(/^set by you · /);
  });
});
