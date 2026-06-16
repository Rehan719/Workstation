import React, { useState, useEffect } from 'react';
import { Card, Button, Badge, notImplemented} from '@workstation/ui';
import {
  Sparkles, FileText, Presentation, Globe, Layers, Download, Play, Loader2, CheckCircle2, Upload,
  BarChart3, BookOpen, Archive, Video, Headphones, Smartphone, Bot, Package, Wrench, Briefcase, CheckSquare, Square, ClipboardCheck
} from 'lucide-react';
import axios from 'axios';
import { PresentationPlayer } from './PresentationPlayer';
import { BusinessModelDashboard } from './BusinessModelDashboard';

const OUTPUT_TYPES = [
  // Written documents
  { id: 'report', label: 'Report', icon: FileText },
  { id: 'review', label: 'Review', icon: ClipboardCheck },
  { id: 'analysis', label: 'Analysis', icon: BarChart3 },
  { id: 'dissertation', label: 'Dissertation', icon: BookOpen },
  { id: 'dossier', label: 'Dossier', icon: Archive },
  // Media outputs
  { id: 'presentation', label: 'Presentation', icon: Presentation },
  { id: 'website', label: 'Website', icon: Globe },
  { id: 'video', label: 'Video', icon: Video },
  { id: 'audiobook', label: 'Audiobook', icon: Headphones },
  // Buildable artifacts
  { id: 'app', label: 'App', icon: Smartphone },
  { id: 'agent', label: 'AI Agent/Model', icon: Bot },
  { id: 'product', label: 'Product', icon: Package },
  { id: 'service', label: 'Service', icon: Wrench },
  // Strategy & simulation
  { id: 'business_model', label: 'Business Model', icon: Briefcase },
  { id: 'simulation', label: 'Simulation', icon: Layers },
];

