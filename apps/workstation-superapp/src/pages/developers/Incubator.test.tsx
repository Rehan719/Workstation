// W1010 (FU-399 part 40) — the Incubator, rendered against its route's own answers.
//
// The Incubator runs a prompt tournament: variants of a base prompt, scored against the criteria a person states, over
// the iterations asked for, with the winner and why. This mounts the real page against what its route answered on a
// fresh store with no model installed (Incubator.fixture.json, captured by w1010_capture.py: a tournament the floor
// scored no variant of, and the route's refusal of a tournament with no base prompt), and has the server be
// unreachable. A refusal says the server's status and reason, a field check by its field, and never takes the page
// down.
import { fireEvent, render, screen } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Incubator.fixture.json';
import { Incubator } from './Incubator';

function answer(reply: { ok?: unknown; refused?: { status: number; body: unknown }; unreachable?: boolean }) {
  vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== '/api/v1/incubator/evolve') throw new Error(`not served in this test: ${url}`);
    if (reply.unreachable) throw Object.assign(new Error('Network Error'), { isAxiosError: true, response: undefined });
    if (reply.refused) {
      throw Object.assign(new Error(`Request failed with status code ${reply.refused.status}`),
        { isAxiosError: true, response: { status: reply.refused.status, data: reply.refused.body } });
    }
    return { data: reply.ok } as any;
  });
}

async function evolve() {
  render(<MemoryRouter><Incubator /></MemoryRouter>);
  fireEvent.click(screen.getByRole('button', { name: /New Tournament/ }));
  fireEvent.change(await screen.findByLabelText('Tournament name'), { target: { value: 'W1010 made-up welcome line' } });
  fireEvent.change(screen.getByLabelText('Base prompt'),
    { target: { value: 'W1010 made up: write a two-line welcome for a bakery cooperative\'s order page' } });
  fireEvent.click(screen.getByRole('button', { name: 'Create Tournament' }));
  fireEvent.click(await screen.findByRole('button', { name: /Run Evolution/ }));
}

describe('Incubator, rendered against its route\'s own answers', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('a tournament the floor scored no variant of names no winner, and says why in the server\'s words', async () => {
    answer({ ok: captured.evolved });
    await evolve();
    expect(captured.evolved.winner).toBeNull();
    expect(await screen.findByText(captured.evolved.winner_basis)).toBeTruthy();
  });

  it('a refused tournament says the server\'s status and reason, a field check by its field', async () => {
    answer({ refused: captured.refused });
    await evolve();
    expect(await screen.findByText('Failed (HTTP 422): base_prompt: Field required')).toBeTruthy();
    expect(screen.getByText('Evolution failed')).toBeTruthy();
  });

  it('a tournament the server cannot be reached for is said as one', async () => {
    answer({ unreachable: true });
    await evolve();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });
});
