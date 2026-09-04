import React, { useEffect, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { BookOpen, Brain, Loader2, Sparkles, Trophy, Languages, CheckCircle2 } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';

// W439 — the REAL Quran Education Platform surface (Owner directive: QEP lives in the Religion
// domain). Every capability here is a wired backend route that was AUDITED before wiring:
// authentic Qur'an text (alquran.cloud — never AI-generated, per the constitution), real SM-2
// hifz scheduling, a written-recall check that says NOTHING about pronunciation, AI lesson
// outlines with serving provenance (floor-served output is labelled an outline, not a lesson),
// translation that REFUSES when only the deterministic floor is available, and gamification from
// a persisted award store (the old surface claimed "recorded" while persisting nothing).

interface Surah { number: number; name_arabic: string; name_transliteration: string; name_english: string; ayah_count: number; revelation_type: string }
interface Ayah { number_in_surah: number; text_arabic: string }
interface HifzProgress { total_ayaat_in_schedule: number; total_ayaat_memorised: number; due_today: number; due_refs: string[]; total_sessions: number }
interface GamiState { xp: number; level: number; level_basis: string; achievements: string[]; streak_days: number; streak_basis: string; awards_recorded: number; scope: string }
interface Recall { comparable: boolean; reason?: string; text_similarity?: number; similarity_basis?: string; missing_rule_markers?: string[]; markers_basis?: string; scope?: string }

const UID = 'local';

function Chip({ tone, children, title }: { tone: 'ok' | 'warn' | 'dim'; children: React.ReactNode; title?: string }) {
  const cls = tone === 'ok' ? 'bg-emerald-500/15 text-emerald-400' : tone === 'warn' ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400';
  return <span title={title} className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${cls}`}>{children}</span>;
}

export const QEPStudio: React.FC = () => {
  const [suwar, setSuwar] = useState<Surah[] | null>(null);
  const [surahNo, setSurahNo] = useState(1);
  const [ayaat, setAyaat] = useState<Ayah[] | null>(null);
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
    setBusy('surah'); setErr(''); setAyaat(null);
    try {
      const d = await apiJson(`/api/v1/qep/surah/${n}`);
      setAyaat(d.ayaat || []);
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
  const [reviewAyah, setReviewAyah] = useState<{ text_arabic: string; surah_name: string } | null>(null);
  const [reviewResult, setReviewResult] = useState<{ new_interval_days: number; next_review_date: string; xp_awarded: number } | null>(null);
  const openReview = async (ref: string) => {
    setReviewRef(ref); setReviewAyah(null); setReviewResult(null); setRecall(null); setRecallText('');
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
      const d = await apiJson('/api/v1/qep/tajweed/analyse', { method: 'POST', body: { ayah_text: reviewAyah.text_arabic, recited_text: recallText } });
      setRecall(d.comparison);
    } catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── lesson plans (provenance disclosed) ──
  const [rule, setRule] = useState('idgham');
  const [lesson, setLesson] = useState<{ lesson_plan: string; served_by: string; floor_served: boolean; floor_note?: string; disclaimer: string } | null>(null);
  const runLesson = async () => {
    setBusy('lesson'); setErr(''); setLesson(null);
    try { setLesson(await apiJson('/api/v1/qep/tajweed/lesson', { method: 'POST', body: { rule_name: rule } })); }
    catch (e) { setErr(errorMessage(e)); }
    setBusy('');
  };

  // ── translation (refuses honestly on floor-only) ──
  const [trText, setTrText] = useState('');
  const [trResult, setTrResult] = useState<{ translation: string; served_by: string; label: string } | null>(null);
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
          <Chip tone={gami.streak_days > 0 ? 'ok' : 'dim'} title={gami.streak_basis}>streak {gami.streak_days}d</Chip>
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
            <div className="max-h-64 overflow-y-auto p-3 rounded-xl bg-slate-950 border border-slate-900 mb-3">
              {ayaat.map(a => (
                <p key={a.number_in_surah} className="text-lg text-white leading-loose font-arabic mb-2" dir="rtl">
                  {a.text_arabic} <span className="text-[10px] text-aura">({a.number_in_surah})</span>
                </p>
              ))}
            </div>
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
              <p className="text-xl text-white leading-loose font-arabic mb-2" dir="rtl">{reviewAyah.text_arabic}</p>
              <p className="text-[9px] text-slate-600 mb-2">{reviewRef} · recall quality (0 = blackout, 5 = perfect):</p>
              <div className="flex gap-1.5 mb-2">
                {[0, 1, 2, 3, 4, 5].map(q => (
                  <button key={q} type="button" onClick={() => submitReview(q)} disabled={busy === 'review'}
                    className={`w-8 h-8 rounded-lg text-[11px] font-black border transition-colors ${q >= 3 ? 'border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10' : 'border-amber-500/30 text-amber-400 hover:bg-amber-500/10'}`}>{q}</button>
                ))}
              </div>
              {reviewResult && (
                <p className="text-[10px] text-emerald-400 mb-2">
                  <CheckCircle2 size={10} className="inline mr-1" />next review in {reviewResult.new_interval_days} day(s) ({reviewResult.next_review_date}){reviewResult.xp_awarded > 0 && ` · +${reviewResult.xp_awarded} XP`}
                </p>
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
                    <p className="text-[11px] text-white">written similarity {Math.round((recall.text_similarity ?? 0) * 100)}% <span className="text-[9px] text-slate-600" title={recall.similarity_basis}>(normalised Levenshtein)</span></p>
                    {(recall.missing_rule_markers ?? []).map((m, i) => <p key={i} className="text-[9px] text-amber-400">{m}</p>)}
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
                {lesson.floor_served && <Chip tone="warn">outline, not a lesson</Chip>}
              </div>
              {lesson.floor_note && <p className="text-[9px] text-amber-200/70 italic mb-1.5">{lesson.floor_note}</p>}
              <p className="text-[11px] text-slate-300 whitespace-pre-wrap max-h-40 overflow-y-auto">{lesson.lesson_plan}</p>
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
          <p className="text-[9px] text-slate-600 mb-2">A translation must come from a model. When only the deterministic floor is available, this REFUSES — the floor's output will never be presented as a translation of sacred text.{trStatus?.tajweed_note ? ` ${trStatus.tajweed_note}` : ''}</p>
          <textarea value={trText} onChange={e => setTrText(e.target.value)} rows={2}
            className="w-full text-[11px] bg-slate-950 border border-slate-900 rounded-lg p-2 text-slate-300 mb-2" placeholder="Arabic educational text…" />
          <Button onClick={runTranslate} disabled={busy === 'translate' || !trText.trim()} className="flex items-center gap-1.5 bg-slate-900 text-aura text-[10px]">
            {busy === 'translate' ? <Loader2 size={11} className="animate-spin" /> : <Languages size={11} />} Translate to English
          </Button>
          {trRefusal && <p className="text-[10px] text-amber-400 mt-2">{trRefusal}</p>}
          {trResult && (
            <div className="mt-2 p-3 rounded-xl bg-slate-950 border border-slate-900">
              <Chip tone="ok">served by {trResult.served_by}</Chip>
              <p className="text-[11px] text-slate-300 mt-1.5 whitespace-pre-wrap">{trResult.translation}</p>
              <p className="text-[8px] text-slate-600 italic mt-1">{trResult.label}</p>
            </div>
          )}
        </Card>
      </div>

      <p className="text-[9px] text-slate-600 flex items-center gap-2">
        <Trophy size={11} className="text-slate-700" />
        Recitation itself is never scored here — no phonetic model is provisioned, and a fabricated judgement about
        recitation of the Qur'an would be a false witness. Written-text tools only; verify all rules with a qualified teacher.
      </p>
    </div>
  );
};
