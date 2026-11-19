// W1071 (FU-399 part 84) — the Quran platform's memorisation practice, rendered against its routes' own answers.
//
// The practice reads a learner's plan of three tracks, sets a portion in one, practises a verse with its words hidden
// (a word at a time, or the whole verse), and sets similar verses side by side; nothing in it is told what the
// learner recalled, and nothing is scored. This mounts the real panel against what each route answered on a fresh
// store (HifzPractice.fixture.json, captured by w1071_capture.py). EVERY VERSE'S TEXT IN IT IS MADE-UP PLACEHOLDER
// WORDS: the capture replaced the routes' fetch from the named source, so no Quran text is kept and the routes' own
// arithmetic ran over the placeholders. It holds a made-up learner's plan before and after a portion is set, the
// route's refusal of a portion that ends before it starts, verses 1:1 and 1:2 word by word, a verse whose fetch
// answered nothing (the route's 503), the similar verses of surah 112, and the plan route's own 500. Rendering found
// "Next word" asking for the verse the boxes named rather than the verse being practised (two verses' words said as
// one), and every failure said in one line above all three cards, taken away by whatever was done next. Fixed here.
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './HifzPractice.fixture.json';
import { HifzPractice } from './HifzPractice';

type Answer = { status: number; body: unknown };
const UID = captured.uid;
const PLAN = `/api/v1/qep/hifz/portions/${UID}`;
const PRACTICE = '/api/v1/qep/hifz/practice/';
const words = (a: Answer[]) => a.map(x => (x.body as { word: string | null }).word);

//  each route as it answered: a verse by its reference, its next word by how many words were already seen; the plan
//  takes the next answer in `plans` (the last one stays), a portion the next in `portions`
function serve(plan: { plans?: Answer[]; portions?: Answer[] } = {}) {
  const plans = [...(plan.plans ?? [captured.plan])];
  const portions = [...(plan.portions ?? [captured.portion_set])];
  const next = (list: Answer[]) => (list.length > 1 ? list.shift()! : list[0]);
  const verses: Record<string, Answer> = {
    '1/1': captured.hidden_1_1, '1/1?reveal=true': captured.reveal_1_1, '1/2': captured.hidden_1_2,
    '2/1': captured.hidden_2_1,
  };
  const nexts: Record<string, Answer[]> = { '1/1': captured.next_1_1, '1/2': captured.next_1_2 };
  const asked: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    asked.push(`${method} ${url}`);
    let a: Answer | undefined;
    if (method === 'GET' && url === PLAN) a = next(plans);
    else if (method === 'POST' && url === '/api/v1/qep/hifz/portion') a = next(portions);
    else if (url === '/api/v1/qep/hifz/similar?surahs=112') a = captured.similar_112;
    else if (url.startsWith(PRACTICE)) {
      const m = /^(\d+\/\d+)\/next\?after_words=(\d+)$/.exec(url.slice(PRACTICE.length));
      a = m ? nexts[m[1]]?.[Number(m[2]) - 1] : verses[url.slice(PRACTICE.length)];
    }
    a = a ?? { status: 404, body: { detail: `not served here: ${method} ${url}` } };
    const body = a.body;
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => body } as unknown as Response;
  }));
  return asked;
}

const mount = () => render(<HifzPractice uid={UID} />);
const shownText = () => screen.getByTestId('hifz-hidden-text').textContent;
//  a track's card, found by its label (its test id is built from the track's name, so it is not queried)
const track = (label: string) => screen.getByText(label, { selector: 'p' }).parentElement as HTMLElement;
const box = (label: string, value: string | number) => fireEvent.change(screen.getByLabelText(label), { target: { value: String(value) } });
const press = (name: string) => fireEvent.click(screen.getByRole('button', { name }));

