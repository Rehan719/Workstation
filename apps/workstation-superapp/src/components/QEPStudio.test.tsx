// W1073 (FU-399 part 86) — the Quran platform's studio, rendered against its routes' own answers.
//
// The studio lists the surahs, reads a surah, makes review cards for a trouble spot (SM-2), opens a due verse with its
// source, shows a sourced translation of its meanings when asked, records a review, composes a tajweed lesson outline
// (withheld until a scholar approves it) and shows the learner's own progress. This mounts the real studio against
// what each route answered on a fresh store (QEPStudio.fixture.json, captured by w1073_capture.py). THE PLATFORM'S
// QURAN CACHE WAS PLANTED WITH MADE-UP PLACEHOLDERS for the capture - Latin words for every verse, made-up surah names
// and a made-up stand-in for each translation - and the source itself was unreachable, so no Quran text, surah name
// or translation is in the fixture. Nothing is scored, and the memorisation practice it mounts is a stand-in here
// (rendered on its own in W1071). Rendering found a verse, its translation and a review said under a reference opened
// after they were asked for, every action's failure said in one line at the top of the studio and taken away by the
// next action, and the sections not read said by two of their reasons. Fixed here.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './QEPStudio.fixture.json';
import { QEPStudio } from './QEPStudio';

vi.mock('./HifzPractice', () => ({ HifzPractice: () => <p>memorisation practice stand-in</p> }));

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer>;
const UID = captured.uid;

