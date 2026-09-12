import { StartProjectCTA } from '../../components/StartProjectCTA';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, HeartPulse, History } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';

export const CareHub: React.FC = () => {
  const navigate = useNavigate();
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'clinical');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter italic break-words">Sanctuary of Healing</h1>
          <div className="flex items-center gap-4">
             <p className="text-vital font-black uppercase text-[10px] tracking-[0.3em]">Patient Sovereignty • Bio-Digital Mesh • Care Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button type="button" onClick={() => navigate('/reactor?domain=care')} variant="outline"><History size={18} /> Diagnostics</Button>
           <Button type="button" onClick={() => navigate('/projects?realm=care&domain=service&new=1')} className="bg-vital text-white shadow-xl shadow-vital/20">
              <HeartPulse size={18} /> New Patient Twin
           </Button>
        </div>
      </header>
      <StartProjectCTA realm="care" domain="service" />

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-vital" />
               Clinical Engines
            </h3>
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
               <button type="button" onClick={() => setActiveTab('clinical')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'clinical' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Clinical</button>
               <button type="button" onClick={() => setActiveTab('care-plan')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'care-plan' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Care Plan</button>
               <button type="button" onClick={() => setActiveTab('risk')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'risk' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Risk Assess</button>
               <button type="button" onClick={() => setActiveTab('safeguarding')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'safeguarding' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>Safeguarding</button>
               <button type="button" onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-vital shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="care" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-3xl font-black text-white mb-10 uppercase tracking-tighter">Bio-Digital Diagnostic Lab</h3>
                    <QEPImmersiveTools domain="care" />
                 </div>
              </motion.div>
            ) : activeTab === 'care-plan' ? (
              <DomainTool
                title="Care Plan Builder"
                description={<>Describe the person and their needs — Workstation's <span className="text-vital">own</span> AI drafts a structured, person-centred care plan (goals, interventions, review schedule), in-house.</>}
                endpoint="/api/v1/care/care-plan"
                resultKey="care_plan"
                submitLabel="Build care plan"
                fields={[
                  { name: 'patient_profile', label: 'Patient profile (key: value per line)', type: 'keyvalue', default: 'age: \ncondition: \nmobility: ' },
                  { name: 'care_needs', label: 'Care needs (one per line)', type: 'list', placeholder: 'breathlessness management\nfalls prevention' },
                  { name: 'setting', label: 'Setting', type: 'select', options: ['community', 'hospital', 'care_home', 'mental_health'], default: 'community' },
                  { name: 'duration_weeks', label: 'Duration (weeks)', type: 'text', default: '4' },
                  { name: 'care_model', label: 'Care model', type: 'text', default: 'person_centred' },
                ]}
              />
            ) : activeTab === 'risk' ? (
              <DomainTool
                title="Clinical Risk Assessment"
                description={<>Pick a tool and enter the observations — the score is <span className="text-vital">computed in-house from the published table</span> (NEWS2 · MUST · Waterlow; NICE CG161 as a factor count) and shown first; Workstation's own AI interprets it. A decision aid — clinical judgement by a qualified professional is required.</>}
                endpoint="/api/v1/care/risk-assess"
                resultKey="assessment"
                submitLabel="Assess risk"
                renderExtra={(r: any) => r.score && (
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-900 space-y-2" data-testid="care-score">
                    {/* W457 (P1.9) — the computed score renders FIRST; the narrative below is interpretation only */}
                    {r.score.available === false ? (
                      <p className="text-[10px] text-amber-400 font-bold">{r.score.note}</p>
                    ) : (
                      <>
                        <p className="text-sm font-black text-white">{String(r.score.tool).toUpperCase().replace('_', ' ')} {r.score.tool === 'falls_risk' ? 'factor count ' : r.score.complete === false && r.score.total != null ? '≥ ' : ''}{r.score.total ?? '—'}{r.score.band ? <span className={`ml-2 text-[10px] uppercase tracking-widest px-1.5 py-0.5 rounded ${/high|very high|emergency/i.test(r.score.band) ? 'bg-vital/15 text-vital' : /medium|at risk|warranted/i.test(r.score.band) ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>{r.score.band}</span> : null}</p>
                        {r.score.response && <p className="text-[11px] text-slate-300">{r.score.response}</p>}
                        <p className="text-[9px] text-slate-500">{r.score.table} · {r.score.basis}</p>
                        <div className="flex flex-wrap gap-1.5">
                          {Object.entries(r.score.components || {}).map(([k, v]: [string, any]) => (
                            <span key={k} className="text-[9px] px-1.5 py-0.5 rounded bg-slate-900 text-slate-400" title={v.note || ''}>{k.replace(/_/g, ' ')}: {String(v.value)} → <b className="text-white">{v.points}</b></span>
                          ))}
                        </div>
                        {(r.score.missing || []).length > 0 && <p className="text-[10px] text-amber-400 font-bold">Incomplete — missing: {r.score.missing.join(' · ')}. The total is a lower bound{r.score.band ? '' : ' — no band until the missing observations are recorded'}.</p>}
                        {(r.score.warnings || []).length > 0 && <p className="text-[10px] text-amber-300">{r.score.warnings.join(' · ')}</p>}
                        {r.score.note && (r.score.missing || []).length === 0 && <p className="text-[10px] text-slate-500">{r.score.note}</p>}
                      </>
                    )}
                  </div>
                )}
                fields={[
                  { name: 'tool', label: 'Tool', type: 'select', options: ['news2', 'must', 'waterlow', 'falls_risk', 'dementia_care', 'mental_health', 'discharge', 'safeguarding'], default: 'news2' },
                  { name: 'patient_data', label: 'Observations / data (key: value per line)', type: 'keyvalue', default: 'resp_rate: \nspo2: \noxygen: air\nsystolic_bp: \npulse: \ntemp: \nconsciousness: alert' },
                  { name: 'clinical_context', label: 'Clinical context (optional)', type: 'textarea', placeholder: 'e.g. 72yo post-op day 2, query chest infection' },
                ]}
              />
            ) : activeTab === 'safeguarding' ? (
              <DomainTool
                title="Safeguarding Triage"
                description={<>Describe a safeguarding concern — Workstation's <span className="text-vital">own</span> AI structures the right response under the Care Act 2014 (immediate-safety check, category, who to notify, what to record, consent &amp; Making Safeguarding Personal), in-house. Process guidance only — if anyone is in immediate danger, call 999.</>}
                endpoint="/api/v1/care/safeguarding"
                resultKey="guidance"
                submitLabel="Triage concern"
                fields={[
                  { name: 'concern', label: 'Safeguarding concern', type: 'textarea', placeholder: 'e.g. an elderly client has unexplained bruising and seems fearful of a relative who manages their finances' },
                  { name: 'setting', label: 'Setting', type: 'select', options: ['community', 'hospital', 'care_home', 'domiciliary'], default: 'community' },
                  { name: 'person_context', label: 'Context (optional)', type: 'textarea', placeholder: 'adult at risk, capacity, who is involved…' },
                  { name: 'jurisdiction', label: 'Framework', type: 'text', default: 'England (Care Act 2014)' },
                ]}
              />
            ) : (
              <DomainTool
                title="Clinical Handover (SBAR)"
                description={<>Compose a structured clinical handover — Workstation's <span className="text-vital">own</span> AI drafts it using the SBAR/ISBAR framework, in-house.</>}
                endpoint="/api/v1/care/handover"
                resultKey="handover"
                submitLabel="Compose handover"
                fields={[
                  { name: 'patient_summary', label: 'Patient summary', type: 'textarea', placeholder: 'e.g. 72yo M, admitted with community-acquired pneumonia, day 2 post-op' },
                  { name: 'current_situation', label: 'Current situation', type: 'textarea', placeholder: 'e.g. rising NEWS2, new confusion, sats 92% on 2L' },
                  { name: 'background', label: 'Background', type: 'text', placeholder: 'relevant history / admission reason' },
                  { name: 'assessment', label: 'Assessment', type: 'text', placeholder: 'your clinical assessment' },
                  { name: 'recommendation', label: 'Recommendation', type: 'text', placeholder: 'what you recommend / are asking for' },
                  { name: 'handover_type', label: 'Framework', type: 'select', options: ['sbar', 'isbar', 'nursing', 'medical'], default: 'sbar' },
                ]}
              />
            )}
         </div>
      </Card>
    </div>
  );
};
