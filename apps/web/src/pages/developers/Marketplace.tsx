import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, UserCheck } from 'lucide-react';

export const Marketplace: React.FC = () => {
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v230/marketplace/products').then(res => setProducts(res.data));
  }, []);

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">BTO Marketplace</h1>
        <p className="text-slate-500">Third-party agentic products and reactors certified by the Workstation CoEs.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {products.map(p => (
          <div key={p.id} className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm group">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-aura/10 text-aura rounded-xl group-hover:scale-110 transition-transform">
                <ShoppingBag size={24} />
              </div>
              <div className="flex items-center gap-1 text-highlight">
                <Star size={14} fill="currentColor" />
                <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Certified</span>
              </div>
            </div>

            <h3 className="text-xl font-bold mb-1">{p.name}</h3>
            <p className="text-xs text-slate-500 mb-6 flex items-center gap-1">
               <UserCheck size={12} />
               By {p.author}
            </p>

            <div className="flex items-center justify-between mt-auto">
              <span className="text-2xl font-black">{p.price.toLocaleString()} WST</span>
              <button className="px-6 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs font-bold hover:border-aura transition-all">Buy Now</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
