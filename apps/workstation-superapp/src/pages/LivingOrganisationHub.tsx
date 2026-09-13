import React from 'react';
import { useSearchParams, Navigate, Link } from 'react-router-dom';
import { MessageSquare, Crown, Network, Radio, Cpu } from 'lucide-react';
import { CEOChat } from './CEOChat';
import { BoardOfDirectors } from './enterprise/BoardOfDirectors';
import SwarmIntelligence from '../components/organism/SwarmIntelligence';
import AgentHubPanel from '../components/organism/AgentHubPanel';

// Consolidated Living Organisation hub (§5 Chief→Board→AI CEO→… + §6 native swarm) — folds the former
// standalone AI CEO · Board of Directors · Swarm Intelligence surfaces into one tabbed surface
// (deep-linkable ?tab=). Default tab = AI CEO (the primary leadership interaction).
// W460 (P1.12) — the "Composer" tab is RETIRED: it was a local canvas whose nodes reached no swarm, seeded
// with fictional model names, and it printed a green "GaaS COMPLIANT" for nodes nobody evaluated. The real
// designer (role + instruction stages · save · edit · run · each stage shows what served it) is on
// /native-ai; ?tab=composer now lands there.
const TABS = [
  { id: 'ceo',      name: 'AI CEO',   icon: MessageSquare, El: CEOChat },
  { id: 'board',    name: 'Board',    icon: Crown,         El: BoardOfDirectors },
  { id: 'swarm',    name: 'Swarm',    icon: Network,       El: SwarmIntelligence },
  // W443 — the Agent Collaboration Hub's 7 live ops (bus/registry/letterbox) had zero consumers
  { id: 'hub',      name: 'Agent Hub', icon: Radio,        El: AgentHubPanel },
] as const;

export const LivingOrganisationHub: React.FC = () => {
  const [sp, setSp] = useSearchParams();
  const requested = sp.get('tab');
  if (requested === 'composer') return <Navigate to="/native-ai?focus=cascade-designer" replace />;
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
        <Link to="/native-ai?focus=cascade-designer" data-testid="swarm-designer-link"
          title="role + instruction stages · save · edit · run · each stage shows what served it"
          className="ml-auto flex items-center gap-2 px-3 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest text-aura border border-aura/30 hover:bg-aura/10">
          <Cpu size={13} /> Design a swarm cascade → Native AI
        </Link>
      </div>
      <Active />
    </div>
  );
};
