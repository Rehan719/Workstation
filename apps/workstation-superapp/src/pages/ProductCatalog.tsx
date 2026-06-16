import React, { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Package, Search, ExternalLink, Loader2, AlertTriangle, Boxes, Layers, Globe2, ArrowDownAZ, Crown } from 'lucide-react';
import { Card, Badge } from '@workstation/ui';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface CatalogProduct {
  slug: string;
  name: string;
  tier: string;
  category: string;
  features: string[];
  source: string | null;
  route: string | null;
}

const CATEGORY_ICON: Record<string, any> = {
  SDK: Boxes,
  Platform: Layers,
  Domain: Globe2,
};

// Collapses near-duplicate category labels (e.g. "Domain (Quran Education Platform)")
// into their parent group for sectioning/filtering, while the full original label
// still displays on the card itself.
const normalizeCategory = (category: string): string => category.split(' (')[0].trim();

// Highest-value tiers float to the top within a category/sort group.
const TIER_RANK: Record<string, number> = {
  'Enterprise+': 0,
  'Enterprise': 1,
  'Standard/Pro/Enterprise': 2,
  'Standard/Pro': 3,
  'Domain': 4,
};
const tierRank = (tier: string) => TIER_RANK[tier] ?? 5;

type SortMode = 'name' | 'tier';

