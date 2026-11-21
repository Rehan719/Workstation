//  W1167 (P5.11 clause 7) - A SUBJECT THAT IS REGULATED ADVICE, as its row says it: who regulates it, the pages' own
//  words, the places they name for each nation, the pages read with the day each was read, and its regulator's own
//  page: read, with the day, or not read and why. Every word is the server's but the heading and the joining ones;
//  nothing here is said as advice. W1181 - each quoted sentence says the page it is from, the one the route named for it.
import React from 'react';
import { UrgentPlace, UrgentSource, urgentPlaceSaid, urgentSourceSaid } from './UrgentRoutes';

export type Boundary = {
  id: string; subject: string; regulated: string; words: string[]; words_from?: (string | null)[]; places: UrgentPlace[];
  sources: UrgentSource[];
  regulator: { name: string | null; read: boolean; page: UrgentSource | null; why: string | null };
};

//  the regulator's own page as the row says it: read, with when; not read, and why; or no regulator's page at all
export const regulatorSaid = (r: Boundary['regulator']) =>
  (r.read && r.page ? `Regulator: ${r.name}. Its own page was read: ${urgentSourceSaid(r.page)}.`
    : r.name ? `Regulator: ${r.name}. Its own page was not read: ${r.why}.`
      : `No regulator's page was read: ${r.why}.`);

//  a page that reads the box by a test id of its own wraps it in an element that carries that id in its own source
export default function RegulatedBoundary({ b }: { b: Boundary }) {
  return (
    <section data-testid="regulated-boundary" aria-label="Regulated advice"
      className="p-3 rounded-xl bg-slate-950 border border-sky-500/30 space-y-1">
      <p data-testid="boundary-subject" className="text-[11px] font-bold text-sky-300">{b.subject}: regulated advice, not answered here</p>
      <p data-testid="boundary-regulated" className="text-[10px] text-slate-300">{b.regulated}.</p>
      {b.words.length > 0 && (
        <ul className="list-disc ml-5 text-[10px] text-slate-300 space-y-0.5">
          {/* W1181 - each quote, then the page the route named for it; no page is named that the route did not */}
          {b.words.map((w, i) => {
            const from = b.sources.find(s => s.id === b.words_from?.[i]);
            return (
              <li key={w}>
                <span data-testid="boundary-words">{w}</span>
                {from && <span data-testid="boundary-words-from" className="text-slate-500"> ({from.name ?? from.id})</span>}
              </li>
            );
          })}
        </ul>
      )}
      {b.places.length > 0 && (
        <ul className="ml-5 text-[10px] text-slate-300 space-y-0.5">
          {b.places.map(p => (
            <li key={`${p.nation}|${p.name}`} data-testid="boundary-place">
              {p.link
                ? <a href={p.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{urgentPlaceSaid(p)}</a>
                : urgentPlaceSaid(p)}
            </li>
          ))}
        </ul>
      )}
      <p data-testid="boundary-read" className="text-[9px] text-slate-500">Read: {b.sources.map(urgentSourceSaid).join('; ')}.</p>
      <p data-testid="boundary-regulator" className="text-[9px] text-slate-500">{regulatorSaid(b.regulator)}</p>
    </section>
  );
}
