import React, { useState, useEffect } from 'react';
import { Card, Button } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { SearchMeshModal } from '../components/SearchMeshModal';
import {
  MessageSquare, ArrowRight, Search, Layers, Rocket, Cpu, Boxes,
  Building2, ShieldCheck, Coins, Activity, Clock,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getPrefs } from '../lib/userPrefs';
import { listOutputs, type OutputRecord } from '../lib/outputHistory';
import { useT } from '../lib/i18n';

// The unified front door (§3A + §17). It orients every user to the two ways Workstation IDBO serves
// them — (1) work now with AI across a domain, or (2) take a challenge Concept→Commercialisation into a
// living VSB enterprise — and maps the platform's capability pillars. All status is real (no fabricated
// metrics): vitals + projects from the live stats endpoint, organism health from /organism/status.

interface ActivityItem { id: string; type: string; msg: string; time: string; }
interface Vitals { cpu: number; memory: number; totalProjects: number; }

// §3A — the two distinct, complementary ways the platform serves each user.
const JOURNEYS = [
  {
    id: 'domains', icon: Layers, route: '/domains', k: 'home.journey1',
    eyebrow: 'Offering 1 · Work now',
    title: 'Work in a Domain',
    desc: 'AI-mediated tools & resources across Religion · Science · Education · Law · Employment · Care — research, analyse, generate, plan, author and review, on Workstation’s own native AI.',
    cta: 'Open Domains',
  },
  {
    id: 'genesis', icon: Rocket, route: '/genesis', k: 'home.journey2',
    eyebrow: 'Offering 2 · Build an enterprise',
    title: 'Concept → Commercialisation',
    desc: 'Take any challenge through the full end-to-end lifecycle into a living VSB IDBO enterprise — bespoke, autonomous and self-running, led by your Chief (your digital twin).',
    cta: 'Start a Genesis',
  },
] as const;

// The platform's capability pillars (the vision map) — each a real, reachable surface.
const PILLARS = [
  { name: 'Native AI Fabric',       desc: 'Our own swarm · models · orchestration', icon: Cpu,        route: '/native-ai' },
  { name: 'Resource Fabric',        desc: 'Engines · reactors · labs · factories',   icon: Boxes,      route: '/resource-fabric' },
  { name: 'Living Enterprises',     desc: 'Your VSB IDBO entities & projects',       icon: Building2,  route: '/projects' },
  { name: 'Governance & Compliance',desc: 'Solution-quality bar · live compliance',  icon: ShieldCheck,route: '/governance-hub' },
  { name: 'Economic Organism',      desc: 'The VSB economy (virtual WST)',           icon: Coins,      route: '/economy' },
  { name: 'Living Organism',        desc: 'The biomimetic body & live vitals',       icon: Activity,   route: '/organism' },
];

