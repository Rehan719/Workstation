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
  summary?: string;
  domain?: string;
  confidence?: number;
  projects_count?: number;
  outputs_count?: number;
}

interface IntelligenceInsights {
  insights: InsightItem[];
  generated_at: number;
  portfolio_size: number;
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
    articles: (insight.projects_count ?? 0) + (insight.outputs_count ?? 0),
    scholars: Math.max(1, Math.round((insight.confidence ?? 0) * 20)),
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
        { name: 'AI Ethics', description: 'Alignment and constitutional safety protocols.', icon: Brain, color: 'text-aura', articles: 0, scholars: 0, domain: 'ai' },
        { name: 'Data Science', description: 'Neural synthesis and graph analytics.', icon: Activity, color: 'text-blue-400', articles: 0, scholars: 0, domain: 'science' },
        { name: 'Security', description: 'Post-quantum cryptography and node defense.', icon: Shield, color: 'text-red-400', articles: 0, scholars: 0, domain: 'security' },
        { name: 'Global Affairs', description: 'Cross-domain synthesis and interfaith dialogue.', icon: Globe, color: 'text-yellow-400', articles: 0, scholars: 0, domain: 'global' },
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
                <div>
                  <p className="text-[10px] font-black text-slate-500 uppercase">Outputs</p>
                  <p className="text-lg font-black text-aura">{coe.articles}</p>
                </div>
                <div>
                  <p className="text-[10px] font-black text-slate-500 uppercase">Confidence</p>
                  <p className="text-lg font-black text-white">{coe.scholars}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Latest insights from intelligence API */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Latest Portfolio Insights</h3>
          {data?.portfolio_size != null && (
            <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">
              Derived from {data.portfolio_size} project{data.portfolio_size !== 1 ? 's' : ''}
            </span>
          )}
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
              <p className="text-slate-500 font-black uppercase tracking-widest text-xs">
                Create projects to generate portfolio insights
              </p>
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
