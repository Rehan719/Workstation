import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { ShoppingBag, Star, UserCheck, Search, Filter, CheckCircle2, Loader2, Plus, X, Tag } from 'lucide-react';
import { toast } from '@workstation/ui';

interface Listing {
  id: string;
  name: string;
  description: string;
  author: string;
  category: string;
  price_wst: number;
  tier: string;
  tags: string[];
  certified: boolean;
  status: string;
  sales_count: number;
}

const CATEGORIES = ['All', 'Platform', 'Reactor', 'Analytics', 'AI Agent', 'Developer', 'Product'];

export const Marketplace: React.FC = () => {
  const [listings,    setListings]    = useState<Listing[]>([]);
  const [loading,     setLoading]     = useState(true);
  const [search,      setSearch]      = useState('');
  const [category,    setCategory]    = useState('All');
  const [certOnly,    setCertOnly]    = useState(false);
  const [buying,      setBuying]      = useState<string | null>(null);
  const [purchased,   setPurchased]   = useState<Set<string>>(new Set());
  const [showCreate,  setShowCreate]  = useState(false);

  // Create form
  const [newName,     setNewName]     = useState('');
  const [newDesc,     setNewDesc]     = useState('');
  const [newPrice,    setNewPrice]    = useState('');
  const [newCat,      setNewCat]      = useState('Product');
  const [creating,    setCreating]    = useState(false);

  const fetchListings = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (search)   params.search = search;
      if (category !== 'All') params.category = category;
      if (certOnly) params.certified_only = 'true';
      const { data } = await axios.get('/api/v1/marketplace/listings', { params });
      setListings(data);
    } catch {
      setListings([]);
    } finally {
      setLoading(false);
    }
  }, [search, category, certOnly]);

  useEffect(() => { fetchListings(); }, [fetchListings]);

  const handleBuy = async (listing: Listing) => {
    if (purchased.has(listing.id)) return;
    setBuying(listing.id);
    try {
      await axios.post(`/api/v1/marketplace/listings/${listing.id}/purchase`, {
        user_id: 'demo_user',
        quantity: 1,
      });
      setPurchased(prev => new Set([...prev, listing.id]));
      toast(`✓ Purchased "${listing.name}" — ${listing.price_wst.toLocaleString()} WST deducted`);
    } catch (err: any) {
      const detail = err.response?.data?.detail ?? err.message;
      toast(`Purchase failed: ${detail}`);
    } finally {
      setBuying(null);
    }
  };

  const handleCreate = async () => {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await axios.post('/api/v1/marketplace/listings', {
        name: newName,
        description: newDesc,
        category: newCat,
        price_wst: parseFloat(newPrice) || 0,
        author: 'You',
        creator_id: 'demo_user',
      });
      toast('Listing created!');
      setShowCreate(false);
      setNewName(''); setNewDesc(''); setNewPrice('');
      fetchListings();
    } catch (err: any) {
      toast(`Create failed: ${err.response?.data?.detail ?? err.message}`);
    } finally {
      setCreating(false);
    }
  };

  const featured = listings.find(l => l.certified && l.category === 'Platform') ?? listings[0];

  return (
    <div className="space-y-10 pb-24" role="main" aria-label="BTO Marketplace">
      {/* Header */}
      <header className="flex flex-col @[480px]:flex-row @[480px]:items-end justify-between gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl font-black text-white uppercase tracking-tighter italic break-words">
            BTO <span className="text-aura">Marketplace</span>
          </h1>
          <p className="text-slate-500 text-xs font-bold mt-1">
            Certified agentic products, reactors, and modules. Pay with WST.
          </p>
        </div>
        <button type="button" onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-aura text-sovereign rounded-xl font-black text-xs uppercase tracking-widest hover:opacity-90 transition-opacity shrink-0">
          <Plus size={14} /> List Product
        </button>
      </header>

      {/* Search + filter bar */}
      <div className="flex flex-wrap gap-3 items-center">
        <div className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-700 bg-slate-900 flex-1 min-w-[180px] max-w-sm">
          <Search size={14} className="text-slate-500 shrink-0" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search listings…"
            aria-label="Search marketplace"
            className="bg-transparent text-xs text-white placeholder-slate-600 outline-none w-full font-bold"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {CATEGORIES.map(c => (
            <button key={c} type="button" onClick={() => setCategory(c)}
              className={`px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all border ${category === c ? 'bg-aura text-sovereign border-aura' : 'border-slate-700 text-slate-500 hover:text-white hover:border-slate-600'}`}>
              {c}
            </button>
          ))}
        </div>
        <label className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border transition-all cursor-pointer ${certOnly ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400' : 'border-slate-700 text-slate-500 hover:text-white'}`}>
          <input type="checkbox" checked={certOnly} onChange={() => setCertOnly(v => !v)} className="sr-only" />
          <Star size={10} aria-hidden="true" /> Certified Only
        </label>
      </div>

      {/* Featured banner */}
      {featured && !loading && (
        <div className="p-8 rounded-[2rem] border border-aura/20 bg-gradient-to-br from-aura/10 to-highlight/5 flex flex-col @[480px]:flex-row gap-8 items-center">
          <div className="w-20 h-20 rounded-2xl bg-slate-900 border border-slate-700 flex items-center justify-center text-4xl shrink-0">
            🚀
          </div>
          <div className="flex-1 min-w-0 text-center @[480px]:text-left">
            <span className="px-2 py-0.5 bg-aura text-sovereign text-[8px] font-black uppercase rounded-full">Featured</span>
            <h2 className="text-2xl font-black text-white italic tracking-tight mt-2">{featured.name}</h2>
            <p className="text-slate-400 text-xs mt-1 line-clamp-2">{featured.description}</p>
          </div>
          <button type="button"
            onClick={() => handleBuy(featured)}
            disabled={!!buying || purchased.has(featured.id)}
            className="px-6 py-2.5 bg-white text-sovereign font-black rounded-xl text-xs uppercase tracking-widest hover:scale-105 transition-all disabled:opacity-50 shrink-0">
            {purchased.has(featured.id) ? '✓ Purchased' : `${featured.price_wst.toLocaleString()} WST`}
          </button>
        </div>
      )}

      {/* Listings grid */}
      {loading ? (
        <div className="flex items-center justify-center py-20 gap-3 text-slate-500">
          <Loader2 size={20} className="animate-spin" />
          <span className="text-xs font-bold uppercase tracking-widest">Loading listings…</span>
        </div>
      ) : listings.length === 0 ? (
        <div className="text-center py-20">
          <ShoppingBag size={36} className="text-slate-700 mx-auto mb-4" />
          <p className="text-sm font-black text-slate-500 uppercase tracking-widest">No listings found</p>
          <p className="text-xs text-slate-600 mt-2">Try a different search or category filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 @[440px]:grid-cols-2 @[720px]:grid-cols-3 gap-6">
          {listings.map(l => {
            const isBuying   = buying === l.id;
            const isPurchased = purchased.has(l.id);
            return (
              <div key={l.id} className="p-6 rounded-2xl border border-slate-800 bg-slate-950/40 hover:border-aura/30 transition-all group flex flex-col"
                role="article" aria-label={`${l.name} by ${l.author}`}>
                <div className="flex justify-between items-start mb-5">
                  <div className="p-2.5 rounded-xl bg-aura/10 text-aura group-hover:scale-110 transition-transform">
                    <ShoppingBag size={18} />
                  </div>
                  <div className="flex items-center gap-2">
                    {l.certified && (
                      <span className="flex items-center gap-1 text-emerald-400 text-[8px] font-black uppercase">
                        <Star size={9} fill="currentColor" /> Certified
                      </span>
                    )}
                    <span className="px-2 py-0.5 bg-slate-800 text-slate-400 text-[8px] font-black uppercase rounded-full">{l.tier}</span>
                  </div>
                </div>

                <h3 className="text-sm font-black text-white uppercase tracking-tight mb-1">{l.name}</h3>
                <p className="text-[9px] text-slate-500 mb-1 flex items-center gap-1">
                  <UserCheck size={10} /> {l.author}
                </p>
                <p className="text-[9px] text-slate-400 leading-relaxed flex-1 mb-4 line-clamp-3">{l.description}</p>

                {l.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-4">
                    {l.tags.slice(0, 3).map(t => (
                      <span key={t} className="flex items-center gap-1 px-1.5 py-0.5 bg-slate-900 border border-slate-800 rounded-md text-[8px] font-bold text-slate-500">
                        <Tag size={7} />{t}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex items-center justify-between mt-auto pt-3 border-t border-slate-800">
                  <span className="text-lg font-black text-white">
                    {l.price_wst > 0 ? `${l.price_wst.toLocaleString()} WST` : 'Free'}
                  </span>
                  <button type="button"
                    onClick={() => handleBuy(l)}
                    disabled={isBuying || isPurchased}
                    className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all ${
                      isPurchased
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : 'bg-slate-800 border border-slate-700 text-white hover:border-aura hover:bg-aura/10 disabled:opacity-40'
                    }`}>
                    {isBuying
                      ? <><Loader2 size={10} className="animate-spin" /> Buying…</>
                      : isPurchased
                        ? <><CheckCircle2 size={10} /> Owned</>
                        : 'Buy Now'
                    }
                  </button>
                </div>

                {l.sales_count > 0 && (
                  <p className="text-[8px] text-slate-600 mt-2">{l.sales_count} sale{l.sales_count !== 1 ? 's' : ''}</p>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Create listing modal */}
      {showCreate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-6">
          <div className="bg-slate-950 border border-slate-800 rounded-[2rem] p-8 w-full max-w-md space-y-5">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-black text-white uppercase tracking-tight">List a Product</h3>
              <button type="button" aria-label="Close" onClick={() => setShowCreate(false)}
                className="text-slate-500 hover:text-white"><X size={18} /></button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-[9px] font-black uppercase text-slate-500 tracking-widest block mb-1">Product Name</label>
                <input value={newName} onChange={e => setNewName(e.target.value)} aria-label="Product name"
                  placeholder="e.g. Custom AI Reactor" className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-aura" />
              </div>
              <div>
                <label className="text-[9px] font-black uppercase text-slate-500 tracking-widest block mb-1">Description</label>
                <textarea value={newDesc} onChange={e => setNewDesc(e.target.value)} rows={3} aria-label="Description"
                  placeholder="What does this product do?" className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-aura resize-none" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[9px] font-black uppercase text-slate-500 tracking-widest block mb-1">Category</label>
                  <select value={newCat} onChange={e => setNewCat(e.target.value)} aria-label="Category"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura">
                    {CATEGORIES.filter(c => c !== 'All').map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-[9px] font-black uppercase text-slate-500 tracking-widest block mb-1">Price (WST)</label>
                  <input type="number" min="0" value={newPrice} onChange={e => setNewPrice(e.target.value)} aria-label="Price in WST"
                    placeholder="0 = Free" className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura" />
                </div>
              </div>
            </div>
            <button type="button" onClick={handleCreate} disabled={!newName.trim() || creating}
              className="w-full py-3 bg-aura text-sovereign rounded-xl font-black uppercase tracking-widest text-xs hover:opacity-90 disabled:opacity-40 flex items-center justify-center gap-2">
              {creating ? <><Loader2 size={12} className="animate-spin" /> Creating…</> : 'Create Listing'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
