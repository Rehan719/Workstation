import React, { useEffect, useState } from 'react';
import { Card, Button, Badge, toast } from '@workstation/ui';
import { apiJson, errorMessage } from '../../lib/api';
import { QEPStudio } from '../../components/QEPStudio';
import { Mic, MicOff, Play, CheckCircle2, AlertCircle, Sparkles, BookOpen, Trophy, Glasses, History, Activity, Brain } from 'lucide-react';
import QEPIntelligence from '../../components/qep/QEPIntelligence';
import QepDonorStatement from '../../components/QepDonorStatement';

export const QEPReligionHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState('coach');

  return (
    <div className="space-y-10 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">QEP <span className="text-aura">Religion</span></h1>
          {/* W625 (FU-538, M2 v9 R5.5) — "Advanced AI Flagship • v1.0" headed a hub where most of A.6's fifteen features are
              absent, and the hub never said so. The header now says what stage it is at and where the state of each is. */}
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]" data-testid="qep-hub-stage">Quran Education Platform • in development — a few features live; the roadmap states each one's state</p>
        </div>
        <div className="flex gap-2 p-1 rounded-2xl bg-slate-900 border border-slate-800 flex-wrap shrink-0">
           {[
             { id: 'coach', label: 'AI Coach', icon: Mic },
             { id: 'mem', label: 'Memorization', icon: BookOpen },
             { id: 'comp', label: 'Competitions', icon: Trophy },
             // W444 — the intelligence layer (XAI/adaptation/compliance) had no surface
             { id: 'intel', label: 'Intelligence', icon: Brain },
             { id: 'lab', label: 'AR/VR Lab', icon: Glasses }
           ].map(t => (
             <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`flex items-center gap-3 px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === t.id ? 'bg-aura text-sovereign' : 'text-slate-500 hover:text-white'}`}
             >
                <t.icon size={16} />
                {t.label}
             </button>
           ))}
        </div>
      </header>

      {activeTab === 'coach' && <TajwidCoach />}
      {activeTab === 'mem' && <MemorizationSuite />}
      {activeTab === 'intel' && <QEPIntelligence />}
      {activeTab === 'comp' && <QuranCompetitions />}
      {activeTab === 'lab' && <ARVRLab />}
      {/* FU-467 — A.8's transparent donor view, on every tab */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
        <QepDonorStatement />
      </div>
    </div>
  );
};

// W403 — this reported a recitation score of 94.2% and two named tajwid violations (Ikhfa,
// Qalqalah) after a three-second setTimeout. It never recorded audio and never called anything:
// the score and the "errors" were literals. It told a user their recitation of the Qur'an was
// assessed, and named mistakes they did not make.
//
// The backend HAS since been fixed (qep_flagship.tajwid_coach now honestly returns
// status UNAVAILABLE with score None) — the capability itself still does not exist.
//
// Assessing recitation needs a phonetic/audio model that is not provisioned. Precedent is already
// set in this repo (W148: image input was left unbuilt because the native floor has no vision
// model, rather than faking analysis). The same applies here, and it matters more: a fabricated
// judgement about someone's recitation of scripture is not a placeholder, it is a false witness.
// W572 (MILESTONE M1 · R5.3) — THE AYAH WAS A LITERAL IN THIS FILE, UNDER A REFERENCE THAT WAS NOT
// ITS OWN. The panel hard-coded the Basmala and badged it with a surah-and-ayah RANGE whose text
// under Hafs is something else, with no source on the panel and no retrieval call anywhere in the
// file. The prose below then vouched for the pairing, so the page asserted the correctness of its own
// mislabelling — scripture under a citation that does not match it, on the one surface where the
// constitution is strictest. (The exact wording of both is in W572's commit message, not here: a
// comment that quotes the string its own guard forbids is the guard's first false positive.)
//
// THE PLATFORM ALREADY HELD THE HONEST PATH: GET /api/v1/qep/ayah/{s}/{a} serves alquran.cloud with
// provenance and separates a prepended Basmala with a stated basis (W483). This panel is now a
// CONSUMER of it, and EVERY LABEL IS DERIVED FROM THE RESPONSE — the surah name, the ref and the
// source are the ones the source returned, never a literal that can drift away from the text beside
// it, which is exactly how this defect was possible. No Arabic is stored in this file any more.
//
// AND THERE IS DELIBERATELY NO FALLBACK COPY. If the retrieval fails, the panel shows no scripture
// and says why. A verse under the wrong reference is worse than no verse.
const COACH_AYAH = { surah: 2, ayah: 1 };   // WHICH ayah is displayed; its LABEL comes from the response

