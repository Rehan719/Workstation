import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  ShoppingBag, Star, TrendingUp, Search, History, Plus,
  Activity, Package, Loader2, AlertTriangle, CheckSquare,
  Crown, Boxes, Layers, Globe2, ExternalLink, ArrowDownAZ, X,
} from 'lucide-react';
import { Card, Button, Badge } from '@workstation/ui';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// ── Types ─────────────────────────────────────────────────────────────────────

type Tab = 'listings' | 'products';

const TAGS = ['LLM', 'ADAPTER', 'TOOL', 'GUARD'];

interface CatalogProduct {
  slug: string;
  name: string;
  tier: string;
  category: string;
  features: string[];
  source: string | null;
  route: string | null;
}

const CATEGORY_ICON: Record<string, React.ElementType> = {
  SDK: Boxes,
  Platform: Layers,
  Domain: Globe2,
};

const normalizeCategory = (cat: string) => cat.split(' (')[0].trim();

const TIER_RANK: Record<string, number> = {
  'Enterprise+': 0, 'Enterprise': 1, 'Standard/Pro/Enterprise': 2, 'Standard/Pro': 3, 'Domain': 4,
};
const tierRank = (t: string) => TIER_RANK[t] ?? 5;
type SortMode = 'name' | 'tier';

// ── Component ─────────────────────────────────────────────────────────────────

