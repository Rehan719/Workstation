// W1083 (P5.19 clauses 1, 2, 4 and 5, FU-1078) — the Law page's assets panel, rendered against its routes' own answers.
//
// The panel keeps physical assets as records and evidence, through the routes of agentic_core/api/assets.py (W1082),
// with owners, possessors and the agreements they are held under drawn from the party and agreement records (W1080).
// This mounts the real panel against what each route answered on a fresh store (AssetsPanel.fixture.json, captured
// by w1083_capture.py): the listing with sign-in off, which keeps nothing; then, signed in as a made-up person, the
// parties and a made-up lease, the empty listing, an asset refused for naming no agreement, the asset, a declaration of
// readiness refused for naming nobody, evidence for four facts (the insurance already lapsed), a declaration of
// readiness, the asset read with the date moved on (its risk assessment lapsed, the declaration withdrawn), and each
// listing's own 503. Every party, asset and piece of evidence is made up, and nothing is judged or connected.
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './AssetsPanel.fixture.json';
import AssetsPanel from './AssetsPanel';

//  the routes' answers, read as the routes gave them (each fact holds the fields of its own kind)
const C: any = captured;
type Answer = { status: number; body: any };
type Reply = Answer | Promise<Answer>;
type Plan = Partial<Record<'list' | 'parties' | 'agreements' | 'asset' | 'read' | 'evidence', Reply[]>>;
const BASE = '/api/v1/assets';
const ASSET = C.asset.body;
const AID = ASSET.id;

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
    const key = method === 'GET' && url === BASE ? 'list'
      : method === 'GET' && url === '/api/v1/agreements/parties' ? 'parties'
        : method === 'GET' && url === '/api/v1/agreements' ? 'agreements'
          : method === 'POST' && url === BASE ? 'asset'
            : method === 'GET' && url === `${BASE}/${AID}` ? 'read'
              : method === 'POST' && url === `${BASE}/${AID}/evidence` ? 'evidence'
                : `${method} ${url}`;
    const a = await next(key);
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body } as unknown as Response;
  }));
  return sent;
}

