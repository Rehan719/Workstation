// W1042 — a domain tool's failure is said by what it was, never guessed as a backend that may be down.
//
// DomainTool is the one component behind the twenty-five domain tools. Its generation and its refine each said
// "the backend may be unavailable" whenever no reason came, which covers both a server that answered without a reason
// (it was not unavailable) and one that could not be reached (which can be said for certain). This mounts the real tool
// against the review options its route gave (DomainTool.fixture.json, W925's capture) and has the tool's own route
// fail: unreachable, and answering with no reason; and a refine the server cannot be reached for.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DomainTool.fixture.json';
import { DomainTool } from './DomainTool';

const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

//  the reads before the form: the tool's review options as the route gave them, and what serves the tools
function serveReads() {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const reply = (status: number, body: unknown) => ({ ok: status < 400, status, statusText: '', json: async () => body });
    if (url.startsWith('/api/v1/review-options?endpoint=')) return reply(captured.signed.status, captured.signed.body);
    if (url === '/api/v1/native-ai/status') return reply(200, captured.status);
    return reply(200, {});
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <DomainTool title="A tool" description="what it does" endpoint={captured.signed.endpoint} resultKey="plan"
        fields={[{ name: 'notes', label: 'Notes', type: 'textarea' }]} />
    </MemoryRouter>,
  );
}

async function generate() {
  fireEvent.change(await screen.findByLabelText('Notes'), { target: { value: 'W1042 made up: notes for a tool' } });
  fireEvent.click(screen.getByRole('button', { name: /Generate/ }));
}

const guessed = () => screen.queryByText(/may be unavailable/);

describe('DomainTool, a failure said by what it was', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('a generation the server cannot be reached for is said as one, not as a backend that may be down', async () => {
    serveReads();
    vi.spyOn(axios, 'post').mockRejectedValue(unreached());
    mount();
    await generate();
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
    expect(guessed()).toBeNull();
  });

  it('a generation the server answered without a reason says its status, and that no reason came', async () => {
    serveReads();
    vi.spyOn(axios, 'post').mockRejectedValue(axiosRefusal(500, {}));
    mount();
    await generate();
    expect(await screen.findByText('Failed (HTTP 500): no reason given')).toBeTruthy();
    expect(guessed()).toBeNull();
  });

  it('a refine the server cannot be reached for is said as one, and the output it would have changed stands', async () => {
    serveReads();
    const post = vi.spyOn(axios, 'post')
      .mockResolvedValueOnce({ status: 200, data: { plan: 'W1042 made up: the first output', ai_provenance: { served_by: 'native', is_external: false } } })
      .mockRejectedValueOnce(unreached());
    mount();
    await generate();
    await waitFor(() => expect(screen.getByText(/W1042 made up: the first output/).textContent).toContain('W1042 made up: the first output'));
    fireEvent.change(screen.getByLabelText('Refinement instruction'), { target: { value: 'W1042 made up: shorter' } });
    fireEvent.click(screen.getByRole('button', { name: /^Refine$/ }));
    expect(await screen.findByText('Failed — backend unreachable. (your current output is unchanged)')).toBeTruthy();
    expect(post).toHaveBeenLastCalledWith('/api/v1/refine', expect.objectContaining({ instruction: 'W1042 made up: shorter' }));
    expect(screen.getByText(/W1042 made up: the first output/)).toBeTruthy();
    expect(guessed()).toBeNull();
  });
});
