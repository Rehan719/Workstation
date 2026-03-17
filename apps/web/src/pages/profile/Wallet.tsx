import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Wallet as WalletIcon, ArrowUpRight, ArrowDownLeft, ShieldCheck, PieChart } from 'lucide-react';

export const Wallet: React.FC = () => {
  const [wallet, setWallet] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v220/economic/wallet/demo_user').then(res => setWallet(res.data));
  }, []);

  if (!wallet) return <div className="p-8 text-slate-500 animate-pulse">Accessing Secure Vault...</div>;

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black mb-2">Sovereign Wallet</h1>
          <p className="text-slate-500">Manage your WST resonance and participation in the Liability Fund.</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-black text-slate-500 uppercase">Available Resonance</p>
          <p className="text-4xl font-black text-aura">{wallet.balance.toLocaleString()} {wallet.currency}</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <BalanceCard label="Staked Resonance" value={wallet.staked} icon={ShieldCheck} color="text-vital" />
        <BalanceCard label="Federation Grant" value="1,200 WST" icon={Zap} color="text-aura" />
        <BalanceCard label="Active Yield" value="8.4%" icon={PieChart} color="text-highlight" />
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
