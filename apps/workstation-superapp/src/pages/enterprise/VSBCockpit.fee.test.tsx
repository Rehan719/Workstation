// W1139 (FU-1281, P5.16 clauses 3 and 4) — the cockpit's latest cycle says the platform's fee it took first and what
// the entity's split was over, in the cycle's own words, as the VSB Economy page says them (W1125).
//
// The cockpit's latest cycle named the intake, the costs, the reserve and the distributable profit, and not the fee
// taken first nor what the split was over, so its stages read short of the profit by the fee; its rendered tests ran no
// cycle that succeeded. Here the cockpit is mounted on its economy tab against what its routes answered on a fresh
// store (VSBCockpit.fee.fixture.json, captured by w1139_capture.py): a made-up entity established through Genesis, the
// one door, opened as the cockpit opens it; a cycle run by the cockpit's own button on the 10,000 WST typed into its
// revenue field, as the route answered it; and the ledger the cockpit reads again after the cycle, as it answered then.
// Virtual WST; nothing is charged.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBCockpit.fee.fixture.json';
import { VSBCockpit } from './VSBCockpit';

type Answer = { status: number; body: any; request?: unknown };
const answers = captured.answers as unknown as Record<string, Answer>;
const cycle = captured.cycle as unknown as Answer;
const after = captured.ledger_after as unknown as Answer;
const VID = captured.vsb_id;
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  each read as its route answered it; the cycle as the route answered it, with what the cockpit asked it kept to be
//  read; and after the cycle, the ledger as it answered then
function serve() {
  const asked: unknown[] = [];
  let ran = false;
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: Record<string, string>; validateStatus?: unknown }) => {
    const key = config?.params ? `${url}?${new URLSearchParams(config.params).toString()}` : url;
    const a = (ran && key === `/api/v1/economy/ledger/${VID}` ? after : undefined) ?? answers[key]
      ?? { status: 404, body: { detail: `not served here: ${key}` } };
    if (a.status >= 400 && !config?.validateStatus) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string, body?: unknown) => {
    if (url !== '/api/v1/economy/cycle') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    asked.push(body);
    ran = true;
    return { status: cycle.status, data: cycle.body };
  });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({ detail: `not served here: ${url}` }) })));
  return asked;
}

//  a figure on the latest cycle's card is drawn after its label
function figure(label: string): string | null {
  return screen.getByText(`${label}:`, { selector: 'span' }).nextElementSibling?.textContent ?? null;
}

describe('VSBCockpit, the latest cycle and the platform fee (P5.16)', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('a cycle run from the cockpit says the fee it took first and what the split was over, in the cycle\'s own words', async () => {
    const asked = serve();
    render(<MemoryRouter initialEntries={['/cockpit?tab=economy']}><VSBCockpit /></MemoryRouter>);
    fireEvent.change(await screen.findByLabelText('Revenue for this economic cycle in virtual WST'), { target: { value: '10000' } });
    fireEvent.click(screen.getByRole('button', { name: /Run economic cycle/ }));
    const cy = cycle.body.cycle;
    expect([cy.platform_fee.posted, cy.platform_fee.fee_wst * 4, cy.split_base_wst + cy.platform_fee.fee_wst])
      .toEqual([true, cy.distributable_profit, cy.distributable_profit]);
    await waitFor(() => expect(screen.getByTestId('cockpit-platform-fee').textContent).toBe(`Platform fee: ${cy.platform_fee.basis}.`));
    expect([figure('Distributable profit'), figure('Platform fee'), figure('Split over')]).toEqual(
      [cy.distributable_profit, cy.platform_fee.fee_wst, cy.split_base_wst].map((n: number) => n.toLocaleString()));
    expect(asked).toEqual([cycle.request]);
  });
});
