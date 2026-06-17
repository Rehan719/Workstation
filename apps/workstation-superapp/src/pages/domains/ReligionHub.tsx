import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { BookOpen, Heart, Sparkles, MessageCircle, History, Info, ShieldCheck, Zap, Globe, HeartPulse, Network, Binary, Compass, Anchor, Wind, Layers, GraduationCap } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPFlagshipFeatures } from '../../components/QEPFlagshipFeatures';
import { LearnTeachModule } from '../../components/LearnTeachModule';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';

export const ReligionHub: React.FC = () => {
   const { layout, emotionalAdjustment } = useAdaptiveUI();
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('wisdom');

  const wisdoms = [
    { id: 'w-1', name: 'Universal Ethics v3', type: 'Moral Framework', status: 'Ratified', hash: 'e8a9b1...' },
    { id: 'w-2', name: 'Interfaith-Dialogue', type: 'Alliance', status: 'Active', hash: 'd4f5g6...' },
    { id: 'w-3', name: 'Compassionate-Inquiry', type: 'Protocol', status: 'Proposed', hash: 'a1b2c3...' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Spire of Inquiry</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Spiritual Inquiry • Ethical Guidance Channel • Religion Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Tradition')} variant="outline"><History size={18} /> Tradition</Button>
           <Button onClick={() => notImplemented('Seek Guidance')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Sparkles size={18} /> Seek Guidance
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <div className="@[440px]:col-span-8 space-y-10">
            <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-aura/5 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Sacred Knowledge Garden
                     <Badge color="aura">Wisdom-Mesh</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Global Spiritual Networks • Article 1126 Compassion Strict</p>
               </div>

               <div className="relative z-10 flex flex-col items-center gap-8">
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 60, ease: "linear" }}>
                     <Compass size={180} className="text-aura opacity-20" />
                  </motion.div>
                  <HeartPulse size={120} className="text-aura opacity-40 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse-slow" />
               </div>

               <div className="absolute bottom-10 right-10 flex gap-10 text-right">
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Active Alliances</p>
                     <p className="text-2xl font-black text-aura">42</p>
                  </div>
                  <div>
                     <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Moral Resonance</p>
                     <p className="text-2xl font-black text-aura">0.99</p>
                  </div>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <BookOpen size={24} className="text-aura" />
                     Scholarly Operations
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('wisdom')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'wisdom' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Wisdom</button>
                     <button onClick={() => setActiveTab('dialogue')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'dialogue' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Dialogue</button>
                     <button onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
                  </div>
               </div>

               <div className="space-y-4">
                  {activeTab === 'qep' ? (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                       <QEPDashboard />

                       <div className="pt-12 border-t border-white/5">
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-10">
                             <GraduationCap size={28} className="text-highlight" />
                             Learn-Teach Ecosystem
                          </h3>
                          <LearnTeachModule />
                       </div>

                       <div className="pt-12 border-t border-white/5">
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-10">
                             <Zap size={28} className="text-aura shadow-2xl shadow-aura/20" />
                             Immersive & Ethical Infrastructure
                          </h3>
                          <QEPImmersiveTools />
                       </div>

                       <div className="pt-12 border-t border-white/5">
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-10">
                             <Sparkles size={28} className="text-aura shadow-2xl shadow-aura/20" />
                             Flagship Suite Completion (v0.9)
                          </h3>
                          <QEPFlagshipFeatures />
                       </div>
                    </motion.div>
                  ) : wisdoms.map((wisdom, i) => (
                    <motion.div
                      key={wisdom.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                             <Heart size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{wisdom.name}</p>
                             <div className="flex items-center gap-4">
                                <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{wisdom.type}</span>
                                <span className="text-[10px] font-mono text-aura/50">{wisdom.hash}</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-6">
                          <Badge color={wisdom.status === 'Ratified' ? 'emerald-500' : 'highlight'}>{wisdom.status}</Badge>
                          <Button onClick={() => notImplemented('Meditate')} variant="outline" className="px-6">Meditate</Button>
                       </div>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </div>

         <div className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <ShieldCheck size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Ethical Guidance</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Real-time moral alignment checks powered by Constitutional AI and Article 1126 ethical regulons.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Alignment Score</span>
                     <span className="text-emerald-500">OPTIMAL</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-[98%]" />
                  </div>
               </div>
               <Button onClick={() => notImplemented('Consult Ethics Council')} className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs">Consult Ethics Council</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Spiritual Markers (Methylation)</h4>
               <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">COMPASSION_STRICT</span>
                     <Badge color="emerald-500">SET</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                     <span className="text-[10px] font-black text-slate-300">CONTEMPLATION_MODE</span>
                     <Badge color="aura">ACTIVE</Badge>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura">
                     <Globe size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white mb-1">Interfaith Mesh</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">142 Global Nodes Synchronized</p>
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
