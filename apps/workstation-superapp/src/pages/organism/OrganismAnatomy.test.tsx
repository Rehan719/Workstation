// W998 (FU-399 part 30) — the Organism Anatomy page, rendered against the organism routes' own answers.
//
// The page shows the organism's health and lifecycle, its systems, the signal feed, the healing log, the genome
// population with a genome lab, and the organism's config. This mounts the real page against the answers its seven reads
// gave on a fresh store (OrganismAnatomy.fixture.json, captured by w998_capture.py), and has the server refuse each
// read. Each failure is said by what was being read, with the server's reason, and an unread log is not an empty one.
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './OrganismAnatomy.fixture.json';
import { OrganismAnatomy } from './OrganismAnatomy';

type Reply = { status: number; body: unknown };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const URL = {
  health: '/api/v1/organism/health-summary', life: '/api/v1/organism/lifecycle', systems: '/api/v1/organism/systems',
  signals: '/api/v1/organism/nervous/signals?n=25', heal: '/api/v1/organism/self-healing/log',
  genome: '/api/v1/organism/genome', config: '/api/v1/organism/config',
};

//  a read the test holds unanswered, to see the page while it is under way
const never = new Promise<never>(() => undefined);
function serve(over: Record<string, Reply> = {}, held: string[] = []) {
  const base: Record<string, Reply> = {
    [URL.health]: ok(captured.health), [URL.life]: ok(captured.life), [URL.systems]: ok(captured.systems),
    [URL.signals]: ok(captured.signals), [URL.heal]: ok(captured.heal_log), [URL.genome]: ok(captured.genome),
    [URL.config]: ok(captured.config),
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (held.includes(url)) await never;
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return { ok: r.status < 400, status: r.status, statusText: '', json: async () => r.body };
  }));
}

const failures = () => screen.queryAllByTestId('read-failure').map(e => e.textContent);

describe('OrganismAnatomy, rendered against the organism routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('every read answered: no failure is said, and an empty healing log is said as empty', async () => {
    serve();
    render(<OrganismAnatomy />);
    expect(await screen.findByText('no healing events this process')).toBeTruthy();
    expect(captured.heal_log.events).toHaveLength(0);
    expect(failures()).toEqual([]);
  });

  it('a refused read of the healing log is not shown as a log of none', async () => {
    serve({ [URL.heal]: refused(503, 'the healing record is locked') });
    render(<OrganismAnatomy />);
    await waitFor(() => expect(failures()).toContain(
      'Could not read the healing log — Failed (HTTP 503): the healing record is locked'));
    expect((await screen.findByTestId('anatomy-heal-log-unread')).textContent).toBe(
      'The healing log could not be read, so this is not a log of none.');
    expect(screen.queryByText('no healing events this process')).toBeNull();
  });

  it('a refused signal feed is not shown as an empty feed', async () => {
    serve({ [URL.signals]: refused(502, 'the nervous system did not answer') });
    render(<OrganismAnatomy />);
    expect((await screen.findByTestId('anatomy-signals-unread')).textContent).toBe(
      'The signal feed could not be read, so this is not a feed of none.');
  });

  it('every failed read is named with its reason, not three of them by URL', async () => {
    serve({
      [URL.health]: refused(503, 'a'), [URL.life]: refused(503, 'b'), [URL.signals]: refused(503, 'c'),
      [URL.heal]: refused(503, 'd'), [URL.config]: refused(503, 'e'),
    });
    render(<OrganismAnatomy />);
    await waitFor(() => expect(failures()).toHaveLength(5));
    expect(failures()).toEqual(expect.arrayContaining([
      'Could not read the health summary — Failed (HTTP 503): a',
      'Could not read the lifecycle — Failed (HTTP 503): b',
      'Could not read the signal feed — Failed (HTTP 503): c',
      'Could not read the healing log — Failed (HTTP 503): d',
      'Could not read the organism config — Failed (HTTP 503): e',
    ]));
    expect(screen.queryByText(/section\(s\) failed to load/)).toBeNull();
  });

  it('the genome list says it failed only when the genome population is what failed', async () => {
    //  the genome read still under way, another read refused: the genome list has not failed
    serve({ [URL.config]: refused(503, 'the config could not be read') }, [URL.genome]);
    render(<OrganismAnatomy />);
    await waitFor(() => expect(failures()).toHaveLength(1));
    expect(screen.queryByTestId('anatomy-genomes-unread')).toBeNull();
  });
});
