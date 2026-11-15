// W1070 (FU-399 part 83) — the Quran platform's donor statement, rendered against its routes' own answers.
//
// The statement reads the living roster, keeps the entities of the QEP form (qep_waqf_trust), and shows the chosen
// one's donor statement: what came in by channel, from the entity's own books, and what its waterfall WOULD
// allocate, which is not a distribution. This mounts the real panel against what each route answered on a fresh
// store (QepDonorStatement.fixture.json, captured by w1070_capture.py: two made-up entities of the QEP form
// established through Genesis, one Sponsor-a-Student contribution of 25 virtual WST and one posting written with no
// source to the first, each entity's statement, the statement route's refusal of an id no entity has, and the
// roster route's own 500). Virtual WST only. Rendering found no entity said as none before the roster was read, a
// statement said under an entity chosen after it was asked for, postings with no channel tag never said (the route
// gives them as an object, read as a number), and the entities offered by id alone in an unlabelled choice. Fixed
// here.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './QepDonorStatement.fixture.json';
import QepDonorStatement from './QepDonorStatement';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const ROSTER = '/api/v1/economy/living-vsbs';
const STATEMENT = '/api/v1/qep/contribute/statement/';
const NONE = 'No QEP entity is on the living roster, so there is no statement to show.';
const [FUNDED, UNFUNDED] = captured.vsb_ids;
const BY_ID: Record<string, Answer> = { [FUNDED]: captured.statement_first, [UNFUNDED]: captured.statement_second };
//  the QEP entities as the roster lists them; the first listed is the one shown on opening
const LISTED = captured.roster_after.body.living_vsbs.filter(v => v.entity_type === 'qep_waqf_trust');

//  each route as it answered; each read of an entity's statement takes the next answer in its list (the last stays)
function serve(plan: { roster?: Reply; statements?: Record<string, Reply[]> } = {}) {
  const lists: Record<string, Reply[]> = {};
  for (const [id, s] of Object.entries(BY_ID)) lists[id] = [...(plan.statements?.[id] ?? [s])];
  const asked: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    asked.push(url);
    let r: Reply;
    if (url === ROSTER) r = plan.roster ?? captured.roster_after;
    else if (url.startsWith(STATEMENT) && lists[url.slice(STATEMENT.length)]) {
      const l = lists[url.slice(STATEMENT.length)];
      r = l.length > 1 ? l.shift()! : l[0];
    } else r = { status: 404, body: { detail: `not served here: ${url}` } };
    const a = await r;
    if (a === 'unreachable') throw new TypeError('Failed to fetch');
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return asked;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const received = (st: typeof captured.statement_first.body) =>
  `Received: ${st.contributions_total_wst} WST in ${st.contributions_count} contribution(s) · ` +
  (Object.entries(st.contributions_by_channel_wst).map(([k, v]) => `${k} ${v}`).join(' · ') || 'no channel recorded');
const choose = (id: string) => fireEvent.change(screen.getByLabelText('QEP entity'), { target: { value: id } });

describe('QepDonorStatement, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('says no entity before the roster is read, then offers each QEP entity by its name', async () => {
    const roster = held(captured.roster_after);
    serve({ roster: roster.reply });
    render(<QepDonorStatement />);
    await waitFor(() => expect(screen.getByText('Reading the living roster…')).toBeTruthy());
    expect(screen.queryByText(NONE)).toBeNull();
    await act(async () => { roster.letGo(); });
    await waitFor(() => expect(screen.getByLabelText('QEP entity')).toBeTruthy());
    const offered = Array.from((screen.getByLabelText('QEP entity') as HTMLSelectElement).options).map(o => o.textContent);
    expect(offered).toEqual(LISTED.map(v => `${v.name} (${v.vsb_id})`));
    await waitFor(() => expect(screen.getByTestId('qep-contributions').textContent).toBe(
      received(BY_ID[LISTED[0].vsb_id].body as typeof captured.statement_first.body)));
    expect(screen.queryByText(NONE)).toBeNull();
  });

  it('says a roster it could not read with its reason, and no entity as none', async () => {
    serve({ roster: captured.roster_failed });
    render(<QepDonorStatement />);
    await waitFor(() => expect(screen.getByTestId('qep-roster-unread').textContent).toBe(
      `The living roster could not be read: Failed (HTTP 500): ${captured.roster_failed.body.detail}`));
    expect(screen.queryByText(NONE)).toBeNull();
    expect(screen.queryByText('Reading the living roster…')).toBeNull();
  });

  it('says what came in by channel, what the waterfall would allocate, and the postings with no channel tag', async () => {
    serve();
    render(<QepDonorStatement />);
    await waitFor(() => expect(screen.getByLabelText('QEP entity')).toBeTruthy());
    choose(FUNDED);
    const st = captured.statement_first.body;
    await waitFor(() => expect(screen.getByTestId('qep-contributions').textContent).toBe(received(st)));
    expect(screen.getByTestId('qep-would-allocate').textContent).toBe(
      'WOULD allocate (the waterfall\'s split of that total, NOT a distribution): '
      + Object.entries(st.would_allocate_wst).map(([k, v]) => `${k} ${v}`).join(' · '));
    expect(st.untagged_postings.count).toBe(1);
    expect(screen.getByTestId('qep-untagged').textContent).toBe(
      `${st.untagged_postings.count} posting(s), ${st.untagged_postings.total_wst} WST in all, carry no channel tag and are not counted by channel.`);
    expect(screen.queryByTestId('qep-template-fallback')).toBeNull();
  });

  it('says a statement only under the entity it was read for', async () => {
    const first = LISTED[0].vsb_id;
    const other = LISTED[1].vsb_id;
    const slow = held(BY_ID[first]);
    serve({ statements: { [first]: [slow.reply] } });
    render(<QepDonorStatement />);
    await waitFor(() => expect(screen.getByText('Reading the statement…')).toBeTruthy());
    choose(other);   // another entity chosen while the first one's statement is still out
    const theirs = received(BY_ID[other].body as typeof captured.statement_first.body);
    await waitFor(() => expect(screen.getByTestId('qep-contributions').textContent).toBe(theirs));
    await act(async () => { slow.letGo(); });
    expect(screen.getByTestId('qep-contributions').textContent).toBe(theirs);
  });

  it('says a statement the route refused by its reason', async () => {
    serve({ statements: { [LISTED[0].vsb_id]: [captured.statement_missing] } });
    render(<QepDonorStatement />);
    await waitFor(() => expect(screen.getByText(/^No statement: /).textContent).toBe(
      `No statement: Failed (HTTP 404): ${captured.statement_missing.body.detail.message}`));
    expect(screen.queryByTestId('qep-contributions')).toBeNull();
    expect(screen.queryByText('Reading the statement…')).toBeNull();
  });
});
