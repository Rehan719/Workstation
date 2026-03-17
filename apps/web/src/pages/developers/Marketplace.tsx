import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, UserCheck } from 'lucide-react';

export const Marketplace: React.FC = () => {
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v230/marketplace/products').then(res => setProducts(res.data));
  }, []);

  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-black mb-2">BTO Marketplace</h1>
        <p className="text-slate-500">Third-party agentic products and reactors certified by the Workstation CoEs.</p>
      </header>

      <section className="p-10 rounded-[3rem] bg-gradient-to-br from-aura/20 to-highlight/10 border border-aura/30 relative overflow-hidden">
         <div className="relative z-10 flex flex-col md:flex-row gap-10 items-center">
            <div className="w-48 h-48 rounded-3xl bg-slate-900 border border-slate-700 flex items-center justify-center text-6xl shadow-2xl">🚀</div>
            <div className="flex-1 space-y-4 text-center md:text-left">
               <span className="px-3 py-1 bg-aura text-sovereign text-[10px] font-black uppercase rounded-full">Developer Spotlight</span>
               <h2 className="text-4xl font-black italic tracking-tight">NeuroSync Synthesizer</h2>
               <p className="text-slate-400 max-w-xl">Accelerate your knowledge synthesis by 400% with the new NeuroSync reactor. Optimized for Research Mission Mode.</p>
               <button className="px-8 py-3 bg-white text-sovereign font-black rounded-xl hover:scale-105 transition-all">Claim 30-Day Resonance Trial</button>
            </div>
         </div>
         <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-aura/20 rounded-full blur-[100px]"></div>
      </section>

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
