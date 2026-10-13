import React, { useEffect, useRef, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { BookOpen, Brain, Loader2, Sparkles, Trophy, Languages, CheckCircle2 } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';
import { HifzPractice } from './HifzPractice';

// W439 — the REAL Quran Education Platform surface (Owner directive: QEP lives in the Religion
// domain). Every capability here is a wired backend route that was AUDITED before wiring:
// authentic Qur'an text (alquran.cloud — never AI-generated, per the constitution), real SM-2
// hifz scheduling, a written-recall check that says NOTHING about pronunciation, AI lesson
// outlines with serving provenance (floor-served output is labelled an outline, not a lesson),
// translation that REFUSES when only the deterministic floor is available, and gamification from
// a persisted award store (the old surface claimed "recorded" while persisting nothing).

interface Surah { number: number; name_arabic: string; name_transliteration: string; name_english: string; ayah_count: number; revelation_type: string }
interface Ayah { number_in_surah: number; text_arabic: string }
// W671 (ledger v16 R1.5) — what the surah and ayah routes have always returned beside the text and this
// component dropped. Every value is the server's; an absent riwayah is said, never filled in.
interface CorpusProvenance {
  source?: string; edition?: string; script?: string | null; riwayah?: string | null;
  licence?: string; provenance_basis?: string; basmala?: string | null; basmala_note?: string | null;
}
interface HifzProgress { total_ayaat_in_schedule: number; total_ayaat_memorised: number; due_today: number; due_refs: string[]; total_sessions: number; identity_verified?: boolean; identity_basis?: string }
interface MonthCount { month: string; days_reviewed: number; awards_recorded: number }
interface OwnProgress { this_month: MonthCount; last_month: MonthCount; basis: string }
interface GamiState { xp: number; level: number; level_basis: string; achievements: string[]; days_reviewed_this_month: number; days_reviewed_basis: string; awards_recorded: number; scope: string; own_progress?: OwnProgress }
interface Recall { comparable: boolean; reason?: string; text_similarity?: number; similarity_basis?: string; exact_similarity?: number; exact_similarity_basis?: string; missing_rule_markers?: string[]; markers_basis?: string; scope?: string }

const UID = 'local';

function Chip({ tone, children, title }: { tone: 'ok' | 'warn' | 'dim'; children: React.ReactNode; title?: string }) {
  const cls = tone === 'ok' ? 'bg-emerald-500/15 text-emerald-400' : tone === 'warn' ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400';
  return <span title={title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cls}`}>{children}</span>;
}

export const QEPStudio: React.FC = () => {
  const [suwar, setSuwar] = useState<Surah[] | null>(null);
  const [surahNo, setSurahNo] = useState(1);
  const [ayaat, setAyaat] = useState<Ayah[] | null>(null);
  const [surahMeta, setSurahMeta] = useState<CorpusProvenance | null>(null);
  const [progress, setProgress] = useState<HifzProgress | null>(null);
  const [gami, setGami] = useState<GamiState | null>(null);
  const [err, setErr] = useState('');
  const [loadErrs, setLoadErrs] = useState<string[]>([]);
  const [busy, setBusy] = useState('');

  const getJson = (url: string, set: (d: any) => void) =>
    fetch(url)
      .then(r => (r.ok ? r.json() : r.json().catch(() => ({})).then((b: any) =>
        Promise.reject(new Error(b?.detail ? String(b.detail).slice(0, 140) : `${url} → HTTP ${r.status}`)))))
      .then(set)
      .catch(e => setLoadErrs(errs => [...errs, String(e?.message ?? e)]));

  // W444 — the platform's own honesty statement (per-component truth lines + the constitutional
  // constraints) and the translation availability were served but never shown to anyone.
  const [qepStatus, setQepStatus] = useState<any>(null);
  const [trStatus, setTrStatus] = useState<any>(null);
  const loadCore = () => {
    setLoadErrs([]);
    getJson(`/api/v1/qep/hifz/progress/${UID}`, setProgress);
    getJson(`/api/v1/qep/gamification/${UID}`, setGami);
    getJson('/api/v1/qep/status', setQepStatus);
    fetch('/api/v1/qep/translation/status')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(setTrStatus)
      .catch(() => setTrStatus(null));   // unknown availability is shown as unknown, never assumed
  };
  const [suwarFailed, setSuwarFailed] = useState(false);
  const loadSuwar = () => {
    setSuwarFailed(false);
    fetch('/api/v1/qep/suwar')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then(d => setSuwar(d.suwar || []))
      .catch(() => setSuwarFailed(true));   // refuter catch: a failed load showed 'loading…' forever
  };
  useEffect(() => {
    loadSuwar();
    loadCore();
  }, []);

  const loadSurah = async (n: number) => {
    setBusy('surah'); setErr(''); setAyaat(null); setSurahMeta(null);
    try {
      const d = await apiJson(`/api/v1/qep/surah/${n}`);
      setAyaat(d.ayaat || []);
      setSurahMeta(d);
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── hifz scheduling + review ──
  const [rangeStart, setRangeStart] = useState(1);
  const [rangeEnd, setRangeEnd] = useState(5);
  const schedule = async () => {
    setBusy('schedule'); setErr('');
    try {
      await apiJson('/api/v1/qep/hifz/schedule', { method: 'POST', body: { uid: UID, surah_number: surahNo, ayaat_range: [rangeStart, rangeEnd] } });
      loadCore();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  const [reviewRef, setReviewRef] = useState<string | null>(null);
  const [reviewAyah, setReviewAyah] = useState<({ text_arabic: string; surah_name: string } & CorpusProvenance) | null>(null);
  //  P3.9 — the route already returns the e-factor and the basis; the screen typed neither, so a
  //  learner saw an interval with no indication of what it was computed from, and the one line
  //  that matters - 'a review count, not a hifz certification' - never reached them.
  const [reviewResult, setReviewResult] = useState<{ new_interval_days: number; next_review_date: string; xp_awarded: number; new_efactor?: number; memorised_basis?: string; total_ayaat_memorised?: number } | null>(null);
  const [meaning, setMeaning] = useState<{ translation_text: string; translator: string; work: string; first_published: number; source: string; edition: string; label: string; register_note: string; licence_basis: string } | null>(null);
  const showMeaning = async () => {
    if (!reviewRef) return;
    setBusy('meaning'); setErr('');
    const [ms, ma] = reviewRef.split(':');
    try { setMeaning(await apiJson(`/api/v1/qep/translation/${ms}/${ma}`)); } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };
  //  W717 (OWNER RULING 2026-10-13) - a REFERENCE recitation to listen to, the words lighting as it plays.
  //  Fetched only when asked for, played from the publisher's own address and never stored. Nothing here
  //  listens to the learner, and nothing here assesses anyone.
  type ListenVerse = { verse_key: string; from_ms: number; to_ms: number; words: { word: number; from_ms: number; to_ms: number }[] };
  type Listen = { audio_url: string; reciter_id: number; credit?: string; environment?: string; assessed_basis?: string; verses: ListenVerse[] };
  const [reciters, setReciters] = useState<{ id: number; name: string }[] | null>(null);
  const [reciterId, setReciterId] = useState<number | null>(null);
  const [listen, setListen] = useState<Listen | null>(null);
  const [listenRefusal, setListenRefusal] = useState('');
  const [litWord, setLitWord] = useState<number | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const listenVerse = listen && reviewRef ? listen.verses.find(v => v.verse_key === reviewRef) ?? null : null;
  const shownWords = reviewAyah ? reviewAyah.text_arabic.trim().split(/\s+/) : [];
  //  the words light ONLY when the publisher times as many words as the text shown has; otherwise the
  //  recitation still plays and the page says why nothing lights
  const wordsLight = !!listenVerse && listenVerse.words.length === shownWords.length;
  const startListening = async (chosen?: number) => {
    if (!reviewRef) return;
    setBusy('listen'); setListenRefusal(''); setLitWord(null);
    try {
      let list = reciters;
      if (!list) {
        list = ((await apiJson('/api/v1/qep/recitation/reciters')).reciters ?? []) as { id: number; name: string }[];
        setReciters(list);
      }
      //  the default is chosen by the publisher's own name for the reciter, never by a number typed here
      const id = chosen ?? reciterId ?? (list.find(r => /husar/i.test(r.name)) ?? list[0])?.id;
      if (id == null) { setListen(null); setListenRefusal('The publisher lists no reciter, so nothing can be played.'); setBusy(''); return; }
      setReciterId(id);
      const [ls] = reviewRef.split(':');
      setListen(await apiJson(`/api/v1/qep/recitation/audio/${ls}?reciter_id=${id}`));
    } catch (e) { setListen(null); setListenRefusal(errorMessage(e)); }
    setBusy('');
  };
  const onAudioReady = () => { if (audioRef.current && listenVerse) audioRef.current.currentTime = listenVerse.from_ms / 1000; };
  //  found by driving it: after the verse ended, play did nothing, because the position was already past
  //  the verse. Play always begins the verse again unless it is part-way through it.
  const onAudioPlay = () => {
    const a = audioRef.current;
    if (!a || !listenVerse) return;
    const ms = a.currentTime * 1000;
    if (ms < listenVerse.from_ms || ms >= listenVerse.to_ms - 50) a.currentTime = listenVerse.from_ms / 1000;
  };
  const onAudioTime = () => {
    const a = audioRef.current;
    if (!a || !listenVerse) return;
    const ms = a.currentTime * 1000;
    if (ms >= listenVerse.to_ms) { a.pause(); setLitWord(null); return; }   // one verse, then it stops
    const i = listenVerse.words.findIndex(w => ms >= w.from_ms && ms < w.to_ms);
    setLitWord(i >= 0 ? i : null);
  };
  const openReview = async (ref: string) => {
    setReviewRef(ref); setReviewAyah(null); setReviewResult(null); setRecall(null); setRecallText(''); setMeaning(null);
    setListen(null); setListenRefusal(''); setLitWord(null);
    const [s, a] = ref.split(':');
    try { setReviewAyah(await apiJson(`/api/v1/qep/ayah/${s}/${a}`)); } catch (e) { setErr(errorMessage(e)); }
  };
  const submitReview = async (quality: number) => {
    if (!reviewRef) return;
    setBusy('review'); setErr('');
    try {
      setReviewResult(await apiJson('/api/v1/qep/hifz/review', { method: 'POST', body: { uid: UID, ayah_ref: reviewRef, quality } }));
      loadCore();
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── written-recall check (TEXT only — never a recitation judgement) ──
  const [recallText, setRecallText] = useState('');
  const [recall, setRecall] = useState<Recall | null>(null);
  const checkRecall = async () => {
    if (!reviewAyah) return;
    setBusy('recall'); setErr('');
    try {
      // W630 (FU-545) — the server fetches the reference from surah + ayah; the page no longer supplies it
      const [rs, ra] = (reviewRef ?? '').split(':').map(Number);
      const d = await apiJson('/api/v1/qep/tajweed/analyse', { method: 'POST', body: { surah: rs, ayah: ra, recited_text: recallText } });
      setRecall(d.comparison);
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── lesson plans (provenance disclosed) ──
  const [rule, setRule] = useState('idgham');
  // W613 (FU-477) — review_state / review_note / withheld_note are TYPED and RENDERED: a withheld lesson
  // showed the "outline" chip and an empty box, and never the reason nothing appeared.
  const [lesson, setLesson] = useState<{ lesson_plan: string | null; served_by: string; floor_served: boolean; floor_note?: string; disclaimer: string; review_state?: string; review_note?: string; withheld_note?: string | null } | null>(null);
  const runLesson = async () => {
    setBusy('lesson'); setErr(''); setLesson(null);
    try { setLesson(await apiJson('/api/v1/qep/tajweed/lesson', { method: 'POST', body: { rule_name: rule } })); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── translation (refuses honestly on floor-only) ──
  const [trText, setTrText] = useState('');
  const [trResult, setTrResult] = useState<{ translation: string | null; served_by: string; label: string; withheld_note?: string | null } | null>(null);
  const [trRefusal, setTrRefusal] = useState('');
  const runTranslate = async () => {
    setBusy('translate'); setErr(''); setTrResult(null); setTrRefusal('');
    try { setTrResult(await apiJson('/api/v1/qep/translation/translate', { method: 'POST', body: { text: trText, target_language: 'English' } })); }
    catch (e) { setTrRefusal(errorMessage(e)); }   // the 503 refusal is the honesty working
    setBusy('');
  };

  const selSurah = (suwar ?? []).find(s => s.number === surahNo);

  return (
    <div className="space-y-6">
      {err && <p className="text-vital text-xs font-bold">{err}</p>}
      {loadErrs.length > 0 && (
        <p className="text-amber-400 text-[10px] font-bold">{loadErrs.length} section(s) failed to load — {loadErrs.slice(0, 2).join(' · ')}</p>
      )}

      {/* W685 (OWNER RULING 2026-10-12) — A LEARNER SEES THEIR OWN PROGRESS, NEVER A RANK. The ranking of learners
          that stood here is retired (its route answers that it is, and its code is kept). What is shown is this
          learner's own two months, counted by the server from their own recorded history, with the server's
          sentence saying so. */}
      {gami?.own_progress && (
        <Card className="p-4" data-testid="qep-own-progress">
          <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-2">your progress — this month against last</p>
          <div className="grid grid-cols-2 gap-2">
            {[gami.own_progress.this_month, gami.own_progress.last_month].map((m, i) => (
              <div key={m.month} data-testid={i === 0 ? 'qep-own-this-month' : 'qep-own-last-month'} className="p-2 rounded-lg border border-slate-900">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-500">{i === 0 ? 'this month' : 'last month'} · {m.month}</p>
                <p className="text-[11px] text-white">{m.days_reviewed} day(s) reviewed · {m.awards_recorded} review(s) recorded</p>
              </div>
            ))}
          </div>
          <p data-testid="qep-own-progress-basis" className="text-[9px] text-slate-500 mt-2 leading-relaxed">{gami.own_progress.basis}</p>
        </Card>
      )}

      {/* gamification strip — REAL persisted awards only */}
      {/* W444 — the QEP ops strip: each component's honest state line, and the constraints that
          govern the whole platform, on screen instead of API-only. */}
      {qepStatus && (
        <Card className="p-4">
          <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-2">QEP components — honest state</p>
          <div className="flex flex-wrap gap-1.5">
            {Object.entries(qepStatus.components || {}).map(([k, v]) => (
              <span key={k} title={String(v)}
                className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${/only|no |never|unavailable/i.test(String(v)) ? 'bg-slate-800 text-slate-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                {k}
              </span>
            ))}
          </div>
          {(qepStatus.constraints || []).length > 0 && (
            <p className="text-[9px] text-amber-400/80 italic mt-2">{(qepStatus.constraints || []).join(' · ')}</p>
          )}
        </Card>
      )}

      {gami && (
        <div className="flex items-center gap-2 flex-wrap">
          <Chip tone="ok" title={gami.level_basis}>level {gami.level}</Chip>
          <Chip tone="ok">{gami.xp} XP</Chip>
          <Chip tone="dim" title={gami.days_reviewed_basis}>{gami.days_reviewed_this_month} day(s) reviewed this month</Chip>
          <Chip tone="dim">{gami.awards_recorded} awards recorded</Chip>
          <span className="text-[9px] text-slate-600">{gami.scope}</span>
        </div>
      )}

      <div className="grid grid-cols-1 @[960px]:grid-cols-2 gap-4">
        {/* ── Qur'an reader + scheduling ── */}
        <Card className="p-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><BookOpen size={14} /> Qur'an — authentic text</h3>
          <p className="text-[9px] text-slate-600 mb-3">Arabic text from alquran.cloud (constitutional source) — never AI-generated. Unreachable source reports 503 honestly.</p>
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <select value={surahNo} onChange={e => setSurahNo(Number(e.target.value))}
              className="text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300 max-w-56">
              {(suwar ?? []).map(s => <option key={s.number} value={s.number}>{s.number}. {s.name_transliteration} ({s.ayah_count} ayaat)</option>)}
              {suwar === null && !suwarFailed && <option>loading surahs…</option>}
              {suwarFailed && <option>surah list unavailable — source unreachable</option>}
            </select>
            {suwarFailed && (
              <button type="button" onClick={loadSuwar} className="text-[9px] font-black uppercase px-2 py-1 rounded border border-slate-700 text-slate-400 hover:text-white">Retry</button>
            )}
            <Button onClick={() => loadSurah(surahNo)} disabled={busy === 'surah'} className="flex items-center gap-1.5 bg-aura text-sovereign text-[10px]">
              {busy === 'surah' ? <Loader2 size={11} className="animate-spin" /> : <BookOpen size={11} />} Read
            </Button>
          </div>
          {ayaat && (
            <>
              <div className="max-h-64 overflow-y-auto p-3 rounded-xl bg-slate-950 border border-slate-900 mb-1">
                {surahMeta?.basmala && (
                  <p data-testid="reader-basmala" title={surahMeta.basmala_note || undefined}
                     className="text-base text-slate-400 leading-loose font-arabic mb-2" dir="rtl">{surahMeta.basmala}</p>
                )}
                {ayaat.map(a => (
                  <p key={a.number_in_surah} className="text-lg text-white leading-loose font-arabic mb-2" dir="rtl">
                    {a.text_arabic} <span className="text-[10px] text-aura">({a.number_in_surah})</span>
                  </p>
                ))}
              </div>
              <p data-testid="reader-provenance" className="text-[9px] text-slate-500 mb-1">
                {surahMeta?.source ?? 'source not stated'} · edition {surahMeta?.edition ?? 'not stated'} · {surahMeta?.riwayah ? `riwayah ${surahMeta.riwayah}` : 'riwayah not declared'}
                {surahMeta?.basmala && surahMeta?.basmala_note ? ` · Basmala ${surahMeta.basmala_note}` : ''}
              </p>
              {surahMeta?.provenance_basis && <p data-testid="reader-provenance-basis" className="text-[9px] text-slate-600 mb-1">{surahMeta.provenance_basis}</p>}
              {surahMeta?.licence && <p data-testid="reader-licence" className="text-[9px] text-slate-600 mb-3">Licence: {surahMeta.licence}</p>}
            </>
          )}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-[9px] font-black uppercase text-slate-500">memorise ayaat</span>
            <input type="number" min={1} max={selSurah?.ayah_count ?? 286} value={rangeStart} onChange={e => setRangeStart(Number(e.target.value))}
              className="w-16 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300" />
            <span className="text-slate-600 text-[10px]">to</span>
            <input type="number" min={1} max={selSurah?.ayah_count ?? 286} value={rangeEnd} onChange={e => setRangeEnd(Number(e.target.value))}
              className="w-16 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-1.5 text-slate-300" />
            <Button onClick={schedule} disabled={busy === 'schedule'} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
              {busy === 'schedule' ? <Loader2 size={11} className="animate-spin" /> : <Brain size={11} />} Schedule (SM-2)
            </Button>
          </div>
        </Card>

        {/* ── Hifz reviews — real SM-2 ── */}
        <Card className="p-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Brain size={14} /> Hifz — spaced repetition (real SM-2)</h3>
          {progress && (
            <div className="flex items-center gap-2 flex-wrap mb-3">
              <Chip tone="dim">{progress.total_ayaat_in_schedule} scheduled</Chip>
              <Chip tone="ok">{progress.total_ayaat_memorised} memorised (≥1 successful review)</Chip>
              {/* W648 (FU-627, ruled) — whose record this is, in the server's words */}
              {progress.identity_verified === false && progress.identity_basis && (
                <p data-testid="hifz-identity-basis" className="basis-full text-[9px] text-amber-300/90">{progress.identity_basis}</p>
              )}
              <Chip tone={progress.due_today > 0 ? 'warn' : 'dim'}>{progress.due_today} due today</Chip>
              <Chip tone="dim">{progress.total_sessions} sessions</Chip>
            </div>
          )}
          <div className="flex flex-wrap gap-1.5 mb-3">
            {(progress?.due_refs ?? []).map(ref => (
              <button key={ref} type="button" onClick={() => openReview(ref)}
                className={`text-[10px] font-mono px-2 py-1 rounded-lg border transition-colors ${reviewRef === ref ? 'border-aura/40 text-aura bg-aura/5' : 'border-slate-800 text-slate-400 hover:text-white'}`}>{ref}</button>
            ))}
            {progress && progress.due_refs.length === 0 && <p className="text-[10px] text-slate-600 italic">nothing due — schedule ayaat on the left</p>}
            {progress && progress.due_today > progress.due_refs.length && (
              <p className="text-[9px] text-slate-600">showing the first {progress.due_refs.length} of {progress.due_today} due</p>
            )}
          </div>
          {reviewRef && reviewAyah && (
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              {/* W717 - the same fetched text in both branches: split on spaces and joined with spaces, never altered */}
              <p className="text-xl text-white leading-loose font-arabic mb-2" dir="rtl">
                {wordsLight
                  ? shownWords.map((w, i) => <span key={i} data-testid={litWord === i ? 'listen-word-lit' : undefined} className={litWord === i ? 'text-aura' : undefined}>{w}{' '}</span>)
                  : reviewAyah.text_arabic}
              </p>
              <p data-testid="review-provenance" className="text-[9px] text-slate-500 mb-2" title={reviewAyah.provenance_basis || undefined}>
                {reviewAyah.source ?? 'source not stated'} · edition {reviewAyah.edition ?? 'not stated'} · {reviewAyah.riwayah ? `riwayah ${reviewAyah.riwayah}` : 'riwayah not declared'}
              </p>
              <div data-testid="listen-reference" className="mb-2">
                <button type="button" onClick={() => startListening()} disabled={busy === 'listen'}
                  className="text-[9px] font-bold text-sky-400 hover:text-sky-300 underline underline-offset-2">
                  {busy === 'listen' ? 'Fetching…' : 'Listen to a reference recitation'}
                </button>
                {reciters && reciters.length > 1 && (
                  <select aria-label="Reciter" value={reciterId ?? ''} onChange={e => startListening(Number(e.target.value))}
                    className="ml-2 text-[9px] bg-slate-900 border border-slate-800 rounded text-slate-300">
                    {reciters.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
                  </select>
                )}
                {listenRefusal && <p data-testid="listen-refusal" className="text-[9px] text-amber-300/90 mt-1">{listenRefusal}</p>}
                {listen && !listenVerse && (
                  <p data-testid="listen-no-timing" className="text-[9px] text-amber-300/90 mt-1">
                    The publisher gives no timing for {reviewRef}, so this verse cannot be played by itself.
                  </p>
                )}
                {listen && listenVerse && (
                  <>
                    <audio ref={audioRef} src={listen.audio_url} controls preload="none"
                      onLoadedMetadata={onAudioReady} onPlay={onAudioPlay} onTimeUpdate={onAudioTime} className="mt-1 w-full h-8" />
                    <p data-testid="listen-basis" className="text-[9px] text-slate-500 mt-1">
                      {listen.credit}{listen.environment ? ` · ${listen.environment} service` : ''} · {listen.assessed_basis}
                      {!wordsLight && ` · The words do not light: the publisher times ${listenVerse.words.length} word(s) and the text shown has ${shownWords.length}.`}
                    </p>
                  </>
                )}
              </div>
              {/* W640 — a SOURCED translation of the meanings, shown only when asked for, in its own block
                  under its own label: the translator, the year, the licence basis and the server's statement
                  that it is not the Qur'an all travel with the words. Never composed by a model. */}
              {!meaning && (
                <button type="button" onClick={showMeaning} disabled={busy === 'meaning'}
                  className="text-[9px] font-bold text-sky-400 hover:text-sky-300 mb-2 underline underline-offset-2">
                  {busy === 'meaning' ? 'Fetching…' : 'Show a translation of the meanings'}
                </button>
              )}
              {meaning && (
                <div data-testid="ayah-translation" className="mb-2 p-2 rounded-lg border border-sky-500/20 bg-sky-500/5">
                  <p className="text-[11px] text-slate-200 leading-relaxed">{meaning.translation_text}</p>
                  <p className="text-[9px] text-slate-500 mt-1">
                    {meaning.translator}, {meaning.work} ({meaning.first_published}) · {meaning.source} · edition {meaning.edition}
                  </p>
                  <p className="text-[9px] text-amber-400/90 mt-1">{meaning.label}</p>
                  <p className="text-[9px] text-slate-600 mt-1">{meaning.register_note}. Licence basis: {meaning.licence_basis}</p>
                </div>
              )}
              <p className="text-[9px] text-slate-600 mb-2">{reviewRef} · recall quality (0 = blackout, 5 = perfect):</p>
              <div className="flex gap-1.5 mb-2">
                {[0, 1, 2, 3, 4, 5].map(q => (
                  <button key={q} type="button" onClick={() => submitReview(q)} disabled={busy === 'review'}
                    className={`w-8 h-8 rounded-lg text-[11px] font-black border transition-colors ${q >= 3 ? 'border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10' : 'border-amber-500/30 text-amber-400 hover:bg-amber-500/10'}`}>{q}</button>
                ))}
              </div>
              {reviewResult && (
                <>
                {/* P3.9 — the SM-2 state a learner is entitled to see: the interval AND the e-factor it
                    was computed with, so the schedule is checkable rather than asserted. */}
                <p data-testid="hifz-efactor" className="text-[10px] text-slate-400 mb-1">
                  e-factor {typeof reviewResult.new_efactor === 'number' ? reviewResult.new_efactor : '—'}
                  {' '}· the SM-2 easiness this ayah now carries, which is what the interval is computed from
                </p>
                {/* P3.9 — AND THE BASIS, which is the one line that stops a review count reading as an
                    attainment. The route has always returned it; no screen showed it. */}
                {reviewResult.memorised_basis && (
                  <p data-testid="hifz-memorised-basis" className="text-[10px] text-amber-400 mb-2 leading-relaxed">
                    {typeof reviewResult.total_ayaat_memorised === 'number'
                      ? `${reviewResult.total_ayaat_memorised} ayah/ayaat counted: ` : ''}
                    {reviewResult.memorised_basis}
                  </p>
                )}
                <p className="text-[10px] text-emerald-400 mb-2">
                  <CheckCircle2 size={10} className="inline mr-1" />next review in {reviewResult.new_interval_days} day(s) ({reviewResult.next_review_date}){reviewResult.xp_awarded > 0 && ` · +${reviewResult.xp_awarded} XP`}
                </p>
                </>
              )}
              <div className="pt-2 border-t border-slate-900">
                <p className="text-[9px] font-black uppercase text-slate-500 mb-1">written recall check — TEXT only</p>
                <textarea value={recallText} onChange={e => setRecallText(e.target.value)} rows={2} dir="rtl"
                  className="w-full text-base font-arabic bg-slate-900 border border-slate-800 rounded-lg p-2 text-white mb-1.5"
                  placeholder="اكتب الآية من الذاكرة…" />
                <Button onClick={checkRecall} disabled={busy === 'recall' || !recallText.trim()} className="bg-slate-900 text-aura text-[10px]">
                  {busy === 'recall' ? <Loader2 size={11} className="animate-spin" /> : 'Compare with the authentic text'}
                </Button>
                {recall && (recall.comparable ? (
                  <div className="mt-2">
                    {/* W617 (FU-478) — the letters figure leads, and each figure says what it compares */}
                    <p className="text-[11px] text-white" data-testid="recall-letters">letters similarity {Math.round((recall.text_similarity ?? 0) * 100)}% <span className="text-[9px] text-slate-500">(diacritics and Uthmani marks not counted)</span></p>
                    {recall.exact_similarity != null && (
                      <p className="text-[9px] text-slate-500" title={recall.exact_similarity_basis} data-testid="recall-exact">with every mark counted: {Math.round(recall.exact_similarity * 100)}% — {recall.exact_similarity_basis}</p>
                    )}
                    {(recall.missing_rule_markers ?? []).map((m, i) => <p key={i} className="text-[9px] text-amber-400">{m}</p>)}
                    {recall.markers_basis && <p className="text-[8px] text-slate-600" data-testid="recall-markers-basis">{recall.markers_basis}</p>}
                    <p className="text-[8px] text-slate-600 italic mt-1">{recall.scope}</p>
                  </div>
                ) : <p className="text-[10px] text-amber-400 mt-2">{recall.reason}</p>)}
              </div>
            </div>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 @[960px]:grid-cols-2 gap-4">
        {/* ── Tajweed lesson outlines — provenance disclosed ── */}
        <Card className="p-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Sparkles size={14} /> Tajweed lesson plans — AI-assisted, labelled</h3>
          <div className="flex items-center gap-2 mb-2">
            <input value={rule} onChange={e => setRule(e.target.value)}
              className="flex-1 text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300" placeholder="rule, e.g. idgham, ikhfa, madd" />
            <Button onClick={runLesson} disabled={busy === 'lesson' || !rule.trim()} className="flex items-center gap-1.5 bg-aura text-sovereign text-[10px]">
              {busy === 'lesson' ? <Loader2 size={11} className="animate-spin" /> : <Sparkles size={11} />} Generate
            </Button>
          </div>
          {lesson && (
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <div className="flex gap-1.5 mb-1.5">
                <Chip tone={lesson.floor_served ? 'warn' : 'ok'}>served by {lesson.served_by}</Chip>
                {lesson.lesson_plan == null
                  ? <Chip tone="warn">withheld — not scholar-reviewed</Chip>
                  : lesson.floor_served && <Chip tone="warn">outline, not a lesson</Chip>}
              </div>
              {lesson.floor_note && <p className="text-[9px] text-amber-200/70 italic mb-1.5">{lesson.floor_note}</p>}
              {lesson.lesson_plan == null
                ? <p className="text-[11px] text-amber-200/80" data-testid="qep-lesson-withheld">{lesson.withheld_note || lesson.review_note || 'Withheld: this lesson has not been approved by a scholar.'}</p>
                : <p className="text-[11px] text-slate-300 whitespace-pre-wrap max-h-40 overflow-y-auto">{lesson.lesson_plan}</p>}
              <p className="text-[8px] text-slate-600 italic mt-1.5">{lesson.disclaimer}</p>
            </div>
          )}
        </Card>

        {/* ── Translation — refuses rather than fabricates ── */}
        <Card className="p-5">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 flex items-center gap-2"><Languages size={14} /> Educational translation — model-only</h3>
          {/* W444 — the COMPUTED availability, shown before anyone types sacred text into a box
              that will refuse; both this chip and the click-time 503 read the same model probe. */}
          <p className="mb-1">
            <Chip tone={trStatus == null ? 'dim' : trStatus.translation_available ? 'ok' : 'warn'}>
              {trStatus == null ? 'availability unknown'
                : trStatus.translation_available ? `available — ${trStatus.availability_basis || 'model discovered'}`
                : 'unavailable — the floor cannot translate; Translate will refuse'}
            </Chip>
          </p>
          <p className="text-[9px] text-slate-600 mb-2">{/* W631 (FU-546) */}Arabic / Qur'anic text is NOT translated here, by ruling, whatever model is available — a translation of the Qur'an's meanings comes only from a named, sourced edition, shown beside the verse in the review card above when you ask for it, never from this tool. This tool is for non-Arabic educational text, and even then only a model may translate; the floor refuses.{trStatus?.tajweed_note ? ` ${trStatus.tajweed_note}` : ''}</p>
          <textarea value={trText} onChange={e => setTrText(e.target.value)} rows={2}
            className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300 mb-2" placeholder="Non-Arabic educational text…" />
          <Button onClick={runTranslate} disabled={busy === 'translate' || !trText.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
            {busy === 'translate' ? <Loader2 size={11} className="animate-spin" /> : <Languages size={11} />} Translate to English
          </Button>
          {trRefusal && <p className="text-[10px] text-amber-400 mt-2">{trRefusal}</p>}
          {trResult && (
            <div className="mt-2 p-3 rounded-xl bg-slate-950 border border-slate-900">
              <Chip tone="ok">served by {trResult.served_by}</Chip>
              {/* W692 (A.12.3) — a model's translation is shown only when a scholar approved it; otherwise the
                  server's reason is shown, never an empty box under a "served by" chip */}
              {trResult.translation
                ? <p data-testid="qep-translation-text" className="text-[11px] text-slate-300 mt-1.5 whitespace-pre-wrap">{trResult.translation}</p>
                : <p data-testid="qep-translation-withheld" className="text-[11px] text-amber-200/80 mt-1.5">{trResult.withheld_note}</p>}
              <p className="text-[8px] text-slate-600 italic mt-1">{trResult.label}</p>
            </div>
          )}
        </Card>
      </div>

      {/* W684 — memorisation practice: the plan in three tracks, the hidden verse, similar verses side by side */}
      <HifzPractice uid={UID} />

      <p className="text-[9px] text-slate-600 flex items-center gap-2">
        <Trophy size={11} className="text-slate-700" />
        Recitation itself is never scored here — no phonetic model is provisioned, and a fabricated judgement about
        recitation of the Qur'an would be a false witness. Written-text tools only; verify all rules with a qualified teacher.
      </p>
    </div>
  );
};
