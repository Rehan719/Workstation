import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Coins, DollarSign, Wallet as WalletIcon } from 'lucide-react';
import { VSBEconomy } from './VSBEconomy';
import { CapitalDashboard } from './CapitalDashboard';
import { Wallet } from '../profile/Wallet';

// Consolidated Economy center (§12 economic organism) — folds the former standalone Economic Metabolism ·
// Capital Fund · Wallet pages into one tabbed surface (deep-linkable ?tab=). Virtual WST until the Owner
// directs real rails.
const TABS = [
  { id: 'overview', name: 'Economy',      icon: Coins,      El: VSBEconomy },
  { id: 'capital',  name: 'Capital Fund', icon: DollarSign, El: CapitalDashboard },
  { id: 'wallet',   name: 'Wallet',       icon: WalletIcon, El: Wallet },
] as const;

export const EconomyCenter: React.FC = () => {
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
