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

  // W1113 (FU-399 part 102) - what the anatomy page draws from its answers, read: the immune reading over no
  // observation, the blend's caption, the wired key whose consumer cannot act, and the genomes' bases
  it('the immune reading, the blend, a key that cannot act and the genomes are said in the answers\' own words', async () => {
    serve();
    render(<OrganismAnatomy />);
    const im = captured.systems.immune;
    expect(im.observations_in_window).toBe(0);
    await waitFor(() => expect(screen.getByTestId('anatomy-immune-reading').textContent).toBe(`nothing observed ${im.threat_level}`));
    expect(screen.getByTestId('anatomy-immune-reading').getAttribute('title')).toBe(im.observed_basis);
    const terms = Object.values(captured.health.composite_health_terms);
    expect(terms.every(t => t.measured === false)).toBe(true);
    expect(screen.getByTestId('blend-caption').textContent).toBe(
      `blended (${Math.round(terms.reduce((a, t) => a + t.weight, 0) * 100)}% not measured)`);
    const cannot = captured.config.key_wiring.filter(k => 'consumer_can_act' in k && k.consumer_can_act === false);
    expect(cannot.map(k => `${k.section}.${k.key}`)).toEqual(['organism.metabolic_throttle']);
    expect(screen.getAllByTestId('consumer-cannot-act').map(e => e.textContent)).toEqual(
      cannot.map(k => ('consumer_can_act_basis' in k ? k.consumer_can_act_basis : '')));
    const pop = captured.genome.population;
    expect([pop.mean_fitness, pop.mean_declared_fitness, Object.keys(pop.fitness_composition)]).toEqual([null, null, []]);
    expect(screen.getByTestId('genome-mean-not-measured').textContent).toBe(pop.mean_fitness_basis);
    //  nothing else is said of the population: no self-declared mean and no composition were returned
    expect(screen.getByTestId('genome-population-basis').textContent).toBe(pop.mean_fitness_basis);
    expect(screen.getByTestId('entity-genomes-basis').textContent).toBe(captured.genome.entity_genomes.basis);
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
    await waitFor(() => expect(screen.getByTestId('anatomy-heal-log-unread').textContent).toBe(
      'The healing log could not be read, so this is not a log of none.'));
    expect(screen.queryByText('no healing events this process')).toBeNull();
  });

  it('a refused signal feed is not shown as an empty feed', async () => {
    serve({ [URL.signals]: refused(502, 'the nervous system did not answer') });
    render(<OrganismAnatomy />);
    await waitFor(() => expect(screen.getByTestId('anatomy-signals-unread').textContent).toBe(
      'The signal feed could not be read, so this is not a feed of none.'));
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
