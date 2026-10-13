import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { BookOpen, Eye, GitCompare, ListChecks, Loader2 } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';

// W684 — MEMORISATION PRACTICE (the four areas, first clause; Owner rulings 2026-10-12). Three things a learner
// does for themselves: set a portion in each of three tracks, practise a verse with its words hidden, and set
// similar verses side by side. EVERY SENTENCE ABOUT WHAT THIS IS comes from the server's answer. Nothing here
// is told what the learner recalled, and nothing here shows a score, a count of mistakes or a rank.

type Portion = { unit: string; start: number | string; end: number | string; set_by: string; set_at: string } | null;
interface Portions { tracks: string[]; portions: Record<string, Portion>; tracks_set: number; defaults_basis: string; earlier_portions_kept: number; identity_verified?: boolean }
interface Hidden { ref: string; shown: string; hidden_words: number; total_words: number; revealed: boolean; text?: string; basis: string; judged_basis: string; source?: string; edition?: string; riwayah?: string | null }
interface Pair { a: string; b: string; shared_words: number; shared: string; a_continues: string | null; b_continues: string | null; whole_verse_identical: boolean }
interface Similar { pairs: Pair[]; pairs_found: number; pairs_returned: number; verses_examined: number; verses_not_available: number; complete_for_these_surahs: boolean; basis: string; scholar_reviewed_basis: string }

const TRACK_LABEL: Record<string, string> = { new_lesson: 'New lesson', recent_revision: 'Recent revision', old_revision: 'Old revision' };
const inputCls = 'text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300';

