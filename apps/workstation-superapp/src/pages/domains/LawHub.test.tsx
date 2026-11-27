// W996 (FU-399 part 28) — the Law hub, rendered against the Law routes' own answers.
//
// The hub says what this machine does in Law before any form: the tools that call no model come first, then each
// form's sentence for what it returns with no model, then the template list with the one it holds for a qualified
// read. This mounts the real page against the answers its reads gave on a fresh store (LawHub.fixture.json, captured
// by w996_capture.py), and has the server refuse each read. A refusal says the server's reason, and a count on the
// page is the server's.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AdaptiveUIProvider } from '../../components/AdaptiveUIProvider';
import captured from './LawHub.fixture.json';
import { LawHub } from './LawHub';

type Reply = { status: number; body: unknown; notJson?: boolean };
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (status: number, detail: string): Reply => ({ status, body: { detail } });

const TEMPLATES = '/api/v1/law/templates';
const TOOLS = '/api/v1/law/tools';

function serve(over: Record<string, Reply> = {}) {
  const base: Record<string, Reply> = {
    [TEMPLATES]: ok(captured.templates), [TOOLS]: ok(captured.tools),
    '/api/v1/native-ai/status': ok(captured.serving), '/api/v1/law/help': ok(captured.help),
    '/api/v1/law/urgent': ok(captured.urgent),   // W1166
    '/api/v1/law/checklists': ok(captured.checklists),   // W1168
  };
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const r = (url in over ? over[url] : base[url]) ?? refused(404, `not served in this test: ${url}`);
    return {
      ok: r.status < 400, status: r.status, statusText: '',
      json: async () => { if (r.notJson) throw new SyntaxError('Unexpected token < in JSON at position 0'); return r.body; },
    };
  }));
}

function mount() {
  render(
    <MemoryRouter>
      <AdaptiveUIProvider>
        <LawHub />
      </AdaptiveUIProvider>
    </MemoryRouter>,
  );
}

