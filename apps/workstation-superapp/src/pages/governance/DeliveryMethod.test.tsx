// W974 (FU-399 part 8) — the Delivery Method page, rendered against the method routes' own answers.
//
// What a person reads on this page are claims about how this platform holds its own discipline: how much of it a tool
// enforces, the defect behind every rule, which rules have been recorded broken, what the pace figure cannot know, and
// which defect classes no screen can find. Seven guards read the page's source. This mounts the real page against the
// answers the four method routes gave on a fresh store (DeliveryMethod.fixture.json, captured by w974_capture.py),
// reads each claim in the DOM, and has the server refuse each read in turn.
import { fireEvent, render, screen, within } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './DeliveryMethod.fixture.json';
import { DeliveryMethod } from './DeliveryMethod';

type Reply = { status: number; body: unknown; statusText?: string; notJson?: boolean };
type Answers = Partial<Record<'method' | 'classes' | 'forecast' | 'learning', Reply>>;
const ok = (body: unknown): Reply => ({ status: 200, body });
const refused = (detail: string): Reply => ({ status: 503, body: { detail } });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const clone = (x: any) => JSON.parse(JSON.stringify(x));

function serve(a: Answers) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const reply = ({ status, body, statusText, notJson }: Reply) => ({
      ok: status < 400, status, statusText: statusText ?? '',
      json: async () => {
        if (notJson) throw new SyntaxError('Unexpected token \'<\', "<html>" is not valid JSON');
        return body;
      },
    });
    if (url === '/api/v1/method') return reply(a.method ?? ok(captured.method));
    if (url === '/api/v1/method/defect-classes') return reply(a.classes ?? ok(captured.classes));
    if (url === '/api/v1/method/forecast') return reply(a.forecast ?? ok(captured.forecast));
    if (url === '/api/v1/method/learning') return reply(a.learning ?? ok(captured.learning_none));
    return reply({ status: 404, body: { detail: `not served in this test: ${url}` } });
  }));
}

const text = (id: string) => screen.getByTestId(id).textContent ?? '';
const lessons = captured.method.lessons;

