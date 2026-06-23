import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from '@workstation/ui';
import { Scale, Microscope, HeartPulse, GraduationCap, Heart, Briefcase, Sparkles, ArrowRight } from 'lucide-react';

// A single front door to every in-house AI tool. Each links straight to its hub + tab (?tab=).
// All tools run on Workstation's OWN native fabric (honest in-house provenance) and are runnable,
// iteratively refinable, and exportable (Copy / Download .md).
interface Tool { tab: string; name: string; desc: string }
interface DomainGroup { name: string; route: string; icon: React.ComponentType<any>; tools: Tool[] }

const DOMAINS: DomainGroup[] = [
  { name: 'Law', route: '/law', icon: Scale, tools: [
    { tab: 'compliance', name: 'Document Analyser', desc: 'Analyse a contract for key clauses, risks and missing provisions.' },
    { tab: 'draft', name: 'Document Drafter', desc: 'Generate a clause-numbered legal document from a template.' },
  ]},
  { name: 'Science', route: '/science', icon: Microscope, tools: [
    { tab: 'research', name: 'Research Synthesiser', desc: 'Synthesise a research question into a structured evidence report.' },
    { tab: 'literature', name: 'Literature Review', desc: 'Map the literature into a themed review outline (key works, gaps).' },
  ]},
  { name: 'Care', route: '/care', icon: HeartPulse, tools: [
    { tab: 'clinical', name: 'Clinical Handover (SBAR)', desc: 'Compose a structured clinical handover.' },
    { tab: 'care-plan', name: 'Care Plan Builder', desc: 'Draft a person-centred care plan with goals and interventions.' },
    { tab: 'risk', name: 'Clinical Risk Assessment', desc: 'Score and interpret a validated tool (NEWS2, MUST, Waterlow…).' },
  ]},
  { name: 'Education', route: '/education', icon: GraduationCap, tools: [
    { tab: 'lessons', name: 'Lesson Plan Generator', desc: 'A classroom-ready lesson plan (objectives, sequence, differentiation).' },
    { tab: 'curriculum', name: 'Curriculum Designer', desc: 'A full framework-aligned, week-by-week curriculum.' },
    { tab: 'assessment', name: 'Assessment Builder', desc: 'Quizzes, rubrics, exams and project briefs with mark schemes.' },
  ]},
  { name: 'Religion', route: '/religion', icon: Heart, tools: [
    { tab: 'dialogue', name: 'Comparative Fiqh Research', desc: 'Research a question of Islamic jurisprudence within a chosen madhab.' },
    { tab: 'tafsir', name: "Qur'anic Tafsir", desc: 'Structured tafsir of an ayah (classical, thematic, contemporary, linguistic).' },
    { tab: 'halal', name: 'Halal Pre-Assessment', desc: 'Halal certification pre-assessment of a product and its ingredients.' },
  ]},
  { name: 'Employment', route: '/employment', icon: Briefcase, tools: [
    { tab: 'cv', name: 'CV / Résumé Tailor', desc: 'Tailor a CV to a target role — achievement-led, ATS-friendly.' },
    { tab: 'cover', name: 'Cover Letter', desc: 'Draft a focused, tailored cover letter.' },
    { tab: 'application', name: 'Application & Supporting Statement', desc: 'Address a person specification point-by-point and answer form questions.' },
    { tab: 'interview', name: 'Interview Preparation', desc: 'Likely questions plus STAR-method answer frameworks.' },
    { tab: 'path', name: 'Career Path & Skills Gap', desc: 'A development roadmap from your current to your target role.' },
  ]},
];

const TOTAL = DOMAINS.reduce((n, d) => n + d.tools.length, 0);

export const AIToolsCatalogue: React.FC = () => (
  <div className="space-y-10 pb-24">
    <header>
      <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · In-House AI</p>
      <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">AI Tools</h1>
      <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
        {TOTAL} tools across {DOMAINS.length} domains — every one runs on Workstation's
        <span className="text-highlight"> own</span> native AI fabric (honest in-house provenance, never an external dependency),
        and each output is <span className="text-aura">runnable, iteratively refinable, and exportable</span> (Copy / Download).
      </p>
    </header>

    {DOMAINS.map(d => {
      const Icon = d.icon;
      return (
        <section key={d.name} className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-highlight/10 flex items-center justify-center"><Icon size={16} className="text-highlight" /></div>
            <h2 className="text-lg font-black text-white uppercase tracking-tight">{d.name}</h2>
            <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">{d.tools.length} tools</span>
          </div>
          <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-4">
            {d.tools.map(t => (
              <Link key={t.tab} to={`${d.route}?tab=${t.tab}`}
                className="group text-left p-5 rounded-2xl border bg-slate-900 border-slate-800 hover:border-highlight/40 transition-all">
                <div className="flex items-start justify-between gap-2">
                  <p className="font-black text-white text-sm flex items-center gap-2"><Sparkles size={13} className="text-aura" /> {t.name}</p>
                  <ArrowRight size={14} className="text-slate-600 group-hover:text-highlight transition-all shrink-0 mt-0.5" />
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed mt-2">{t.desc}</p>
              </Link>
            ))}
          </div>
        </section>
      );
    })}
  </div>
);
