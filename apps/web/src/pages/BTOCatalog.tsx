import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Package, ChevronRight, Settings2 } from 'lucide-react';

export const BTOCatalog: React.FC = () => {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/v180/products/')
      .then(res => {
        setProducts(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch products", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="animate-pulse flex space-x-4">Loading Catalog...</div>;

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Build-to-Order Catalog</h1>
        <p className="text-slate-500">Configure and deploy custom agentic infrastructure.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {products.map((product) => (
          <motion.div
            key={product.id}
            whileHover={{ y: -5 }}
            className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm flex flex-col"
          >
            <div className="flex justify-between items-start mb-6">
              <div className="p-4 rounded-2xl bg-highlight/10 text-highlight">
                <Package size={32} />
              </div>
              <span className="text-[10px] font-black px-3 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700 uppercase tracking-widest">
                {product.category}
              </span>
            </div>

            <h3 className="text-2xl font-black mb-3">{product.name}</h3>
            <p className="text-slate-400 text-sm mb-8 flex-1">{product.description}</p>

            <div className="flex items-center justify-between mt-auto">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Starting at</p>
                <p className="text-2xl font-black text-white">{product.basePrice.toLocaleString()} WST</p>
              </div>
              <button className="flex items-center gap-2 px-6 py-3 bg-aura text-sovereign font-bold rounded-xl hover:scale-105 transition-transform">
                <Settings2 size={18} />
                Configure
                <ChevronRight size={18} />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
