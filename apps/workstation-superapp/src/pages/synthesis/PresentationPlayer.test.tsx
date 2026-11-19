// W1023 (FU-399 part 49) — the deck player, rendered against a deck the route composed.
//
// The synthesis studio opens a deck in this player, from /generate's answer for a presentation. With no model the
// route answers a note that none came back, which the studio does not open (W1021), so the deck here is the route's
// answer to a reply made up for the capture and run through it (PresentationPlayer.fixture.json): three slides, one
// with a list, one with no narration, from a made-up local model. Each is drawn as the studio opens it: the slides,
// and the result's served_by and is_external beside them.
//
// Each is drawn inside StrictMode, as main.tsx renders the app. Rendering found four defects, fixed in this round:
// - the header called every deck an "AI CEO Presentation", whatever composed it; it says what composed it;
// - a deck with no slide took the player down; it says there is nothing to play;
// - a slide with no narration showed an empty pair of quotes as its script; it says the slide has none;
// - a slide's named image was drawn as a box holding its file name; it says the player does not show it.
import { act, fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import captured from './PresentationPlayer.fixture.json';
import { PresentationPlayer } from './PresentationPlayer';

const { answer, slides } = captured;

function open(deck = slides as any[], onClose = () => {}) {
  return render(
    <React.StrictMode>
      <PresentationPlayer slides={deck} servedBy={answer.served_by} isExternal={answer.is_external} onClose={onClose} />
    </React.StrictMode>,
  );
}

//  time passing as it does in a browser: the slide timer ticks every 100 ms, and the page is drawn between ticks
function elapse(ms: number) {
  for (let t = 0; t < ms; t += 100) act(() => { vi.advanceTimersByTime(100); });
}

describe('PresentationPlayer, a deck the route composed', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  it('says what composed the deck, and opens on its first slide with that slide\'s script', () => {
    open();
    expect(screen.getByTestId('player-provenance').textContent).toBe(`in-house · ${answer.served_by}`);
    expect(screen.queryByText(/AI CEO/)).toBeNull();
    expect(screen.getByText(`Slide 1 of ${slides.length}`)).toBeTruthy();
    expect(screen.getByTestId('player-narration').textContent).toBe(`"${slides[0].narration}"`);
    // the outline lists every slide the deck has, in order
    for (const [i, s] of slides.entries()) expect(screen.getByText(`${i + 1}. ${s.title}`)).toBeTruthy();
  });

  it('moves by its controls and its outline, and says a slide with no narration has none', () => {
    open();
    fireEvent.click(screen.getByRole('button', { name: 'Next slide' }));
    expect(screen.getByText(`Slide 2 of ${slides.length}`)).toBeTruthy();
    expect(screen.getByTestId('player-narration').textContent).toBe(`"${slides[1].narration}"`);
    fireEvent.click(screen.getByText(`3. ${slides[2].title}`));
    expect(screen.getByText(`Slide 3 of ${slides.length}`)).toBeTruthy();
    expect(slides[2].narration).toBe('');
    expect(screen.getByTestId('player-narration').textContent).toBe('This slide has no narration.');
    fireEvent.click(screen.getByRole('button', { name: 'Previous slide' }));
    expect(screen.getByText(`Slide 2 of ${slides.length}`)).toBeTruthy();
  });

  it('advances by itself every five seconds, stops on the last slide, and holds while paused', () => {
    open();
    elapse(5200);
    expect(screen.getByText(`Slide 2 of ${slides.length}`)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Pause' }));
    elapse(20000);
    expect(screen.getByText(`Slide 2 of ${slides.length}`)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Play' }));
    elapse(30000);
    expect(screen.getByText(`Slide ${slides.length} of ${slides.length}`)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Play' })).toBeTruthy();     // it stopped, and offers to play again
  });

  it('says a deck with no slide has nothing to play, and offers only to close', () => {
    const onClose = vi.fn();
    open([], onClose);
    expect(screen.getByTestId('player-nothing-to-play').textContent).toBe('This deck has no slide, so there is nothing to play.');
    expect(screen.getAllByRole('button').map(b => b.textContent)).toEqual(['Close']);
    fireEvent.click(screen.getByRole('button', { name: 'Close' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
