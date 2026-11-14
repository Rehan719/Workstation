// W1031 (FU-399 part 54) — the Management Systems hub, rendered against its routes' own answers.
//
// The hub lists the management standards it knows and drafts six frameworks, one per tab. Until now it was read only
// as source text. This mounts the real hub against the routes' answers (ManagementSystemsHub.fixture.json, captured on
// a fresh store with no model installed): the standards, the floor's QMS framework and risk register for a made-up
// organisation, and the field check the QMS route gives a request that names no organisation.
//
// Rendering found two defects, fixed in this round:
// - a failed generation was handed to the result panel as if it were a framework, under "Result", with a Download
//   button that saved the failure sentence as management_framework.txt;
// - the hub kept its tab in state only, so a reload went back to QMS and no link could name a generator.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './ManagementSystemsHub.fixture.json';
import { ManagementSystemsHub } from './ManagementSystemsHub';

const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });

function serve(posts: Array<{ status: number; data: unknown }>) {
  vi.spyOn(axios, 'get').mockImplementation(async (url: string) => {
    if (url === '/api/v1/mgmt/standards') return { status: 200, data: captured.standards } as never;
    throw axiosRefusal(404, { detail: `not served here: ${url}` });
  });
  //  each generation is answered in turn
  const post = vi.spyOn(axios, 'post');
  for (const a of posts) {
    post.mockImplementationOnce(async () => {
      if (a.status >= 400) throw axiosRefusal(a.status, a.data);
      return a as never;
    });
  }
  return post;
}

function Where() {
  const l = useLocation();
  return <p>at: {l.pathname}{l.search}</p>;
}

function mount(at = '/management') {
  render(<MemoryRouter initialEntries={[at]}><ManagementSystemsHub /><Where /></MemoryRouter>);
}

async function generateQms() {
  fireEvent.change(screen.getByPlaceholderText('Acme Ltd'), { target: { value: captured.org } });
  fireEvent.click(screen.getByRole('button', { name: /Generate QMS Framework/ }));
}

const pre = (text: string) => screen.queryAllByText((_, el) => el?.tagName === 'PRE' && el.textContent === text);

describe('ManagementSystemsHub, rendered against its routes\' own answers', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.spyOn(window, 'scrollTo').mockImplementation(() => {});
  });

  it('lists the standards the route knows, and opens on the QMS generator', async () => {
    serve([]);
    mount();
    const [first] = captured.standards.standards;
    await waitFor(() => expect(screen.getByText(first.name).textContent).toBe(first.name));
    expect(captured.standards.standards.every(s => screen.queryAllByText(s.name).length > 0)).toBe(true);
    expect(screen.getByRole('button', { name: /Generate QMS Framework/ })).toBeTruthy();
  });

  it('shows a framework the floor composed whole, with its note', async () => {
    const post = serve([{ status: 200, data: captured.qms }]);
    mount();
    await generateQms();
    await waitFor(() => expect(pre(captured.qms.framework).length).toBe(1));
    expect(screen.getByText('Framework text')).toBeTruthy();
    expect(screen.getByText(captured.qms.ai_provenance.floor_note)).toBeTruthy();
    expect(screen.queryByTestId('mgmt-generate-failed')).toBeNull();
    expect(post).toHaveBeenCalledWith('/api/v1/mgmt/qms/generate', { organisation_name: captured.org, domain: 'general', size: 'small' });
  });

  it('says a refused generation as a failure where the form is, and offers nothing for download', async () => {
    serve([{ status: 200, data: captured.qms }, { status: captured.qms_refused.status, data: captured.qms_refused.body }]);
    mount();
    await generateQms();
    await waitFor(() => expect(pre(captured.qms.framework).length).toBe(1));
    await generateQms();
    const d = captured.qms_refused.body.detail[0];
    await waitFor(() => expect(screen.getByTestId('mgmt-generate-failed').textContent).toBe(
      `Nothing was generated: Failed (HTTP ${captured.qms_refused.status}): ${d.loc[d.loc.length - 1]}: ${d.msg}`));
    expect(screen.queryByText('Result')).toBeNull();
    expect(screen.queryByText('Framework text')).toBeNull();
    expect(pre(captured.qms.framework).length).toBe(0);
  });

  it('opens the generator the address names, and choosing one writes it into the address', async () => {
    serve([]);
    mount('/management?tab=risk');
    expect(screen.getByRole('button', { name: /Generate Risk Register/ })).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /EMS \(ISO 14001\)/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /management?tab=ems'));
    fireEvent.click(screen.getByRole('button', { name: /QMS \(ISO 9001\)/ }));
    await waitFor(() => expect(screen.getByText(/^at: /).textContent).toBe('at: /management'));
    expect(screen.getByRole('button', { name: /Generate QMS Framework/ })).toBeTruthy();
  });

  it('opens the QMS generator for a tab the hub does not have', () => {
    serve([]);
    mount('/management?tab=not-a-tab');
    expect(screen.getByRole('button', { name: /Generate QMS Framework/ })).toBeTruthy();
  });
});
