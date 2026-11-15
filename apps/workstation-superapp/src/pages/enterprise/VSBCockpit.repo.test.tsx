// W1057 (FU-399 part 75) — the cockpit's repository panel, rendered against its routes' own answers.
//
// The transformation tab shows an entity's repository (its declared tree, a file opened from it, whether the shipped
// body is current) and lists its products on the marketplace. This mounts the real cockpit on the tab against what
// each route answered for two entities established through Genesis on a fresh store with no model installed, the one
// the cockpit opens on with its repository shipped (VSBCockpit.repo.fixture.json, captured by w1057_capture.py: every
// read on opening either after that ship, one file of its tree, and the listing route's refusal of an entity with no
// objective of its own). Rendering found the panel's reads and actions tied to no entity: a slow answer for one entity
// was said under the next one opened, its files as the other's tree, "Shipped body is current" over an entity never
// shipped, its refusal as the other's. Fixed in this round.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.repo.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: unknown };
const answers = captured.answers as Record<string, Answer>;
const VID = captured.vsb_id;
const OTHER = captured.other_id;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  each read as its route answered it; when asked, the shipped entity's tree and ship state, or its listing, are held
//  back until the test lets them go
function serve(o: { hold?: 'reads' | 'listing' } = {}) {
  let letGo: () => void = () => undefined;
  const gate = new Promise<void>(go => { letGo = go; });
  const held = (key: string) => o.hold === 'reads' && (key === `/api/v1/vsb/${VID}/repo` || key === `/api/v1/vsb/${VID}/repo/ship`);
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    if (held(key)) await gate;
    if (key === `/api/v1/vsb/${VID}/repo/file?path=${encodeURIComponent(captured.file.path)}`) {
      return { status: captured.file.status, data: captured.file.text, headers: { 'x-repo-bytes': captured.file.bytes } };
    }
    const a = answers[key] ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== `/api/v1/marketplace/listings/from-entity/${VID}`) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (o.hold === 'listing') await gate;
    return { status: captured.listed.status, data: captured.listed.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return { letGo: () => letGo() };
}

const mount = () => render(<MemoryRouter initialEntries={['/cockpit?tab=transform']}><VSBCockpit /></MemoryRouter>);
const open = (id: string) => fireEvent.change(screen.getByLabelText('Select VSB'), { target: { value: id } });
const shippedAt = String((answers[`/api/v1/vsb/${VID}/repo/ship`].body as { shipped_at: string }).shipped_at);
const noneOf = (id: string) => String((answers[`/api/v1/vsb/${id}/repo`].body as { detail: string }).detail);
const current = () => screen.queryByText(/^Shipped body is current/);

describe('VSBCockpit\'s repository panel, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('shows the shipped repository, opens a file from it, and says the shipped body is current', async () => {
    serve();
    mount();
    await waitFor(() => expect(current()?.textContent).toBe(`Shipped body is current (shipped ${shippedAt})`));
    fireEvent.click(await screen.findByRole('button', { name: captured.file.path }));
    await waitFor(() => expect(screen.getByTestId('cockpit-repo-preview').textContent).toBe(captured.file.text.slice(0, 4000)));
    expect(screen.getByText(`${captured.file.path} · ${captured.file.bytes} bytes`)).toBeTruthy();
  });

  it('a slow read of one entity\'s repository is never said under the entity opened after it', async () => {
    const { letGo } = serve({ hold: 'reads' });
    mount();
    await screen.findByTestId('cockpit-repo');
    open(OTHER);
    await waitFor(() => expect(screen.getByTestId('cockpit-repo-none').textContent).toBe(noneOf(OTHER)));
    letGo();
    await new Promise(r => setTimeout(r, 50));
    expect(screen.queryByTestId('cockpit-repo-tree')).toBeNull();
    expect(current()).toBeNull();
    expect(screen.getByTestId('cockpit-repo-none').textContent).toBe(noneOf(OTHER));
  });

  it('a listing refused for one entity is never said under the entity opened after it', async () => {
    const { letGo } = serve({ hold: 'listing' });
    mount();
    await waitFor(() => expect(current()).toBeTruthy());
    fireEvent.click(screen.getByTestId('cockpit-list-products'));
    open(OTHER);
    await waitFor(() => expect(screen.getByTestId('cockpit-repo-none').textContent).toBe(noneOf(OTHER)));
    letGo();
    await new Promise(r => setTimeout(r, 50));
    expect(screen.queryByTestId('cockpit-repo-error')).toBeNull();
  });

  it('the listing route\'s refusal is said under the entity it was asked for', async () => {
    serve();
    mount();
    await waitFor(() => expect(current()).toBeTruthy());
    fireEvent.click(screen.getByTestId('cockpit-list-products'));
    //  W1058 - by the route's sentence: the shared reader said the gate's code, "kpi_gate"
    const why = String((captured.listed.body as { detail: { detail: string } }).detail.detail);
    //  W1059 - and the sentence around it ends once: the route's own full stop was followed by the page's
    await waitFor(() => expect(screen.getByTestId('cockpit-repo-error').textContent).toBe(
      `The products were not listed (HTTP 409): ${why.replace(/\.$/, '')}. Nothing was added to the marketplace.`));
    expect(screen.getByTestId('cockpit-repo-error').textContent).not.toContain('kpi_gate');
  });
});