function held(a: Answer) {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const type = (label: string, value: string) => fireEvent.change(screen.getByLabelText(label), { target: { value } });
const press = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', { name }));
const failed = (a: Answer) => `Failed (HTTP ${a.status}): ${a.body.detail}`;
const facts = () => screen.getAllByTestId('asset-fact').map(li => li.textContent);
const line = (e: any) => `${e.evidence}${e.named_person ? `, declared by ${e.named_person}` : ''} - attached by ${e.attached_by} at ${e.attached_at}, lapses on ${e.lapses_on}: ${e.state}`;

//  the asset opened from the listing, then each answer of the plan
async function opened(plan: Plan, read: Answer) {
  const sent = serve({ list: [C.list_one], parties: [C.parties], agreements: [C.agreements], read: [read], ...plan });
  render(<AssetsPanel />);
  fireEvent.click(await screen.findByRole('button', { name: new RegExp(`^${ASSET.what}`) }));
  await waitFor(() => expect(screen.getByTestId('asset-open')).toBeTruthy());
  return sent;
}

describe('AssetsPanel, rendered against its routes\' own answers (a made-up asset)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('with sign-in off says nothing is kept by the route\'s reason, offers no form, and says nothing is controlled', async () => {
    serve({ list: [C.list_off], parties: [C.parties], agreements: [C.agreements] });
    render(<AssetsPanel />);
    await waitFor(() => expect(screen.getByTestId('assets-not-kept').textContent).toBe(C.list_off.body.not_kept_because));
    expect(screen.getByTestId('assets-not-controlled').textContent).toBe(C.list_off.body.controlled_basis);
    expect(screen.queryByTestId('assets-form')).toBeNull();
    expect(screen.queryByTestId('assets-none')).toBeNull();
  });

  it('says no asset only once the list is read, and offers owners and agreements only from their records', async () => {
    const list = held(C.list_empty);
    serve({ list: [list.reply], parties: [C.parties], agreements: [C.agreements] });
    render(<AssetsPanel />);
    expect(screen.getByText('Reading the asset records…')).toBeTruthy();
    expect(screen.queryByTestId('assets-none')).toBeNull();
    await act(async () => { list.letGo(); });
    await waitFor(() => expect(screen.getByTestId('assets-none').textContent).toBe('No asset is recorded yet.'));
    expect(screen.getByTestId('assets-not-judged').textContent).toBe(C.list_empty.body.judged_basis);
    await screen.findByTestId('assets-form');
    const values = (label: string) => within(screen.getByLabelText(label)).getAllByRole('option').map(o => (o as HTMLOptionElement).value);
    const pids = C.parties.body.parties.map((p: any) => p.id);
    expect(values('Owned by')).toEqual(['', ...pids]);
    expect(values('Possessed by')).toEqual(['', ...pids]);
    expect(values('Held under')).toEqual(['', ...C.agreements.body.agreements.map((g: any) => g.id)]);
    expect(values('Kind of asset')).toEqual(['vehicle', 'robot', 'drone', 'laboratory_instrument', 'other']);
  });

  it('a refused entry says the route\'s reason beside its button; an entered asset\'s six facts each read not evidenced', async () => {
    const sent = serve({ list: [C.list_empty, C.list_one], parties: [C.parties], agreements: [C.agreements], asset: [C.asset_refused, C.asset] });
    render(<AssetsPanel />);
    await screen.findByTestId('assets-form');
    type('What the asset is', ASSET.what);
    type('Owned by', ASSET.owned_by.party_id);
    type('Possessed by', ASSET.possessed_by.party_id);
    press('Enter this asset');
    await waitFor(() => expect(screen.getByTestId('assets-error').textContent).toBe(`The asset was not entered: ${failed(C.asset_refused)}`));
    type('Held under', ASSET.held_under.agreement_id);
    press('Enter this asset');
    await waitFor(() => expect(screen.getByTestId('asset-open')).toBeTruthy());
    expect(screen.getByTestId('asset-held').textContent).toBe(
      `Owned by ${ASSET.owned_by.name}; possessed by ${ASSET.possessed_by.name}; held under ${ASSET.held_under.title}. ${ASSET.held_under.basis}`);
    expect(facts()).toEqual(ASSET.facts.map((f: any) => `${f.name}: ${f.said}`));
    expect(ASSET.facts.every((f: any) => f.said === 'not evidenced')).toBe(true);
    await waitFor(() => expect(screen.getAllByTestId('asset-row')).toHaveLength(1));
    expect(sent.filter(s => s.method === 'POST').map(s => s.body)).toEqual([
      { what: ASSET.what, kind: 'robot', owned_by: ASSET.owned_by.party_id, possessed_by: ASSET.possessed_by.party_id, agreement_id: '' },
      { what: ASSET.what, kind: 'robot', owned_by: ASSET.owned_by.party_id, possessed_by: ASSET.possessed_by.party_id, agreement_id: ASSET.held_under.agreement_id }]);
  });

  it('evidence is said with who, when, its lapse and its state; a declaration naming nobody is refused beside its button', async () => {
    const sent = await opened({ evidence: [C.ev_insurance, C.ev_refused, C.ev_ready] }, C.ev_conformity);
    type('Evidence for', 'insurance');
    type('The evidence', 'a made-up policy that ended yesterday, as stated');
    type('It lapses on', C.ev_insurance.body.facts[4].evidence[0].lapses_on);
    press('Attach this evidence');
    const ins = C.ev_insurance.body.facts[4].evidence[0];
    await waitFor(() => expect(screen.getAllByTestId('asset-evidence').map(s => s.textContent)).toContain(line(ins)));
    expect(ins.state).toBe('lapsed');
    type('Evidence for', 'readiness');
    type('The evidence', 'a made-up declaration, as stated');
    type('It lapses on', '2030-01-01');
    press('Attach this evidence');
    await waitFor(() => expect(screen.getByTestId('asset-evidence-error').textContent).toBe(
      `The evidence was not attached: ${failed(C.ev_refused)}`));
    type('The person declaring it ready', 'Dee W1083-Madeup, as named');
    press('Attach this evidence');
    const dec = C.ev_ready.body.facts[5].evidence[0];
    await waitFor(() => expect(screen.getAllByTestId('asset-evidence').map(s => s.textContent)).toContain(line(dec)));
    expect(screen.queryByTestId('asset-evidence-error')).toBeNull();
    const posts = sent.filter(s => s.method === 'POST').map(s => s.body);
    expect(posts[0]).toEqual({ fact: 'insurance', evidence: 'a made-up policy that ended yesterday, as stated', lapses_on: ins.lapses_on });
    expect(posts[1]).toEqual({ fact: 'readiness', evidence: 'a made-up declaration, as stated', lapses_on: '2030-01-01', named_person: '' });
    expect(posts[2]).toEqual({ fact: 'readiness', evidence: 'a made-up declaration, as stated', lapses_on: '2030-01-01', named_person: 'Dee W1083-Madeup, as named' });
  });

  it('a declaration resting on evidence that has lapsed is said withdrawn, with the route\'s reason, and nothing is computed across the six', async () => {
    await opened({}, C.read_withdrawn);
    const f = Object.fromEntries(C.read_withdrawn.body.facts.map((x: any) => [x.fact, x]));
    await waitFor(() => expect(screen.getByTestId('asset-withdrawn').textContent).toBe(
      `Withdrawn: ${f.readiness.evidence[0].withdrawn_because}`));
    const said = screen.getAllByTestId('asset-evidence').map(s => s.textContent);
    expect(said).toContain(line(f.user_safety.evidence[0]));
    expect(f.user_safety.evidence[0].state).toBe('lapsed');
    expect(facts()[1]).toBe(`${f.place_permission.name}: not evidenced`);
    //  no word, score or percentage of readiness anywhere on the panel (the route's own sentence that none is computed
    //  aside)
    const text = (screen.getByTestId('assets-panel').textContent ?? '').replace(C.list_one.body.judged_basis, '');
    expect(text).not.toMatch(/ready to use|score|percent|%|fully evidenced/i);
  });

  it('a failed read says its reason in its own place, and says no record as none', async () => {
    serve({ list: [C.list_unread], parties: [C.parties], agreements: [C.agreements] });
    render(<AssetsPanel />);
    await waitFor(() => expect(screen.getByTestId('assets-unread').textContent).toBe(
      `The asset records could not be read (${failed(C.list_unread)}), so none is shown.`));
    expect(screen.queryByTestId('assets-none')).toBeNull();
  });

  it('a party list or an agreement list that could not be read is said on its own, and no asset is offered for entry', async () => {
    serve({ list: [C.list_empty], parties: [C.parties_unread], agreements: [C.agreements] });
    const first = render(<AssetsPanel />);
    await waitFor(() => expect(screen.getByTestId('assets-parties-unread').textContent).toBe(
      `The parties could not be read (${failed(C.parties_unread)}), so no owner or possessor can be chosen.`));
    await waitFor(() => expect(screen.queryByText('Reading the parties and agreements…')).toBeNull());
    expect(screen.queryByTestId('assets-agreements-unread')).toBeNull();
    expect(screen.queryByTestId('assets-form')).toBeNull();
    first.unmount();
    vi.unstubAllGlobals();
    serve({ list: [C.list_empty], parties: [C.parties], agreements: [C.agreements_unread] });
    render(<AssetsPanel />);
    await waitFor(() => expect(screen.getByTestId('assets-agreements-unread').textContent).toBe(
      `The agreements could not be read (${failed(C.agreements_unread)}), so none can be chosen to hold it under.`));
  });
});
