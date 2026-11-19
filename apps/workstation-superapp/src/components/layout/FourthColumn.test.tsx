// W1067 (FU-399 part 80) — the shell's fourth column, rendered against its routes' own answers.
//
// The column docks beside every page: the channels, a history of the avatar sessions and of the platform's own
// commits, and the in-house assistant (rendered on its own in W1064). This mounts the real column on its history
// against what each route answered on a fresh store (FourthColumn.fixture.json, captured by w1067_capture.py: the
// avatar sessions before and after a session was opened and a made-up question asked, the commit log of a made-up
// repository, the log of a directory that is no repository, the log of a repository git would not read for the
// server's user, and the sessions route's own 500). Rendering found the two lists read together, so one refused
// read took the other's answer off the column and was said as both failing; a failed read setting off both reads
// again without end; and a list read once never read again while the shell stayed open. Fixed here.
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './FourthColumn.fixture.json';
import { FourthColumn } from './FourthColumn';

type Answer = { status: number; body: unknown };
type Reply = Answer | 'unreachable' | Promise<Answer | 'unreachable'>;
const SESSIONS = '/api/v1/avatar/sessions';
const GIT = '/api/v1/workstation/git-history';
const COMMITS = captured.git_history.body.commits;
const LISTED = captured.sessions_after.body;
const NO_SESSIONS = 'No active sessions yet.';
const AGAIN = 'Read the sessions and the commits again';

