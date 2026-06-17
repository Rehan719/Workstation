import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented, toast } from '@workstation/ui';
import { Globe, FileText, Send, ShieldCheck, History, Info, ChevronRight, Zap, Globe2, AlertCircle, Plus, Network, Gavel, Scale } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, gaas } from '@workstation/shared';
import { ethers } from 'ethers';

export const TreatyDashboard: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('active');

  const alliances = [
    { id: 'al-1', name: 'Open-Sovereign-Federation', status: 'Active', members: 12, trust: 0.98, type: 'Security' },
    { id: 'al-2', name: 'Global-Data-Common', status: 'Proposed', members: 42, trust: 0.85, type: 'Economy' },
    { id: 'al-3', name: 'Research-Guild-X', status: 'Active', members: 8, trust: 0.99, type: 'Scholarship' },
  ];

   const [treaties, setTreaties] = useState([
    { id: 'tr-142', name: 'L11-Mesh-Syndication', status: 'Ratified', hash: 'e8a9b1c2...', date: '2026-03-20', network: 'Polygon' },
    { id: 'tr-219', name: 'Sovereign-Data-Handshake', status: 'Review', hash: 'd4f5g6h7...', date: '2026-03-21', network: 'Polygon' },
  ]);

  const handleProposeTreaty = async () => {
     try {
        // v0.2: Real Ethereum Testnet Integration Simulation (Article 1108)
        const provider = new ethers.BrowserProvider((window as any).ethereum);
        const signer = await provider.getSigner();
        const address = await signer.getAddress();

        const validation = await gaas.validateAction('TREATY_PROPOSAL', user?.did || 'anon', { wallet: address });
        if (!validation.valid) { toast("GaaS Blocked — Treaty proposal denied."); return; }

        const newTreaty = {
           id: `tr-${Math.floor(Math.random()*1000)}`,
           name: 'New Federated Treaty',
           status: 'Pending',
           hash: '0x' + Math.random().toString(16).slice(2, 10),
           date: new Date().toISOString().split('T')[0],
           network: 'Ethereum-Sepolia'
        };

        setTreaties([newTreaty, ...treaties]);
        toast(`Treaty Proposed — Article 1108 compliance verified for ${address.slice(0, 8)}...`);
     } catch (err) {
        console.error("Blockchain error:", err);
        toast("Wallet Connection Required — Connect a web3 wallet to propose treaties.");
     }
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Diplomacy Hub</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Inter-Civilization Treaties & Alliances • Layer 11 Civilisation</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Archive')} variant="outline"><History size={18} /> Archive</Button>
           <Button onClick={handleProposeTreaty} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Propose Treaty
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <div className="@[440px]:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Gavel size={28} className="text-aura" />
                     Sovereign Treaties
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('active')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'active' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Active</button>
                     <button onClick={() => setActiveTab('alliances')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'alliances' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Alliances</button>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     {activeTab === 'active' ? (
                       <motion.div key="treaties" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                          {treaties.map((tr, i) => (
                            <div key={tr.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer">
                               <div className="flex items-center gap-8">
                                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                                     <FileText size={24} />
                                  </div>
                                  <div>
                                     <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{tr.name}</p>
                                     <div className="flex items-center gap-4">
                                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">ID: {tr.id} • {tr.date}</span>
                                        <Badge color="emerald-500">{tr.network}</Badge>
                                     </div>
                                  </div>
                               </div>
                               <div className="flex items-center gap-6">
                                  <Badge color={tr.status === 'Ratified' ? 'emerald-500' : 'highlight'}>{tr.status}</Badge>
                                  <Button onClick={() => notImplemented('View Terms')} variant="outline" className="px-6 py-3">View Terms</Button>
                               </div>
                            </div>
                          ))}
                       </motion.div>
                     ) : (
                       <motion.div key="alliances" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                          {alliances.map((al, i) => (
                            <div key={al.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer">
                               <div className="flex items-center gap-8">
                                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                                     <Globe size={24} />
                                  </div>
                                  <div>
                                     <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{al.name}</p>
                                     <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                        <span>{al.members} Members</span>
                                        <Badge color="aura">{al.type}</Badge>
                                     </div>
                                  </div>
                               </div>
                               <div className="text-right flex items-center gap-6">
                                  <div>
                                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Trust Score</p>
                                     <p className="text-xl font-black text-white">{al.trust * 100}%</p>
                                  </div>
                                  <ChevronRight size={24} className="text-slate-800 group-hover:text-aura transition-colors" />
                               </div>
                            </div>
                          ))}
                       </motion.div>
                     )}
                  </AnimatePresence>
               </div>
            </Card>

            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950/40 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     Alliance Network Graph
                     <Badge color="aura">L11-Discovery</Badge>
                  </h3>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Inter-Civilization Treaty Handshake Map</p>
               </div>
               <Network size={240} className="text-aura opacity-20 animate-pulse-slow group-hover:scale-110 transition-transform duration-1000" />
            </Card>
         </div>

         <div className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <ShieldCheck size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Diplomacy Engine</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Autonomous treaty negotiation and alliance management powered by Article 1117 mandates.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Negotiations</span>
                     <span className="text-white">Active</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Success Rate</span>
                     <span className="text-emerald-500">92%</span>
                  </div>
               </div>
               <Button onClick={() => notImplemented('Initialize Handshake')} className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs">Initialize Handshake</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                     <Scale size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Smart Enforcement</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Polygon Mainnet Active</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
