import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import { Heart, Microscope, GraduationCap, Scale, HeartPulse, Briefcase, Sparkles, Rocket, ArrowRight } from 'lucide-react';
import { useT } from '../../lib/i18n';

// Offering 1 (WHOLE_VISION §3A) — the Domains section's front door: domain-specific AI-mediated tools &
// resources for working in any domain/realm, usable directly without establishing an enterprise. All
// tools run on Workstation's OWN native fabric (honest in-house provenance). The full launcher with every
// tool + tab lives at /ai-tools; this page frames the offering and routes into each domain hub.
interface Domain { name: string; route: string; icon: React.ComponentType<any>; tools: number; blurb: string }

const DOMAINS: Domain[] = [
  { name: 'Religion', route: '/religion', icon: Heart, tools: 4, blurb: 'Comparative fiqh research, Qur’anic tafsir, halal pre-assessment.' },
  { name: 'Science', route: '/science', icon: Microscope, tools: 3, blurb: 'Research synthesis into structured evidence; literature-review mapping.' },
  { name: 'Education', route: '/education', icon: GraduationCap, tools: 4, blurb: 'Lesson plans, framework-aligned curricula, assessments with mark schemes.' },
  { name: 'Law', route: '/law', icon: Scale, tools: 2, blurb: 'Contract/document analysis for risks; clause-numbered document drafting.' },
  { name: 'Care', route: '/care', icon: HeartPulse, tools: 4, blurb: 'SBAR clinical handover, person-centred care plans, validated risk scoring.' },
  { name: 'Employment', route: '/employment', icon: Briefcase, tools: 6, blurb: 'CV tailoring, cover letters, applications, interview prep, career pathing.' },
];
const TOTAL = DOMAINS.reduce((n, d) => n + d.tools, 0);

export const DomainsHub: React.FC = () => {
  const navigate = useNavigate();
  const { t, rtl } = useT();
  return (
    <div dir={rtl ? 'rtl' : undefined} className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2">{t('domains.eyebrow', 'Workstation IDBO · Offering 1')}</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">{t('domains.title', 'Domains')}</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          <span className="text-aura">{t('domains.intro.lead', 'Domain-specific AI-mediated tools & resources')}</span> for working across every
          domain and realm — research, analyse, generate, plan, assess, author, design. Use them directly, on demand,
          with honest in-house AI provenance. No enterprise required.
        </p>
      </header>

      {/* The two ways Workstation IDBO serves you (§3A) */}
      <div className="grid grid-cols-1 @[760px]:grid-cols-2 gap-4">
        <Card className="p-6 border-aura/40 bg-aura/5">
          <div className="flex items-center gap-2 mb-2"><Sparkles size={16} className="text-aura" /><h3 className="text-xs font-black uppercase tracking-widest text-aura">{t('domains.off1.tag', 'Offering 1 · You are here')}</h3></div>
          <p className="text-sm font-black text-white mb-1">{t('domains.off1.title', 'Work now with domain tools')}</p>
          <p className="text-[11px] text-slate-400 leading-relaxed">Get best-in-class capability on demand inside your domain — without building an enterprise. {TOTAL} tools across {DOMAINS.length} domains.</p>
        </Card>
        <Card className="p-6 border-highlight/30 hover:border-highlight/60 transition-colors cursor-pointer" onClick={() => navigate('/genesis')}>
          <div className="flex items-center gap-2 mb-2"><Rocket size={16} className="text-highlight" /><h3 className="text-xs font-black uppercase tracking-widest text-highlight">{t('domains.off2.tag', 'Offering 2')}</h3></div>
          <p className="text-sm font-black text-white mb-1 flex items-center gap-2">{t('domains.off2.title', 'Establish a living enterprise')} <ArrowRight size={14} className="text-highlight" /></p>
          <p className="text-[11px] text-slate-400 leading-relaxed">Go end-to-end — Concept → Commercialisation — and establish a self-running VSB IDBO enterprise that delivers and forever evolves a whole solution.</p>
        </Card>
      </div>

      {/* The six domains */}
      <div>
        <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">{t('domains.six', 'The six domains')}</h3>
          <Button onClick={() => navigate('/ai-tools')} className="bg-aura text-sovereign text-xs flex items-center gap-2"><Sparkles size={13} /> {t('domains.browseAll', 'Browse all')} {TOTAL} {t('domains.tools', 'tools')}</Button>
        </div>
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-3">
          {DOMAINS.map(d => (
            <Card key={d.route} className="p-5 hover:border-aura/40 transition-colors cursor-pointer group" onClick={() => navigate(d.route)}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center group-hover:border-aura/40">
                    <d.icon size={16} className="text-aura" />
                  </div>
                  <p className="font-black text-white text-sm uppercase tracking-wide">{t(`nav.${d.route.slice(1)}`, d.name)}</p>
                </div>
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-600">{d.tools} {t('domains.tools', 'tools')}</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">{d.blurb}</p>
              <p className="mt-3 text-[10px] font-black uppercase tracking-widest text-aura/70 flex items-center gap-1 group-hover:text-aura">{t('domains.open', 'Open')} {t(`nav.${d.route.slice(1)}`, d.name)} <ArrowRight size={11} /></p>
            </Card>
          ))}
        </div>
      </div>

      <p className="text-[10px] text-slate-600 leading-relaxed max-w-2xl">
        Every tool runs on Workstation IDBO’s own native AI fabric (in-house-first; external providers are optional
        accelerants, never dependencies) and is runnable, iteratively refinable, and exportable (Copy / Download .md).
      </p>
    </div>
  );
};
