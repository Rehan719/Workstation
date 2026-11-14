// W1034 (FU-399 part 56) — My Work, rendered, signed out as shipped (sign-in off; no switch turned).
//
// My Work lists the outputs the domain tools and the Genesis journeys saved in this browser. It reads them through
// lib/outputHistory, so two made-up outputs are saved here the way a tool saves one (saveOutput), and the real page is
// mounted over them. Rendering found one defect, fixed in this round: "Clear all" removed every saved output on one
// click, with no question. It now asks in AskPerson's shape (W968), and the clearing waits for "clear all" typed back.
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it } from 'vitest';

import { listOutputs, saveOutput } from '../lib/outputHistory';
import { MyWork } from './MyWork';

function seed() {
  localStorage.clear();
  saveOutput({ kind: 'domain-tool', title: 'W1034 made up: a lesson plan on fractions', domain: 'education',
               endpoint: '/api/v1/education/lesson-plan', input: 'W1034 made up: fractions for year five',
               output: 'W1034 made up: an outline of a lesson on fractions.', provenance: { served_by: 'native', is_external: false } });
  saveOutput({ kind: 'domain-tool', title: 'W1034 made up: a supporting statement', domain: 'employment',
               endpoint: '/api/v1/employment/application', input: 'W1034 made up: a bakery role',
               output: 'W1034 made up: a statement against two criteria.', provenance: { served_by: 'native', is_external: false } });
}

function mount() {
  render(<MemoryRouter><MyWork /></MemoryRouter>);
}

describe('MyWork, rendered over what this browser saved', () => {
  beforeEach(() => {
    seed();
  });

  it('lists each saved output by its title', async () => {
    mount();
    await waitFor(() => expect(screen.getByText('W1034 made up: a supporting statement').textContent).toBe('W1034 made up: a supporting statement'));
    expect(screen.getByText('W1034 made up: a lesson plan on fractions')).toBeTruthy();
  });

  it('asks before it clears every saved output, and keeping them changes nothing', async () => {
    mount();
    fireEvent.click(await screen.findByRole('button', { name: /Clear all/ }));
    await waitFor(() => expect(screen.getByTestId('ask-question').textContent).toBe('Clear all 2 saved outputs?'));
    //  each option, by its label: what it does, what undoing it costs, and which is recommended
    const option = (label: string) => screen.getByText(label, { selector: 'li > span' }).closest('li') as HTMLElement;
    expect(option('Clear them all').textContent).toContain('every saved output is removed from this browser');
    expect(option('Clear them all').textContent).toContain('it cannot be undone');
    expect(option('Keep them').textContent).toContain('Recommended');
    expect(option('Clear them all').textContent).not.toContain('Recommended');
    expect(listOutputs()).toHaveLength(2);
    fireEvent.click(screen.getByRole('button', { name: 'Keep them' }));
    await waitFor(() => expect(screen.queryByTestId('ask-person')).toBeNull());
    expect(listOutputs()).toHaveLength(2);
  });

  it('clears them only once "clear all" is typed back', async () => {
    mount();
    fireEvent.click(await screen.findByRole('button', { name: /Clear all/ }));
    const clear = screen.getByRole('button', { name: 'Clear them all' }) as HTMLButtonElement;
    expect(clear.disabled).toBe(true);
    fireEvent.change(screen.getByTestId('ask-type-back'), { target: { value: 'clear all' } });
    expect(clear.disabled).toBe(false);
    fireEvent.click(clear);
    await waitFor(() => expect(screen.getByText('No saved outputs yet').textContent).toBe('No saved outputs yet'));
    expect(listOutputs()).toHaveLength(0);
  });
});
