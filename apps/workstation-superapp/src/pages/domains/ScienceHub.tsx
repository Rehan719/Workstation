import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { BookOpen, Heart, Sparkles, MessageCircle, History, Info, ShieldCheck, Zap, Globe, HeartPulse, Network, Binary, Compass, Anchor, Wind, Layers, Microscope } from 'lucide-react';
import { useStore } from '@workstation/shared';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';
import { toolsFor } from '../../lib/toolRegistry';
import { apiJson, errorMessage } from '../../lib/api';   // W1004

export const ScienceHub: React.FC = () => {
  const T = toolsFor('/science');   // W470 — the one tool registry the front doors count from
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'research');
  // W824 (FU-862) - the methodologies the API lists (GET /api/v1/science/methodologies had no caller: the design select
  // typed eight of its ten and the synthesis form offered none). Null = not read; a failed read is SAID.
  const [methods, setMethods] = useState<string[] | null>(null);
  const [methodNames, setMethodNames] = useState<Record<string, string>>({});
  const [methodsNote, setMethodsNote] = useState('');
  useEffect(() => {
    let alive = true;
    //  W1004 - a refusal says the server's reason (it said "HTTP 503" alone), and a list read empty is said as
    //  empty: it was said as one that could not be read
    apiJson<any>('/api/v1/science/methodologies')
      .then(d => {
        if (!alive) return;
        if (!Array.isArray(d?.methodologies)) {
          setMethods(null);
          setMethodsNote('The methodology list could not be read (the answer held no list), so only the methodologies typed on this page are offered.');
          return;
        }
        const list = d.methodologies;
        const ids = list.map((m: any) => String(m?.id ?? '')).filter(Boolean);
        if (ids.length === 0) {
          setMethods(null);
          setMethodsNote('The server lists no methodologies, so only the methodologies typed on this page are offered.');
          return;
        }
        const names: Record<string, string> = {};
        list.forEach((m: any) => { if (m?.id && m?.name) names[String(m.id)] = String(m.name); });
        setMethods(ids); setMethodNames(names); setMethodsNote('');
      })
      .catch(e => { if (alive) { setMethods(null); setMethodsNote(`The methodology list could not be read (${errorMessage(e)}), so only the methodologies typed on this page are offered.`); } });
    return () => { alive = false; };
  }, []);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter italic break-words">Frontier of Discovery</h1>
          <div className="flex items-center gap-4">
             <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Science Hub • the tools are in the tabs below</p>
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
           <Button type="button" onClick={() => navigate('/projects?realm=science&domain=research')} variant="outline"><History size={18} /> Science projects</Button>
           <Button type="button" onClick={() => navigate('/reactor?domain=science')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Microscope size={18} /> Open the Reactor (science)
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
               {/* P3.30 (ledger v16 R5.10) — POST /api/v1/science/hypothesis had no screen */}
               <button type="button" onClick={() => setActiveTab('hypothesis')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'hypothesis' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Hypotheses</button>
               <button type="button" onClick={() => setActiveTab('design')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'design' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Experiment Design</button>
               <button type="button" onClick={() => setActiveTab('literature')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'literature' ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>Literature</button>
            </div>
         </div>

         <div className="space-y-12">
            {methodsNote && <p className="text-[10px] text-amber-400" data-testid="science-methods-note">{methodsNote}</p>}
            {/* W824 (FU-862) - A STATED ABSENCE. The manufacturing-record gate has routes and no screen. */}
            <p className="text-[10px] text-slate-500 leading-relaxed" data-testid="science-gmp-absent">
              Not on this page: the manufacturing-record (GMP) gate - a roster of named signatories, batch records, and
              their signing. Its routes exist (/api/v1/science/gmp/...) and no screen calls them.
            </p>
            {activeTab === 'hypothesis' ? (
              <DomainTool
                title={T['hypothesis'].title}
                description={<>Pose a research question — you get candidate hypotheses, each with a null and an alternative, a rationale and a suggested test. Any feasibility or novelty figure in the text is the composing model's own estimate: nothing here measures either. What served the answer is shown with it.</>}
                endpoint="/api/v1/science/hypothesis"
                resultKey="hypotheses_text"
                submitLabel="Generate hypotheses"
                fields={[
                  { name: 'research_question', label: 'Research question', type: 'textarea', placeholder: 'e.g. Does a later school start time improve attendance in secondary schools?' },
                  { name: 'domain', label: 'Domain', type: 'text', default: 'general', placeholder: 'education | medicine | physics | …' },
                  { name: 'background_context', label: 'Background (optional)', type: 'text', placeholder: 'what is already known, in a sentence' },
                  { name: 'num_hypotheses', label: 'How many (2 to 5)', type: 'select', options: ['2', '3', '4', '5'], default: '3' },
                ]}
              />
            ) : activeTab === 'design' ? (
              <DomainTool
                title={T['design'].title}
                description={<>State a hypothesis — Workstation's <span className="text-aura">own</span> AI designs a rigorous study (variables, controls, sampling &amp; power, procedure, analysis plan, validity, ethics), grounded in your chosen methodology, in-house.</>}
                endpoint="/api/v1/science/experiment-design"
                resultKey="design"
                submitLabel="Design the study"
                fields={[
                  { name: 'hypothesis', label: 'Hypothesis to test', type: 'textarea', placeholder: 'e.g. A 10-minute daily mindfulness app reduces self-reported anxiety in undergraduates' },
                  { name: 'methodology', label: 'Methodology', type: 'select', options: (methods && methods.length > 0 ? methods : ['experimental', 'rct', 'cohort_study', 'case_control', 'mixed_methods', 'computational', 'survey', 'grounded_theory']), optionLabels: methodNames, default: 'experimental' },
                  { name: 'domain', label: 'Domain', type: 'text', default: 'psychology', placeholder: 'psychology | biology | materials | …' },
                  { name: 'constraints', label: 'Constraints (optional)', type: 'textarea', placeholder: 'budget, time, sample availability, ethics' },
                  { name: 'sample_size_hint', label: 'Effect-size / sample context (optional)', type: 'text', placeholder: 'e.g. expect a small-to-medium effect; ~200 available' },
                ]}
              />
            ) : activeTab === 'literature' ? (
              <DomainTool
                title={T['literature'].title}
                description={<>Pose a research question — Workstation's <span className="text-aura">own</span> AI maps the literature into a structured review outline (themes, key works, gaps), in-house.</>}
                endpoint="/api/v1/science/literature"
                resultKey="outline"
                submitLabel="Map the literature"
                fields={[
                  { name: 'research_question', label: 'Research question', type: 'textarea', placeholder: 'e.g. How does sleep affect memory consolidation?' },
                  { name: 'domain', label: 'Domain', type: 'text', default: 'neuroscience', placeholder: 'neuroscience | economics | …' },
                  { name: 'scope_years', label: 'Scope (years back)', type: 'text', default: '10' },
                ]}
              />
            ) : (
              <DomainTool
                title={T['research'].title}
                description={<>Pose a research question — Workstation's <span className="text-aura">own</span> AI synthesises a structured, methodology-grounded evidence report, in-house.</>}
                endpoint="/api/v1/science/synthesise"
                resultKey="report"
                submitLabel="Synthesise report"
                fields={[
                  { name: 'research_question', label: 'Research question', type: 'textarea', placeholder: 'e.g. Does intermittent fasting reduce inflammatory markers in adults?' },
                  { name: 'domain', label: 'Domain', type: 'text', default: 'medicine', placeholder: 'medicine | physics | social science' },
                  { name: 'methodology', label: 'Methodology', type: 'select', options: (methods && methods.length > 0 ? methods : ['systematic_review']), optionLabels: methodNames, default: 'systematic_review' },
                  { name: 'depth', label: 'Depth', type: 'select', options: ['brief', 'standard', 'comprehensive'], default: 'standard' },
                ]}
              />
            )}
         </div>
      </Card>
    </div>
  );
};
