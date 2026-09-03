import { StartProjectCTA } from '../../components/StartProjectCTA';
import { provenanceBadge } from '../../lib/api';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Landmark, History, ScrollText, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';

export const LawHub: React.FC = () => {
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'compliance');
  const [docText, setDocText] = useState('');
  const [focus, setFocus] = useState('risk');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<{ analysis: string; disclaimer?: string; ai_provenance?: { served_by?: string; is_external?: boolean } } | null>(null);
  const [error, setError] = useState('');

  const analyse = async () => {
    if (!docText.trim()) return;
    setAnalyzing(true); setError(''); setResult(null);
    try {
      const r = await axios.post('/api/v1/law/analyse', { document_text: docText, analysis_focus: focus });
      setResult(r.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Analysis failed — the backend may be unavailable.');
    }
    setAnalyzing(false);
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter uppercase break-words">Bastion of Order</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Legal Framework • Constitutional Mesh • Law Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button type="button" onClick={() => navigate('/projects?realm=law&domain=policy')} variant="outline"><History size={18} /> Precedent</Button>
           <Button type="button" onClick={() => navigate('/projects?realm=law&domain=policy&new=1')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Landmark size={18} /> New Treaty
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
               <button type="button" onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="law" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-3xl font-black text-white mb-10 uppercase tracking-tighter">Constitutional Simulation</h3>
                    <QEPImmersiveTools domain="law" />
                 </div>
              </motion.div>
            ) : activeTab === 'research' ? (
              <DomainTool
                title="Legal Research (IRAC)"
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
                title="Legal Document Drafter"
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
              <div className="space-y-5">
                 <div>
                    <h4 className="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2"><ScrollText size={18} className="text-aura" /> Legal Document Analyser</h4>
                    <p className="text-[11px] text-slate-500 font-bold mt-1 max-w-2xl leading-relaxed">Paste a contract or legal document — Workstation's <span className="text-aura">own</span> AI runs a structured England &amp; Wales analysis (key clauses, risks, missing provisions, recommendations) in-house.</p>
                 </div>
                 <textarea value={docText} onChange={e => setDocText(e.target.value)} rows={6}
                    className="w-full text-xs bg-slate-950 border border-slate-900 rounded-2xl p-4 text-slate-300"
                    placeholder="Paste the legal document text here…" />
                 <div className="flex items-center gap-3 flex-wrap">
                    <select aria-label="Analysis focus" value={focus} onChange={e => setFocus(e.target.value)}
                       className="text-[10px] font-black uppercase bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2">
                       <option value="general">General</option>
                       <option value="risk">Risk</option>
                       <option value="compliance">Compliance</option>
                       <option value="negotiation">Negotiation</option>
                    </select>
                    <Button type="button" onClick={analyse} disabled={analyzing || !docText.trim()} className="bg-aura text-sovereign flex items-center gap-2 text-xs">
                       {analyzing ? <Loader2 size={14} className="animate-spin" /> : <ScrollText size={14} />} Analyse document
                    </Button>
                 </div>
                 {error && <p className="text-vital text-xs font-bold">{error}</p>}
                 {result && (
                    <Card className="p-6 space-y-3">
                       <div className="flex items-center justify-between">
                          <h4 className="text-sm font-black text-white uppercase tracking-wide">Analysis</h4>
                          <span className={`text-[8px] font-black uppercase px-2 py-1 rounded ${result.ai_provenance?.is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                             {provenanceBadge(result.ai_provenance?.served_by, result.ai_provenance?.is_external).label}
                          </span>
                       </div>
                       <pre className="text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed bg-slate-950 border border-slate-900 rounded-xl p-4 max-h-[420px] overflow-y-auto">{result.analysis}</pre>
                       {result.disclaimer && <p className="text-[10px] text-slate-600 italic leading-relaxed">{result.disclaimer}</p>}
                    </Card>
                 )}
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};
