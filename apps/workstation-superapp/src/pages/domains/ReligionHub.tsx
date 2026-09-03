import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Badge, Button } from '@workstation/ui';
import { BookOpen, Heart, Sparkles, MessageCircle, History, Info, ShieldCheck, Zap, Globe, HeartPulse, Network, Binary, Compass, Anchor, Wind, Layers, GraduationCap } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';
import { QEPStudio } from '../../components/QEPStudio';
import { QEPFlagshipFeatures } from '../../components/QEPFlagshipFeatures';
import { LearnTeachModule } from '../../components/LearnTeachModule';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';
import { DomainTool } from '../../components/DomainTool';

interface Madhab { id: string; name: string; region: string; founder: string }

export const ReligionHub: React.FC = () => {
  const navigate = useNavigate();
   const { layout, emotionalAdjustment } = useAdaptiveUI();
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get('tab') || 'wisdom');
  const [madhabs, setMadhabs] = useState<Madhab[]>([]);

  const [schoolsError, setSchoolsError] = useState(false);
  useEffect(() => {
    axios.get('/api/v1/religion/schools')
      .then(res => setMadhabs(res.data.madhabs ?? []))
      .catch(() => setSchoolsError(true));   // W439: a failed fetch used to pulse "Loading…" forever
  }, []);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Spire of Inquiry</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Spiritual Inquiry • Ethical Guidance Channel • Religion Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => navigate('/projects?realm=religion&domain=content')} variant="outline"><History size={18} /> Tradition</Button>
           <Button onClick={() => navigate('/ceo')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Sparkles size={18} /> Seek Guidance
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <div className="@[440px]:col-span-8 space-y-10">
            <Card className="h-[500px] flex flex-col justify-center items-center relative overflow-hidden bg-aura/5 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     Sacred Knowledge Garden
                     <Badge color="aura">Wisdom-Mesh</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Global Spiritual Networks • compassion-first</p>
               </div>

               <div className="relative z-10 flex flex-col items-center gap-8">
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 60, ease: "linear" }}>
                     <Compass size={180} className="text-aura opacity-20" />
                  </motion.div>
                  <HeartPulse size={120} className="text-aura opacity-40 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse-slow" />
               </div>

               {/* W411 — "Active Alliances 42" and "Moral Resonance 0.99" were rendered here as
                   live figures. Nothing counts alliances and nothing measures moral resonance;
                   both were literals. No real source exists for either, so neither is shown. */}
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <BookOpen size={24} className="text-aura" />
                     Scholarly Operations
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button type="button" onClick={() => setActiveTab('wisdom')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'wisdom' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Wisdom</button>
                     <button type="button" onClick={() => setActiveTab('dialogue')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'dialogue' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Dialogue</button>
                     <button type="button" onClick={() => setActiveTab('tafsir')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'tafsir' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Tafsir</button>
                     <button type="button" onClick={() => setActiveTab('halal')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'halal' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Halal Review</button>
                     <button type="button" onClick={() => setActiveTab('hadith')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'hadith' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Hadith</button>
                     <button type="button" onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
                  </div>
               </div>

               <div className="space-y-4">
                  {activeTab === 'qep' ? (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                       {/* W439 — the Owner's directive: the REAL Quran Education Platform lives in
                           the Religion domain. QEPStudio is the wired, audited surface (authentic
                           text, real SM-2 hifz, honest written-recall, provenance-labelled AI).
                           The generic four-engine QEPDashboard filler left this tab. */}
                       <div>
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-6">
                             <BookOpen size={28} className="text-aura" />
                             Quran Education Platform
                          </h3>
                          <QEPStudio />
                       </div>

                       <div className="pt-12 border-t border-white/5">
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-10">
                             <GraduationCap size={28} className="text-highlight" />
                             Learn-Teach Ecosystem
                          </h3>
                          <LearnTeachModule />
                       </div>

                       <div className="pt-12 border-t border-white/5">
                          <h3 className="text-3xl font-black text-white flex items-center gap-4 uppercase tracking-tighter mb-10">
                             <Sparkles size={28} className="text-aura shadow-2xl shadow-aura/20" />
                             Roadmap — modules not yet built (honestly labelled)
                          </h3>
                          <QEPFlagshipFeatures />
                       </div>
                    </motion.div>
                  ) : activeTab === 'dialogue' ? (
                    <DomainTool
                      title="Comparative Fiqh Research"
                      description={<>Pose a question of Islamic jurisprudence — Workstation's <span className="text-aura">own</span> AI researches it within your chosen madhab, in-house, with scholarly humility.</>}
                      endpoint="/api/v1/religion/fatwa-research"
                      resultKey="research"
                      submitLabel="Research question"
                      fields={[
                        { name: 'question', label: 'Question', type: 'textarea', placeholder: 'e.g. What are the conditions for combining prayers when travelling?' },
                        { name: 'madhab', label: 'Madhab (school of jurisprudence)', type: 'select', options: ['hanafi', 'maliki', 'shafi', 'hanbali', 'jafari'], default: 'hanafi' },
                        { name: 'context', label: 'Context (optional)', type: 'text', placeholder: 'geographic / circumstantial context' },
                      ]}
                    />
                  ) : activeTab === 'tafsir' ? (
                    <DomainTool
                      title="Qur'anic Tafsir"
                      description={<>Study an ayah — Workstation's <span className="text-aura">own</span> AI offers structured tafsir (classical, thematic, contemporary or linguistic), in-house, drawing on the classical mufassirun.</>}
                      endpoint="/api/v1/religion/quran-tafsir"
                      resultKey="tafsir"
                      submitLabel="Generate tafsir"
                      fields={[
                        { name: 'surah', label: 'Surah (1–114)', type: 'text', default: '1' },
                        { name: 'ayah_start', label: 'Ayah (start)', type: 'text', default: '1' },
                        { name: 'ayah_end', label: 'Ayah (end — 0 for a single ayah)', type: 'text', default: '0' },
                        { name: 'tafsir_approach', label: 'Approach', type: 'select', options: ['classical', 'thematic', 'contemporary', 'linguistic'], default: 'classical' },
                      ]}
                    />
                  ) : activeTab === 'halal' ? (
                    <DomainTool
                      title="Halal Certification Pre-Assessment"
                      description={<>Describe a product — Workstation's <span className="text-aura">own</span> AI gives a halal pre-assessment (ingredient flags, process concerns, certification guidance), in-house, with scholarly humility.</>}
                      endpoint="/api/v1/religion/halal-review"
                      resultKey="assessment"
                      submitLabel="Assess product"
                      fields={[
                        { name: 'product_name', label: 'Product name', type: 'text', placeholder: 'e.g. Fruit gummy sweets' },
                        { name: 'product_description', label: 'Product description', type: 'textarea', placeholder: 'what the product is and how it is used' },
                        { name: 'ingredients', label: 'Ingredients (one per line)', type: 'list', placeholder: 'bovine gelatin\nglucose syrup\ncitric acid' },
                        { name: 'manufacturing_process', label: 'Manufacturing process (optional)', type: 'text', placeholder: 'e.g. boiled, moulded, coated' },
                        { name: 'target_markets', label: 'Target markets (one per line)', type: 'list', placeholder: 'UK\nMalaysia' },
                      ]}
                    />
                  ) : activeTab === 'hadith' ? (
                    <DomainTool
                      title="Hadith Study (Ulum al-Hadith)"
                      description={<>Enter a hadith (text or reference) — Workstation's <span className="text-aura">own</span> AI researches its narration, isnad, grading and sharh, in-house, with scholarly humility. Research only — grading must be verified against authenticated collections and a qualified scholar.</>}
                      endpoint="/api/v1/religion/hadith-study"
                      resultKey="study"
                      submitLabel="Study hadith"
                      fields={[
                        { name: 'hadith', label: 'Hadith (text or reference)', type: 'textarea', placeholder: 'e.g. "Actions are but by intentions" — or Bukhari 1' },
                        { name: 'focus', label: 'Focus', type: 'select', options: ['authentication', 'explanation', 'thematic'], default: 'authentication' },
                        { name: 'madhab', label: 'Jurisprudential lens (optional)', type: 'select', options: ['', 'hanafi', 'maliki', 'shafi', 'hanbali', 'jafari'], default: '' },
                      ]}
                    />
                  ) : madhabs.length > 0 ? madhabs.map((madhab, i) => (
                    <motion.div
                      key={madhab.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                             <Heart size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{madhab.name}</p>
                             <div className="flex items-center gap-4">
                                <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{madhab.region}</span>
                                <span className="text-[10px] font-mono text-aura/50">{madhab.founder}</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-6">
                          {/* W439 — an "Active" badge sat on every madhab row; madhabs are static
                              reference data, not live entities with a state */}
                          <Button onClick={() => navigate('/qep')} variant="outline" className="px-6">Explore</Button>
                       </div>
                    </motion.div>
                  )) : schoolsError ? (
                    <div className="text-center py-8 text-amber-400 text-sm">Backend unreachable — jurisprudential reference data could not be loaded.</div>
                  ) : (
                    <div className="text-center py-8 text-slate-600 text-sm animate-pulse">Loading jurisprudential traditions…</div>
                  )}
               </div>
            </Card>
         </div>

         <div className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <ShieldCheck size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Ethical Guidance</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Moral alignment checks run through the real §11 compliance engines (Halal/Sharia · Ethical).
                  </p>
               </div>
               {/* W439 — an "Alignment Score OPTIMAL" row with a 98% bar sat here, directly under
                   copy claiming the real §11 engines. Both figures were literals: nothing computed
                   an alignment score for this page. Removed rather than replaced — the real
                   compliance checks run per-entity in the §11 engines, not as a page decoration. */}
               <Button onClick={() => navigate('/ceo')} className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black uppercase tracking-widest text-xs">Consult Ethics Council</Button>
            </Card>

            {/* W439 — two fabrication cards sat here: "Spiritual Markers (Methylation)" with
                COMPASSION_STRICT SET / CONTEMPLATION_MODE ACTIVE badges (nothing sets or reads
                either), and "Interfaith Mesh — 142 Global Nodes Synchronized" (nothing counts
                nodes and no mesh exists — the same fabricated-figure class the browser smoke
                bans). Removed rather than replaced: no real source exists for any of it. */}
         </div>
      </div>
    </div>
  );
};
