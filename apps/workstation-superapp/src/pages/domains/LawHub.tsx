import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Landmark, History } from 'lucide-react';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import MatterAssemblyPanel from '../../components/MatterAssemblyPanel';
import { DomainTool } from '../../components/DomainTool';
import { toolsFor } from '../../lib/toolRegistry';

export const LawHub: React.FC = () => {
  const T = toolsFor('/law');   // W470 — the one tool registry the front doors count from
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'compliance');
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase break-words">Bastion of Order</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Law Hub • the tools are in the tabs below</p>
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

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-aura" />
               Legislative Engines
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
                description={<>Ask a legal question — Workstation's <span className="text-aura">own</span> AI researches it via the IRAC method (Issue · Relevant Law · Application · Conclusion) with practical steps, risks and next actions, in-house. Informational only — not legal advice.</>}
                endpoint="/api/v1/law/research"
                resultKey="analysis"
                submitLabel="Research question"
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
                description={<>Pick a template — Workstation's <span className="text-aura">own</span> AI drafts the full document (clause-numbered Markdown) for your parties and jurisdiction, in-house.</>}
                endpoint="/api/v1/law/generate"
                resultKey="document"
                submitLabel="Draft document"
                fields={[
                  { name: 'template_id', label: 'Template', type: 'select', options: ['nda', 'employment_contract', 'service_agreement', 'partnership_deed', 'privacy_policy', 'terms_of_service', 'ip_assignment', 'et1_claim', 'cease_desist', 'data_processing_agreement'], default: 'nda' },
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
                description={<>Paste a contract or legal document — Workstation's <span className="text-aura">own</span> AI runs a structured England &amp; Wales analysis (key clauses, risks, missing provisions, recommendations) in-house.</>}
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
      {/* P3.23 — the matter specialist: provenance per particular, refused authorities, unresolved checks */}
      <Card className="p-6">
        <MatterAssemblyPanel />
      </Card>
    </div>
  );
};
