import React, { useState } from 'react';
import { Card, Button, Badge, toast } from '@workstation/ui';
import { Mic, MicOff, Play, CheckCircle2, AlertCircle, Sparkles, BookOpen, Trophy, Glasses, History, Activity } from 'lucide-react';

export const QEPReligionHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState('coach');

  return (
    <div className="space-y-10 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">QEP <span className="text-aura">Religion</span></h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Quran Education Platform • Advanced AI Flagship • v1.0</p>
        </div>
        <div className="flex gap-2 p-1 rounded-2xl bg-slate-900 border border-slate-800 flex-wrap shrink-0">
           {[
             { id: 'coach', label: 'AI Coach', icon: Mic },
             { id: 'mem', label: 'Memorization', icon: BookOpen },
             { id: 'comp', label: 'Competitions', icon: Trophy },
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
      {activeTab === 'comp' && <QuranCompetitions />}
      {activeTab === 'lab' && <ARVRLab />}
    </div>
  );
};

// W403 — this reported a recitation score of 94.2% and two named tajwid violations (Ikhfa,
// Qalqalah) after a three-second setTimeout. It never recorded audio and never called anything:
// the score and the "errors" were literals. It told a user their recitation of the Qur'an was
// assessed, and named mistakes they did not make.
//
// The backend is no better — qep_flagship.tajwid_coach() ignores its audio argument and returns
// 0.98 + random()*0.015 — so there is no assessment capability anywhere to wire this to.
//
// Assessing recitation needs a phonetic/audio model that is not provisioned. Precedent is already
// set in this repo (W148: image input was left unbuilt because the native floor has no vision
// model, rather than faking analysis). The same applies here, and it matters more: a fabricated
// judgement about someone's recitation of scripture is not a placeholder, it is a false witness.
const TajwidCoach = () => {
  return (
    <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
       <div className="@[440px]:col-span-8">
          <Card className="p-12 border-slate-900 bg-slate-950/20 relative min-h-[500px] flex flex-col items-center justify-center text-center">
             <div className="absolute top-10 left-10 flex items-center gap-4">
                <Badge color="aura">Al-Baqarah: 1-5</Badge>
                <Badge color="slate-800">Hafs 'an 'Asim</Badge>
             </div>

             <div className="mb-12">
                <p className="text-4xl font-bold text-white mb-4 leading-loose font-arabic" dir="rtl">
                   بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
                </p>
                <p className="text-slate-500 italic">In the name of Allah, the Most Gracious, the Most Merciful.</p>
             </div>

             <div className="w-32 h-32 rounded-full flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-600">
                <MicOff size={44} />
             </div>
             <p className="mt-8 text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">
                Recitation assessment unavailable
             </p>
             <p className="mt-4 max-w-md text-xs text-slate-500 font-semibold leading-relaxed">
                Assessing tajwid requires a phonetic model that is not provisioned on this
                deployment. Rather than show a score nothing measured, this reports nothing. The
                verse and riwayah above are real; no judgement is made about your recitation.
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
          </Card>
       </div>
    </div>
  );
};

const MemorizationSuite = () => (
   <div className="grid grid-cols-1 md:grid-cols-3 gap-8 animate-in fade-in duration-700">
      <Card className="p-10 col-span-2 border-slate-900 bg-slate-950/20">
         <h3 className="text-xl font-black text-white uppercase tracking-tight mb-8">Retention Heatmap</h3>
         {/* W412 — this drew 60 cells coloured from the LOOP INDEX (i % 7, i % 3) with titles
             reading "Level {i % 5}". It is a picture of the modulo operator presented as a
             retention history: it looked identical for every user, on every visit, forever, and
             nobody had a retention record behind it. */}
         <p className="text-xs text-slate-500 font-semibold leading-relaxed">
            No retention history is recorded for this user yet. Review ayat with the SM-2 scheduler
            below and the heatmap will show real intervals once there is something to show.
         </p>
         <div className="mt-8 flex justify-between items-center text-[9px] font-black uppercase text-slate-500">
            <span>Last 60 Days Intensity</span>
            <div className="flex gap-1">
               <span>Less</span>
               <div className="w-2 h-2 bg-slate-900 rounded-sm" />
               <div className="w-2 h-2 bg-aura/20 rounded-sm" />
               <div className="w-2 h-2 bg-aura/60 rounded-sm" />
               <div className="w-2 h-2 bg-aura rounded-sm" />
               <span>More</span>
            </div>
         </div>
      </Card>
      <Card className="p-10 bg-aura/5 border-aura/20">
         <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">SM-2 Algorithm</h3>
         <div className="space-y-6">
            <VitalRow label="Ease Factor" value="2.5 (SM-2 default)" />
            <VitalRow label="Interval" value="4 Days" />
            <VitalRow label="Repetitions" value="— (no history yet)" />
            {/* W339/W329 — the REAL SM-2 review endpoint; success claimed only from the server's
                actual computed interval, failure surfaced honestly. (The old code posted to a
                nonexistent path and toasted a fabricated success regardless.) */}
            <Button onClick={async () => {
               try {
                  const r = await fetch('/api/v1/qep/hifz/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ uid: 'local', ayah_ref: '2:255', quality: 5 }) });
                  if (r.ok) {
                     const d = await r.json();
                     toast(`Review recorded — SM-2 next interval: ${d?.new_interval_days ?? '?'} day(s), next review ${d?.next_review_date ?? '?'}`);
                  } else {
                     toast(`Could not record the review (HTTP ${r.status}) — nothing was saved`);
                  }
               } catch {
                  toast('Backend unreachable — nothing was saved');
               }
            }} className="w-full bg-aura text-sovereign mt-4 font-black uppercase text-[10px]">Mark as Mastered</Button>
         </div>
      </Card>
   </div>
);

const QuranCompetitions = () => (
   <div className="space-y-8 animate-in fade-in duration-700">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         {/* W329/W339 — honest: illustrative previews; no real tournament backend exists yet */}
         <TournamentCard title="Ramadan Global (preview)" tier="Expert" players={0} status="PLANNED" />
         <TournamentCard title="Linguistic Roots (preview)" tier="Novice" players={0} status="PLANNED" />
         <TournamentCard title="Sovereign Reciters (preview)" tier="All" players={0} status="PLANNED" />
      </div>
   </div>
);

const ARVRLab = () => (
   <Card className="p-20 border-dashed border-2 border-slate-800 bg-slate-950/40 text-center space-y-8 animate-in zoom-in-95 duration-700">
      <div className="w-24 h-24 rounded-3xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura mx-auto">
         <Glasses size={48} />
      </div>
      <div>
         <h3 className="text-2xl font-black text-white uppercase tracking-tighter italic">Immersive Lab Ready</h3>
         <p className="text-slate-500 font-bold max-w-md mx-auto mt-2">
            Initialize Three.js articulation overlays or A-Frame virtual mosque environments.
         </p>
      </div>
      <div className="flex gap-4 justify-center">
         <Button onClick={() => toast('AR Mouth Model requires a WebXR-compatible device — coming in Phase 4')} variant="outline" className="border-slate-800">Launch AR Mouth Model</Button>
         <Button onClick={() => toast('VR Mosque requires a WebXR headset — coming in Phase 4')} className="bg-white text-sovereign">Enter VR Mosque</Button>
      </div>
   </Card>
);

const VitalRow = ({ label, value }: any) => (
  <div className="flex justify-between items-center text-[10px] font-black uppercase">
     <span className="text-slate-500 tracking-widest">{label}</span>
     <span className="text-white tracking-widest">{value}</span>
  </div>
);

const TournamentCard = ({ title, tier, players, status }: any) => (
  <Card className="p-8 border-slate-900 bg-slate-950/40 group hover:border-aura/30 transition-all">
     <div className="flex justify-between items-start mb-6">
        <Badge color={status === 'LIVE' ? 'vital' : status === 'OPEN' ? 'aura' : 'slate-800'}>{status}</Badge>
        <Trophy size={20} className="text-slate-700 group-hover:text-aura transition-colors" />
     </div>
     <h4 className="text-xl font-black text-white uppercase tracking-tight mb-2">{title}</h4>
     <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{tier} • {players} Participants</p>
     <Button onClick={() => toast('Global leaderboard launching with QEP Season 2')} variant="outline" className="w-full mt-8 text-[9px] uppercase font-black">View Leaderboard</Button>
  </Card>
);
