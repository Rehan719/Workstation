// W980 (FU-399 part 13) — the Settings page, rendered against its routes' own answers.
//
// Settings holds three records a person keeps: their profile (exactly what is added to their prompts), the avatar's
// clearance records (what they approved the avatar for, and the Owner's reply goals), and the protected-entities
// record the Owner names their own enterprises on. Each is three-state: read and empty, read and holding something,
// or NOT READ, and the third must never be said as the first. This mounts the real page against the answers the routes
// gave on a fresh store (Settings.fixture.json, captured by w980_capture.py: a made-up profile, a made-up approval, and
// one entity the capture established in its own store and named), drives it as a person would, and has the server
// refuse each read and each write.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { PROFILE_FIELDS } from '../lib/userProfile';
import captured from './Settings.fixture.json';
import { Settings } from './Settings';

type Reply = { status: number; body?: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

// answer each "METHOD url" with the captured answer, or with what a case puts in its place (a reply, or a function
// for a read whose answer changes after a write)
function serve(over: Record<string, Reply | (() => Reply)> = {}) {
  const calls: { method: string; url: string; body?: unknown }[] = [];
  const base: Record<string, Reply> = {
    'GET /api/v1/user/profile': ok(captured.profile_empty),
    'PUT /api/v1/user/profile': ok(captured.profile_put),
    'GET /api/v1/avatar/ratifications': ok(captured.ratifications_empty),
    'POST /api/v1/avatar/ratifications': ok(captured.ratification_recorded),
    'GET /api/v1/avatar/balance-objectives': ok(captured.goals),
    'GET /api/v1/economy/protected-entities': ok(captured.protected_unnamed),
    'PUT /api/v1/economy/protected-entities': ok(captured.protected_put),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const method = (init?.method ?? 'GET').toUpperCase();
    const key = `${method} ${url}`;
    calls.push({ method, url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    const r = key in over ? over[key] : base[key];
    const reply = (typeof r === 'function' ? r() : r) ?? refused(404, `not served in this test: ${key}`);
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
  return calls;
}

const NOTHING_SAVED = 'Nothing saved — no profile is added to your prompts.';
const preambleShown = (text: string) => screen.findByText(text, { selector: 'pre', normalizer: s => s });

describe('Settings, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a profile never filled in says nothing is saved, with every field empty', async () => {
    const calls = serve();
    render(<Settings />);
    await screen.findByTestId('avatar-ratifications-none');
    await waitFor(() => expect(calls.some(c => c.method === 'GET' && c.url === '/api/v1/user/profile')).toBe(true));
    expect(screen.getByText(NOTHING_SAVED)).toBeTruthy();
    expect(screen.queryByTestId('profile-unread')).toBeNull();
    for (const f of PROFILE_FIELDS) expect((screen.getByLabelText(f.label) as HTMLTextAreaElement).value).toBe('');
  });

  it('a saved profile shows each field and exactly what the server adds to prompts', async () => {
    serve({ 'GET /api/v1/user/profile': ok(captured.profile_saved) });
    render(<Settings />);
    expect(await preambleShown(captured.profile_saved.preamble_preview)).toBeTruthy();
    for (const f of PROFILE_FIELDS) {
      expect((screen.getByLabelText(f.label) as HTMLTextAreaElement).value).toBe(captured.profile_saved.profile[f.key]);
    }
    expect(screen.queryByText(NOTHING_SAVED)).toBeNull();
  });

  it('saving sends the form and shows the preamble the server built', async () => {
    const calls = serve();
    render(<Settings />);
    await screen.findByTestId('avatar-ratifications-none');
    for (const f of PROFILE_FIELDS) {
      fireEvent.change(screen.getByLabelText(f.label), { target: { value: captured.profile_put.profile[f.key] } });
    }
    fireEvent.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(await preambleShown(captured.profile_put.preamble_preview)).toBeTruthy();
    expect(calls.find(c => c.method === 'PUT' && c.url === '/api/v1/user/profile')?.body).toEqual(captured.profile_put.profile);
  });

  it('a profile that could not be read is said with the server\'s reason, never as nothing saved', async () => {
    serve({ 'GET /api/v1/user/profile': refused(503, 'the profile store is busy') });
    render(<Settings />);
    const said = await screen.findByTestId('profile-unread');
    expect(said.textContent).toContain('Your stored profile could not be read — Failed (HTTP 503): the profile store is busy.');
    expect(said.textContent).toContain('saving now would replace it');
    expect(screen.queryByText(NOTHING_SAVED)).toBeNull();
  });

  it('a refused save says the server\'s reason and is never shown as saved', async () => {
    const detail = 'w980 the stored profile could not be read whole; your profile was NOT overwritten, so nothing stored was lost';
    serve({ 'PUT /api/v1/user/profile': refused(503, detail) });
    render(<Settings />);
    await screen.findByTestId('avatar-ratifications-none');
    fireEvent.change(screen.getByLabelText(PROFILE_FIELDS[0].label), { target: { value: 'w980 a made-up line' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(await screen.findByText(`Failed (HTTP 503): ${detail}`)).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Saved' })).toBeNull();
    expect(screen.getByText(NOTHING_SAVED)).toBeTruthy();
  });

  it('a stored profile read only in part is said before anything is saved over it', async () => {
    const part = clone(captured.profile_empty);
    part.profile_is_incomplete = true;
    part.store_incomplete = 'w980 the stored document ended early';
    serve({ 'GET /api/v1/user/profile': ok(part) });
    render(<Settings />);
    const said = await screen.findByTestId('profile-store-incomplete');
    expect(said.getAttribute('title')).toBe('w980 the stored document ended early');
    expect(screen.queryByText(NOTHING_SAVED)).toBeNull();
  });

  it('a refused delete says the server\'s reason, and the profile stays shown', async () => {
    serve({ 'GET /api/v1/user/profile': ok(captured.profile_saved),
            'DELETE /api/v1/user/profile': refused(503, 'Profile busy — please retry.') });
    render(<Settings />);
    await preambleShown(captured.profile_saved.preamble_preview);
    fireEvent.click(screen.getByRole('button', { name: 'Delete profile' }));
    expect(await screen.findByText('Failed (HTTP 503): Profile busy — please retry.')).toBeTruthy();
    expect(screen.getByText(captured.profile_saved.preamble_preview, { selector: 'pre', normalizer: s => s })).toBeTruthy();
  });

  it('approvals: none is said only when they were read, an unread list is said as unread, and a recorded one is listed', async () => {
    serve();
    const a = render(<Settings />);
    await waitFor(() => expect(screen.getByTestId('avatar-ratifications-none').textContent).toBe(
      'No approval is recorded, so replies are not cleared by the chain.'));
    expect(screen.getByTestId('avatar-clearance-panel').textContent).toContain(
      `High-impact modes (${captured.ratifications_empty.high_impact_modes.join(', ')}) also need the Owner's co-signature.`);
    a.unmount();

    serve({ 'GET /api/v1/avatar/ratifications': refused(503, 'the approvals store could not be read') });
    const b = render(<Settings />);
    await waitFor(() => expect(screen.getByTestId('avatar-ratifications-unread').textContent).toBe(
      'The approvals were not read, so whether one is recorded is not known.'));
    expect(screen.getByTestId('avatar-clearance-error').textContent).toBe(
      'The avatar\'s clearance records could not be read: Failed (HTTP 503): the approvals store could not be read');
    expect(screen.queryByTestId('avatar-ratifications-none')).toBeNull();
    b.unmount();

    let recorded = false;
    const calls = serve({
      'GET /api/v1/avatar/ratifications': () => ok(recorded ? captured.ratifications : captured.ratifications_empty),
      'POST /api/v1/avatar/ratifications': () => { recorded = true; return ok(captured.ratification_recorded); },
    });
    render(<Settings />);
    await screen.findByTestId('avatar-ratifications-none');
    const purpose = captured.ratification_recorded.ratification.purpose;
    fireEvent.change(screen.getByTestId('avatar-ratification-purpose'), { target: { value: purpose } });
    fireEvent.click(screen.getByTestId('avatar-ratification-record'));
    const r = captured.ratifications.ratifications[0];
    expect(await screen.findByText(`${r.purpose} · modes ${r.modes.join(', ')} · signed by ${r.signatories.join(', ')}`)).toBeTruthy();
    expect(screen.queryByTestId('avatar-ratifications-none')).toBeNull();
    expect(calls.find(c => c.method === 'POST')?.body).toEqual({ purpose, modes: ['instructor'] });
  });

  it('reply goals: none recorded is said with the record\'s basis; a failed read is said as not read, never as none', async () => {
    serve();
    const a = render(<Settings />);
    await waitFor(() => expect(screen.getByTestId('avatar-balance-goals').textContent).toBe(
      `Reply goals (set by the Owner): none recorded — ${captured.goals.basis}`));
    await waitFor(() => expect(screen.getByTestId('avatar-approval-without-goals').textContent).toContain(captured.goals.basis));
    a.unmount();

    serve({ 'GET /api/v1/avatar/balance-objectives': refused(503, 'the goals record could not be read') });
    render(<Settings />);
    await waitFor(() => expect(screen.getByTestId('avatar-balance-goals').textContent).toBe(
      'Reply goals (set by the Owner): not read — Failed (HTTP 503): the goals record could not be read'));
    expect(screen.getByTestId('avatar-balance-goals').textContent).not.toContain('none recorded');
    expect(screen.queryByTestId('avatar-approval-without-goals')).toBeNull();
    // the approvals were read, so the list says what it read
    expect(screen.getByTestId('avatar-ratifications-none')).toBeTruthy();
  });

  it('the protected record is said in the server\'s words; naming one records and lists it; a refusal is said once', async () => {
    let named = false;
    const calls = serve({
      'GET /api/v1/economy/protected-entities': () => ok(named ? captured.protected_named : captured.protected_unnamed),
      'PUT /api/v1/economy/protected-entities': () => { named = true; return ok(captured.protected_put); },
    });
    const a = render(<Settings />);
    await waitFor(() => expect(screen.getByTestId('protected-entities-rule').textContent).toBe(captured.protected_unnamed.rule));
    expect(screen.getByTestId('protected-entities-state').textContent).toBe(captured.protected_unnamed.basis);
    const save = screen.getByTestId('protected-entities-save') as HTMLButtonElement;
    expect(save.disabled).toBe(true);
    const [id, why] = Object.entries(captured.protected_named.named)[0];
    fireEvent.change(screen.getByLabelText('Enterprise id 1'), { target: { value: id } });
    fireEvent.change(screen.getByLabelText('Why enterprise 1 is protected'), { target: { value: why } });
    expect(save.disabled).toBe(true);
    fireEvent.click(screen.getByLabelText('This is the Owner\'s own direction.'));
    fireEvent.click(save);
    await waitFor(() => expect(screen.getByTestId('protected-entities-saved').textContent).toBe(captured.protected_put.basis));
    expect(calls.find(c => c.method === 'PUT' && c.url === '/api/v1/economy/protected-entities')?.body).toEqual(
      { entities: { [id]: why }, owner_confirms: true });
    await waitFor(() => expect(screen.getByTestId('protected-entities-list').textContent).toContain(`${id} · ${why}`));
    expect(screen.getByTestId('protected-entities-list').textContent).toContain(`${captured.protected_named.apex[0]} · the apex`);
    expect(screen.getByTestId('protected-entities-state').textContent).toBe(captured.protected_named.basis);
    a.unmount();

    serve({ 'PUT /api/v1/economy/protected-entities': { status: captured.protected_refused.status, body: captured.protected_refused.body } });
    render(<Settings />);
    await screen.findByTestId('protected-entities-rule');
    fireEvent.change(screen.getByLabelText('Enterprise id 1'), { target: { value: 'w980-no-such-entity' } });
    fireEvent.change(screen.getByLabelText('Why enterprise 1 is protected'), { target: { value: 'a made-up reason' } });
    fireEvent.click(screen.getByLabelText('This is the Owner\'s own direction.'));
    fireEvent.click(screen.getByTestId('protected-entities-save'));
    const err = await screen.findByTestId('protected-entities-error');
    expect(err.textContent).toBe(`Failed (HTTP ${captured.protected_refused.status}): ${captured.protected_refused.body.detail}`);
    expect(err.textContent?.match(/Not recorded:/g)).toHaveLength(1);
  });
});
