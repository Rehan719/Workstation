// W1081 (P5.18 clauses 1 and 2, FU-1075) — the Law page's agreements panel, rendered against its routes' own answers.
//
// The panel keeps the enterprise's own agreements as records that say only what is true of them, through the routes
// of agentic_core/api/agreements.py (W1080). This mounts the real panel against what each route answered on a fresh
// store (AgreementsPanel.fixture.json, captured by w1081_capture.py): the listing with sign-in off, which keeps
// nothing; then, signed in as a made-up person, the empty listings, a party refused for a date not yet come, a
// registered body and a person entered, a draft refused for naming one party twice, the draft, a review, an approval,
// a change to the text that ends it, an approval of the old text refused, the second approval, a signatory, the
// execution, that it is in force, an end refused for its date and the end, and the listing's own 503. Every party,
// entity and text is made up, and nothing is legal advice.
// W1086 (P5.18 clauses 3 and 7): an obligation refused for naming one party on both sides, the obligation, a second,
// a person's confirmation and a second one refused, and the notice period as the text states it.
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './AgreementsPanel.fixture.json';
import AgreementsPanel from './AgreementsPanel';

//  the routes' answers, read as the routes gave them (each fact holds the fields of its own kind)
const C: any = captured;

type Answer = { status: number; body: any };
type Reply = Answer | Promise<Answer>;
type Plan = Partial<Record<'list' | 'parties' | 'party' | 'draft' | 'read' | 'review' | 'approve' | 'text' | 'executed'
  | 'in_force' | 'ended' | 'signatories' | 'obligation' | 'confirm' | 'notice', Reply[]>>;
const BASE = '/api/v1/agreements';
const DRAFTED = C.draft.body;
const AID = DRAFTED.id;
const BODY = C.party_body.body.party;
const PERSON = C.party_person.body.party;

//  each route as it answered; each call takes the next answer in its list, and the last one stays
function serve(plan: Plan) {
  const lists: Record<string, Reply[]> = Object.fromEntries(Object.entries(plan).map(([k, v]) => [k, [...(v ?? [])]]));
  const next = (k: string): Reply => {
    const l = lists[k];
    if (!l || l.length === 0) return { status: 404, body: { detail: `not served in this test: ${k}` } };
    return l.length > 1 ? l.shift()! : l[0];
  };
  const sent: { url: string; method: string; body?: any }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    sent.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    const act = url.startsWith(`${BASE}/${AID}/`) ? url.slice(`${BASE}/${AID}/`.length) : '';
    const key = method === 'GET' && url === BASE ? 'list'
      : method === 'GET' && url === `${BASE}/parties` ? 'parties'
        : method === 'POST' && url === `${BASE}/parties` ? 'party'
          : method === 'POST' && url === BASE ? 'draft'
            : method === 'GET' && url === `${BASE}/${AID}` ? 'read'
              : method === 'PUT' && act === 'text' ? 'text'
                : method === 'POST' && act === 'in-force' ? 'in_force'
                  : method === 'POST' && act === 'obligations' ? 'obligation'
                    : method === 'POST' && /^obligations\/[^/]+\/confirm$/.test(act) ? 'confirm'
                      : method === 'POST' && act === 'notice' ? 'notice'
                  : method === 'POST' && ['review', 'approve', 'executed', 'ended', 'signatories'].includes(act) ? act
                    : `${method} ${url}`;
    const a = await next(key);
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return sent;
}

