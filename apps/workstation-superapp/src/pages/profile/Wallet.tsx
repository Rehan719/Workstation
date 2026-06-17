import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Wallet as WalletIcon, ArrowUpRight, ArrowDownLeft, ShieldCheck, PieChart, Activity, Star, Shield, CreditCard, Landmark, DollarSign } from 'lucide-react';
import { notImplemented } from '@workstation/ui';

export const Wallet: React.FC = () => {
  const [wallet, setWallet] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v310/payments/wallet/demo_user/v2').then(res => setWallet(res.data));
  }, []);

  if (!wallet) return <div className="p-8 text-slate-500 animate-pulse">Accessing Secure Vault...</div>;

  return (
    <div className="space-y-12 animate-in fade-in duration-1000">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black tracking-tight neon-text break-words">Sovereign Economy</h1>
          <p className="text-slate-500 font-bold text-lg mt-2">Manage your creator earnings, WST liquidity, and fiat payouts.</p>
        </div>
        <div className="text-right flex items-center gap-6">
           <div>
             <p className="text-[10px] font-black text-slate-500 uppercase">WST Resonance</p>
             <p className="text-4xl font-black text-aura">{wallet.balances.wst.toLocaleString()}</p>
           </div>
           <div className="h-10 w-[1px] bg-white/10"></div>
           <div>
             <p className="text-[10px] font-black text-slate-500 uppercase">Pending Fiat</p>
             <p className="text-4xl font-black text-white">${wallet.balances.fiat_pending_usd.toFixed(2)}</p>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <BalanceCard label="Staked WST" value="8,400" icon={Shield} color="text-vital" />
        <BalanceCard label="Fiat Connected" value={wallet.stripe_connected ? "STRIPE ACTIVE" : "NOT LINKED"} icon={CreditCard} color="text-aura" />
        <BalanceCard label="Polygon Node" value="SYNCED" icon={Activity} color="text-highlight" />
        <BalanceCard label="Creator Score" value="A+" icon={Star} color="text-aura" />
      </div>

      <div className="p-12 glass-card bg-aura/5 border-aura/20 flex items-center justify-between">
         <div className="flex items-center gap-6">
            <div className="p-4 bg-aura/20 rounded-2xl text-aura">
               <Landmark size={32} />
            </div>
            <div>
               <h3 className="text-2xl font-black">Withdraw to Bank</h3>
               <p className="text-slate-400 font-bold">Transfer your pending USD balance to your linked Stripe account.</p>
            </div>
         </div>
         <button onClick={() => notImplemented('Initiate Payout')} className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all">Initiate Payout</button>
      </div>

      <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800">
        <h3 className="text-xl font-bold mb-8">Recent Transactions</h3>
        <div className="space-y-4">
          {wallet.transactions.map((tx: any, i: number) => (
            <div key={i} className="flex items-center justify-between p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
               <div className="flex items-center gap-4">
                 <div className={`p-2 rounded-lg ${tx.amount > 0 ? 'bg-vital/10 text-vital' : 'bg-rose-500/10 text-rose-500'}`}>
                   {tx.amount > 0 ? <ArrowDownLeft size={20} /> : <ArrowUpRight size={20} />}
                 </div>
                 <div>
                   <p className="font-bold uppercase tracking-widest text-xs text-white">{tx.type}</p>
                   <p className="text-[10px] text-slate-500 mt-1">Status: {tx.status}</p>
                 </div>
               </div>
               <div className={`text-lg font-black ${tx.amount > 0 ? 'text-vital' : 'text-white'}`}>
                 {tx.amount > 0 ? '+' : ''}{tx.amount} WST
               </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const BalanceCard = ({ label, value, icon: Icon, color }: any) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
    <div className="flex justify-between items-center mb-6">
      <div className={`p-3 rounded-xl bg-slate-800/50 ${color}`}>
        <Icon size={24} />
      </div>
    </div>
    <div className="text-3xl font-black">{typeof value === 'number' ? value.toLocaleString() : value}</div>
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mt-1">{label}</p>
  </div>
);
