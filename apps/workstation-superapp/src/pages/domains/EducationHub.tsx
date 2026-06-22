import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, GraduationCap, History } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';

export const EducationHub: React.FC = () => {
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState('lessons');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter italic break-words">Aula of Enlightenment</h1>
          <div className="flex items-center gap-4">
             <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Adaptive Pedagogy • Knowledge Mesh • Education Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button type="button" onClick={() => navigate('/projects?realm=education&domain=curriculum')} variant="outline"><History size={18} /> Curriculum</Button>
           <Button type="button" onClick={() => navigate('/projects?realm=education&domain=curriculum&new=1')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <GraduationCap size={18} /> New Lesson
           </Button>
        </div>
      </header>
      <StartProjectCTA realm="education" domain="curriculum" />

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-highlight" />
               Pedagogical Engines
            </h3>
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
               <button type="button" onClick={() => setActiveTab('lessons')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'lessons' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Lessons</button>
               <button type="button" onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="education" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-3xl font-black text-white mb-10 uppercase tracking-tighter">Universal Aula VR</h3>
                    <QEPImmersiveTools domain="education" />
                 </div>
              </motion.div>
            ) : (
              <DomainTool
                title="Lesson Plan Generator"
                description={<>Describe a lesson — Workstation's <span className="text-highlight">own</span> AI produces a classroom-ready plan (objectives, sequence, differentiation, assessment), in-house.</>}
                endpoint="/api/v1/education/lesson-plan"
                resultKey="lesson_plan"
                submitLabel="Generate lesson plan"
                fields={[
                  { name: 'subject', label: 'Subject', type: 'text', placeholder: 'e.g. Biology', default: 'Biology' },
                  { name: 'topic', label: 'Topic', type: 'textarea', placeholder: 'e.g. Photosynthesis — light-dependent reactions' },
                  { name: 'level', label: 'Level', type: 'text', placeholder: 'e.g. GCSE / KS3 / A-Level', default: 'GCSE' },
                  { name: 'duration_minutes', label: 'Duration (minutes)', type: 'text', default: '60' },
                ]}
              />
            )}
         </div>
      </Card>
    </div>
  );
};
