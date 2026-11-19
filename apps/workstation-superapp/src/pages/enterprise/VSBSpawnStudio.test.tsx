// W1039 (FU-399 part 60) — the VSB Spawn Studio, rendered against its routes' own answers.
//
// The studio lists the entities, opens one into its board, economy, plan, orchestration, swarm and deliverables, and
// carries what is typed to Genesis, the one door. This mounts the real page against what the routes answered on a
// fresh store with no model installed (VSBSpawnStudio.fixture.json, captured by w1039_capture.py): one made-up entity
// established through Genesis, its record, its deliverables (none yet), and the server's own 500 when reading the
// entities, reading the entity, orchestrating it, or reading its deliverables fails inside. Rendering found each
// failure said in the wrong place or as something else, fixed in this round: the list's, the entity's and the
// orchestration's were said at the Genesis form, the list beneath saying "No VSB entities yet" and the entity saying
// "Loading org…" for good, and an unread list of deliverables was said as "None yet".
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './VSBSpawnStudio.fixture.json';
import { VSBSpawnStudio } from './VSBSpawnStudio';

type Answer = { status: number; body: unknown };
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

const VID = captured.vsb_id;
const NAME = 'W1039 Bakery Van';

//  the routes the page reads and runs, each answering as captured unless a test says otherwise
function serve(over: { list?: Answer; detail?: Answer; deliverables?: Answer; orchestrate?: Answer } = {}) {
  const answer = (a: Answer) => {
    if (a.status >= 400) throw axiosRefusal(a.status, a.body);
    return { status: a.status, data: a.body };
  };
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/vsb') return answer(over.list ?? captured.list);
    if (url === `/api/v1/vsb/${VID}`) return answer(over.detail ?? captured.detail);
    if (url === `/api/v1/deliverables?vsb_id=${VID}`) return answer(over.deliverables ?? captured.deliverables);
    if (url === '/api/v1/deliverables/types') return answer(captured.types);
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url === '/api/v1/transformation/orchestrate' && over.orchestrate) return answer(over.orchestrate);
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
}

function mount() {
  render(<MemoryRouter><VSBSpawnStudio /></MemoryRouter>);
}

async function openEntity() {
  fireEvent.click(await screen.findByText(NAME));
}

describe('VSBSpawnStudio, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('lists the entity the route answered, and opens it into its board, economy and deliverables', async () => {
    serve();
    mount();
    await waitFor(() => expect(screen.getByText(/^Spawned Entities/).textContent).toBe('Spawned Entities (1)'));
    await openEntity();
    await waitFor(() => expect(screen.getByText(captured.detail.body.board.chief.title).textContent)
      .toBe(captured.detail.body.board.chief.title));
    expect(screen.getByText(captured.detail.body.economy.entity_name)).toBeTruthy();
    await waitFor(() => expect(screen.getByText(/^Living deliverables/).textContent?.trim()).toBe('Living deliverables (0)'));
    expect(screen.getByText('None yet — produce one, or use the Deliverables page.')).toBeTruthy();
  });

  it('a list that could not be read says so in the list, and claims no entity', async () => {
    serve({ list: captured.list_failed });
    mount();
    await waitFor(() => expect(screen.getByTestId('spawn-entities-unread').textContent)
      .toBe(`The entities could not be read, so the list is not what is there: Failed (HTTP 500): ${captured.list_failed.body.detail}`));
    expect(screen.queryByText('No VSB entities yet. Establish your first one in Genesis.')).toBeNull();
    expect(screen.getByText(/^Spawned Entities/).textContent).toBe('Spawned Entities (not read)');
  });

  it('an entity whose read failed says so in its own panel, not "Loading org…"', async () => {
    serve({ detail: captured.detail_failed });
    mount();
    await openEntity();
    await waitFor(() => expect(screen.getByTestId('spawn-detail-failed').textContent)
      .toBe(`Could not load ${VID}: Failed (HTTP 500): ${captured.detail_failed.body.detail}`));
    expect(screen.queryByText('Loading org…')).toBeNull();
    expect(screen.getAllByText(/^Could not load /)).toHaveLength(1);
  });

  it('a failed orchestration is said under the entity\'s own button, once', async () => {
    serve({ orchestrate: captured.orch_failed });
    mount();
    await openEntity();
    fireEvent.click(await screen.findByRole('button', { name: /Orchestrate transformation/ }));
    await waitFor(() => expect(screen.getByTestId('spawn-orchestrate-failed').textContent)
      .toBe(`Orchestration failed: Failed (HTTP 500): ${captured.orch_failed.body.detail}`));
    expect(screen.getAllByText(/^Orchestration failed: /)).toHaveLength(1);
  });

  it('deliverables that could not be read are said as unread, not as none', async () => {
    serve({ deliverables: captured.deliv_failed });
    mount();
    await openEntity();
    await waitFor(() => expect(screen.getByTestId('read-failures').textContent).toContain("this entity's deliverables"));
    expect(screen.getByText(/^Living deliverables/).textContent?.trim()).toBe('Living deliverables (not read)');
    expect(screen.queryByText('None yet — produce one, or use the Deliverables page.')).toBeNull();
  });
});
