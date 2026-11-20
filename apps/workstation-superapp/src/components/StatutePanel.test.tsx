// W1106 (FU-399 part 95) — THE ACT ITSELF, AND WHERE HELP FROM A PERSON IS, rendered against the routes' own answers.
//
// The Law page's statute panel reads one provision of an Act word for word from its publisher when asked, and says
// where help from a person is. No rendered test mounted it. This mounts the real panel against what the routes
// answered on a fresh store (StatutePanel.fixture.json, captured by w1106_capture.py): where help is, with the five
// expectations as the server assesses them, and an address that names no provision, refused before anything is
// fetched. A provision's own text needs its publisher, which the capture's network refused, so none is served here.
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './StatutePanel.fixture.json';
import StatutePanel from './StatutePanel';

//  W1163 - a place's row as the panel says it: for whom, and when the page that says so was read and how
const listing = (xs: string[]) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} and ${xs[xs.length - 1]}`);

type Answer = { status: number; body: unknown };

//  each address answers what the routes answered for it; what was asked is kept in order
function serve(answers: Record<string, Answer>) {
  const sent: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    sent.push(url);
    const a = answers[url] ?? { status: 599, body: { detail: `the test served nothing for ${url}` } };
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => a.body };
  }));
  return sent;
}

function typeTheAddress() {
  const a = captured.ask;
  fireEvent.change(screen.getByLabelText('Kind of legislation'), { target: { value: a.kind } });
  fireEvent.change(screen.getByLabelText('Year'), { target: { value: a.year } });
  fireEvent.change(screen.getByLabelText('Number'), { target: { value: a.number } });
  fireEvent.change(screen.getByLabelText('Section'), { target: { value: a.section } });
}

describe('StatutePanel, the Act itself and where help from a person is, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('nothing is fetched until asked, and Read it waits for a year, a number and a section', () => {
    const a = captured.ask;
    const sent = serve({});
    render(<StatutePanel />);
    expect(screen.getByTestId('law-statute-panel').querySelector('h3')?.textContent).toBe('Read the Act itself');
    const readIt = screen.getByRole('button', { name: 'Read it' }) as HTMLButtonElement;
    expect(readIt.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText('Year'), { target: { value: a.year } });
    fireEvent.change(screen.getByLabelText('Number'), { target: { value: a.number } });
    expect(readIt.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText('Section'), { target: { value: a.section } });
    expect(readIt.disabled).toBe(false);
    expect(sent).toEqual([]);
  });

  it('an address that names no provision is refused in the route\'s words, and no text is shown', async () => {
    const refused = captured.not_an_address;
    const sent = serve({ [refused.url]: refused });
    render(<StatutePanel />);
    typeTheAddress();
    fireEvent.click(screen.getByRole('button', { name: 'Read it' }));
    await waitFor(() => expect(screen.getByTestId('law-statute-refusal').textContent).toBe(
      `Failed (HTTP 422): ${refused.body.detail}`));
    expect(sent).toEqual([refused.url]);
    expect(screen.queryByTestId('law-statute-text')).toBeNull();
  });

  it('where help is: each place by name and link, what the platform is not, how to complain, and the five expectations', async () => {
    const h = captured.help.body;
    const sent = serve({ '/api/v1/law/help': captured.help });
    render(<StatutePanel />);
    expect(screen.queryByTestId('law-help')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Where to get help from a person' }));
    await waitFor(() => expect(screen.getByTestId('law-expectations').querySelectorAll('[data-testid="law-expectation"]').length).toBe(5));
    expect(screen.getAllByTestId('law-expectation').map(e => e.textContent)).toEqual(
      h.expectations.rows.map(e => `${e.expectation}: ${e.state}. ${e.how}`));
    const help = screen.getByTestId('law-help');
    //  W1166 - the urgent routes come first in the help, one for each the answer carries
    const urgent = within(help).getByTestId('law-help-urgent');
    expect(urgent.querySelectorAll('[data-testid="urgent-route"]').length).toBe(h.urgent.length);
    expect(urgent.compareDocumentPosition(within(help).getByRole('link', { name: h.regulated_and_free_help[0].name }))
      & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    for (const p of h.regulated_and_free_help) {
      const link = within(help).getByRole('link', { name: p.name });
      expect(link.getAttribute('href')).toBe(p.link);
      expect(link.parentElement?.textContent).toBe(`${p.name} — ${p.for_what}`);
      expect(within(link.parentElement!.parentElement!).getByTestId('law-help-checked').textContent).toBe(
        `For ${listing(p.nations)}: ${p.checked}, ${p.how_read}.`);
    }
    for (const s of h.this_platform_is_not) expect(within(help).getByText(s)).toBeTruthy();
    expect(within(help).getByText(h.to_complain)).toBeTruthy();
    expect(within(help).getByText(h.basis)).toBeTruthy();
    expect(within(help).getByText(h.expectations.basis).getAttribute('title')).toBe(h.expectations.source_basis);
    const page = screen.getByTestId('law-help-the-page');
    expect(page.textContent).toBe(
      'The same list, with how to find a qualified scholar and how to raise a claim, is on the support page.');
    expect(page.querySelector('a')?.getAttribute('href')).toBe(h.the_page);
    expect(sent).toEqual(['/api/v1/law/help']);
  });
});