//  an answer held back until the test lets it go
function held(a: Answer) {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const type = (label: string, value: string) => fireEvent.change(screen.getByLabelText(label), { target: { value } });
const press = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', { name }));
const failed = (a: Answer) => `Failed (HTTP ${a.status}): ${a.body.detail}`;
const facts = () => screen.getAllByTestId('agreement-fact').map(li => li.textContent);
const short = (h: string) => h.replace(/^sha256:/, '').slice(0, 12);

//  the record opened from the listing, then each answer of the plan
async function opened(plan: Plan, read: Answer) {
  const sent = serve({ list: [C.list_one], parties: [C.parties_two], read: [read], ...plan });
  render(<AgreementsPanel />);
  fireEvent.click(await screen.findByRole('button', { name: /^W1081 Made-up Supply - version 1/ }));
  await waitFor(() => expect(screen.getByTestId('agreement-current').textContent).toBe(
    `The text as it stands is version ${read.body.current.version} (${read.body.current.hash}).`));
  return sent;
}

describe('AgreementsPanel, rendered against its routes\' own answers (made-up parties)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('with sign-in off says nothing is kept by the route\'s reason, offers no form, and lists the service contracts apart', async () => {
    serve({ list: [C.list_off], parties: [C.parties_off] });
    render(<AgreementsPanel />);
    await waitFor(() => expect(screen.getByTestId('agreements-not-kept').textContent).toBe(C.list_off.body.not_kept_because));
    expect(screen.queryByTestId('agreements-party-form')).toBeNull();
    expect(screen.queryByTestId('agreements-draft-form')).toBeNull();
    expect(screen.queryByTestId('agreements-none')).toBeNull();
    const apart = screen.getByTestId('agreements-service-contracts');
    expect(within(apart).getByText(C.list_off.body.internal_service_contracts.what_these_are)).toBeTruthy();
  });

  it('says no party and no agreement only once each is read, and offers a draft only with two parties', async () => {
    const list = held(C.list_empty);
    const parties = held(C.parties_empty);
    serve({ list: [list.reply], parties: [parties.reply] });
    render(<AgreementsPanel />);
    expect(screen.getByText('Reading the agreement records…')).toBeTruthy();
    await act(async () => { list.letGo(); });
    await waitFor(() => expect(screen.getByTestId('agreements-none').textContent).toBe('No agreement is recorded yet.'));
    expect(screen.queryByTestId('agreements-no-parties')).toBeNull();   // the parties are not read yet
    expect(screen.getByText('Reading the parties…')).toBeTruthy();
    await act(async () => { parties.letGo(); });
    await waitFor(() => expect(screen.getByTestId('agreements-no-parties').textContent).toBe('No party is entered yet.'));
    expect(screen.getByTestId('agreements-draft-needs-parties')).toBeTruthy();
    expect(screen.queryByTestId('agreements-draft-form')).toBeNull();
    expect(screen.getByTestId('agreements-not-advice').textContent).toBe(C.list_empty.body.not_legal_advice);
    expect(C.list_empty.body.internal_service_contracts.contracts).toEqual([]);
    expect(within(screen.getByTestId('agreements-service-contracts')).getByText('None is recorded.')).toBeTruthy();
  });

  it('enters a party with where and when it was read; a refused entry says the route\'s reason beside its button', async () => {
    const sent = serve({ list: [C.list_empty], parties: [C.parties_empty, C.parties_two], party: [C.party_refused, C.party_body] });
    render(<AgreementsPanel />);
    await screen.findByTestId('agreements-no-parties');
    type('Party name', BODY.name);
    type('Register', BODY.registered_on);
    type('Number on the register', BODY.registered_number);
    type('Where it was read', BODY.read_from);
    type('When it was read', '2099-01-01');
    press('Enter this party');
    await waitFor(() => expect(screen.getByTestId('agreements-party-error').textContent).toBe(
      `The party was not entered: ${failed(C.party_refused)}`));
    type('When it was read', BODY.read_on);
    press('Enter this party');
    await waitFor(() => expect(screen.getAllByTestId('agreement-party')).toHaveLength(2));
    expect(screen.queryByTestId('agreements-party-error')).toBeNull();
    const rows = screen.getAllByTestId('agreement-party').map(li => li.textContent);
    expect(rows).toContain(`${BODY.name} - a registered body, on ${BODY.registered_on} as ${BODY.registered_number}${BODY.basis}`);
    expect(rows).toContain(`${PERSON.name} - a person${PERSON.basis}`);
    expect(BODY.basis).toMatch(/This platform did not check it against any register or document\.$/);
    const posts = sent.filter(s => s.method === 'POST');
    expect(posts.map(s => s.body)).toEqual([
      { kind: 'registered_body', name: BODY.name, read_from: BODY.read_from, read_on: '2099-01-01',
        registered_on: BODY.registered_on, registered_number: BODY.registered_number },
      { kind: 'registered_body', name: BODY.name, read_from: BODY.read_from, read_on: BODY.read_on,
        registered_on: BODY.registered_on, registered_number: BODY.registered_number }]);
  });

  it('drafts an agreement on party records only, and its six facts stay apart: drafted, then each said as not recorded', async () => {
    const sent = serve({ list: [C.list_empty, C.list_one], parties: [C.parties_two], draft: [C.draft_refused, C.draft] });
    render(<AgreementsPanel />);
    await screen.findByTestId('agreements-draft-form');
    //  a party is offered only from the party records
    const offered = within(screen.getByLabelText('Party 1')).getAllByRole('option').map(o => (o as HTMLOptionElement).value);
    expect(offered).toEqual(['', ...C.parties_two.body.parties.map((x: any) => x.id)]);
    type('Agreement title', DRAFTED.title);
    type('Agreement text', DRAFTED.versions[0].text);
    type('Party 1', BODY.id); type('Role of party 1', 'supplier');
    type('Party 2', BODY.id); type('Role of party 2', 'customer');
    press('Draft this agreement');
    await waitFor(() => expect(screen.getByTestId('agreements-draft-error').textContent).toBe(
      `The agreement was not drafted: ${failed(C.draft_refused)}`));
    type('Party 2', PERSON.id);
    press('Draft this agreement');
    await waitFor(() => expect(screen.getByTestId('agreement-current').textContent).toBe(
      `The text as it stands is version 1 (${DRAFTED.current.hash}).`));
    const d = DRAFTED.facts[0];
    expect(facts()).toEqual([
      `Drafted version 1 (${short(d.hash)}) - by ${d.by} at ${d.at}`,
      ...DRAFTED.facts.slice(1).map((f: any) => `${({ reviewed: 'Reviewed', approved: 'Approved', executed: 'Executed', in_force: 'In force', ended: 'Ended' } as any)[f.state]} ${f.said}`),
    ]);
    await waitFor(() => expect(screen.getAllByTestId('agreement-row')).toHaveLength(1));
    //  the internal service contract is listed apart, never among the agreements
    const contracts = C.list_one.body.internal_service_contracts.contracts;
    expect(contracts).toHaveLength(1);
    expect(screen.getAllByTestId('agreements-service-contract').map(li => li.textContent)).toEqual(
      contracts.map((c: any) => `${c.id}: ${c.client_vsb} commissions ${c.provider_vsb} for ${c.price_wst} WST (virtual), ${c.status}`));
    expect(screen.getAllByTestId('agreement-row').map(li => li.textContent).join(' ')).not.toContain(contracts[0].id);
    expect(sent.filter(s => s.method === 'POST').map(s => s.body)).toEqual([
      { title: DRAFTED.title, text: DRAFTED.versions[0].text, parties: [{ party_id: BODY.id, role: 'supplier' }, { party_id: BODY.id, role: 'customer' }] },
      { title: DRAFTED.title, text: DRAFTED.versions[0].text, parties: [{ party_id: BODY.id, role: 'supplier' }, { party_id: PERSON.id, role: 'customer' }] }]);
  });

  it('an approval names its version; a change to the text ends it and says why; a refused approval is said beside its button', async () => {
    const sent = await opened({ approve: [C.approve, C.approve_old], text: [C.text] }, C.read_drafted);
    const h1 = DRAFTED.current.hash;
    press(`Approve version 1 (${short(h1)})`);
    await waitFor(() => expect(facts()[2]).toBe(`Approved version 1 (${short(h1)}) - by ${C.approve.body.facts[2].by} at ${C.approve.body.facts[2].at}`));
    type('The text', C.text.body.versions[1].text);
    press('Save as version 2');
    const h2 = C.text.body.current.hash;
    await waitFor(() => expect(screen.getByTestId('agreement-current').textContent).toBe(`The text as it stands is version 2 (${h2}).`));
    const e = C.text.body.facts[2].ended_approvals[0];
    expect(screen.getByTestId('agreement-approval-ended').textContent).toBe(
      `The approval of version 1 by ${e.by} ended at ${e.ended_at}: ${e.ended_because}.`);
    expect(facts()[2]).toContain(C.text.body.facts[2].said);
    press(`Approve version 2 (${short(h2)})`);
    await waitFor(() => expect(screen.getByTestId('agreement-error-approve').textContent).toBe(`Not recorded: ${failed(C.approve_old)}`));
    const writes = sent.filter(s => s.method !== 'GET').map(s => [s.method, s.url.slice(BASE.length), s.body]);
    expect(writes).toEqual([
      ['POST', `/${AID}/approve`, { hash: h1 }],
      ['PUT', `/${AID}/text`, { text: C.text.body.versions[1].text, from_hash: h1 }],
      ['POST', `/${AID}/approve`, { hash: h2 }]]);
  });

  it('an execution is the person\'s entry, and the law\'s formalities are not stated; the text is then not offered for change', async () => {
    const sent = await opened({ executed: [C.executed] }, C.read_drafted);
    type('Date it was signed', C.executed.body.facts[3].signed_on);
    type('Evidence that it was executed', C.executed.body.facts[3].evidence);
    type('Formalities met', `${C.executed.body.facts[3].formalities_met[0]}\n\n`);
    press('Record the execution of version 1');
    const x = C.executed.body.facts[3];
    await waitFor(() => expect(facts()[3]).toContain(
      `Executed version ${x.version} (${short(x.hash)}), signed on ${x.signed_on} - by ${x.entered_by} at ${x.entered_at}`));
    expect(screen.getByTestId('agreement-execution-evidence').textContent).toBe(
      `Evidence, as entered: ${x.evidence}. Formalities met, as entered: ${x.formalities_met.join('; ')}.`);
    expect(screen.getByTestId('agreement-law-basis').textContent).toBe(x.law_basis);
    expect(x.formalities_the_law_requires).toBeNull();
    expect(screen.getByTestId('agreement-text-fixed')).toBeTruthy();
    expect(screen.queryByLabelText('The text')).toBeNull();
    expect(screen.queryByTestId('agreement-execution-form')).toBeNull();
    expect(sent.find(s => s.url.endsWith('/executed'))!.body).toEqual({
      hash: DRAFTED.current.hash, signed_on: x.signed_on, evidence: x.evidence, formalities_met: x.formalities_met });
  });

  it('a signatory\'s authority is said as stated and by whom, and as not verified', async () => {
    await opened({ signatories: [C.signatory] }, C.read_drafted);
    const s = C.signatory.body.parties[0].signatories[0];
    type('Signs for', BODY.id);
    type('Signatory name', s.name);
    type('Signs as', s.capacity);
    type('Authority, as stated', s.authority_as_stated);
    type('Stated by', s.stated_by);
    press('Record this signatory');
    await waitFor(() => expect(screen.getByTestId('agreement-signatory').textContent).toBe(
      `Signs as ${s.capacity}: ${s.name}. Authority, as stated by ${s.stated_by}: ${s.authority_as_stated}. ${s.basis}`));
    expect(s.verified_by_this_platform).toBe(false);
  });

  it('an end dated before the signing is refused beside its button; once ended, nothing more is offered', async () => {
    await opened({ ended: [C.ended_refused, C.ended] }, C.in_force);
    type('Date it ended', '2000-01-01');
    type('How it ended', 'w1081');
    press('Record its end');
    await waitFor(() => expect(screen.getByTestId('agreement-error-ended').textContent).toBe(`Not recorded: ${failed(C.ended_refused)}`));
    press('Record its end');
    await waitFor(() => expect(screen.getByTestId('agreement-ended-note')).toBeTruthy());
    const e = C.ended.body.facts[5];
    expect(facts()[5]).toBe(`Ended on ${e.on}: ${e.how} - by ${e.entered_by} at ${e.entered_at}`);
    expect(screen.queryByRole('button', { name: /^Approve version/ })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Record its end' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Record this obligation' })).toBeNull();   // W1086 - nothing more is offered
  });

  it('an obligation is entered from its clause, refused beside its button when it is not one, and confirmed by a person', async () => {
    const sent = await opened({ obligation: [C.obligation_refused, C.obligation], confirm: [C.confirmed] }, C.in_force);
    expect(screen.getByTestId('agreement-no-obligations').textContent).toBe('No obligation is entered yet.');
    expect(screen.getByTestId('agreement-date-basis').textContent).toBe(C.in_force.body.date_basis);
    const o = C.obligation.body.obligations[0];
    type('Owed by', BODY.id);
    type('Owed to', BODY.id);
    type('What is owed', o.what);
    type('The clause it was read from', o.clause);
    type('It falls due on', o.due_on);
    press('Record this obligation');
    await waitFor(() => expect(screen.getByTestId('agreement-error-obligation').textContent).toBe(`Not recorded: ${failed(C.obligation_refused)}`));
    type('Owed to', PERSON.id);
    press('Record this obligation');
    await waitFor(() => expect(screen.getAllByTestId('agreement-obligation')).toHaveLength(1));
    expect(screen.getByTestId('agreement-obligation').textContent).toContain(
      `${BODY.name} owes ${PERSON.name}: ${o.what} (${o.clause}). Falls due on ${o.due_on}, as entered. ${o.confirmed_said}`);
    press(`Confirm it was read from ${o.clause}`);
    const c = C.confirmed.body.obligations[0].confirmed;
    await waitFor(() => expect(screen.getAllByTestId('agreement-obligation')[0].textContent).toContain(`Confirmed by ${c.by} at ${c.at}.`));
    expect(screen.queryByRole('button', { name: `Confirm it was read from ${o.clause}` })).toBeNull();
    const posts = sent.filter(s => s.method === 'POST').map(s => [s.url.slice(BASE.length), s.body]);
    expect(posts).toEqual([
      [`/${AID}/obligations`, { owed_by: BODY.id, owed_to: BODY.id, what: o.what, clause: o.clause, due_on: o.due_on }],
      [`/${AID}/obligations`, { owed_by: BODY.id, owed_to: PERSON.id, what: o.what, clause: o.clause, due_on: o.due_on }],
      [`/${AID}/obligations/${o.id}/confirm`, {}]]);
  });

  it('the notice period is said as not known until it is entered, then as entered with its clause; the text is kept as data', async () => {
    await opened({ notice: [C.notice] }, C.in_force);
    expect(screen.getByTestId('agreement-notice-said').textContent).toBe(C.in_force.body.notice.said);
    expect(C.in_force.body.notice.known).toBe(false);
    const tk = C.in_force.body.text_kept;
    expect(screen.getByTestId('agreement-text-kept').textContent).toBe(`${tk.chars} of the ${tk.of} characters of the text are kept. ${tk.basis}`);
    const n = C.notice.body.notice;
    type('The notice period, as stated', n.as_stated);
    type('The notice clause', n.clause);
    press('Record the notice period');
    await waitFor(() => expect(screen.getByTestId('agreement-notice-said').textContent).toBe(
      `Notice period: ${n.as_stated} (${n.clause}), entered by ${n.entered_by} at ${n.entered_at}.`));
  });

  // W1103 (FU-399 part 92) - each action's refusal is said beside its own button, in the route's own words, and
  // nothing is said in any other action's place
  const ERRORS = ['review', 'approve', 'text', 'executed', 'in-force', 'ended', 'signatory', 'obligation', 'notice', 'confirm'];
  const REFUSALS: [string, string, Answer, Answer, () => void][] = [
    ['review', 'review', C.review_refused, C.read_drafted, () => press(/^Record a review of version 1/)],
    ['text', 'text', C.text_refused, C.read_drafted, () => { type('The text', 'w1103 a changed made-up text'); press(/^Save as version 2/); }],
    ['executed', 'executed', C.executed_refused, C.read_drafted, () => {
      type('Date it was signed', C.captured_on); type('Evidence that it was executed', 'w1103 made-up evidence');
      type('Formalities met', 'w1103 signed, as stated'); press(/^Record the execution of version 1/); }],
    ['in-force', 'in_force', C.in_force_refused, C.read_drafted, () => {
      type('In force from', C.captured_on); type('What puts it in force', 'w1103 made up'); press('Record that it is in force'); }],
    ['signatory', 'signatories', C.signatory_refused, C.read_drafted, () => {
      type('Signs for', C.read_drafted.body.parties[0].party_id); type('Signatory name', 'w1103 made-up name');
      type('Signs as', 'w1103 as stated'); type('Authority, as stated', 'w1103 as stated'); type('Stated by', 'w1103 made up');
      press('Record this signatory'); }],
    ['notice', 'notice', C.notice_refused, C.read_drafted, () => {
      type('The notice period, as stated', 'w1103 sixty days'); type('The notice clause', 'clause 9'); press('Record the notice period'); }],
    ['confirm', 'confirm', C.confirm_again, C.obligation, () => press('Confirm it was read from clause 3')],
  ];
  for (const [id, key, refusal, read, doIt] of REFUSALS) {
    it(`a refused ${id} is said beside its own button, in the route's words, and in no other place`, async () => {
      await opened({ [key]: [refusal] } as Plan, read);
      doIt();
      await waitFor(() => expect(screen.getByTestId(`agreement-error-${id}`).textContent).toBe(`Not recorded: ${failed(refusal)}`));
      for (const other of ERRORS.filter(e => e !== id)) expect(screen.queryByTestId(`agreement-error-${other}`)).toBeNull();
    });
  }

  // W1103 - what was typed for one agreement is never offered for the next one opened
  it('a form typed for one agreement is empty when another is opened', async () => {
    const A2 = C.second_draft_a.body.id;
    const B2 = C.second_draft_b.body.id;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const plan: any = { list: [C.second_list], parties: [C.second_parties],
                        [`GET ${BASE}/${A2}`]: [C.second_read_a], [`GET ${BASE}/${B2}`]: [C.second_read_b] };
    serve(plan);
    render(<AgreementsPanel />);
    fireEvent.click(await screen.findByRole('button', { name: /^W1103 Made-up First - version 1/ }));
    await waitFor(() => expect(screen.getByTestId('agreement-current').textContent).toContain(C.second_read_a.body.current.hash));
    const typed = ['Review note', 'Signatory name', 'Evidence that it was executed', 'What puts it in force', 'The notice clause'];
    for (const label of typed) type(label, `w1103 typed for the first agreement: ${label}`);
    fireEvent.click(screen.getByRole('button', { name: /^W1103 Made-up Second - version 1/ }));
    await waitFor(() => expect(screen.getByTestId('agreement-current').textContent).toContain(C.second_read_b.body.current.hash));
    for (const label of typed) expect((screen.getByLabelText(label) as HTMLInputElement).value).toBe('');
  });

  it('a failed read of the records says its reason, and says no record as none', async () => {
    serve({ list: [C.list_unread], parties: [C.parties_two] });
    render(<AgreementsPanel />);
    await waitFor(() => expect(screen.getByTestId('agreements-unread').textContent).toBe(
      `The agreement records could not be read (${failed(C.list_unread)}), so none is shown.`));
    expect(screen.queryByTestId('agreements-none')).toBeNull();
    expect(screen.queryByTestId('agreements-party-form')).toBeNull();
  });
});
