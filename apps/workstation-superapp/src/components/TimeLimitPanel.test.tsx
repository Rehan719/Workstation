// W1119 (FU-399 part 108) — HOW LONG A TIME LIMIT RUNS, rendered against the Law routes' own answers.
//
// The Law page's time-limit panel works out the primary limit a rule sets from a date, as arithmetic on the rule's own
// words, checked against the provision as its publisher returns it, and says what the limit does not account for and
// who to ask. No rendered test read it. This mounts the real panel against what the routes answered on a fresh store
// (TimeLimitPanel.fixture.json, captured by w1119_capture.py): the rules, a limit worked out, a provision that no longer
// holds the rule's words, and a publisher that could not be read. The provision comes from www.legislation.gov.uk when
// a person asks; a test reaches no outside host, so it was stood in as test_w875 stands it in: by its address and a
// part that holds the rule's own words, or one that does not.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './TimeLimitPanel.fixture.json';
import TimeLimitPanel from './TimeLimitPanel';

type Answer = { status: number; body: unknown };

//  the rules' read answers what the route answered (or fails as a server out of reach does); a limit asked for
//  answers what the route answered for that ask, and each ask is kept
function serve(rules: Answer | Error, worked?: Answer) {
  const posted: unknown[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const reply = (a: Answer) => ({ ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body });
    if (url !== captured.rules.url) return reply({ status: 599, body: { detail: `the test served nothing for ${url}` } });
    if (init?.method === 'POST') {
      posted.push(JSON.parse(String(init.body)));
      return reply(worked ?? { status: 599, body: { detail: 'the test served no limit' } });
    }
    if (rules instanceof Error) throw rules;
    return reply(rules);
  }));
  return posted;
}

//  a limit asked for as a person asks: the claim the rules' read put first, and the capture's date
async function ask(date: string) {
  await waitFor(() => expect((screen.getByLabelText('Claim') as HTMLSelectElement).value).toBe(captured.computed.request.rule));
  fireEvent.change(screen.getByLabelText('The date it runs from'), { target: { value: date } });
  fireEvent.click(screen.getByRole('button', { name: 'Work it out' }));
}

const said = () => [...screen.getByTestId('law-time-limit-result').querySelectorAll('p')].map(p => p.textContent);

describe('TimeLimitPanel, how long a time limit runs, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('the rules are read, and nothing is worked out until a claim and a date are given', async () => {
    const posted = serve(captured.rules);
    render(<TimeLimitPanel />);
    const panel = screen.getByTestId('law-time-limit-panel');
    expect(panel.querySelector('h4')?.textContent).toBe('How long a time limit runs');
    expect(panel.querySelector('p')?.textContent).toBe(
      'Pick the claim and the date it runs from. The provision that sets the limit is read from its publisher when you'
      + ' ask, and a date is worked out only if the provision still has the words the rule was built from.');
    await waitFor(() => expect([...(screen.getByLabelText('Claim') as HTMLSelectElement).options].map(o => o.textContent)).toEqual(
      captured.rules.body.rules.map(r => r.name)));
    const go = screen.getByRole('button', { name: 'Work it out' }) as HTMLButtonElement;
    expect(go.disabled).toBe(true);
    expect(posted).toEqual([]);
    expect(screen.queryByTestId('law-time-limit-rules-note')).toBeNull();
  });

  it('a limit worked out from the provision\'s own words, with what it does not account for, who to ask and the arithmetic', async () => {
    const a = captured.computed.body;
    const posted = serve(captured.rules, captured.computed);
    render(<TimeLimitPanel />);
    await ask(captured.computed.request.event_date);
    await waitFor(() => expect(said()[0]).toBe(`The primary limit ends at the end of ${a.last_day}.`));
    expect(posted).toEqual([captured.computed.request]);
    expect(said()).toEqual([
      `The primary limit ends at the end of ${a.last_day}.`,
      a.basis,
      `It does not account for ${a.does_not_account_for}.`,
      `Ask ${a.route.name} - ${a.route.for_what}.`,
      `${a.act}, section ${a.section} - ${a.provision_address}. ${a.arithmetic}. ${a.not_advice}`,
    ]);
    expect(screen.getByRole('link', { name: a.route.name }).getAttribute('href')).toBe(a.route.link);
    expect(screen.queryByTestId('law-time-limit-refusal')).toBeNull();
  });

  it('a provision that no longer holds the rule\'s words: no date is worked out, and the page says why', async () => {
    const g = captured.words_gone.body;
    serve(captured.rules, captured.words_gone);
    render(<TimeLimitPanel />);
    await ask(captured.words_gone.request.event_date);
    await waitFor(() => expect(said()[0]).toBe('No date is worked out.'));
    expect(g.computed).toBe(false);
    expect(said().slice(1, 3)).toEqual([g.basis, `It does not account for ${g.does_not_account_for}.`]);
  });

  it('a publisher that cannot be read: the refusal is said with who to ask, and no result is shown', async () => {
    const r = captured.refused;
    serve(captured.rules, r);
    render(<TimeLimitPanel />);
    await ask(r.request.event_date);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-refusal').textContent).toBe(
      `Failed (HTTP ${r.status}): ${r.body.detail}`));
    expect(screen.queryByTestId('law-time-limit-result')).toBeNull();
    expect(screen.getByRole('button', { name: 'Work it out' })).toBeTruthy();
  });

  it('rules that cannot be read are said with the reason, and nothing can be worked out', async () => {
    serve(new TypeError('Failed to fetch'));
    render(<TimeLimitPanel />);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-rules-note').textContent).toBe(
      'The rules could not be read (Failed — backend unreachable.), so no limit can be worked out here.'));
    expect(screen.queryByLabelText('Claim')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Work it out' })).toBeNull();
  });
});
