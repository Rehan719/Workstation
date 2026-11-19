//  W1083 (P5.19 clauses 1, 2, 4 and 5, FU-1078) - PHYSICAL ASSETS AS RECORDS AND EVIDENCE, on the Law page beside the
//  agreements they are held under. Everything here is the routes' own (agentic_core/api/assets.py, W1082): an asset is
//  what a person entered, owned and possessed by party records and held under an agreement record; its six facts
//  are drawn apart, each "not evidenced" until a person attaches evidence with who, when and when it lapses; evidence
//  past its date reads lapsed, and a declaration of readiness resting on it reads withdrawn, with the route's reason.
//  Nothing across the six is computed here: no score, no percentage, no single word of readiness. Nothing connects to
//  the thing itself. With sign-in off nothing is kept, and the panel says the route's reason. Each read and each
//  action says its own failure, in its own place.
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

const BASE = '/api/v1/assets';
const KINDS: [string, string][] = [
  ['vehicle', 'a vehicle'], ['robot', 'a robot'], ['drone', 'a drone'],
  ['laboratory_instrument', 'a laboratory instrument'], ['other', 'something else'],
];
//  W1084 (P5.19 clause 3) - where it would be used; the rows that apply are the route's, said as it gave them
const USES: [string, string][] = [
  ['workplace', 'in a workplace'], ['road', 'on a road'], ['footway', 'on a public footway'], ['air', 'in the air'],
  ['elsewhere', 'somewhere else'],
];
const field = 'w-full p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-200';
const button = 'px-3 py-1.5 rounded-lg bg-slate-800 text-[10px] font-black uppercase tracking-widest text-aura disabled:opacity-40';

//  one fact, as the route answered it: each piece of evidence with who attached it, when, when it lapses and its
//  state, or the route's own "not evidenced"
function FactBlock({ f }: { f: any }) {
  return (
    <li data-testid="asset-fact" className="text-[11px] text-slate-300">
      <span className="font-black text-slate-100">{f.name}</span>{': '}
      {(f.evidence ?? []).length === 0 ? (
        <span className="text-slate-500">{f.said}</span>
      ) : (
        <span>
          {(f.evidence ?? []).map((e: any) => (
            <span key={e.id} data-testid="asset-evidence" className="block">
              {`${e.evidence}${e.named_person ? `, declared by ${e.named_person}` : ''} - attached by ${e.attached_by} at ${e.attached_at}, lapses on ${e.lapses_on}: ${e.state}`}
              {e.withdrawn_because && <span data-testid="asset-withdrawn" className="block text-amber-300">{`Withdrawn: ${e.withdrawn_because}`}</span>}
            </span>
          ))}
        </span>
      )}
    </li>
  );
}

