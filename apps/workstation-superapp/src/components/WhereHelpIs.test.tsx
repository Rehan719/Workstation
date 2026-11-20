// W953 (P5.20 clause 6) — the one page of where help is, rendered against the route's own answer
// (WhereHelpIs.fixture.json is written from agentic_core/api/where_help.page() by the round that built it, and the
// suite holds it equal to what GET /api/v1/support/where-help-is returns).
import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './WhereHelpIs.fixture.json';
import { WhereHelpIs } from './WhereHelpIs';

//  W1163 - a place's row as the panel says it: for whom, and when the page that says so was read and how
const listing = (xs: string[]) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} and ${xs[xs.length - 1]}`);

type Reply = { status: number; body: unknown };

function serve(reply: Reply) {
  const urls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    urls.push(url);
    return { ok: reply.status < 400, status: reply.status, statusText: '', json: async () => reply.body };
  }));
  return urls;
}

describe("WhereHelpIs, rendered against the route's own answer", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('says how to find a qualified scholar, in the server\'s words, and names none', async () => {
    const urls = serve({ status: 200, body: captured.page });
    render(<WhereHelpIs />);
    const scholar = await screen.findByTestId('where-help-scholar');
    const s = captured.page.a_qualified_scholar;
    expect(scholar.textContent).toContain(s.heading);
    for (const step of s.steps) expect(scholar.textContent).toContain(step);
    expect(screen.getByTestId('where-help-scholar-none').textContent).toBe(s.names_none_because);
    expect(screen.getByTestId('where-help-scholar-platform').textContent).toBe(s.this_platform);
    expect(scholar.querySelectorAll('a').length).toBe(0);
    expect(urls).toEqual(['/api/v1/support/where-help-is']);
  });

  it('links each place of legal help to its own page, with our one line, and copies nothing', async () => {
    serve({ status: 200, body: captured.page });
    render(<WhereHelpIs />);
    const rows = await screen.findAllByTestId('where-help-legal-entry');
    expect(rows.length).toBe(captured.page.regulated_and_free_help.length);
    captured.page.regulated_and_free_help.forEach((e, i) => {
      const a = rows[i].querySelector('a')!;
      expect(a.getAttribute('href')).toBe(e.link);
      expect(a.getAttribute('rel')).toBe('noreferrer');
      expect(a.textContent).toBe(e.name);
      expect(rows[i].querySelector('span')!.textContent).toBe(`${e.name} — ${e.for_what}`);
      expect(rows[i].querySelector('[data-testid="where-help-legal-checked"]')!.textContent).toBe(
        `For ${listing(e.nations)}: ${e.checked}, ${e.how_read}.`);
    });
  });

  it('says how to complain and what this platform is not, in the server\'s words', async () => {
    serve({ status: 200, body: captured.page });
    render(<WhereHelpIs />);
    await waitFor(() => expect(screen.getByTestId('where-help-complain').textContent).toBe(captured.page.to_complain));
    const not = screen.getByTestId('where-help-not');
    expect(Array.from(not.querySelectorAll('li')).map(li => li.textContent)).toEqual(captured.page.this_platform_is_not);
    expect(screen.getByTestId('where-help-basis').textContent).toBe(captured.page.basis);
  });

  it('a place whose page was read more than ninety days ago is said as not recently checked', async () => {
    const stale = captured.page_stale.regulated_and_free_help;
    serve({ status: 200, body: captured.page_stale });
    render(<WhereHelpIs />);
    await waitFor(() => expect(screen.getAllByTestId('where-help-legal-checked').map(s => s.textContent)).toEqual(
      stale.map(e => `For ${listing(e.nations)}: ${e.checked}, ${e.how_read}.`)));
    expect(stale.every(e => e.checked.startsWith('NOT RECENTLY CHECKED') && !e.recently_checked)).toBe(true);
  });

  it('a failed read is said in the server\'s words, and nothing is drawn as if there were no help', async () => {
    serve({ status: 503, body: { detail: captured.refusal_detail } });
    render(<WhereHelpIs />);
    const said = await screen.findByTestId('where-help-refusal');
    expect(said.textContent).toContain('Where help is could not be read');
    expect(said.textContent).toContain(captured.refusal_detail);
    expect(screen.queryByTestId('where-help-scholar')).toBeNull();
    expect(screen.queryByTestId('where-help-legal')).toBeNull();
  });
});
