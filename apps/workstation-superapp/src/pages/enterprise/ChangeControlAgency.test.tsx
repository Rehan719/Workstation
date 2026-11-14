// W1043 (FU-399 part 63) — the Change Control Agency, rendered against its routes' own answers.
//
// The agency lists the change queue and takes a change request. This mounts the real page against what the routes
// answered on a fresh store with no model installed (ChangeControlAgency.fixture.json, captured by w1043_capture.py: a
// made-up LOW change with a rationale and its affected systems, held by the health gate because nothing was measured;
// the queue it joined; and the field check of a request with no title). Rendering found three defects, fixed in this
// round: the outcome closed and cleared itself a second and a half after a submission; a LOW change the health gate
// held was said only as awaiting review; and the ledger's word was folded into the outcome's own colour.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ChangeControlAgency.fixture.json';
import { ChangeControlAgency } from './ChangeControlAgency';

type Answer = { status: number; body: unknown };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

//  the queue as the route answered it, and the submission's answer as given
function serve(submitted: Answer) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/cca') return { status: 200, data: captured.queue.body };
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  return vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/cca/submit') throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (submitted.status >= 400) throw axiosRefusal(submitted.status, submitted.body);
    return { status: submitted.status, data: submitted.body };
  });
}

//  how many times the page has read the queue
const queueReads = () => vi.mocked(axios.get).mock.calls.filter(([url]) => url === '/api/v1/cca').length;

//  the page asks what the capture asked: its title, description, the LOW type it opens on, rationale and systems
async function submit() {
  render(<ChangeControlAgency />);
  const ask = captured.ask;
  fireEvent.click(await screen.findByRole('button', { name: /Submit Change Request/ }));
  fireEvent.change(screen.getByPlaceholderText('Brief change title'), { target: { value: ask.title } });
  fireEvent.change(screen.getByPlaceholderText('Describe the change and its expected impact...'), { target: { value: ask.description } });
  fireEvent.change(screen.getByTestId('cca-rationale'), { target: { value: ask.rationale } });
  fireEvent.change(screen.getByTestId('cca-systems'), { target: { value: ask.affected_systems.join(', ') } });
  fireEvent.click(screen.getByRole('button', { name: /^Submit$/ }));
}

const held = captured.submitted.body.health_gate;

describe('ChangeControlAgency, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('asks what was typed; a LOW change the health gate held says the gate\'s reason, and the outcome stays', async () => {
    const post = serve(captured.submitted);
    await submit();
    await waitFor(() => expect(screen.getByText(/^✓ Change submitted/).textContent)
      .toBe(`✓ Change submitted — the health gate did not approve it automatically: ${held.basis}.`));
    expect(post).toHaveBeenCalledWith('/api/v1/cca/submit', captured.ask);
    expect(held.verdict).toBe('held_not_decidable');
    //  the queue is read again at once: it was read again only when the outcome was taken back
    expect(queueReads()).toBe(2);
    //  and the outcome is not withdrawn before it can be read: it was, a second and a half after it was shown. The
    //  wait runs a second past that, as the form's closing animation ends well within it
    await new Promise(r => setTimeout(r, 2500));
    expect(screen.getByText(/^✓ Change submitted/).textContent).toContain('the health gate did not approve it automatically');
  }, 10_000);

  it('a decision the ledger did not record is a warning of its own, not part of the outcome', async () => {
    //  written here: a fresh store measures nothing, so no LOW change is approved there; the captured answer is re-said
    //  as an approval whose ledger append failed
    serve({ status: 200, body: { ...captured.submitted.body, status: 'approved', ueg_logged: false,
      health_gate: { ...held, verdict: 'pass', measured_health: 0.8, measured_weight: 0.6, basis: 'W1043 made up: measured' } } });
    await submit();
    await waitFor(() => expect(screen.getByTestId('cca-ledger').textContent).toBe(
      '⚠ NOT RECORDED IN THE GOVERNANCE LEDGER: the decision stands but its append to the UEG failed, so the audit trail does not carry it.'));
    expect(screen.getByTestId('cca-ledger').getAttribute('role')).toBe('alert');
    expect(screen.getByText(/^✓ Auto-approved/).textContent).not.toContain('NOT RECORDED');
  });

  it('a refused submission says the field check by its field', async () => {
    serve(captured.refused);
    await submit();
    expect(await screen.findByText('Error: title: Field required')).toBeTruthy();
    expect(screen.queryByTestId('cca-ledger')).toBeNull();
  });
});
