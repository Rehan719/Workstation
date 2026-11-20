//  W1166 (P5.11 clause 4) - THE URGENT ROUTES, drawn before anything else wherever help is said: each situation, its
//  steps in the words of the GOV.UK page that gives them, the places that page names for each nation, and the page
//  with the day it was read. Every word here is the server's but the heading and the joining ones; a page whose
//  route list could not be read says so in its own place, and nothing is drawn as if there were no route.
import React from 'react';

export type UrgentPlace = { nation: string; name: string; number: string | null; link: string | null; own_site: string };
export type UrgentSource = {
  id: string; read: boolean; name?: string; page?: string; read_on?: string; checked: string; recently_checked: boolean;
};
export type UrgentRoute = {
  id: string; situation: string; nations: string[]; steps: string[]; places: UrgentPlace[]; here: string | null;
  sources: UrgentSource[]; added_by_screen?: boolean;
};

//  a source as the panel says it: its name and when it was read, or why it is not said as read
export const urgentSourceSaid = (s: UrgentSource) => (s.read ? `${s.name}, ${s.checked}` : s.checked);

//  a place as the panel says it: its nation and name, its number when the page gives one, and whether its own site
//  was opened
export const urgentPlaceSaid = (p: UrgentPlace) =>
  `${p.nation}: ${p.name}${p.number ? `, ${p.number}` : ''} (${p.own_site})`;

//  a page that reads the box by a test id of its own wraps it in an element that carries that id in its own source
export default function UrgentRoutes({ routes, basis }: { routes: UrgentRoute[]; basis?: string }) {
  return (
    <section data-testid="urgent-routes" aria-label="If it is urgent"
      className="rounded-xl border border-rose-500/40 bg-rose-500/5 p-4 space-y-3">
      <h3 className="text-xs font-black uppercase tracking-widest text-rose-300">If it is urgent</h3>
      {routes.map(r => (
        <div key={r.id} data-testid="urgent-route" className="space-y-1">
          <p data-testid="urgent-situation" className="text-sm font-bold text-white">{r.situation}</p>
          <ul className="list-disc ml-5 text-xs text-slate-200 space-y-0.5">
            {r.steps.map(s => <li key={s} data-testid="urgent-step">{s}</li>)}
          </ul>
          {r.places.length > 0 && (
            <ul className="ml-5 text-[11px] text-slate-300 space-y-0.5">
              {r.places.map(p => (
                <li key={`${p.nation}|${p.name}`} data-testid="urgent-place">
                  {p.link
                    ? <a href={p.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{urgentPlaceSaid(p)}</a>
                    : urgentPlaceSaid(p)}
                </li>
              ))}
            </ul>
          )}
          {r.here && <p data-testid="urgent-here" className="text-[11px] text-slate-300">{r.here}</p>}
          <p data-testid="urgent-read" className="text-[10px] text-slate-500">
            Read: {r.sources.map(urgentSourceSaid).join('; ')}.
          </p>
        </div>
      ))}
      {basis && <p data-testid="urgent-basis" className="text-[10px] text-slate-500">{basis}</p>}
    </section>
  );
}
