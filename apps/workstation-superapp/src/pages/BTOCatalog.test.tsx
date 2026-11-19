// W1032 (FU-399 part 55) — the BTO catalogue, rendered against its routes' own answers.
//
// The catalogue composes a design blueprint from the components chosen, and builds to order the live products of its
// catalogue. Until now it was read only as source text. This mounts the real page against the routes' answers
// (BTOCatalog.fixture.json, captured on a fresh store with no model installed): the blueprint for a made-up entity
// with three components, the build-to-order answer for that blueprint's first live products, and what the server
// answers when the configure route fails inside (its own 500, which names the failure's class).
//
// Rendering found one defect, fixed in this round: both actions said every failure, a server's refusal included, as
// "check the API server is running".
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './BTOCatalog.fixture.json';
import { BTOCatalog } from './BTOCatalog';

const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

type Answer = { status: number; data: unknown } | 'unreached';
function serve(configure: Answer, build?: Answer) {
  return vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    const a = url === '/api/v1/bto/configure' ? configure : url === '/api/v1/bto/build' ? build : undefined;
    if (a === undefined) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (a === 'unreached') throw unreached();
    if (a.status >= 400) throw axiosRefusal(a.status, a.data);
    return a as never;
  });
}

function mount() {
  render(<MemoryRouter><BTOCatalog /></MemoryRouter>);
}

async function composeBlueprint() {
  for (const label of ['Entity', 'Virtual Sovereign Business', 'Products']) {
    fireEvent.click(screen.getByRole('button', { name: label }));
  }
  fireEvent.change(screen.getByPlaceholderText('Name your Sovereign Digital Entity...'), { target: { value: captured.name } });
  fireEvent.click(screen.getByRole('button', { name: /^Build Entity/ }));
}

describe('BTOCatalog, rendered against its routes\' own answers', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('shows the blueprint the route composed, said as a specification with nothing provisioned', async () => {
    const post = serve({ status: 200, data: captured.blueprint });
    mount();
    await composeBlueprint();
    await waitFor(() => expect(screen.getByText(captured.blueprint.entity_name).textContent).toBe(captured.blueprint.entity_name));
    expect(screen.getByText('Blueprint specified — not provisioned')).toBeTruthy();
    expect(screen.getByText(String(captured.blueprint.component_count))).toBeTruthy();
    expect(screen.getAllByText('SPECIFIED (blueprint only)').length).toBe(2);
    expect(post).toHaveBeenCalledWith('/api/v1/bto/configure', captured.request);
  });

  it('builds to order and says what was delivered, and what was only composed', async () => {
    const post = serve({ status: 200, data: captured.blueprint }, { status: 200, data: captured.build });
    mount();
    await composeBlueprint();
    await waitFor(() => expect(screen.getByRole('button', { name: /Build to Order/ })).toBeTruthy());
    fireEvent.click(screen.getByRole('button', { name: /Build to Order/ }));
    await waitFor(() => expect(screen.getByTestId('bto-delivered-line').textContent).toBe(
      `Delivered ${captured.build.delivered_count} · ${captured.build.composed_not_assessed_count} composed, not assessed · ${captured.build.posture}`));
    expect(screen.getByTestId('bto-delivered-basis').textContent).toBe(captured.build.delivered_basis);
    for (const b of captured.build.built) {
      expect(screen.getByTestId(`bto-status-${b.slug}`).textContent).toBe(String(b.status).replace(/_/g, ' ').toLowerCase());
    }
    expect(post).toHaveBeenLastCalledWith('/api/v1/bto/build', expect.objectContaining({ product_resources: captured.slugs }));
  });

  it('says a failed blueprint by its reason, never as a server that is not running', async () => {
    serve({ status: captured.configure_failed.status, data: captured.configure_failed.body });
    mount();
    await composeBlueprint();
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain(
      `Build failed: Failed (HTTP ${captured.configure_failed.status}): ${captured.configure_failed.body.detail}`));
    expect(screen.getByRole('alert').textContent).not.toMatch(/API server is running/);
  });

  it('says a build-to-order that reached no server as one', async () => {
    serve({ status: 200, data: captured.blueprint }, 'unreached');
    mount();
    await composeBlueprint();
    await waitFor(() => expect(screen.getByRole('button', { name: /Build to Order/ })).toBeTruthy());
    fireEvent.click(screen.getByRole('button', { name: /Build to Order/ }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('Build-to-Order failed: Failed — backend unreachable.'));
    expect(screen.queryByTestId('bto-delivered-line')).toBeNull();
  });
});
