import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Copy, RefreshCw, Plus, Share2 } from 'lucide-react';

export const TwinManagement: React.FC = () => {
  const [twins, setTwins] = useState<any[]>([]);
  const [activeBlueprint, setActiveBlueprint] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v210/federation/twins').then(res => setTwins(res.data));
  }, []);

  const handleSpawn = async () => {
    const node = prompt("Enter Node ID to spawn twin:");
    if (!node) return;
    const res = await axios.post(`/api/v210/federation/spawn-twin?node_id=${node}`);
    setTwins([...twins, res.data]);
  };

  const handleInspect = async (id: string) => {
    const res = await axios.get(`/api/v220/twin/blueprint/${id}`);
    setActiveBlueprint(res.data);
  };

  const handleSyncNow = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    setTwins(prev => prev.map(t => t.id === id ? { ...t, status: 'synced', last_sync: 'just now' } : t));
  };

  return (
    <div className="space-y-10">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black mb-2 break-words">Digital Twin Management</h1>
          <p className="text-slate-500">Replicating application state and epigenetic memory across the federation.</p>
        </div>
        <button
          onClick={handleSpawn}
          className="flex items-center gap-2 px-6 py-3 bg-aura text-sovereign font-bold rounded-xl hover:scale-105 transition-all"
        >
          <Plus size={18} />
          Spawn Twin
        </button>
      </header>

      {activeBlueprint && (
        <div className="p-8 mb-10 bg-aura/5 border border-aura/20 rounded-3xl animate-in fade-in slide-in-from-top-4">
           <div className="flex justify-between items-start mb-6">
             <h3 className="text-2xl font-black">Ecosystem Blueprint: {activeBlueprint.id}</h3>
             <button onClick={() => setActiveBlueprint(null)} className="text-slate-500 hover:text-white">&times;</button>
           </div>
           <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase">Genomic Profile</p>
                <p className="font-bold">{activeBlueprint.genomic_profile}</p>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase">Memory size</p>
                <p className="font-bold">{activeBlueprint.epigenetic_memory_size}</p>
              </div>
              <div className="col-span-2">
                <p className="text-[10px] font-black text-slate-500 uppercase">Active Reactors</p>
                <p className="font-bold">{activeBlueprint.active_reactors.join(', ')}</p>
              </div>
           </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-3 gap-8">
        {twins.map(t => (
          <div key={t.id} onClick={() => handleInspect(t.node)} className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm space-y-6 cursor-pointer hover:border-aura/50 transition-all">
            <div className="flex justify-between items-start">
              <div className="p-3 bg-aura/10 text-aura rounded-xl">
                <Copy size={24} />
              </div>
              <span className={`text-[10px] font-black uppercase px-2 py-1 rounded ${
                t.status === 'synced' ? 'bg-vital/10 text-vital' : 'bg-rose-500/10 text-rose-500'
              }`}>
                {t.status}
              </span>
            </div>

            <div>
              <h3 className="text-xl font-bold">{t.node}</h3>
              <p className="text-xs text-slate-500 font-mono mt-1">{t.id}</p>
            </div>

            <div className="pt-6 border-t border-slate-800 flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
               <span>Last Sync: {t.last_sync}</span>
               <button type="button" onClick={(e) => handleSyncNow(e, t.id)} className="flex items-center gap-1 text-aura hover:underline">
                 <RefreshCw size={12} />
                 Sync Now
               </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