describe('HifzPractice, rendered against its routes\' own answers (placeholder words for every verse)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('asks the next word of the verse being practised, whatever the boxes say when it is pressed', async () => {
    const asked = serve();
    mount();
    press('Begin');
    await waitFor(() => expect(shownText()).toBe(`${captured.hidden_1_1.body.shown} …`));
    press('Next word');
    await waitFor(() => expect(shownText()).toBe(`${captured.hidden_1_1.body.shown} ${words(captured.next_1_1)[0]} …`));
    press('Next word');
    await waitFor(() => expect(screen.getByTestId('hifz-hidden-count').textContent).toMatch(/^1:1 · 3 of /));
    box('Ayah', 2);   // the box now names another verse; the one being practised is still 1:1
    press('Next word');
    const four = [captured.hidden_1_1.body.shown, ...words(captured.next_1_1).slice(0, 3)].join(' ');
    await waitFor(() => expect(shownText()).toBe(`${four} …`));
    expect(asked).toContain(`GET ${PRACTICE}1/1/next?after_words=3`);
    expect(asked.some(u => u.includes('1/2/next'))).toBe(false);
  });

  it('shows the whole of the verse being practised', async () => {
    serve();
    mount();
    press('Begin');
    await waitFor(() => expect(screen.getByTestId('hifz-hidden')).toBeTruthy());
    box('Ayah', 2);
    press('Show the whole verse');
    const whole = captured.reveal_1_1.body;
    await waitFor(() => expect(shownText()).toBe(whole.text));
    expect(screen.getByTestId('hifz-hidden-count').textContent).toBe(
      `1:1 · ${whole.total_words} of ${whole.total_words} words shown · ${whole.source} · ${whole.edition} · ${whole.riwayah}`);
    expect(screen.getByTestId('hifz-hidden-judged').textContent).toBe(whole.judged_basis);
  });

  it('says a verse it could not fetch in the hidden verse card', async () => {
    serve();
    mount();
    box('Surah', 2);
    press('Begin');
    await waitFor(() => expect(screen.getByTestId('hifz-hidden-error').textContent).toBe(
      `Failed (HTTP 503): ${captured.hidden_2_1.body.detail}`));
    expect(screen.queryByTestId('hifz-hidden')).toBeNull();
    expect(screen.queryByTestId('hifz-plan-error')).toBeNull();
  });

  it('reads the plan and sets a portion as the panel asks', async () => {
    const asked = serve({ plans: [captured.plan, captured.plan_after] });
    mount();
    await waitFor(() => expect(screen.getByTestId('hifz-plan-defaults').textContent).toBe(captured.plan.body.defaults_basis));
    expect(within(track('New lesson')).getByText('not set')).toBeTruthy();
    box('From', 3);
    box('To', 4);
    press('Set portion');
    await waitFor(() => expect(within(track('New lesson')).getByText(/^page 3 to 4/)).toBeTruthy());
    expect(asked).toContain(`POST /api/v1/qep/hifz/portion`);
    const posted = (vi.mocked(fetch).mock.calls.find(c => c[0] === '/api/v1/qep/hifz/portion')![1] as RequestInit).body;
    expect(JSON.parse(String(posted))).toEqual(captured.portion_ask);
  });

  it('says a portion that was not set in the plan card, and keeps saying it when a verse is opened', async () => {
    serve({ portions: [captured.portion_backwards] });
    mount();
    await waitFor(() => expect(screen.getByTestId('hifz-plan-defaults')).toBeTruthy());
    box('From', 9);
    box('To', 2);
    press('Set portion');
    const refused = `Failed (HTTP 422): ${captured.portion_backwards.body.detail}`;
    await waitFor(() => expect(screen.getByTestId('hifz-plan-error').textContent).toBe(refused));
    press('Begin');
    await waitFor(() => expect(screen.getByTestId('hifz-hidden')).toBeTruthy());
    expect(screen.getByTestId('hifz-plan-error').textContent).toBe(refused);
  });

  it('says a plan it could not read in the plan card', async () => {
    serve({ plans: [captured.plan_failed] });
    mount();
    await waitFor(() => expect(screen.getByTestId('hifz-plan-error').textContent).toBe(
      `Failed (HTTP 500): ${captured.plan_failed.body.detail}`));
    expect(screen.queryByTestId('hifz-plan-defaults')).toBeNull();
  });

  it('sets similar verses side by side as the route found them', async () => {
    serve();
    mount();
    box('Surahs to compare', '112');
    press('Compare');
    const s = captured.similar_112.body;
    await waitFor(() => expect(screen.getByTestId('hifz-similar-basis').textContent).toBe(s.basis));
    expect(screen.getByTestId('hifz-similar-scholar').textContent).toBe(s.scholar_reviewed_basis);
    expect(screen.getByText(`${s.pairs_returned} of ${s.pairs_found} pair(s) shown · ${s.verses_examined} verse(s) examined`)).toBeTruthy();
    const first = s.pairs[0];
    expect(screen.getByText(`${first.a} and ${first.b} · ${first.shared_words} words shared`)).toBeTruthy();
    expect(screen.queryByTestId('hifz-similar-incomplete')).toBeNull();
  });
});
