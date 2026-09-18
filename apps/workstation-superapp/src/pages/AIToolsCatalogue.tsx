import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from '@workstation/ui';
import { Scale, Microscope, HeartPulse, GraduationCap, Heart, Briefcase, Sparkles, ArrowRight } from 'lucide-react';
import { TOOL_REGISTRY, TOOL_TOTAL, DomainTools } from '../lib/toolRegistry';

// A single front door to every in-house AI tool. Each links straight to its hub + tab (?tab=).
// W470 — every entry and every count comes from the ONE tool registry the hubs mount from
// (src/lib/toolRegistry.ts); this file adds only the icons. The suite fails when a hub and the
// registry disagree.
// All tools run on Workstation's OWN native fabric (honest in-house provenance) and are runnable,
// iteratively refinable, and exportable (Copy / Download .md).
const ICONS: Record<string, React.ComponentType<any>> = {
  Law: Scale, Science: Microscope, Care: HeartPulse, Education: GraduationCap, Religion: Heart, Employment: Briefcase,
};
const DOMAINS: DomainTools[] = TOOL_REGISTRY;
const TOTAL = TOOL_TOTAL;
const KIND_LABEL: Record<string, string> = { custom: 'surface', flagship: 'flagship' };
const FORMS = DOMAINS.reduce((n, d) => n + d.tools.filter(t => t.kind === 'form').length, 0);
const SURFACES = DOMAINS.reduce((n, d) => n + d.tools.filter(t => t.kind === 'custom').length, 0);

export const AIToolsCatalogue: React.FC = () => (
  <div className="space-y-10 pb-24">
    <header>
      <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · In-House AI</p>
      <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">AI Tools</h1>
      <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
        {TOTAL} tools across {DOMAINS.length} domains, every one on Workstation's
        <span className="text-highlight"> own</span> native AI fabric (honest in-house provenance, never an external dependency):
        {FORMS} form tools whose output is <span className="text-aura">runnable, iteratively refinable, and exportable</span> (Copy / Download),
        {SURFACES} hand-built surfaces, and the Religion domain's QEP flagship — each labelled below.
      </p>
    </header>

    {DOMAINS.map(d => {
      const Icon = ICONS[d.name] ?? Sparkles;
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
                  <p className="font-black text-white text-sm flex items-center gap-2"><Sparkles size={13} className="text-aura" /> {t.title}
                    {KIND_LABEL[t.kind] && <span className="text-[8px] font-black uppercase tracking-widest text-slate-500 border border-slate-800 rounded px-1.5 py-0.5">{KIND_LABEL[t.kind]}</span>}</p>
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
