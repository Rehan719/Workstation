import React, { useRef, useState } from 'react';
import { Card, Badge, Button, notImplemented } from '@workstation/ui';
import { File, Folder, Upload, Search, Filter, MoreVertical, Download, Trash2, LayoutGrid, List, Sparkles, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { progressWidthClass } from '../../lib/progressWidth';

export const FileHub: React.FC = () => {
  const [files, setFiles] = useState([
    { name: 'genome_v138.work', size: '2.4MB', type: 'GENOME', date: '2h ago' },
    { name: 'constitution_final.md', size: '156KB', type: 'DOC', date: '5m ago' },
    { name: 'merger_config.json', size: '12KB', type: 'CONFIG', date: '1d ago' },
    { name: 'orbital_auth.pqc', size: '84KB', type: 'KEY', date: '3h ago' },
  ]);
  const uploadInputRef = useRef<HTMLInputElement>(null);

  const handleFilesChosen = (e: React.ChangeEvent<HTMLInputElement>) => {
    const chosen = e.target.files;
    if (!chosen || chosen.length === 0) return;
    const additions = Array.from(chosen).map(f => ({
      name: f.name,
      size: f.size > 1024 * 1024 ? `${(f.size / (1024 * 1024)).toFixed(1)}MB` : `${Math.max(1, Math.round(f.size / 1024))}KB`,
      type: (f.name.split('.').pop() || 'FILE').toUpperCase(),
      date: 'just now',
    }));
    setFiles(prev => [...additions, ...prev]);
    e.target.value = '';
  };

  const downloadFile = (f: { name: string }) => {
    const blob = new Blob([`Placeholder content for ${f.name}`], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = f.name;
    a.click();
    URL.revokeObjectURL(url);
  };

  const deleteFile = (name: string) => {
    setFiles(prev => prev.filter(f => f.name !== name));
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black text-white tracking-tighter uppercase italic break-words">Sovereign Files</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Knowledge Artifact Orchestration • Layer 7 Library</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('File CLI')} variant="outline"><Terminal size={18} /> File CLI</Button>
           <Button onClick={() => uploadInputRef.current?.click()} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20"><Upload size={18} /> Upload Artifact</Button>
           <input ref={uploadInputRef} type="file" multiple aria-label="Upload artifact files" title="Upload artifact files" className="hidden" onChange={handleFilesChosen} />
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-4 gap-8">
         <aside className="space-y-8">
            <Card className="p-6 bg-slate-900/60">
               <h4 className="text-xs font-black uppercase text-slate-500 tracking-widest mb-6">Storage Nodes</h4>
               <div className="space-y-4">
                  {[
                    { label: 'Terrestrial-Primary', val: 82, color: 'bg-aura' },
                    { label: 'Orbital-LEO-Cache', val: 45, color: 'bg-highlight' },
                    { label: 'Deep-Archive-Vault', val: 12, color: 'bg-vital' }
                  ].map(n => (
                    <div key={n.label} className="space-y-2">
                       <div className="flex justify-between text-[10px] font-black uppercase">
                          <span className="text-slate-400">{n.label}</span>
                          <span className="text-white">{n.val}%</span>
                       </div>
                       <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                          <div className={`h-full ${n.color} ${progressWidthClass(n.val)}`} />
                       </div>
                    </div>
                  ))}
               </div>
            </Card>

            <div className="p-6 bg-highlight/5 border border-highlight/20 rounded-3xl space-y-4">
               <div className="flex items-center gap-3 text-highlight">
                  <Sparkles size={20} />
                  <span className="text-xs font-black uppercase tracking-widest">AI Artifact Gen</span>
               </div>
               <p className="text-[10px] text-slate-500 font-bold leading-relaxed">
                  Generate synthetic training data or neural architectures directly in the hub.
               </p>
               <button type="button" onClick={() => notImplemented('AI Artifact Gen')} className="w-full py-3 bg-highlight/10 text-highlight border border-highlight/30 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-highlight hover:text-sovereign transition-all">Launch AI Gen</button>
            </div>
         </aside>

         <main className="@[440px]:col-span-3 space-y-8">
            <Card className="p-0 overflow-hidden border-white/5">
               <div className="p-6 border-b border-white/5 bg-slate-900/40 flex justify-between items-center">
                  <div className="flex items-center gap-4 bg-slate-950 px-4 py-2 rounded-xl border border-white/5">
                     <Search size={16} className="text-slate-600" />
                     <input placeholder="Search artifacts..." className="bg-transparent border-none outline-none text-xs font-bold text-white w-64" />
                  </div>
                  <div className="flex gap-2">
                     <button type="button" onClick={() => notImplemented('Filter')} aria-label="Filter" title="Filter" className="p-2 bg-slate-950 rounded-lg border border-white/5 text-slate-500"><Filter size={16} /></button>
                     <button type="button" onClick={() => notImplemented('Grid view')} aria-label="Grid view" title="Grid view" className="p-2 bg-slate-950 rounded-lg border border-white/5 text-slate-500"><LayoutGrid size={16} /></button>
                  </div>
               </div>

               <div className="divide-y divide-white/5 bg-slate-950/20">
                  {files.map((f, i) => (
                    <div key={i} className="p-6 flex items-center justify-between group hover:bg-white/5 transition-all">
                       <div className="flex items-center gap-6">
                          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-slate-500 group-hover:text-highlight transition-colors">
                             <File size={24} />
                          </div>
                          <div>
                             <p className="text-sm font-black text-white mb-1">{f.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{f.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span>{f.size}</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity">
                          <span className="text-[10px] font-mono text-slate-600 uppercase mr-4">{f.date}</span>
                          <button type="button" onClick={() => downloadFile(f)} aria-label={`Download ${f.name}`} title={`Download ${f.name}`} className="p-2 hover:text-highlight transition-colors"><Download size={16} /></button>
                          <button type="button" onClick={() => deleteFile(f.name)} aria-label={`Delete ${f.name}`} title={`Delete ${f.name}`} className="p-2 hover:text-vital transition-colors"><Trash2 size={16} /></button>
                       </div>
                    </div>
                  ))}
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
