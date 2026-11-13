// W911 (FU-399 part 4) — a beat's failed steps, rendered: how many, which, and each one's reason.
//
// FU-417 found a beat whose step raised inside `except Exception: pass`, so the run that failed left no record of
// the cause anywhere. Since W611 (FU-461) every beat step's failure is recorded on the beat, by name, with its
// reason, and the Heartbeat page shows it as a chip on the beat's row. A chip is a claim about what a person SEES,
// the kind FU-399 converts. This mounts the real page against the heartbeat's own answers, captured from the app's
// route before and after one real beat (HeartbeatMonitor.fixture.json), and reads the beat rows in the DOM.
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import captured from './HeartbeatMonitor.fixture.json';
import { HeartbeatMonitor } from './HeartbeatMonitor';

// answer the page's one read with a captured status, its last beat's failed steps replaced where a case says so
function serve(which: 'before' | 'after', stepsFailed?: Record<string, string>) {
  const status = JSON.parse(JSON.stringify(captured[which]));
  if (stepsFailed) status.recent[status.recent.length - 1].steps_failed = stepsFailed;
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, status: 200, json: async () => status })));
  return status;
}

function mount() {
  return render(
    <MemoryRouter>
      <HeartbeatMonitor />
    </MemoryRouter>,
  );
}

describe('HeartbeatMonitor, the beat rows, rendered', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('a real beat that raised nothing shows its row and no failure chip', async () => {
    const s = serve('after');
    expect(s.recent[s.recent.length - 1].steps_failed).toEqual({});
    mount();
    await screen.findByText(`#${s.recent[s.recent.length - 1].beat}`);
    expect(screen.queryByTestId('beat-steps-failed')).toBeNull();
    // the note on what the survival instinct reads sits where the beats are read
    expect(screen.getByTestId('heartbeat-survival-note').textContent).toContain('work budget');
  });

  it('a beat whose steps raised says how many and which, with each reason in the chip', async () => {
    serve('after', {
      cadence_refresh: "ValueError: invalid literal for int() with base 10: 'n/a'",
      metabolic_cycle: 'StoreUnavailable: the ledger could not be read whole',
    });
    mount();
    const chip = await screen.findByTestId('beat-steps-failed');
    expect(chip.textContent).toBe('2 step(s) FAILED: cadence_refresh, metabolic_cycle');
    const title = chip.getAttribute('title') ?? '';
    expect(title).toContain("cadence_refresh: ValueError: invalid literal for int()");
    expect(title).toContain('metabolic_cycle: StoreUnavailable');
  });

  it('with no beat recorded, there is no beat row and no chip', async () => {
    serve('before');
    mount();
    await screen.findByText(/^(Beating|Stopped)$/);                 // the status has loaded: the absence below is read
    expect(screen.queryByTestId('beat-steps-failed')).toBeNull();
    expect(screen.queryByTestId('heartbeat-survival-note')).toBeNull();
  });

  // W929 - the page's one read, refused: said where the page starts, with the server's reason, and nothing drawn from it
  it('a refused status read is said, with the server\'s reason', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 503, json: async () => ({ detail: 'the heartbeat store could not be read' }) })));
    mount();
    expect((await screen.findByTestId('read-failure')).textContent)
      .toBe('Could not read the heartbeat status — Failed (HTTP 503): the heartbeat store could not be read');
    expect(screen.queryByTestId('beat-steps-failed')).toBeNull();
  });
});
