import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { useStore, gaas } from '@workstation/shared';
import { Shield, Settings, Activity, Database, Cpu, Globe, Key, AlertTriangle, TrendingUp, DollarSign, PieChart, BarChart3, Users, Zap, Terminal, Heart } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const AdminPanel: React.FC = () => {
  const { systemVitals, currentRealm } = useStore();
  const [activeTab, setActiveTab] = useState('security');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">CFO & Entity Control</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Homeostatic Orchestrator • Profitability Ledger • Layer 5 Hardening</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><Activity size={18} /> UEG Export</Button>
           <Button className="bg-vital text-white shadow-xl shadow-vital/20"><AlertTriangle size={18} /> Emergency 888_HOLD</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
               <button onClick={() => setActiveTab('security')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'security' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Security</button>
               <button onClick={() => setActiveTab('economy')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'economy' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Economy</button>
               <button onClick={() => setActiveTab('cl1')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'cl1' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>CL1 Vitals</button>
            </div>

            <AnimatePresence mode="wait">
               {activeTab === 'security' && (
                 <motion.div key="security" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-10">
                    <Card className="p-10">
                       <h3 className="text-2xl font-black mb-10 flex items-center gap-4 uppercase tracking-tight">
                          <Shield size={28} className="text-aura" />
                          ASI Hardening Posture
                       </h3>
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {[
                            { id: 'ASI-01', name: 'Goal Hijacking', status: 'Mitigated', color: 'text-emerald-500' },
                            { id: 'ASI-02', name: 'Tool Misuse', status: 'Mitigated', color: 'text-emerald-500' },
                            { id: 'ASI-04', name: 'Supply Chain', status: 'Hardened', color: 'text-aura' },
                            { id: 'ASI-06', name: 'Negotiation', status: 'Monitoring', color: 'text-yellow-500' },
                          ].map((asi) => (
                            <div key={asi.id} className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                               <div className="flex items-center gap-5">
                                  <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center text-slate-700 font-black text-[10px] group-hover:text-aura transition-colors">#{asi.id.split('-')[1]}</div>
                                  <span className="text-xs font-black text-white uppercase tracking-widest">{asi.name}</span>
                               </div>
                               <Badge color={asi.color.includes('emerald') ? 'emerald-500' : 'aura'}>{asi.status}</Badge>
                            </div>
                          ))}
                       </div>
                    </Card>
                 </motion.div>
               )}

               {activeTab === 'economy' && (
                 <motion.div key="economy" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-10">
                    <Card className="p-10 space-y-10">
                       <div className="flex justify-between items-center">
                          <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                             <TrendingUp size={24} className="text-aura" />
                             Profitability Ledger
                          </h3>
                          <Badge color="emerald-500">Independence Certified</Badge>
                       </div>

                       <div className="h-64 flex items-end gap-2 px-4">
                          {[30, 45, 60, 55, 80, 75, 90, 85, 100, 95, 110, 120].map((h, i) => (
                            <motion.div
                              key={i}
                              initial={{ height: 0 }}
                              animate={{ height: `${h / 1.5}%` }}
                              className={`flex-1 rounded-t-xl ${i > 10 ? 'bg-aura shadow-[0_0_15px_rgba(100,255,218,0.3)]' : 'bg-slate-800'}`}
                            />
                          ))}
                       </div>

                       <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                          <div className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900">
                             <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Total Revenue</p>
                             <p className="text-2xl font-black text-white">1.42M <span className="text-aura text-xs">WST</span></p>
                          </div>
                          <div className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900">
                             <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Operating Costs</p>
                             <p className="text-2xl font-black text-white">420K <span className="text-aura text-xs">WST</span></p>
                          </div>
                          <div className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900">
                             <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Net Profit (6m)</p>
                             <p className="text-2xl font-black text-emerald-500">+1.0M <span className="text-emerald-500 text-xs">WST</span></p>
                          </div>
                       </div>
                    </Card>
                 </motion.div>
               )}

               {activeTab === 'cl1' && (
                 <motion.div key="cl1" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-10">
                    <Card className="p-10 flex flex-col items-center text-center gap-10">
                       <div className="relative">
                          <div className="w-64 h-64 rounded-full border-8 border-slate-900 border-t-aura flex items-center justify-center animate-pulse-slow">
                             <div className="text-center">
                                <p className="text-6xl font-black text-white">12.5x</p>
                                <p className="text-[10px] font-black text-aura uppercase tracking-widest">Efficiency Multiplier</p>
                             </div>
                          </div>
                          <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 20, ease: "linear" }} className="absolute -inset-4 border-2 border-dashed border-aura/20 rounded-full" />
                       </div>
                       <div className="space-y-4">
                          <h3 className="text-2xl font-black text-white uppercase tracking-tight">Parallel Bio-Compute</h3>
                          <p className="text-sm text-slate-400 font-bold leading-relaxed max-w-lg">
                             20% of total inference is currently offloaded to parallel CL1 units, achieving 10x energy reduction per token vs GPU baseline.
                          </p>
                       </div>
                       <Button className="px-12 py-5 bg-aura text-sovereign font-black rounded-2xl uppercase tracking-widest">Toggle CL1 Scaling</Button>
                    </Card>
                 </motion.div>
               )}
            </AnimatePresence>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-4 text-aura">
                  <Key size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">PQC & Cryptography</h4>
               </div>
               <div className="space-y-4">
                  <div className="flex justify-between items-center p-4 rounded-2xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Algorithm</span>
                     <span className="text-xs font-black text-white">Kyber-1024</span>
                  </div>
                  <div className="flex justify-between items-center p-4 rounded-2xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Signature</span>
                     <span className="text-xs font-black text-white">Dilithium-5</span>
                  </div>
               </div>
               <Badge color="emerald-500" className="w-full text-center py-2">NIST Standards Compliant</Badge>
            </Card>

            <Card className="p-10 space-y-6 bg-slate-950 border-slate-900">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Enterprise SLAs</h4>
               <div className="space-y-4">
                  {[
                    { label: 'Uptime', value: '99.99%', color: 'emerald-500' },
                    { label: 'Latency', value: '18ms', color: 'aura' },
                    { label: 'Resolution', value: '2.4m', color: 'highlight' },
                  ].map(sla => (
                    <div key={sla.label} className="flex justify-between items-center">
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{sla.label}</span>
                       <span className={`text-xs font-black text-${sla.color}`}>{sla.value}</span>
                    </div>
                  ))}
               </div>
            </Card>

            <Card className="p-8 border-slate-800 flex items-center gap-6">
               <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                  <PieChart size={28} />
               </div>
               <div>
                  <h4 className="text-lg font-black text-white mb-1">Resource Split</h4>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">80% GPU / 20% CL1</p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
