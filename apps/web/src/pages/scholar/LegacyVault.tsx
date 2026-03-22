import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Database, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, Archive, Network, Binary, Clock, Server } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const LegacyVault: React.FC = () => {
  const [activeTab, setActiveTab] = useState('archives');

  const archives = [
    { id: 'arc-1', name: 'Planetary-Culture-Snapshot', date: '2026-03-21', type: 'Merkle-DAG', size: '14.2 PB', status: 'Locked' },
    { id: 'arc-2', name: 'Workstation-Genome-Root', date: '2026-01-01', type: 'PQC-Back-up', size: '1.2 TB', status: 'Immutable' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Legacy Vault</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Millennium-Scale Archival • Autonomous Replication Triggers</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><Archive size={18} /> Deep Storage</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Initialize Archive
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Database size={24} className="text-aura" />
                     Sovereign Archives
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="aura">Millennium-Proof</Badge>
                     <Badge color="emerald-500">PQC Sealed</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  {archives.map((arc, i) => (
                    <motion.div
                      key={arc.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all`}>
                             <Binary size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{arc.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{arc.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span>{arc.size}</span>
                             </div>
                          </div>
                       </div>
                       <Badge color={arc.status === 'Immutable' ? 'emerald-500' : 'aura'}>{arc.status}</Badge>
                    </motion.div>
                  ))}
               </div>
            </Card>

            <Card className="p-10 bg-vital/5 border-vital/20 space-y-8 relative overflow-hidden">
               <div className="absolute top-0 right-0 p-10 opacity-5">
                  <AlertCircle size={120} className="text-vital" />
               </div>
               <div className="flex items-center gap-4 text-vital">
                  <Activity size={24} />
                  <h3 className="text-2xl font-black uppercase tracking-tight">Replication Triggers</h3>
               </div>
               <p className="text-sm text-slate-400 font-bold leading-relaxed max-w-2xl">
                  Detected Civilization State: <span className="text-emerald-500 font-black">STABLE</span>.
                  <br/><br/>
                  Archival nodes are configured to autonomously trigger offspring spawning and legacy broadcasting upon detection of terrestrial civilisation collapse (Article 1150).
               </p>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6 border-t border-vital/10">
                  <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                     <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Trigger Condition</p>
                     <p className="text-xs font-black text-white uppercase">Sync-Loss > 14 Days</p>
                  </div>
                  <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900">
                     <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Target</p>
                     <p className="text-xs font-black text-white uppercase">Ceres-Seed-Relay</p>
                  </div>
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Clock size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Eternity Sync</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Synchronizing local state to off-world archival nodes via DTN. Verified durable for &ge;1,000 years.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10 text-[10px] font-black uppercase text-slate-500">
                  <div className="flex justify-between items-center">
                     <span>Last Orbital Sync</span>
                     <span className="text-white">2m ago</span>
                  </div>
                  <div className="flex justify-between items-center">
                     <span>Archival Health</span>
                     <span className="text-emerald-500">OPTIMAL</span>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                     <Server size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Storage Node</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Lunar-Lava-Tube-01</p>
                  </div>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