export const SynthesisStudio: React.FC = () => {
  const [ingestedFiles, setIngestedFiles] = useState<any[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [outputTypes, setOutputTypes] = useState<string[]>(['report']);
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [activePresentation, setActivePresentation] = useState<any[] | null>(null);
  const [ingesting, setIngesting] = useState(false);
  const [ingestUrl, setIngestUrl] = useState('');
  const [instructions, setInstructions] = useState('');

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const resp = await axios.get('/api/v1/ingest/list');
      setIngestedFiles(resp.data);
    } catch (e) { console.error(e); }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const file = e.target.files[0];

    setIngesting(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('/api/v1/ingest/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchFiles();
    } catch (e) {
      alert('Upload failed: ' + (e as any).message);
    } finally {
      setIngesting(false);
    }
  };

  const handleURLIngest = async () => {
    if (!ingestUrl) return;
    setIngesting(true);
    try {
      await axios.post('/api/v1/ingest/url', { url: ingestUrl });
      setIngestUrl('');
      fetchFiles();
    } catch (e) {
      alert('URL Ingestion failed.');
    } finally {
      setIngesting(false);
    }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  const toggleOutputType = (id: string) => {
    setOutputTypes(prev => prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]);
  };

  const allOutputTypesSelected = outputTypes.length === OUTPUT_TYPES.length;
  const toggleSelectAllOutputTypes = () => {
    setOutputTypes(allOutputTypesSelected ? [] : OUTPUT_TYPES.map(t => t.id));
  };

  const handleGenerate = async () => {
    if (selectedIds.length === 0) return alert('Select content first.');
    if (outputTypes.length === 0) return alert('Select at least one output type.');
    setGenerating(true);
    setResults([]);
    try {
      const generated = await Promise.all(
        outputTypes.map(type =>
          axios.post('/api/v1/synthesis/generate', {
            content_ids: selectedIds,
            output_type: type,
            instructions
          }).then(resp => ({ ...resp.data, outputType: type }))
        )
      );
      setResults(generated);
    } catch (e) { alert('Generation failed.'); }
    finally { setGenerating(false); }
  };

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Synthesis <span className="text-aura">Studio</span></h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Multi-Modal Output Generation • AI CEO Orchestrated • v1.0</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         {/* Left: Content Selection */}
         <div className="lg:col-span-4 space-y-8">
            <Card className="p-8 border-slate-900 bg-slate-950/40">
               <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Select Knowledge Base</h3>

               <div className="space-y-3 mb-6">
                  <div className="flex bg-slate-900 border border-slate-800 rounded-2xl p-1">
                     <input
                        value={ingestUrl}
                        onChange={(e) => setIngestUrl(e.target.value)}
                        placeholder="Paste DeepSeek/Web URL..."
                        className="flex-1 bg-transparent px-4 text-xs outline-none min-w-0"
                     />
                     <Button onClick={handleURLIngest} disabled={ingesting || !ingestUrl} className="bg-aura text-sovereign px-4 py-2 rounded-xl text-[10px]">Fetch</Button>
                  </div>
                  <label className="cursor-pointer block">
                     <input type="file" className="hidden" onChange={handleFileUpload} disabled={ingesting} />
                     <span className="w-full flex items-center justify-center gap-2 bg-white text-sovereign rounded-xl py-3 px-6 font-bold text-xs shadow-xl pointer-events-none">
                        {ingesting ? <Loader2 className="animate-spin" size={16} /> : <Upload size={16} />}
                        {ingesting ? 'Processing...' : 'Ingest File'}
                     </span>
                  </label>
               </div>

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
               <div className="space-y-2">
                  <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Instructions (optional)</label>
                  <textarea
                     value={instructions}
                     onChange={(e) => setInstructions(e.target.value)}
                     placeholder="Describe the topic, focus, or angle for the generated output..."
                     rows={4}
                     className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura resize-none"
                  />
               </div>
               <div className="flex items-center justify-between">
                  <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Output Types ({outputTypes.length} selected)</label>
                  <button
                    type="button"
                    onClick={toggleSelectAllOutputTypes}
                    className="flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest text-aura hover:text-white transition-colors"
                  >
                    {allOutputTypesSelected ? <CheckSquare size={12} /> : <Square size={12} />}
                    {allOutputTypesSelected ? 'Clear All' : 'Select All'}
                  </button>
               </div>
               <div className="grid grid-cols-3 gap-3">
                  {OUTPUT_TYPES.map(t => {
                    const active = outputTypes.includes(t.id);
                    return (
                      <button
                        type="button"
                        key={t.id}
                        onClick={() => toggleOutputType(t.id)}
                        aria-pressed={active ? 'true' : 'false'}
                        className={`p-3 rounded-2xl border flex flex-col items-center gap-2 transition-all ${active ? 'bg-aura text-sovereign border-aura' : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700'}`}
                      >
                         <t.icon size={18} />
                         <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{t.label}</span>
                      </button>
                    );
                  })}
               </div>
               <Button
                onClick={handleGenerate}
                disabled={generating || selectedIds.length === 0 || outputTypes.length === 0}
                className="w-full bg-white text-sovereign py-6 shadow-2xl shadow-white/5"
               >
                  {generating ? <Loader2 className="animate-spin mr-2" /> : <Sparkles className="mr-2" size={18} />}
                  {generating ? 'Orchestrating...' : `Generate Synthesis${outputTypes.length > 1 ? ` (${outputTypes.length})` : ''}`}
               </Button>
            </Card>
         </div>

         {/* Right: Preview / Output */}
         <div className="lg:col-span-8">
            <Card className="h-full p-10 border-slate-800 bg-slate-950/20 relative overflow-hidden flex flex-col min-h-[600px]">
               {results.length === 0 && !generating && (
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

               {results.length > 0 && !generating && (
                 <div className="flex-1 overflow-y-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="flex items-center gap-4 mb-10">
                       <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
                          <CheckCircle2 size={24} />
                       </div>
                       <div>
                          <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Synthesis Complete</p>
                          <h3 className="text-2xl font-black text-white uppercase tracking-tight">{results.length} Output{results.length > 1 ? 's' : ''} Finalized</h3>
                       </div>
                    </div>

                    <div className="space-y-10">
                       {results.map((result, i) => {
                         const typeInfo = OUTPUT_TYPES.find(t => t.id === result.outputType);
                         return (
                           <div key={i} className={i > 0 ? 'pt-10 border-t border-slate-800' : ''}>
                              <div className="flex justify-between items-start mb-6 gap-4">
                                 <div>
                                    <p className="text-[9px] font-black text-aura uppercase tracking-widest mb-1">{typeInfo?.label || result.outputType}</p>
                                    <h4 className="text-lg font-black text-white uppercase tracking-tight">{result.metadata?.title || `${typeInfo?.label || result.outputType} Output`}</h4>
                                 </div>
                                 <Button onClick={() => notImplemented('This action')} variant="outline" className="border-slate-800 shrink-0">
                                    <Download size={16} /> {result.metadata.format.toUpperCase()}
                                 </Button>
                              </div>

                              <div className="bg-slate-950/80 border border-slate-800 rounded-3xl p-8 font-mono text-xs text-slate-400 overflow-y-auto max-h-96 custom-scrollbar leading-relaxed whitespace-pre-wrap">
                                 {result.content}
                              </div>

                              {(result.outputType === 'presentation' || result.outputType === 'video') && (
                                <div className="mt-6 p-6 rounded-2xl bg-aura/5 border border-aura/20 flex items-center justify-between gap-4">
                                   <div className="flex items-center gap-4">
                                      <div className="w-10 h-10 rounded-full bg-aura flex items-center justify-center text-sovereign shrink-0">
                                         <Play size={18} />
                                      </div>
                                      <p className="text-[10px] font-black text-aura uppercase tracking-widest">Web Player Ready: {result.metadata.slides_count} Slides with AI Narration</p>
                                   </div>
                                   <Button onClick={() => setActivePresentation(JSON.parse(result.content))} variant="secondary" className="px-6 py-2 text-[8px] uppercase font-black shrink-0">Launch Player</Button>
                                </div>
                              )}

                              {result.outputType === 'simulation' && (
                                 <div className="mt-8 pt-8 border-t border-slate-800">
                                    <BusinessModelDashboard data={JSON.parse(result.content)} />
                                 </div>
                              )}
                           </div>
                         );
                       })}
                    </div>
                 </div>
               )}
            </Card>
         </div>
      </div>

      {activePresentation && (
        <PresentationPlayer
          slides={activePresentation}
          onClose={() => setActivePresentation(null)}
        />
      )}
    </div>
  );
};
