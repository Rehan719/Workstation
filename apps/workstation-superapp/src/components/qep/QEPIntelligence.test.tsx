// W1072 (FU-399 part 85) — the Quran platform's intelligence layer, rendered against its routes' own answers.
//
// The layer reads the adaptation registry and the compliance audit on opening (and again after a proposal or a
// blueprint), explains how the SM-2 scheduler would schedule a review for typed inputs, proposes recommendation
// weights (a change record is filed; nothing is applied), and generates an adaptation blueprint. This mounts the real
// panel against what each route answered on a fresh store (QEPIntelligence.fixture.json, captured by
// w1072_capture.py): the registry and the audit; explanations for the panel's default inputs, for other inputs, and
// the field check of an input out of range; a weights proposal and the refusal of weights that do not sum to one; a
// blueprint for a made-up pedagogical pattern adapted from education into science; and the registry and audit
// routes' own 500s. Nothing in it was approved or applied, and it holds no religious text. Rendering found every
// action's failure said in one line at the foot of the page, an explanation of earlier inputs left standing over a
// refusal, and a registry and an audit that could not be read again still shown under "showing nothing". Fixed here.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { bodyDetail } from '../../lib/api';
import captured from './QEPIntelligence.fixture.json';
import QEPIntelligence from './QEPIntelligence';

type Answer = { status: number; body: unknown };
const REGISTRY = '/api/v1/qep/adaptation/registry';
const AUDIT = '/api/v1/qep/compliance/audit';
const XAI = '/api/v1/qep/xai/explanations?';
const asked = (inputs: Record<string, number>) => new URLSearchParams(Object.entries(inputs).map(([k, v]) => [k, String(v)])).toString();
const EXPLAINED: Record<string, Answer> = {
  [asked(captured.xai_ask)]: captured.xai,
  [asked(captured.xai_other_ask)]: captured.xai_other,
  [asked(captured.xai_out_of_range_ask)]: captured.xai_out_of_range,
};
const SEED = captured.registry.body.adaptations[0].pattern;

//  each route as it answered; each read of the registry or the audit takes the next answer in its list (the last one
//  stays), and each proposal the next in `weights`
function serve(plan: { registry?: Answer[]; audit?: Answer[]; weights?: Answer[] } = {}) {
  const lists = {
    registry: [...(plan.registry ?? [captured.registry, captured.registry_after])],
    audit: [...(plan.audit ?? [captured.audit, captured.audit_after])],
    weights: [...(plan.weights ?? [captured.weights_proposed])],
  };
  const next = (list: Answer[]) => (list.length > 1 ? list.shift()! : list[0]);
  const sent: { url: string; body?: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    sent.push({ url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    let a: Answer | undefined;
    if (url === REGISTRY) a = next(lists.registry);
    else if (url === AUDIT) a = next(lists.audit);
    else if (url.startsWith(XAI)) a = EXPLAINED[url.slice(XAI.length)];
    else if (url === '/api/v1/qep/recommendation/update') a = next(lists.weights);
    else if (url === '/api/v1/qep/adaptation/execute') a = captured.blueprint;
    a = a ?? { status: 404, body: { detail: `not served here: ${url}` } };
    const body = a.body;
    return { ok: a.status < 400, status: a.status, statusText: '', json: async () => body } as unknown as Response;
  }));
  return sent;
}

const set = (label: string, value: string | number) => fireEvent.change(screen.getByLabelText(label), { target: { value: String(value) } });
const press = (name: string) => fireEvent.click(screen.getByRole('button', { name }));
const verdict = (x: typeof captured.xai.body) => `${x.decision === 'advance' ? 'ADVANCE' : 'RESET'} → next review in ${x.next_interval_days} day(s) · new efactor ${x.new_efactor}`;

