import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented, toast } from '@workstation/ui';
import { FileText, Search, Link as LinkIcon, Database, Info, ChevronRight, Filter } from 'lucide-react';
import { motion } from 'framer-motion';

export const BackgroundTextIndex: React.FC = () => {
  const [artifacts] = useState([
    { path: 'docs/plans/v138_galactic_era.md', obj: 'Galactic Era Implementation', qep: 'YES' },
    { path: 'README.md', obj: 'Project Overview', qep: 'YES' },
    { path: 'docs/knowledge/v137_blueprint.md', obj: 'v137 Architectural Spec', qep: 'YES' },
    { path: 'CONSTITUTION_FINAL.md', obj: 'Legal Framework', qep: 'NO' },
  ]);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black text-white tracking-tighter uppercase italic break-words">Text Archive</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Indexed Background Knowledge • Forensic Knowledge Hub</p>
        </div>
        <Button onClick={() => notImplemented('Refresh Index')} variant="outline" className="border-aura/30 text-aura"><Database size={18} /> Refresh Index</Button>
      </header>

      <Card className="p-0 overflow-hidden border-white/5">
         <div className="p-6 border-b border-white/5 bg-slate-900/40 flex justify-between items-center">
            <div className="flex items-center gap-4 bg-slate-950 px-4 py-2 rounded-xl border border-white/5">
               <Search size={16} className="text-slate-600" />
               <input placeholder="Search text artifacts..." className="bg-transparent border-none outline-none text-xs font-bold text-white w-64" />
            </div>
            <div className="flex gap-2">
               <button type="button" onClick={() => notImplemented('Filter')} aria-label="Filter" title="Filter" className="p-2 bg-slate-950 rounded-lg border border-white/5 text-slate-500"><Filter size={16} /></button>
            </div>
         </div>

         <div className="divide-y divide-white/5 bg-slate-950/20">
            {artifacts.map((a, i) => (
              <div key={i} className="p-6 flex items-center justify-between group hover:bg-white/5 transition-all cursor-pointer">
                 <div className="flex items-center gap-6">
                    <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-slate-500 group-hover:text-aura transition-colors">
                       <FileText size={24} />
                    </div>
                    <div>
                       <p className="text-sm font-black text-white mb-1">{a.path}</p>
                       <p className="text-[10px] font-black text-slate-500 uppercase">{a.obj}</p>
                    </div>
                 </div>
                 <div className="flex items-center gap-8">
                    <div className="text-right">
                       <p className="text-[10px] font-black text-slate-700 uppercase mb-1">QEP Align</p>
                       <Badge color={a.qep === 'YES' ? 'aura' : 'sovereign'}>{a.qep}</Badge>
                    </div>
                    <button
                      type="button"
                      onClick={() => toast(`${a.path} · ${a.obj}`)}
                      aria-label={`View source for ${a.path}`}
                      title={`View source for ${a.path}`}
                      className="p-3 bg-slate-900 rounded-xl text-slate-600 hover:text-white transition-colors border border-slate-800"
                    >
                       <LinkIcon size={18} />
                    </button>
                 </div>
              </div>
            ))}
         </div>
      </Card>
    </div>
  );
};
