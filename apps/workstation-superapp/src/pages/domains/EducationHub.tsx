import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, GraduationCap, History } from 'lucide-react';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';
import { toolsFor } from '../../lib/toolRegistry';
import { useTab } from '../../lib/useTab';   // W1027 - the tab is in the address
import { useServingStatus, servingIsFloor } from '../../components/ServingNow';   // W956 (P5.12 clause 5)
import { apiJson, errorMessage } from '../../lib/api';

const EDUCATION_TABS = ['lessons', 'curriculum', 'assessment', 'feedback'] as const;

export const EducationHub: React.FC = () => {
  const T = toolsFor('/education');   // W470 — the one tool registry the front doors count from
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useTab(EDUCATION_TABS, 'lessons');
  // P3.30 (ledger v16 R5.10) — the curriculum frameworks the API lists (GET /api/v1/education/frameworks had no
  // caller: this select offered four typed values, three of which that list does not hold). Null = not read
  // yet; a failed read is SAID, and only the default is offered then.
  const [frameworks, setFrameworks] = useState<string[] | null>(null);
  // W816 (FU-835) - the select showed each framework's id; it shows the name the API gives and still sends the id
  const [frameworkNames, setFrameworkNames] = useState<Record<string, string>>({});
  const [frameworksNote, setFrameworksNote] = useState('');
  useEffect(() => {
    let alive = true;
    //  W1004 - a refusal says the server's reason (it said "HTTP 503" alone), and a list read empty is said as
    //  empty: it was said as one that could not be read
    apiJson<any>('/api/v1/education/frameworks')
      .then(d => {
        if (!alive) return;
        if (!Array.isArray(d?.frameworks)) {
          setFrameworks(null);
          setFrameworksNote('The framework list could not be read (the answer held no list), so only the default framework is offered below.');
          return;
        }
        const list = d.frameworks;
        const ids = list.map((f: any) => String(f?.id ?? '')).filter(Boolean);
        if (ids.length === 0) {
          setFrameworks(null);
          setFrameworksNote('The server lists no frameworks, so only the default framework is offered below.');
          return;
        }
        const names: Record<string, string> = {};
        list.forEach((f: any) => { if (f?.id && f?.name) names[String(f.id)] = String(f.name); });
        setFrameworks(ids); setFrameworkNames(names); setFrameworksNote('');
      })
      .catch(e => { if (alive) { setFrameworks(null); setFrameworksNote(`The framework list could not be read (${errorMessage(e)}), so only the default framework is offered below.`); } });
    return () => { alive = false; };
  }, []);

  // W956 (P5.12 clause 5) - WHAT EACH FORM DOES ON THIS MACHINE NOW, said before it is filled: the server's sentence
  // for the form, with the sentence its answer carries with a model or without one, chosen by the serving status.
  // Nothing here is typed about a form; a failed read is said, and nothing is claimed in its place.
  const serving = useServingStatus();
  const [eduTools, setEduTools] = useState<Record<string, any> | null>(null);
  const [eduToolsNote, setEduToolsNote] = useState('');
  useEffect(() => {
    let alive = true;
    apiJson<any>('/api/v1/education/tools')
      .then(d => {
        if (!alive) return;
        const byId: Record<string, any> = {};
        (Array.isArray(d?.forms) ? d.forms : []).forEach((f: any) => { if (f?.id) byId[String(f.id)] = f; });
        setEduTools(byId); setEduToolsNote('');
      })
      .catch(e => { if (alive) { setEduTools(null); setEduToolsNote(`What each form does could not be read (${errorMessage(e)}), so nothing is said about it here. Each answer still says what composed it.`); } });
    return () => { alive = false; };
  }, []);
  const floorNow = serving ? servingIsFloor(serving) : null;
  const formSays = (id: string) => {
    const f = eduTools?.[id];
    if (!f) return <span data-testid="education-form-not-read" className="text-amber-400">{eduToolsNote}</span>;
    const now = serving === undefined ? ''
      : serving === null ? `Whether a model is serving could not be read just now; without one, its answer says: ${f.when_no_model_serves}`
      : floorNow ? `No model is serving on this deployment now, so its answer says: ${f.when_no_model_serves}`
      : `A model is serving now (${serving.active_model_label || 'a local model'}), so its answer says: ${f.with_a_model}`;
    return <span data-testid="education-form-says">{f.does} {now}</span>;
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter italic break-words">Aula of Enlightenment</h1>
          <div className="flex items-center gap-4">
             <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Education Hub • the tools are in the tabs below</p>
             {/* W493 (FU-154, sweep S10.5, C4) - these read "GUIDED MODE" / "ENCOURAGING TONE" as
                 though the hub adapted to them. Nothing does: only this badge reads the values.
                 No affordance is gated on the mode and no request carries the tone. They are
                 saved preferences, and the badges now say so. */}
             <Badge color="highlight" className="text-[8px]"
                    title="a saved preference - no affordance on this hub is gated on it yet">{layout} MODE (saved pref.)</Badge>
             <Badge color="aura" className="text-[8px]"
                    title="a saved preference - no request from this hub carries it yet">{emotionalAdjustment} TONE (saved pref.)</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button type="button" onClick={() => navigate('/projects?realm=education&domain=curriculum')} variant="outline"><History size={18} /> Education projects</Button>
           <Button type="button" onClick={() => navigate('/projects?realm=education&domain=curriculum&new=1')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <GraduationCap size={18} /> Start an education project
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
               <button type="button" onClick={() => setActiveTab('curriculum')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'curriculum' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Curriculum</button>
               <button type="button" onClick={() => setActiveTab('assessment')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'assessment' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Assessment</button>
               <button type="button" onClick={() => setActiveTab('feedback')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'feedback' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Marking</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'curriculum' ? (
              <DomainTool
                title={T['curriculum'].title}
                description={<>{formSays('curriculum')}{frameworksNote && <span className="block mt-1 text-amber-400" data-testid="education-frameworks-note">{frameworksNote}</span>}</>}
                endpoint="/api/v1/education/curriculum"
                resultKey="curriculum"
                submitLabel="Design curriculum"
                fields={[
                  { name: 'subject', label: 'Subject', type: 'text', placeholder: 'e.g. Introduction to Machine Learning', default: 'Introduction to Machine Learning' },
                  { name: 'level', label: 'Level', type: 'text', placeholder: 'e.g. GCSE / A-Level / University Year 1', default: 'University Year 1' },
                  { name: 'duration_weeks', label: 'Duration (weeks)', type: 'text', default: '12' },
                  { name: 'framework', label: 'Framework', type: 'select', options: (frameworks && frameworks.length > 0 ? frameworks : ['bloom']), optionLabels: frameworkNames, default: 'bloom' },
                  { name: 'learning_objectives_count', label: 'Learning objectives', type: 'text', default: '6' },
                ]}
              />
            ) : activeTab === 'assessment' ? (
              <DomainTool
                title={T['assessment'].title}
                description={<>{formSays('assessment')}</>}
                endpoint="/api/v1/education/assessment"
                resultKey="assessment"
                submitLabel="Build assessment"
                fields={[
                  { name: 'subject', label: 'Subject', type: 'text', placeholder: 'e.g. Biology', default: 'Biology' },
                  { name: 'topic', label: 'Topic', type: 'text', placeholder: 'e.g. Photosynthesis', default: 'Photosynthesis' },
                  { name: 'level', label: 'Level', type: 'text', placeholder: 'e.g. GCSE / KS3 / A-Level', default: 'GCSE' },
                  { name: 'assessment_type', label: 'Type', type: 'select', options: ['quiz', 'rubric', 'exam', 'project_brief', 'formative'], default: 'quiz' },
                  { name: 'learning_objectives', label: 'Learning objectives (one per line)', type: 'list', placeholder: 'explain the light-dependent reactions' },
                ]}
              />
            ) : activeTab === 'feedback' ? (
              <DomainTool
                title={T['feedback'].title}
                description={<>{formSays('feedback')}</>}
                endpoint="/api/v1/education/feedback"
                resultKey="feedback"
                submitLabel="Mark & give feedback"
                fields={[
                  { name: 'student_work', label: "Student's work", type: 'textarea', placeholder: "paste the student's answer / essay / response here" },
                  { name: 'task', label: 'Task / question', type: 'textarea', placeholder: 'e.g. Explain the causes of the First World War (12 marks)' },
                  { name: 'rubric', label: 'Rubric / marking criteria (optional)', type: 'textarea', placeholder: 'paste the mark scheme or success criteria' },
                  { name: 'subject', label: 'Subject', type: 'text', default: 'general', placeholder: 'e.g. History' },
                  { name: 'level', label: 'Level', type: 'text', placeholder: 'e.g. GCSE / KS2 / A-Level' },
                  { name: 'tone', label: 'Feedback tone', type: 'select', options: ['constructive', 'encouraging', 'rigorous'], default: 'constructive' },
                ]}
              />
            ) : (
              <DomainTool
                title={T['lessons'].title}
                description={<>{formSays('lesson_plan')}</>}
                endpoint="/api/v1/education/lesson-plan"
                resultKey="lesson_plan"
                submitLabel="Generate lesson plan"
                fields={[
                  { name: 'subject', label: 'Subject', type: 'text', placeholder: 'e.g. Biology', default: 'Biology' },
                  { name: 'topic', label: 'Topic', type: 'textarea', placeholder: 'e.g. Photosynthesis — light-dependent reactions' },
                  { name: 'level', label: 'Level', type: 'text', placeholder: 'e.g. GCSE / KS3 / A-Level', default: 'GCSE' },
                  { name: 'duration_minutes', label: 'Duration (minutes)', type: 'text', default: '60' },
                  // W949 (P5.12 clause 6) - a pupil is not named: the form says so where the needs are typed
                  { name: 'special_needs', label: 'Needs to plan for (do not name a pupil)', type: 'textarea',
                    placeholder: 'e.g. two learners need large print. Never a name: what you type is sent as typed.' },
                ]}
              />
            )}
         </div>
      </Card>
    </div>
  );
};