export const LivingMarketplace: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<Tab>('listings');

  // ── Listings state ─────────────────────────────────────────────────────────
  const [listings, setListings] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [activeTags, setActiveTags] = useState<string[]>([]);
  const [walletConnected, setWalletConnected] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const notify = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  // ── Products state ─────────────────────────────────────────────────────────
  const [catalogProducts, setCatalogProducts] = useState<CatalogProduct[]>([]);
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [catalogError, setCatalogError] = useState(false);
  const [productSearch, setProductSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [sortMode, setSortMode] = useState<SortMode>('tier');

  // ── Load ───────────────────────────────────────────────────────────────────

  useEffect(() => {
    setListings(Array.from({ length: 8 }).map((_, i) => ({
      id: `list-${i + 1}`,
      name: `Specialized Agent v${i}.0`,
      author: `did:vsb:node-${i + 42}`,
      price: (0.5 + i * 0.2).toFixed(1),
      rating: 4.8 + (i % 3) * 0.1,
      sales: 142 + i * 5,
      trust: 0.94 + (i % 5) * 0.01,
      tag: TAGS[i % TAGS.length],
    })));
  }, []);

  useEffect(() => {
    axios.get('/api/v1/catalog/products')
      .then(r => setCatalogProducts(r.data.products))
      .catch(() => setCatalogError(true))
      .finally(() => setCatalogLoading(false));
  }, []);

  // ── Products derived ───────────────────────────────────────────────────────

  const categories = useMemo(
    () => Array.from(new Set(catalogProducts.map(p => normalizeCategory(p.category)))).sort(),
    [catalogProducts]
  );

  const sortProducts = (list: CatalogProduct[]) =>
    [...list].sort(
      sortMode === 'name'
        ? (a, b) => a.name.localeCompare(b.name)
        : (a, b) => tierRank(a.tier) - tierRank(b.tier) || a.name.localeCompare(b.name)
    );

  const filteredCatalog = sortProducts(catalogProducts.filter(p =>
    (!activeCategory || normalizeCategory(p.category) === activeCategory) &&
    (!productSearch || p.name.toLowerCase().includes(productSearch.toLowerCase()) || p.slug.toLowerCase().includes(productSearch.toLowerCase()))
  ));

  const catalogSections = useMemo(() => {
    if (activeCategory) return [{ category: activeCategory, items: filteredCatalog }];
    const map = new Map<string, CatalogProduct[]>();
    filteredCatalog.forEach(p => { const k = normalizeCategory(p.category); map.set(k, [...(map.get(k) || []), p]); });
    return categories.filter(c => map.has(c)).map(c => ({ category: c, items: map.get(c)! }));
  }, [filteredCatalog, activeCategory, categories]);

  const toggleTag = (tag: string) =>
    setActiveTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]);

  const filteredListings = listings.filter(item =>
    (!search || item.name.toLowerCase().includes(search.toLowerCase())) &&
    (activeTags.length === 0 || activeTags.includes(item.tag))
  );

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-8 pb-10">

      <header>
        <h1 className="text-3xl @[440px]:text-4xl @[900px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">
          Living <span className="text-aura">Marketplace</span>
        </h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">
          Global Sovereign Economy · {catalogProducts.length} Products
        </p>
      </header>

      {/* Toast */}
      {toast && (
        <div role="status" aria-live="polite" className="px-4 py-3 rounded-2xl bg-aura/10 border border-aura/30 text-aura text-xs font-bold animate-in fade-in slide-in-from-top-2 duration-200">
          {toast}
        </div>
      )}

      {/* Tab bar */}
      <div className="flex items-center gap-1 p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
        <button
          type="button"
          onClick={() => setActiveTab('listings')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
            activeTab === 'listings' ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-white'
          }`}
        >
          <ShoppingBag size={13} /> Marketplace
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('products')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
            activeTab === 'products' ? 'bg-aura text-sovereign shadow-lg' : 'text-slate-500 hover:text-white'
          }`}
        >
          <Package size={13} /> Products ({catalogProducts.length})
        </button>
      </div>

      {/* ── LISTINGS TAB ──────────────────────────────────────────────────── */}
      {activeTab === 'listings' && (
        <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
          <main className="@[440px]:col-span-9 space-y-10">
            <div className="flex justify-between items-center flex-wrap gap-4">
              <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                <TrendingUp size={24} className="text-aura" /> Trending Agents
              </h3>
              <div className="flex gap-3 flex-wrap">
                <Button variant="outline" onClick={() => notify('Order history: no purchases on this node yet.')}><History size={18} /> Orders</Button>
                <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20" onClick={() => notify('Opening agent publishing wizard...')}>
                  <Plus size={18} /> Publish Agent
                </Button>
              </div>
            </div>

            <section className="grid grid-cols-1 @[440px]:grid-cols-2 @[700px]:grid-cols-3 gap-6">
              {filteredListings.length === 0 && (
                <p className="text-xs text-slate-500 italic col-span-full">No listings match the current filters.</p>
              )}
              {filteredListings.map(item => (
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
                      onClick={() => notify(`Acquiring instance of ${item.name} for ${item.price} WST...`)}
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
                    Publish high-fitness recombinants to the global mesh and earn WST rewards from 100+ sovereign nodes.
                  </p>
                </div>
                <Button variant="outline" onClick={() => notify('Opening Publisher Portal...')} className="px-12 py-4">Publisher Portal</Button>
              </div>
            </Card>
          </main>

          <aside className="@[440px]:col-span-3 space-y-10">
            <Card className="p-8 space-y-10 bg-aura/5 border-aura/20">
              <h4 className="text-xl font-black flex items-center gap-3">
                <Activity size={20} className="text-aura" /> Economy Vitals
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
                onClick={() => { if (!walletConnected) { notify('Connecting wallet via PQC-secured gateway...'); setWalletConnected(true); } }}
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
                    onChange={e => setSearch(e.target.value)}
                    placeholder="Search..."
                    aria-label="Search marketplace"
                    className="bg-transparent border-none outline-none text-[10px] text-white font-bold w-full"
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                  {TAGS.map(tag => {
                    const active = activeTags.includes(tag);
                    return (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => toggleTag(tag)}
                        {...({ 'aria-pressed': active ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
                        className={`px-3 py-1 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all ${
                          active ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-500 hover:text-aura'
                        }`}
                      >{tag}</button>
                    );
                  })}
                </div>
              </div>
            </Card>
          </aside>
        </div>
      )}

      {/* ── PRODUCTS TAB ──────────────────────────────────────────────────── */}
      {activeTab === 'products' && (
        <div className="flex flex-col gap-8">
          <div className="flex flex-col gap-3">
            <div className="flex flex-col @[500px]:flex-row gap-3 @[500px]:items-center @[500px]:justify-between">
              <div className="flex items-center gap-3 px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-2xl max-w-xs flex-1">
                <Search size={14} className="text-slate-600 shrink-0" />
                <input
                  value={productSearch}
                  onChange={e => setProductSearch(e.target.value)}
                  placeholder="Search products..."
                  aria-label="Search products"
                  className="bg-transparent outline-none text-xs text-white font-bold w-full"
                />
                {productSearch && (
                  <button type="button" onClick={() => setProductSearch('')} aria-label="Clear search" title="Clear" className="text-slate-600 hover:text-white shrink-0">
                    <X size={12} />
                  </button>
                )}
              </div>
              <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 w-fit">
                {(['tier', 'name'] as SortMode[]).map(mode => (
                  <button
                    key={mode}
                    type="button"
                    onClick={() => setSortMode(mode)}
                    {...({ 'aria-pressed': sortMode === mode ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all ${
                      sortMode === mode ? 'bg-aura text-sovereign' : 'text-slate-500 hover:text-white'
                    }`}
                  >
                    {mode === 'tier' ? <Crown size={10} /> : <ArrowDownAZ size={10} />}
                    {mode === 'tier' ? 'Tier' : 'Name'}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <button type="button" onClick={() => setActiveCategory(null)}
                className={`px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all ${
                  activeCategory === null ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-500 hover:text-white border border-slate-800'
                }`}>
                All ({catalogProducts.length})
              </button>
              {categories.map(cat => {
                const Icon = CATEGORY_ICON[cat] || Package;
                return (
                  <button key={cat} type="button" onClick={() => setActiveCategory(cat)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all ${
                      activeCategory === cat ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-500 hover:text-white border border-slate-800'
                    }`}>
                    <Icon size={11} /> {cat} ({catalogProducts.filter(p => normalizeCategory(p.category) === cat).length})
                  </button>
                );
              })}
            </div>
          </div>

          {catalogLoading && (
            <div className="flex items-center justify-center py-20 gap-3 text-slate-500">
              <Loader2 className="animate-spin" size={18} />
              <span className="text-xs font-black uppercase tracking-widest">Scanning Registry...</span>
            </div>
          )}
          {catalogError && (
            <div className="flex items-center justify-center py-20 gap-3 text-red-400">
              <AlertTriangle size={18} />
              <span className="text-xs font-black uppercase tracking-widest">Failed to load catalog.</span>
            </div>
          )}

          {!catalogLoading && !catalogError && (
            <div className="space-y-12">
              {catalogSections.map(section => {
                const Icon = CATEGORY_ICON[section.category] || Package;
                return (
                  <div key={section.category} className="space-y-5">
                    {!activeCategory && (
                      <div className="flex items-center gap-3 pb-3 border-b border-slate-800/60">
                        <div className="p-2 rounded-xl bg-slate-900 text-aura"><Icon size={14} /></div>
                        <h2 className="text-xs font-black uppercase tracking-widest text-white">{section.category}</h2>
                        <span className="text-[10px] font-bold text-slate-600">({section.items.length})</span>
                      </div>
                    )}
                    <div className="grid grid-cols-1 @[440px]:grid-cols-2 @[700px]:grid-cols-3 gap-5">
                      {section.items.map((product, i) => {
                        const PIcon = CATEGORY_ICON[normalizeCategory(product.category)] || Package;
                        const isPremium = product.tier === 'Enterprise+';
                        return (
                          <motion.div key={product.slug} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.02 }}>
                            <Card className={`relative h-full flex flex-col group transition-all p-6 ${isPremium ? 'border-highlight/40 hover:border-highlight/70 shadow-lg shadow-highlight/5' : 'hover:border-aura/50'}`}>
                              {isPremium && (
                                <div className="absolute -top-3 right-6 flex items-center gap-1 px-2.5 py-1 rounded-full bg-highlight text-sovereign text-[8px] font-black uppercase tracking-widest shadow-lg">
                                  <Crown size={9} /> Premium
                                </div>
                              )}
                              <div className="flex justify-between items-start mb-5">
                                <div className={`p-3 rounded-2xl transition-transform group-hover:scale-110 ${isPremium ? 'bg-highlight/10 text-highlight' : 'bg-slate-800/50 text-aura'}`}>
                                  <PIcon size={22} />
                                </div>
                                <span className="text-[9px] font-black px-2.5 py-1 rounded-full bg-slate-950 text-slate-500 border border-slate-900 uppercase tracking-widest text-right max-w-[110px] leading-tight">
                                  {product.category}
                                </span>
                              </div>
                              <h3 className="text-base font-black mb-1 text-white leading-tight">{product.name}</h3>
                              <p className="text-[9px] font-mono text-slate-600 uppercase mb-4 truncate">{product.slug}</p>
                              <div className="space-y-1.5 mb-5 flex-1">
                                {product.features.map(f => (
                                  <div key={f} className="flex items-center gap-2 text-[10px] font-bold text-slate-400">
                                    <span className="w-1 h-1 rounded-full bg-aura shrink-0" />
                                    {f}
                                  </div>
                                ))}
                              </div>
                              <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-800/50">
                                <Badge variant="outline" className={`font-black text-[9px] ${isPremium ? 'border-highlight/40 text-highlight' : 'border-slate-800 text-slate-400'}`}>
                                  {product.tier}
                                </Badge>
                                {product.route && (
                                  <button
                                    type="button"
                                    onClick={() => navigate(product.route!)}
                                    className="flex items-center gap-1.5 px-3 py-1.5 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all text-[9px] uppercase tracking-widest"
                                  >
                                    Open <ExternalLink size={10} />
                                  </button>
                                )}
                              </div>
                            </Card>
                          </motion.div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
              {filteredCatalog.length === 0 && (
                <p className="text-xs text-slate-500 italic text-center py-12">No products match the current filters.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
