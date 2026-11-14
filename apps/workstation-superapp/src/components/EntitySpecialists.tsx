// W933 (P5.15 clause 6 and its RELEASE clause; row FU-1178 part 2) — AN ENTITY'S OWN SPECIALISTS, on its page.
// The roster is the entity's own and short, not a registry of people (GET/POST /api/v1/entity-specialists/{id},
// W932). Every sentence about it is the server's: the five places and why five, that no credential is verified, and
// whether Workstation recommends a specialist for this entity, with what engaging one would cost the entity and when
// one is warranted. This component types none of them. A refusal is shown in the server's own words; a failed read
// is said and never drawn as an empty roster.
import React, { useCallback, useEffect, useState } from 'react';
import { apiJson, errorMessage } from '../lib/api';

interface Specialist {
  specialist_id: string;
  name: string;
  discipline: string;
  credential_as_stated: string;
  reviews: string;
  lapses_on: string;
  state: string;
  retired_at?: string;
  retired_by?: string;
  retired_reason?: string;
}
interface Recommendation { recommended: boolean; said: string; charge: string; when_warranted: string }
interface Roster {
  limit: number;
  places_left: number;
  active: Specialist[];
  lapsed: Specialist[];
  retired: Specialist[];
  disciplines: string[];
  basis: string;
  credential_basis: string;
  recommendation: Recommendation;
}

//  the five things clause 5 names, and nothing else: the server refuses any other field
const BLANK = { name: '', discipline: '', credential_as_stated: '', reviews: '', lapses_on: '' };

