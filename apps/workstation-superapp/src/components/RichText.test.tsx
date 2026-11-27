// W1238 — the shared renderer for a reply's text (components/RichText.tsx), rendered.
//
// The AI CEO chat printed a reply as plain text, so the structured floor's frame reached the reader as raw markdown;
// the footer's conversation panel had a smaller renderer of its own. Both now render through RichText, which builds
// React elements only. The page-level test (pages/CEOChat.test.tsx) renders the floor's own reply in the chat; this
// one holds each rule of the renderer on made-up text.
import { render } from '@testing-library/react';
import React from 'react';
import { describe, expect, it } from 'vitest';

import { RichText, inlineParts } from './RichText';

const shown = (text: string) => render(<RichText text={text} />).container;

describe('RichText, a reply\'s text rendered as elements', () => {
  it('renders a heading for a "## " line and a list for "- " lines, with no marker left', () => {
    const box = shown('_[W1238 made up: a banner]_\n\n## Assessment\n- first term\n- second term\n\n## Next actions\n- check it');
    expect([...box.querySelectorAll('h4')].map(h => h.textContent)).toEqual(['Assessment', 'Next actions']);
    expect(box.querySelectorAll('ul').length).toBe(2);
    expect([...box.querySelectorAll('li')].map(li => li.textContent)).toEqual(['•first term', '•second term', '•check it']);
    expect(box.querySelector('em')?.textContent).toBe('[W1238 made up: a banner]');
    expect(box.textContent).not.toContain('##');
    expect(box.textContent).not.toContain('_[');
    for (const el of box.querySelectorAll('p, li, h3, h4, h5, h6')) expect(el.textContent?.startsWith('- ')).toBe(false);
  });

  it('gives each heading level its own element and keeps a line with no space after the hashes as a line', () => {
    const box = shown('# One\n### Three\n#hashtag');
    expect(box.querySelector('h3')?.textContent).toBe('One');
    expect(box.querySelector('h5')?.textContent).toBe('Three');
    expect(box.querySelector('p')?.textContent).toBe('#hashtag');
  });

  it('renders bold, inline code and italics, and keeps the underscores of a name', () => {
    expect(inlineParts('a **bold** b `code` c _said_ d')).toEqual([
      { kind: 'text', text: 'a ' }, { kind: 'bold', text: 'bold' }, { kind: 'text', text: ' b ' },
      { kind: 'code', text: 'code' }, { kind: 'text', text: ' c ' }, { kind: 'em', text: 'said' }, { kind: 'text', text: ' d' }]);
    expect(inlineParts('set AI_ALLOW_EXTERNAL and snake_case_name here')).toEqual([
      { kind: 'text', text: 'set AI_ALLOW_EXTERNAL and snake_case_name here' }]);
    expect(inlineParts('keep snake_case and other_ name')).toEqual([{ kind: 'text', text: 'keep snake_case and other_ name' }]);
    expect(inlineParts('_see AI_ALLOW_EXTERNAL here_')).toEqual([{ kind: 'em', text: 'see AI_ALLOW_EXTERNAL here' }]);
    const box = shown('**open and `open and _open');
    expect(box.textContent).toBe('**open and `open and _open');
    expect(box.querySelector('strong, code, em')).toBeNull();
  });

  it('keeps each line apart, and a run of empty lines is one gap', () => {
    const box = shown('first line\nsecond line\n\n\n\nthird line\n');
    expect([...box.querySelectorAll('p')].map(p => p.textContent)).toEqual(['first line', 'second line', 'third line']);
    expect(box.querySelectorAll('div[aria-hidden="true"]').length).toBe(1);
  });

  it('shows markup in a reply as text and never as HTML', () => {
    const box = shown('<b>W1238 made up</b> <img src="x" onerror="alert(1)">\n- <i>item</i>');
    expect(box.querySelector('b, img, i')).toBeNull();
    expect(box.textContent).toContain('<b>W1238 made up</b> <img src="x" onerror="alert(1)">');
    expect(box.querySelector('li')?.textContent).toBe('•<i>item</i>');
  });

  it('makes no link, so a link a reply carries is shown as typed and cannot be followed', () => {
    const box = shown('[W1238 made up](javascript:alert(1))\n- <a href="javascript:alert(1)">W1238 made up</a>');
    expect(box.querySelector('a, [href]')).toBeNull();
    expect(box.querySelector('p')?.textContent).toBe('[W1238 made up](javascript:alert(1))');
    expect(box.querySelector('li')?.textContent).toBe('•<a href="javascript:alert(1)">W1238 made up</a>');
  });

  it('reads a long line of markers with no partner in one pass, so no reply can stall the page', () => {
    const line = ' _a'.repeat(60000) + ' **b `c';
    const started = performance.now();
    const parts = inlineParts(line);
    const took = performance.now() - started;
    expect(parts).toEqual([{ kind: 'text', text: line }]);
    expect(took).toBeLessThan(1000);
  });

  it('shows a value that is not a string as its text instead of failing', () => {
    expect(shown(42 as unknown as string).textContent).toBe('42');
    expect(shown(undefined as unknown as string).textContent).toBe('');
  });
});