const refusal = (a: Answer) => Object.assign(new Error(`Request failed with status code ${a.status}`),
  { isAxiosError: true, response: { status: a.status, data: a.body } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  each route as it answered; each read takes the next answer in its list (the last one stays)
function serve(plan: { sessions?: Reply[]; git?: Reply[] } = {}) {
  const sessions = [...(plan.sessions ?? [captured.sessions_after])];
  const git = [...(plan.git ?? [captured.git_history])];
  const calls: { url: string; params?: unknown }[] = [];
  const next = (list: Reply[]) => (list.length > 1 ? list.shift()! : list[0]);
  const answer = async (r: Reply) => {
    const a = await r;
    if (a === 'unreachable') throw unreached();
    if (a.status >= 400) throw refusal(a);
    return { status: a.status, data: a.body };
  };
  vi.spyOn(axios, 'get').mockImplementation(async (url: string, config?: { params?: unknown }) => {
    calls.push({ url, params: config?.params });
    if (url === SESSIONS) return answer(next(sessions)) as never;
    if (url === GIT) return answer(next(git)) as never;
    throw refusal({ status: 404, body: { detail: `not served here: ${url}` } });
  });
  return calls;
}

//  an answer held back until the test lets it go
function held(a: Answer | 'unreachable') {
  let letGo: () => void = () => undefined;
  const reply = new Promise<Answer | 'unreachable'>(go => { letGo = () => go(a); });
  return { reply, letGo: () => letGo() };
}

const open = () => <FourthColumn isCollapsed={false} onToggle={() => undefined} />;
const closed = () => <FourthColumn isCollapsed onToggle={() => undefined} />;
const read = (calls: { url: string }[], url: string) => calls.filter(c => c.url === url).length;

describe('FourthColumn, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('reads each list once on opening the history, and says what each answered', async () => {
    const calls = serve();
    render(open());
    await waitFor(() => expect(screen.getByText(`${LISTED[0].message_count} msg`)).toBeTruthy());
    expect(screen.getByText(`${LISTED[1].message_count} msg`)).toBeTruthy();
    for (const s of LISTED) expect(screen.getByText(s.context)).toBeTruthy();
    expect(document.body.textContent).toContain(LISTED[0].last_message);
    for (const c of COMMITS) expect(screen.getByText(c.message)).toBeTruthy();
    expect(screen.getByTestId('git-history-count').textContent).toBe(
      `showing ${COMMITS.length} of ${captured.git_history.body.repository_commits_total} commits in the repository`);
    expect(screen.getByTestId('git-history-caption').textContent).toContain(`(${captured.git_history.body.repository})`);
    expect(read(calls, SESSIONS)).toBe(1);
    expect(calls.filter(c => c.url === GIT)).toEqual([{ url: GIT, params: { limit: 12 } }]);
  });

  it('says a refused read of the sessions in its place, and the commits it did read', async () => {
    serve({ sessions: [captured.sessions_failed] });
    render(open());
    await waitFor(() => expect(screen.getByTestId('dock-sessions-unread').textContent).toBe(
      `The avatar sessions could not be read: Failed (HTTP 500): ${captured.sessions_failed.body.detail}`));
    await waitFor(() => expect(screen.getByText(COMMITS[0].message)).toBeTruthy());
    for (const c of COMMITS) expect(screen.getByText(c.message)).toBeTruthy();
    expect(screen.queryByTestId('git-history-unread')).toBeNull();
    expect(screen.queryByText(NO_SESSIONS)).toBeNull();
  });

  it('reads a list that failed again only when asked, never on its own', async () => {
    const calls = serve({ sessions: ['unreachable', captured.sessions_after], git: ['unreachable', captured.git_history] });
    render(open());
    await waitFor(() => expect(screen.getByTestId('git-history-unread').textContent).toBe(
      'The platform commits could not be read: Failed — backend unreachable.'));
    expect(screen.getByTestId('dock-sessions-unread').textContent).toBe(
      'The avatar sessions could not be read: Failed — backend unreachable.');
    //  the column waits for the person: a failed read is not read again on its own
    await act(async () => { await new Promise(r => setTimeout(r, 60)); });
    expect(read(calls, SESSIONS)).toBe(1);
    expect(read(calls, GIT)).toBe(1);
    fireEvent.click(screen.getByRole('button', { name: AGAIN }));
    await waitFor(() => expect(screen.getByText(COMMITS[0].message)).toBeTruthy());
    await waitFor(() => expect(screen.getByText(`${LISTED[0].message_count} msg`)).toBeTruthy());
    expect(screen.queryByTestId('dock-sessions-unread')).toBeNull();
    expect(screen.queryByTestId('git-history-unread')).toBeNull();
    expect(read(calls, SESSIONS)).toBe(2);
    expect(read(calls, GIT)).toBe(2);
  });

  it('reads the lists again each time the history is opened', async () => {
    const calls = serve({ sessions: [captured.sessions, captured.sessions_after] });
    const view = render(open());
    await waitFor(() => expect(screen.getByText(NO_SESSIONS)).toBeTruthy());
    view.rerender(closed());
    view.rerender(open());
    await waitFor(() => expect(screen.getByText(`${LISTED[0].message_count} msg`)).toBeTruthy());
    expect(screen.queryByText(NO_SESSIONS)).toBeNull();
    expect(read(calls, SESSIONS)).toBe(2);
    expect(read(calls, GIT)).toBe(2);
  });

  it('says an answer only for the opening that asked it, and no list before it is read', async () => {
    const first = held(captured.sessions);
    serve({ sessions: [first.reply, captured.sessions_after] });
    const view = render(open());
    await waitFor(() => expect(screen.getByText('Reading the avatar sessions…')).toBeTruthy());
    expect(screen.queryByText(NO_SESSIONS)).toBeNull();
    view.rerender(closed());
    view.rerender(open());   // opened again while the first read is still out
    await waitFor(() => expect(screen.getByText(`${LISTED[0].message_count} msg`)).toBeTruthy());
    await act(async () => { first.letGo(); });
    //  the first opening's answer (no session) is not said over the second's
    expect(screen.queryByText(NO_SESSIONS)).toBeNull();
    expect(screen.getByText(`${LISTED[1].message_count} msg`)).toBeTruthy();
  });

  it('says a commit log it could not read as that, with git\'s reason whole, never as no commits', async () => {
    serve({ git: [captured.git_unreadable, captured.git_refused] });
    const view = render(open());
    await waitFor(() => expect(screen.getByTestId('git-history-unreadable').textContent).toBe(
      `The platform commit log could not be read whole: ${captured.git_unreadable.body.unreadable_reason}.`));
    expect(screen.queryByText('No platform commits to show.')).toBeNull();
    expect(screen.queryByTestId('git-history-count')).toBeNull();
    //  a repository git will not read for the server's user: its reason carries git's own remedy, whole
    view.rerender(closed());
    view.rerender(open());
    await waitFor(() => expect(screen.getByTestId('git-history-unreadable').textContent).toBe(
      `The platform commit log could not be read whole: ${captured.git_refused.body.unreadable_reason}.`));
    const refused = captured.git_refused.body.unreadable_reason;
    const at = /repository at '([^']+)'/.exec(refused)![1];
    expect(refused.endsWith(`git config --global --add safe.directory ${at}`)).toBe(true);
    expect(screen.queryByText('No platform commits to show.')).toBeNull();
  });
});
