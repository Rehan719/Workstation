import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Landmark, History } from 'lucide-react';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import MatterAssemblyPanel from '../../components/MatterAssemblyPanel';
import StatutePanel from '../../components/StatutePanel';
import TimeLimitPanel from '../../components/TimeLimitPanel';   // W875 (FU-1012)
import { DomainTool } from '../../components/DomainTool';
import { toolsFor } from '../../lib/toolRegistry';
import { useServingStatus, servingIsFloor } from '../../components/ServingNow';   // W866 (FU-1013)
import { apiJson, ApiError, errorMessage } from '../../lib/api';   // W996

//  W996 (FU-399 part 28) - a refusal says the server's status and reason, an unreachable server says that, and a
//  sentence of this page's own (an empty list) stands as written
const readFailure = (e: unknown) => (e instanceof ApiError || e instanceof TypeError ? errorMessage(e)
  : String((e as { message?: string } | null)?.message ?? e));

export const LawHub: React.FC = () => {
  const T = toolsFor('/law');   // W470 — the one tool registry the front doors count from
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'compliance');
  // W825 (FU-862) - the templates the API lists (GET /api/v1/law/templates had no caller), with the one it HOLDS for a
  // qualified read said on the page. A failed read is said, and the typed ids are offered.
  const [templates, setTemplates] = useState<string[] | null>(null);
  const [templateNames, setTemplateNames] = useState<Record<string, string>>({});
  const [templatesHeld, setTemplatesHeld] = useState<{ templates?: string[]; reason?: string } | null>(null);
  const [templatesNote, setTemplatesNote] = useState('');
  useEffect(() => {
    let alive = true;
    //  W996 - this threw `HTTP ${r.status}`, so a refusal lost its reason and a body that was not JSON said a parse error
    apiJson('/api/v1/law/templates')
      .then(d => {
        if (!alive) return;
        const list = Array.isArray(d?.templates) ? d.templates : [];
        const ids = list.map((t: any) => String(t?.id ?? '')).filter(Boolean);
        if (ids.length === 0) throw new Error('the list came back empty');
        const names: Record<string, string> = {};
        list.forEach((t: any) => { if (t?.id && t?.name) names[String(t.id)] = String(t.name); });
        setTemplates(ids); setTemplateNames(names); setTemplatesHeld(d?.held ?? null); setTemplatesNote('');
      })
      .catch(e => { if (alive) { setTemplates(null); setTemplatesNote(`The template list could not be read (${readFailure(e)}), so the templates typed on this page are offered and which is held is not known.`); } });
    return () => { alive = false; };
  }, []);
  // W866 (FU-1013) - WHAT THIS MACHINE DOES IN LAW, said before any form: the server's list of the tools that call
  // no model, which come first on this page, and for each form the sentence its answer carries when no model
  // composed it. Whether a model is serving now is the one status read the forms below also show. A failed read
  // is said, and nothing is claimed in its place.
  const serving = useServingStatus();
  const [lawTools, setLawTools] = useState<{ needs_no_model?: any[]; needs_a_model?: any[]; basis?: string } | null>(null);
  const [lawToolsNote, setLawToolsNote] = useState('');
  useEffect(() => {
    let alive = true;
    apiJson('/api/v1/law/tools')   // W996 - through apiJson, as the template list
      .then(d => { if (alive) { setLawTools(d); setLawToolsNote(''); } })
      .catch(e => { if (alive) { setLawTools(null); setLawToolsNote(`What each Law tool does could not be read (${readFailure(e)}), so nothing is said about it here. Each answer still says what composed it.`); } });
    return () => { alive = false; };
  }, []);
  const floorNow = serving ? servingIsFloor(serving) : null;
  const formsNow = serving === undefined ? ''
    : serving === null ? 'Whether one is serving could not be read just now, so what each returns without one is said here.'
    : floorNow ? 'None is serving on this deployment now, so each returns what is said here.'
    : `One is serving now (${serving.active_model_label || 'a local model'}): each returns that model's draft, which no person has reviewed and which is not legal advice.`;
  const showWithoutModel = serving === null || floorNow === true;
  // the forms whose answers carry the same sentence are named together, so the sentence is said once
  const withoutModel: [string, string[]][] = [];
  (lawTools?.needs_a_model ?? []).forEach((f: any) => {
    const title = T[String(f.id)]?.title ?? String(f.id);
    const at = withoutModel.find(([s]) => s === f.when_no_model_serves);
    if (at) at[1].push(title); else withoutModel.push([String(f.when_no_model_serves ?? ''), [title]]);
  });
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase break-words">Bastion of Order</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Law Hub • the tools that need no model come first</p>
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
           <Button type="button" onClick={() => navigate('/projects?realm=law&domain=policy')} variant="outline"><History size={18} /> Law projects</Button>
           <Button type="button" onClick={() => navigate('/projects?realm=law&domain=policy&new=1')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Landmark size={18} /> Start a law project
           </Button>
        </div>
      </header>
      <StartProjectCTA realm="law" domain="policy" />

      {/* W866 (FU-1013) - WHAT THIS MACHINE DOES IN LAW, before any form. The tools that call no model come first and
          work now; the forms say, before they are filled, what their answer is when no model composes it, in the
          server's own sentence - the one the answer carries. */}
      <Card className="p-6 space-y-3" data-testid="law-what-runs-here">
        <h3 className="text-sm font-black text-white uppercase tracking-widest">What this machine does in Law</h3>
        {lawToolsNote && <p data-testid="law-tools-note" className="text-[11px] text-amber-300/90">{lawToolsNote}</p>}
        {lawTools && (
          <>
            <p className="text-[11px] text-slate-400" title={lawTools.basis}>These call no model and work now. They are the first tools on this page:</p>
            <ul className="space-y-1">
              {(lawTools.needs_no_model ?? []).map((t: any) => (
                <li key={t.id} data-testid="law-no-model-tool" className="text-[11px] text-slate-300">
                  <span className="font-bold text-white">{t.name}</span>: {t.does} {t.does_not}
                </li>
              ))}
            </ul>
            {/* W996 - "The three forms" was typed; the count is the server's list's */}
            {(() => { const n = (lawTools.needs_a_model ?? []).length; return (
              <p data-testid="law-forms-need-a-model" className="text-[11px] text-slate-400">
                {n === 0 ? 'No form further down needs a model.' : `The ${n === 1 ? 'one form' : `${n} forms`} further down need${n === 1 ? 's' : ''} a model.`} {formsNow}
              </p>); })()}
            {showWithoutModel && withoutModel.map(([sentence, titles]) => (
              <p key={sentence} data-testid="law-form-without-model" className="text-[11px] text-amber-300/90">
                {titles.join(' and ')}, with no model: {sentence}
              </p>
            ))}
          </>
        )}
      </Card>
      {/* W724 (plan item P5.20) - one provision of an Act, word for word from its publisher, and where help is */}
      <Card className="p-6">
        <StatutePanel />
      </Card>
      {/* W875 (FU-1012) - how long a time limit runs: arithmetic on the rule's own words, and who to ask */}
      <Card className="p-6">
        <TimeLimitPanel />
      </Card>
      {/* P3.23 — the matter specialist: provenance per particular, refused authorities, unresolved checks */}
      <Card className="p-6">
        <MatterAssemblyPanel />
      </Card>

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-aura" />
               Forms that need a model
            </h3>
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
               <button type="button" onClick={() => setActiveTab('compliance')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'compliance' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Compliance</button>
               <button type="button" onClick={() => setActiveTab('draft')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'draft' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Draft</button>
               <button type="button" onClick={() => setActiveTab('research')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'research' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Research</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'research' ? (
              <DomainTool
                title={T['research'].title}
                description={<>Ask a legal question. With a model serving, Workstation's <span className="text-aura">own</span> AI composes an answer under the IRAC headings (Issue · Relevant Law · Application · Conclusion) with practical steps, risks and next actions, in-house. Informational only — not legal advice.</>}
                endpoint="/api/v1/law/research"
                resultKey="analysis"
                submitLabel="Research question"
                renderExtra={(r: any) => Array.isArray(r?.routed_to_people) && r.routed_to_people.length > 0 ? (
                  /* W874 (FU-1082) - a question about the person's own case is routed to people: who they are */
                  <div data-testid="law-routed-to-people" className="p-3 rounded-xl bg-slate-950 border border-amber-500/30 space-y-1">
                    <p className="text-[10px] font-bold text-amber-300">Help from a person</p>
                    <ul className="space-y-1">
                      {r.routed_to_people.map((h: any) => (
                        <li key={h.link} className="text-[10px] text-slate-300"><a href={h.link} target="_blank" rel="noreferrer" className="underline text-sky-400">{h.name}</a> - {h.for_what}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                fields={[
                  { name: 'question', label: 'Legal question', type: 'textarea', placeholder: 'e.g. Can an employer enforce a 12-month non-compete clause against a junior employee?' },
                  { name: 'area_of_law', label: 'Area of law', type: 'select', options: ['general', 'contract', 'employment', 'intellectual property', 'data protection', 'dispute resolution', 'company', 'property', 'consumer'], default: 'general' },
                  { name: 'jurisdiction', label: 'Jurisdiction', type: 'text', default: 'England & Wales' },
                  { name: 'context', label: 'Context / facts (optional)', type: 'textarea', placeholder: 'Any relevant facts or background…' },
                ]}
              />
            ) : activeTab === 'draft' ? (
              <DomainTool
                title={T['draft'].title}
                description={<>Pick a template. With a model serving, Workstation's <span className="text-aura">own</span> AI drafts the full document (clause-numbered Markdown) for your parties and jurisdiction, in-house.
                  {(templatesHeld?.templates ?? []).length > 0 && (
                    <span className="block text-[10px] text-amber-400 mt-1" data-testid="law-templates-held">
                      Held for a qualified read: {(templatesHeld!.templates ?? []).map(t => templateNames[t] ?? t).join(', ')} - {templatesHeld!.reason}
                    </span>
                  )}
                  {templatesNote && <span className="block text-[10px] text-amber-400 mt-1" data-testid="law-templates-note">{templatesNote}</span>}</>}
                endpoint="/api/v1/law/generate"
                resultKey="document"
                submitLabel="Draft document"
                fields={[
                  { name: 'template_id', label: 'Template', type: 'select', options: (templates && templates.length > 0 ? templates : ['nda', 'employment_contract', 'service_agreement', 'partnership_deed', 'privacy_policy', 'terms_of_service', 'ip_assignment', 'et1_claim', 'cease_desist', 'data_processing_agreement']), optionLabels: templateNames, default: 'nda' },
                  { name: 'parties', label: 'Parties (key: value per line)', type: 'keyvalue', default: 'party_a: \nparty_b: ' },
                  { name: 'custom_instructions', label: 'Custom instructions (optional)', type: 'textarea', placeholder: 'e.g. 2-year term, mutual confidentiality, governed by English law' },
                  { name: 'jurisdiction', label: 'Jurisdiction', type: 'text', default: 'England & Wales' },
                ]}
              />
            ) : (
              /* W662 (FU-726) - the shared tool component, like every other form tool on this hub: the compliance
                 verdict and the floor note the response carries are shown, and the output can be copied,
                 downloaded, refined and saved to My Work. It was a hand-built form that showed none of those. */
              <DomainTool
                title={T['compliance'].title}
                description={<>Paste a contract or legal document. With a model serving, Workstation's <span className="text-aura">own</span> AI composes a structured England &amp; Wales analysis (key clauses, risks, missing provisions, recommendations), in-house.</>}
                endpoint="/api/v1/law/analyse"
                resultKey="analysis"
                submitLabel="Analyse document"
                fields={[
                  { name: 'document_text', label: 'Legal document text', type: 'textarea', placeholder: 'Paste the legal document text here…' },
                  { name: 'analysis_focus', label: 'Analysis focus', type: 'select', options: ['general', 'risk', 'compliance', 'negotiation'], default: 'risk' },
                ]}
              />
            )}
         </div>
      </Card>
    </div>
  );
};
