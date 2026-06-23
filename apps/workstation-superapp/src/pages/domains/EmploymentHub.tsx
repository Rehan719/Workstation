import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Briefcase, History } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { ApplicationStudio } from '../../components/employment/ApplicationStudio';
import { DomainTool } from '../../components/DomainTool';

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
               {([['studio', 'Application Studio'], ['cv', 'CV Tailor'], ['cover', 'Cover Letter'], ['application', 'Application Form'], ['interview', 'Interview Prep'], ['path', 'Career Path'], ['qep', 'QEP Flagship']] as [string, string][]).map(([id, label]) => (
                 <button key={id} type="button" onClick={() => setActiveTab(id)} className={`shrink-0 whitespace-nowrap px-3 @[480px]:px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === id ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>{label}</button>
               ))}
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
            ) : activeTab === 'cv' ? (
              <DomainTool
                title="CV / Résumé Tailor"
                description={<>Tailor your CV to a target role — Workstation's <span className="text-aura">own</span> AI rewrites it as achievement-led, ATS-friendly bullets, in-house.</>}
                endpoint="/api/v1/employment/cv"
                resultKey="cv"
                submitLabel="Tailor CV"
                fields={[
                  { name: 'target_role', label: 'Target role', type: 'text', placeholder: 'e.g. Senior Data Engineer' },
                  { name: 'experience', label: 'Experience summary', type: 'textarea', placeholder: 'your career history, achievements, and context' },
                  { name: 'skills', label: 'Key skills (one per line)', type: 'list', placeholder: 'Python\nSpark\nAWS' },
                  { name: 'seniority', label: 'Seniority', type: 'select', options: ['entry', 'mid', 'senior', 'lead', 'executive'], default: 'mid' },
                ]}
              />
            ) : activeTab === 'cover' ? (
              <DomainTool
                title="Cover Letter"
                description={<>Draft a focused, tailored cover letter — Workstation's <span className="text-aura">own</span> AI, in-house, no generic filler.</>}
                endpoint="/api/v1/employment/cover-letter"
                resultKey="cover_letter"
                submitLabel="Draft cover letter"
                fields={[
                  { name: 'target_role', label: 'Target role', type: 'text', placeholder: 'e.g. Product Manager' },
                  { name: 'company', label: 'Company (optional)', type: 'text', placeholder: 'e.g. Acme Ltd' },
                  { name: 'highlights', label: 'What to emphasise', type: 'textarea', placeholder: 'key achievements / motivation' },
                  { name: 'tone', label: 'Tone', type: 'select', options: ['professional', 'warm', 'concise', 'enthusiastic'], default: 'professional' },
                ]}
              />
            ) : activeTab === 'application' ? (
              <DomainTool
                title="Application Form & Supporting Statement"
                description={<>Paste the person specification and your experience — Workstation's <span className="text-aura">own</span> AI drafts a criterion-by-criterion supporting statement and answers your form questions, in-house, never inventing experience.</>}
                endpoint="/api/v1/employment/application"
                resultKey="statement"
                submitLabel="Draft application"
                fields={[
                  { name: 'target_role', label: 'Target role', type: 'text', placeholder: 'e.g. Band 5 Staff Nurse' },
                  { name: 'organisation', label: 'Organisation (optional)', type: 'text', placeholder: 'e.g. NHS Trust / charity name' },
                  { name: 'person_spec', label: 'Person specification / selection criteria', type: 'textarea', placeholder: 'paste the essential & desirable criteria' },
                  { name: 'experience', label: 'Your relevant experience', type: 'textarea', placeholder: 'your evidence, achievements, and context' },
                  { name: 'questions', label: 'Application-form questions (one per line)', type: 'list', placeholder: 'Describe a time you handled a deteriorating patient.\nWhy this organisation?' },
                  { name: 'word_limit', label: 'Word limit (0 = none)', type: 'text', default: '0' },
                ]}
              />
            ) : activeTab === 'interview' ? (
              <DomainTool
                title="Interview Preparation"
                description={<>Prepare for an interview — Workstation's <span className="text-aura">own</span> AI gives likely questions + STAR frameworks, in-house.</>}
                endpoint="/api/v1/employment/interview-prep"
                resultKey="prep"
                submitLabel="Prepare"
                fields={[
                  { name: 'target_role', label: 'Target role', type: 'text', placeholder: 'e.g. Backend Engineer' },
                  { name: 'seniority', label: 'Seniority', type: 'select', options: ['entry', 'mid', 'senior', 'lead', 'executive'], default: 'mid' },
                  { name: 'competencies', label: 'Focus competencies (one per line)', type: 'list', placeholder: 'system design\nownership' },
                ]}
              />
            ) : activeTab === 'path' ? (
              <DomainTool
                title="Career Path & Skills Gap"
                description={<>Map a development roadmap from your current to your target role — Workstation's <span className="text-aura">own</span> AI, in-house, with an honest assessment.</>}
                endpoint="/api/v1/employment/career-path"
                resultKey="roadmap"
                submitLabel="Map roadmap"
                fields={[
                  { name: 'current_role', label: 'Current role', type: 'text', placeholder: 'e.g. QA Analyst' },
                  { name: 'target_role', label: 'Target role', type: 'text', placeholder: 'e.g. SDET' },
                  { name: 'experience_years', label: 'Years of experience', type: 'text', default: '3' },
                  { name: 'constraints', label: 'Constraints (optional)', type: 'text', placeholder: 'e.g. evenings only, 12-month horizon' },
                ]}
              />
            ) : (
              <div className="p-20 text-center border-2 border-dashed border-slate-900 rounded-[3rem]">
                 <p className="text-slate-600 font-black uppercase tracking-widest">Select an engine to begin.</p>
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};
