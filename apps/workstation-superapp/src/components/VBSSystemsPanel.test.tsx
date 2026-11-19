// W983 (FU-399 part 15) — the VBS systems panel, rendered against the VBS routes' own answers.
//
// The panel is on the Cockpit, and it is where the Owner turns the defect loop on their own store (FU-1038): select an
// open defect whose label no live surface uses, type the reason once and close it as its source retired, or report
// one not reproducible with what was tried. This mounts the real panel against the answers the VBS routes gave on a
// fresh store (VBSSystemsPanel.fixture.json, captured by w983_capture.py: one defect opened by a failing what-if gate,
// one under a label no live surface uses, each taken out of the loop as the Owner will, and the route's refusals),
// drives the loop as the Owner would, and has the server refuse each read.
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VBSSystemsPanel.fixture.json';
import { VBSSystemsPanel } from './VBSSystemsPanel';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

const RETIRED = captured.defects_open.defects.find(d => d.label_live === false);
const LIVE = captured.defects_open.defects.find(d => d.label_live === true);
const REASON = captured.closed_retired.defect.closure.reason;

function serve(over: Record<string, Reply | (() => Reply)> = {}) {
  const posts: { url: string; body: unknown }[] = [];
  const base: Record<string, Reply> = {
    'GET /api/v1/vbs/systems': ok(captured.systems),
    'GET /api/v1/vbs/qms/defects': ok(captured.defects_open),
    'GET /api/v1/vbs/qms/document-control': ok(captured.document_control),
    'GET /api/v1/vbs/backbone/health': ok(captured.backbone),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = (init?.method ?? 'GET').toUpperCase();
    const key = `${method} ${url}`;
    if (method === 'POST') posts.push({ url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    const r = key in over ? over[key] : base[key];
    const reply = (typeof r === 'function' ? r() : r) ?? refused(404, `not served in this test: ${key}`);
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
  return posts;
}

const rowButton = (id: string) => screen.getByText(id).closest('button') as HTMLElement;

describe('VBSSystemsPanel, rendered against the VBS routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the catalogue is the route\'s: what is real, what is simulated, and the system another owns', async () => {
    serve();
    render(<VBSSystemsPanel />);
    // each system's card opens with its name, in the catalogue's own paragraph
    const card = (name: string) => screen.getAllByText(name, { exact: false }).find(el => el.textContent?.startsWith(name));
    await screen.findAllByText(captured.systems.systems[0].name, { exact: false });
    for (const s of captured.systems.systems) expect(card(s.name)).toBeTruthy();
    const dcms = captured.systems.systems.find(s => s.id === 'dcms') as { name: string; owned_by?: string };
    expect(card(dcms.name)?.textContent).toContain(`(owned by ${String(dcms.owned_by).toUpperCase()})`);
  });

  it('each open defect is listed, and one under a label no live surface uses is marked so', async () => {
    serve();
    render(<VBSSystemsPanel />);
    const s = captured.defects_open.summary;
    expect(await screen.findByText(`${s.open} open`)).toBeTruthy();
    expect(screen.getByText(`${s.open_from_retired_labels} open under a label no live surface uses`)).toBeTruthy();
    expect(screen.getByTestId('qms-no-gates')).toBeTruthy();
    expect(rowButton(String(RETIRED?.id)).textContent).toContain('no live surface uses this label');
    expect(rowButton(String(LIVE?.id)).textContent).not.toContain('no live surface uses this label');
  });

  it('the Owner\'s loop: the reason typed once closes a retired source, then reports the next not reproducible', async () => {
    let state = 0;
    const mid = clone(captured.defects_open);
    mid.defects = mid.defects.map((d: { id: string }) =>
      d.id === RETIRED?.id ? captured.defects_after.defects.find(x => x.id === d.id) : d);
    const posts = serve({
      'GET /api/v1/vbs/qms/defects': () => ok(state === 0 ? captured.defects_open : state === 1 ? mid : captured.defects_after),
      [`POST /api/v1/vbs/qms/defects/${RETIRED?.id}/close-source-retired`]: () => { state = 1; return ok(captured.closed_retired); },
      [`POST /api/v1/vbs/qms/defects/${LIVE?.id}/not-reproducible`]: () => { state = 2; return ok(captured.not_reproducible); },
    });
    render(<VBSSystemsPanel />);
    fireEvent.click(await waitFor(() => rowButton(String(RETIRED?.id))));
    const dispose = screen.getByTestId('defect-dispose');
    expect(within(dispose).queryByTestId('defect-retired-route')).toBeNull();
    const close = screen.getByTestId('defect-close-retired') as HTMLButtonElement;
    fireEvent.change(screen.getByTestId('defect-dispose-reason'), { target: { value: 'too short' } });
    expect(close.disabled).toBe(true);
    fireEvent.change(screen.getByTestId('defect-dispose-reason'), { target: { value: REASON } });
    fireEvent.click(close);
    const c1 = captured.closed_retired.defect.closure;
    await waitFor(() => expect(screen.getByTestId('defect-closure').textContent).toBe(
      `closed — its source was retired by ${c1.by} (typed, sign-in off) at ${c1.at} (it was ${c1.status_before}): ${c1.reason} · ${c1.source_check}`));
    expect(posts[0]).toEqual({ url: `/api/v1/vbs/qms/defects/${RETIRED?.id}/close-source-retired`, body: { reason: REASON } });

    //  the next one: its label is live, so the route field is offered; the reason is still there, typed once
    fireEvent.click(rowButton(String(LIVE?.id)));
    expect(screen.getByTestId('defect-retired-route')).toBeTruthy();
    expect((screen.getByTestId('defect-dispose-reason') as HTMLInputElement).value).toBe(REASON);
    fireEvent.click(screen.getByTestId('defect-not-reproducible'));
    const c2 = captured.not_reproducible.defect.closure;
    await waitFor(() => expect(screen.getByTestId('defect-closure').textContent).toBe(
      `reported not reproducible by ${c2.by} (typed, sign-in off) at ${c2.at} (it was ${c2.status_before}): ${c2.reason}`));
    expect(posts[1]).toEqual({ url: `/api/v1/vbs/qms/defects/${LIVE?.id}/not-reproducible`, body: { tried: REASON } });
  });

  it('a live label closed as retired with no route named is refused in the server\'s own words', async () => {
    serve({ [`POST /api/v1/vbs/qms/defects/${LIVE?.id}/close-source-retired`]: {
      status: captured.refused_live_label.status, body: captured.refused_live_label.body } });
    render(<VBSSystemsPanel />);
    fireEvent.click(await waitFor(() => rowButton(String(LIVE?.id))));
    fireEvent.change(screen.getByTestId('defect-dispose-reason'), { target: { value: REASON } });
    fireEvent.click(screen.getByTestId('defect-close-retired'));
    expect(await screen.findByText(
      `Failed (HTTP ${captured.refused_live_label.status}): ${captured.refused_live_label.body.detail}`)).toBeTruthy();
    expect(screen.queryByTestId('defect-closure')).toBeNull();
  });

  it('each section that could not be read is named, with the server\'s reason', async () => {
    serve({
      'GET /api/v1/vbs/systems': refused(503, 'the catalogue could not be read'),
      'GET /api/v1/vbs/qms/defects': refused(503, 'the QMS store is locked'),
      'GET /api/v1/vbs/backbone/health': refused(502, 'the backbone did not answer'),
    });
    render(<VBSSystemsPanel />);
    await waitFor(() => expect(screen.getAllByTestId('read-failure')).toHaveLength(3));
    const said = screen.getAllByTestId('read-failure').map(p => p.textContent);
    expect(said).toEqual(expect.arrayContaining([
      'Could not read the VBS systems — Failed (HTTP 503): the catalogue could not be read',
      'Could not read the QMS defects — Failed (HTTP 503): the QMS store is locked',
      'Could not read the backbone health — Failed (HTTP 502): the backbone did not answer',
    ]));
    expect(screen.queryByText(/no defects recorded/)).toBeNull();
  });

  it('an empty list read whole says none is recorded; one not read whole says it is not a record of none', async () => {
    serve({ 'GET /api/v1/vbs/qms/defects': ok(captured.defects_empty) });
    const a = render(<VBSSystemsPanel />);
    expect(await screen.findByText('no defects recorded — a failed gate opens one, including a failed what-if')).toBeTruthy();
    a.unmount();

    const partial = clone(captured.defects_empty);
    partial.listing_is_incomplete = true;
    partial.store_incomplete = 'w983 the store ended early';
    serve({ 'GET /api/v1/vbs/qms/defects': ok(partial) });
    render(<VBSSystemsPanel />);
    expect(await screen.findByText('the defect list could NOT be read — this is not a record of zero defects')).toBeTruthy();
    expect(screen.queryByText(/no defects recorded/)).toBeNull();
  });
});
