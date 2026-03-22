import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Heart, Activity, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, LayoutGrid, Terminal, Database, TrendingUp, HeartPulse, Microscope, Users, Phone, Video } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const CareHub: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('wellness');

  const vitals = [
    { label: 'Cognitive Resonance', value: '0.98', status: 'Optimal' },
    { label: 'Sleep Efficiency', value: '84%', status: 'Normal' },
    { label: 'Stress Index', value: '0.12', status: 'Low' },
  ];

  const interventions = [
    { id: 'i-1', name: 'Rest-Mode-Activation', type: 'Regulation', status: 'Completed', date: '2h ago' },
    { id: 'i-2', name: 'Compassionate-Response', type: 'AI-Care', status: 'Active', date: 'Now' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">Sanctuary of Compassion</h1>
          <p className="text-vital font-black uppercase text-[10px] tracking-[0.3em]">Compassionate AI • Article 1126 Care Mandate • Care Hub</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Wellness Log</Button>
           <Button className="bg-vital text-white shadow-xl shadow-vital/20">
              <Plus size={18} /> New Care Plan
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
               {vitals.map(v => (
                 <Card key={v.label} className="text-center group hover:border-vital/30 transition-all">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">{v.label}</p>
                    <p className="text-4xl font-black text-white mb-2">{v.value}</p>
                    <Badge color={v.status === 'Optimal' ? 'emerald-500' : 'vital'}>{v.status}</Badge>
                 </Card>
               ))}
            </div>

            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-vital/5 border-vital/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,82,82,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     Well-being Resonance
                     <Badge color="vital">Real-time</Badge>
                  </h3>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Biomimetic Health Monitoring • L4 Regulation</p>
               </div>

               <div className="relative w-full h-full flex items-center justify-center">
                  <HeartPulse size={200} className="text-vital opacity-20 animate-pulse-slow group-hover:scale-110 transition-transform duration-1000" />
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Activity size={24} className="text-vital" />
                     Care & Support
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('wellness')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'wellness' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Wellness</button>
                     <button onClick={() => setActiveTab('network')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'network' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Network</button>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                        {interventions.map((item, i) => (
                          <div key={item.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-vital/30 transition-all cursor-pointer">
                             <div className="flex items-center gap-8">
                                <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-vital group-hover:bg-vital group-hover:text-white transition-all">
                                   <Heart size={24} />
                                </div>
                                <div>
                                   <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{item.name}</p>
                                   <div className="flex items-center gap-4">
                                      <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{item.type} • {item.date}</span>
                                      <Badge color={item.status === 'Active' ? 'vital' : 'emerald-500'}>{item.status}</Badge>
                                   </div>
                                </div>
                             </div>
                             <Button variant="outline" className="px-6 py-3">Details</Button>
                          </div>
                        ))}
                     </motion.div>
                  </AnimatePresence>
               </div>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-vital/5 border-vital/20">
               <div className="w-16 h-16 rounded-2xl bg-vital flex items-center justify-center text-white shadow-xl shadow-vital/20">
                  <ShieldCheck size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Patient Sovereignty</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     All care-related data is owned by you, encrypted with your DID, and accessible only via Article 1122 consent protocols.
                  </p>
               </div>
               <Button className="w-full bg-vital text-white py-6 rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-vital/20">Manage Consent</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <div className="flex items-center gap-4 text-vital">
                  <Phone size={20} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Care Team</h4>
               </div>
               <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-900 border border-slate-800">
                     <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-500 font-bold text-[10px]">DA</div>
                        <span className="text-xs font-bold text-white">Dr. Alpha</span>
                     </div>
                     <Video size={16} className="text-slate-500 hover:text-vital cursor-pointer" />
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-900 border border-slate-800">
                     <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-500 font-bold text-[10px]">NA</div>
                        <span className="text-xs font-bold text-white">Nurse Agent</span>
                     </div>
                     <Phone size={16} className="text-slate-500 hover:text-vital cursor-pointer" />
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-vital">
                     <Microscope size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Care Analytics</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Optimized by GRN Inference</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
