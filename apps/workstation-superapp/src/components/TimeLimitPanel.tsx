import React, { useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

//  W875 (FU-1012) - HOW LONG A TIME LIMIT RUNS: arithmetic on a rule's own words, checked against the provision as
//  its publisher returns it when asked, with what the limit does not account for and who to ask. Nothing here is
//  composed and nothing is advice. The rules are this platform's list; the provision is fetched only on a person's
//  action.
type Rule = { id: string; name: string; act: string; section: string; words: string; event: string };
type Limit = {
  name: string; act: string; section: string; words: string; event: string; event_date: string;
  last_day: string | null; computed: boolean; basis: string; does_not_account_for: string; arithmetic: string;
  route: { name: string; link: string; for_what: string }; provision_address: string | null; not_advice: string;
};

const TimeLimitPanel: React.FC = () => {
  const [rules, setRules] = useState<Rule[] | null>(null);
  const [rulesNote, setRulesNote] = useState('');
  const [rule, setRule] = useState('');
  const [date, setDate] = useState('');
  const [busy, setBusy] = useState(false);
  const [got, setGot] = useState<Limit | null>(null);
  const [refusal, setRefusal] = useState('');

  useEffect(() => {
    let alive = true;
    apiJson<{ rules: Rule[] }>('/api/v1/law/time-limit')
      .then(d => { if (alive) { setRules(d.rules); setRule(d.rules[0]?.id ?? ''); } })
      .catch(e => { if (alive) setRulesNote(`The rules could not be read (${errorMessage(e)}), so no limit can be worked out here.`); });
    return () => { alive = false; };
  }, []);

  const work = async () => {
    setBusy(true); setRefusal(''); setGot(null);
    try { setGot(await apiJson<Limit>('/api/v1/law/time-limit', { method: 'POST', body: { rule, event_date: date } })); }
    catch (e) { setRefusal(errorMessage(e)); }
    setBusy(false);
  };
  const field = 'bg-slate-900 border border-slate-800 rounded-lg px-2 py-1 text-[11px] text-slate-200';

  return (
    <div data-testid="law-time-limit-panel" className="space-y-3">
      <h4 className="text-sm font-black text-white uppercase tracking-tight">How long a time limit runs</h4>
      <p className="text-[10px] text-slate-500 max-w-2xl leading-relaxed">
        Pick the claim and the date it runs from. The provision that sets the limit is read from its publisher when you
        ask, and a date is worked out only if the provision still has the words the rule was built from.
      </p>
      {rulesNote && <p data-testid="law-time-limit-rules-note" className="text-[11px] text-amber-300/90">{rulesNote}</p>}
      {rules && (
        <div className="flex flex-wrap gap-2 items-center">
          <select className={field} value={rule} onChange={e => setRule(e.target.value)} aria-label="Claim">
            {rules.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
          </select>
          <input className={field} type="date" value={date} onChange={e => setDate(e.target.value)} aria-label="The date it runs from" />
          <button type="button" disabled={busy || !rule || !date} onClick={work}
                  className="px-3 py-1 rounded-lg bg-aura text-sovereign text-[10px] font-black uppercase tracking-widest disabled:opacity-40">
            {busy ? 'Reading the provision…' : 'Work it out'}
          </button>
        </div>
      )}
      {refusal && <p data-testid="law-time-limit-refusal" className="text-[11px] text-amber-300/90">{refusal}</p>}
      {got && (
        <div data-testid="law-time-limit-result" className="p-3 rounded-xl bg-slate-950 border border-slate-900 text-[11px] text-slate-300 space-y-1">
          {got.computed && got.last_day
            ? <p className="font-bold text-white">The primary limit ends at the end of {got.last_day}.</p>
            : <p className="font-bold text-amber-300">No date is worked out.</p>}
          <p>{got.basis}</p>
          <p className="text-[10px] text-slate-400">It does not account for {got.does_not_account_for}.</p>
          <p className="text-[10px] text-slate-400">
            Ask <a href={got.route.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{got.route.name}</a> - {got.route.for_what}.
          </p>
          <p className="text-[9px] text-slate-600">{got.act}, section {got.section}{got.provision_address ? ` - ${got.provision_address}` : ''}. {got.arithmetic}. {got.not_advice}</p>
        </div>
      )}
    </div>
  );
};

export default TimeLimitPanel;
