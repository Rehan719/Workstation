import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Download, CheckCircle, Database, Server, RefreshCw } from 'lucide-react';
import axios from 'axios';

export const ModelManager: React.FC = () => {
  const [models, setModels] = useState<any[]>([]);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    // Simulated model list from Ollama
    setModels([
      { id: 'llama3.2:3b', name: 'Llama 3.2 3B', size: '2.0 GB', description: 'Default fast model for v149.0.', status: 'installed' },
      { id: 'llama3.1:8b', name: 'Llama 3.1 8B', size: '4.7 GB', description: 'Advanced general purpose intelligence.', status: 'available' },
      { id: 'mistral:7b', name: 'Mistral 7B', size: '4.1 GB', description: 'High-performance open-source model.', status: 'available' },
      { id: 'phi3:3.8b', name: 'Phi-3 Mini', size: '2.3 GB', description: 'Microsoft specialized small model.', status: 'available' }
    ]);
  }, []);

  const handleDownload = (id: string) => {
    setDownloading(id);
    setTimeout(() => {
      setModels(models.map(m => m.id === id ? { ...m, status: 'installed' } : m));
      setDownloading(null);
    }, 3000);
  };

  return (
    <div className="space-y-10">
      <header>
        <h2 className="text-3xl font-black mb-2">Model Manager</h2>
        <p className="text-slate-500">Manage local AI intelligence via Ollama.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {models.map(m => (
          <div key={m.id} className={`p-8 glass-card border-white/5 ${m.status === 'installed' ? 'border-aura/30' : ''}`}>
             <div className="flex justify-between items-start mb-6">
                <div className={`p-4 rounded-2xl ${m.status === 'installed' ? 'bg-aura/10 text-aura' : 'bg-surface text-slate-500'}`}>
                   <Cpu size={28} />
                </div>
                <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 uppercase tracking-widest">
                   {m.size}
                </span>
             </div>
             <h3 className="text-xl font-bold mb-2">{m.name}</h3>
             <p className="text-xs text-slate-500 font-bold mb-8 leading-relaxed">{m.description}</p>

             <button
               onClick={() => handleDownload(m.id)}
               disabled={m.status === 'installed' || downloading === m.id}
               className={`w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${
                 m.status === 'installed'
                   ? 'bg-aura/10 text-aura border border-aura/20 cursor-default'
                   : 'bg-aura text-sovereign hover:scale-[1.02] shadow-lg shadow-aura/10'
               }`}
             >
               {downloading === m.id ? (
                 <>
                   <RefreshCw size={18} className="animate-spin" />
                   Downloading...
                 </>
               ) : m.status === 'installed' ? (
                 <>
                   <CheckCircle size={18} />
                   Active Engine
                 </>
               ) : (
                 <>
                   <Download size={18} />
                   Install Local Engine
                 </>
               )}
             </button>
          </div>
        ))}
      </div>
    </div>
  );
};
