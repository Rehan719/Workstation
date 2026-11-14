// W1038 (FU-399 part 59) — the Creator Studio, rendered against the AI CEO's blueprint route.
//
// The studio asks the blueprint route for a blueprint from an intent, a realm and a stage, draws the blueprint's
// pipeline on the canvas, and shows its deliverable with what composed it. This mounts the real page, canvas and all,
// against what the route answered on a fresh store with no model installed (CreatorStudio.fixture.json, captured by
// w1038_capture.py: the floor's blueprint for a made-up intent, and the route's refusal of a request with no intent),
// and has the server be unreachable. Rendering found two defects, fixed in this round: "AI Generate" and the intent's
// Enter replaced a graph the person had built with no question, while only "Regenerate blueprint" asked; and the
// blueprint's name cut the intent mid-word and said nothing.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import componentRegistry from '@workstation/shared/data/component_registry.json';

import captured from './CreatorStudio.fixture.json';
import { CreatorStudio } from './CreatorStudio';

const ROUTE = '/api/v290/ceo/generate-blueprint';
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const unreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });
type Answer = { status: number; data: unknown } | 'unreached';

function serve(answer: Answer) {
  return vi.spyOn(axios, 'post').mockImplementation(async (url: string) => {
    if (url !== ROUTE) throw axiosRefusal(404, { detail: `not served here: ${url}` });
    if (answer === 'unreached') throw unreached();
    if (answer.status >= 400) throw axiosRefusal(answer.status, answer.data);
    return { status: answer.status, data: answer.data };
  });
}

const bp = captured.blueprint.body;
//  a component from the palette, which the person adds to the canvas by hand
const PALETTE = componentRegistry.categories[0].components[0].name;

//  the page asks what the capture asked: its intent, realm and stage
function ask() {
  fireEvent.change(screen.getByLabelText('Blueprint intent'), { target: { value: captured.ask.intent } });
  fireEvent.change(screen.getByLabelText('Realm'), { target: { value: captured.ask.realm } });
  fireEvent.change(screen.getByLabelText('Stage'), { target: { value: captured.ask.stage } });
}

//  a node on the canvas, by the label it is drawn with (the palette's own button is not on the canvas)
const onCanvas = (label: string) => screen.queryAllByText(label, { selector: '.react-flow__node' });

describe('CreatorStudio, rendered against the blueprint route\'s own answers', () => {
  beforeEach(() => {
    //  jsdom has no layout and so no ResizeObserver, which the canvas needs to mount
    vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} });
  });
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('draws the route\'s blueprint on an empty canvas, asking nothing, and says what composed it', async () => {
    const post = serve({ status: 200, data: bp });
    render(<CreatorStudio />);
    ask();
    fireEvent.click(screen.getByRole('button', { name: /AI Generate/ }));
    await waitFor(() => expect(screen.getByTestId('blueprint-provenance').textContent).toBe('structured floor — not model analysis'));
    expect(post).toHaveBeenCalledTimes(1);
    expect(post).toHaveBeenCalledWith(ROUTE, captured.ask);
    for (const n of bp.nodes) expect(onCanvas(`${n.label} (template)`)).toHaveLength(1);
    expect(screen.getByTestId('creator-nodes-template').textContent).toBe(bp.nodes_basis);
    //  the name the route gave: the intent cut once, between words, and marked
    expect(screen.getByText(bp.name)).toBeTruthy();
    expect(bp.name).toBe('W1038 made up: a lending library of garden tools for one… — Design Blueprint');
    expect(screen.queryByTestId('ask-person')).toBeNull();
  });

  it('"AI Generate" over a graph the person built asks first, and keeping it changes nothing', async () => {
    const post = serve({ status: 200, data: bp });
    render(<CreatorStudio />);
    fireEvent.click(screen.getByRole('button', { name: PALETTE }));
    expect(onCanvas(PALETTE)).toHaveLength(1);
    ask();
    fireEvent.click(screen.getByRole('button', { name: /AI Generate/ }));
    await waitFor(() => expect(screen.getByTestId('ask-question').textContent).toBe('Regenerate the blueprint from the intent text?'));
    expect(post).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Keep the canvas' }));
    await waitFor(() => expect(screen.queryByTestId('ask-person')).toBeNull());
    expect(post).not.toHaveBeenCalled();
    expect(onCanvas(PALETTE)).toHaveLength(1);
  });

  it('Enter in the intent field over a built graph asks first too, and replacing waits for "replace"', async () => {
    const post = serve({ status: 200, data: bp });
    render(<CreatorStudio />);
    fireEvent.click(screen.getByRole('button', { name: PALETTE }));
    ask();
    fireEvent.keyDown(screen.getByLabelText('Blueprint intent'), { key: 'Enter' });
    await waitFor(() => expect(screen.getByTestId('ask-question').textContent).toBe('Regenerate the blueprint from the intent text?'));
    expect(post).not.toHaveBeenCalled();
    const replace = screen.getByRole('button', { name: 'Regenerate and replace the canvas' }) as HTMLButtonElement;
    expect(replace.disabled).toBe(true);
    fireEvent.change(screen.getByTestId('ask-type-back'), { target: { value: 'replace' } });
    expect(replace.disabled).toBe(false);
    fireEvent.click(replace);
    await waitFor(() => expect(screen.getByTestId('blueprint-provenance').textContent).toBe('structured floor — not model analysis'));
    expect(post).toHaveBeenCalledTimes(1);
    expect(onCanvas(PALETTE)).toHaveLength(0);
    for (const n of bp.nodes) expect(onCanvas(`${n.label} (template)`)).toHaveLength(1);
  });

  it('a refused generation says the server\'s reason, a field check by its field', async () => {
    serve({ status: captured.refused.status, data: captured.refused.body });
    render(<CreatorStudio />);
    ask();
    fireEvent.click(screen.getByRole('button', { name: /AI Generate/ }));
    expect(await screen.findByText('intent: Field required')).toBeTruthy();
  });

  it('a generation the server cannot be reached for is said as one', async () => {
    serve('unreached');
    render(<CreatorStudio />);
    ask();
    fireEvent.click(screen.getByRole('button', { name: /AI Generate/ }));
    expect(await screen.findByText('Failed — backend unreachable.')).toBeTruthy();
  });
});
