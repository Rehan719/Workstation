import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Gavel, Scale, FileText, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, Send, Terminal, Database, Fingerprint } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const LawHub: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('constitution');

  const articles = [
    { id: '1122', title: 'Patient Sovereignty', status: 'Ratified', category: 'Care' },
    { id: '1126', title: 'Compassionate AI Mandate', status: 'Active', category: 'Care' },
    { id: '1121', title: 'Open Source Leadership', status: 'Ratified', category: 'Civilisation' },
  ];

  const treaties = [
    { id: 'tr-42', name: 'Planetary-Mesh-Alliance', status: 'Ratified', participants: 100 },
    { id: 'tr-107', name: 'Data-Privacy-Handshake', status: 'Review', participants: 12 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">Hall of Justice</h1>
          <p className="text-blue-500 font-black uppercase text-[10px] tracking-[0.3em]">Sovereign Regulation • Constitutional Enforcement • Law Hub</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Audit Log</Button>
           <Button className="bg-blue-500 text-sovereign shadow-xl shadow-blue-500/20">
              <Plus size={18} /> Propose Amendment
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Gavel size={24} className="text-blue-500" />
                     Sovereign Jurisprudence
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('constitution')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'constitution' ? 'bg-slate-800 text-blue-500 shadow-lg' : 'text-slate-500 hover:text-white'}`}>Constitution</button>
                     <button onClick={() => setActiveTab('treaties')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'treaties' ? 'bg-slate-800 text-blue-500 shadow-lg' : 'text-slate-500 hover:text-white'}`}>Treaties</button>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     {activeTab === 'constitution' ? (
                       <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                          {articles.map((art, i) => (
                            <div key={art.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-blue-500/30 transition-all cursor-pointer">
                               <div className="flex items-center gap-8">
                                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-500 group-hover:bg-blue-500 group-hover:text-sovereign transition-all">
                                     <FileText size={24} />
                                  </div>
                                  <div>
                                     <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{art.title}</p>
                                     <div className="flex items-center gap-4">
                                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Article {art.id}</span>
                                        <Badge color="blue-500">{art.category}</Badge>
                                     </div>
                                  </div>
                               </div>
                               <div className="flex items-center gap-6">
                                  <Badge color={art.status === 'Ratified' ? 'emerald-500' : 'highlight'}>{art.status}</Badge>
                                  <button className="p-4 bg-slate-900 border border-slate-800 rounded-2xl text-slate-500 hover:text-blue-500 transition-all"><ChevronRight size={20} /></button>
                               </div>
                            </div>
                          ))}
                       </motion.div>
                     ) : (
                       <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                          {treaties.map((tr, i) => (
                            <div key={tr.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-blue-500/30 transition-all cursor-pointer">
                               <div className="flex items-center gap-8">
                                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-500 group-hover:bg-blue-500 group-hover:text-sovereign transition-all">
                                     <Scale size={24} />
                                  </div>
                                  <div>
                                     <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{tr.name}</p>
                                     <div className="flex items-center gap-4">
                                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{tr.participants} Sovereign Nodes</span>
                                     </div>
                                  </div>
                               </div>
                               <div className="flex items-center gap-6">
                                  <Badge color="emerald-500">{tr.status}</Badge>
                                  <Button variant="outline" className="px-6 py-3">View Terms</Button>
                               </div>
                            </div>
                          ))}
                       </motion.div>
                     )}
                  </AnimatePresence>
               </div>
            </Card>

            <Card className="p-10 bg-blue-500/5 border-blue-500/20 flex flex-col items-center text-center gap-6 relative overflow-hidden">
               <div className="absolute top-0 left-0 p-10 opacity-5 text-blue-500">
                  <Scale size={120} />
               </div>
               <div className="w-20 h-20 rounded-3xl bg-blue-500 flex items-center justify-center text-sovereign shadow-2xl shadow-blue-500/20 relative z-10">
                  <ShieldCheck size={40} />
               </div>
               <div className="space-y-2 relative z-10">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight">GaaS Validation Active</h3>
                  <p className="text-sm text-slate-400 font-bold max-w-xl">
                     Every system action is automatically validated against the 1,127 articles of the Workstation Constitution. Zero bypass policy enforced by Layer 1.
                  </p>
               </div>
               <Button variant="outline" className="px-10 py-4 border-blue-500/30 text-blue-500 hover:bg-blue-500/10 relative z-10">Open Transparency Panel</Button>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-slate-950 border-slate-900">
               <div className="flex items-center gap-4 text-blue-500">
                  <Terminal size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Governance View</h4>
               </div>
               <div className="space-y-4 pt-6 border-t border-white/5">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Amendments</span>
                     <span className="text-white">Active (Article 1118)</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Council Status</span>
                     <span className="text-emerald-500">100% AI-LED</span>
                  </div>
               </div>
               <Button variant="outline" className="w-full text-[9px] py-2">Open Self-Modification UI</Button>
            </Card>

            <Card className="p-10 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Legal Markers</h4>
               <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">PQC_MANDATORY</span>
                     <Badge color="emerald-500">SET</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">AUDIT_STRICT</span>
                     <Badge color="blue-500">ACTIVE</Badge>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-500">
                     <Scale size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Compliance</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">ISO 42001 & EU AI Act</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
