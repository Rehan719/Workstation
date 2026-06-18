import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Briefcase, History } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { ApplicationStudio } from '../../components/employment/ApplicationStudio';

export const EmploymentHub: React.FC = () => {
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState('studio');

  const scrollToSection = (id: string) => {
    // Defer until the tab's content has mounted.
    requestAnimationFrame(() => {
      setTimeout(() => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    });
  };

  const handleCareerPath = () => {
    setActiveTab('studio');
    scrollToSection('input-materials-section');
  };

  const handleNewOpportunity = () => {
    setActiveTab('studio');
    scrollToSection('job-search-engine-section');
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div className="min-w-0">
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase break-words">Nexus of Talent</h1>
          <div className="flex flex-wrap items-center gap-y-2 gap-x-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Workforce Orchestration • Skill Mesh • Employment Hub</p>
             <Badge color="highlight" className="text-[8px] shrink-0">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px] shrink-0">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex flex-wrap gap-4 shrink-0">
           <Button variant="outline" onClick={handleCareerPath}><History size={18} /> Career Path</Button>
           <Button onClick={handleNewOpportunity} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Briefcase size={18} /> New Opportunity
           </Button>
        </div>
      </header>

      <Card className="p-10 space-y-10">
         <div className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-center gap-6 border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight min-w-0 shrink-0">
               <Layers size={24} className="text-aura shrink-0" />
               <span className="truncate">Employment Engines</span>
            </h3>
            <div className="flex gap-2 @[480px]:gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800 max-w-full overflow-x-auto custom-scrollbar">
               <button type="button" onClick={() => setActiveTab('studio')} className={`shrink-0 whitespace-nowrap px-3 @[480px]:px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'studio' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Application Studio</button>
               <button type="button" onClick={() => setActiveTab('skills')} className={`shrink-0 whitespace-nowrap px-3 @[480px]:px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'skills' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Skills</button>
               <button type="button" onClick={() => setActiveTab('qep')} className={`shrink-0 whitespace-nowrap px-3 @[480px]:px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="employment" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-xl @[480px]:text-2xl @[680px]:text-3xl font-black text-white mb-10 uppercase tracking-tighter break-words">Virtual Skill Garden</h3>
                    <QEPImmersiveTools domain="employment" />
                 </div>
              </motion.div>
            ) : activeTab === 'studio' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                 <ApplicationStudio />
              </motion.div>
            ) : (
              <div className="p-20 text-center border-2 border-dashed border-slate-900 rounded-[3rem]">
                 <p className="text-slate-600 font-black uppercase tracking-widest">Update your skills to see matches.</p>
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};
