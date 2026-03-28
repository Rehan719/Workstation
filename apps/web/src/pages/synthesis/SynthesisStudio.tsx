import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { Sparkles, FileText, Presentation, Globe, Layers, Download, Play, Loader2, CheckCircle2 } from 'lucide-react';
import axios from 'axios';
import { PresentationPlayer } from './PresentationPlayer';
import { BusinessModelDashboard } from './BusinessModelDashboard';

export const SynthesisStudio: React.FC = () => {
  const [ingestedFiles, setIngestedFiles] = useState<any[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [outputType, setOutputType] = useState('report');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showPlayer, setShowPlayer] = useState(false);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const resp = await axios.get('/api/v1/ingest/list');
      setIngestedFiles(resp.data);
    } catch (e) { console.error(e); }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  const handleGenerate = async () => {
    if (selectedIds.length === 0) return alert('Select content first.');
    setGenerating(true);
    setResult(null);
    try {
      const resp = await axios.post('/api/v1/synthesis/generate', {
        content_ids: selectedIds,
        output_type: outputType
      });
      setResult(resp.data);
    } catch (e) { alert('Generation failed.'); }
    finally { setGenerating(false); }
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Synthesis <span className="text-aura">Studio</span></h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Multi-Modal Output Generation • AI CEO Orchestrated • v1.0</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         {/* Left: Content Selection */}
         <div className="lg:col-span-4 space-y-8">
            <Card className="p-8 border-slate-900 bg-slate-950/40">
               <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Select Knowledge Base</h3>
               <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                  {ingestedFiles.map(f => (
                    <div
                      key={f.file_id}
                      onClick={() => toggleSelect(f.file_id)}
                      className={`p-4 rounded-xl border transition-all cursor-pointer ${selectedIds.includes(f.file_id) ? 'bg-aura/10 border-aura' : 'bg-slate-900 border-slate-800 opacity-60'}`}
                    >
                       <p className="text-xs font-bold text-white truncate">{f.filename}</p>
                       <p className="text-[9px] text-slate-500 uppercase font-black">{f.content_type}</p>
                    </div>
                  ))}
                  {ingestedFiles.length === 0 && <p className="text-[10px] text-slate-500 italic">No files ingested yet.</p>}
               </div>
            </Card>

            <Card className="p-8 border-slate-900 bg-slate-950/40 space-y-6">
               <h3 className="text-sm font-black text-white uppercase tracking-widest">Output Configuration</h3>
               <div className="grid grid-cols-2 gap-4">
                  {[
                    { id: 'report', label: 'Report', icon: FileText },
                    { id: 'presentation', label: 'Presentation', icon: Presentation },
                    { id: 'website', label: 'Website', icon: Globe },
                    { id: 'simulation', label: 'Simulation', icon: Layers }
                  ].map(t => (
                    <button
                      key={t.id}
                      onClick={() => setOutputType(t.id)}
                      className={`p-4 rounded-2xl border flex flex-col items-center gap-3 transition-all ${outputType === t.id ? 'bg-aura text-sovereign border-aura' : 'bg-slate-900 border-slate-800 text-slate-400'}`}
                    >
                       <t.icon size={20} />
                       <span className="text-[9px] font-black uppercase tracking-widest">{t.label}</span>
                    </button>
                  ))}
               </div>
               <Button
                onClick={handleGenerate}
                disabled={generating || selectedIds.length === 0}
                className="w-full bg-white text-sovereign py-6 shadow-2xl shadow-white/5"
               >
                  {generating ? <Loader2 className="animate-spin mr-2" /> : <Sparkles className="mr-2" size={18} />}
                  {generating ? 'Orchestrating...' : 'Generate Synthesis'}
               </Button>
            </Card>
         </div>

         {/* Right: Preview / Output */}
         <div className="lg:col-span-8">
            <Card className="h-full p-10 border-slate-800 bg-slate-950/20 relative overflow-hidden flex flex-col min-h-[600px]">
               {!result && !generating && (
                 <div className="flex-1 flex flex-col items-center justify-center text-center space-y-6">
                    <div className="w-20 h-20 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
                       <Play size={40} />
                    </div>
                    <div>
                       <p className="text-xl font-black text-slate-700 uppercase tracking-tighter italic">Studio Offline</p>
                       <p className="text-xs text-slate-500 font-bold max-w-sm mx-auto">Select source materials and output type to begin autonomous synthesis.</p>
                    </div>
                 </div>
               )}

               {generating && (
                 <div className="flex-1 flex flex-col items-center justify-center text-center space-y-10">
                    <div className="relative">
                       <div className="w-32 h-32 rounded-full border-2 border-aura/20 animate-ping absolute inset-0" />
                       <div className="w-32 h-32 rounded-full border-2 border-aura animate-spin border-t-transparent" />
                    </div>
                    <div>
                       <p className="text-aura font-black uppercase tracking-[0.3em] text-xs">AI CEO Synthesis In Progress</p>
                       <p className="text-slate-500 text-[10px] mt-2 font-bold uppercase tracking-widest italic animate-pulse">
                          Accessing L4 Meta-Cognitive Buffers...
                       </p>
                    </div>
                 </div>
               )}

               {result && (
                 <div className="flex-1 flex flex-col animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="flex justify-between items-start mb-10">
                       <div className="flex items-center gap-4">
                          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center">
                             <CheckCircle2 size={24} />
                          </div>
                          <div>
                             <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Synthesis Complete</p>
                             <h3 className="text-2xl font-black text-white uppercase tracking-tight">{outputType} Finalized</h3>
                          </div>
                       </div>
                       <Button variant="outline" className="border-slate-800">
                          <Download size={18} /> Download {result.metadata.format.toUpperCase()}
                       </Button>
                    </div>

                    <div className="flex-1 bg-slate-950/80 border border-slate-800 rounded-3xl p-10 font-mono text-xs text-slate-400 overflow-y-auto custom-scrollbar leading-relaxed">
                       {result.content}
                    </div>

                    {outputType === 'presentation' && (
                      <div className="mt-8 p-6 rounded-2xl bg-aura/5 border border-aura/20 flex items-center justify-between">
                         <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-aura flex items-center justify-center text-sovereign">
                               <Play size={18} />
                            </div>
                            <p className="text-[10px] font-black text-aura uppercase tracking-widest">Web Player Ready: {result.metadata.slides_count} Slides with AI Narration</p>
                         </div>
                         <Button onClick={() => setShowPlayer(true)} variant="secondary" className="px-6 py-2 text-[8px] uppercase font-black">Launch Player</Button>
                      </div>
                    )}

                    {outputType === 'simulation' && (
                       <div className="mt-10 pt-10 border-t border-slate-800">
                          <BusinessModelDashboard data={JSON.parse(result.content)} />
                       </div>
                    )}
                 </div>
               )}
            </Card>
         </div>
      </div>

      {showPlayer && result && (
        <PresentationPlayer
          slides={JSON.parse(result.content)}
          onClose={() => setShowPlayer(false)}
        />
      )}
    </div>
  );
};
