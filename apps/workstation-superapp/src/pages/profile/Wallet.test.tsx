// W981 (FU-399 part 14) — the Wallet page, rendered against the fund routes' own answers.
//
// The Wallet is where the capital fund is read: what it holds and has allocated, the requests held at Change Control,
// and the reversal of an allocation (the Owner's FU-1005 action starts here). Four guards read its source. This mounts
// the real page against the answers the fund routes gave on a fresh store (Wallet.fixture.json, captured by
// w981_capture.py from a made-up fund of two allocations, one reversal held, approved and applied, and two refusals),
// drives the reversal as a person would, and has the server refuse each read and each request.
import { fireEvent, render, screen, within } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Wallet.fixture.json';
import { Wallet } from './Wallet';

type Reply = { status: number; data: unknown };
const ok = (data: unknown): Reply => ({ status: 200, data });
const refused = (status: number, detail: string): Reply => ({ status, data: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: { status?: Reply; portfolio?: Reply; reverse?: Reply | Error; unreachable?: boolean } = {}) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (a.unreachable) throw new Error('Network Error');
    if (url === '/api/v1/fund/status') return (a.status ?? ok(captured.status)) as never;
    if (url === '/api/v1/fund/portfolio') return (a.portfolio ?? ok(captured.portfolio)) as never;
    return refused(404, `not served in this test: ${url}`) as never;
  });
  const posts: { url: string; body: unknown }[] = [];
  vi.spyOn(axios, 'post').mockImplementation(async (url: string, body?: unknown) => {
    posts.push({ url, body });
    const r = a.reverse ?? ok(captured.reverse_held);
    if (r instanceof Error) throw r;
    return r as never;
  });
  return posts;
}

// a figure card: its label is a <p>, its value the card's large figure
const card = (label: string) => {
  const el = screen.getByText(label, { selector: 'p' }).parentElement as HTMLElement;
  return el.querySelector('div.text-3xl')?.textContent;
};
// the reason the capture gave, and the row of the allocation it reversed
const WHY = captured.portfolio_held.reversal_requests[0].reason;
const REVERSED = captured.portfolio.allocations.find(a => a.allocation_id === captured.reverse_held.allocation_id);
const rowOf = (name: string) => screen.getByText(name).closest('div.justify-between') as HTMLElement;

