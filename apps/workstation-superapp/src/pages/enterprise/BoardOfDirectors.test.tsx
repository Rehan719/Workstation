// W926 (FU-399 part 7) — the Board of Directors page, rendered against the API's own answers.
//
// What a person reads on the Board page are claims about their own standing and decisions: whether their Chief carries
// their record or is a role, what the Board's charter makes it ratify, whether a topic was deliberated or only framed,
// and what became of a change a review approved. This mounts the real page against the answers the board routes gave
// on a fresh store (BoardOfDirectors.fixture.json, captured by w926_capture.py) and reads each claim in the DOM, then
// the same answers changed the ways the server changes them, and the reads the server refuses.
import { fireEvent, render, screen, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './BoardOfDirectors.fixture.json';
import { BoardOfDirectors } from './BoardOfDirectors';

type Reply = { status: number; body: unknown };
type Answers = Partial<Record<'status' | 'charter' | 'model' | 'ratifications' | 'directive' | 'ratify' | 'instruct' | 'statusAfter', Reply>>;
const ok = (body: unknown): Reply => ({ status: 200, body });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: Answers) {
  let statusReads = 0;
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    const reply = ({ status, body }: Reply) => ({ ok: status < 400, status, statusText: '', json: async () => body });
    const post = init?.method === 'POST';
    if (url === '/api/v1/board/status') {
      statusReads += 1;
      return reply(statusReads > 1 && a.statusAfter ? a.statusAfter : (a.status ?? ok(captured.status)));
    }
    if (url === '/api/v1/board/charter') return reply(a.charter ?? ok(captured.charter));
    if (url === '/api/v1/board/chief/model') return reply(a.model ?? ok(captured.model_role));
    if (url === '/api/v1/board/ratifications' && !post) return reply(a.ratifications ?? ok(captured.ratifications_empty));
    if (url.startsWith('/api/v1/board/ratifications/') && post) return reply(a.ratify ?? ok(captured.ratified));
    if (url === '/api/v1/board/directive' && post) return reply(a.directive ?? ok(captured.topic_answer));
    if (url === '/api/v1/board/chief/instruct' && post) return reply(a.instruct ?? ok(captured.instruct_answer));
    return reply(ok({}));
  }));
}

const text = (id: string) => screen.getByTestId(id).textContent;

