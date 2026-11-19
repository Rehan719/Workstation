// W953 (P5.20 clause 6) — THE ONE PAGE OF WHERE HELP IS, on the support page: how to find a qualified scholar, where
// regulated and free legal help is, and how to complain about an answer (GET /api/v1/support/where-help-is). The Law
// page's help is built on the server from the same source. Below the four headings, every sentence is the server's;
// links open the services' own pages and nothing of theirs is copied. A failed read is said, never drawn as no help.
import React, { useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

export interface WhereHelp {
  a_qualified_scholar: { heading: string; steps: string[]; names_none_because: string; this_platform: string };
  regulated_and_free_help: { name: string; link: string; for_what: string }[];
  this_platform_is_not: string[];
  to_complain: string;
  basis: string;
}

export const WhereHelpIs: React.FC = () => {
  const [help, setHelp] = useState<WhereHelp | null>(null);
  const [readError, setReadError] = useState('');

  useEffect(() => {
    let live = true;
    apiJson<WhereHelp>('/api/v1/support/where-help-is')
      .then(h => { if (live) setHelp(h); })
      .catch(e => { if (live) setReadError(errorMessage(e)); });
    return () => { live = false; };
  }, []);

  //  a page that sent the person here by this section's address brings it into view once it is drawn
  useEffect(() => {
    if (help && typeof window !== 'undefined' && window.location.hash === '#where-help-is') {
      document.getElementById('where-help-is')?.scrollIntoView?.();
    }
  }, [help]);

  const h3 = 'text-sm font-black uppercase tracking-wider text-slate-300';
  return (
    <section id="where-help-is" data-testid="where-help-is" className="border border-slate-800 rounded-2xl p-6 bg-slate-900/40 space-y-4">
      <h2 className="text-xl font-black uppercase tracking-wider text-slate-300">Where help from a person is</h2>
      {readError && (
        <p role="alert" data-testid="where-help-refusal" className="text-vital font-bold">
          Where help is could not be read: {readError}
        </p>
      )}
      {!readError && !help && <p className="text-slate-500 font-bold animate-pulse">Reading…</p>}
      {help && (
        <>
          <div data-testid="where-help-scholar" className="space-y-2">
            <h3 className={h3}>{help.a_qualified_scholar.heading}</h3>
            <ol className="list-decimal ml-5 space-y-1 text-sm text-slate-300">
              {help.a_qualified_scholar.steps.map(s => <li key={s}>{s}</li>)}
            </ol>
            <p data-testid="where-help-scholar-none" className="text-xs text-slate-400">{help.a_qualified_scholar.names_none_because}</p>
            <p data-testid="where-help-scholar-platform" className="text-xs text-slate-400">{help.a_qualified_scholar.this_platform}</p>
          </div>
          <div data-testid="where-help-legal" className="space-y-2">
            <h3 className={h3}>Regulated and free legal help</h3>
            <ul className="space-y-1 text-sm text-slate-300">
              {help.regulated_and_free_help.map(e => (
                <li key={e.link} data-testid="where-help-legal-entry">
                  <a href={e.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{e.name}</a> — {e.for_what}
                </li>
              ))}
            </ul>
          </div>
          <div className="space-y-1">
            <h3 className={h3}>What this platform is not</h3>
            <ul data-testid="where-help-not" className="text-xs text-slate-400 list-disc ml-5">
              {help.this_platform_is_not.map(s => <li key={s}>{s}</li>)}
            </ul>
          </div>
          <div className="space-y-1">
            <h3 className={h3}>How to complain about an answer</h3>
            <p data-testid="where-help-complain" className="text-sm text-slate-300">{help.to_complain}</p>
          </div>
          <p data-testid="where-help-basis" className="text-[10px] text-slate-600">{help.basis}</p>
        </>
      )}
    </section>
  );
};

export default WhereHelpIs;
