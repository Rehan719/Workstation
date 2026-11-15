//  W1081 (P5.18 clauses 1 and 2, FU-1075) - THE ENTERPRISE'S OWN AGREEMENTS, AS RECORDS THAT SAY ONLY WHAT IS TRUE OF
//  THEM, on the Law page. Everything here is the routes' own (agentic_core/api/agreements.py, W1080): a party is a real
//  person or a registered body entered with where and when it was read; an agreement keeps drafted, reviewed,
//  approved, executed, in force and ended as six facts apart, each with who and when; an approval names the hash of
//  the one version approved, and a change to the text ends it; an execution is the person's own entry. Parties are
//  offered only from the party records, never from the entities of this platform. The internal service contracts in
//  virtual units are listed apart, never as agreements. With sign-in off nothing is kept, and the page says the
//  route's reason. Each read and each action says its own failure, in its own place.
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

const BASE = '/api/v1/agreements';
const NAMES: Record<string, string> = {
  drafted: 'Drafted', reviewed: 'Reviewed', approved: 'Approved', executed: 'Executed', in_force: 'In force', ended: 'Ended',
};
const short = (h?: string) => (h ? h.replace(/^sha256:/, '').slice(0, 12) : '');
const field = 'w-full p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-200';
const button = 'px-3 py-1.5 rounded-lg bg-slate-800 text-[10px] font-black uppercase tracking-widest text-aura disabled:opacity-40';

type Party = { id: string; kind: string; name: string; registered_on?: string | null; registered_number?: string | null;
  read_from: string; read_on: string; entered_by: string; basis: string };
type Fact = { state: string; recorded: boolean; said?: string; by?: string; at?: string; entered_by?: string;
  entered_at?: string; [k: string]: any };
type Agreement = { id: string; title: string; parties: any[]; versions: any[]; current: { version: number; hash: string };
  facts: Fact[]; not_legal_advice?: string;
  obligations?: any[]; notice?: any; text_kept?: any; date_basis?: string };   // W1086 (P5.18 clauses 3 and 7)

//  one fact, said as the route recorded it: who and when, and what it holds; a fact not recorded says so
function FactLine({ f }: { f: Fact }) {
  const who = f.by ?? f.entered_by;
  const when = f.at ?? f.entered_at;
  let held = '';
  if (f.state === 'drafted' || f.state === 'approved') held = f.recorded ? `version ${f.version} (${short(f.hash)})` : '';
  if (f.state === 'executed' && f.recorded) {
    held = `version ${f.version} (${short(f.hash)}), signed on ${f.signed_on}${f.of_current_text ? '' : ' - not the text as it stands'}`;
  }
  if (f.state === 'in_force' && f.recorded) held = `from ${f.from}: ${f.basis}`;
  if (f.state === 'ended' && f.recorded) held = `on ${f.on}: ${f.how}`;
  return (
    <li data-testid="agreement-fact" className="text-[11px] text-slate-300">
      <span className="font-black text-slate-100">{NAMES[f.state] ?? f.state}</span>{' '}
      {f.state === 'reviewed' && f.recorded ? (
        <span>{(f.reviews ?? []).map((r: any) => `by ${r.by} at ${r.at}, of version ${r.version}${r.of_current_text ? '' : ' (not the text as it stands)'}${r.note ? `: ${r.note}` : ''}`).join('; ')}</span>
      ) : f.recorded ? (
        <span>{`${held ? `${held} - ` : ''}by ${who} at ${when}`}</span>
      ) : (
        <span className="text-slate-500">{f.said}</span>
      )}
      {f.state === 'approved' && (f.ended_approvals ?? []).map((e: any, i: number) => (
        <span key={i} data-testid="agreement-approval-ended" className="block text-[10px] text-amber-300">
          {`The approval of version ${e.version} by ${e.by} ended at ${e.ended_at}: ${e.ended_because}.`}
        </span>
      ))}
      {f.state === 'executed' && f.recorded && (
        <span className="block text-[10px] text-slate-400">
          <span data-testid="agreement-execution-evidence">{`Evidence, as entered: ${f.evidence}. Formalities met, as entered: ${(f.formalities_met ?? []).join('; ')}.`}</span>{' '}
          <span data-testid="agreement-law-basis">{f.law_basis}</span>
        </span>
      )}
    </li>
  );
}

