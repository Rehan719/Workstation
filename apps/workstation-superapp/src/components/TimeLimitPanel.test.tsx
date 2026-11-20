// W1119 (FU-399 part 108) — HOW LONG A TIME LIMIT RUNS, rendered against the Law routes' own answers.
//
// The Law page's time-limit panel works out the primary limit a rule sets from a date, as arithmetic on the rule's own
// words, checked against the provision as its publisher returns it, and says what the limit does not account for and
// who to ask. No rendered test read it. This mounts the real panel against what the routes answered on a fresh store
// (TimeLimitPanel.fixture.json, captured by w1119_capture.py): the rules, a limit worked out, a provision that no longer
// holds the rule's words, and a publisher that could not be read. The provision comes from www.legislation.gov.uk when
// a person asks; a test reaches no outside host, so it was stood in as test_w875 stands it in: by its address and a
// part that holds the rule's own words, or one that does not.
//
// W1161 (P5.11 clause 2) — a person says where the claim is, and a claim with no rule here, or one whose rule is not
// for that nation, is answered that a time limit may still apply, with where to ask today for that nation. Two more
// answers are captured (w1161_capture.py): a claim not listed here, in Scotland, and an unfair dismissal claim in
// Northern Ireland, which no rule here is for. Neither reads a provision.
//
// W1162 (P5.11 clause 2) — each answer says the rule's sources, the day each was read and the round that read it; two
// more answers are captured (w1162_capture.py): a claim from 31 August, whose same date three months on does not exist,
// worked out to the earlier of the two days it could end on, and the same limit asked ninety-one days after its sources
// were read, each said as not recently checked.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './TimeLimitPanel.fixture.json';
import TimeLimitPanel from './TimeLimitPanel';

type Answer = { status: number; body: unknown };
type Ask = { rule: string; event_date: string; nation: string };

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

//  a limit asked for as a person asks: where the claim is, the claim, and its date when the claim is one with a rule
async function ask(request: Ask) {
  await waitFor(() => expect((screen.getByLabelText('Claim') as HTMLSelectElement).value).toBe(captured.rules.body.rules[0].id));
  fireEvent.change(screen.getByLabelText('Where the claim is'), { target: { value: request.nation } });
  fireEvent.change(screen.getByLabelText('Claim'), { target: { value: request.rule } });
  if (request.event_date) fireEvent.change(screen.getByLabelText('The date it runs from'), { target: { value: request.event_date } });
  fireEvent.click(screen.getByRole('button', { name: 'Work it out' }));
}

//  what the panel says of a source: as read, with its day and the round that read it, or as not checked
type Src = { id: string; read: boolean; name?: string; checked: string; read_by?: string | null };
const sourceSaid = (s: Src) => (s.read ? `${s.name}, ${s.checked}${s.read_by ? ` (${s.read_by.split(',')[0]})` : ''}` : `${s.id}: ${s.checked}`);

const said = () => [...screen.getByTestId('law-time-limit-result').querySelectorAll('p')].map(p => p.textContent);
const go = () => screen.getByRole('button', { name: 'Work it out' }) as HTMLButtonElement;

