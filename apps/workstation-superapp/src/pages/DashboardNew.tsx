import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { SearchMeshModal } from '../components/SearchMeshModal';
import {
  MessageSquare,
  Zap,
  Clock,
  ArrowRight,
  Search,
  Sparkles,
  BookOpen,
  Binary,
  FolderOpen,
  FileText,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface ActivityItem {
  id: string;
  type: string;
  msg: string;
  time: string;
}

interface VitalsData {
  cpu: number;
  memory: number;
  totalProjects: number;
  swarmHealth: number;
}

export const DashboardNew: React.FC = () => {
  const { user, setCurrentTab } = useStore();
  const navigate = useNavigate();
  const [searchOpen, setSearchOpen] = useState(false);
  const [activity,   setActivity]   = useState<ActivityItem[]>([]);
  const [vitals,     setVitals]     = useState<VitalsData | null>(null);

  useEffect(() => {
    // Load live activity from project store
    axios.get('/api/v1/projects/').then(({ data }) => {
      const projects: any[] = data ?? [];
      const items: ActivityItem[] = projects.slice(0, 5).map(p => ({
        id: p.id,
        type: 'Project',
        msg: `${p.title} — stage: ${p.stage}`,
        time: p.updated_at
          ? new Date(p.updated_at * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          : 'recently',
      }));
      if (items.length > 0) setActivity(items);
    }).catch(() => {});

    // Load real vitals from psutil endpoint
    axios.get('/api/v1/projects/stats/summary').then(({ data }) => {
      setVitals({
        cpu: data.cpu_percent ?? 0,
        memory: data.memory_percent ?? 0,
        totalProjects: data.total_projects ?? 0,
        swarmHealth: data.swarm_health ?? 0.98,
      });
    }).catch(() => {});
  }, []);

  const actions = [
    { id: 'synthesis',       name: 'Synthesis Studio', icon: Sparkles,  color: 'text-highlight',    bg: 'bg-highlight/10',    desc: 'Ingest knowledge & generate reports.',  route: '/synthesis' },
    { id: 'qep-religion',    name: 'QEP Religion',     icon: BookOpen,  color: 'text-vital',        bg: 'bg-vital/10',        desc: 'Quran Education Platform Hub.',         route: '/qep-religion' },
    { id: 'genome-explorer', name: 'Genome Core',      icon: Binary,    color: 'text-emerald-500',  bg: 'bg-emerald-500/10',  desc: 'System evolution & GRN.',               route: '/genome-explorer' },
    { id: 'ceo',             name: 'AI CEO',            icon: MessageSquare, color: 'text-aura',     bg: 'bg-aura/10',         desc: 'Consult your autonomous executive.',    route: '/ceo' },
  ];

  const displayActivity = activity.length > 0 ? activity : [
    { id: 'placeholder', type: 'System', msg: 'No projects yet — create your first project', time: '' },
  ];

  return (
    <>
    <SearchMeshModal open={searchOpen} onClose={() => setSearchOpen(false)} />
    <div className="space-y-12 animate-in fade-in duration-700">
      <header className="flex flex-col gap-6">
        <div className="space-y-2 min-w-0">
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black tracking-tighter text-white uppercase italic break-words">
            Command <span className="text-aura">Center</span>
          </h1>
          <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
            Welcome, <span className="text-white">{user?.displayName}</span>. System status is <span className="text-emerald-500">Optimal</span>.
            All {user?.role === 'ADMIN' ? 'Executive' : 'Sovereign'} channels active.
          </p>
        </div>
        <div className="flex flex-wrap gap-4 shrink-0">
           <Button onClick={() => setSearchOpen(true)} variant="outline" className="bg-slate-900 border-slate-800">
              <Search size={18} /> Search Mesh
           </Button>
           <Button onClick={() => { setCurrentTab('ceo'); navigate('/ceo'); }} className="bg-aura text-sovereign shadow-2xl shadow-aura/20">
              <MessageSquare size={18} /> Consult CEO
           </Button>
        </div>
      </header>

      <section className="grid grid-cols-1 @[480px]:grid-cols-2 @[720px]:grid-cols-4 gap-6">
        {actions.map((action, i) => (
          <motion.div
            key={action.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card
              className="p-8 group cursor-pointer hover:border-aura/40 transition-all bg-slate-950/40 backdrop-blur-sm border-slate-900 flex flex-col h-full"
              onClick={() => { setCurrentTab(action.id); navigate(action.route); }}
            >
              <div className={`w-14 h-14 rounded-2xl ${action.bg} ${action.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                <action.icon size={28} />
              </div>
              <h3 className="text-xl font-black text-white mb-2 uppercase">{action.name}</h3>
              <p className="text-xs text-slate-500 font-bold leading-relaxed mb-6 flex-1">{action.desc}</p>
              <div className="flex items-center gap-2 text-[10px] font-black uppercase text-aura tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                Execute Action <ArrowRight size={12} />
              </div>
            </Card>
          </motion.div>
        ))}
      </section>

      <div className="grid grid-cols-1 @[720px]:grid-cols-12 gap-10">
         <div className="@[720px]:col-span-8 space-y-10">
            <Card className="p-10 border-slate-900 bg-slate-950/20">
               <div className="flex justify-between items-center mb-8">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     <Clock size={24} className="text-highlight" />
                     Sovereign Stream
                  </h3>
                  <Badge color="highlight">Real-time</Badge>
               </div>
               <div className="space-y-4">
                  {displayActivity.map((act) => (
                    <div key={act.id} className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-center justify-between gap-4 group hover:border-aura/20 transition-all">
                       <div className="flex items-center gap-6 min-w-0">
                          <div className="w-2 h-2 rounded-full bg-aura animate-pulse shrink-0" />
                          <div className="min-w-0">
                             <p className="text-sm font-bold text-white truncate">{act.msg}</p>
                             <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest truncate">{act.type}{act.time ? ` • ${act.time}` : ''}</p>
                          </div>
                       </div>
                       {act.id !== 'placeholder' && (
                         <button type="button" onClick={() => navigate('/projects')}
                           className="text-[8px] py-1 px-3 border border-slate-700 rounded-lg text-slate-400 hover:text-white shrink-0 uppercase font-black tracking-widest">
                           View
                         </button>
                       )}
                    </div>
                  ))}
               </div>
               <button type="button" onClick={() => navigate('/projects')}
                 className="w-full mt-8 py-4 border border-slate-800 rounded-2xl text-xs font-black uppercase tracking-widest text-slate-500 hover:text-white hover:border-slate-600 transition-colors">
                 View All Projects
               </button>
            </Card>
         </div>

         <div className="@[720px]:col-span-4 space-y-10">
            <Card className="p-10 bg-aura/5 border-aura/20 space-y-8">
               <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                     <Zap size={24} />
                  </div>
                  <div>
                     <h4 className="text-lg font-black text-white uppercase">Vitals</h4>
                     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Mesh Harmony: Optimal</p>
                  </div>
               </div>
               <div className="space-y-6 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500 tracking-widest">
                     <span>CPU</span>
                     <span className="text-aura">{vitals ? `${vitals.cpu.toFixed(1)}%` : '—'}</span>
                  </div>
                  <progress value={vitals?.cpu ?? 0} max={100} aria-label="CPU usage"
                    className="w-full h-1.5 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-900 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura" />
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500 tracking-widest">
                     <span>Memory</span>
                     <span className="text-highlight">{vitals ? `${vitals.memory.toFixed(1)}%` : '—'}</span>
                  </div>
                  <progress value={vitals?.memory ?? 0} max={100} aria-label="Memory usage"
                    className="w-full h-1.5 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-900 [&::-webkit-progress-value]:bg-highlight [&::-moz-progress-bar]:bg-highlight" />
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500 tracking-widest">
                     <span>Projects</span>
                     <span className="text-emerald-400">{vitals?.totalProjects ?? '—'}</span>
                  </div>
                  <Button
                    onClick={() => { setCurrentTab('admin'); navigate('/admin'); }}
                    variant="outline" className="w-full text-[10px] py-4 uppercase font-black border-aura/20 text-aura">
                    Advanced Telemetry
                  </Button>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-8">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Active Objectives</h4>
               <div className="space-y-4">
                  {[
                    { name: 'v1.0 Global Launch', prog: 100, cls: 'w-full' },
                    { name: 'QEP Domain Parity', prog: 100, cls: 'w-full' },
                    { name: 'v2.0 Neural Mesh', prog: 12, cls: 'w-[12%]' },
                  ].map((obj, i) => (
                    <div key={i} className="space-y-2">
                       <div className="flex justify-between text-[9px] font-black uppercase tracking-widest">
                          <span className="text-white">{obj.name}</span>
                          <span className="text-slate-600">{obj.prog}%</span>
                       </div>
                       <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                          <div className={`h-full bg-highlight transition-all duration-1000 ${obj.cls}`} />
                       </div>
                    </div>
                  ))}
               </div>
            </Card>
         </div>
      </div>
    </div>
    </>
  );
};
