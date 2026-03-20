import React from 'react';
import { useStore } from '@workstation/shared';

export const CommandCenter = () => {
  const { currentRealm, systemVitals } = useStore();

  const channels = [
    { id: 'avatar', name: 'Avatar', icon: '👤', description: 'Real-time interaction' },
    { id: 'notification', name: 'Notification', icon: '🔔', description: 'System alerts' },
    { id: 'signal', name: 'Signal', icon: '📶', description: 'Agent pheromones' },
    { id: 'summary', name: 'Summary', icon: '📝', description: 'AI reports' },
    { id: 'dashboard', name: 'Dashboard', icon: '📊', description: 'Live metrics' },
    { id: 'predictive', name: 'Predictive', icon: '🔮', description: 'Forecasts' },
    { id: 'ethical', name: 'Ethical', icon: '⚖️', description: 'Constitutional AI' },
  ];

  return (
    <div className="fixed left-6 top-1/2 -translate-y-1/2 flex flex-col gap-4 z-50">
      <div className="p-4 rounded-3xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl flex flex-col gap-6 shadow-2xl">
        {channels.map((channel) => (
          <div
            key={channel.id}
            className="w-12 h-12 rounded-xl bg-slate-800/50 flex items-center justify-center cursor-pointer hover:bg-aura/20 hover:scale-110 transition-all group relative"
            title={channel.name}
          >
            <span className="text-xl">{channel.icon}</span>
            <div className="absolute left-16 px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none text-xs text-slate-300">
              {channel.name}: {channel.description}
            </div>
          </div>
        ))}

        <div className="h-px bg-slate-800 my-2" />

        <div className="flex flex-col gap-2 items-center">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest vertical-rl">Live</span>
        </div>
      </div>
    </div>
  );
};

export const RealmSelector = () => {
  const { currentRealm, setCurrentRealm } = useStore();

  const realms = ['UNIFIED', 'LEARNER', 'DEVELOPER', 'ENTERPRISE', 'SCHOLAR'] as const;

  return (
    <div className="flex gap-4 p-2 rounded-2xl bg-slate-900/50 border border-slate-800 w-fit">
      {realms.map((realm) => (
        <button
          key={realm}
          onClick={() => setCurrentRealm(realm)}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            currentRealm === realm
              ? 'bg-aura text-sovereign shadow-lg'
              : 'text-slate-500 hover:text-slate-300 hover:bg-slate-800/50'
          }`}
        >
          {realm}
        </button>
      ))}
    </div>
  );
};
