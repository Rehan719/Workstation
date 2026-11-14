// W968 (P5.14 clause 6) — the one shape of a question to a person, rendered: its kind, what each option does and what
// undoing it costs, the one recommended option, and an act that cannot be undone held until its name is typed back.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { describe, expect, it, vi } from 'vitest';

import { AskPerson, KIND_SAID } from './AskPerson';

const OPTIONS = [
  { id: 'delete', label: 'Delete the project', differs: 'its record is removed', undo: 'it cannot be undone' },
  { id: 'keep', label: 'Keep it', differs: 'nothing changes', undo: 'nothing to undo', recommended: true },
];
const [DEL, KEEP] = OPTIONS.map(o => o.id);

describe('AskPerson, rendered', () => {
  it('says its kind, what each option does, what undoing it costs, and which is recommended', () => {
    render(<AskPerson question="Delete the project W968?" kind="confirmation" options={OPTIONS} onChoose={() => {}} />);
    expect(screen.getByTestId('ask-question').textContent).toBe('Delete the project W968?');
    expect(screen.getByTestId('ask-kind').textContent).toBe(KIND_SAID.confirmation);
    expect(screen.getByTestId(`ask-option-${DEL}`).textContent).toContain('What it does: its record is removed');
    expect(screen.getByTestId(`ask-option-${DEL}`).textContent).toContain('To undo it: it cannot be undone');
    expect(screen.queryByTestId(`ask-recommended-${DEL}`)).toBeNull();
    expect(screen.getByTestId(`ask-recommended-${KEEP}`).textContent).toBe('Recommended');
  });

  it('a decision says it is one', () => {
    render(<AskPerson question="Which?" kind="decision" options={OPTIONS} onChoose={() => {}} />);
    expect(screen.getByTestId('ask-kind').textContent).toBe(KIND_SAID.decision);
  });

  it('an act that cannot be undone waits until its name is typed back exactly, then is chosen', () => {
    const chose = vi.fn();
    render(<AskPerson question="Delete the project W968?" kind="confirmation" options={OPTIONS}
      typeBack={{ optionId: 'delete', text: 'W968 project', label: "Type the project's title to delete it" }} onChoose={chose} />);
    const del = screen.getByTestId(`ask-choose-${DEL}`) as HTMLButtonElement;
    expect(del.disabled).toBe(true);
    fireEvent.click(del);
    expect(chose).not.toHaveBeenCalled();
    fireEvent.change(screen.getByLabelText("Type the project's title to delete it"), { target: { value: 'W968 projec' } });
    expect(del.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("Type the project's title to delete it"), { target: { value: 'W968 project' } });
    expect(del.disabled).toBe(false);
    fireEvent.click(del);
    expect(chose).toHaveBeenCalledWith('delete');
  });

  it('the option that can be undone is never held', () => {
    const chose = vi.fn();
    render(<AskPerson question="Delete?" kind="confirmation" options={OPTIONS}
      typeBack={{ optionId: 'delete', text: 'x', label: 'Type x' }} onChoose={chose} />);
    fireEvent.click(screen.getByTestId(`ask-choose-${KEEP}`));
    expect(chose).toHaveBeenCalledWith('keep');
  });
});