export default function AgreementsPanel() {
  const [list, setList] = useState<any | null>(null);
  const [listErr, setListErr] = useState('');
  const [parties, setParties] = useState<Party[] | null>(null);
  const [partiesErr, setPartiesErr] = useState('');
  const [open, setOpen] = useState<Agreement | null>(null);
  const [openErr, setOpenErr] = useState('');
  const openId = useRef<string | null>(null);
  const [errs, setErrs] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState('');
  const say = (k: string, v: string) => setErrs(e => ({ ...e, [k]: v }));

  const [p, setP] = useState({ kind: 'registered_body', name: '', registered_on: '', registered_number: '', read_from: '', read_on: '' });
  const [d, setD] = useState({ title: '', text: '', a: '', roleA: '', b: '', roleB: '' });
  const [note, setNote] = useState('');
  const [text, setText] = useState('');
  const [ex, setEx] = useState({ signed_on: '', evidence: '', formalities: '' });
  const [inf, setInf] = useState({ from_date: '', basis: '' });
  const [end, setEnd] = useState({ on: '', how: '' });
  const [sig, setSig] = useState({ party_id: '', name: '', capacity: '', authority_as_stated: '', stated_by: '' });
  //  W1086 (P5.18 clause 3) - an obligation from its clause, and the notice period as the text states it
  const [ob, setOb] = useState({ owed_by: '', owed_to: '', what: '', clause: '', due_on: '' });
  const [nt, setNt] = useState({ as_stated: '', clause: '' });

  const readList = useCallback(async () => {
    setListErr('');
    try {
      setList(await apiJson(BASE));
    } catch (e) {
      setList(null);
      setListErr(`The agreement records could not be read (${errorMessage(e)}), so none is shown.`);
    }
  }, []);
  const readParties = useCallback(async () => {
    setPartiesErr('');
    try {
      const r = await apiJson(`${BASE}/parties`);
      setParties(Array.isArray(r?.parties) ? r.parties : []);
    } catch (e) {
      setParties(null);
      setPartiesErr(`The parties could not be read (${errorMessage(e)}), so none is offered.`);
    }
  }, []);
  useEffect(() => { readList(); readParties(); }, [readList, readParties]);

  //  a record opened is said under its own id only: an answer for one opened before is dropped
  const show = (a: Agreement) => {
    if (openId.current !== a.id) return;
    setOpen(a);
    setText(a.versions?.[a.versions.length - 1]?.text ?? '');
  };
  const openRecord = async (id: string) => {
    openId.current = id;
    setOpen(null); setOpenErr(''); setErrs({});
    try {
      show(await apiJson(`${BASE}/${id}`));
    } catch (e) {
      if (openId.current === id) setOpenErr(`This agreement record could not be read (${errorMessage(e)}).`);
    }
  };

  const enterParty = async () => {
    say('party', ''); setBusy('party');
    const body: Record<string, string> = { kind: p.kind, name: p.name, read_from: p.read_from, read_on: p.read_on };
    if (p.kind === 'registered_body') { body.registered_on = p.registered_on; body.registered_number = p.registered_number; }
    try {
      await apiJson(`${BASE}/parties`, { method: 'POST', body });
      setP({ kind: p.kind, name: '', registered_on: '', registered_number: '', read_from: '', read_on: '' });
      await readParties();
    } catch (e) {
      say('party', `The party was not entered: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };

  const draft = async () => {
    say('draft', ''); setBusy('draft');
    try {
      const a: Agreement = await apiJson(BASE, { method: 'POST', body: {
        title: d.title, text: d.text,
        parties: [{ party_id: d.a, role: d.roleA }, { party_id: d.b, role: d.roleB }] } });
      setD({ title: '', text: '', a: '', roleA: '', b: '', roleB: '' });
      openId.current = a.id; setErrs({}); show(a);
      await readList();
    } catch (e) {
      say('draft', `The agreement was not drafted: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };

  //  one fact on the open record, said under its own button
  const act = async (key: string, path: string, body: Record<string, unknown>, method: 'POST' | 'PUT' = 'POST') => {
    if (!open) return;
    const id = open.id;
    say(key, ''); setBusy(key);
    try {
      const a: Agreement = await apiJson(`${BASE}/${id}/${path}`, { method, body });
      show(a);
      if (openId.current === id) await readList();
    } catch (e) {
      if (openId.current === id) say(key, `Not recorded: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };

  const cur = open?.current;
  //  W1086 - a party by its name on the open record, as the route gave it
  const nameOf = (pid: string) => open?.parties.find((x: any) => x.party_id === pid)?.party?.name ?? pid;
  const fact = (s: string) => open?.facts.find(f => f.state === s);
  const executed = !!fact('executed')?.recorded;
  const ended = !!fact('ended')?.recorded;
  const two = (parties ?? []).length >= 2;
  const isc = list?.internal_service_contracts;

  return (
    <div className="space-y-6" data-testid="agreements-panel">
      <div className="space-y-1">
        <h3 className="text-lg font-black text-white uppercase tracking-tight">Agreements with an outside party</h3>
        <p className="text-[11px] text-slate-400">
          The enterprise's own agreements, as records that say only what is true of them: who the parties are and where
          each was read, and each step of an agreement as its own fact, with who and when.
        </p>
        {list?.not_legal_advice && <p data-testid="agreements-not-advice" className="text-[10px] text-amber-300">{list.not_legal_advice}</p>}
      </div>

      {list === null && !listErr && <p className="text-[11px] text-slate-500">Reading the agreement records…</p>}
      {listErr && <p data-testid="agreements-unread" className="text-[11px] text-rose-300">{listErr}</p>}

      {list && list.kept === false && (
        <p data-testid="agreements-not-kept" className="text-[11px] text-amber-300">{list.not_kept_because}</p>
      )}

      {list && list.kept === true && (
        <>
          <section className="space-y-2">
            <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Parties</h4>
            {parties === null && !partiesErr && <p className="text-[11px] text-slate-500">Reading the parties…</p>}
            {partiesErr && <p data-testid="agreements-parties-unread" className="text-[11px] text-rose-300">{partiesErr}</p>}
            {parties && parties.length === 0 && <p data-testid="agreements-no-parties" className="text-[11px] text-slate-500">No party is entered yet.</p>}
            <ul className="space-y-1">
              {(parties ?? []).map(x => (
                <li key={x.id} data-testid="agreement-party" className="text-[11px] text-slate-300">
                  <span className="font-black text-slate-100">{x.name}</span>
                  {x.kind === 'registered_body' ? ` - a registered body, on ${x.registered_on} as ${x.registered_number}` : ' - a person'}
                  <span className="block text-[10px] text-slate-500">{x.basis}</span>
                </li>
              ))}
            </ul>
            <div className="grid grid-cols-2 gap-2" data-testid="agreements-party-form">
              <label className="text-[10px] text-slate-400">A party is
                <select aria-label="Kind of party" className={field} value={p.kind} onChange={e => setP({ ...p, kind: e.target.value })}>
                  <option value="registered_body">a registered body</option>
                  <option value="person">a person</option>
                </select>
              </label>
              <label className="text-[10px] text-slate-400">Name, as read
                <input aria-label="Party name" className={field} value={p.name} onChange={e => setP({ ...p, name: e.target.value })} />
              </label>
              {p.kind === 'registered_body' && (
                <>
                  <label className="text-[10px] text-slate-400">The register it is on
                    <input aria-label="Register" className={field} value={p.registered_on} onChange={e => setP({ ...p, registered_on: e.target.value })} />
                  </label>
                  <label className="text-[10px] text-slate-400">Its number there
                    <input aria-label="Number on the register" className={field} value={p.registered_number} onChange={e => setP({ ...p, registered_number: e.target.value })} />
                  </label>
                </>
              )}
              <label className="text-[10px] text-slate-400">Where it was read
                <input aria-label="Where it was read" className={field} value={p.read_from} onChange={e => setP({ ...p, read_from: e.target.value })} />
              </label>
              <label className="text-[10px] text-slate-400">When it was read
                <input aria-label="When it was read" type="date" className={field} value={p.read_on} onChange={e => setP({ ...p, read_on: e.target.value })} />
              </label>
            </div>
            <button type="button" className={button} disabled={busy === 'party'} onClick={enterParty}>Enter this party</button>
            {errs.party && <p data-testid="agreements-party-error" className="text-[11px] text-rose-300">{errs.party}</p>}
          </section>

          <section className="space-y-2">
            <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Draft an agreement</h4>
            {!two ? (
              <p data-testid="agreements-draft-needs-parties" className="text-[11px] text-slate-500">
                An agreement names at least two parties, each entered above as the person or registered body it is.
              </p>
            ) : (
              <div className="space-y-2" data-testid="agreements-draft-form">
                <input aria-label="Agreement title" className={field} placeholder="Title" value={d.title} onChange={e => setD({ ...d, title: e.target.value })} />
                <textarea aria-label="Agreement text" className={field} rows={4} placeholder="The agreement's text" value={d.text} onChange={e => setD({ ...d, text: e.target.value })} />
                {(['a', 'b'] as const).map((k, i) => (
                  <div key={k} className="grid grid-cols-2 gap-2">
                    <select aria-label={`Party ${i + 1}`} className={field} value={d[k]} onChange={e => setD({ ...d, [k]: e.target.value })}>
                      <option value="">Choose a party</option>
                      {(parties ?? []).map(x => <option key={x.id} value={x.id}>{x.name}</option>)}
                    </select>
                    <input aria-label={`Role of party ${i + 1}`} className={field} placeholder="Its role, e.g. supplier"
                      value={k === 'a' ? d.roleA : d.roleB} onChange={e => setD({ ...d, [k === 'a' ? 'roleA' : 'roleB']: e.target.value })} />
                  </div>
                ))}
                <button type="button" className={button} disabled={busy === 'draft'} onClick={draft}>Draft this agreement</button>
                {errs.draft && <p data-testid="agreements-draft-error" className="text-[11px] text-rose-300">{errs.draft}</p>}
              </div>
            )}
          </section>

          <section className="space-y-2">
            <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Agreement records</h4>
            {(list.agreements ?? []).length === 0 && <p data-testid="agreements-none" className="text-[11px] text-slate-500">No agreement is recorded yet.</p>}
            <ul className="space-y-1">
              {(list.agreements ?? []).map((a: any) => (
                <li key={a.id} data-testid="agreement-row">
                  <button type="button" className="text-left text-[11px] text-sky-300 underline" onClick={() => openRecord(a.id)}>
                    {`${a.title} - version ${a.version}, ${(a.facts ?? []).filter((f: any) => f.recorded).map((f: any) => NAMES[f.state] ?? f.state).join(', ')} recorded`}
                  </button>
                </li>
              ))}
            </ul>
          </section>

          {openErr && <p data-testid="agreements-open-error" className="text-[11px] text-rose-300">{openErr}</p>}
          {open && cur && (
            <section className="space-y-3 p-4 rounded-xl border border-slate-800" data-testid="agreement-open">
              <h4 className="text-[12px] font-black text-white">{open.title}</h4>
              <p data-testid="agreement-current" className="text-[10px] text-slate-400">{`The text as it stands is version ${cur.version} (${cur.hash}).`}</p>
              <ul className="space-y-1">
                {open.parties.map((x: any) => (
                  <li key={x.party_id} className="text-[11px] text-slate-300">
                    {`${x.role}: ${x.party?.name ?? x.said}`}
                    {(x.signatories ?? []).map((s: any, i: number) => (
                      <span key={i} data-testid="agreement-signatory" className="block text-[10px] text-slate-400">
                        {`Signs as ${s.capacity}: ${s.name}. Authority, as stated by ${s.stated_by}: ${s.authority_as_stated}. ${s.basis}`}
                      </span>
                    ))}
                  </li>
                ))}
              </ul>
              <ul className="space-y-1">{open.facts.map(f => <FactLine key={f.state} f={f} />)}</ul>

              {/* W1086 (P5.18 clauses 3 and 7) - obligations from the text, the notice period, the text kept as data */}
              <div className="space-y-1" data-testid="agreement-obligations">
                <p className="text-[11px] font-black text-slate-100">Obligations, as read from the text</p>
                {(open.obligations ?? []).length === 0 && <p data-testid="agreement-no-obligations" className="text-[11px] text-slate-500">No obligation is entered yet.</p>}
                <ul className="space-y-1">
                  {(open.obligations ?? []).map((o: any) => (
                    <li key={o.id} data-testid="agreement-obligation" className="text-[11px] text-slate-300">
                      {`${nameOf(o.owed_by)} owes ${nameOf(o.owed_to)}: ${o.what} (${o.clause}). ${o.due_on ? `Falls due on ${o.due_on}, as entered.` : o.due_said} ${o.confirmed ? `Confirmed by ${o.confirmed.by} at ${o.confirmed.at}.` : o.confirmed_said}`}
                      {!o.confirmed && !ended && (
                        <button type="button" className={`${button} ml-2`} disabled={!!busy} onClick={() => act(`confirm-${o.id}`, `obligations/${o.id}/confirm`, {})}>
                          {`Confirm it was read from ${o.clause}`}
                        </button>
                      )}
                      {errs[`confirm-${o.id}`] && <span data-testid="agreement-error-confirm" className="block text-[11px] text-rose-300">{errs[`confirm-${o.id}`]}</span>}
                    </li>
                  ))}
                </ul>
                {open.date_basis && <p data-testid="agreement-date-basis" className="text-[10px] text-slate-500">{open.date_basis}</p>}
                {!ended && (
                  <div className="grid grid-cols-2 gap-2">
                    {([['owed_by', 'Owed by'], ['owed_to', 'Owed to']] as const).map(([k, label]) => (
                      <select key={k} aria-label={label} className={field} value={ob[k]} onChange={e => setOb({ ...ob, [k]: e.target.value })}>
                        <option value="">{`${label}: choose a party`}</option>
                        {open.parties.map((x: any) => <option key={x.party_id} value={x.party_id}>{x.party?.name ?? x.party_id}</option>)}
                      </select>
                    ))}
                    <input aria-label="What is owed" className={field} placeholder="What is owed, as the text says" value={ob.what} onChange={e => setOb({ ...ob, what: e.target.value })} />
                    <input aria-label="The clause it was read from" className={field} placeholder="The clause, e.g. clause 3" value={ob.clause} onChange={e => setOb({ ...ob, clause: e.target.value })} />
                    <input aria-label="It falls due on" type="date" className={field} value={ob.due_on} onChange={e => setOb({ ...ob, due_on: e.target.value })} />
                    <button type="button" className={button} disabled={!!busy} onClick={() => act('obligation', 'obligations', { ...ob, due_on: ob.due_on || null })}>Record this obligation</button>
                  </div>
                )}
                {errs.obligation && <p data-testid="agreement-error-obligation" className="text-[11px] text-rose-300">{errs.obligation}</p>}
              </div>
              {open.notice && (
                <div className="space-y-1" data-testid="agreement-notice">
                  <p data-testid="agreement-notice-said" className="text-[11px] text-slate-300">
                    {open.notice.known ? `Notice period: ${open.notice.as_stated} (${open.notice.clause}), entered by ${open.notice.entered_by} at ${open.notice.entered_at}.` : open.notice.said}
                  </p>
                  {!ended && (
                    <div className="grid grid-cols-2 gap-2">
                      <input aria-label="The notice period, as stated" className={field} placeholder="As the text states it" value={nt.as_stated} onChange={e => setNt({ ...nt, as_stated: e.target.value })} />
                      <input aria-label="The notice clause" className={field} placeholder="The clause it was read from" value={nt.clause} onChange={e => setNt({ ...nt, clause: e.target.value })} />
                      <button type="button" className={button} disabled={!!busy} onClick={() => act('notice', 'notice', nt)}>Record the notice period</button>
                    </div>
                  )}
                  {errs.notice && <p data-testid="agreement-error-notice" className="text-[11px] text-rose-300">{errs.notice}</p>}
                </div>
              )}
              {open.text_kept && (
                <p data-testid="agreement-text-kept" className="text-[10px] text-slate-500">
                  {`${open.text_kept.chars} of the ${open.text_kept.of} characters of the text are kept. ${open.text_kept.basis}`}
                </p>
              )}

              {ended ? (
                <p data-testid="agreement-ended-note" className="text-[11px] text-slate-500">Its end is recorded, so nothing more is recorded on it.</p>
              ) : (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <input aria-label="Review note" className={field} placeholder="A note on the review (optional)" value={note} onChange={e => setNote(e.target.value)} />
                    <button type="button" className={button} disabled={!!busy} onClick={() => act('review', 'review', { hash: cur.hash, ...(note ? { note } : {}) })}>
                      {`Record a review of version ${cur.version}`}
                    </button>
                    {errs.review && <p data-testid="agreement-error-review" className="text-[11px] text-rose-300">{errs.review}</p>}
                  </div>
                  <div className="space-y-1">
                    <button type="button" className={button} disabled={!!busy} onClick={() => act('approve', 'approve', { hash: cur.hash })}>
                      {`Approve version ${cur.version} (${short(cur.hash)})`}
                    </button>
                    {errs.approve && <p data-testid="agreement-error-approve" className="text-[11px] text-rose-300">{errs.approve}</p>}
                  </div>
                  {executed ? (
                    <p data-testid="agreement-text-fixed" className="text-[11px] text-slate-500">
                      Its execution is recorded, so its text is not changed here: a variation is an agreement record of its own.
                    </p>
                  ) : (
                    <div className="space-y-1">
                      <textarea aria-label="The text" className={field} rows={4} value={text} onChange={e => setText(e.target.value)} />
                      <button type="button" className={button} disabled={!!busy} onClick={() => act('text', 'text', { text, from_hash: cur.hash }, 'PUT')}>
                        {`Save as version ${cur.version + 1}`}
                      </button>
                      {errs.text && <p data-testid="agreement-error-text" className="text-[11px] text-rose-300">{errs.text}</p>}
                    </div>
                  )}
                  {!executed && (
                    <div className="space-y-1" data-testid="agreement-execution-form">
                      <input aria-label="Date it was signed" type="date" className={field} value={ex.signed_on} onChange={e => setEx({ ...ex, signed_on: e.target.value })} />
                      <input aria-label="Evidence that it was executed" className={field} placeholder="What shows it was executed" value={ex.evidence} onChange={e => setEx({ ...ex, evidence: e.target.value })} />
                      <textarea aria-label="Formalities met" className={field} rows={2} placeholder="Each formality met, as you state it, one to a line" value={ex.formalities} onChange={e => setEx({ ...ex, formalities: e.target.value })} />
                      <button type="button" className={button} disabled={!!busy} onClick={() => act('executed', 'executed', {
                        hash: cur.hash, signed_on: ex.signed_on, evidence: ex.evidence,
                        formalities_met: ex.formalities.split('\n').map(s => s.trim()).filter(Boolean) })}>
                        {`Record the execution of version ${cur.version}`}
                      </button>
                      {errs.executed && <p data-testid="agreement-error-executed" className="text-[11px] text-rose-300">{errs.executed}</p>}
                    </div>
                  )}
                  {!fact('in_force')?.recorded && (
                    <div className="space-y-1">
                      <input aria-label="In force from" type="date" className={field} value={inf.from_date} onChange={e => setInf({ ...inf, from_date: e.target.value })} />
                      <input aria-label="What puts it in force" className={field} placeholder="What puts it in force, as you state it" value={inf.basis} onChange={e => setInf({ ...inf, basis: e.target.value })} />
                      <button type="button" className={button} disabled={!!busy} onClick={() => act('in_force', 'in-force', inf)}>Record that it is in force</button>
                      {errs.in_force && <p data-testid="agreement-error-in-force" className="text-[11px] text-rose-300">{errs.in_force}</p>}
                    </div>
                  )}
                  <div className="space-y-1">
                    <input aria-label="Date it ended" type="date" className={field} value={end.on} onChange={e => setEnd({ ...end, on: e.target.value })} />
                    <input aria-label="How it ended" className={field} placeholder="How it ended, as you state it" value={end.how} onChange={e => setEnd({ ...end, how: e.target.value })} />
                    <button type="button" className={button} disabled={!!busy} onClick={() => act('ended', 'ended', end)}>Record its end</button>
                    {errs.ended && <p data-testid="agreement-error-ended" className="text-[11px] text-rose-300">{errs.ended}</p>}
                  </div>
                  <div className="space-y-1">
                    <select aria-label="Signs for" className={field} value={sig.party_id} onChange={e => setSig({ ...sig, party_id: e.target.value })}>
                      <option value="">Signs for which party</option>
                      {open.parties.map((x: any) => <option key={x.party_id} value={x.party_id}>{x.party?.name ?? x.party_id}</option>)}
                    </select>
                    <input aria-label="Signatory name" className={field} placeholder="The signatory's name" value={sig.name} onChange={e => setSig({ ...sig, name: e.target.value })} />
                    <input aria-label="Signs as" className={field} placeholder="The capacity they sign in" value={sig.capacity} onChange={e => setSig({ ...sig, capacity: e.target.value })} />
                    <input aria-label="Authority, as stated" className={field} placeholder="Their authority, as stated" value={sig.authority_as_stated} onChange={e => setSig({ ...sig, authority_as_stated: e.target.value })} />
                    <input aria-label="Stated by" className={field} placeholder="Who stated it" value={sig.stated_by} onChange={e => setSig({ ...sig, stated_by: e.target.value })} />
                    <button type="button" className={button} disabled={!!busy} onClick={() => act('signatory', 'signatories', sig)}>Record this signatory</button>
                    {errs.signatory && <p data-testid="agreement-error-signatory" className="text-[11px] text-rose-300">{errs.signatory}</p>}
                  </div>
                </div>
              )}
            </section>
          )}
        </>
      )}

      {isc && (
        <section className="space-y-1 pt-4 border-t border-white/5" data-testid="agreements-service-contracts">
          <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Internal service contracts, listed apart</h4>
          <p className="text-[10px] text-slate-400">{isc.what_these_are}</p>
          {isc.unread ? (
            <p data-testid="agreements-service-contracts-unread" className="text-[11px] text-rose-300">{isc.unread}</p>
          ) : (isc.contracts ?? []).length === 0 ? (
            <p className="text-[11px] text-slate-500">None is recorded.</p>
          ) : (
            <ul className="space-y-1">
              {(isc.contracts ?? []).map((c: any) => (
                <li key={c.id} data-testid="agreements-service-contract" className="text-[11px] text-slate-300">
                  {`${c.id}: ${c.client_vsb} commissions ${c.provider_vsb} for ${c.price_wst} WST (virtual), ${c.status}`}
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}
