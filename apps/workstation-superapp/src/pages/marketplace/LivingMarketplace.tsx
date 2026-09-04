import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  Search, Package, Loader2, AlertTriangle,
  Crown, Boxes, Layers, Globe2, ExternalLink, ArrowDownAZ, X,
} from 'lucide-react';
import { Card, Badge } from '@workstation/ui';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { apiJson, errorMessage, provenanceBadge } from '../../lib/api';

// ── Types ─────────────────────────────────────────────────────────────────────
//
// The Living Marketplace is the §12 economy surface. Two distinct layers:
//
//   1. CATALOGUE (/api/v1/catalog/products) — the platform's LIVE registered products. Every entry
//      is a real, openable capability.
//   2. LISTINGS (/api/v1/marketplace/listings) — what someone has actually PRICED for virtual-WST
//      trade. Purchases run through the real token ledger and return a real receipt.
//
// W392 — an earlier round left layer 2 unwired, noting the listings economy was Owner-gated and
// must not be "seeded with invented sales/trust figures". That was the right call at the time: the
// backend was auto-writing six fabricated listings at boot (invented products, invented prices,
// certified: true asserted by nobody). The Owner has since decided to wire it ON REAL DATA, so the
// fabricated seeds were retired and listings now derive from the real catalogue — unpriced and
// uncertified, because nobody has priced or certified them. Money here stays virtual WST; no
// real-money rail is involved.

interface CatalogProduct {
  slug: string;
  name: string;
  tier: string;
  category: string;
  features: string[];
  source: string | null;
  route: string | null;
}

// W392 — the TRADEABLE layer. The catalogue above says what exists; a listing says what someone has
// priced for virtual-WST trade. The two are deliberately not merged: a catalogue-derived listing is
// unpriced (origin 'catalog', price_wst 0) and would only duplicate the grid above, so this section
// shows what is genuinely purchasable and says so plainly when nothing is.
interface Listing {
  id: string;
  name: string;
  description: string;
  author: string;
  category: string;
  price_wst: number;
  tier: string;
  certified: boolean;
  status: string;
  sales_count: number;
  origin: string;
  route: string;
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

  const [listings, setListings] = useState<Listing[]>([]);
  const [listingsError, setListingsError] = useState('');
  const [buying, setBuying] = useState<string | null>(null);
  const [receipt, setReceipt] = useState<string>('');

  useEffect(() => {
    axios.get('/api/v1/catalog/products')
      .then(r => setCatalogProducts(r.data.products))
      .catch(() => setCatalogError(true))
      .finally(() => setCatalogLoading(false));
  }, []);

  const loadListings = () => {
    apiJson<Listing[]>('/api/v1/marketplace/listings')
      .then(d => { setListings(Array.isArray(d) ? d : []); setListingsError(''); })
      .catch(e => setListingsError(errorMessage(e)));
  };
  useEffect(loadListings, []);

  // Only what someone has actually priced is purchasable. A §11-held listing never reaches the
  // client — the backend filters it — so nothing here can offer a compliance-failed item.
  const tradeable = listings.filter(l => l.price_wst > 0 && l.status !== 'held');
  // W444 — unpriced listings were hidden entirely, so the PATCH that could ever price one had
  // no possible surface and the §12 tradeable economy was structurally empty forever. All
  // listings render now; unpriced ones are badged, and the detail drawer hosts edit/delete.
  const [drawerId, setDrawerId] = useState<string | null>(null);

  const purchase = async (l: Listing) => {
    setBuying(l.id);
    setListingsError('');
    setReceipt('');
    try {
      // Field names taken from a real response, not assumed: the server returns receipt_id,
      // listing_name, quantity, total_cost_wst and status.
      const res = await apiJson<{
        receipt_id?: string; listing_name?: string; quantity?: number;
        total_cost_wst?: number; status?: string;
      }>(`/api/v1/marketplace/listings/${l.id}/purchase`, { method: 'POST', body: { quantity: 1 } });
      const cost = res.total_cost_wst ?? l.price_wst;
      setReceipt(
        `${res.status === 'confirmed' ? 'Confirmed' : res.status ?? 'Recorded'}: ` +
        `${res.quantity ?? 1} × "${res.listing_name ?? l.name}" for ${cost.toLocaleString()} WST (virtual).` +
        (res.receipt_id ? ` Receipt ${res.receipt_id}.` : ''),
      );
      loadListings();
    } catch (e) {
      // 409 sold-out and 409 §11-held are real outcomes, not glitches — show what the server said.
      setListingsError(errorMessage(e));
    } finally {
      setBuying(null);
    }
  };

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

