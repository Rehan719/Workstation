import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, RefreshCw, Download, Zap, Heart, User, Filter, CreditCard, History } from 'lucide-react';

export const LivingMarketplace: React.FC = () => {
  const [listings, setListings] = useState<any[]>([]);
  const [wallet, setWallet] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v290/marketplace/v2/listings').then(res => setListings(res.data));
    axios.get('/api/v290/marketplace/v2/wallet/guardian').then(res => setWallet(res.data));
  }, []);

  const handleRemix = async (id: string) => {
    const res = await axios.post(`/api/v290/marketplace/v2/remix?listing_id=${id}&user_id=guardian`);
    if (res.data.status === 'remixed') {
      alert("Creation Remixed! A hard-fork has been added to your Creator Studio.");
    }
  };

  return (
    <div className="space-y-12">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-4xl font-black mb-2">Living Marketplace</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Community Forge & Exchange v150.0</p>
        </div>

        {wallet && (
           <div className="flex items-center gap-4 bg-vital/10 border border-vital/30 px-6 py-3 rounded-2xl">
              <div className="text-right">
                 <p className="text-[10px] font-black text-vital uppercase">Creator Balance</p>
                 <p className="text-xl font-black">{wallet.balance_wst.toLocaleString()} WST</p>
              </div>
              <div className="p-2 bg-vital/20 rounded-lg text-vital">
                 <CreditCard size={20} />
              </div>
           </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {listings.map(item => (
          <div key={item.id} className="glass-card p-8 group border-white/5 hover:border-aura/30 flex flex-col">
             <div className="flex justify-between items-start mb-6">
                <div className="p-4 bg-surface rounded-2xl text-slate-500 group-hover:text-aura transition-colors">
                   <Zap size={24} />
                </div>
                <div className="flex items-center gap-1 bg-sovereign px-3 py-1 rounded-full border border-white/5 text-[10px] font-black text-highlight">
                   <Star size={12} fill="currentColor" />
                   {item.rating}
                </div>
             </div>

             <h3 className="text-2xl font-black mb-1">{item.name}</h3>
             <div className="flex items-center gap-2 mb-6">
                <User size={12} className="text-slate-500" />
                <span className="text-xs font-bold text-slate-500">by @{item.creator_id}</span>
             </div>

             <div className="mt-auto space-y-4 pt-6 border-t border-white/5">
                <div className="flex justify-between items-end">
                   <div>
                      <p className="text-[10px] font-black text-slate-500 uppercase">License Fee</p>
                      <p className="text-xl font-black">{item.price_wst === 0 ? 'FREE' : `${item.price_wst} WST`}</p>
                   </div>
                   <button
                     onClick={() => handleRemix(item.id)}
                     className="flex items-center gap-2 px-6 py-3 bg-white/5 border border-white/10 rounded-xl font-bold text-xs uppercase tracking-widest hover:border-aura hover:text-aura transition-all"
                   >
                     <RefreshCw size={14} />
                     Remix
                   </button>
                </div>
                <button className="w-full py-4 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all shadow-lg shadow-aura/10 uppercase tracking-widest text-xs">
                  {item.price_wst === 0 ? 'Install Creation' : 'Purchase License'}
                </button>
             </div>
          </div>
        ))}
      </div>
    </div>
  );
};