describe('LawHub, rendered against the Law routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('the urgent routes come before anything else on the page, in the route\'s own words', async () => {
    serve();
    mount();
    const box = await screen.findByTestId('law-urgent');
    expect(box.compareDocumentPosition(screen.getByRole('heading', { level: 1 })) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(Array.from(box.querySelectorAll('[data-testid="urgent-situation"]')).map(e => e.textContent))
      .toEqual(captured.urgent.routes.map(r => r.situation));
    expect(Array.from(box.querySelectorAll('[data-testid="urgent-step"]')).map(e => e.textContent))
      .toEqual(captured.urgent.routes.flatMap(r => r.steps));
    expect(box.querySelector('[data-testid="urgent-basis"]')!.textContent).toBe(captured.urgent.basis);
  });

  it('a list of urgent routes that could not be read is said in its place, with the line to call 999', async () => {
    serve({ '/api/v1/law/urgent': refused(503, 'the register of sources could not be read') });
    mount();
    const note = await screen.findByTestId('law-urgent-note');
    expect(note.textContent).toBe('The urgent routes could not be read (Failed (HTTP 503): the register of sources '
      + 'could not be read). '
      + 'If you are in immediate danger, call 999.');
    expect(screen.queryByTestId('law-urgent')).toBeNull();
    expect(note.compareDocumentPosition(screen.getByRole('heading', { level: 1 })) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  //  W1167 (P5.11 clause 7) - the research route's own answer to a question on a regulated subject (its POST is
  //  axios's, answered here with the answer the route gave): its row after the urgent routes, before the people
  it('a question on a regulated subject is answered by its row and a route, after the urgent routes', async () => {
    serve();
    const a = captured.research_boundary;
    const post = vi.spyOn(axios, 'post').mockResolvedValue({ data: a } as never);
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Research' }));
    fireEvent.change(screen.getByLabelText('Legal question'), { target: { value: a.question } });
    fireEvent.click(screen.getByRole('button', { name: /Research question/ }));
    const box = await screen.findByTestId('law-research-boundary');
    expect(post.mock.calls[0][0]).toBe('/api/v1/law/research');
    const b = a.boundary;
    const texts = (id: string) => Array.from(box.querySelectorAll(`[data-testid="${id}"]`)).map(e => e.textContent);
    expect(texts('boundary-subject')).toEqual([`${b.subject}: regulated advice, not answered here`]);
    expect(texts('boundary-regulated')).toEqual([`${b.regulated}.`]);
    expect(texts('boundary-words')).toEqual(b.words);
    //  W1181 - each quote says the page it is from, inside its own item: the page the route named for it, or none
    const items = Array.from(box.querySelectorAll('li')).filter(li => li.querySelector('[data-testid="boundary-words"]'));
    expect(items.map(li => [li.querySelector('[data-testid="boundary-words"]')?.textContent,
      li.querySelector('[data-testid="boundary-words-from"]')?.textContent ?? null]))
      .toEqual(b.words.map((w, i) => {
        const s = b.sources.find(x => x.id === b.words_from[i]);
        return [w, s ? ` (${s.name ?? s.id})` : null];
      }));
    expect(texts('boundary-place')).toEqual(b.places.map(p => `${p.nation}: ${p.name} (${p.own_site})`));
    expect(texts('boundary-read')).toEqual([`Read: ${b.sources.map(s => `${s.name}, ${s.checked}`).join('; ')}.`]);
    expect(texts('boundary-regulator')).toEqual(
      [`Regulator: ${b.regulator.name}. Its own page was read: ${b.regulator.page.name}, ${b.regulator.page.checked}.`]);
    //  the urgent routes come first, the people it is routed to after, and the answer's text is the route's message
    expect(screen.getByTestId('law-research-urgent').compareDocumentPosition(box) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(box.compareDocumentPosition(screen.getByTestId('law-routed-to-people')) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(screen.getByText(a.analysis)).toBeTruthy();
  });

  it('what runs here is the server\'s, and the count of forms that need a model is its list\'s', async () => {
    serve();
    mount();
    const noModel = captured.tools.needs_no_model;
    expect(await screen.findAllByTestId('law-no-model-tool')).toHaveLength(noModel.length);
    const n = captured.tools.needs_a_model.length;
    expect(screen.getByTestId('law-forms-need-a-model').textContent).toMatch(
      new RegExp(`^The ${n === 1 ? 'one form' : `${n} forms`} further down need${n === 1 ? 's' : ''} a model\\.`));
  });

  it('a list with a different number of forms is counted as the server lists them', async () => {
    const one = { ...captured.tools, needs_a_model: captured.tools.needs_a_model.slice(0, 1) };
    serve({ [TOOLS]: ok(one) });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-forms-need-a-model').textContent).toMatch(/^The one form further down needs a model\./));
  });

  it('a refused read of the tools says the server\'s reason', async () => {
    serve({ [TOOLS]: refused(503, 'the tools register is being rebuilt') });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-tools-note').textContent).toBe(
      'What each Law tool does could not be read (Failed (HTTP 503): the tools register is being rebuilt), so nothing is said about it here. Each answer still says what composed it.'));
  });

  it('a refused read of the templates says the server\'s reason on the draft tab', async () => {
    serve({ [TEMPLATES]: refused(502, 'the template store did not answer') });
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    await waitFor(() => expect(screen.getByTestId('law-templates-note').textContent).toMatch(
      /^The template list could not be read \(Failed \(HTTP 502\): the template store did not answer\), so the templates typed/));
  });

  it('an answer that is not JSON is said by its status, not by the parser', async () => {
    serve({ [TOOLS]: { status: 502, body: null, notJson: true } });
    mount();
    await waitFor(() => expect(screen.getByTestId('law-tools-note').textContent)
      .toMatch(/^What each Law tool does could not be read \(Failed \(HTTP 502\): /));
    expect(screen.getByTestId('law-tools-note').textContent).not.toContain('Unexpected token');   // once it has settled
  });

  it('the templates held for a qualified read are said on the draft tab', async () => {
    serve();
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    const held = captured.templates.held;
    await waitFor(() => expect(screen.getByTestId('law-templates-held').textContent).toContain(held.reason));
  });

  // W1195 (P5.18 clause 4) - the reserved documents, beside the held line, with what the screen reads
  it('the reserved documents are said on the draft tab, with what the screen of a request reads', async () => {
    serve();
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    const reserved = captured.templates.reserved;
    await waitFor(() => expect(screen.getByTestId('law-templates-reserved').textContent).toContain(reserved.reason));
    expect(screen.getByTestId('law-templates-reserved').textContent).toContain(reserved.screen_basis);
  });

  // W1195 (review PW5) - the person's half of 'refused through the route a person would use': words typed on the
  // Draft tab are posted, the route refuses them (its own answer, captured by a real POST), and the page says the
  // route's reason whole, never a status or a guess
  it('a reserved document asked for in a listed template\'s words is refused, in the route\'s own words', async () => {
    serve();
    const refusal = captured.generate_refused;
    const post = vi.spyOn(axios, 'post').mockRejectedValue(
      { response: { status: refusal.status, data: { detail: refusal.detail } } } as never);
    mount();
    fireEvent.click(await screen.findByRole('button', { name: 'Draft' }));
    const asked = refusal.request;
    fireEvent.change(await screen.findByLabelText('Template'), { target: { value: asked.template_id } });
    fireEvent.change(screen.getByLabelText('Parties (key: value per line)'),
      { target: { value: Object.entries(asked.parties).map(([k, v]) => `${k}: ${v}`).join('\n') } });
    fireEvent.change(screen.getByLabelText('Custom instructions (optional)'), { target: { value: asked.custom_instructions } });
    fireEvent.click(screen.getByRole('button', { name: /Draft document/ }));
    expect(await screen.findByText(refusal.detail)).toBeTruthy();
    expect(post.mock.calls[0][0]).toBe('/api/v1/law/generate');
    const body = post.mock.calls[0][1] as { template_id: string; parties: unknown; custom_instructions: string };
    expect([body.template_id, body.parties, body.custom_instructions]).toEqual(
      [asked.template_id, asked.parties, asked.custom_instructions]);
  });
});
