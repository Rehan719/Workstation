// W1033 — the Contribute page, rendered. It reads nothing; what it offers is two links out and a statement of what is
// not connected. Rendering found that it offered a forum and a chat server that do not exist: two buttons whose only
// action was to say "not implemented". It now says there is neither, and opens the repository's discussions, which
// exist.
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { Contribute } from './Contribute';

const REPO = 'https://github.com/Rehan719/Workstation';

describe('Contribute, rendered', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('says there is no forum and no chat server, and opens the repository\'s discussions', () => {
    const open = vi.spyOn(window, 'open').mockImplementation(() => null);
    render(<Contribute />);
    expect(screen.getByTestId('contribute-no-forum').textContent?.trim())
      .toBe('There is no forum and no chat server. Discussion is on the repository.');
    fireEvent.click(screen.getByRole('button', { name: "Open the repository's discussions" }));
    expect(open).toHaveBeenCalledWith(`${REPO}/discussions`, '_blank', 'noopener,noreferrer');
    expect(screen.queryByRole('button', { name: /Discourse|Discord/ })).toBeNull();
    expect(document.querySelector('[data-notimpl-toast]')).toBeNull();
  });

  it('opens the repository from the header', () => {
    const open = vi.spyOn(window, 'open').mockImplementation(() => null);
    render(<Contribute />);
    fireEvent.click(screen.getByRole('button', { name: /View Source/ }));
    expect(open).toHaveBeenCalledWith(REPO, '_blank', 'noopener,noreferrer');
  });
});
