// W989 (FU-399 part 21) — the Deliverables page, rendered against the deliverables routes' own answers.
//
// The page produces a living deliverable, lists them, opens one with its versions and its gates, refines it into a new
// version, and exports it. This mounts the real page against the answers its routes gave on a fresh store
// (Deliverables.fixture.json, captured by w989_capture.py: no deliverable, then one made-up brief on the deterministic
// floor, refined once), and has the server refuse each read and each action. An unread list is not an empty one, and
// a refusal is said on the page with the server's reason.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Deliverables.fixture.json';
import { Deliverables } from './Deliverables';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const one = captured.one;
const URL = {
  list: '/api/v1/deliverables', types: '/api/v1/deliverables/types', formats: '/api/v1/deliverables/output-formats',
  one: `/api/v1/deliverables/${one.id}`, refine: '/api/v1/refine', version: `/api/v1/deliverables/${one.id}/regenerate`,
  exportMd: `/api/v1/deliverables/${one.id}/export?format=md`,
};

function serve(list: Reply, over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [URL.list]: list, [URL.types]: ok(captured.types), [URL.formats]: ok(captured.formats), [URL.one]: ok(one),
    [URL.refine]: ok(captured.refine), [URL.version]: ok(captured.version), [URL.exportMd]: captured.export_missing,
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const heading = () => screen.getByText(/^Deliverables \(/).textContent?.trim();
const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);
async function openTheDeliverable() {
  fireEvent.click(await screen.findByRole('button', { name: new RegExp(one.title) }));
  await screen.findByText(`${one.type} · v${one.versions.length}`);
}

describe('Deliverables, rendered against the deliverables routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('no deliverable yet: the list says none', async () => {
    serve(ok(captured.list_empty));
    render(<Deliverables />);
    expect(await screen.findByText('None yet — produce one above.')).toBeTruthy();
    expect(heading()).toBe('Deliverables (0)');
  });

  it('a refused list is not shown as an empty one', async () => {
    serve(refused(503, 'the deliverables store could not be read'));
    render(<Deliverables />);
    await waitFor(() => expect(screen.getByTestId('deliverables-unread').textContent).toBe(
      'The deliverables could not be read, so this is not a list of none.'));
    expect(failures()).toContain('Could not read the deliverables — Failed (HTTP 503): the deliverables store could not be read');
    expect(heading()).toBe('Deliverables (not read)');
    expect(screen.queryByText('None yet — produce one above.')).toBeNull();
  });

  it('a refused read of the types is said with its reason, and opening a deliverable does not erase it', async () => {
    serve(ok(captured.list), { [URL.types]: refused(502, 'the type registry did not answer') });
    render(<Deliverables />);
    const said = 'Could not read the deliverable types — Failed (HTTP 502): the type registry did not answer';
    await waitFor(() => expect(failures()).toContain(said));
    expect(screen.queryByText('Failed to load types')).toBeNull();
    await openTheDeliverable();
    expect(failures()).toContain(said);
  });

  it('a deliverable opens, is refined, and the refined text is kept as its next version', async () => {
    serve(ok(captured.list));
    render(<Deliverables />);
    await openTheDeliverable();
    fireEvent.change(screen.getByPlaceholderText(/^Refine this deliverable/), { target: { value: 'Make the aims one sentence each.' } });
    fireEvent.click(screen.getByRole('button', { name: /Refine → new version/ }));
    await screen.findByText(`${captured.version.type} · v${captured.version.versions.length}`);
    expect(captured.version.versions.length).toBe(one.versions.length + 1);
    expect(screen.queryByTestId('deliverables-error')).toBeNull();
  });

  it('a refused refine says the step and the server\'s reason', async () => {
    serve(ok(captured.list), { [URL.refine]: refused(503, 'the refiner is paused') });
    render(<Deliverables />);
    await openTheDeliverable();
    fireEvent.change(screen.getByPlaceholderText(/^Refine this deliverable/), { target: { value: 'Shorter.' } });
    fireEvent.click(screen.getByRole('button', { name: /Refine → new version/ }));
    await waitFor(() => expect(screen.getByTestId('deliverables-error').textContent).toBe(
      'The refine was not done: Failed (HTTP 503): the refiner is paused'));
  });

  it('a refused version says the step and the server\'s reason', async () => {
    serve(ok(captured.list), { [URL.version]: refused(409, 'the quality gate refused this version') });
    render(<Deliverables />);
    await openTheDeliverable();
    fireEvent.change(screen.getByPlaceholderText(/^Refine this deliverable/), { target: { value: 'Shorter.' } });
    fireEvent.click(screen.getByRole('button', { name: /Refine → new version/ }));
    await waitFor(() => expect(screen.getByTestId('deliverables-error').textContent).toBe(
      'The refined text was not saved as a new version: Failed (HTTP 409): the quality gate refused this version'));
  });

  it('a refused export is said on the page with the server\'s reason, not in an alert', async () => {
    const alert = vi.spyOn(window, 'alert').mockImplementation(() => undefined);
    serve(ok(captured.list));
    render(<Deliverables />);
    await openTheDeliverable();
    fireEvent.click(screen.getByRole('button', { name: /^Download/ }));
    const r = captured.export_missing;
    await waitFor(() => expect(screen.getByTestId('deliverables-error').textContent).toBe(
      `Export failed (HTTP ${r.status}): ${r.body.detail}`));
    expect(alert).not.toHaveBeenCalled();
  });
});
