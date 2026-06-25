import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  Search, Package, Loader2, AlertTriangle,
  Crown, Boxes, Layers, Globe2, ExternalLink, ArrowDownAZ, X,
} from 'lucide-react';
import { Card, Badge } from '@workstation/ui';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// ── Types ─────────────────────────────────────────────────────────────────────
//
// The Living Marketplace is the §12 economy surface. It presents the platform's
// LIVE registered products (from /api/v1/catalog/products) — every entry is a real,
// openable capability. (It deliberately holds NO fabricated trading data: a real
// VSB-to-VSB listing/orders economy is Owner-gated and will be built on real WST
// rails, not seeded with invented sales/trust figures.)

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

  const [catalogProducts, setCatalogProducts] = useState<CatalogProduct[]>([]);
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [catalogError, setCatalogError] = useState(false);
  const [productSearch, setProductSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [sortMode, setSortMode] = useState<SortMode>('tier');

  useEffect(() => {
    axios.get('/api/v1/catalog/products')
      .then(r => setCatalogProducts(r.data.products))
      .catch(() => setCatalogError(true))
      .finally(() => setCatalogLoading(false));
  }, []);

  // ── Derived ──────────────────────────────────────────────────────────────────

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

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-8 pb-10">

      <header>
        <h1 className="text-3xl @[440px]:text-4xl @[900px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">
          Living <span className="text-aura">Marketplace</span>
        </h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">
          Sovereign Economy · {catalogProducts.length} Live Products
        </p>
        <p className="text-slate-500 text-xs font-semibold mt-3 max-w-2xl leading-relaxed">
          The platform's registered products and capabilities — every entry runs on Workstation's own
          native AI fabric and opens to a live surface. Listings reflect what is actually built.
        </p>
      </header>

      {/* Controls */}
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
  );
};