//  each route as it answered; a read listed takes the next answer in its list (the last one stays)
function serve(plan: Record<string, Reply[]> = {}) {
  const lists: Record<string, Reply[]> = {
    [`/api/v1/qep/hifz/progress/${UID}`]: [captured.progress],
    [`/api/v1/qep/gamification/${UID}`]: [captured.gamification],
    '/api/v1/qep/hifz/schedule': [captured.scheduled],
    '/api/v1/qep/hifz/review': [captured.reviewed],
    ...Object.fromEntries(Object.entries(plan).map(([k, v]) => [k, [...v]])),
  };
  const fixed: Record<string, Answer> = {
    '/api/v1/auth/me': captured.me,
    '/api/v1/qep/suwar': captured.suwar,
    '/api/v1/qep/status': captured.status,
    '/api/v1/qep/translation/status': captured.translation_status,
    '/api/v1/qep/surah/1': captured.surah_1,
    '/api/v1/qep/surah/2': captured.surah_2,
    '/api/v1/qep/ayah/1/2': captured.ayah_1_2,
    '/api/v1/qep/ayah/1/3': captured.ayah_1_3,
    '/api/v1/qep/ayah/1/4': captured.ayah_1_4,
    '/api/v1/qep/translation/1/2': captured.translation_1_2,
    '/api/v1/qep/translation/1/3': captured.translation_1_3,
    '/api/v1/qep/tajweed/lesson': captured.lesson,
    '/api/v1/qep/tajweed/analyse': captured.recalled,
    '/api/v1/qep/recitation/reciters': captured.reciters,
  };
  const sent: { url: string; body?: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    sent.push({ url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    const l = lists[url];
    const r: Reply = l ? (l.length > 1 ? l.shift()! : l[0]) : (fixed[url] ?? { status: 404, body: { detail: `not served here: ${url}` } });
    const a = await r;
    if (a === 'unreachable') throw new TypeError('Failed to fetch');
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

const mount = () => render(<QEPStudio />);
const press = (name: string) => fireEvent.click(screen.getByRole('button', { name }));
const verse = (a: { body: unknown }) => (a.body as { text_arabic: string }).text_arabic;
const DUE = { [`/api/v1/qep/hifz/progress/${UID}`]: [captured.progress_after] };

describe('QEPStudio, rendered against its routes\' own answers (placeholder text for every verse)', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('reads the surah list, the learner\'s own progress and the platform\'s statement on opening', async () => {
    serve();
    mount();
    const s = captured.suwar.body.suwar;
    await waitFor(() => expect(screen.getByRole('option', { name: `1. ${s[0].name_transliteration} (${s[0].ayah_count} ayaat)` })).toBeTruthy());
    await waitFor(() => expect(screen.getByText(`${captured.progress.body.total_ayaat_in_schedule} scheduled`)).toBeTruthy());
    expect(screen.getByText('nothing due — schedule ayaat on the left')).toBeTruthy();
    expect(screen.getByTestId('qep-own-progress-basis').textContent).toBe(captured.gamification.body.own_progress.basis);
    expect(screen.queryByTestId('qep-sections-unread')).toBeNull();
  });

  it('reads a surah, and says a surah it could not read in the reader card', async () => {
    serve();
    mount();
    await waitFor(() => expect(screen.getAllByRole('option').length).toBe(2));
    press('Read');
    await waitFor(() => expect(screen.getByText(captured.surah_1.body.ayaat[1].text_arabic)).toBeTruthy());
    expect(screen.getByTestId('reader-provenance').textContent).toMatch(/^alquran\.cloud \(cached /);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '2' } });
    press('Read');
    await waitFor(() => expect(screen.getByTestId('qep-reader-error').textContent).toBe(
      `Surah 2 was not read: Failed (HTTP 503): ${captured.surah_2.body.detail}`));
    expect(screen.queryByText(captured.surah_1.body.ayaat[1].text_arabic)).toBeNull();
  });

  it('makes cards for a trouble spot, and says a spot past the surah\'s end in the reader card', async () => {
    const sent = serve({ [`/api/v1/qep/hifz/progress/${UID}`]: [captured.progress, captured.progress_after] });
    mount();
    await waitFor(() => expect(screen.getAllByRole('option').length).toBe(2));
    const [from, to] = screen.getAllByRole('spinbutton');
    fireEvent.change(from, { target: { value: '2' } });
    fireEvent.change(to, { target: { value: '4' } });
    press('Make cards for this spot (SM-2)');
    await waitFor(() => expect(screen.getByRole('button', { name: '1:2' })).toBeTruthy());
    expect(sent.find(x => x.url === '/api/v1/qep/hifz/schedule')!.body).toEqual(captured.schedule_ask);
    serve({ '/api/v1/qep/hifz/schedule': [captured.schedule_past_end], ...DUE });
    fireEvent.change(from, { target: { value: '5' } });
    fireEvent.change(to, { target: { value: '9' } });
    press('Make cards for this spot (SM-2)');
    await waitFor(() => expect(screen.getByTestId('qep-reader-error').textContent).toBe(
      `Failed (HTTP 422): ${captured.schedule_past_end.body.detail}`));
  });

  it('opens a due verse with its source, shows its translation when asked, and records a review', async () => {
    const sent = serve(DUE);
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: '1:2' })).toBeTruthy());
    press('1:2');
    await waitFor(() => expect(screen.getByText(verse(captured.ayah_1_2))).toBeTruthy());
    expect(screen.getByTestId('review-provenance').textContent).toMatch(/^alquran\.cloud/);
    press('Show a translation of the meanings');
    await waitFor(() => expect(screen.getByText(captured.translation_1_2.body.translation_text)).toBeTruthy());
    expect(screen.getByText(captured.translation_1_2.body.label)).toBeTruthy();
    press('4');
    await waitFor(() => expect(screen.getByTestId('hifz-efactor').textContent).toMatch(/^e-factor /));
    expect(sent.find(x => x.url === '/api/v1/qep/hifz/review')!.body).toEqual(captured.review_ask);
    expect(screen.getByTestId('hifz-memorised-basis').textContent).toContain(captured.reviewed.body.memorised_basis);
  });

  it('says a verse it could not read in the review card, and keeps the reader card\'s own failure', async () => {
    serve(DUE);
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: '1:4' })).toBeTruthy());
    press('1:4');
    await waitFor(() => expect(screen.getByTestId('qep-review-error').textContent).toBe(
      `The verse 1:4 could not be read: Failed (HTTP 503): ${captured.ayah_1_4.body.detail}`));
    expect(screen.queryByTestId('qep-reader-error')).toBeNull();
    press('1:2');   // another verse opened: the failure of the one before is not left standing
    await waitFor(() => expect(screen.getByText(verse(captured.ayah_1_2))).toBeTruthy());
    expect(screen.queryByTestId('qep-review-error')).toBeNull();
  });

  it('says a verse only under the reference it was asked for', async () => {
    const slow = held(captured.ayah_1_2);
    serve({ ...DUE, '/api/v1/qep/ayah/1/2': [slow.reply] });
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: '1:2' })).toBeTruthy());
    press('1:2');
    press('1:3');   // another verse opened while the first is still being read
    await waitFor(() => expect(screen.getByText(verse(captured.ayah_1_3))).toBeTruthy());
    await act(async () => { slow.letGo(); });
    expect(screen.queryByText(verse(captured.ayah_1_2))).toBeNull();
    expect(screen.getByText(verse(captured.ayah_1_3))).toBeTruthy();
  });

  it('says a translation only under the verse it was asked for', async () => {
    const slow = held(captured.translation_1_2);
    serve({ ...DUE, '/api/v1/qep/translation/1/2': [slow.reply] });
    mount();
    await waitFor(() => expect(screen.getByRole('button', { name: '1:2' })).toBeTruthy());
    press('1:2');
    await waitFor(() => expect(screen.getByText(verse(captured.ayah_1_2))).toBeTruthy());
    press('Show a translation of the meanings');
    press('1:3');   // the next verse opened while the translation of the first is still out
    await waitFor(() => expect(screen.getByText(verse(captured.ayah_1_3))).toBeTruthy());
    await act(async () => { slow.letGo(); });
    expect(screen.queryByText(captured.translation_1_2.body.translation_text)).toBeNull();
    expect(screen.queryByTestId('ayah-translation')).toBeNull();
  });

  it('asks a lesson outline and says why it is withheld, and says every section it could not read', async () => {
    serve({ [`/api/v1/qep/hifz/progress/${UID}`]: [captured.progress_failed] });
    mount();
    await waitFor(() => expect(screen.getByTestId('qep-sections-unread').textContent).toBe(
      `1 section(s) failed to load — ${captured.progress_failed.body.detail}`));
    press('Generate');
    const l = captured.lesson.body;
    await waitFor(() => expect(screen.getByTestId('qep-lesson-withheld').textContent).toBe(l.withheld_note || l.review_note));
    expect(screen.queryByTestId('qep-lesson-error')).toBeNull();
  });

  it('says a lesson outline that reached no server in the lesson card', async () => {
    serve({ '/api/v1/qep/tajweed/lesson': ['unreachable'] });
    mount();
    await waitFor(() => expect(screen.getAllByRole('option').length).toBe(2));
    press('Generate');
    await waitFor(() => expect(screen.getByTestId('qep-lesson-error').textContent).toBe(
      'No lesson outline: Failed — backend unreachable.'));
    expect(screen.queryByTestId('qep-reader-error')).toBeNull();
  });
});