describe('TimeLimitPanel, how long a time limit runs, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('the rules are read, and nothing is worked out until where the claim is, the claim and a date are given', async () => {
    const posted = serve(captured.rules);
    render(<TimeLimitPanel />);
    const panel = screen.getByTestId('law-time-limit-panel');
    expect(panel.querySelector('h4')?.textContent).toBe('How long a time limit runs');
    expect(panel.querySelector('p')?.textContent).toBe(
      'Pick where the claim is, the claim and the date it runs from. The provision that sets the limit is read from its'
      + ' publisher when you ask, and a date is worked out only if the provision still has the words the rule was built'
      + ' from. If no rule here is for your claim, or for where it is, you are told where to ask today.');
    await waitFor(() => expect([...(screen.getByLabelText('Claim') as HTMLSelectElement).options].map(o => o.textContent)).toEqual(
      [...captured.rules.body.rules.map(r => r.name), captured.rules.body.not_listed.name]));
    expect([...(screen.getByLabelText('Where the claim is') as HTMLSelectElement).options].map(o => o.textContent)).toEqual(
      ['Where the claim is', ...captured.rules.body.nations]);
    expect(go().disabled).toBe(true);
    //  a nation and a claim with a rule still need the date it runs from...
    fireEvent.change(screen.getByLabelText('Where the claim is'), { target: { value: captured.rules.body.nations[0] } });
    expect(go().disabled).toBe(true);
    //  ...and a claim not listed needs none
    fireEvent.change(screen.getByLabelText('Claim'), { target: { value: captured.rules.body.not_listed.id } });
    expect(go().disabled).toBe(false);
    expect(posted).toEqual([]);
    expect(screen.queryByTestId('law-time-limit-rules-note')).toBeNull();
  });

  it('a limit worked out from the provision\'s own words, with what it does not account for, who to ask and the arithmetic', async () => {
    const a = captured.computed.body;
    const posted = serve(captured.rules, captured.computed);
    render(<TimeLimitPanel />);
    await ask(captured.computed.request);
    await waitFor(() => expect(said()[0]).toBe(`The primary limit ends at the end of ${a.last_day}.`));
    expect(posted).toEqual([captured.computed.request]);
    expect(said()).toEqual([
      `The primary limit ends at the end of ${a.last_day}.`,
      a.basis,
      `It does not account for ${a.does_not_account_for}.`,
      `Ask ${a.route.name} - ${a.route.for_what}.`,
      `Read: ${a.sources.map(sourceSaid).join('; ')}.`,
      `${a.act}, ${a.part} ${a.section} - ${a.provision_address}. ${a.arithmetic}. ${a.not_advice}`,
    ]);
    expect(screen.getByRole('link', { name: a.route.name }).getAttribute('href')).toBe(a.route.link);
    expect(screen.queryByTestId('law-time-limit-refusal')).toBeNull();
    expect(screen.queryByTestId('law-time-limit-no-rule')).toBeNull();
  });

  it('a provision that no longer holds the rule\'s words: no date is worked out, and the page says why', async () => {
    const g = captured.words_gone.body;
    serve(captured.rules, captured.words_gone);
    render(<TimeLimitPanel />);
    await ask(captured.words_gone.request);
    await waitFor(() => expect(said()[0]).toBe('No date is worked out.'));
    expect(g.computed).toBe(false);
    expect(said().slice(1, 3)).toEqual([g.basis, `It does not account for ${g.does_not_account_for}.`]);
  });

  it('a month with no such day: the earlier of the two days the period could end on, said as unsettled', async () => {
    const u = captured.unsettled;
    serve(captured.rules, u);
    render(<TimeLimitPanel />);
    await ask(u.request);
    await waitFor(() => expect(said()[0]).toBe(
      `The primary limit ends at the end of ${u.body.last_day}, the earlier of the two days the provision leaves unsettled.`));
    expect(u.body.settled).toBe(false);
    expect(said()[1]).toBe(u.body.basis);
    expect(u.body.basis).toContain('The provision does not settle how such a period ends');
  });

  it('a source read more than ninety days ago is said as not recently checked', async () => {
    const s = captured.stale;
    serve(captured.rules, s);
    render(<TimeLimitPanel />);
    await ask(s.request);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-sources').textContent).toBe(
      `Read: ${s.body.sources.map(sourceSaid).join('; ')}.`));
    expect(s.body.sources.length).toBeGreaterThan(0);
    expect(s.body.sources.every(x => x.checked.startsWith('NOT RECENTLY CHECKED'))).toBe(true);
  });

  it('a publisher that cannot be read: the refusal is said with who to ask, and no result is shown', async () => {
    const r = captured.refused;
    serve(captured.rules, r);
    render(<TimeLimitPanel />);
    await ask(r.request);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-refusal').textContent).toBe(
      `Failed (HTTP ${r.status}): ${r.body.detail}`));
    expect(screen.queryByTestId('law-time-limit-result')).toBeNull();
    expect(screen.getByRole('button', { name: 'Work it out' })).toBeTruthy();
  });

  it('a claim not listed here: a time limit may still apply, the rules there are and where to ask today, for that nation', async () => {
    const n = captured.not_listed;
    const posted = serve(captured.rules, n);
    render(<TimeLimitPanel />);
    await ask(n.request);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-no-rule').querySelector('p')?.textContent).toBe('No date is worked out.'));
    expect(posted).toEqual([n.request]);
    const box = screen.getByTestId('law-time-limit-no-rule');
    expect(box.querySelectorAll('p')[1].textContent).toBe(n.body.basis);
    expect(n.body.basis).toContain('A time limit may still apply: ask today.');
    expect(screen.getByTestId('law-time-limit-rules-here').textContent).toBe(
      `The rules here for a claim in ${n.request.nation}: ${n.body.rules_for_this_nation.map(r => r.name).join('; ')}.`);
    const lists = screen.getAllByTestId('law-time-limit-where-to-ask');
    expect(lists.map(l => l.querySelector('p')?.textContent)).toEqual([`Where to ask today, for a claim in ${n.request.nation}:`]);
    const places = n.body.where_to_ask[n.request.nation as keyof typeof n.body.where_to_ask];
    expect([...lists[0].querySelectorAll('li')].map(li => li.textContent)).toEqual(places.map(p => `${p.name} - ${p.for_what}.`));
    expect([...lists[0].querySelectorAll('a')].map(x => x.getAttribute('href'))).toEqual(places.map(p => p.link));
    const o = n.body.named_on;
    expect(screen.getByTestId('law-time-limit-named-on').textContent).toBe(
      `Each place is named on ${o.publisher}'s guide ${o.name}, ${o.checked}. ${o.own_sites} ${n.body.not_advice}`);
    expect(screen.getByRole('link', { name: o.name }).getAttribute('href')).toBe(o.page);
    expect(screen.queryByTestId('law-time-limit-result')).toBeNull();
  });

  it('a claim in a nation no rule here is for: a route and not a rule, and no rule listed for it', async () => {
    const x = captured.not_this_nation;
    const posted = serve(captured.rules, x);
    render(<TimeLimitPanel />);
    await ask(x.request);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-no-rule').querySelectorAll('p')[1]?.textContent).toBe(x.body.basis));
    expect(posted).toEqual([x.request]);
    expect(x.body.rules_for_this_nation).toEqual([]);
    expect(screen.queryByTestId('law-time-limit-rules-here')).toBeNull();
    const lists = screen.getAllByTestId('law-time-limit-where-to-ask');
    const places = x.body.where_to_ask[x.request.nation as keyof typeof x.body.where_to_ask];
    expect(lists.length).toBe(1);
    expect([...lists[0].querySelectorAll('a')].map(a => a.getAttribute('href'))).toEqual(places.map(p => p.link));
    expect(screen.queryByTestId('law-time-limit-result')).toBeNull();
  });

  it('rules that cannot be read are said with the reason, and nothing can be worked out', async () => {
    serve(new TypeError('Failed to fetch'));
    render(<TimeLimitPanel />);
    await waitFor(() => expect(screen.getByTestId('law-time-limit-rules-note').textContent).toBe(
      'The rules could not be read (Failed — backend unreachable.), so no limit can be worked out here.'));
    expect(screen.queryByLabelText('Claim')).toBeNull();
    expect(screen.queryByLabelText('Where the claim is')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Work it out' })).toBeNull();
  });
});