describe('DeliveryMethod, rendered against the method routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('the headline is the enforced share the server reports, and the page says it is not a badge', async () => {
    serve({});
    render(<DeliveryMethod />);
    const e = captured.method.enforcement;
    const head = await screen.findByTestId('method-enforcement');
    expect(head.textContent).toContain(`${e.mechanically_enforced} of ${e.lessons_total} mechanically enforced`);
    expect(head.textContent).toContain(`${e.judgement_only} judgement only`);
    expect(text('method-not-a-badge')).toContain('This is not a compliance badge.');
    expect(screen.getByText(e.basis)).toBeTruthy();
  });

  it('every lesson is a card with the defect that produced it; an unenforced one says why nothing enforces it', async () => {
    serve({});
    render(<DeliveryMethod />);
    const cards = await screen.findAllByTestId('method-lesson');
    expect(cards).toHaveLength(lessons.length);
    cards.forEach((card, i) => {
      const l = lessons[i];
      expect(within(card).getByText(l.rule)).toBeTruthy();
      expect(within(card).getByTestId('method-defect').textContent).toContain(l.defect);
      if ((l.enforced_by ?? '').trim()) {
        expect(card.textContent).toContain(`Caught by · ${l.enforced_by}`);
        expect(card.textContent).not.toContain('Nothing enforces this');
      } else {
        expect(card.textContent).toContain(
          `Nothing enforces this · ${l.why_not_enforced || 'no reason is recorded, which is itself a gap'}`);
      }
      const ratified = within(card).queryByTestId('lesson-ratified');
      expect(Boolean(ratified)).toBe(Boolean(l.ratified));
      if (l.ratified) expect(ratified?.textContent).toContain(String(l.ratified));
    });
  });

  it('every group has a label, and choosing one shows that group\'s lessons and mechanisms only', async () => {
    serve({});
    render(<DeliveryMethod />);
    await screen.findAllByTestId('method-lesson');
    expect(screen.getByRole('button', { name: `All ${lessons.length}` })).toBeTruthy();
    for (const g of captured.method.groups) {
      const n = lessons.filter(l => l.group === g).length;
      const button = screen.getAllByRole('button').find(b => (b.textContent ?? '').endsWith(` ${n}`)
        && (b.textContent ?? '').toLowerCase().startsWith(g.slice(0, 4)));
      expect(button, `no labelled button for the group ${g}`).toBeTruthy();
      expect(button?.textContent?.startsWith(g), `the group ${g} is shown as its raw slug`).toBe(false);
    }
    const appraisal = lessons.filter(l => l.group === 'appraisal');
    fireEvent.click(screen.getByRole('button', { name: `Appraisal ${appraisal.length}` }));
    expect(screen.getAllByTestId('method-lesson')).toHaveLength(appraisal.length);
    const mech = captured.method.mechanisms.filter(m => m.group === 'appraisal');
    expect(screen.queryAllByTestId('method-mechanism')).toHaveLength(mech.length);
  });

  it('with no breach recorded, the loop says none is recorded, not that none happened, and what it cannot see', async () => {
    serve({});
    render(<DeliveryMethod />);
    const none = await screen.findByTestId('learning-none-recorded');
    expect(none.textContent).toContain('this is not a statement that none has happened');
    expect(screen.queryAllByTestId('learning-breach')).toHaveLength(0);
    expect(text('learning-limit')).toBe(captured.learning_none.what_this_cannot_see);
    const c = captured.learning_none.currency;
    expect(text('learning-currency')).toContain(
      `The latest round a lesson cites is W${c.latest_round_a_lesson_cites}; the latest round in the history is ` +
      `W${c.latest_round_the_history_declares} (${c.rounds_since_the_method_last_learned} round ids later).`);
    expect(text('learning-currency')).toContain(c.basis);
  });

  it('recorded breaches are listed by count, and one at the threshold says a change was raised for a tool', async () => {
    serve({ learning: ok(captured.learning_breached) });
    render(<DeliveryMethod />);
    const rows = await screen.findAllByTestId('learning-breach');
    expect(rows).toHaveLength(captured.learning_breached.breached.length);
    expect(screen.queryByTestId('learning-none-recorded')).toBeNull();
    const at = rows.find(r => r.textContent?.includes(captured.breached_at_threshold));
    const once = rows.find(r => r.textContent?.includes(captured.breached_once));
    expect(at?.textContent).toContain('3×');
    expect(at?.textContent).toContain('At the threshold and nothing enforces it');
    expect(once?.textContent).toContain('1×');
    expect(once?.textContent).not.toContain('At the threshold');
  });

  it('the pace discipline is drawn from the response: the lever, the over-statement, the cost, the ruling and the limits', async () => {
    serve({});
    render(<DeliveryMethod />);
    const f = captured.forecast;
    const lever = await screen.findByTestId('pace-lever');
    expect(lever.textContent).toContain(`${f.which_rate_measures_completion.rows_per_round} rows per round`);
    expect(lever.textContent).toContain(f.which_rate_measures_completion.the_lever);
    expect(text('pace-overstates')).toContain(f.the_count_overstates.why_it_is_an_upper_bound);
    expect(text('pace-cost')).toContain(`dominated by ${f.cost_of_a_round.dominated_by}`);
    expect(text('pace-limit')).toBe(f.limits);
    expect(screen.getByText(f.projection_computed_by)).toBeTruthy();
  });

  it('the classes: one card per class, and those no screen can find are named, never reported clear', async () => {
    serve({});
    render(<DeliveryMethod />);
    const k = captured.classes;
    expect(await screen.findAllByTestId('defect-class')).toHaveLength(k.defect_classes.length);
    expect(text('classes-basis')).toBe(k.basis);
    const hidden = screen.getByTestId('classes-not-screenable');
    for (const n of k.not_screenable) expect(hidden.textContent).toContain(n.defect_class);
    expect(hidden.textContent).toContain('No screen can find these — they are not reported clear');
  });

  it('with every class screenable, no block claims some are not', async () => {
    const k = clone(captured.classes);
    k.not_screenable = [];
    serve({ classes: ok(k) });
    render(<DeliveryMethod />);
    await screen.findAllByTestId('defect-class');
    expect(screen.queryByTestId('classes-not-screenable')).toBeNull();
  });

  it('a refused method is said with its status and the server\'s reason, and never as a platform with no method', async () => {
    serve({ method: refused('the method register could not be read') });
    render(<DeliveryMethod />);
    const said = await screen.findByTestId('method-unavailable');
    expect(said.textContent).toContain('Failed (HTTP 503): the method register could not be read');
    expect(said.textContent).toContain('This is not a statement that the platform holds no method.');
    expect(screen.queryAllByTestId('method-lesson')).toHaveLength(0);
  });

  it('a refusal whose body is not JSON is said by its status, not as a parse error', async () => {
    serve({ method: { status: 502, body: null, statusText: 'Bad Gateway', notJson: true } });
    render(<DeliveryMethod />);
    const said = await screen.findByTestId('method-unavailable');
    expect(said.textContent).toContain('Failed (HTTP 502): Bad Gateway');
    expect(said.textContent).not.toContain('is not valid JSON');
  });

  it('a refused loop, pace or class read is said in its place, and the rest of the page still stands', async () => {
    serve({ learning: refused('the breach ledger could not be read'), forecast: refused('the plan could not be read'),
            classes: refused('the class register could not be read') });
    render(<DeliveryMethod />);
    expect(await screen.findAllByTestId('method-lesson')).toHaveLength(lessons.length);
    const loop = await screen.findByTestId('learning-unavailable');
    expect(loop.textContent).toContain('Failed (HTTP 503): the breach ledger could not be read');
    expect(loop.textContent).toContain('This is not a statement that no rule has been breached.');
    expect(screen.queryByTestId('learning-none-recorded')).toBeNull();
    const pace = await screen.findByTestId('pace-unavailable');
    expect(pace.textContent).toContain('Failed (HTTP 503): the plan could not be read');
    expect(pace.textContent).toContain('No rate is substituted.');
    const cls = await screen.findByTestId('classes-unavailable');
    expect(cls.textContent).toContain('Failed (HTTP 503): the class register could not be read');
    expect(cls.textContent).toContain('This is not a statement that the method holds no classes.');
    expect(screen.queryAllByTestId('defect-class')).toHaveLength(0);
  });
});
