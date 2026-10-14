import React, { useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

//  W724 (P5.20 clauses 1, 3 and 6) - ONE PROVISION OF AN ACT, WORD FOR WORD, FROM ITS PUBLISHER, and where
//  regulated and free help is. Nothing here is composed by a model and nothing is fetched until asked for.
type Part = { level: number; number: string; text: string };
type Provision = {
  act: string | null; heading: string | null; section: string; parts: Part[];
  version_dated: string | null; extent: string | null; changes_basis: string;
  changes_not_yet_applied_count: number; changes_not_yet_applied_across_the_act: number;
  publisher: string; address: string; licence: string; fetched_at: string; what_this_is: string;
  fidelity: { checked: boolean; matches: boolean; basis: string };
};
type Help = { regulated_and_free_help: { name: string; link: string; for_what: string }[]; this_platform_is_not: string[]; to_complain: string; basis: string };

const KINDS: [string, string][] = [
  ['ukpga', 'Act of the UK Parliament'], ['uksi', 'UK statutory instrument'], ['asp', 'Act of the Scottish Parliament'],
  ['asc', 'Act of Senedd Cymru'], ['anaw', 'Act of the National Assembly for Wales'], ['nia', 'Act of the Northern Ireland Assembly'],
];

const StatutePanel: React.FC = () => {
  const [kind, setKind] = useState('ukpga');
  const [year, setYear] = useState('');
  const [number, setNumber] = useState('');
  const [section, setSection] = useState('');
  const [busy, setBusy] = useState('');
  const [got, setGot] = useState<Provision | null>(null);
  const [refusal, setRefusal] = useState('');
  const [help, setHelp] = useState<Help | null>(null);
  const [helpRefusal, setHelpRefusal] = useState('');

  const read = async () => {
    setBusy('read'); setRefusal(''); setGot(null);
    try {
      setGot(await apiJson(`/api/v1/law/statute/${kind}/${encodeURIComponent(year.trim())}/${encodeURIComponent(number.trim())}/section/${encodeURIComponent(section.trim())}`));
    } catch (e) { setRefusal(errorMessage(e)); }
    setBusy('');
  };
  const showHelp = async () => {
    setBusy('help'); setHelpRefusal('');
    try { setHelp(await apiJson('/api/v1/law/help')); } catch (e) { setHelpRefusal(errorMessage(e)); }
    setBusy('');
  };
  const field = 'bg-slate-900 border border-slate-800 rounded-lg px-2 py-1 text-[11px] text-slate-200';

  return (
    <div data-testid="law-statute-panel" className="space-y-3">
      <h3 className="text-sm font-black text-white uppercase tracking-tight">Read the Act itself</h3>
      <p className="text-[10px] text-slate-500">
        One provision, word for word, fetched from its publisher when you ask. It is not advice and not an explanation.
      </p>
      <div className="flex flex-wrap gap-2 items-end">
        <label className="text-[9px] text-slate-500">Kind<br />
          <select aria-label="Kind of legislation" value={kind} onChange={e => setKind(e.target.value)} className={field}>
            {KINDS.map(([k, label]) => <option key={k} value={k}>{label}</option>)}
          </select>
        </label>
        <label className="text-[9px] text-slate-500">Year<br /><input aria-label="Year" value={year} onChange={e => setYear(e.target.value)} className={`${field} w-20`} /></label>
        <label className="text-[9px] text-slate-500">Number<br /><input aria-label="Number" value={number} onChange={e => setNumber(e.target.value)} className={`${field} w-20`} /></label>
        <label className="text-[9px] text-slate-500">Section<br /><input aria-label="Section" value={section} onChange={e => setSection(e.target.value)} className={`${field} w-20`} /></label>
        <button type="button" onClick={read} disabled={busy === 'read' || !year || !number || !section}
          className="px-3 py-1.5 rounded-lg bg-slate-800 text-aura text-[10px] font-black uppercase disabled:opacity-40">
          {busy === 'read' ? 'Fetching…' : 'Read it'}
        </button>
      </div>
      {refusal && <p data-testid="law-statute-refusal" className="text-[11px] text-amber-300/90">{refusal}</p>}
      {got && (
        <div data-testid="law-statute-text" className="p-3 rounded-xl bg-slate-950 border border-slate-900">
          <p className="text-[12px] text-white font-bold">{got.act ?? 'title not given by the publisher'} — section {got.section}{got.heading ? `: ${got.heading}` : ''}</p>
          <div className="mt-2 space-y-1">
            {got.parts.filter(p => p.text || p.level > 1).map((p, i) => (
              <p key={i} className="text-[12px] text-slate-200 leading-relaxed" style={{ marginLeft: `${Math.max(0, p.level - 2) * 18}px` }}>
                {p.level > 1 && <span className="text-slate-500">({p.number}) </span>}{p.text}
              </p>
            ))}
          </div>
          <div data-testid="law-statute-source" className="mt-3 pt-2 border-t border-slate-900 text-[9px] text-slate-500 space-y-0.5">
            <p>{got.what_this_is}.</p>
            <p>Publisher: {got.publisher} · <a href={got.address} target="_blank" rel="noreferrer" className="underline text-sky-400">{got.address}</a> · fetched {got.fetched_at}</p>
            <p>Version dated {got.version_dated ?? 'not stated'} · extent as the publisher writes it: {got.extent ?? 'not stated'}</p>
            <p data-testid="law-statute-changes" className={got.changes_not_yet_applied_count ? 'text-amber-300/90' : undefined}>
              {got.changes_basis} Across the whole Act the publisher lists {got.changes_not_yet_applied_across_the_act}.
            </p>
            <p data-testid="law-statute-fidelity">{got.fidelity.basis}</p>
            <p>{got.licence}</p>
          </div>
        </div>
      )}
      <button type="button" onClick={showHelp} disabled={busy === 'help'} className="text-[10px] font-bold text-sky-400 underline underline-offset-2">
        {busy === 'help' ? 'Fetching…' : 'Where to get help from a person'}
      </button>
      {helpRefusal && <p className="text-[11px] text-amber-300/90">{helpRefusal}</p>}
      {help && (
        <div data-testid="law-help" className="p-3 rounded-xl bg-slate-950 border border-slate-900 text-[11px] text-slate-300 space-y-2">
          <ul className="space-y-1">
            {help.regulated_and_free_help.map(h => (
              <li key={h.link}><a href={h.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{h.name}</a> — {h.for_what}</li>
            ))}
          </ul>
          <ul className="text-[10px] text-slate-500 list-disc ml-4">{help.this_platform_is_not.map(s => <li key={s}>{s}</li>)}</ul>
          <p className="text-[10px] text-slate-400">{help.to_complain}</p>
          <p className="text-[9px] text-slate-600">{help.basis}</p>
        </div>
      )}
    </div>
  );
};

export default StatutePanel;
