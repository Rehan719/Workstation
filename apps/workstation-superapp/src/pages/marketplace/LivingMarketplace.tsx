import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, ShieldCheck, TrendingUp, Search, Tag, ArrowUpRight, History, Plus, DollarSign, Activity, Users, Filter } from 'lucide-react';
import { Card, Button, Badge } from '@workstation/ui';
import { motion, AnimatePresence } from 'framer-motion';

const TAGS = ['LLM', 'ADAPTER', 'TOOL', 'GUARD'];

export const LivingMarketplace: React.FC = () => {
  const [listings, setListings] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [activeTags, setActiveTags] = useState<string[]>([]);
  const [walletConnected, setWalletConnected] = useState(false);

  useEffect(() => {
    // Simulated fetch of 100+ listings
    const mock = Array.from({ length: 8 }).map((_, i) => ({
      id: `list-${i+1}`,
      name: `Specialized Agent v${i}.0`,
      author: `did:vsb:node-${i+42}`,
      price: (0.5 + i * 0.2).toFixed(1),
      rating: 4.8 + (i % 3) * 0.1,
      sales: 142 + i * 5,
      trust: 0.94 + (i % 5) * 0.01,
      tag: TAGS[i % TAGS.length]
    }));
    setListings(mock);
  }, []);

  const filteredListings = listings.filter(item =>
    (!search || item.name.toLowerCase().includes(search.toLowerCase())) &&
    (activeTags.length === 0 || activeTags.includes(item.tag))
  );

  const toggleTag = (tag: string) => {
    setActiveTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]);
  };

  const handleAction = (msg: string) => alert(msg);

  const handleConnectWallet = () => {
    if (walletConnected) return;
    handleAction('Connecting wallet via PQC-secured gateway...');
    setWalletConnected(true);
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter break-words">Living Marketplace</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Global Sovereign Economy • Layer 11 Civilisation</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button variant="outline" onClick={() => handleAction('Order history: no purchases on this node yet.')}><History size={18} /> Orders</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20" onClick={() => handleAction('Opening agent publishing wizard...')}>
              <Plus size={18} /> Publish Agent
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-9 space-y-10">
            {/* Featured Section */}
            <div className="flex justify-between items-center">
               <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                  <TrendingUp size={24} className="text-aura" />
                  Trending Agents
               </h3>
               <div className="flex gap-3">
                  <Badge color="aura">Top Fitness</Badge>
                  <Badge color="highlight">High Reputation</Badge>
               </div>
            </div>

            <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredListings.length === 0 && (
                <p className="text-xs text-slate-500 italic col-span-full">No listings match the current filters.</p>
              )}
              {filteredListings.map((item) => (
                <Card key={item.id} className="group hover:border-aura/50 transition-all flex flex-col relative overflow-hidden">
                   <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10">
                      <ShoppingBag size={80} />
                   </div>
                   <div className="flex justify-between items-start mb-8 relative z-10">
                      <div className="p-4 bg-slate-900 rounded-2xl text-aura shadow-lg border border-slate-800">
                         <ShoppingBag size={24} />
                      </div>
                      <div className="flex flex-col items-end gap-2">
                         <div className="flex items-center gap-1 text-amber-500">
                            <Star size={14} fill="currentColor" />
                            <span className="text-xs font-black">{item.rating.toFixed(1)}</span>
                         </div>
                         <Badge color="emerald-500">{item.trust * 100}% Trust</Badge>
                      </div>
                   </div>

                   <h3 className="text-xl font-black mb-2 text-white uppercase tracking-tight">{item.name}</h3>
                   <p className="text-[10px] font-mono text-slate-500 uppercase mb-8">{item.author.substring(0, 20)}...</p>

                   <div className="mt-auto space-y-6">
                      <div className="flex justify-between items-end">
                         <div>
                            <p className="text-[10px] font-black text-slate-700 uppercase mb-1 tracking-widest">Price</p>
                            <p className="text-2xl font-black text-white">{item.price} <span className="text-aura text-xs">WST</span></p>
                         </div>
                         <div className="text-right">
                            <p className="text-[10px] font-black text-slate-700 uppercase mb-1 tracking-widest">Sales</p>
                            <p className="text-sm font-bold text-slate-400">{item.sales}</p>
                         </div>
                      </div>
                      <Button
                        onClick={() => handleAction(`Acquiring instance of ${item.name} for ${item.price} WST...`)}
                        className="w-full py-4 text-xs font-black uppercase tracking-[0.2em] shadow-lg hover:scale-[1.02]"
                      >Acquire Instance</Button>
                   </div>
                </Card>
              ))}
            </section>

            <Card className="bg-slate-900/40 p-12 border-dashed border-slate-800 text-center">
               <div className="flex flex-col items-center gap-6">
                  <div className="w-20 h-20 rounded-3xl bg-slate-900 flex items-center justify-center text-slate-700">
                     <TrendingUp size={40} />
                  </div>
                  <div className="space-y-2">
                     <h3 className="text-2xl font-black text-slate-400 uppercase tracking-tight">Expand Your Reach</h3>
                     <p className="text-sm text-slate-600 font-bold max-w-lg mx-auto leading-relaxed">
                        Publish your high-fitness recombinants to the global mesh and earn WST rewards from 100+ sovereign nodes.
                     </p>
                  </div>
                  <Button variant="outline" onClick={() => handleAction('Opening Publisher Portal...')} className="px-12 py-4">Publisher Portal</Button>
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-3 space-y-10">
            <Card className="p-8 space-y-10 bg-aura/5 border-aura/20">
               <h4 className="text-xl font-black flex items-center gap-3">
                  <Activity size={20} className="text-aura" />
                  Economy Vitals
               </h4>
               <div className="space-y-8">
                  <div className="space-y-3">
                     <div className="flex justify-between items-end">
                        <span className="text-[10px] font-black uppercase text-slate-500">24h Volume</span>
                        <span className="text-xl font-black text-white">12.4K WST</span>
                     </div>
                     <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-aura w-[74%]" />
                     </div>
                  </div>

                  <div className="grid grid-cols-1 gap-4">
                     <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                        <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Fee Burn</p>
                        <p className="text-lg font-black text-vital">142 WST</p>
                     </div>
                     <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                        <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Reputation Avg</p>
                        <p className="text-lg font-black text-emerald-500">4.92/5</p>
                     </div>
                  </div>
               </div>
               <Button
                  onClick={handleConnectWallet}
                  disabled={walletConnected}
                  className="w-full bg-white text-sovereign py-5 rounded-2xl font-black text-[10px] uppercase tracking-widest disabled:opacity-60"
               >{walletConnected ? 'Wallet Connected' : 'Connect Wallet'}</Button>
            </Card>

            <Card className="p-8 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Filter Marketplace</h4>
               <div className="space-y-4">
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-950 border border-slate-900">
                     <Search size={14} className="text-slate-700" />
                     <input
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search..."
                        className="bg-transparent border-none outline-none text-[10px] text-white font-bold w-full"
                     />
                  </div>
                  <div className="flex flex-wrap gap-2">
                     {TAGS.map(tag => {
                       const active = activeTags.includes(tag);
                       const activeClass = 'px-3 py-1 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all bg-aura text-sovereign';
                       const inactiveClass = 'px-3 py-1 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all bg-slate-900 text-slate-500 hover:text-aura';
                       return active ? (
                         <button type="button" key={tag} onClick={() => toggleTag(tag)} aria-pressed="true" className={activeClass}>{tag}</button>
                       ) : (
                         <button type="button" key={tag} onClick={() => toggleTag(tag)} aria-pressed="false" className={inactiveClass}>{tag}</button>
                       );
                     })}
                  </div>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