describe('QEPIntelligence, rendered against its routes\' own answers', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('reads the registry and the audit on opening, and explains the default inputs as the engine schedules them', async () => {
    serve();
    render(<QEPIntelligence />);
    await waitFor(() => expect(screen.getByText(SEED)).toBeTruthy());
    expect(screen.getByText('NOT ESTABLISHED — controls could not run')).toBeTruthy();
    press('Explain');
    await waitFor(() => expect(screen.getByText(captured.xai.body.interval_basis)).toBeTruthy());
    expect(screen.getByText(captured.xai.body.interval_basis).previousElementSibling?.textContent).toBe(verdict(captured.xai.body));
  });

  it('says an explanation it was refused beside its button, and leaves none of other inputs standing', async () => {
    serve();
    render(<QEPIntelligence />);
    press('Explain');
    await waitFor(() => expect(screen.getByText(captured.xai.body.interval_basis)).toBeTruthy());
    set('ease_factor', 5);
    press('Explain');
    await waitFor(() => expect(screen.getByTestId('qep-xai-error').textContent).toBe(
      `Not explained: Failed (HTTP 422): ${bodyDetail(captured.xai_out_of_range.body, 'no reason given')}`));
    expect(screen.queryByText(captured.xai.body.interval_basis)).toBeNull();
  });

  it('proposes the weights as the panel sends them, and says the change record filed', async () => {
    const sent = serve();
    render(<QEPIntelligence />);
    press('Propose weights');
    const p = captured.weights_proposed.body;
    await waitFor(() => expect(screen.getByText(`${p.status} — ${p.basis} Change record ${p.cca_id} (${p.change_status}).`)).toBeTruthy());
    expect(sent.find(s => s.url === '/api/v1/qep/recommendation/update')!.body).toEqual(captured.weights_ask);
    expect(screen.queryByTestId('qep-weights-error')).toBeNull();
  });

  it('says weights it was refused beside their button', async () => {
    serve({ weights: [captured.weights_bad] });
    render(<QEPIntelligence />);
    for (const k of ['ease_weight', 'interval_weight', 'quality_weight']) set(k, 0.5);
    press('Propose weights');
    await waitFor(() => expect(screen.getByTestId('qep-weights-error').textContent).toBe(
      `Not proposed: Failed (HTTP 422): ${captured.weights_bad.body.detail}`));
    expect(screen.queryByTestId('qep-xai-error')).toBeNull();
  });

  it('generates a blueprint for a pattern as the panel asks, and reads the registry again', async () => {
    const sent = serve();
    render(<QEPIntelligence />);
    await waitFor(() => expect(screen.getByText(SEED)).toBeTruthy());
    set('adaptation pattern', captured.adapt_ask.pattern);
    set('source_domain', captured.adapt_ask.source_domain);
    set('target_domain', captured.adapt_ask.target_domain);
    press('Generate blueprint');
    await waitFor(() => expect(screen.getByText(captured.blueprint.body.status_note)).toBeTruthy());
    expect(sent.find(s => s.url === '/api/v1/qep/adaptation/execute')!.body).toEqual(captured.adapt_ask);
    await waitFor(() => expect(screen.getByText(captured.adapt_ask.pattern)).toBeTruthy());
  });

  it('takes a registry and an audit it could not read again off the page, as it says', async () => {
    serve({ registry: [captured.registry, captured.registry_failed], audit: [captured.audit, captured.audit_failed] });
    render(<QEPIntelligence />);
    await waitFor(() => expect(screen.getByText(SEED)).toBeTruthy());
    set('adaptation pattern', captured.adapt_ask.pattern);
    press('Generate blueprint');   // the registry and the audit are read again after it
    await waitFor(() => expect(screen.getByText(/showing nothing rather than stale figures$/)).toBeTruthy());
    expect(screen.getByText(/showing nothing rather than stale figures$/).textContent).toBe(
      `the registry was not read: Failed (HTTP 500): ${captured.registry_failed.body.detail} · `
      + `the audit was not read: Failed (HTTP 500): ${captured.audit_failed.body.detail} — showing nothing rather than stale figures`);
    expect(screen.queryByText(SEED)).toBeNull();
    expect(screen.queryByText('NOT ESTABLISHED — controls could not run')).toBeNull();
  });
});
