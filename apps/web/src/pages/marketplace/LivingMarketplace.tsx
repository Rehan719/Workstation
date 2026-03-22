import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, ShieldCheck, TrendingUp, Search, Tag, ArrowUpRight } from 'lucide-react';
import { Card, Button } from '@workstation/ui';

export const LivingMarketplace: React.FC = () => {
  const [listings, setListings] = useState<any[]>([]);

  useEffect(() => {
    // Simulated fetch of 100+ listings
    const mock = Array.from({ length: 12 }).map((_, i) => ({
      id: `list-${i+1}`,
      name: `Specialized Agent v${i}.0`,
      author: 'Node-Omega',
      price: (0.5 + i * 0.2).toFixed(1),
      rating: 4.8,
      sales: 142 + i * 5
    }));
    setListings(mock);
  }, []);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end border-b border-white/5 pb-8">
        <div>
          <h1 className="text-5xl font-black mb-1 text-aura">Agent Marketplace</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-aura">Global Sovereign Economy • L11 Civilisation</p>
        </div>
        <div className="flex gap-4">
           <Card className="px-6 py-2 bg-aura/5 border-aura/20">
              <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Monthly TX</p>
              <p className="text-xl font-black text-aura">1,240+</p>
           </Card>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {listings.map((item) => (
          <Card key={item.id} className="group hover:border-aura/50 transition-all flex flex-col">
             <div className="flex justify-between items-start mb-6">
                <div className="p-3 bg-slate-900 rounded-xl text-aura">
                   <ShoppingBag size={24} />
                </div>
                <div className="flex items-center gap-1 text-amber-500">
                   <Star size={12} fill="currentColor" />
                   <span className="text-[10px] font-black">{item.rating}</span>
                </div>
             </div>

             <h3 className="text-lg font-bold mb-1 text-white">{item.name}</h3>
             <p className="text-[10px] font-black text-slate-600 uppercase mb-6">Author: {item.author}</p>

             <div className="mt-auto space-y-4">
                <div className="flex justify-between items-end">
                   <div>
                      <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Price</p>
                      <p className="text-xl font-black text-white">{item.price} WST</p>
                   </div>
                   <div className="text-right">
                      <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Deployments</p>
                      <p className="text-sm font-bold text-slate-400">{item.sales}</p>
                   </div>
                </div>
                <Button className="w-full text-[10px] uppercase tracking-widest">Acquire Instance</Button>
             </div>
          </Card>
        ))}
      </section>

      <Card className="bg-slate-900/40 p-10 border-dashed border-slate-800">
         <div className="flex flex-col items-center text-center gap-6">
            <TrendingUp size={48} className="text-slate-700" />
            <div className="space-y-2">
               <h3 className="text-xl font-black text-slate-400">Expand Your Reach</h3>
               <p className="text-sm text-slate-600 font-bold max-w-md">Publish your high-fitness recombinants to the global mesh and earn WST rewards from 100+ sovereign nodes.</p>
            </div>
            <Button variant="secondary">Access Publisher Portal</Button>
         </div>
      </Card>
    </div>
  );
};