describe('Wallet, rendered against the fund routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('the fund\'s figures are the status route\'s own, the pool included', async () => {
    serve();
    render(<Wallet />);
    const s = captured.status;
    expect((await screen.findByTestId('wallet-allocated')).textContent).toBe(s.allocated.toLocaleString());
    expect(screen.getByText(s.available.toLocaleString())).toBeTruthy();
    expect(card('Utilisation')).toBe(`${s.utilisation_pct}%`);
    expect(card('Fund Health')).toBe(s.fund_health);
    expect(card('Allocations')).toBe(String(s.allocation_count));
    expect(card('Total Pool')).toBe(`${s.total_capital.toLocaleString()} WST`);
    expect(screen.queryByTestId('wallet-status-unread')).toBeNull();
  });

  it('a refused status read is said, and every figure it would have given is a dash, never a zero', async () => {
    serve({ status: refused(503, 'the fund store is locked') });
    render(<Wallet />);
    expect((await screen.findByTestId('wallet-status-unread')).textContent).toBe(
      'The fund\'s status could not be read (HTTP 503): the fund store is locked');
    expect(screen.getByTestId('wallet-allocated').textContent).toBe('—');
    expect(card('Utilisation')).toBe('—');
    expect(card('Fund Health')).toBe('NOT READ');
    expect(card('Allocations')).toBe('—');
    expect(card('Total Pool')).toBe('—');
  });

  it('a portfolio that could not be read is said in both cards, never as nothing allocated or requested', async () => {
    serve({ portfolio: refused(503, 'the fund store could not be read') });
    render(<Wallet />);
    expect((await screen.findByTestId('wallet-portfolio-error')).textContent).toBe(
      'The portfolio could not be read (HTTP 503): the fund store could not be read');
    expect(screen.getByTestId('wallet-allocations-unread').textContent).toContain(
      'The portfolio was not read, so whether any capital has been allocated is not known.');
    expect(screen.queryByTestId('wallet-allocations-none')).toBeNull();
    expect(screen.queryByText('No allocation has been requested.')).toBeNull();
  });

  it('an unreachable server is said, never as an empty portfolio', async () => {
    serve({ unreachable: true });
    render(<Wallet />);
    expect((await screen.findByTestId('wallet-portfolio-error')).textContent).toBe(
      'The portfolio could not be read: the server could not be reached.');
    expect(card('Fund Health')).toBe('BACKEND UNREACHABLE');
    expect(screen.getByTestId('wallet-allocations-unread')).toBeTruthy();
    expect(screen.queryByText('No allocation has been requested.')).toBeNull();
    expect(screen.getByTestId('wallet-allocated').textContent).toBe('—');
  });

  it('a fund read whole that holds no allocation says none has been allocated', async () => {
    const empty = clone(captured.portfolio);
    empty.allocations = [];
    serve({ portfolio: ok(empty) });
    render(<Wallet />);
    expect((await screen.findByTestId('wallet-allocations-none')).textContent?.trim()).toBe('No capital has been allocated.');
    expect(screen.queryByTestId('wallet-allocations-unread')).toBeNull();
  });

  it('each allocation is the portfolio\'s own, with its record state, and an active one offers its reversal', async () => {
    serve();
    render(<Wallet />);
    const allocs = captured.portfolio.allocations;
    for (const a of allocs) expect(await screen.findByText(a.project_name)).toBeTruthy();
    const states = screen.getAllByTestId('wallet-allocation-state');
    expect(states.map(s => s.textContent)).toEqual(
      [...allocs].reverse().map(a => `${a.record_state_label}${(a as { cca_id?: string }).cca_id ? ` · change ${(a as { cca_id?: string }).cca_id}` : ''}`));
    const offers = screen.getAllByTestId('wallet-allocation-reverse');
    expect(offers).toHaveLength(allocs.filter(a => a.status === 'active').length);
    const button = within(offers[0]).getByRole('button', { name: 'request reversal' }) as HTMLButtonElement;
    expect(button.disabled).toBe(true);
    fireEvent.change(within(offers[0]).getByPlaceholderText('why this allocation is reversed…'), { target: { value: 'too short' } });
    expect(button.disabled).toBe(true);
  });

  it('a reversal requested is held, and the page says the server\'s own sentence', async () => {
    const posts = serve();
    render(<Wallet />);
    await screen.findByText(String(REVERSED?.project_name));
    const target = within(rowOf(String(REVERSED?.project_name))).getByTestId('wallet-allocation-reverse');
    fireEvent.change(within(target).getByPlaceholderText('why this allocation is reversed…'), { target: { value: WHY } });
    fireEvent.click(within(target).getByRole('button', { name: 'request reversal' }));
    expect((await within(target).findByTestId('wallet-allocation-reverse-said')).textContent).toBe(captured.reverse_held.basis);
    expect(posts).toEqual([{ url: `/api/v1/fund/allocations/${captured.reverse_held.allocation_id}/reverse`, body: { reason: WHY } }]);
  });

  it('a refused reversal says its status and the server\'s reason; one that could not be sent says so', async () => {
    serve({ reverse: { status: captured.refused_unknown.status, data: captured.refused_unknown.body } });
    const a = render(<Wallet />);
    let offer = (await screen.findAllByTestId('wallet-allocation-reverse'))[0];
    fireEvent.change(within(offer).getByPlaceholderText('why this allocation is reversed…'), { target: { value: WHY } });
    fireEvent.click(within(offer).getByRole('button', { name: 'request reversal' }));
    expect((await within(offer).findByTestId('wallet-allocation-reverse-said')).textContent).toBe(
      `Not requested (HTTP ${captured.refused_unknown.status}): ${captured.refused_unknown.body.detail}`);
    a.unmount();
    vi.restoreAllMocks();

    serve({ reverse: new Error('Network Error') });
    render(<Wallet />);
    offer = (await screen.findAllByTestId('wallet-allocation-reverse'))[0];
    fireEvent.change(within(offer).getByPlaceholderText('why this allocation is reversed…'), { target: { value: WHY } });
    fireEvent.click(within(offer).getByRole('button', { name: 'request reversal' }));
    expect((await within(offer).findByTestId('wallet-allocation-reverse-said')).textContent).toBe(
      'Not requested: the server could not be reached, so nothing was asked of Change Control.');
  });

  it('a held reversal is listed with its reason; a reversed allocation is shown reversed and offers no reversal', async () => {
    serve({ portfolio: ok(captured.portfolio_held) });
    const a = render(<Wallet />);
    const held = captured.portfolio_held.reversal_requests[0];
    const line = await screen.findByTestId('wallet-reversal-request');
    for (const part of [held.allocation_id, `${held.amount.toLocaleString()} WST`, held.status, `change ${held.cca_id}`,
                        `"${held.reason}"`, `asked by ${held.requested_by}`]) expect(line.textContent).toContain(part);
    a.unmount();

    serve({ portfolio: ok(captured.portfolio_reversed), status: ok(captured.status_reversed) });
    render(<Wallet />);
    const row = captured.portfolio_reversed.allocations.find(x => x.status === 'reversed') as unknown as
      { reversal: { reason: string; reversed_at: string; cca_id: string; requested_by: string } };
    const said = await screen.findByTestId('wallet-allocation-reversed');
    expect(said.textContent?.trim()).toBe(
      `REVERSED ${row.reversal.reversed_at}: ${row.reversal.reason} · change ${row.reversal.cca_id} · asked by ${row.reversal.requested_by}`);
    expect(screen.getAllByTestId('wallet-allocation-reverse')).toHaveLength(
      captured.portfolio_reversed.allocations.filter(x => x.status === 'active').length);
    expect(screen.getByTestId('wallet-allocated').textContent).toBe(captured.status_reversed.allocated.toLocaleString());
  });
});
