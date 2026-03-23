import React from 'react';
import { useStore } from '@workstation/shared';

export const RealmSelector = () => {
  const { currentRealm, setCurrentRealm } = useStore();

  const realms = ['UNIFIED', 'LEARNER', 'DEVELOPER', 'ENTERPRISE', 'SCHOLAR'] as const;

  return (
    <div className="flex gap-4 p-2 rounded-2xl bg-slate-950/80 border border-slate-900 w-fit backdrop-blur-xl">
      {realms.map((realm) => (
        <button
          key={realm}
          onClick={() => setCurrentRealm(realm)}
          className={`px-5 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
            currentRealm === realm
              ? 'bg-aura text-sovereign shadow-xl shadow-aura/20'
              : 'text-slate-500 hover:text-slate-300 hover:bg-slate-900'
          }`}
        >
          {realm}
        </button>
      ))}
    </div>
  );
};
