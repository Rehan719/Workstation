import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Search, FileText, Shield, Activity, Globe, Brain, Sparkles, Loader2, BookOpen, FlaskConical, Scale } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@workstation/ui';

// The live /api/v1/intelligence/insights payload uses { id, type, title, detail, score };
// earlier richer fields (domain/summary/confidence/…) may be absent, so every field is optional
// and read defensively below.
interface InsightItem {
  title?: string;
  type?: string;
  detail?: string;
  score?: number;
  score_basis?: string;   // W489 — the API says what the score IS (a salience weight)
  summary?: string;
  domain?: string;
  confidence?: number;
  projects_count?: number;
  outputs_count?: number;
}

// W578 (FU-394) — DECLARED AGAINST THE ROUTE, measured rather than assumed. This declared
// `generated_at` and `portfolio_size`; the route sends `computed_at` and `total_projects` and has never
// sent either of those two. So the provenance chip below — "Derived from N projects" — was gated on a
// field that is always undefined and HAS NEVER ONCE RENDERED, which is exactly the class W489 fixed in
// this same file when it found three other fields the API never sends: it corrected three and left two.
// `error` was being read through `(data as any)` even after W576 made it load-bearing, and
// `score_meaning` had no declaration at all, which is how it reached no surface.
interface IntelligenceInsights {
  insights: InsightItem[];
  computed_at: number;
  total_projects: number | null;     // null on the crash branch: nothing was counted
  error: string | null;
  score_meaning?: string;
}

const DOMAIN_META: Record<string, { icon: React.ElementType; description: string; color: string }> = {
  AI: { icon: Brain,      description: 'Alignment, constitutional safety, and cognitive architecture.',    color: 'text-aura' },
  Science: { icon: FlaskConical, description: 'Research synthesis, lab automation, and discovery pipelines.', color: 'text-blue-400' },
  Law: { icon: Scale,     description: 'Constitutional governance, compliance, and policy frameworks.',     color: 'text-purple-400' },
  Enterprise: { icon: Activity,  description: 'Business model generation, strategy, and commercialisation.',    color: 'text-emerald-400' },
  Security: { icon: Shield,    description: 'Post-quantum cryptography, threat intelligence, node defense.',   color: 'text-red-400' },
  Global: { icon: Globe,     description: 'Interfaith dialogue, cross-domain synthesis, civilizational data.',color: 'text-yellow-400' },
};

function coeFromInsight(insight: InsightItem, idx: number) {
  const domainLabel = insight.domain ?? insight.type ?? '';
  const title = insight.title ?? '';
  const domainKey = Object.keys(DOMAIN_META).find(k =>
    domainLabel.toLowerCase().includes(k.toLowerCase()) ||
    title.toLowerCase().includes(k.toLowerCase())
  ) ?? Object.keys(DOMAIN_META)[idx % Object.keys(DOMAIN_META).length];
  const meta = DOMAIN_META[domainKey];
  const label = domainLabel || domainKey;
  return {
    name: title && title.length <= 30 ? title : `${label.charAt(0).toUpperCase()}${label.slice(1)} CoE`,
    description: insight.summary ?? insight.detail ?? '',
    icon: meta.icon,
    color: meta.color,
    // W489 (sweep S13.2, C3) — `articles` and `scholars` were computed from THREE FIELDS THE API
    // NEVER SENDS. /api/v1/intelligence/insights emits exactly id, type, title, detail and score;
    // projects_count, outputs_count and confidence do not exist on it. So every card showed the same
    // two numbers — a zero output count, and a confidence of 1 that came only from a floor applied to
    // a zero, which reads like a measurement. The one real per-insight number is `score`,
    // which was rendered nowhere.
    //   (refutation) But `score` is not a measurement either: three of the four insights carry a
    // fixed constant and the fourth scales with the project count, so rendering it as "Insight
    // score" would have been the same defect in a new name. It is shown as the SALIENCE WEIGHT it
    // is, with the API's own basis on hover.
    score: typeof insight.score === 'number' ? insight.score : null,
    scoreBasis: insight.score_basis ?? null,
    domain: label,
  };
}