export const DashboardNew: React.FC = () => {
  const { user, setCurrentTab } = useStore();
  const navigate = useNavigate();
  const { t, rtl } = useT();
  const [searchOpen, setSearchOpen] = useState(false);
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [vitals, setVitals] = useState<Vitals | null>(null);
  const [health, setHealth] = useState<{ composite: number; mode: string } | null>(null);

  // E5 — personalisation: greet by the stored name and surface recent work from My Work history.
  const prefs = getPrefs();
  const greetName = prefs.displayName?.trim() || user?.displayName;
  const genesisRoute = `/genesis${prefs.defaultRealm || prefs.defaultDomain
    ? `?${[prefs.defaultRealm ? `realm=${encodeURIComponent(prefs.defaultRealm)}` : '', prefs.defaultDomain ? `domain=${encodeURIComponent(prefs.defaultDomain)}` : ''].filter(Boolean).join('&')}`
    : ''}`;
  const [recent, setRecent] = useState<OutputRecord[]>([]);
  useEffect(() => {
    const refresh = () => setRecent(listOutputs().slice(0, 3));
    refresh();
    window.addEventListener('ws:output-history', refresh);
    return () => window.removeEventListener('ws:output-history', refresh);
  }, []);

  useEffect(() => {
    axios.get('/api/v1/projects/').then(({ data }) => {
      const projects: any[] = data ?? [];
      const items: ActivityItem[] = projects.slice(0, 5).map(p => ({
        id: p.id,
        type: `${p.realm ?? 'project'} · ${p.stage ?? ''}`.trim(),
        msg: p.title,
        time: p.updated_at ? new Date(p.updated_at * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'recently',
      }));
      if (items.length > 0) setActivity(items);
    }).catch(() => {});

    axios.get('/api/v1/projects/stats/summary').then(({ data }) => {
      setVitals({ cpu: data.cpu_percent ?? 0, memory: data.memory_percent ?? 0, totalProjects: data.total_projects ?? 0 });
    }).catch(() => {});

    axios.get('/api/v1/organism/status').then(({ data }) => {
      setHealth({ composite: data.composite_health ?? 0, mode: String(data.mode ?? '').replace(/_/g, ' ') });
    }).catch(() => {});
  }, []);

  const displayActivity = activity.length > 0 ? activity
    : [{ id: 'placeholder', type: 'System', msg: 'No projects yet — start a Genesis or open a Domain tool', time: '' }];

  return (
    <>
      <SearchMeshModal open={searchOpen} onClose={() => setSearchOpen(false)} />
      <div dir={rtl ? 'rtl' : undefined} className="space-y-12 animate-in fade-in duration-700">

        {/* Header — honest, vision-framed */}
        <header className="flex flex-col gap-6">
          <div className="space-y-3 min-w-0">
            <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura">{t('home.eyebrow')}</p>
            <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black tracking-tighter text-white uppercase italic break-words">
              {t('home.title.concept')} <span className="text-aura">&rarr;</span> {t('home.title.commercialisation')}
            </h1>
            <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
              {t('home.welcome')}{greetName ? <>, <span className="text-white">{greetName}</span></> : ''}. {t('home.intro')}{' '}
              <span className="text-white">{t('home.intro.work')}</span>, {t('home.intro.or', 'or')}
              <span className="text-white"> {t('home.intro.build')}</span> {t('home.intro.tail')}
            </p>
          </div>
          <div className="flex flex-wrap gap-4 shrink-0">
            <Button onClick={() => setSearchOpen(true)} variant="outline" className="bg-slate-900 border-slate-800">
              <Search size={18} /> {t('home.searchMesh')}
            </Button>
            <Button onClick={() => { setCurrentTab('ceo'); navigate('/ceo'); }} className="bg-aura text-sovereign shadow-2xl shadow-aura/20">
              <MessageSquare size={18} /> {t('home.consultCEO')}
            </Button>
          </div>
        </header>

        {/* §3A — the two primary journeys */}
        <section className="grid grid-cols-1 @[720px]:grid-cols-2 gap-6">
          {JOURNEYS.map((j, i) => (
            <motion.div key={j.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
              <Card
                className="p-8 group cursor-pointer hover:border-aura/50 transition-all bg-slate-950/40 border-slate-900 flex flex-col h-full"
                onClick={() => { setCurrentTab(j.id); navigate(j.id === 'genesis' ? genesisRoute : j.route); }}
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="w-14 h-14 rounded-2xl bg-aura/10 text-aura flex items-center justify-center group-hover:scale-110 transition-transform">
                    <j.icon size={28} />
                  </div>
                  <span className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-500">{t(`${j.k}.eyebrow`, j.eyebrow)}</span>
                </div>
                <h3 className="text-2xl font-black text-white mb-3 uppercase tracking-tight">{t(`${j.k}.title`, j.title)}</h3>
                <p className="text-sm text-slate-400 font-semibold leading-relaxed mb-6 flex-1">{j.desc}</p>
                <div className="flex items-center gap-2 text-[11px] font-black uppercase text-aura tracking-widest">
                  {t(`${j.k}.cta`, j.cta)} <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
                </div>
              </Card>
            </motion.div>
          ))}
        </section>

        {/* E5 — personalised "continue" strip: your recent outputs (from My Work), if any */}
        {recent.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-[10px] font-black uppercase tracking-[0.25em] text-slate-400">{t('home.recent')}</h3>
              <button type="button" onClick={() => navigate('/my-work')} className="text-[10px] font-black uppercase tracking-widest text-slate-500 hover:text-white">{t('home.myWork')} &rarr;</button>
            </div>
            <div className="grid grid-cols-1 @[560px]:grid-cols-3 gap-3">
              {recent.map(r => (
                <button key={r.id} type="button" onClick={() => navigate('/my-work')}
                  className="text-left p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-aura/50 transition-all">
                  <p className="font-black text-white text-xs truncate">{r.title}</p>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mt-1 truncate">
                    {new Date(r.ts).toLocaleDateString()}{r.domain ? ` · ${r.domain}` : ''}
                  </p>
                  {r.input && <p className="text-[10px] text-slate-500 mt-1.5 line-clamp-2">{r.input}</p>}
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Capability pillars — the platform map */}
        <section>
          <h3 className="text-[10px] font-black uppercase tracking-[0.25em] text-slate-400 mb-4">{t('home.platform')}</h3>
          <div className="grid grid-cols-2 @[560px]:grid-cols-3 @[900px]:grid-cols-6 gap-3">
            {PILLARS.map(p => (
              <button key={p.route} type="button" onClick={() => navigate(p.route)}
                className="group text-left p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-aura/50 transition-all">
                <div className="w-9 h-9 rounded-xl bg-aura/10 flex items-center justify-center mb-3"><p.icon size={15} className="text-aura" /></div>
                <p className="font-black text-white text-xs leading-tight">{p.name}</p>
                <p className="text-[10px] text-slate-500 leading-snug mt-1">{p.desc}</p>
              </button>
            ))}
          </div>
        </section>

        {/* Live status — all real data */}
        <div className="grid grid-cols-1 @[720px]:grid-cols-12 gap-10">
          <div className="@[720px]:col-span-8 space-y-10">
            <Card className="p-10 border-slate-900 bg-slate-950/20">
              <div className="flex justify-between items-center mb-8">
                <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                  <Clock size={24} className="text-highlight" /> Recent Activity
                </h3>
                <button type="button" onClick={() => navigate('/projects')} className="text-[10px] font-black uppercase tracking-widest text-slate-500 hover:text-white">All projects &rarr;</button>
              </div>
              <div className="space-y-4">
                {displayActivity.map(act => (
                  <div key={act.id} className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-center justify-between gap-4 group hover:border-aura/20 transition-all">
                    <div className="flex items-center gap-6 min-w-0">
                      <div className="w-2 h-2 rounded-full bg-aura shrink-0" />
                      <div className="min-w-0">
                        <p className="text-sm font-bold text-white truncate">{act.msg}</p>
                        <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest truncate">{act.type}{act.time ? ` • ${act.time}` : ''}</p>
                      </div>
                    </div>
                    {act.id !== 'placeholder' && (
                      <button type="button" onClick={() => navigate('/projects')}
                        className="text-[8px] py-1 px-3 border border-slate-700 rounded-lg text-slate-400 hover:text-white shrink-0 uppercase font-black tracking-widest">View</button>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <div className="@[720px]:col-span-4 space-y-10">
            <Card className="p-10 bg-aura/5 border-aura/20 space-y-8">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20"><Activity size={24} /></div>
                <div>
                  <h4 className="text-lg font-black text-white uppercase">{t('home.organism')}</h4>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{health ? `${health.mode} · ${Math.round(health.composite * 100)}% health` : 'reading vitals…'}</p>
                </div>
              </div>
              <div className="space-y-6 pt-6 border-t border-aura/10">
                <Vital label="Composite Health" value={health ? `${Math.round(health.composite * 100)}%` : '—'} pct={health ? health.composite * 100 : 0} tone="aura" />
                <Vital label="CPU" value={vitals ? `${vitals.cpu.toFixed(1)}%` : '—'} pct={vitals?.cpu ?? 0} tone="highlight" />
                <Vital label="Memory" value={vitals ? `${vitals.memory.toFixed(1)}%` : '—'} pct={vitals?.memory ?? 0} tone="highlight" />
                <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500 tracking-widest">
                  <span>Projects</span><span className="text-emerald-400">{vitals?.totalProjects ?? '—'}</span>
                </div>
                <Button onClick={() => navigate('/organism')} variant="outline" className="w-full text-[10px] py-4 uppercase font-black border-aura/20 text-aura">
                  {t('home.openOrganism')}
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
};

const Vital: React.FC<{ label: string; value: string; pct: number; tone: 'aura' | 'highlight' }> = ({ label, value, pct, tone }) => (
  <div className="space-y-2">
    <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500 tracking-widest">
      <span>{label}</span><span className={tone === 'aura' ? 'text-aura' : 'text-highlight'}>{value}</span>
    </div>
    <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
      <div className={`h-full ${tone === 'aura' ? 'bg-aura' : 'bg-highlight'} transition-all duration-1000`} style={{ width: `${Math.min(100, Math.max(0, pct))}%` }} />
    </div>
  </div>
);
