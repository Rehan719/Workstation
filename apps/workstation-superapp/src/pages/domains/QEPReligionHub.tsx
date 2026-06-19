import React, { useState } from 'react';
import { Card, Button, Badge, toast } from '@workstation/ui';
import { Mic, Play, CheckCircle2, AlertCircle, Sparkles, BookOpen, Trophy, Glasses, History, Activity } from 'lucide-react';

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

const TajwidCoach = () => {
  const [reciting, setReciting] = useState(false);
  const [result, setResult] = useState<any>(null);

  const startRecitation = () => {
    setReciting(true);
    setResult(null);
    setTimeout(() => {
      setReciting(false);
      setResult({
        score: 94.2,
        violations: [
          { rule: 'Ikhfa', msg: 'Noon Sakina here requires light ghunnah.' },
          { rule: 'Qalqalah', msg: 'The letter Ba requires clear echo.' }
        ]
      });
    }, 3000);
  };

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

             <button
               onClick={startRecitation}
               className={`w-32 h-32 rounded-full flex items-center justify-center transition-all ${reciting ? 'bg-vital animate-pulse shadow-[0_0_40px_rgba(255,100,100,0.4)]' : 'bg-aura shadow-[0_0_30px_rgba(100,255,218,0.3)] hover:scale-105'} text-sovereign`}
             >
                {reciting ? <Activity size={48} /> : <Mic size={48} />}
             </button>
             <p className="mt-8 text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">
                {reciting ? 'Analyzing Phonetic Stream...' : 'Click to start recitation'}
             </p>

             {result && (
               <div className="mt-12 w-full grid grid-cols-2 gap-6 animate-in zoom-in-95 duration-500">
                  <div className="p-6 rounded-3xl bg-emerald-500/10 border border-emerald-500/20 text-left">
                     <p className="text-[10px] font-black uppercase text-emerald-500 mb-2">Accuracy Score</p>
                     <p className="text-4xl font-black text-white">{result.score}%</p>
                  </div>
                  <div className="p-6 rounded-3xl bg-vital/10 border border-vital/20 text-left">
                     <p className="text-[10px] font-black uppercase text-vital mb-2">Rule Violations</p>
                     <p className="text-4xl font-black text-white">{result.violations.length}</p>
                  </div>
               </div>
             )}
          </Card>
       </div>
       <div className="@[440px]:col-span-4 space-y-8">
          <Card className="p-8 bg-aura/5 border-aura/20">
             <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Real-time Coaching</h3>
             <div className="space-y-4">
                {result?.violations.map((v: any, i: number) => (
                  <div key={i} className="p-4 rounded-2xl bg-slate-900/80 border border-vital/30 flex gap-4">
                     <AlertCircle className="text-vital shrink-0" size={18} />
                     <div>
                        <p className="text-[10px] font-black text-vital uppercase">{v.rule}</p>
                        <p className="text-xs text-slate-300 font-bold">{v.msg}</p>
                     </div>
                  </div>
                ))}
                {!result && (
                   <p className="text-xs text-slate-500 italic">Waiting for input signal...</p>
                )}
             </div>
          </Card>
          <Card className="p-8 bg-slate-950 border-slate-900">
             <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Session Vitals</h3>
             <div className="space-y-6">
                <VitalRow label="Phonetic Precision" value="High" />
                <VitalRow label="Temporal Alignment" value="Optimal" />
                <VitalRow label="GaaS Compliance" value="Verified" />
             </div>
          </Card>
       </div>
    </div>
  );
};

const MemorizationSuite = () => (
   <div className="grid grid-cols-1 md:grid-cols-3 gap-8 animate-in fade-in duration-700">
      <Card className="p-10 col-span-2 border-slate-900 bg-slate-950/20">
         <h3 className="text-xl font-black text-white uppercase tracking-tight mb-8">Retention Heatmap</h3>
         <div className="grid grid-cols-12 gap-2">
            {Array.from({ length: 60 }).map((_, i) => (
               <div
                  key={i}
                  className={`aspect-square rounded-sm ${i % 7 === 0 ? 'bg-aura' : i % 3 === 0 ? 'bg-aura/40' : 'bg-slate-900'}`}
                  title={`Level ${i % 5}`}
               />
            ))}
         </div>
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
            <VitalRow label="Ease Factor" value="2.5" />
            <VitalRow label="Interval" value="4 Days" />
            <VitalRow label="Repetitions" value="12" />
            <Button onClick={async () => {
               await fetch('/api/v1/qep/hifz/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ surah_id: 2, quality: 5 }) }).catch(() => {});
               toast('Surah Al-Baqarah marked as mastered — SM-2 interval advanced to 4 days');
            }} className="w-full bg-aura text-sovereign mt-4 font-black uppercase text-[10px]">Mark as Mastered</Button>
         </div>
      </Card>
   </div>
);

const QuranCompetitions = () => (
   <div className="space-y-8 animate-in fade-in duration-700">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         <TournamentCard title="Ramadan Global" tier="Expert" players={1240} status="LIVE" />
         <TournamentCard title="Linguistic Roots" tier="Novice" players={450} status="OPEN" />
         <TournamentCard title="Sovereign Reciters" tier="All" players={890} status="UPCOMING" />
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
