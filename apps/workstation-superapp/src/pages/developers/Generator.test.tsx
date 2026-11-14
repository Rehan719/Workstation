// W1006 (FU-399 part 36) — the Generator, rendered against the generator route's own answers.
//
// The Generator composes one artefact (code, a configuration, a schema, a document) from a description and says what
// served it. This mounts the real page against the answers its route gave on a fresh store, with no model installed
// (Generator.fixture.json, captured by w1006_capture.py: an artefact, and the route's refusal of a request with no
// description), and has the server be unreachable. A refusal says the server's reason, a field check by its field,
// and an answer that holds no artefact is not shown as nothing having run.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './Generator.fixture.json';
import { Generator } from './Generator';

type Reply = { status: number; body: unknown; unreachable?: boolean };
const PRODUCE = '/api/v1/generator/produce';

function serve(reply: Reply) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url !== PRODUCE) return { ok: false, status: 404, statusText: '', json: async () => ({ detail: `not served: ${url}` }) };
    if (reply.unreachable) throw new TypeError('Failed to fetch');
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
}

function generate() {
  render(<MemoryRouter><Generator /></MemoryRouter>);
  fireEvent.change(screen.getByLabelText('Artefact specification'), {
    target: { value: 'W1006 made up: a REST endpoint that validates and stores a user record' } });
  fireEvent.click(screen.getByRole('button', { name: /Generate/ }));
}

describe('Generator, rendered against the generator route\'s own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a description produces its artefact, shown as the server composed it', async () => {
    serve(captured.produced);
    generate();
    const output = (captured.produced.body as { output: string }).output;
    expect(await screen.findByText((_, el) => el?.tagName === 'PRE' && el.textContent === output)).toBeTruthy();
    expect(screen.queryByText(/^\[ERROR\]/)).toBeNull();
  });

  it('a refused run says the server\'s reason, a field check by its field', async () => {
    serve(captured.refused);
    generate();
    expect(await screen.findByText('[ERROR] Failed (HTTP 422): spec: Field required')).toBeTruthy();
  });

  it('a run the server cannot be reached for is said as one', async () => {
    serve({ status: 0, body: null, unreachable: true });
    generate();
    expect(await screen.findByText('[ERROR] Failed — backend unreachable.')).toBeTruthy();
  });

  it('an answer that holds no artefact is said, not shown as nothing having run', async () => {
    //  written here: the route has not been seen to answer an empty artefact, so this is its answer with the output emptied
    serve({ status: 200, body: { ...(captured.produced.body as object), output: '' } });
    generate();
    expect((await screen.findByTestId('generator-no-artefact')).textContent).toBe(
      'The generator answered, and its answer held no artefact.');
    expect(screen.queryByText('Describe an artefact and click Generate')).toBeNull();
  });
});
