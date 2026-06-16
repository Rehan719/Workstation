import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, UserCheck, Search, Filter, TrendingUp } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';
import { notImplemented } from '@workstation/ui';

export const Marketplace: React.FC = () => {
  const { theme } = useTheme();
  const isAdvanced = theme === 'advanced';
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v230/marketplace/products').then(res => setProducts(res.data));
  }, []);

  return (
    <div className={`space-y-12 transition-all duration-1000 ${isAdvanced ? 'animate-in fade-in slide-in-from-bottom-4' : ''}`} role="main" aria-label="BTO Marketplace">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-black mb-2 transition-all">BTO Marketplace</h1>
          <p className="text-slate-500">Third-party agentic products and reactors certified by the Workstation CoEs.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${
            isAdvanced ? 'bg-sovereign border-aura/30 focus-within:border-aura' : 'bg-slate-900 border-slate-700'
          }`}>
            <Search size={16} className="text-slate-500" />
            <input placeholder="Search products..." className="bg-transparent border-none outline-none text-xs w-48 font-bold" />
          </div>
          <button type="button" onClick={() => notImplemented('Filter products')} className={`p-2.5 rounded-xl border transition-all ${
            isAdvanced ? 'bg-sovereign border-aura/30 hover:border-aura' : 'bg-slate-900 border-slate-700 hover:border-aura'
          }`} aria-label="Filter products">
            <Filter size={18} className="text-aura" />
          </button>
        </div>
      </header>

      <section className={`p-10 rounded-[3rem] border relative overflow-hidden transition-all duration-700 ${
        isAdvanced ? 'bg-sovereign border-aura/30 shadow-[0_0_50px_rgba(100,255,218,0.1)]' : 'bg-gradient-to-br from-aura/20 to-highlight/10 border-aura/30'
      }`}>
         <div className="relative z-10 flex flex-col md:flex-row gap-10 items-center">
            <div className="w-48 h-48 rounded-3xl bg-slate-900 border border-slate-700 flex items-center justify-center text-6xl shadow-2xl">🚀</div>
            <div className="flex-1 space-y-4 text-center md:text-left">
               <span className="px-3 py-1 bg-aura text-sovereign text-[10px] font-black uppercase rounded-full">Developer Spotlight</span>
               <h2 className="text-4xl font-black italic tracking-tight">NeuroSync Synthesizer</h2>
               <p className="text-slate-400 max-w-xl">Accelerate your knowledge synthesis by 400% with the new NeuroSync reactor. Optimized for Research Mission Mode.</p>
               <button type="button" onClick={() => notImplemented('Claim 30-Day Resonance Trial')} className="px-8 py-3 bg-white text-sovereign font-black rounded-xl hover:scale-105 transition-all">Claim 30-Day Resonance Trial</button>
            </div>
         </div>
         <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-aura/20 rounded-full blur-[100px]"></div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {products.map(p => (
          <div key={p.id} className={`p-8 rounded-3xl border transition-all group backdrop-blur-sm ${
            isAdvanced ? 'bg-sovereign border-aura/10 hover:border-aura/50 shadow-lg' : 'bg-slate-900/40 border-slate-800 hover:border-aura'
          }`} role="article" aria-label={`${p.name} by ${p.author}`}>
            <div className="flex justify-between items-start mb-6">
              <div className={`p-3 rounded-xl group-hover:scale-110 transition-transform ${
                isAdvanced ? 'bg-aura/10 text-aura shadow-[0_0_15px_rgba(100,255,218,0.2)]' : 'bg-aura/10 text-aura'
              }`}>
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
              <button type="button" onClick={() => notImplemented(`Buy ${p.name}`)} className="px-6 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs font-bold hover:border-aura transition-all">Buy Now</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
