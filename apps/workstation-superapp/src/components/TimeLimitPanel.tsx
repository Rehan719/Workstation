import React, { useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

//  W875 (FU-1012) - HOW LONG A TIME LIMIT RUNS: arithmetic on a rule's own words, checked against the provision as
//  its publisher returns it when asked, with what the limit does not account for and who to ask. Nothing here is
//  composed and nothing is advice. The rules are this platform's list; the provision is fetched only on a person's
//  action.
//  W1161 (P5.11 clause 2) - a person says where the claim is. A claim not listed, or one whose rule is not for that
//  nation, is answered that a time limit may still apply, with where to ask today for that nation: never "no deadline".
//  An Order's provision is an article, and the answer says so.
//  W1162 (P5.11 clause 2) - each answer says the rule's sources: the page, the day it was read and by whom, and NOT
//  RECENTLY CHECKED ninety days on; a month with no such day is worked out to the earlier of the two days it could end
//  on, and the headline says the provision leaves it unsettled.
type Source = { id: string; read: boolean; name?: string; checked: string; read_by?: string | null };
type Rule = { id: string; name: string; act: string; section: string; part: string; nations: string[] };
type Route = { name: string; link: string; for_what: string };
type Limit = {
  matched: true; name: string; act: string; part: string; section: string; event: string; event_date: string;
  last_day: string | null; computed: boolean; basis: string; does_not_account_for: string; arithmetic: string;
  route: Route; provision_address: string | null; not_advice: string; settled?: boolean; sources: Source[];
};
type NoRule = {
  matched: false; nation: string | null; basis: string; rules_for_this_nation: { id: string; name: string }[];
  where_to_ask: Record<string, Route[]>;
  named_on: { name: string; publisher: string; page: string; checked: string; recently_checked: boolean; own_sites: string };
  not_advice: string;
};
type Listed = { rules: Rule[]; nations: string[]; not_listed: { id: string; name: string } };

const TimeLimitPanel: React.FC = () => {
  const [listed, setListed] = useState<Listed | null>(null);
  const [rulesNote, setRulesNote] = useState('');
  const [nation, setNation] = useState('');
  const [rule, setRule] = useState('');
  const [date, setDate] = useState('');
  const [busy, setBusy] = useState(false);
  const [got, setGot] = useState<Limit | NoRule | null>(null);
  const [refusal, setRefusal] = useState('');

  useEffect(() => {
    let alive = true;
    apiJson<Listed>('/api/v1/law/time-limit')
      .then(d => { if (alive) { setListed(d); setRule(d.rules[0]?.id ?? ''); } })
      .catch(e => { if (alive) setRulesNote(`The rules could not be read (${errorMessage(e)}), so no limit can be worked out here.`); });
    return () => { alive = false; };
  }, []);

  //  a claim not listed needs no date: no rule is there to work one out from
  const unlisted = listed !== null && rule === listed.not_listed.id;
  const work = async () => {
    setBusy(true); setRefusal(''); setGot(null);
    try {
      setGot(await apiJson<Limit | NoRule>('/api/v1/law/time-limit',
        { method: 'POST', body: { rule, event_date: unlisted ? '' : date, nation } }));
    } catch (e) { setRefusal(errorMessage(e)); }
    setBusy(false);
  };
  //  a source as read, with its day and the round that read it, or as not checked
  const sourceSaid = (s: Source) => (s.read
    ? `${s.name}, ${s.checked}${s.read_by ? ` (${s.read_by.split(',')[0]})` : ''}`
    : `${s.id}: ${s.checked}`);
  const field = 'bg-slate-900 border border-slate-800 rounded-lg px-2 py-1 text-[11px] text-slate-200';
  const link = 'underline text-sky-400';

  return (
    <div data-testid="law-time-limit-panel" className="space-y-3">
      <h4 className="text-sm font-black text-white uppercase tracking-tight">How long a time limit runs</h4>
      <p className="text-[10px] text-slate-500 max-w-2xl leading-relaxed">
        Pick where the claim is, the claim and the date it runs from. The provision that sets the limit is read from its
        publisher when you ask, and a date is worked out only if the provision still has the words the rule was built
        from. If no rule here is for your claim, or for where it is, you are told where to ask today.
      </p>
      {rulesNote && <p data-testid="law-time-limit-rules-note" className="text-[11px] text-amber-300/90">{rulesNote}</p>}
      {listed && (
        <div className="flex flex-wrap gap-2 items-center">
          <select className={field} value={nation} onChange={e => setNation(e.target.value)} aria-label="Where the claim is">
            <option value="">Where the claim is</option>
            {listed.nations.map(n => <option key={n} value={n}>{n}</option>)}
          </select>
          <select className={field} value={rule} onChange={e => setRule(e.target.value)} aria-label="Claim">
            {listed.rules.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            <option value={listed.not_listed.id}>{listed.not_listed.name}</option>
          </select>
          <input className={field} type="date" value={date} onChange={e => setDate(e.target.value)} aria-label="The date it runs from" />
          <button type="button" disabled={busy || !nation || !rule || (!unlisted && !date)} onClick={work}
                  className="px-3 py-1 rounded-lg bg-aura text-sovereign text-[10px] font-black uppercase tracking-widest disabled:opacity-40">
            {busy ? 'Reading the provision…' : 'Work it out'}
          </button>
        </div>
      )}
      {refusal && <p data-testid="law-time-limit-refusal" className="text-[11px] text-amber-300/90">{refusal}</p>}
      {got && got.matched && (
        <div data-testid="law-time-limit-result" className="p-3 rounded-xl bg-slate-950 border border-slate-900 text-[11px] text-slate-300 space-y-1">
          {got.computed && got.last_day
            ? <p className="font-bold text-white">The primary limit ends at the end of {got.last_day}{got.settled === false ? ', the earlier of the two days the provision leaves unsettled' : ''}.</p>
            : <p className="font-bold text-amber-300">No date is worked out.</p>}
          <p>{got.basis}</p>
          <p className="text-[10px] text-slate-400">It does not account for {got.does_not_account_for}.</p>
          <p className="text-[10px] text-slate-400">
            Ask <a href={got.route.link} target="_blank" rel="noreferrer" className={link}>{got.route.name}</a> - {got.route.for_what}.
          </p>
          <p data-testid="law-time-limit-sources" className="text-[9px] text-slate-500">Read: {got.sources.map(sourceSaid).join('; ')}.</p>
          <p className="text-[9px] text-slate-600">{got.act}, {got.part} {got.section}{got.provision_address ? ` - ${got.provision_address}` : ''}. {got.arithmetic}. {got.not_advice}</p>
        </div>
      )}
      {got && !got.matched && (
        <div data-testid="law-time-limit-no-rule" className="p-3 rounded-xl bg-slate-950 border border-slate-900 text-[11px] text-slate-300 space-y-1">
          <p className="font-bold text-amber-300">No date is worked out.</p>
          <p>{got.basis}</p>
          {got.rules_for_this_nation.length > 0 && (
            <p data-testid="law-time-limit-rules-here" className="text-[10px] text-slate-400">
              The rules here for a claim in {got.nation}: {got.rules_for_this_nation.map(r => r.name).join('; ')}.
            </p>
          )}
          {Object.entries(got.where_to_ask).map(([n, places]) => (
            <div key={n} data-testid="law-time-limit-where-to-ask">
              <p className="text-[10px] text-slate-400">Where to ask today, for a claim in {n}:</p>
              <ul className="list-disc pl-4 text-[10px] text-slate-400">
                {places.map(p => (
                  <li key={p.link}><a href={p.link} target="_blank" rel="noreferrer" className={link}>{p.name}</a> - {p.for_what}.</li>
                ))}
              </ul>
            </div>
          ))}
          <p data-testid="law-time-limit-named-on" className="text-[9px] text-slate-600">
            Each place is named on {got.named_on.publisher}'s guide <a href={got.named_on.page} target="_blank" rel="noreferrer" className={link}>{got.named_on.name}</a>, {got.named_on.checked}. {got.named_on.own_sites} {got.not_advice}
          </p>
        </div>
      )}
    </div>
  );
};

export default TimeLimitPanel;
