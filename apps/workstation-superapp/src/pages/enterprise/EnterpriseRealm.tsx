import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Bot, FolderPlus, Factory, Zap, TrendingUp, Layers, ChevronRight } from 'lucide-react';

interface PortfolioStats {
  total_projects: number;
  total_outputs: number;
  by_stage: Record<string, number>;
  cpu_percent: number;
  memory_percent: number;
}

export const EnterpriseRealm: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<PortfolioStats | null>(null);

  useEffect(() => {
    axios.get<PortfolioStats>('/api/v1/projects/stats/summary', { validateStatus: () => true })
      .then(r => { if (r.status === 200) setStats(r.data); })
      .catch(() => {});
  }, []);

  const kpis = [
    { label: 'Total Projects', value: stats ? String(stats.total_projects) : '—' },
    { label: 'AI Deliverables', value: stats ? String(stats.total_outputs) : '—' },
    { label: 'In Concept',     value: stats ? String(stats.by_stage?.concept ?? 0) : '—' },
    { label: 'Commercialised', value: stats ? String(stats.by_stage?.commercialise ?? 0) : '—' },
  ];

  return (
    <div className="space-y-12 animate-in fade-in duration-700">

      {/* Header */}
      <header className="border-b border-white/5 pb-8">
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2">Enterprise Realm</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          Forest of Collaboration
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-xl leading-relaxed">
          AI-mediated workspace for Enterprise projects. Create, run, and commercialise real AI deliverables through the CEO → Project → Factory lifecycle.
        </p>
      </header>

      {/* KPI strip */}
      <div className="grid grid-cols-2 @[480px]:grid-cols-4 gap-4">
        {kpis.map(k => (
          <div key={k.label} className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
            <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500 mb-1">{k.label}</p>
            <p className="text-3xl font-black text-white">{k.value}</p>
          </div>
        ))}
      </div>

      {/* Primary CTAs */}
      <div className="grid grid-cols-1 @[480px]:grid-cols-3 gap-6">

        {/* AI CEO */}
        <button
          type="button"
          onClick={() => navigate('/ceo')}
          className="group p-8 rounded-3xl bg-aura/5 border border-aura/20 text-left hover:border-aura/50 hover:bg-aura/10 transition-all"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 rounded-2xl bg-aura/20 text-aura"><Bot size={24} /></div>
            <ChevronRight size={16} className="text-slate-600 group-hover:text-aura transition-colors" />
          </div>
          <h3 className="text-base font-black text-white mb-1">Talk to AI CEO</h3>
          <p className="text-[10px] text-slate-500 leading-relaxed">
            Consult the AI CEO on strategy, realm selection, and project scope.
          </p>
        </button>

        {/* Create Project */}
        <button
          type="button"
          onClick={() => navigate('/projects?realm=enterprise&domain=saas&new=1')}
          className="group p-8 rounded-3xl bg-highlight/5 border border-highlight/20 text-left hover:border-highlight/50 hover:bg-highlight/10 transition-all"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 rounded-2xl bg-highlight/20 text-highlight"><FolderPlus size={24} /></div>
            <ChevronRight size={16} className="text-slate-600 group-hover:text-highlight transition-colors" />
          </div>
          <h3 className="text-base font-black text-white mb-1">Create Enterprise Project</h3>
          <p className="text-[10px] text-slate-500 leading-relaxed">
            Start a new project. Run the AI workflow to generate your first deliverable.
          </p>
        </button>

        {/* Factory */}
        <button
          type="button"
          onClick={() => navigate('/factory')}
          className="group p-8 rounded-3xl bg-vital/5 border border-vital/20 text-left hover:border-vital/50 hover:bg-vital/10 transition-all"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 rounded-2xl bg-vital/20 text-vital"><Factory size={24} /></div>
            <ChevronRight size={16} className="text-slate-600 group-hover:text-vital transition-colors" />
          </div>
          <h3 className="text-base font-black text-white mb-1">Business Model Factory</h3>
          <p className="text-[10px] text-slate-500 leading-relaxed">
            Run a production line to generate a Business Model Canvas, Pitch Deck, or Technical Spec.
          </p>
        </button>
      </div>

      {/* Secondary tools */}
      <div className="grid grid-cols-1 @[480px]:grid-cols-3 gap-4">
        {[
          { icon: Zap,        label: 'Digital Reactor',  sub: 'Domain simulation + AI trace',  path: '/reactor'   },
          { icon: TrendingUp, label: 'Incubator',         sub: 'Prompt evolution tournament',   path: '/incubator' },
          { icon: Layers,     label: 'All Projects',      sub: 'View and manage your portfolio', path: '/projects'  },
        ].map(({ icon: Icon, label, sub, path }) => (
          <button
            key={path}
            type="button"
            onClick={() => navigate(path)}
            className="group flex items-center gap-4 p-5 rounded-2xl bg-slate-900/40 border border-slate-800 text-left hover:border-slate-700 hover:bg-slate-900/70 transition-all"
          >
            <div className="p-2.5 rounded-xl bg-slate-800 text-slate-400 group-hover:text-white transition-colors">
              <Icon size={16} />
            </div>
            <div className="min-w-0">
              <p className="text-xs font-black text-white">{label}</p>
              <p className="text-[9px] text-slate-600 mt-0.5 truncate">{sub}</p>
            </div>
            <ChevronRight size={14} className="ml-auto text-slate-700 group-hover:text-slate-400 transition-colors shrink-0" />
          </button>
        ))}
      </div>

    </div>
  );
};
