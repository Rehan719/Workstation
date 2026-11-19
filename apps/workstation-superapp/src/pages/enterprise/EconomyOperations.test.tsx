// W1000 (FU-399 part 31) — the Economy Operations panels, rendered against the economy routes' own answers.
//
// The venture portfolio panel shows an entity's holdings, the returns recorded on them and the candidates the next
// cycle's allocation draws on; the transfer panel moves virtual WST to the owner's other entities, offers to complete
// a debited transfer, and shows where the entity's recorded credits came from. This mounts both against the answers
// their routes gave on a fresh store (EconomyOperations.fixture.json, captured by w1000_capture.py: two made-up living
// entities, and a transfer from one whose fund is empty), and has the server refuse each read. A failed read is said
// with the server's reason, a read under way is not an empty portfolio, and an unread list is not a list of none.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './EconomyOperations.fixture.json';
import { TransferPanel, VenturePortfolioPanel } from './EconomyOperations';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const [A, B] = captured.entities.map(e => e.vsb_id);
const URL = {
  portfolio: `/api/v1/economy/ventures/portfolio?vsb_id=${A}`,
  candidates: `/api/v1/economy/ventures/candidates?vsb_id=${A}&top=5`,
  open: `/api/v1/economy/transfers/open?from_vsb=${A}`,
  intake: `/api/v1/economy/transfers/intake-sources?vsb_id=${A}`,
  transfer: '/api/v1/economy/transfer',
};

//  a read the test holds unanswered, to see the panel while it is under way
const never = new Promise<never>(() => undefined);
function serve(over: Record<string, Reply> = {}, held: string[] = []) {
  const base: Record<string, Reply> = {
    [URL.portfolio]: ok(captured.portfolio), [URL.candidates]: ok(captured.candidates), [URL.open]: ok(captured.open),
    [URL.intake]: ok(captured.intake),
    [URL.transfer]: { status: captured.transfer.status, body: captured.transfer.body },
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (held.includes(url)) await never;
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', headers: { get: () => null }, json: async () => r.body };
  }));
}

const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);
const portfolio = () => render(<VenturePortfolioPanel vsbId={A} />);
const transfers = () => render(<TransferPanel fromVsb={A} entities={captured.entities} />);

describe('VenturePortfolioPanel, rendered against the venture routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('both reads answered: the empty portfolio is said as the server says it, and the candidate is listed', async () => {
    serve();
    portfolio();
    expect(await screen.findByText(captured.portfolio.note)).toBeTruthy();
    expect(captured.portfolio.holdings).toHaveLength(0);
    expect(await screen.findByText(captured.candidates.candidates[0].name)).toBeTruthy();
    expect(failures()).toEqual([]);
  });

  it('a refused portfolio read is said with the server\'s reason, and is not a portfolio of none', async () => {
    serve({ [URL.portfolio]: refused(404, 'no such entity for this owner') });
    portfolio();
    await waitFor(() => expect(failures()).toEqual([
      'Could not read the venture portfolio — Failed (HTTP 404): no such entity for this owner']));
    expect(screen.queryByText(/^No venture investments yet/)).toBeNull();
  });

  it('a portfolio still being read is not shown as a portfolio of none', async () => {
    serve({}, [URL.portfolio]);
    portfolio();
    expect(await screen.findByText(captured.candidates.candidates[0].name)).toBeTruthy();
    expect(screen.queryByText(/^No venture investments yet/)).toBeNull();
  });

  it('a refused read of the candidates is said, not hidden as none', async () => {
    serve({ [URL.candidates]: refused(503, 'the venture register is locked') });
    portfolio();
    await waitFor(() => expect(failures()).toEqual([
      'Could not read the investment candidates — Failed (HTTP 503): the venture register is locked']));
    expect(await screen.findByText(captured.portfolio.note)).toBeTruthy();
  });
});

describe('TransferPanel, rendered against the transfer routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a transfer from an empty fund is refused as the server says it, and nothing is said stranded', async () => {
    serve();
    transfers();
    expect(await screen.findByText(captured.intake.basis)).toBeTruthy();
    fireEvent.change(screen.getByLabelText('transfer receiver'), { target: { value: B } });
    fireEvent.change(screen.getByLabelText('transfer amount'), { target: { value: '5' } });
    const send = screen.getByRole('button', { name: /Transfer/ });
    await waitFor(() => expect((send as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(send);
    expect(await screen.findByText(captured.transfer.body.detail)).toBeTruthy();
    expect(captured.transfer.status).toBe(400);
    expect(screen.queryByTestId('transfer-stranded')).toBeNull();
  });

  it('a refused check for debited transfers says the server\'s reason, and Transfer stays locked', async () => {
    serve({ [URL.open]: refused(503, 'the ledger store is locked') });
    transfers();
    await waitFor(() => expect(screen.getByTestId('transfer-open-error').textContent).toContain(
      'Could not check for debited transfers awaiting completion — Failed (HTTP 503): the ledger store is locked'));
    expect((screen.getByRole('button', { name: /Transfer/ }) as HTMLButtonElement).disabled).toBe(true);
  });

  it('a refused read of where the credits came from is said, not hidden', async () => {
    serve({ [URL.intake]: refused(500, 'the transfer record could not be read') });
    transfers();
    await waitFor(() => expect(screen.getByTestId('transfer-intake-unread').textContent).toBe(
      'Where this entity\'s recorded credits came from could not be read — Failed (HTTP 500): the transfer record could not be read'));
    expect(screen.queryByTestId('transfer-intake-sources')).toBeNull();
  });
});