      {/* ── Tradeable listings (virtual WST) ──────────────────────────────────────
          Separate from the catalogue above on purpose: the catalogue says what EXISTS,
          this says what someone has PRICED. Nothing is presented as certified unless the
          listing actually carries a certification, and an empty state says why. */}
      <section className="border-t border-slate-800/60 pt-8">
        <h2 className="text-lg font-black uppercase tracking-tight text-white italic">
          Listings <span className="text-aura">· virtual WST</span>
        </h2>
        <p className="text-slate-500 text-xs font-semibold mt-2 max-w-2xl leading-relaxed">
          Priced for trade in virtual WST. Money here is simulated — no real-money rail is involved.
          Catalogue entries above are registered but unpriced, so they are not listed here.
        </p>

        {listingsError && (
          <div role="alert" className="mt-4 flex items-start gap-2 rounded-xl border border-vital/30 bg-vital/10 px-3 py-2">
            <AlertTriangle size={12} className="text-vital shrink-0 mt-0.5" />
            <p className="text-[10px] font-bold text-vital leading-relaxed">{listingsError}</p>
          </div>
        )}
        {receipt && (
          <div role="status" className="mt-4 rounded-xl border border-aura/30 bg-aura/10 px-3 py-2">
            <p className="text-[10px] font-bold text-aura leading-relaxed">{receipt}</p>
          </div>
        )}

