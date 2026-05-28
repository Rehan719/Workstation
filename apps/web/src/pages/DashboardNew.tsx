import React from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import {
  Plus,
  FileText,
  Calendar,
  Layout,
  MessageSquare,
  Zap,
  CheckCircle2,
  Clock,
  ArrowRight,
  Search,
  Sparkles,
  BookOpen,
  Binary
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const DashboardNew: React.FC = () => {
  const { user, setCurrentTab } = useStore();
  const navigate = useNavigate();

  const actions = [
    { id: 'task', name: 'Knowledge Ingest', icon: Plus, color: 'text-aura', bg: 'bg-aura/10', desc: 'Upload and process raw data.', route: '/file-hub' },
    { id: 'note', name: 'Synthesis Studio', icon: Sparkles, color: 'text-highlight', bg: 'bg-highlight/10', desc: 'Generate reports & presentations.', route: '/synthesis' },
    { id: 'event', name: 'QEP Religion', icon: BookOpen, color: 'text-vital', bg: 'bg-vital/10', desc: 'Quran Education Platform Hub.', route: '/qep-religion' },
    { id: 'project', name: 'Genome Core', icon: Binary, color: 'text-emerald-500', bg: 'bg-emerald-500/10', desc: 'System evolution & GRN.', route: '/genome-explorer' },
  ];

  const recentActivity = [
    { id: 1, type: 'System', msg: 'Article 1127 Validation Passed', time: '2m ago' },
    { id: 2, type: 'Agent', msg: 'Llama-3-Graft Synthesis Complete', time: '15m ago' },
    { id: 3, type: 'Governance', msg: 'Zakat ROI Allocation Verified', time: '1h ago' },
    { id: 4, type: 'Security', msg: 'PQC Handshake Rotated', time: '3h ago' },
    { id: 5, type: 'Evolution', msg: 'Recursive Optimization Loop Active', time: '5h ago' }
  ];

  return (
    <div className="space-y-12 animate-in fade-in duration-700">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div className="space-y-2">
          <h1 className="text-6xl font-black tracking-tighter text-white uppercase italic">
            Command <span className="text-aura">Center</span>
          </h1>
          <p className="text-slate-400 font-bold text-lg max-w-2xl leading-relaxed">
            Welcome, <span className="text-white">{user?.displayName}</span>. System status is <span className="text-emerald-500">Optimal</span>.
            All {user?.role === 'CEO' ? 'Executive' : 'Sovereign'} channels active.
          </p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline" className="bg-slate-900 border-slate-800">
              <Search size={18} /> Search Mesh
           </Button>
           <Button onClick={() => setCurrentTab('ceo')} className="bg-aura text-sovereign shadow-2xl shadow-aura/20">
              <MessageSquare size={18} /> Consult CEO
           </Button>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {actions.map((action, i) => (
          <motion.div
            key={action.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card
              className="p-8 group cursor-pointer hover:border-aura/40 transition-all bg-slate-950/40 backdrop-blur-sm border-slate-900 flex flex-col h-full"
              onClick={() => navigate(action.route)}
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

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="p-10 border-slate-900 bg-slate-950/20">
               <div className="flex justify-between items-center mb-8">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     <Clock size={24} className="text-highlight" />
                     Sovereign Stream
                  </h3>
                  <Badge color="highlight">Real-time</Badge>
               </div>
               <div className="space-y-4">
                  {recentActivity.map((act) => (
                    <div key={act.id} className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-center justify-between group hover:border-aura/20 transition-all">
                       <div className="flex items-center gap-6">
                          <div className="w-2 h-2 rounded-full bg-aura animate-pulse" />
                          <div>
                             <p className="text-sm font-bold text-white">{act.msg}</p>
                             <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest">{act.type} • {act.time}</p>
                          </div>
                       </div>
                       <Button variant="outline" className="text-[8px] py-1 px-3">View Audit</Button>
                    </div>
                  ))}
               </div>
               <Button variant="secondary" className="w-full mt-8 uppercase font-black tracking-widest text-xs py-4">View All System Activity</Button>
            </Card>
         </div>

         <div className="lg:col-span-4 space-y-10">
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
                     <span>System Resonance</span>
                     <span className="text-aura">98.4%</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                     <div className="h-full bg-aura w-[98%]" />
                  </div>
                  <Button
                    onClick={() => setCurrentTab('admin')}
                    variant="outline" className="w-full text-[10px] py-4 uppercase font-black border-aura/20 text-aura">
                    Advanced Telemetry
                  </Button>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-8">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Active Objectives</h4>
               <div className="space-y-4">
                  {[
                    { name: 'v1.0 Global Launch', prog: 100 },
                    { name: 'QEP Domain Parity', prog: 100 },
                    { name: 'v2.0 Neural Mesh', prog: 12 },
                  ].map((obj, i) => (
                    <div key={i} className="space-y-2">
                       <div className="flex justify-between text-[9px] font-black uppercase tracking-widest">
                          <span className="text-white">{obj.name}</span>
                          <span className="text-slate-600">{obj.prog}%</span>
                       </div>
                       <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                          <div className="h-full bg-highlight transition-all duration-1000" style={{ width: `${obj.prog}%` }} />
                       </div>
                    </div>
                  ))}
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