export const HifzPractice: React.FC<{ uid: string }> = ({ uid }) => {
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState('');

  // ── the plan ──
  const [plan, setPlan] = useState<Portions | null>(null);
  const [track, setTrack] = useState('new_lesson');
  const [unit, setUnit] = useState('page');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [setBy, setSetBy] = useState('learner');
  const loadPlan = () => apiJson<Portions>(`/api/v1/qep/hifz/portions/${encodeURIComponent(uid)}`).then(setPlan).catch(e => setErr(errorMessage(e)));
  useEffect(() => { loadPlan(); }, [uid]);
  const savePortion = async () => {
    setBusy('portion'); setErr('');
    const asValue = (v: string) => (unit === 'ayah_range' ? v.trim() : Number(v));
    try {
      await apiJson('/api/v1/qep/hifz/portion', { method: 'POST', body: { uid, track, unit, start: asValue(start), end: asValue(end), set_by: setBy } });
      await loadPlan();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── the hidden verse ──
  const [surah, setSurah] = useState(1);
  const [ayah, setAyah] = useState(1);
  const [hidden, setHidden] = useState<Hidden | null>(null);
  const [seen, setSeen] = useState<string[]>([]);
  const [ended, setEnded] = useState(false);
  const openHidden = async (reveal = false) => {
    setBusy('hidden'); setErr('');
    try {
      const r = await apiJson<Hidden>(`/api/v1/qep/hifz/practice/${surah}/${ayah}${reveal ? '?reveal=true' : ''}`);
      setHidden(r);
      if (!reveal) { setSeen(r.shown ? [r.shown] : []); setEnded(r.hidden_words === 0); }
    } catch (e) { setHidden(null); setErr(errorMessage(e)); }
    setBusy('');
  };
  const nextWord = async () => {
    setBusy('next'); setErr('');
    try {
      const r = await apiJson<{ word: string | null; end_of_verse: boolean }>(`/api/v1/qep/hifz/practice/${surah}/${ayah}/next?after_words=${seen.length}`);
      if (r.word) setSeen(s => [...s, r.word as string]);
      setEnded(r.end_of_verse);
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── similar verses ──
  const [surahs, setSurahs] = useState('');
  const [similar, setSimilar] = useState<Similar | null>(null);
  const findSimilar = async () => {
    setBusy('similar'); setErr(''); setSimilar(null);
    try { setSimilar(await apiJson<Similar>(`/api/v1/qep/hifz/similar?surahs=${encodeURIComponent(surahs.trim())}`)); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  return (
    <div className="space-y-4" data-testid="hifz-practice">
      {err && <p data-testid="hifz-practice-error" className="text-[10px] text-vital">{err}</p>}

      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><ListChecks size={14} /> Your plan — three tracks</h3>
        {plan && <p data-testid="hifz-plan-defaults" className="text-[9px] text-slate-500 mb-3 leading-relaxed">{plan.defaults_basis}</p>}
        <div className="grid sm:grid-cols-3 gap-2 mb-3">
          {(plan?.tracks ?? []).map(t => {
            const p = plan?.portions[t];
            return (
              <div key={t} data-testid={`hifz-track-${t}`} className="p-2 rounded-lg border border-slate-900">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">{TRACK_LABEL[t] ?? t}</p>
                {p ? <p className="text-[11px] text-white">{p.unit.replace('_', ' ')} {String(p.start)}{String(p.start) !== String(p.end) ? ` to ${String(p.end)}` : ''} <span className="text-[9px] text-slate-500">· set by {p.set_by}</span></p>
                   : <p className="text-[11px] text-slate-500">not set</p>}
              </div>
            );
          })}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <select aria-label="Track" value={track} onChange={e => setTrack(e.target.value)} className={inputCls}>
            {(plan?.tracks ?? Object.keys(TRACK_LABEL)).map(t => <option key={t} value={t}>{TRACK_LABEL[t] ?? t}</option>)}
          </select>
          <select aria-label="Unit" value={unit} onChange={e => setUnit(e.target.value)} className={inputCls}>
            <option value="page">page</option><option value="juz">juz</option><option value="ayah_range">ayah range</option>
          </select>
          <input aria-label="From" value={start} onChange={e => setStart(e.target.value)} placeholder={unit === 'ayah_range' ? '2:1' : 'from'} className={`${inputCls} w-20`} />
          <input aria-label="To" value={end} onChange={e => setEnd(e.target.value)} placeholder={unit === 'ayah_range' ? '2:5' : 'to'} className={`${inputCls} w-20`} />
          <select aria-label="Set by" value={setBy} onChange={e => setSetBy(e.target.value)} className={inputCls}>
            <option value="learner">I set this</option><option value="teacher">my teacher set this</option>
          </select>
          <Button onClick={savePortion} disabled={busy === 'portion' || !start || !end} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
            {busy === 'portion' ? <Loader2 size={11} className="animate-spin" /> : <ListChecks size={11} />} Set portion
          </Button>
        </div>
      </Card>

      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Eye size={14} /> Hidden verse</h3>
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <input aria-label="Surah" type="number" min={1} max={114} value={surah} onChange={e => setSurah(Number(e.target.value))} className={`${inputCls} w-16`} />
          <input aria-label="Ayah" type="number" min={1} value={ayah} onChange={e => setAyah(Number(e.target.value))} className={`${inputCls} w-16`} />
          <Button onClick={() => openHidden(false)} disabled={busy === 'hidden'} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
            {busy === 'hidden' ? <Loader2 size={11} className="animate-spin" /> : <BookOpen size={11} />} Begin
          </Button>
        </div>
        {hidden && (
          <div data-testid="hifz-hidden">
            <p dir="rtl" lang="ar" data-testid="hifz-hidden-text" className="text-xl text-white leading-loose mb-2">
              {hidden.revealed && hidden.text ? hidden.text : seen.join(' ')}{!hidden.revealed && !ended ? ' …' : ''}
            </p>
            <p data-testid="hifz-hidden-count" className="text-[9px] text-slate-500 mb-2">
              {hidden.ref} · {hidden.revealed ? hidden.total_words : seen.length} of {hidden.total_words} words shown
              {hidden.source ? ` · ${hidden.source}` : ''}{hidden.edition ? ` · ${hidden.edition}` : ''}{hidden.riwayah ? ` · ${hidden.riwayah}` : ''}
            </p>
            <div className="flex flex-wrap gap-2 mb-2">
              <Button onClick={nextWord} disabled={busy === 'next' || ended || hidden.revealed} className="bg-slate-900 text-slate-200 text-[10px]">Next word</Button>
              <Button onClick={() => openHidden(true)} disabled={busy === 'hidden' || hidden.revealed} className="bg-slate-900 text-slate-200 text-[10px]">Show the whole verse</Button>
            </div>
            <p data-testid="hifz-hidden-judged" className="text-[9px] text-slate-600 leading-relaxed">{hidden.judged_basis}</p>
          </div>
        )}
      </Card>

      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><GitCompare size={14} /> Similar verses, side by side</h3>
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <input aria-label="Surahs to compare" value={surahs} onChange={e => setSurahs(e.target.value)} placeholder="one to three surah numbers, e.g. 55 or 2,3" className={`${inputCls} w-72`} />
          <Button onClick={findSimilar} disabled={busy === 'similar' || !surahs.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
            {busy === 'similar' ? <Loader2 size={11} className="animate-spin" /> : <GitCompare size={11} />} Compare
          </Button>
        </div>
        {similar && (
          <div data-testid="hifz-similar">
            <p data-testid="hifz-similar-basis" className="text-[9px] text-slate-500 leading-relaxed">{similar.basis}</p>
            <p data-testid="hifz-similar-scholar" className="text-[9px] text-amber-300/90 leading-relaxed mb-2">{similar.scholar_reviewed_basis}</p>
            {!similar.complete_for_these_surahs && (
              <p data-testid="hifz-similar-incomplete" className="text-[9px] text-vital mb-2">{similar.verses_not_available} verse(s) could not be fetched, so this list does not cover the whole of these surahs.</p>
            )}
            <p className="text-[9px] text-slate-500 mb-2">{similar.pairs_returned} of {similar.pairs_found} pair(s) shown · {similar.verses_examined} verse(s) examined</p>
            <div className="space-y-2">
              {similar.pairs.map(p => (
                <div key={`${p.a}-${p.b}`} data-testid={`hifz-pair-${p.a}-${p.b}`} className="p-2 rounded-lg border border-slate-900">
                  <p className="text-[10px] font-mono text-slate-400">{p.a} and {p.b} · {p.shared_words} words shared{p.whole_verse_identical ? ' · the whole verse is the same' : ''}</p>
                  <p dir="rtl" lang="ar" className="text-base text-white leading-loose">{p.shared}</p>
                  {!p.whole_verse_identical && (
                    <p className="text-[9px] text-slate-500">
                      then {p.a} continues <span dir="rtl" lang="ar" className="text-sm text-slate-200">{p.a_continues ?? '(ends)'}</span> and {p.b} continues <span dir="rtl" lang="ar" className="text-sm text-slate-200">{p.b_continues ?? '(ends)'}</span>
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};
