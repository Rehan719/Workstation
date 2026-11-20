//  W1168 (P5.11 clause 8) - WHAT TO GATHER, as lists: for each subject, its groups of items in the words of the page
//  that gives them, the part of the page each group is in, the nations the page is for, and the page with the day it
//  was read. Every word is the server's but the headings and the joining ones; lists that could not be read are said
//  in their place, never as none.
import React, { useEffect, useState } from 'react';
import { apiJson, ApiError, errorMessage } from '../lib/api';
import { UrgentSource, urgentSourceSaid } from './UrgentRoutes';

export type ChecklistGroup = { heading: string; part: string; lead: string | null; items: string[] };
export type Checklist = {
  id: string; subject: string; nations: string[]; elsewhere: string | null; groups: ChecklistGroup[];
  here: string | null; sources: UrgentSource[];
};

const readFailure = (e: unknown) => (e instanceof ApiError || e instanceof TypeError ? errorMessage(e)
  : String((e as { message?: string } | null)?.message ?? e));

//  the nations a list is for, joined as a person reads them
export const nationsSaid = (n: string[]) =>
  (n.length < 2 ? n.join('') : `${n.slice(0, -1).join(', ')} and ${n[n.length - 1]}`);

export default function ChecklistsPanel() {
  const [lists, setLists] = useState<{ checklists: Checklist[]; basis: string } | null>(null);
  const [note, setNote] = useState('');
  useEffect(() => {
    let alive = true;
    apiJson('/api/v1/law/checklists')
      .then(d => { if (alive) { setLists(d); setNote(''); } })
      .catch(e => { if (alive) { setLists(null); setNote(`What to gather could not be read (${readFailure(e)}).`); } });
    return () => { alive = false; };
  }, []);
  return (
    <section data-testid="law-checklists" aria-label="What to gather"
      className="glass-card p-6 rounded-3xl border border-slate-800 space-y-3">
      <h3 className="text-sm font-black uppercase tracking-widest text-white">What to gather</h3>
      {note && <p data-testid="law-checklists-note" className="text-[11px] text-amber-400">{note}</p>}
      {lists && lists.checklists.length === 0 && (
        <p data-testid="law-checklists-none" className="text-[11px] text-slate-400">The server lists no subject.</p>
      )}
      {lists?.checklists.map(c => (
        <div key={c.id} data-testid="checklist" className="space-y-1">
          <p data-testid="checklist-subject" className="text-xs font-bold text-white">{c.subject}</p>
          <p data-testid="checklist-nations" className="text-[10px] text-slate-400">For {nationsSaid(c.nations)}.</p>
          {c.elsewhere && <p data-testid="checklist-elsewhere" className="text-[10px] text-slate-400">{c.elsewhere}</p>}
          {c.groups.map(g => (
            <div key={`${c.id}|${g.heading}`} data-testid="checklist-group" className="ml-2">
              <p data-testid="checklist-heading" className="text-[10px] font-bold text-sky-300">
                {g.heading} <span className="font-normal text-slate-500">(the page's part "{g.part}")</span>
              </p>
              {g.lead && <p data-testid="checklist-lead" className="text-[10px] text-slate-300">{g.lead}</p>}
              <ul className="list-disc ml-5 text-[10px] text-slate-300 space-y-0.5">
                {g.items.map(i => <li key={i} data-testid="checklist-item">{i}</li>)}
              </ul>
            </div>
          ))}
          {c.here && <p data-testid="checklist-here" className="text-[10px] text-slate-300">{c.here}</p>}
          <p data-testid="checklist-read" className="text-[9px] text-slate-500">Read: {c.sources.map(urgentSourceSaid).join('; ')}.</p>
        </div>
      ))}
      {lists && <p data-testid="law-checklists-basis" className="text-[9px] text-slate-500">{lists.basis}</p>}
    </section>
  );
}
