import React from 'react';

interface TajweedMeterProps {
  score: number;
}

const TajweedMeter: React.FC<TajweedMeterProps> = ({ score }) => {
  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Tajweed Accuracy</h3>
        <span className="text-xs font-black text-emerald-500">{score}%</span>
      </div>
      <div className="flex items-center gap-1">
        {Array.from({ length: 10 }).map((_, idx) => (
          <div
            key={idx}
            className={`h-6 flex-1 rounded-sm transition-all duration-500 ${
              idx < score / 10 ? 'bg-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-slate-800'
            }`}
          />
        ))}
      </div>
      <p className="mt-4 text-[9px] font-bold text-slate-600 uppercase tracking-widest text-center">
        Excellent. Focus on Madd rules next.
      </p>
    </div>
  );
};

export default TajweedMeter;