interface SourcedAyah {
  ref: string;
  text_arabic: string;
  surah_name: string;
  source: string;
  basmala?: string;
  basmala_separated?: boolean | null;
  basmala_basis?: string | null;
}

const TajwidCoach = () => {
  const [ayah, setAyah] = useState<SourcedAyah | null>(null);
  const [ayahErr, setAyahErr] = useState('');

  useEffect(() => {
    let live = true;
    apiJson<SourcedAyah>(`/api/v1/qep/ayah/${COACH_AYAH.surah}/${COACH_AYAH.ayah}`)
      .then(d => { if (live) setAyah(d); })
      .catch((e: unknown) => { if (live) setAyahErr(errorMessage(e)); });
    return () => { live = false; };
  }, []);

  return (
    <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
       <div className="@[440px]:col-span-8">
          <Card className="p-12 border-slate-900 bg-slate-950/20 relative min-h-[500px] flex flex-col items-center justify-center text-center">
             <div className="absolute top-10 left-10 flex items-center gap-4">
                {/* The reference is the one the SOURCE returned for the text below it. The old pair
                    was two literals: a surah-ayah range the text was not, and a riwayah nothing in
                    the response states. */}
                {ayah ? (
                  <>
                    {/* The ref leads because it is unambiguous; the name is the SOURCE's own, which
                        is Arabic, so it carries its own direction. It is omitted when the response
                        has none rather than left as a dangling separator implying a missing word. */}
                    <Badge color="aura">
                      {ayah.ref}
                      {ayah.surah_name ? <> · <span dir="rtl" className="font-arabic">{ayah.surah_name}</span></> : null}
                    </Badge>
                    <Badge color="slate-800">{ayah.source}</Badge>
                  </>
                ) : (
                  <Badge color="slate-800">{ayahErr ? 'verse unavailable' : 'retrieving verse…'}</Badge>
                )}
             </div>

             <div className="mb-12">
                {ayah ? (
                  <>
                    {/* Where this edition PREPENDS the Basmala to ayah 1, the route returns it
                        separately with the basis on which it was separated (W483). It is shown as
                        what it is, above the ayah, rather than silently inside it. */}
                    {ayah.basmala && ayah.basmala_separated && (
                      <p className="text-2xl font-bold text-slate-400 mb-6 leading-loose font-arabic" dir="rtl"
                         title={ayah.basmala_basis || undefined}>
                         {ayah.basmala}
                      </p>
                    )}
                    <p className="text-4xl font-bold text-white mb-4 leading-loose font-arabic" dir="rtl">
                       {ayah.text_arabic}
                    </p>
                    {ayah.basmala_separated && ayah.basmala_basis && (
                      <p className="mx-auto max-w-md text-[10px] text-slate-500 font-semibold leading-relaxed">
                         {ayah.basmala_basis}
                      </p>
                    )}
                  </>
                ) : (
                  <p className="max-w-md text-xs text-slate-500 font-semibold leading-relaxed">
                     {ayahErr
                       ? `No verse is shown: the sourced text could not be retrieved \u2014 ${ayahErr}`
                       : 'Retrieving the verse from its source\u2026'}
                  </p>
                )}
             </div>

             <div className="w-32 h-32 rounded-full flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-600">
                <MicOff size={44} />
             </div>
             <p className="mt-8 text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">
                Recitation assessment unavailable
             </p>
             <p className="mt-4 max-w-md text-xs text-slate-500 font-semibold leading-relaxed">
                Assessing tajwid requires a phonetic model that is not provisioned on this
                deployment. Rather than show a score nothing measured, this reports nothing.
                {ayah
                  ? ` The text above was retrieved from ${ayah.source} at ${ayah.ref}: it is not stored in this page and is never generated.`
                  : ' This page keeps no copy of the Qur\u2019an to fall back on, so when the source cannot be reached it shows no verse at all.'}
                {' '}No judgement is made about your recitation.
             </p>
          </Card>
       </div>
       <div className="@[440px]:col-span-4 space-y-8">
          <Card className="p-8 bg-slate-950 border-slate-900">
             <h3 className="text-sm font-black text-white uppercase tracking-widest mb-4">Coaching</h3>
             <p className="text-xs text-slate-500 font-semibold leading-relaxed">
                Per-rule coaching (Ikhfa, Qalqalah, Ghunnah and the rest) is produced from a real
                assessment of recorded audio. With no phonetic model provisioned there is nothing
                to coach from, so nothing is shown. Previously this panel listed specific rule
                violations that were written into the page as literals.
             </p>
             <p className="text-xs text-aura font-semibold leading-relaxed mt-4">
                What IS live (W439): written-text tools in the Memorization tab — a written-recall
                check against the authentic text, and AI-assisted lesson outlines with their
                serving provenance labelled. Neither claims anything about your recitation.
             </p>
          </Card>
       </div>
    </div>
  );
};

