import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Github, Globe, MessageSquare, History, Info, ChevronRight, Zap, Star, Users, Terminal, BookOpen, HeartPulse } from 'lucide-react';
import { motion } from 'framer-motion';

const REPO = 'https://github.com/Rehan719/Workstation';
const openExternal = (url: string) => window.open(url, '_blank', 'noopener,noreferrer');

export const Contribute: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Contributor Portal</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Open Source Leadership • community governance</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => openExternal(REPO)} variant="outline"><Github size={18} /> View Source</Button>
           <Button onClick={() => openExternal(REPO)} className="bg-white text-sovereign shadow-xl">
              <Star size={18} /> Star Repository
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <main className="@[440px]:col-span-8 space-y-10">
            <Card className="p-10 space-y-10 bg-aura/5 border-aura/10 relative overflow-hidden">
               <div className="absolute top-0 right-0 p-10 opacity-5">
                  <Github size={120} className="text-white" />
               </div>
               <div className="space-y-4 relative z-10">
                  <h3 className="text-3xl font-black text-white uppercase tracking-tight">Build the Digital Civilisation</h3>
                  <p className="text-lg text-slate-400 font-bold leading-relaxed max-w-2xl">
                     Workstation Sovereign v3.0 is a community-driven ecosystem. Help us evolve the genomic core, expand the audience realms, or refine the multi-modal fabric.
                  </p>
               </div>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10">
                  {[
                    { title: 'Genomic Core', desc: 'Enhance the Merkle-DAG and GRN engine.', icon: Zap },
                    { title: 'Audience Realms', desc: 'Build tools for Religion, Science, and Care.', icon: HeartPulse },
                    { title: 'Orchestration', desc: 'Optimize L9 swarms and L10 evolution.', icon: Terminal },
                    { title: 'Standards', desc: 'Contribute to ACP/A2A specifications.', icon: BookOpen },
                  ].map(area => (
                    <div key={area.title} className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900 group hover:border-aura/30 transition-all">
                       <div className="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all mb-4">
                          <area.icon size={24} />
                       </div>
                       <h4 className="text-lg font-black text-white mb-1 uppercase tracking-tight">{area.title}</h4>
                       <p className="text-xs font-bold text-slate-500 leading-relaxed">{area.desc}</p>
                    </div>
                  ))}
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <History size={24} className="text-aura" />
                     Recent RFCs
                  </h3>
                  <Button onClick={() => openExternal(`${REPO}/discussions`)} variant="outline" className="text-[10px]">View RFC Archive</Button>
               </div>
               <div className="space-y-4">
                  {[
                    { id: 'RFC-142', title: 'Planetary Latency Optimization via LEO Routing', status: 'Proposed', date: '2h ago' },
                    { id: 'RFC-107', title: 'Standardized Care Plan JSON Schema v3', status: 'Ratified', date: '1d ago' },
                  ].map(rfc => (
                    <div key={rfc.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer">
                       <div className="flex items-center gap-8">
                          <div className="text-[10px] font-black text-slate-700 uppercase vertical-rl">Open</div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{rfc.title}</p>
                             <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{rfc.id} • {rfc.date}</span>
                          </div>
                       </div>
                       <Badge color={rfc.status === 'Ratified' ? 'emerald-500' : 'aura'}>{rfc.status}</Badge>
                    </div>
                  ))}
               </div>
            </Card>
         </main>

         <aside className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-8">
               <h4 className="text-xl font-black flex items-center gap-3">
                  <Users size={20} className="text-aura" />
                  Community Vitals
               </h4>
               <div className="space-y-8">
                  <div className="flex justify-between items-end">
                     <span className="text-[10px] font-black uppercase text-slate-500">External Contributors</span>
                     <span className="text-2xl font-black text-white">142</span>
                  </div>
                  <div className="flex justify-between items-end">
                     <span className="text-[10px] font-black uppercase text-slate-500">Adopting Projects</span>
                     <span className="text-2xl font-black text-white">12</span>
                  </div>
                  <div className="flex justify-between items-end">
                     <span className="text-[10px] font-black uppercase text-slate-500">Open Issues</span>
                     <span className="text-2xl font-black text-aura">24</span>
                  </div>
               </div>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-8">
               <div className="flex items-center gap-4 text-aura">
                  <MessageSquare size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Join the Discussion</h4>
               </div>
               <div className="space-y-4">
                  <Button onClick={() => notImplemented('Access Discourse Forum')} variant="outline" className="w-full py-4 text-[10px]">Access Discourse Forum</Button>
                  <Button onClick={() => notImplemented('Join Discord Server')} variant="outline" className="w-full py-4 text-[10px]">Join Discord Server</Button>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Governance is shared between the AI-led Council and the Open Source Steering Committee.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