describe('BoardOfDirectors, rendered against the board routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a Chief with nothing of yours is a role, said in the server\'s words, with the charter\'s duty and an empty queue', async () => {
    serve({});
    render(<BoardOfDirectors />);
    const role = await screen.findByTestId('chief-model-role');
    expect(role.textContent).toContain('A role, not a modelled twin');
    expect(role.textContent).toContain(captured.model_role.basis);
    expect(screen.queryByTestId('chief-model-twin')).toBeNull();
    expect(text('board-ratification-duty')).toBe(captured.charter.ratification);
    expect(text('recent-directives-basis')).toBe(captured.status.recent_directives_basis);
    expect(await screen.findByText('No change is waiting for ratification.')).toBeTruthy();
    expect(text('board-ratification-count')).toBe('0');
  });

  it('a Chief carrying your record says how many of your instructions and decisions it holds', async () => {
    const m = captured.model_twin;
    serve({ model: ok(m), status: ok(captured.status_after_instruction) });
    render(<BoardOfDirectors />);
    const twin = await screen.findByTestId('chief-model-twin');
    expect(twin.textContent).toContain(
      `Chief carrying your record — ${m.instructions.count} instruction(s) you wrote · ${m.decisions.count} decision(s) you made`);
    expect(twin.textContent).toContain(m.basis);
    expect(within(await screen.findByTestId('latest-owner-instruction')).getByText(captured.instruction)).toBeTruthy();
  });

  it('a refused read is said, and never drawn as the Chief\'s standing, the charter or the Board', async () => {
    const refused: Reply = { status: 503, body: { detail: 'the store could not be read' } };
    serve({ model: refused, status: refused, charter: refused });
    render(<BoardOfDirectors />);
    const err = await screen.findByTestId('chief-model-error');
    expect(err.textContent).toContain('Failed (HTTP 503): the store could not be read');
    expect(screen.queryByTestId('chief-model-role')).toBeNull();
    expect(screen.queryByTestId('chief-model-twin')).toBeNull();
    expect(screen.queryByTestId('board-ratification-duty')).toBeNull();
    expect((await screen.findAllByText(/Could not load the board (status|charter) — Failed \(HTTP 503\)/)).length).toBeGreaterThan(0);
    expect(screen.queryByText('The Board')).toBeNull();
  });

  it('a topic the floor framed says so with the server\'s basis, and the list re-read shows it framed', async () => {
    const t = captured.topic_answer;
    serve({ statusAfter: ok(captured.status_after_topic) });
    render(<BoardOfDirectors />);
    fireEvent.change(screen.getByTestId('board-topic'), { target: { value: captured.topic } });
    fireEvent.click(screen.getByTestId('board-topic-submit'));
    expect((await screen.findByTestId('board-topic-status')).textContent).toBe('Framed by the floor — not deliberated');
    expect(text('board-topic-status-basis')).toBe(t.status_basis);
    const chips = await screen.findAllByTestId('deliberation-status');
    expect(chips.map(c => c.textContent)).toContain('framed by the floor — not deliberated');
    expect(chips[0].getAttribute('title')).toBe(t.status_basis);
  });

  it('a topic the server refuses is said, and nothing is shown as a result', async () => {
    serve({ directive: { status: 422, body: { detail: 'a topic names what the Board is to decide' } } });
    render(<BoardOfDirectors />);
    fireEvent.change(screen.getByTestId('board-topic'), { target: { value: 'x' } });
    fireEvent.click(screen.getByTestId('board-topic-submit'));
    expect((await screen.findByTestId('board-topic-error')).textContent)
      .toBe('Not put to the Board: Failed (HTTP 422): a topic names what the Board is to decide');
    expect(screen.queryByTestId('board-topic-result')).toBeNull();
  });

  it('a change a review approved waits; ratified on your direction, the decision is said as the server recorded it', async () => {
    const row = captured.pending.pending[0];
    const r = captured.ratified;
    let queue: Reply = ok(captured.pending);
    serve({});
    vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
      const reply = ({ status, body }: Reply) => ({ ok: status < 400, status, statusText: '', json: async () => body });
      if (url === '/api/v1/board/ratifications' && init?.method !== 'POST') return reply(queue);
      if (url === `/api/v1/board/ratifications/${row.cca_id}` && init?.method === 'POST') {
        queue = ok(captured.ratifications_empty);
        return reply(ok(r));
      }
      if (url === '/api/v1/board/chief/model') return reply(ok(captured.model_role));
      if (url === '/api/v1/board/charter') return reply(ok(captured.charter));
      return reply(ok(captured.status));
    }));
    render(<BoardOfDirectors />);
    const card = await screen.findByTestId('board-ratification-row');
    expect(within(card).getByText(row.title)).toBeTruthy();
    expect(card.textContent).toContain('approved by: the reviewing model’s decision marker');
    expect((within(card).getByTestId('board-ratify') as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(within(card).getByTestId('board-ratification-owner-direction'));
    fireEvent.click(within(card).getByTestId('board-ratify'));
    expect((await screen.findByTestId('board-ratification-result')).textContent)
      .toBe(`${row.cca_id}: ${r.decision.toUpperCase()} — ${r.note} Recorded on the constitutional ledger.`);
    expect(screen.queryByTestId('board-ratification-row')).toBeNull();
  });

  it('a decision the server refuses is said on the row, which stays waiting', async () => {
    const row = captured.pending.pending[0];
    serve({ ratifications: ok(captured.pending),
            ratify: { status: 409, body: { detail: 'this change is no longer awaiting ratification' } } });
    render(<BoardOfDirectors />);
    const card = await screen.findByTestId('board-ratification-row');
    fireEvent.click(within(card).getByTestId('board-ratification-owner-direction'));
    fireEvent.click(within(card).getByTestId('board-refuse'));
    expect(await within(card).findByText('Failed (HTTP 409): this change is no longer awaiting ratification')).toBeTruthy();
    expect(screen.queryByTestId('board-ratification-result')).toBeNull();
    expect(screen.getByTestId('board-ratification-row')).toBeTruthy();
    expect(row.decision_source_inferred).toBe(false);
  });

  it('a row whose source was read from its shape says so, and a restated directive is not shown as yours', async () => {
    const pending = clone(captured.pending);
    Object.assign(pending.pending[0], { decision_source: 'unrecorded_decision', decision_source_inferred: true });
    const status = clone(captured.status_after_instruction);
    const mine = status.recent_directives.find((d: { instruction?: string }) => d.instruction === captured.instruction);
    Object.assign(mine, { unprompted: true, restated_kind: 'decision', instruction_source: 'restated by the Chief on a beat' });
    serve({ ratifications: ok(pending), status: ok(status) });
    render(<BoardOfDirectors />);
    const card = await screen.findByTestId('board-ratification-row');
    expect(card.textContent).toContain('a decision made before W459 that recorded no source (read as a review’s)');
    expect(within(card).getByTestId('ratification-source-inferred').textContent)
      .toBe(' (read from the record’s shape; the record itself names no source)');
    expect((await screen.findByTestId('directive-unprompted')).getAttribute('title')).toBe('restated by the Chief on a beat');
    expect(text('directive-restated-kind')).toBe('restates your last recorded decision');
  });

  it('an instruction filed through the floor shows the Chief\'s standing beside it and the server\'s reason', async () => {
    const a = captured.instruct_answer;
    serve({ model: ok(captured.model_twin) });
    render(<BoardOfDirectors />);
    fireEvent.change(screen.getByPlaceholderText(/Give your Chief an instruction/), { target: { value: captured.instruction } });
    fireEvent.click(screen.getByText('Issue Instruction'));
    expect((await screen.findByTestId('chief-directive-reason')).textContent).toBe(a.directive_reason);
    expect(within(screen.getByTestId('chief-standing-with-output')).getByTestId('chief-model-twin')).toBeTruthy();
  });
});
