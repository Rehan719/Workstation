import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { BookOpen, Heart, Sparkles, MessageCircle, History, Info, ShieldCheck, Zap, Globe, HeartPulse, Network, Binary, Compass, Anchor, Wind, Layers, Microscope } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';

export const ScienceHub: React.FC = () => {
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState('research');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter italic break-words">Frontier of Discovery</h1>
          <div className="flex items-center gap-4">
             <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Scientific Inquiry • Empirical Mesh • Science Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button type="button" onClick={() => navigate('/projects?realm=science&domain=research')} variant="outline"><History size={18} /> Lab Notes</Button>
           <Button type="button" onClick={() => navigate('/reactor?domain=science')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Microscope size={18} /> New Experiment
           </Button>
        </div>
      </header>
      <StartProjectCTA realm="science" domain="research" />

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-highlight" />
               Scholarly Engines
            </h3>
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
               <button type="button" onClick={() => setActiveTab('research')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'research' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Research</button>
               <button type="button" onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="science" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-3xl font-black text-white mb-10 uppercase tracking-tighter">Immersive Lab Environment</h3>
                    <QEPImmersiveTools domain="science" />
                 </div>
              </motion.div>
            ) : (
              <div className="p-20 text-center border-2 border-dashed border-slate-900 rounded-[3rem]">
                 <p className="text-slate-600 font-black uppercase tracking-widest">Select an engine to begin exploration.</p>
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};