export const ProductCatalog: React.FC = () => {
  const [products, setProducts] = useState<CatalogProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [sortMode, setSortMode] = useState<SortMode>('tier');
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('/api/v1/catalog/products')
      .then(resp => setProducts(resp.data.products))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  const categories = useMemo(
    () => Array.from(new Set(products.map(p => normalizeCategory(p.category)))).sort(),
    [products]
  );

  const sortProducts = (list: CatalogProduct[]) => {
    const sorted = [...list];
    if (sortMode === 'name') {
      sorted.sort((a, b) => a.name.localeCompare(b.name));
    } else {
      sorted.sort((a, b) => tierRank(a.tier) - tierRank(b.tier) || a.name.localeCompare(b.name));
    }
    return sorted;
  };

  const filtered = sortProducts(products.filter(p =>
    (!activeCategory || normalizeCategory(p.category) === activeCategory) &&
    (!search || p.name.toLowerCase().includes(search.toLowerCase()) || p.slug.toLowerCase().includes(search.toLowerCase()))
  ));

  // When no category filter is active, present the catalog grouped into sections
  // by category rather than one flat grid — this is the "categorized" view.
  const sections = useMemo(() => {
    if (activeCategory) return [{ category: activeCategory, items: filtered }];
    const byCategory = new Map<string, CatalogProduct[]>();
    filtered.forEach(p => {
      const key = normalizeCategory(p.category);
      byCategory.set(key, [...(byCategory.get(key) || []), p]);
    });
    return categories
      .filter(c => byCategory.has(c))
      .map(c => ({ category: c, items: byCategory.get(c)! }));
  }, [filtered, activeCategory, categories]);

  const renderCard = (product: CatalogProduct, i: number) => {
    const Icon = CATEGORY_ICON[normalizeCategory(product.category)] || Package;
    const isPremiumTier = product.tier === 'Enterprise+';
    return (
      <motion.div key={product.slug} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.02 }}>
        <Card className={`relative h-full flex flex-col group transition-all p-8 ${isPremiumTier ? 'border-highlight/40 hover:border-highlight/70 shadow-lg shadow-highlight/5' : 'hover:border-aura/50'}`}>
          {isPremiumTier && (
            <div className="absolute -top-3 right-6 flex items-center gap-1 px-2.5 py-1 rounded-full bg-highlight text-sovereign text-[8px] font-black uppercase tracking-widest shadow-lg">
              <Crown size={10} /> Premium
            </div>
          )}
          <div className="flex justify-between items-start mb-6">
            <div className={`p-4 rounded-2xl text-aura group-hover:scale-110 transition-transform ${isPremiumTier ? 'bg-highlight/10 text-highlight' : 'bg-slate-800/50'}`}>
              <Icon size={28} />
            </div>
            <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-slate-950 text-slate-500 border border-slate-900 uppercase tracking-widest text-right">
              {product.category}
            </span>
          </div>

          <h3 className="text-xl font-black mb-2 text-white">{product.name}</h3>
          <p className="text-[9px] font-mono text-slate-600 uppercase mb-6">{product.slug}</p>

          <div className="space-y-2 mb-6 flex-1">
            {product.features.map(f => (
              <div key={f} className="flex items-center gap-2 text-[10px] font-bold text-slate-400">
                <span className="w-1 h-1 rounded-full bg-aura shrink-0" />
                {f}
              </div>
            ))}
          </div>

          <div className="flex items-end justify-between mt-auto pt-6 border-t border-slate-800/50">
            <Badge variant="outline" className={`font-black text-[9px] ${isPremiumTier ? 'border-highlight/40 text-highlight' : 'border-slate-800 text-slate-400'}`}>{product.tier}</Badge>
            {product.route ? (
              <button
                type="button"
                onClick={() => navigate(product.route!)}
                className="flex items-center gap-2 px-4 py-2 bg-aura text-sovereign font-black rounded-xl hover:scale-105 transition-all text-[10px] uppercase tracking-widest"
              >
                Open <ExternalLink size={12} />
              </button>
            ) : (
              <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest italic">{product.source || 'Internal SDK'}</span>
            )}
          </div>
        </Card>
      </motion.div>
    );
  };

  return (
    <div className="space-y-12 pb-24">
      <header>
        <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Product <span className="text-aura">Catalog</span></h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Live Inventory • /products • {products.length} Registered</p>
      </header>

      <div className="flex flex-col gap-4">
        <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div className="flex items-center gap-3 px-4 py-3 bg-slate-900 border border-slate-800 rounded-2xl max-w-md">
            <Search size={16} className="text-slate-600 shrink-0" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search products..."
              className="bg-transparent outline-none text-xs text-white font-bold w-full"
            />
          </div>
          <div className="flex items-center gap-2 p-1 rounded-xl bg-slate-900 border border-slate-800">
            {sortMode === 'tier' ? (
              <button type="button" onClick={() => setSortMode('tier')} aria-pressed="true" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all bg-aura text-sovereign">
                <Crown size={11} /> Tier
              </button>
            ) : (
              <button type="button" onClick={() => setSortMode('tier')} aria-pressed="false" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all text-slate-500 hover:text-white">
                <Crown size={11} /> Tier
              </button>
            )}
            {sortMode === 'name' ? (
              <button type="button" onClick={() => setSortMode('name')} aria-pressed="true" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all bg-aura text-sovereign">
                <ArrowDownAZ size={11} /> Name
              </button>
            ) : (
              <button type="button" onClick={() => setSortMode('name')} aria-pressed="false" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-all text-slate-500 hover:text-white">
                <ArrowDownAZ size={11} /> Name
              </button>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveCategory(null)}
            className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeCategory === null ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-500 hover:text-white border border-slate-800'}`}
          >
            All ({products.length})
          </button>
          {categories.map(cat => {
            const Icon = CATEGORY_ICON[cat] || Package;
            const count = products.filter(p => normalizeCategory(p.category) === cat).length;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setActiveCategory(cat)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeCategory === cat ? 'bg-aura text-sovereign' : 'bg-slate-900 text-slate-500 hover:text-white border border-slate-800'}`}
              >
                <Icon size={12} /> {cat} ({count})
              </button>
            );
          })}
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-24 gap-3 text-slate-500">
          <Loader2 className="animate-spin" size={20} />
          <span className="text-xs font-black uppercase tracking-widest">Scanning Product Registry...</span>
        </div>
      )}

      {error && (
        <div className="flex items-center justify-center py-24 gap-3 text-vital">
          <AlertTriangle size={20} />
          <span className="text-xs font-black uppercase tracking-widest">Failed to load product catalog.</span>
        </div>
      )}

      {!loading && !error && (
        <div className="space-y-16">
          {sections.map(section => {
            const Icon = CATEGORY_ICON[section.category] || Package;
            return (
              <div key={section.category} className="space-y-6">
                {!activeCategory && (
                  <div className="flex items-center gap-3 pb-3 border-b border-slate-800/60">
                    <div className="p-2 rounded-xl bg-slate-900 text-aura">
                      <Icon size={16} />
                    </div>
                    <h2 className="text-sm font-black uppercase tracking-widest text-white">{section.category}</h2>
                    <span className="text-[10px] font-bold text-slate-600">({section.items.length})</span>
                  </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {section.items.map((product, i) => renderCard(product, i))}
                </div>
              </div>
            );
          })}
          {filtered.length === 0 && (
            <p className="text-xs text-slate-500 italic col-span-full text-center py-12">No products match the current filters.</p>
          )}
        </div>
      )}
    </div>
  );
};
