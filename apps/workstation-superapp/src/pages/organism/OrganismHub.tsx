import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Activity, HeartPulse, Network } from 'lucide-react';
import { OrganismDashboard } from './OrganismDashboard';
import { HeartbeatMonitor } from './HeartbeatMonitor';
import { CognitionIntegration } from '../CognitionIntegration';

// Consolidated Organism hub (§8 biomimetic living organism) — folds the former standalone
// Organism · Heartbeat · Cognition pages into one tabbed surface (deep-linkable via ?tab=).
const TABS = [
  { id: 'overview',  name: 'Organism',  icon: Activity,   El: OrganismDashboard },
  { id: 'heartbeat', name: 'Heartbeat', icon: HeartPulse, El: HeartbeatMonitor },
  { id: 'cognition', name: 'Cognition', icon: Network,    El: CognitionIntegration },
] as const;

export const OrganismHub: React.FC = () => {
  const [sp, setSp] = useSearchParams();
  const requested = sp.get('tab');
  const active = TABS.some(t => t.id === requested) ? requested! : 'overview';
  const Active = (TABS.find(t => t.id === active) ?? TABS[0]).El;

  return (
    <div className="space-y-6 pb-16">
      <div className="flex items-center gap-2 flex-wrap border-b border-slate-900 pb-3">
        {TABS.map(t => (
          <button
            key={t.id}
            type="button"
            onClick={() => setSp(t.id === 'overview' ? {} : { tab: t.id }, { replace: true })}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-[11px] font-black uppercase tracking-widest transition-all ${
              active === t.id ? 'bg-aura text-sovereign shadow-lg shadow-aura/20' : 'text-slate-500 hover:text-white hover:bg-slate-900/50'
            }`}
          >
            <t.icon size={14} /> {t.name}
          </button>
        ))}
      </div>
      <Active />
    </div>
  );
};
