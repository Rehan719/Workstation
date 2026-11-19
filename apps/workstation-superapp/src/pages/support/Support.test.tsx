// W995 (FU-399 part 27) — the Support page, rendered against the support routes' own answers.
//
// The page takes a technical question and shows the answer with what served it, records whether it resolved anything
// only when the person says so, and shows the resolution and satisfaction records beside the help and claims panels.
// This mounts the real page against the answers its routes gave on a fresh store (Support.fixture.json, captured by
// w995_capture.py: one made-up question confirmed resolved, one rating), and has the server refuse each read and each
// action. A refusal is said with the server's reason, and a refused confirmation is never silent.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Support.fixture.json';
import { Support } from './Support';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const SLA = '/api/v1/support/sla';
const SAT = '/api/v1/support/satisfaction';
const ASK = '/api/v1/support/ask';
const CONFIRM = '/api/v1/support/confirm';

//  the page reads through axios with validateStatus () => true; the help and claims panels read through fetch
function serve(over: Record<string, Reply> = {}) {
  const page: Record<string, Reply> = {
    [`GET ${SLA}`]: ok(captured.sla), [`GET ${SAT}`]: ok(captured.satisfaction),
    [`POST ${ASK}`]: ok(captured.ask), [`POST ${CONFIRM}`]: ok(captured.confirm), [`POST ${SAT}`]: ok(captured.rate),
  };
  const answer = (key: string) => {
    const r = over[key] ?? page[key];
    if (!r) throw new Error(`not served in this test: ${key}`);
    return { status: r.status, data: r.body };
  };
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => answer(`GET ${url}`));
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => answer(`POST ${url}`));
  const panels: Record<string, unknown> = {
    '/api/v1/support/where-help-is': captured.help, '/api/v1/support/claims': captured.claims,
    '/api/v1/deliverables': captured.deliverables,
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const known = url in panels;
    return { ok: known, status: known ? 200 : 404, statusText: '', json: async () => (known ? panels[url] : { detail: 'not served' }) };
  }));
}

async function askAndAnswer() {
  fireEvent.change(screen.getByPlaceholderText('What is going wrong?'), { target: { value: 'The export button does nothing.' } });
  fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
  await screen.findByRole('button', { name: /This resolved it/ });
}

describe('Support, rendered against the support routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('a question answered and confirmed resolved is recorded as the person said', async () => {
    serve();
    render(<Support />);
    await askAndAnswer();
    fireEvent.click(screen.getByRole('button', { name: /This resolved it/ }));
    expect(await screen.findByText('Recorded as resolved — thank you.')).toBeTruthy();
    expect(screen.queryByTestId('support-confirm-error')).toBeNull();
  });

  it('a refused confirmation is said, with the server\'s reason', async () => {
    serve({ [`POST ${CONFIRM}`]: captured.confirm_refused });
    render(<Support />);
    await askAndAnswer();
    fireEvent.click(screen.getByRole('button', { name: /It did not/ }));
    await waitFor(() => expect(screen.getByTestId('support-confirm-error').textContent).toBe(
      `What you said was not recorded (HTTP 404: ${captured.confirm_refused.body.detail}).`));
    expect(screen.queryByText('Recorded as unresolved. It stays open.')).toBeNull();
  });

  it('a confirmation that could not be sent is said', async () => {
    serve();
    render(<Support />);
    await askAndAnswer();
    vi.spyOn(axios, 'post').mockImplementation(async () => { throw new Error('Network Error'); });
    fireEvent.click(screen.getByRole('button', { name: /This resolved it/ }));
    await waitFor(() => expect(screen.getByTestId('support-confirm-error').textContent).toBe(
      'What you said was not recorded — the support surface could not be reached.'));
  });

  it('a refused read of each record says the server\'s reason', async () => {
    serve({ [`GET ${SLA}`]: refused(503, 'the ticket store is locked'), [`GET ${SAT}`]: refused(502, 'the ratings did not answer') });
    render(<Support />);
    await waitFor(() => expect(screen.getAllByRole('alert').map(e => e.textContent)).toEqual(expect.arrayContaining([
      'The support record is not reporting (HTTP 503: the ticket store is locked). No figure is shown.',
      'The satisfaction record is not reporting (HTTP 502: the ratings did not answer). No figure is shown.',
    ])));
  });

  it('a refused question says the server\'s reason', async () => {
    serve({ [`POST ${ASK}`]: refused(503, 'the support surface is paused') });
    render(<Support />);
    fireEvent.change(screen.getByPlaceholderText('What is going wrong?'), { target: { value: 'Help.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    await waitFor(() => expect(screen.getAllByRole('alert').map(e => e.textContent)).toContain(
      'The support surface did not answer (HTTP 503: the support surface is paused). Nothing was recorded as an answer.'));
  });

  it('a refused rating says the store\'s own reason', async () => {
    serve({ [`POST ${SAT}`]: captured.rate_refused });
    render(<Support />);
    fireEvent.click(await screen.findByRole('button', { name: '5' }));
    await waitFor(() => expect(screen.getByTestId('support-rating-result').textContent).toBe(
      `Not recorded (HTTP 422: ${captured.rate_refused.body.detail}).`));
  });
});