const MemorizationSuite = () => (
   // W439 — the empty-state suite below became the REAL wired studio: authentic Qur'an text,
   // SM-2 scheduling + reviews, written-recall, provenance-labelled lessons, persisted awards.
   <div className="animate-in fade-in duration-700"><QEPStudio /></div>
);

const QuranCompetitions = () => (
   <div className="space-y-8 animate-in fade-in duration-700">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         {/* W329/W339 — honest: illustrative previews; no tournament backend exists yet.
             W613 (FU-499, M1 v8 R5.0) — "Sovereign Reciters" was a RECITATION tournament marked PLANNED, and
             Appendix A.9.1 rules that recitation is never scored, so it is not planned: it is refused. */}
         <TournamentCard title="Ramadan Global (preview)" tier="Expert" players={0} status="PLANNED" />
         <TournamentCard title="Linguistic Roots (preview)" tier="Novice" players={0} status="PLANNED" />
         <TournamentCard title="Recitation contests" tier="Not offered" players={0} status="REFUSED (A.9.1)" />
      </div>
   </div>
);

const ARVRLab = () => (
   <Card className="p-20 border-dashed border-2 border-slate-800 bg-slate-950/40 text-center space-y-8 animate-in zoom-in-95 duration-700">
      <div className="w-24 h-24 rounded-3xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura mx-auto">
         <Glasses size={48} />
      </div>
      <div>
         <h3 className="text-2xl font-black text-white uppercase tracking-tighter italic">Immersive Lab — planned (Phase 4)</h3>
         <p className="text-slate-500 font-bold max-w-md mx-auto mt-2">
            AR articulation overlays and VR environments are planned; no WebXR code exists yet,
            so nothing here claims readiness.
         </p>
      </div>
      <div className="flex gap-4 justify-center">
         <Button onClick={() => toast('No WebXR code exists yet - this is not blocked by your device')} variant="outline" className="border-slate-800">Launch AR Mouth Model</Button>
         <Button onClick={() => toast('No WebXR code exists yet - this is not blocked by your headset')} className="bg-white text-sovereign">Enter VR Mosque</Button>
      </div>
   </Card>
);

const TournamentCard = ({ title, tier, players, status }: any) => (
  <Card className="p-8 border-slate-900 bg-slate-950/40 group hover:border-aura/30 transition-all">
     <div className="flex justify-between items-start mb-6">
        <Badge color={status === 'LIVE' ? 'vital' : status === 'OPEN' ? 'aura' : 'slate-800'}>{status}</Badge>
        <Trophy size={20} className="text-slate-700 group-hover:text-aura transition-colors" />
     </div>
     <h4 className="text-xl font-black text-white uppercase tracking-tight mb-2">{title}</h4>
     <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{tier} • {players} Participants</p>
     <Button onClick={() => toast(status === 'PLANNED' ? 'No tournament exists yet - this card is a preview, not a fixture. The live XP leaderboard is on the Memorization tab.' : 'Recitation is never scored (Appendix A.9.1), so no recitation contest is run or ranked. The live XP leaderboard is on the Memorization tab.')} variant="outline" className="w-full mt-8 text-[9px] uppercase font-black">View Leaderboard</Button>
  </Card>
);
