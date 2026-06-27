import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Shield, FileText, ShieldCheck } from 'lucide-react';
import { GovernanceHub } from './GovernanceHub';
import { ConstitutionalUI } from './ConstitutionalUI';
import { ComplianceChecker } from './ComplianceChecker';

// Consolidated Governance & Trust center (§11 live compliance + constitutional gaas) — folds the former
// standalone Governance Hub · Constitution · Compliance pages into one tabbed surface (deep-linkable ?tab=).
const TABS = [
  { id: 'overview',     name: 'Governance',   icon: Shield,      El: GovernanceHub },
  { id: 'constitution', name: 'Constitution', icon: FileText,    El: ConstitutionalUI },
  { id: 'compliance',   name: 'Compliance',   icon: ShieldCheck, El: ComplianceChecker },
] as const;

export const GovernanceCenter: React.FC = () => {
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
