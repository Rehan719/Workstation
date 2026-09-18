// W470 (P1.13 catalogue honesty) — the ONE registry of the Domains section's tools.
//
// Every hub mounts its tool titles from here (`toolsFor('/law').research.title`), and both front doors
// (DomainsHub, AIToolsCatalogue) derive their counts and their launch links from here — so a tool added
// hub-by-hub can no longer leave the front door under-counting it (the R5.8 drift: 23 advertised, 18
// listed, 24 mounted). The suite parses this file and every hub and fails when they disagree.
//
// `tab` is the hub's ?tab= key. `kind`:
//   form     — a <DomainTool> form (the count P1.13 guards);
//   custom   — a hand-built surface on the hub that runs a real backend route (Law's analyser, the
//              Employment Application Studio);
//   flagship — the Religion domain's Quran Education Platform (the Owner's directive 2026-09-03: QEP
//              lives in Religion, and nowhere else).
export type ToolKind = 'form' | 'custom' | 'flagship';
export interface ToolEntry { tab: string; title: string; desc: string; kind: ToolKind }
export interface DomainTools { name: string; route: string; tools: ToolEntry[] }

const form = (tab: string, title: string, desc: string): ToolEntry => ({ tab, title, desc, kind: 'form' });

export const TOOL_REGISTRY: DomainTools[] = [
  { name: 'Religion', route: '/religion', tools: [
    form('dialogue', 'Comparative Fiqh Research', 'Research a question of Islamic jurisprudence within a chosen madhab, with scholarly humility.'),
    form('tafsir', "Qur'anic Tafsir", 'Structured tafsir of an ayah (classical, thematic, contemporary, linguistic), drawing on the classical mufassirun.'),
    form('halal', 'Halal Certification Pre-Assessment', 'Halal pre-assessment of a product and its ingredients: flags, process concerns, certification guidance.'),
    form('hadith', 'Hadith Study (Ulum al-Hadith)', 'Research a hadith’s narration, isnad, grading and sharh. Research only — grading must be verified against authenticated collections.'),
    { tab: 'qep', kind: 'flagship', title: 'Quran Education Platform', desc: 'The Religion domain’s flagship: authentic Quran text from the recognised sources, real SM-2 hifz scheduling, honest written recall, provenance-labelled AI. Recitation is never scored.' },
  ]},
  { name: 'Science', route: '/science', tools: [
    form('research', 'Research Synthesiser', 'Synthesise a research question into a structured, methodology-grounded evidence report.'),
    form('design', 'Experiment Designer', 'Design a rigorous study from a hypothesis: variables, controls, sampling and power, procedure, analysis plan, validity, ethics.'),
    form('literature', 'Literature Review', 'Map the literature into a themed review outline (themes, key works, gaps).'),
  ]},
  { name: 'Education', route: '/education', tools: [
    form('lessons', 'Lesson Plan Generator', 'A classroom-ready lesson plan (objectives, sequence, differentiation, assessment).'),
    form('curriculum', 'Curriculum Designer', 'A full framework-aligned, week-by-week curriculum with objectives and assessment.'),
    form('assessment', 'Assessment Builder', 'Quizzes, rubrics, exams, project briefs and formative checks with mark schemes.'),
    form('feedback', 'Marking & Feedback', 'Mark a student’s work against the task and rubric with constructive feedback and an indicative level. An aid to your judgement, never a grade.'),
  ]},
  { name: 'Law', route: '/law', tools: [
    { tab: 'compliance', kind: 'custom', title: 'Legal Document Analyser', desc: 'Analyse a contract or legal document for key clauses, risks, compliance points and missing provisions.' },
    form('draft', 'Legal Document Drafter', 'Draft a clause-numbered legal document from a template for your parties and jurisdiction.'),
    form('research', 'Legal Research (IRAC)', 'Research a legal question by the IRAC method with practical steps, risks and next actions. Informational only — not legal advice.'),
  ]},
  { name: 'Care', route: '/care', tools: [
    form('clinical', 'Clinical Handover (SBAR)', 'Compose a structured clinical handover in the SBAR/ISBAR framework.'),
    form('care-plan', 'Care Plan Builder', 'A person-centred care plan: goals, interventions, review schedule.'),
    form('risk', 'Clinical Risk Assessment', 'Score a validated tool from its published table (NEWS2 · MUST · Waterlow · NICE CG161 factor count) with AI interpretation. A decision aid.'),
    form('safeguarding', 'Safeguarding Triage', 'Structure the response to a safeguarding concern under the Care Act 2014: immediate safety, category, who to notify, what to record.'),
  ]},
  { name: 'Employment', route: '/employment', tools: [
    { tab: 'studio', kind: 'custom', title: 'Application Studio', desc: 'One flow for a whole application: ingest your documents, target a role, and produce the tailored CV, cover letter and supporting statement together.' },
    form('cv', 'CV / Résumé Tailor', 'Tailor a CV to a target role — achievement-led, ATS-friendly.'),
    form('cover', 'Cover Letter', 'A focused, tailored cover letter with no generic filler.'),
    form('application', 'Application Form & Supporting Statement', 'A criterion-by-criterion supporting statement and form answers from the person specification — never inventing experience.'),
    form('interview', 'Interview Preparation', 'Likely questions plus STAR-method answer frameworks.'),
    form('path', 'Career Path & Skills Gap', 'A development roadmap from your current to your target role, with an honest assessment.'),
    form('salary', 'Salary & Offer Negotiation', 'Market positioning, a target range, negotiation scripts, non-salary levers and BATNA. Reasoned guidance, not live salary data.'),
  ]},
];

export const TOOL_TOTAL = TOOL_REGISTRY.reduce((n, d) => n + d.tools.length, 0);

/** The tools of one hub keyed by tab, so a hub writes `T.research.title` and can never spell its own title differently. */
export function toolsFor(route: string): Record<string, ToolEntry> {
  const d = TOOL_REGISTRY.find(x => x.route === route);
  if (!d) throw new Error(`toolRegistry: no domain at ${route}`);
  return Object.fromEntries(d.tools.map(t => [t.tab, t]));
}