export default function AssetsPanel() {
  const [list, setList] = useState<any | null>(null);
  const [listErr, setListErr] = useState('');
  const [parties, setParties] = useState<any[] | null>(null);
  const [agreements, setAgreements] = useState<any[] | null>(null);
  const [partiesErr, setPartiesErr] = useState('');
  const [agreementsErr, setAgreementsErr] = useState('');
  const [open, setOpen] = useState<any | null>(null);
  const openId = useRef<string | null>(null);
  const [errs, setErrs] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState('');
  const say = (k: string, v: string) => setErrs(e => ({ ...e, [k]: v }));
  const [a, setA] = useState({ what: '', kind: 'robot', owned_by: '', possessed_by: '', agreement_id: '', use: '' });
  const [use, setUse] = useState('');
  const [ev, setEv] = useState({ fact: 'right_to_use', evidence: '', lapses_on: '', named_person: '' });

  const readList = useCallback(async () => {
    setListErr('');
    try {
      setList(await apiJson(BASE));
    } catch (e) {
      setList(null);
      setListErr(`The asset records could not be read (${errorMessage(e)}), so none is shown.`);
    }
  }, []);
  //  who may own or possess an asset, and what it may be held under: the party and agreement records only, each
  //  read on its own, so one that could not be read is said as that and never takes the other down
  const readParties = useCallback(async () => {
    setPartiesErr('');
    try {
      const p = await apiJson('/api/v1/agreements/parties');
      setParties(Array.isArray(p?.parties) ? p.parties : []);
    } catch (e) {
      setParties(null);
      setPartiesErr(`The parties could not be read (${errorMessage(e)}), so no owner or possessor can be chosen.`);
    }
  }, []);
  const readAgreements = useCallback(async () => {
    setAgreementsErr('');
    try {
      const g = await apiJson('/api/v1/agreements');
      setAgreements(Array.isArray(g?.agreements) ? g.agreements : []);
    } catch (e) {
      setAgreements(null);
      setAgreementsErr(`The agreements could not be read (${errorMessage(e)}), so none can be chosen to hold it under.`);
    }
  }, []);
  useEffect(() => { readList(); readParties(); readAgreements(); }, [readList, readParties, readAgreements]);

  const show = (x: any) => { if (openId.current === x.id) setOpen(x); };
  const [openErr, setOpenErr] = useState('');
  //  a record opened is read again, and said under its own id only: an answer for one opened before is dropped
  const openRecord = async (id: string) => {
    openId.current = id;
    setOpen(null); setOpenErr(''); setErrs({});
    try {
      show(await apiJson(`${BASE}/${id}`));
    } catch (e) {
      if (openId.current === id) setOpenErr(`This asset record could not be read (${errorMessage(e)}).`);
    }
  };

  const enter = async () => {
    say('asset', ''); setBusy('asset');
    try {
      const x = await apiJson(BASE, { method: 'POST', body: a });
      setA({ what: '', kind: a.kind, owned_by: '', possessed_by: '', agreement_id: '', use: '' });
      openId.current = x.id; setErrs({}); show(x);
      await readList();
    } catch (e) {
      say('asset', `The asset was not entered: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };

  const attach = async () => {
    if (!open) return;
    const id = open.id;
    say('evidence', ''); setBusy('evidence');
    const body: Record<string, string> = { fact: ev.fact, evidence: ev.evidence, lapses_on: ev.lapses_on };
    if (ev.fact === 'readiness') body.named_person = ev.named_person;
    try {
      const x = await apiJson(`${BASE}/${id}/evidence`, { method: 'POST', body });
      show(x);
      if (openId.current === id) { setEv({ ...ev, evidence: '', lapses_on: '', named_person: '' }); await readList(); }
    } catch (e) {
      if (openId.current === id) say('evidence', `The evidence was not attached: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };

  //  W1084 - where it would be used, entered on the open record; the route's answer is said under its own id only
  const recordUse = async () => {
    if (!open) return;
    const id = open.id;
    say('use', ''); setBusy('use');
    try {
      show(await apiJson(`${BASE}/${id}/use`, { method: 'POST', body: { use } }));
      if (openId.current === id) await readList();
    } catch (e) {
      if (openId.current === id) say('use', `Where it would be used was not recorded: ${errorMessage(e)}`);
    } finally { setBusy(''); }
  };
  const choices = parties !== null && agreements !== null;
  return (
    <div className="space-y-6" data-testid="assets-panel">
      <div className="space-y-1">
        <h3 className="text-lg font-black text-white uppercase tracking-tight">Physical assets held under these agreements</h3>
        <p className="text-[11px] text-slate-400">
          A vehicle, a robot, a drone or an instrument, as a record and its evidence: six facts kept apart, each with who
          attached it, when and when it lapses.
        </p>
        {list?.controlled_basis && <p data-testid="assets-not-controlled" className="text-[10px] text-amber-300">{list.controlled_basis}</p>}
      </div>

      {list === null && !listErr && <p className="text-[11px] text-slate-500">Reading the asset records…</p>}
      {listErr && <p data-testid="assets-unread" className="text-[11px] text-rose-300">{listErr}</p>}
      {list && list.kept === false && <p data-testid="assets-not-kept" className="text-[11px] text-amber-300">{list.not_kept_because}</p>}

      {list && list.kept === true && (
        <>
          {list.judged_basis && <p data-testid="assets-not-judged" className="text-[10px] text-slate-400">{list.judged_basis}</p>}
          <section className="space-y-2">
            <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Enter an asset</h4>
            {!choices && !partiesErr && !agreementsErr && <p className="text-[11px] text-slate-500">Reading the parties and agreements…</p>}
            {partiesErr && <p data-testid="assets-parties-unread" className="text-[11px] text-rose-300">{partiesErr}</p>}
            {agreementsErr && <p data-testid="assets-agreements-unread" className="text-[11px] text-rose-300">{agreementsErr}</p>}
            {choices && (
              <div className="grid grid-cols-2 gap-2" data-testid="assets-form">
                <input aria-label="What the asset is" className={field} placeholder="What it is, as you would describe it" value={a.what} onChange={e => setA({ ...a, what: e.target.value })} />
                <select aria-label="Kind of asset" className={field} value={a.kind} onChange={e => setA({ ...a, kind: e.target.value })}>
                  {KINDS.map(([v, label]) => <option key={v} value={v}>{label}</option>)}
                </select>
                {([['owned_by', 'Owned by'], ['possessed_by', 'Possessed by']] as const).map(([k, label]) => (
                  <select key={k} aria-label={label} className={field} value={a[k]} onChange={e => setA({ ...a, [k]: e.target.value })}>
                    <option value="">{`${label}: choose a party`}</option>
                    {(parties ?? []).map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
                  </select>
                ))}
                <select aria-label="Held under" className={field} value={a.agreement_id} onChange={e => setA({ ...a, agreement_id: e.target.value })}>
                  <option value="">Held under: choose an agreement</option>
                  {(agreements ?? []).map((g: any) => <option key={g.id} value={g.id}>{g.title}</option>)}
                </select>
                <select aria-label="Where it would be used" className={field} value={a.use} onChange={e => setA({ ...a, use: e.target.value })}>
                  <option value="">Where it would be used: not said yet</option>
                  {USES.map(([v, label]) => <option key={v} value={v}>{label}</option>)}
                </select>
              </div>
            )}
            {choices && <button type="button" className={button} disabled={busy === 'asset'} onClick={enter}>Enter this asset</button>}
            {errs.asset && <p data-testid="assets-error" className="text-[11px] text-rose-300">{errs.asset}</p>}
          </section>

          <section className="space-y-2">
            <h4 className="text-[11px] font-black text-slate-200 uppercase tracking-widest">Asset records</h4>
            {(list.assets ?? []).length === 0 && <p data-testid="assets-none" className="text-[11px] text-slate-500">No asset is recorded yet.</p>}
            <ul className="space-y-1">
              {(list.assets ?? []).map((x: any) => (
                <li key={x.id} data-testid="asset-row">
                  <button type="button" className="text-left text-[11px] text-sky-300 underline" onClick={() => openRecord(x.id)}>
                    {`${x.what} - held under ${x.held_under?.title ?? x.held_under?.agreement_id}`}
                  </button>
                </li>
              ))}
            </ul>
          </section>

          {openErr && <p data-testid="asset-open-error" className="text-[11px] text-rose-300">{openErr}</p>}
          {open && (
            <section className="space-y-3 p-4 rounded-xl border border-slate-800" data-testid="asset-open">
              <h4 className="text-[12px] font-black text-white">{open.what}</h4>
              <p data-testid="asset-held" className="text-[10px] text-slate-400">
                {`Owned by ${open.owned_by?.name ?? open.owned_by?.party_id}; possessed by ${open.possessed_by?.name ?? open.possessed_by?.party_id}; held under ${open.held_under?.title ?? open.held_under?.agreement_id}. ${open.held_under?.basis}`}
              </p>
              <ul className="space-y-1">{(open.facts ?? []).map((f: any) => <FactBlock key={f.fact} f={f} />)}</ul>
              <div className="space-y-1" data-testid="asset-rules">
                <p className="text-[11px] font-black text-slate-100">
                  {open.rules?.use_name ? `Which rules apply, used ${open.rules.use_name}` : 'Which rules apply'}
                </p>
                {(open.rules?.rows ?? []).length === 0 ? (
                  <p data-testid="asset-rules-said" className="text-[11px] text-amber-300">{open.rules?.said}</p>
                ) : (
                  <ul className="space-y-1">
                    {(open.rules?.rows ?? []).map((r: any) => (
                      <li key={r.id} data-testid="asset-rule-row" className="text-[10px] text-slate-300">
                        {r.said ? `${r.id}: ${r.said}` : `${(r.names ?? [r.id])[0]} (${r.kind}, ${(r.nation ?? []).join(', ')}): read on ${r.read_on}, by ${r.read_by}. It says: ${r.says} Not read: ${r.not_read}.${r.stands && r.stands !== 'current' ? ` Marked ${r.stands} in the register.` : ''}${r.recently_checked ? '' : ` Not recently checked: ${r.checked_basis}.`}`}
                      </li>
                    ))}
                  </ul>
                )}
                <p data-testid="asset-rules-basis" className="text-[10px] text-slate-500">{open.rules?.basis}</p>
                <select aria-label="It would be used" className={field} value={use} onChange={e => setUse(e.target.value)}>
                  <option value="">It would be used: choose</option>
                  {USES.map(([v, label]) => <option key={v} value={v}>{label}</option>)}
                </select>
                <button type="button" className={button} disabled={busy === 'use'} onClick={recordUse}>Record where it would be used</button>
                {errs.use && <p data-testid="asset-use-error" className="text-[11px] text-rose-300">{errs.use}</p>}
              </div>
              <div className="space-y-1" data-testid="asset-evidence-form">
                <select aria-label="Evidence for" className={field} value={ev.fact} onChange={e => setEv({ ...ev, fact: e.target.value })}>
                  {(open.facts ?? []).map((f: any) => <option key={f.fact} value={f.fact}>{f.name}</option>)}
                </select>
                <input aria-label="The evidence" className={field} placeholder="What the evidence is and where it is kept" value={ev.evidence} onChange={e => setEv({ ...ev, evidence: e.target.value })} />
                <input aria-label="It lapses on" type="date" className={field} value={ev.lapses_on} onChange={e => setEv({ ...ev, lapses_on: e.target.value })} />
                {ev.fact === 'readiness' && (
                  <input aria-label="The person declaring it ready" className={field} placeholder="Who declares it ready" value={ev.named_person} onChange={e => setEv({ ...ev, named_person: e.target.value })} />
                )}
                <button type="button" className={button} disabled={busy === 'evidence'} onClick={attach}>Attach this evidence</button>
                {errs.evidence && <p data-testid="asset-evidence-error" className="text-[11px] text-rose-300">{errs.evidence}</p>}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
