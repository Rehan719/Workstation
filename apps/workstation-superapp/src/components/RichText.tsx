// W1238 - ONE RENDERER FOR A REPLY'S TEXT, shared by the AI CEO chat (pages/CEOChat.tsx) and the footer's conversation
// panel (components/avatar/ConversationPanel.tsx). The CEO chat printed a reply as plain text, so the structured
// floor's frame reached the reader as raw markdown ("## Assessment", "- term", "_[...]_"); the panel had its own
// smaller renderer (bold, inline code and bullets only), which this replaces.
//
// It builds React elements only. No raw HTML is set anywhere, so whatever a reply carries is shown as text, and it
// makes no link: a markdown link, an address or an anchor tag in a reply is shown as typed and cannot be followed.
// Each line is read in one pass, so a long line of markers with no partner cannot stall the page, and a value that
// is not a string is shown as its text instead of failing the render.
//   a line '# ' to '###### '     a heading (the hashes and the space are not shown)
//   a line '- '                  an item of a list; consecutive items are one list
//   an empty line                a gap; a run of empty lines is one gap
//   any other line               a line of its own
//   inline **bold**, `code` and _italic_. An underscore opens an italic only at the line's start or after a character
//   that is not a letter or a digit, and closes it only at the line's end or before one, so a name such as
//   AI_ALLOW_EXTERNAL keeps its underscores. A marker with no partner is shown as typed.
import React from 'react';

export type InlinePart = { kind: 'text' | 'bold' | 'code' | 'em'; text: string };

const isWordChar = (ch: string | undefined): boolean => !!ch && /[\p{L}\p{N}]/u.test(ch);

/** The line's inline parts, in order: bold, code, italic and the plain text between them. */
export function inlineParts(line: string): InlinePart[] {
  const out: InlinePart[] = [];
  let plain = '';
  const flush = () => { if (plain) { out.push({ kind: 'text', text: plain }); plain = ''; } };
  //  no closing underscore stands at or after this index. Whether an underscore closes does not depend on the one
  //  that opened, so once a scan finds no closer no later opener scans again: one pass, however many openers
  let noCloser = line.length;
  let i = 0;
  while (i < line.length) {
    if (line.startsWith('**', i)) {
      const end = line.indexOf('**', i + 2);
      if (end > i + 2) { flush(); out.push({ kind: 'bold', text: line.slice(i + 2, end) }); i = end + 2; continue; }
    } else if (line[i] === '`') {
      const end = line.indexOf('`', i + 1);
      if (end > i + 1) { flush(); out.push({ kind: 'code', text: line.slice(i + 1, end) }); i = end + 1; continue; }
    } else if (line[i] === '_' && !isWordChar(line[i - 1]) && line[i + 1] !== undefined && line[i + 1] !== ' ' && line[i + 1] !== '_') {
      let end = -1;
      for (let j = i + 2; j < noCloser; j++) {
        if (line[j] === '_' && line[j - 1] !== ' ' && !isWordChar(line[j + 1])) { end = j; break; }
      }
      if (end < 0) noCloser = Math.min(noCloser, i + 2);
      if (end > 0) { flush(); out.push({ kind: 'em', text: line.slice(i + 1, end) }); i = end + 1; continue; }
    }
    plain += line[i];
    i += 1;
  }
  flush();
  return out;
}

function inline(line: string): React.ReactNode[] {
  return inlineParts(line).map((p, k) => {
    if (p.kind === 'bold') return <strong key={k} className="font-bold text-white">{p.text}</strong>;
    if (p.kind === 'code') return <code key={k} className="px-1 py-0.5 rounded bg-black/30 text-aura font-mono text-[11px]">{p.text}</code>;
    if (p.kind === 'em') return <em key={k} className="italic">{p.text}</em>;
    return <React.Fragment key={k}>{p.text}</React.Fragment>;
  });
}

const HEADING = /^(#{1,6}) +(.*)$/;
const HEADING_TAG = ['h3', 'h4', 'h5', 'h6', 'h6', 'h6'] as const;

/** The text as React elements: headings, lists, gaps and lines, each line's inline parts rendered. */
export function renderRichText(text: string): React.ReactNode[] {
  const out: React.ReactNode[] = [];
  let items: string[] = [];
  let gap = false;
  const endList = () => {
    if (!items.length) return;
    out.push(
      <ul key={`ul${out.length}`} className="space-y-0.5">
        {items.map((it, k) => (
          <li key={k} className="flex gap-2 pl-1"><span aria-hidden="true" className="text-aura">•</span><span>{inline(it)}</span></li>
        ))}
      </ul>);
    items = [];
  };
  for (const raw of String(text ?? '').split('\n')) {
    const line = raw.trimEnd();
    const lead = line.trimStart();
    if (!lead) { endList(); gap = out.length > 0; continue; }
    if (gap) { out.push(<div key={`gap${out.length}`} aria-hidden="true" className="h-2" />); gap = false; }
    if (lead.startsWith('- ')) { items.push(lead.slice(2)); continue; }
    endList();
    const h = HEADING.exec(lead);
    if (h) {
      out.push(React.createElement(HEADING_TAG[h[1].length - 1],
        { key: `h${out.length}`, className: 'font-black text-white mt-1' }, inline(h[2])));
      continue;
    }
    out.push(<p key={`p${out.length}`}>{inline(line)}</p>);
  }
  endList();
  return out;
}

/** A reply's text, rendered. */
export const RichText: React.FC<{ text: string }> = ({ text }) => <>{renderRichText(text)}</>;
