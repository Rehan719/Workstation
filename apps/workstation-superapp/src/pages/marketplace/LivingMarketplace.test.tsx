// W1040 (FU-399 part 61) — the Living Marketplace, rendered against its routes' own answers.
//
// The marketplace shows the product catalogue (what exists) and the listings priced for trade in virtual WST (what
// someone has priced). This mounts the real page against what the two routes answered on a fresh store
// (LivingMarketplace.fixture.json, captured by w1040_capture.py): the catalogue, the listings the store seeds from it,
// and each route's own 500 when its read fails inside; and has the listings' server be unreachable. Rendering found two
// defects, fixed in this round: a failed read of the catalogue was said in one fixed sentence with the reason
// dropped, and a failed read of the listings sat above a list that said none were registered.
import { render, screen, waitFor, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './LivingMarketplace.fixture.json';
import { LivingMarketplace } from './LivingMarketplace';

type Answer = { status: number; body: unknown };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  the catalogue is read through axios, the listings through fetch (apiJson); each answers as captured unless told
function serve(over: { catalog?: Answer; listings?: Answer | 'unreached' } = {}) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/catalog/products') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    const a = over.catalog ?? captured.catalog;
    if (a.status >= 400) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== '/api/v1/marketplace/listings') return { ok: false, status: 404, statusText: '', json: async () => ({ detail: `not served: ${url}` }) };
    const a = over.listings ?? captured.listings;
    if (a === 'unreached') throw new TypeError('Failed to fetch');
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
}

function mount() {
  render(<MemoryRouter><LivingMarketplace /></MemoryRouter>);
}

const listingsSection = () => screen.getByTestId('listings-caption').closest('section') as HTMLElement;
const NONE = 'No listings are registered.';

describe('LivingMarketplace, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('shows the catalogue and the listings the routes answered', async () => {
    serve();
    mount();
    const product = captured.catalog.body.products.find(p => p.status === 'live') as { name: string };
    expect((await screen.findAllByText(product.name)).length).toBeGreaterThan(0);
    const listing = captured.listings.body[0] as { name: string };
    await waitFor(() => expect(within(listingsSection()).getByText(listing.name).textContent).toBe(listing.name));
    expect(screen.queryByText(NONE)).toBeNull();
    expect(screen.queryByTestId('catalog-unread')).toBeNull();
    expect(screen.queryByTestId('listings-unread')).toBeNull();
  });

  it('a catalogue that could not be read says why', async () => {
    serve({ catalog: captured.catalog_failed });
    mount();
    await waitFor(() => expect(screen.getByTestId('catalog-unread').textContent)
      .toBe(`The catalogue could not be read: Failed (HTTP 500): ${captured.catalog_failed.body.detail}`));
    expect(screen.queryByText('Failed to load catalog.')).toBeNull();
  });

  it('listings that could not be read are said as unread, not as none registered', async () => {
    serve({ listings: captured.listings_failed });
    mount();
    await waitFor(() => expect(screen.getByTestId('listings-unread').textContent)
      .toBe(`The listings could not be read: Failed (HTTP 500): ${captured.listings_failed.body.detail}`));
    expect(screen.queryByText(NONE)).toBeNull();
  });

  it('listings whose server cannot be reached are said as such, not as none registered', async () => {
    serve({ listings: 'unreached' });
    mount();
    await waitFor(() => expect(screen.getByTestId('listings-unread').textContent)
      .toBe('The listings could not be read: Failed — backend unreachable.'));
    expect(screen.queryByText(NONE)).toBeNull();
  });
});
