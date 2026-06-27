import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { MessageSquare, Crown, Network, Workflow } from 'lucide-react';
import { CEOChat } from './CEOChat';
import { BoardOfDirectors } from './enterprise/BoardOfDirectors';
import VisualAgentComposer from '../components/organism/VisualAgentComposer';
import SwarmIntelligence from '../components/organism/SwarmIntelligence';

// Consolidated Living Organisation hub (§5 Chief→Board→AI CEO→… + §6 native swarm) — folds the former
// standalone AI CEO · Board of Directors · Swarm Intelligence · Visual Composer surfaces into one tabbed
// surface (deep-linkable ?tab=). Default tab = AI CEO (the primary leadership interaction).
const TABS = [
  { id: 'ceo',      name: 'AI CEO',   icon: MessageSquare, El: CEOChat },
  { id: 'board',    name: 'Board',    icon: Crown,         El: BoardOfDirectors },
  { id: 'swarm',    name: 'Swarm',    icon: Network,       El: SwarmIntelligence },
  { id: 'composer', name: 'Composer', icon: Workflow,      El: VisualAgentComposer },
] as const;

export const LivingOrganisationHub: React.FC = () => {
  const [sp, setSp] = useSearchParams();
  const requested = sp.get('tab');
  const active = TABS.some(t => t.id === requested) ? requested! : 'ceo';
  const Active = (TABS.find(t => t.id === active) ?? TABS[0]).El;

  return (
    <div className="space-y-6 pb-16">
      <div className="flex items-center gap-2 flex-wrap border-b border-slate-900 pb-3">
        {TABS.map(t => (
          <button
            key={t.id}
            type="button"
            onClick={() => setSp(t.id === 'ceo' ? {} : { tab: t.id }, { replace: true })}
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