        {/* W444 refuter lesson: the smoke needle must anchor on text that renders in EVERY
            state — this hint line is permanent, not conditional on what happens to be priced. */}
        {listings.length > 0 && (
          <p className="text-[10px] text-slate-500 font-bold mt-2">
            Open any listing to set its price (virtual WST), edit it, or get an AI valuation.
          </p>
        )}
        {listings.length === 0 ? (
          <p className="text-xs text-slate-500 italic py-8">No listings are registered.</p>
        ) : (
          <>
            {tradeable.length === 0 && (
              <p className="text-xs text-slate-500 italic py-3">
                Nothing is priced for trade yet — {listings.length} catalogue {listings.length === 1 ? 'entry is' : 'entries are'} registered
                but unpriced — nobody has set a WST price, so none is offered for sale yet.
              </p>
            )}
            <div className="grid grid-cols-1 @[700px]:grid-cols-2 @[1100px]:grid-cols-3 gap-4 mt-5">
              {listings.map(l => (
                <Card key={l.id} className="p-4 flex flex-col gap-2 border-slate-800 cursor-pointer hover:border-slate-700 transition-colors"
                  onClick={() => setDrawerId(l.id)}>
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-sm font-black text-white leading-tight">{l.name}</h3>
                    <div className="flex items-center gap-1.5 shrink-0">
                      {l.certified && <Badge className="text-[8px]">Certified</Badge>}
                      {!(l.price_wst > 0) && <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">unpriced — not for sale</span>}
                    </div>
                  </div>
                  <p className="text-[10px] text-slate-500 font-semibold leading-relaxed line-clamp-3">{l.description}</p>
                  <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-widest text-slate-600">
                    <span>{l.category}</span><span>·</span><span>{l.author}</span>
                    {l.sales_count > 0 && <><span>·</span><span>{l.sales_count} sold</span></>}
                  </div>
                  <div className="flex items-center justify-between gap-2 mt-1">
                    <span className="text-sm font-black text-aura">{l.price_wst > 0 ? `${l.price_wst.toLocaleString()} WST` : '—'}</span>
                    {l.price_wst > 0 && l.status !== 'held' ? (
                      <button
                        type="button"
                        onClick={e => { e.stopPropagation(); purchase(l); }}
                        disabled={buying === l.id || l.status === 'sold_out'}
                        className="px-3 py-1.5 bg-aura text-sovereign font-black rounded-xl text-[9px] uppercase tracking-widest disabled:opacity-40 hover:scale-105 transition-all"
                      >
                        {buying === l.id ? <Loader2 size={10} className="animate-spin" />
                          : l.status === 'sold_out' ? 'Sold out' : 'Purchase'}
                      </button>
                    ) : (
                      <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">details →</span>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </>
        )}
      </section>

      {drawerId && (
        <ListingDrawer id={drawerId} onClose={() => { setDrawerId(null); loadListings(); }} />
      )}
    </div>
  );
};

// ── W444 — listing detail drawer: the GET-by-id, PATCH (pricing/editing) and DELETE ops had no
// surface; the §11 compliance verdicts stored on every listing were invisible; and the AI
// valuation helper ships with the provenance badge (a floor scaffold is refused server-side).
const ListingDrawer: React.FC<{ id: string; onClose: () => void }> = ({ id, onClose }) => {
  const [detail, setDetail] = useState<any>(null);
  const [dErr, setDErr] = useState('');
  const [edit, setEdit] = useState<{ name: string; description: string; price_wst: number } | null>(null);
  const [busy, setBusy] = useState('');
  const [notice, setNotice] = useState('');
  const [held, setHeld] = useState(false);
  const [valuation, setValuation] = useState<any>(null);

  const load = () =>
    apiJson<any>(`/api/v1/marketplace/listings/${id}`)
      .then(d => { setDetail(d); setEdit({ name: d.name, description: d.description, price_wst: d.price_wst }); setDErr(''); })
      .catch(e => setDErr(errorMessage(e)));
  useEffect(() => { load(); }, [id]);

  const save = async () => {
    if (!edit) return;
    setBusy('save'); setNotice(''); setDErr(''); setHeld(false);
    try {
      const d = await apiJson<any>(`/api/v1/marketplace/listings/${id}`, { method: 'PATCH', body: edit });
      setDetail(d); setHeld(d.status === 'held');
      setNotice(d.status === 'held' ? '' : 'Saved — the public text was re-screened (§11) and stays live.');
    } catch (e) { setDErr(errorMessage(e)); }
    setBusy('');
  };

  const remove = async () => {
    if (!window.confirm('Delete this listing? A listing with recorded sales is retired to draft instead (its receipts keep resolving).')) return;
    setBusy('del'); setDErr('');
    try {
      const d = await apiJson<any>(`/api/v1/marketplace/listings/${id}`, { method: 'DELETE' });
      setNotice(d.retired_to_draft ? String(d.note) : 'Listing deleted.');
      if (!d.retired_to_draft) { onClose(); return; }
      load();
    } catch (e) { setDErr(errorMessage(e)); }
    setBusy('');
  };

  const getValuation = async () => {
    setBusy('val'); setDErr(''); setValuation(null);
    try {
      const d = await apiJson<any>('/api/v1/marketplace/value', {
        method: 'POST',
        body: { title: detail?.name ?? '', description: detail?.description ?? '', domain: detail?.category ?? 'general' },
      });
      setValuation(d);
    } catch (e) { setDErr(errorMessage(e)); }   // the 503 floor-refusal is the guard working — shown verbatim
    setBusy('');
  };

  const badge = valuation ? provenanceBadge(valuation.served_by, valuation.is_external) : null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/50" onClick={onClose}>
      <div className="w-full max-w-lg h-full overflow-y-auto bg-slate-950 border-l border-slate-800 p-6 space-y-4"
        onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-lg font-black text-white leading-tight">{detail?.name ?? '…'}</h3>
          <button type="button" onClick={onClose} className="text-slate-500 hover:text-white text-xs font-black uppercase">close</button>
        </div>
        {dErr && (
          <div role="alert" className="flex items-start gap-2 rounded-xl border border-vital/30 bg-vital/10 px-3 py-2">
            <AlertTriangle size={12} className="text-vital shrink-0 mt-0.5" />
            <p className="text-[10px] font-bold text-vital leading-relaxed">{dErr}</p>
          </div>
        )}
        {held && (
          <div role="alert" className="rounded-xl border border-amber-500/40 bg-amber-500/10 px-3 py-2">
            <p className="text-[10px] font-bold text-amber-400 leading-relaxed">§11 screen FAIL — this edit put the listing on hold, off the marketplace, until a clean re-screen.</p>
          </div>
        )}
        {notice && <p role="status" className="text-[10px] font-bold text-aura">{notice}</p>}
        {detail && edit && (
          <>
            <div className="grid grid-cols-2 gap-2 text-[10px]">
              {[['status', detail.status], ['origin', detail.origin], ['author', detail.author],
                ['category', detail.category], ['tier', detail.tier], ['sales', String(detail.sales_count)],
                ['vsb', detail.vsb_id || '—'], ['certified', detail.certified ? 'yes' : 'no']].map(([k, v]) => (
                <p key={k as string}><span className="font-black uppercase tracking-widest text-slate-600">{k}:</span> <span className="text-slate-300 font-bold">{v as string}</span></p>
              ))}
            </div>
            {/* W444 refuter catch: an EMPTY compliance dict rendered an unnamed amber verdict
                pill — implying a screen ran. Only a screen that produced an overall verdict renders. */}
            {detail.compliance?.overall && (
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1.5">§11 compliance screen</p>
                <p className="text-[10px] font-bold mb-1">
                  <span className={`px-1.5 py-0.5 rounded text-[8px] font-black uppercase ${detail.compliance.overall === 'pass' ? 'bg-emerald-500/15 text-emerald-400' : detail.compliance.overall === 'fail' ? 'bg-vital/15 text-vital' : 'bg-amber-500/20 text-amber-400'}`}>{detail.compliance.overall}</span>
                </p>
                {(detail.compliance.verdicts || []).map((v: any, i: number) => (
                  <p key={i} className="text-[9px] text-slate-500">{v.framework}: <span className="text-slate-300">{v.status}</span></p>
                ))}
              </div>
            )}
            <div className="space-y-2">
              <p className="text-[9px] font-black uppercase tracking-widest text-slate-600">Edit listing (re-screens public text)</p>
              <input value={edit.name} onChange={e => setEdit({ ...edit, name: e.target.value })} aria-label="listing name"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
              <textarea value={edit.description} onChange={e => setEdit({ ...edit, description: e.target.value })} rows={3} aria-label="listing description"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
              <div className="flex items-end gap-2">
                <div>
                  <label className="text-[8px] font-black uppercase tracking-widest text-slate-600 block mb-1">Set price (WST, virtual; 0 = unpriced)</label>
                  <input type="number" min={0} value={edit.price_wst} onChange={e => setEdit({ ...edit, price_wst: Number(e.target.value) })}
                    aria-label="listing price"
                    className="w-32 bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white" />
                </div>
                <button type="button" onClick={save} disabled={busy === 'save'}
                  className="px-3 py-2 bg-aura text-sovereign font-black rounded-xl text-[9px] uppercase tracking-widest disabled:opacity-40">
                  {busy === 'save' ? 'Saving…' : 'Save'}
                </button>
                {detail.origin === 'user' && (
                  <button type="button" onClick={remove} disabled={busy === 'del'}
                    className="px-3 py-2 bg-vital/20 text-vital font-black rounded-xl text-[9px] uppercase tracking-widest disabled:opacity-40">
                    Delete listing
                  </button>
                )}
              </div>
              {detail.origin !== 'user' && (
                <p className="text-[9px] text-slate-600 italic">catalog-derived listing — it mirrors a registered platform product and cannot be deleted here (edit or unprice it instead)</p>
              )}
            </div>
            <div className="pt-2 border-t border-slate-900">
              <button type="button" onClick={getValuation} disabled={busy === 'val'}
                className="px-3 py-2 bg-slate-900 border border-slate-800 text-slate-300 font-black rounded-xl text-[9px] uppercase tracking-widest disabled:opacity-40">
                {busy === 'val' ? 'Valuing…' : 'Get AI valuation'}
              </button>
              <p className="text-[9px] text-slate-600 mt-1">Advisory only — nothing is auto-priced; a floor-only backend refuses rather than fabricating a valuation.</p>
              {valuation && badge && (
                <div className="mt-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${badge.cls}`} title={badge.title}>{badge.label}</span>
                  <pre className="text-[10px] text-slate-300 whitespace-pre-wrap max-h-48 overflow-y-auto mt-1.5">{valuation.valuation}</pre>
                  <p className="text-[9px] text-amber-400/80 italic mt-1">{valuation.disclaimer}</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};
