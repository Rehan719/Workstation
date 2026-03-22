import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Briefcase, Activity, Rocket, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, LayoutGrid, Terminal, Database, TrendingUp, DollarSign, Hammer, TooltipIcon } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const EmploymentHub: React.FC = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('opportunities');

  const jobs = [
    { id: 'j-1', title: 'Senior Recombinator', realm: 'Developer', salary: '14,200 WST', status: 'Active' },
    { id: 'j-2', title: 'Ethical Auditor', realm: 'Scholar', salary: '8,400 WST', status: 'Active' },
    { id: 'j-3', title: 'Mesh Architect', realm: 'Enterprise', salary: '22,000 WST', status: 'Urgent' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter">Forge of Vocation</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Economic Participation • Sovereign Freelance Markets • Employment Hub</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Resume</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Plus size={18} /> Post Opportunity
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <div className="lg:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Briefcase size={24} className="text-aura" />
                     Sovereign Opportunities
                  </h3>
                  <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
                     <button onClick={() => setActiveTab('opportunities')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'opportunities' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Active</button>
                     <button onClick={() => setActiveTab('contracts')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'contracts' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Contracts</button>
                  </div>
               </div>

               <div className="space-y-4">
                  <AnimatePresence mode="wait">
                     <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                        {jobs.map((job, i) => (
                          <div key={job.id} className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer">
                             <div className="flex items-center gap-8">
                                <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                                   <Zap size={24} />
                                </div>
                                <div>
                                   <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{job.title}</p>
                                   <div className="flex items-center gap-4">
                                      <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Realm: {job.realm}</span>
                                      <Badge color={job.status === 'Urgent' ? 'vital' : 'aura'}>{job.status}</Badge>
                                   </div>
                                </div>
                             </div>
                             <div className="flex items-center gap-8">
                                <div className="text-right">
                                   <p className="text-[10px] font-black text-slate-700 uppercase mb-1">Bounty</p>
                                   <p className="text-xl font-black text-white">{job.salary}</p>
                                </div>
                                <Button variant="outline" className="px-6 py-3">Apply</Button>
                             </div>
                          </div>
                        ))}
                     </motion.div>
                  </AnimatePresence>
               </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
               <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
                  <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                     <TrendingUp size={32} />
                  </div>
                  <div>
                     <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Market Demand</h3>
                     <p className="text-sm text-slate-400 font-bold leading-relaxed">
                        Recombination and Orchestration skills are currently in high demand across the 100+ mesh nodes.
                     </p>
                  </div>
                  <div className="pt-6 border-t border-aura/10 flex justify-between items-center">
                     <span className="text-[10px] font-black uppercase text-slate-500">Avg. Rate</span>
                     <span className="text-lg font-black text-white">420 WST / Cycle</span>
                  </div>
               </Card>

               <Card className="p-10 space-y-8 bg-highlight/5 border-highlight/20">
                  <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign shadow-xl shadow-highlight/20">
                     <DollarSign size={32} />
                  </div>
                  <div>
                     <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Personal Earnings</h3>
                     <p className="text-sm text-slate-400 font-bold leading-relaxed">
                        Your participation in the mesh as a Developer has generated 12,400 WST this month.
                     </p>
                  </div>
                  <Button className="w-full bg-highlight text-sovereign py-5 rounded-2xl font-black uppercase tracking-widest text-[10px]">Withdraw to Wallet</Button>
               </Card>
            </div>
         </div>

         <div className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-slate-950 border-slate-900">
               <div className="flex items-center gap-4 text-aura">
                  <Hammer size={24} />
                  <h4 className="text-xl font-black uppercase tracking-tight">Skill Genome</h4>
               </div>
               <div className="space-y-8 pt-6 border-t border-white/5">
                  {[
                    { label: 'Recombination', progress: 92 },
                    { label: 'Orchestration', progress: 78 },
                    { label: 'Governance', progress: 45 },
                  ].map(skill => (
                    <div key={skill.label} className="space-y-3">
                       <div className="flex justify-between items-end">
                          <span className="text-[10px] font-black uppercase text-slate-500">{skill.label}</span>
                          <span className="text-xs font-black text-white">{skill.progress}%</span>
                       </div>
                       <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                          <div className="h-full bg-aura transition-all duration-1000" style={{ width: `${skill.progress}%` }} />
                       </div>
                    </div>
                  ))}
               </div>
               <Button variant="outline" className="w-full text-[9px] py-2">Sequence Skill Genome</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     All work contracts are cryptographically secured and managed by the Article 1116 Economic Independence module.
                  </p>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};
