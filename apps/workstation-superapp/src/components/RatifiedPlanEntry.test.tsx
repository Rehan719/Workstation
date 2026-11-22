// W1105 (FU-399 part 94) — THE OWNER'S RATIFIED PLAN, ENTERED BY ONE ACTION, rendered against its routes' own answers.
//
// The entry reads the business plan document the Owner ratified, shows what would be entered, and writes nothing until
// it is confirmed; the confirmation carries the fingerprint of the document that was shown, so a document changed in
// between is refused. No rendered test mounted it. This mounts the real panel against what the routes answered on a
// fresh store (RatifiedPlanEntry.fixture.json, captured by w1105_capture.py): with sign-in off; for a made-up person
// with no role; and for a made-up administrator who previews, is refused a fingerprint that is not the document's,
// enters it, and edits one field by hand after.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './RatifiedPlanEntry.fixture.json';
import { RatifiedPlanEntry } from './RatifiedPlanEntry';

type Answer = { status: number; body: unknown };
const PREVIEW = '/api/v1/business-plan/ratified/preview';
const ENTER = '/api/v1/business-plan/ratified/enter';

//  the preview answers each of `previews` in turn (the last again after that), and the entry `entered`; what was
//  asked is kept in order
function serve(previews: Answer[], entered?: Answer) {
  const sent: { url: string; method: string; body: unknown }[] = [];
  let read = 0;
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET';
    sent.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    const reply = (a: Answer) => ({ ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body });
    if (url === PREVIEW && method === 'GET') return reply(previews[Math.min(read++, previews.length - 1)]);
    if (url === ENTER && method === 'POST' && entered) return reply(entered);
    return reply({ status: 599, body: { detail: `the test served nothing for ${method} ${url}` } });
  }));
  return sent;
}

function mount() {
  const entered = vi.fn();
  render(<RatifiedPlanEntry onEntered={entered} />);
  return entered;
}

describe('RatifiedPlanEntry, the Owner\'s ratified plan entered by one action, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('nothing is read until asked; the preview says the document, its ratification, every field and what is not entered', async () => {
    const a = captured.preview_admin.body;
    //  W1193c: the document has changed more than once since it was ratified, and the page says every change
    expect(a.changes.length).toBeGreaterThan(1);
    const sent = serve([captured.preview_admin]);
    const entered = mount();
    expect(sent).toEqual([]);
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-document').textContent).toBe(
      `${a.document} · ratified by the Owner on ${a.ratified_on}`
      + a.changes.map(c => ` · changed on ${c.on}: ${c.what}`).join('')));
    for (const [k, v] of Object.entries(a.fields)) {
      expect(screen.getByText(k.replace('_', ' ')).nextElementSibling?.textContent).toBe(v);
    }
    expect(screen.getByTestId('ratified-not-entered').textContent).toBe(
      `Not entered, because this plan has no place for them: ${a.not_entered.join(', ')}. Also, ${a.canvas}.`);
    expect(screen.getByTestId('ratified-enter').textContent).toBe('Enter this into the plan');
    expect(screen.queryByTestId('ratified-already')).toBeNull();
    expect(screen.queryByTestId('ratified-cannot')).toBeNull();
    expect(screen.queryByTestId('ratified-preview')).toBeNull();
    expect(sent).toEqual([{ url: PREVIEW, method: 'GET', body: undefined }]);
    expect(entered).not.toHaveBeenCalled();
  });

  //  W1193c: a preview whose changes could not be read says so, never that the document did not change
  it('a preview with no changes to give says they could not be read', async () => {
    const a = captured.preview_admin.body;
    const body: Record<string, unknown> = { ...a };
    delete body.changes;
    serve([{ status: 200, body }]);
    mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-document').textContent).toBe(
      `${a.document} · ratified by the Owner on ${a.ratified_on} · its changes since ratification could not be read`));
  });

  it('a preview whose changes are null says they could not be read', async () => {
    const a = captured.preview_admin.body;
    serve([{ status: 200, body: { ...a, changes: null, changed_since: null } }]);
    mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-document').textContent).toBe(
      `${a.document} · ratified by the Owner on ${a.ratified_on} · its changes since ratification could not be read`));
  });

  it('entering sends the fingerprint of the document shown, says the basis and what was added, and reads the preview again', async () => {
    const a = captured.preview_admin.body;
    const e = captured.entered.body;
    const after = captured.preview_entered.body.already_entered;
    const sent = serve([captured.preview_admin, captured.preview_entered], captured.entered);
    const entered = mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-enter').textContent).toBe('Enter this into the plan'));
    fireEvent.click(screen.getByTestId('ratified-enter'));
    await waitFor(() => expect(screen.getByTestId('ratified-said').textContent).toBe(
      `${e.stamp.basis}. ${e.objectives_added} objective(s) added.`));
    expect(sent[1]).toEqual({ url: ENTER, method: 'POST', body: { sha256: a.sha256 } });
    expect(entered).toHaveBeenCalledTimes(1);
    await waitFor(() => expect(screen.getByTestId('ratified-already').textContent).toBe(
      `Entered ${after.entered_at} by ${after.entered_by}. ${after.basis}.`));
    expect(sent.map(s => `${s.method} ${s.url}`)).toEqual([`GET ${PREVIEW}`, `POST ${ENTER}`, `GET ${PREVIEW}`]);
  });

  it('a document changed after its preview is refused in the route\'s words, and nothing is said entered', async () => {
    serve([captured.preview_admin], captured.enter_stale);
    const entered = mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-enter').textContent).toBe('Enter this into the plan'));
    fireEvent.click(screen.getByTestId('ratified-enter'));
    await waitFor(() => expect(screen.getByTestId('ratified-refusal').textContent).toBe(
      `Failed (HTTP 409): ${captured.enter_stale.body.detail}`));
    expect(screen.queryByTestId('ratified-said')).toBeNull();
    expect(entered).not.toHaveBeenCalled();
  });

  it('with sign-in off nothing can be entered, and the route\'s reason is said where the button would be', async () => {
    const off = captured.preview_off.body;
    serve([captured.preview_off]);
    mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-cannot').textContent).toBe(
      `Cannot be entered now: ${off.cannot_because}.`));
    expect(off.can_enter).toBe(false);
    expect(screen.queryByTestId('ratified-enter')).toBeNull();
  });

  it('a person who is not the administrator reads no plan: the refusal is said, and nothing is offered to enter', async () => {
    serve([captured.preview_user]);
    mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-refusal').textContent).toBe(
      `Failed (HTTP 404): ${captured.preview_user.body.detail}`));
    expect(screen.queryByTestId('ratified-document')).toBeNull();
    expect(screen.queryByTestId('ratified-enter')).toBeNull();
    expect(screen.getByTestId('ratified-preview').textContent).toBe('Show what would be entered');
  });

  it('a field edited by hand since the entry is named beside who entered it', async () => {
    const ed = captured.preview_edited.body;
    serve([captured.preview_edited]);
    mount();
    fireEvent.click(screen.getByTestId('ratified-preview'));
    await waitFor(() => expect(screen.getByTestId('ratified-already').textContent).toBe(
      `Entered ${ed.already_entered.entered_at} by ${ed.already_entered.entered_by}. ${ed.already_entered.basis}.`
      + ` Edited by hand since: ${ed.edited_since.join(', ')}.`));
    expect(ed.edited_since).toEqual(['strategy']);
  });
});
