import React from 'react';

interface HifzProgressProps {
  juzMemorized: number;
}

const HifzProgress: React.FC<HifzProgressProps> = ({ juzMemorized }) => {
  const totalJuz = 30;
  const percentage = (juzMemorized / totalJuz) * 100;

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Hifz Tracker</h3>
        <span className="text-xs font-black text-aura">{juzMemorized}/{totalJuz} Juz</span>
      </div>
      <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-aura to-sovereign transition-all duration-1000"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="mt-4 text-[9px] font-bold text-slate-600 uppercase tracking-widest text-center">
        Next milestone: Juz {juzMemorized + 1}
      </p>
    </div>
  );
};

export default HifzProgress;