export const EntitySpecialists: React.FC<{ vsbId: string }> = ({ vsbId }) => {
  const [roster, setRoster] = useState<Roster | null>(null);
  const [readError, setReadError] = useState('');
  const [form, setForm] = useState(BLANK);
  const [reasons, setReasons] = useState<Record<string, string>>({});
  const [refused, setRefused] = useState('');
  const [done, setDone] = useState('');
  const [busy, setBusy] = useState(false);
  const base = `/api/v1/entity-specialists/${encodeURIComponent(vsbId)}`;

  useEffect(() => {
    let live = true;
    setRoster(null);
    setReadError('');
    setRefused('');
    setDone('');
    apiJson<Roster>(base)
      .then(r => { if (live) setRoster(r); })
      .catch(e => { if (live) setReadError(errorMessage(e)); });
    return () => { live = false; };
  }, [base]);

  //  after a write the roster is read again; a failed re-read is said, and the roster is not drawn from memory
  const reread = useCallback(async () => {
    try {
      setRoster(await apiJson<Roster>(base));
      setReadError('');
    } catch (e) {
      setRoster(null);
      setReadError(errorMessage(e));
    }
  }, [base]);

  const attach = async () => {
    setBusy(true);
    setRefused('');
    setDone('');
    try {
      const a = await apiJson<{ specialist: Specialist }>(base, { method: 'POST', body: form });
      setDone(`Attached: ${a.specialist.name}.`);
      setForm(BLANK);
      await reread();
    } catch (e) {
      setRefused(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const retire = async (s: Specialist) => {
    setBusy(true);
    setRefused('');
    setDone('');
    try {
      await apiJson(`${base}/${encodeURIComponent(s.specialist_id)}/retire`, {
        method: 'POST', body: { reason: reasons[s.specialist_id] ?? '' } });
      setDone(`Retired: ${s.name}.`);
      await reread();
    } catch (e) {
      setRefused(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const field = 'bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white';
  return (
    <div data-testid="entity-specialists" className="space-y-3">
      <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight">This entity's own specialists</h4>
      {readError ? (
        <p data-testid="specialists-unread" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">
          Could not read this entity's roster — {readError}
        </p>
      ) : !roster ? (
        <p className="text-[10px] text-slate-600">Reading this entity's roster…</p>
      ) : (
        <>
          <div className="space-y-1 border border-slate-800 rounded-lg p-3">
            <p data-testid="specialists-recommendation" className={`text-[11px] leading-relaxed ${roster.recommendation.recommended ? 'text-highlight font-bold' : 'text-slate-400'}`}>
              {roster.recommendation.said}
            </p>
            <p data-testid="specialists-charge" className="text-[10px] text-slate-400 leading-relaxed">{roster.recommendation.charge}</p>
            <p data-testid="specialists-when" className="text-[10px] text-slate-400 leading-relaxed">{roster.recommendation.when_warranted}</p>
          </div>
          <p data-testid="specialists-basis" className="text-[10px] text-slate-500 leading-relaxed">{roster.basis}</p>
          <p data-testid="specialists-credential" className="text-[10px] text-slate-500 leading-relaxed">Credentials: {roster.credential_basis}.</p>
          <p data-testid="specialists-places" className="text-[10px] font-black uppercase tracking-widest text-slate-300">
            {roster.places_left} of {roster.limit} places free
          </p>
          {roster.active.length === 0 && (
            <p data-testid="specialists-none" className="text-[10px] text-slate-600">No specialist holds a place on this entity's roster.</p>
          )}
          {roster.active.map(s => (
            <div key={s.specialist_id} data-testid={`specialist-${s.specialist_id}`} className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <p className="text-sm font-black text-white">{s.name} — {s.discipline}</p>
              <p className="text-[10px] text-slate-400">Credential as stated: {s.credential_as_stated}</p>
              <p className="text-[10px] text-slate-400">Reviews: {s.reviews} · the place lapses on {s.lapses_on}</p>
              <div className="flex gap-2 items-center">
                <input value={reasons[s.specialist_id] ?? ''} aria-label={`Reason for retiring ${s.name}`}
                  placeholder="Reason for retiring"
                  onChange={e => setReasons(r => ({ ...r, [s.specialist_id]: e.target.value }))} className={field} />
                <button type="button" disabled={busy} onClick={() => retire(s)}
                  className="text-[10px] font-black uppercase text-slate-300 border border-slate-700 px-3 py-1.5 rounded-lg">Retire</button>
              </div>
            </div>
          ))}
          {roster.lapsed.map(s => (
            <p key={s.specialist_id} data-testid={`specialist-lapsed-${s.specialist_id}`} className="text-[10px] text-slate-500">
              {s.name} — {s.discipline} · lapsed: the place ran to {s.lapses_on}
            </p>
          ))}
          {roster.retired.map(s => (
            <p key={s.specialist_id} data-testid={`specialist-retired-${s.specialist_id}`} className="text-[10px] text-slate-500">
              {s.name} — {s.discipline} · retired {s.retired_at} by {s.retired_by}: {s.retired_reason}
            </p>
          ))}
          <div className="grid grid-cols-1 @[560px]:grid-cols-5 gap-2">
            <input value={form.name} aria-label="Specialist's name" placeholder="Name"
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))} className={field} />
            <select value={form.discipline} aria-label="Discipline"
              onChange={e => setForm(f => ({ ...f, discipline: e.target.value }))} className={field}>
              <option value="">Discipline</option>
              {roster.disciplines.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
            <input value={form.credential_as_stated} aria-label="Credential as stated" placeholder="Credential, as they state it"
              onChange={e => setForm(f => ({ ...f, credential_as_stated: e.target.value }))} className={field} />
            <input value={form.reviews} aria-label="What they review" placeholder="What they review for this entity"
              onChange={e => setForm(f => ({ ...f, reviews: e.target.value }))} className={field} />
            <input type="date" value={form.lapses_on} aria-label="Place lapses on"
              onChange={e => setForm(f => ({ ...f, lapses_on: e.target.value }))} className={field} />
          </div>
          <button type="button" disabled={busy} onClick={attach}
            className="text-[10px] font-black uppercase text-sovereign bg-highlight px-3 py-1.5 rounded-lg">Attach a specialist</button>
          {refused && <p data-testid="specialists-refused" role="alert" className="text-[11px] font-bold text-amber-400 leading-relaxed">{refused}</p>}
          {done && <p data-testid="specialists-done" className="text-[11px] text-slate-300">{done}</p>}
        </>
      )}
    </div>
  );
};