export const KnowledgeHub: React.FC = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');

  const { data, isLoading } = useQuery<IntelligenceInsights>({
    queryKey: ['intelligence-insights'],
    queryFn: () => axios.get<IntelligenceInsights>('/api/v1/intelligence/insights').then(r => r.data),
    staleTime: 60_000,
    retry: 1,
    refetchOnWindowFocus: false,
  });

  const coes = data?.insights?.length
    ? data.insights.map(coeFromInsight)
    : [
        // W489 — the standing centres, shown when no insight has been computed yet. They carry NO
        // score, because none has been computed for them; the card says so rather than showing a 0.
        { name: 'AI Ethics', description: 'Alignment and constitutional safety protocols.', icon: Brain, color: 'text-aura', score: null, scoreBasis: null, domain: 'ai' },
        { name: 'Data Science', description: 'Neural synthesis and graph analytics.', icon: Activity, color: 'text-blue-400', score: null, scoreBasis: null, domain: 'science' },
        { name: 'Security', description: 'Post-quantum cryptography and node defense.', icon: Shield, color: 'text-red-400', score: null, scoreBasis: null, domain: 'security' },
        { name: 'Global Affairs', description: 'Cross-domain synthesis and interfaith dialogue.', icon: Globe, color: 'text-yellow-400', score: null, scoreBasis: null, domain: 'global' },
      ];

  const filtered = coes.filter(c => (c.name ?? '').toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-4xl @[680px]:text-5xl font-black mb-3 tracking-tight neon-text">Centers of Excellence</h1>
          <p className="text-slate-500 font-bold">Federated knowledge hubs derived from live portfolio intelligence.</p>
        </div>
        <Button onClick={() => navigate('/synthesis')} className="bg-aura text-sovereign shrink-0">
          <Sparkles size={16} /> Generate Insight
        </Button>
      </header>

      <div className="relative max-w-2xl">
        <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-aura" size={20} />
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search CoE knowledge base…"
          className="w-full bg-surface/50 border border-white/10 rounded-2xl py-5 pl-14 pr-8 text-xl focus:outline-none focus:border-aura transition-all shadow-2xl backdrop-blur-xl font-bold"
        />
      </div>

      {isLoading && (
        <div className="flex items-center gap-3 text-slate-500">
          <Loader2 className="animate-spin" size={18} /> Deriving CoEs from live portfolio…
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-4 gap-8">
        <AnimatePresence>
          {filtered.map((coe, i) => (
            <motion.div
              layout
              key={coe.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: i * 0.05 }}
              className="p-8 glass-card group cursor-pointer"
              onClick={() => navigate(`/projects?domain=${coe.domain}`)}
            >
              <div className={`w-14 h-14 rounded-2xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-aura group-hover:text-sovereign transition-all duration-500 shadow-lg ${coe.color}`}>
                <coe.icon size={28} />
              </div>
              <h3 className="text-xl font-black mb-2 tracking-tight">{coe.name}</h3>
              <p className="text-sm text-slate-500 mb-6 font-bold leading-relaxed">{coe.description}</p>
              <div className="flex items-center gap-4 border-t border-white/5 pt-6">
                {/* W489 — one number, the one the API actually computes, under its own name */}
                {coe.score != null ? (
                  <div data-testid="coe-score" title={coe.scoreBasis || 'a salience weight, not a measurement'}>
                    <p className="text-[10px] font-black text-slate-500 uppercase">Salience weight</p>
                    <p className="text-lg font-black text-aura">{coe.score.toFixed(2)}</p>
                    <p className="text-[8px] font-bold text-slate-600 uppercase">not a measurement</p>
                  </div>
                ) : (
                  <p className="text-[10px] font-bold text-slate-600" data-testid="coe-no-score">
                    No score was returned for this centre.
                  </p>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* W578 (FU-394) — the route returns `score_meaning`, a response-level statement about what
          EVERY score on this page means, and nothing read it. The per-insight `score_basis` already
          reaches the reader on hover (above), so this is not that fact repeated: it is the AGGREGATE
          one — that three of the four are fixed constants and the fourth only scales with the project
          count, so the ORDER of this list is not a ranking of anything measured. A reader who hovers
          one card learns about one score; nobody learns that without this. Rendered once, where the
          ordering it qualifies is visible. */}
      {data?.score_meaning && (
        <p data-testid="insights-score-meaning"
           className="text-[10px] font-bold text-slate-500 leading-relaxed max-w-3xl">
          About the scores above: {data.score_meaning}
        </p>
      )}

      {/* Latest insights from intelligence API */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Latest Portfolio Insights</h3>
          {/* W578 (FU-394) — `total_projects` is the key the route actually sends. It is null on the
              crash branch, where nothing was counted, and that is NOT zero: a count of 0 would read as
              "you have no projects", which is the whole untruth FU-323 was about. So null says so. */}
          {data?.total_projects != null ? (
            <span data-testid="insights-provenance"
                  className="text-[10px] font-black text-slate-500 uppercase tracking-widest">
              Derived from {data.total_projects} project{data.total_projects !== 1 ? 's' : ''}
            </span>
          ) : data?.error ? (
            <span data-testid="insights-provenance-unknown"
                  className="text-[10px] font-black text-amber-400 uppercase tracking-widest">
              nothing was counted — the portfolio could not be read
            </span>
          ) : null}
        </div>
        {data?.insights?.length ? (
          data.insights.map((insight, i) => (
            <div key={i} className="flex items-center justify-between p-6 rounded-2xl bg-slate-900/40 border border-slate-800 group hover:border-aura/30 transition-all">
              <div className="flex items-center gap-4 flex-1 min-w-0">
                <FileText className="text-aura flex-shrink-0" size={18} />
                <div className="min-w-0">
                  <p className="font-bold text-white truncate">{insight.title ?? insight.type ?? 'Insight'}</p>
                  <p className="text-[10px] text-slate-500 font-bold uppercase mt-0.5">
                    {insight.domain ?? insight.type ?? 'portfolio'}
                    {insight.confidence != null ? ` · ${(insight.confidence * 100).toFixed(0)}% confidence` : ''}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => navigate(`/synthesis`)}
                className="ml-4 text-xs font-bold text-aura hover:underline flex items-center gap-1 shrink-0"
              >
                <BookOpen size={12} /> Explore
              </button>
            </div>
          ))
        ) : (
          !isLoading && (
            <div className="p-12 text-center border-2 border-dashed border-slate-800 rounded-[3rem]">
              <Sparkles className="mx-auto text-slate-700 mb-4" size={48} />
              {/* W576 (FU-323) — the route's error key had NO READER. This page took `insights`
                  alone, so a crash inside the computation rendered as the statement below: a
                  failure shown to the founder as "you have no projects". The producer now carries
                  the failure inside `insights` itself, so even this branch cannot be reached by a
                  crash — and if it ever is, the error is named here rather than hidden. */}
              {data?.error ? (
                <p data-testid="insights-error" className="text-amber-400 font-bold text-xs leading-relaxed max-w-md mx-auto">
                  Portfolio insights could not be computed, so nothing was counted — this is not a
                  statement that you have no projects. Reason: {String(data.error)}
                </p>
              ) : (
              <p className="text-slate-500 font-black uppercase tracking-widest text-xs">
                Create projects to generate portfolio insights
              </p>
              )}
              <Button className="mt-6 bg-aura text-sovereign" onClick={() => navigate('/projects')}>
                Start a Project
              </Button>
            </div>
          )
        )}
      </div>
    </div>
  );
};
