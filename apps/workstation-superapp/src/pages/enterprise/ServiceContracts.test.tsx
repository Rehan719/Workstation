// W997 (FU-399 part 29) — the service contracts panel, rendered against the contract routes' own answers.
//
// The panel lists the contracts between two entities of this platform in virtual units and moves them along: offer,
// accept, deliver, settle, or a withdrawal — the provider declines, the client cancels. This mounts the real component
// against the answers its routes gave on a fresh store (ServiceContracts.fixture.json, captured by w997_capture.py: two
// made-up entities, a contract the client cancelled and one the provider declined), and has the server refuse the list
// and an offer. A withdrawal is announced as the party the server names, and an unread list is not an empty one.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ServiceContracts.fixture.json';
import { ServiceContracts } from './ServiceContracts';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const LIST = '/api/v1/economy/contracts';
const offered = captured.offered;
const CANCEL = `/api/v1/economy/contracts/${offered.id}/cancel`;
const DECLINE = `/api/v1/economy/contracts/${offered.id}/decline`;

//  each route answers its captured reply; a list is answered in order, its last reply kept
function serve(over: Record<string, Reply | Reply[]> = {}) {
  const base: Record<string, Reply> = { [LIST]: ok(captured.contracts) };
  const queues: Record<string, Reply[]> = Object.fromEntries(
    Object.entries(over).map(([u, r]) => [u, Array.isArray(r) ? [...r] : [r]]));
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: { method?: string }) => {
    const key = init?.method === 'POST' && url === LIST ? `POST ${LIST}` : url;
    const q = queues[key];
    const r = (q ? (q.length > 1 ? q.shift()! : q[0]) : base[key]) ?? refused(404, `not served in this test: ${key}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const mount = () => render(<ServiceContracts entities={captured.entities} />);

describe('ServiceContracts, rendered against the contract routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('no contract yet: the list says none', async () => {
    serve({ [LIST]: ok(captured.contracts_empty) });
    mount();
    expect(await screen.findByText('No contracts yet. Offer one above — nothing is created until you do.')).toBeTruthy();
  });

  it('a refused read of the list is not shown as an empty one', async () => {
    serve({ [LIST]: refused(503, 'the contracts store is locked') });
    mount();
    await waitFor(() => expect(screen.getByTestId('contracts-load-error').textContent).toBe('Failed (HTTP 503): the contracts store is locked'));
    expect(screen.getByTestId('contracts-unread').textContent?.trim()).toBe('The contracts could not be read, so this is not a list of none.');
    expect(screen.queryByText(/^No contracts yet\./)).toBeNull();
  });

  it('a client\'s cancellation is announced as the client\'s', async () => {
    serve({ [LIST]: [ok(captured.contracts), ok(captured.contracts)], [CANCEL]: ok(captured.cancelled) });
    mount();
    expect(captured.cancelled.withdrawn.by).toBe('client');
    fireEvent.click(await screen.findByRole('button', { name: 'Cancel (client)' }));
    expect(await screen.findByText(
      `Contract ${captured.cancelled.status} by the client (it was ${captured.cancelled.withdrawn.from_status}) — nothing was paid.`)).toBeTruthy();
    expect(screen.queryByText(/by the provider/)).toBeNull();
  });

  it('a provider\'s decline is announced as the provider\'s', async () => {
    const declined = { ...captured.declined, id: offered.id };
    serve({ [DECLINE]: ok(declined) });
    mount();
    expect(captured.declined.withdrawn.by).toBe('provider');
    fireEvent.click(await screen.findByRole('button', { name: 'Decline (provider)' }));
    expect(await screen.findByText(
      `Contract ${declined.status} by the provider (it was ${declined.withdrawn.from_status}) — nothing was paid.`)).toBeTruthy();
  });

  it('a refused offer says the server\'s reason, and an entity is never offered a contract with itself', async () => {
    serve({ [`POST ${LIST}`]: refused(503, 'the contracts store is locked') });
    mount();
    const [a, b] = captured.entities;
    fireEvent.change(await screen.findByLabelText('Client entity'), { target: { value: a.vsb_id } });
    //  the provider list leaves the client out, as the server refuses it (captured: the offer_refused answer)
    const providers = Array.from((screen.getByLabelText('Provider entity') as HTMLSelectElement).options).map(o => o.value);
    expect(providers).not.toContain(a.vsb_id);
    expect(captured.offer_refused.status).toBe(400);
    fireEvent.change(screen.getByLabelText('Provider entity'), { target: { value: b.vsb_id } });
    fireEvent.change(screen.getByPlaceholderText('What is being commissioned?'), { target: { value: 'Forty loaves.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Offer contract' }));
    await waitFor(() => expect(screen.getByTestId('contract-action-error').textContent).toBe(
      'Failed (HTTP 503): the contracts store is locked'));
  });
});
