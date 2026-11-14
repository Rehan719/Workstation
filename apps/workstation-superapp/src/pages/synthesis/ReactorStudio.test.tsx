// W1006 (FU-399 part 36) — the Reactor's Studio, rendered against the studio route's own answers.
//
// The Studio draws a chart over a data series a person types, with computed statistics and a narrative, and says what
// served the narrative. This mounts the real page against the answers its route gave on a fresh store, with no model
// installed (ReactorStudio.fixture.json, captured by w1006_capture.py: a drawn series, and the route's refusal of a
// series with no point), and has the server be unreachable. A refusal says the server's reason.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './ReactorStudio.fixture.json';
import { ReactorStudio } from './ReactorStudio';

type Reply = { status: number; body: unknown; unreachable?: boolean };
const STUDIO = '/api/v1/reactor/studio';

function serve(reply: Reply) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== STUDIO) return { ok: false, status: 404, statusText: '', json: async () => ({ detail: `not served: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
}

function draw() {
  render(<MemoryRouter><ReactorStudio /></MemoryRouter>);
  fireEvent.click(screen.getByRole('button', { name: /Render analytics/ }));
}

describe('ReactorStudio, rendered against the studio route\'s own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a series is drawn with the server\'s title and narrative', async () => {
    serve(captured.drawn);
    draw();
    const drawn = captured.drawn.body as { title: string; insight: string };
    expect(await screen.findByText(drawn.title)).toBeTruthy();
    expect(screen.getByText((_, el) => el?.tagName === 'P' && el.textContent === drawn.insight)).toBeTruthy();
  });

  it('a refused render says the server\'s reason, not its status alone', async () => {
    serve(captured.refused);
    draw();
    expect(await screen.findByText(
      `Failed (HTTP 400): ${(captured.refused.body as { detail: string }).detail}`)).toBeTruthy();
  });

  it('a render the server cannot be reached for is said as one', async () => {
    serve({ status: 0, body: null, unreachable: true });
    draw();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });
});
