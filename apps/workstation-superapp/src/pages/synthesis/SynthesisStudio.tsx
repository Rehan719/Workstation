import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, Button } from '@workstation/ui';
import { FabricLink } from '../../components/FabricLink';
import {
  Sparkles, FileText, Presentation, Globe, Layers, Download, Play, Loader2,
  CheckCircle2, Upload, BarChart3, BookOpen, Archive, Video, Headphones,
  Smartphone, Bot, Package, Wrench, Briefcase, CheckSquare, Square,
  ClipboardCheck, X, Link, History, Trash2, ChevronDown, ChevronUp,
  ExternalLink, Clock,
} from 'lucide-react';
import axios from 'axios';
import { PresentationPlayer } from './PresentationPlayer';
import { BusinessModelDashboard } from './BusinessModelDashboard';

// ── Output type registry ──────────────────────────────────────────────────────

const OUTPUT_TYPES = [
  { id: 'report',         label: 'Report',         icon: FileText,      group: 'Document' },
  { id: 'review',         label: 'Review',          icon: ClipboardCheck,group: 'Document' },
  { id: 'analysis',       label: 'Analysis',        icon: BarChart3,     group: 'Document' },
  { id: 'dissertation',   label: 'Dissertation',    icon: BookOpen,      group: 'Document' },
  { id: 'dossier',        label: 'Dossier',         icon: Archive,       group: 'Document' },
  { id: 'presentation',   label: 'Presentation',    icon: Presentation,  group: 'Media' },
  { id: 'website',        label: 'Website',         icon: Globe,         group: 'Media' },
  // honest label: the synthesis "video" output is a script & storyboard (slide deck + narration);
  // a real self-playing render exists via deliverables /export?format=video-html — mp4 stays not-yet.
  { id: 'video',          label: 'Video (script & storyboard)', icon: Video, group: 'Media' },
  { id: 'audiobook',      label: 'Audiobook',       icon: Headphones,    group: 'Media' },
  { id: 'app',            label: 'App',             icon: Smartphone,    group: 'Build' },
  { id: 'agent',          label: 'AI Agent',        icon: Bot,           group: 'Build' },
  { id: 'product',        label: 'Product',         icon: Package,       group: 'Build' },
  { id: 'service',        label: 'Service',         icon: Wrench,        group: 'Build' },
  { id: 'business_model', label: 'Business Model',  icon: Briefcase,     group: 'Strategy' },
  { id: 'simulation',     label: 'Simulation',      icon: Layers,        group: 'Strategy' },
] as const;

type OutputTypeId = typeof OUTPUT_TYPES[number]['id'];

// ── Types ─────────────────────────────────────────────────────────────────────

interface IngestedFile {
  file_id: string;
  filename: string;
  content_type: string;
  size: number;
  timestamp: string;
  extracted_text: string;
  status: string;
}

interface SynthesisResult {
  output_id: string;
  output_url: string;
  content: string;
  metadata: Record<string, any>;
  timestamp: string;
  outputType: OutputTypeId;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function formatBytes(n: number) {
  if (n < 1024) return `${n} B`;
  if (n < 1048576) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1048576).toFixed(1)} MB`;
}

function formatTs(ts: string) {
  try { return new Date(ts).toLocaleString(); } catch { return ts; }
}

// ── Component ─────────────────────────────────────────────────────────────────

export const SynthesisStudio: React.FC = () => {
  // Knowledge base
  const [ingestedFiles, setIngestedFiles] = useState<IngestedFile[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [ingesting, setIngesting] = useState(false);
  const [ingestUrl, setIngestUrl] = useState('');
  const [showUrlBar, setShowUrlBar] = useState(false);

  // Composer
  const [outputTypes, setOutputTypes] = useState<OutputTypeId[]>(['report']);
  const [instructions, setInstructions] = useState('');

  // Generation
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState<SynthesisResult[]>([]);
  const [streamTokens, setStreamTokens] = useState<Record<string, string>>({});
  const [activePresentation, setActivePresentation] = useState<any[] | null>(null);

  // History
  const [history, setHistory] = useState<SynthesisResult[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // UI state
  const [expandedResults, setExpandedResults] = useState<Set<number>>(new Set());
  const [previewHtml, setPreviewHtml] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const urlInputRef = useRef<HTMLInputElement>(null);

  // ── Data loading ────────────────────────────────────────────────────────────

  const fetchFiles = useCallback(async () => {
    try {
      const resp = await axios.get('/api/v1/ingest/list');
      setIngestedFiles(resp.data);
    } catch (e) { console.error('Failed to load files:', e); }
  }, []);

  useEffect(() => { fetchFiles(); }, [fetchFiles]);

  useEffect(() => {
    if (showUrlBar) urlInputRef.current?.focus();
  }, [showUrlBar]);

  const loadHistory = useCallback(async () => {
    setLoadingHistory(true);
    try {
      const resp = await axios.get('/api/v1/synthesis/history');
      setHistory(resp.data);
    } catch (e) { console.error('Failed to load history:', e); }
    finally { setLoadingHistory(false); }
  }, []);

  useEffect(() => {
    if (showHistory) loadHistory();
  }, [showHistory, loadHistory]);

  // ── Ingestion ────────────────────────────────────────────────────────────────

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const file = e.target.files[0];
    setIngesting(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const resp = await axios.post('/api/v1/ingest/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setIngestedFiles(prev => [resp.data, ...prev]);
      setSelectedIds(prev => [...prev, resp.data.file_id]);
    } catch (e) {
      setErrorMsg('Upload failed: ' + (e as any).message);
    } finally {
      setIngesting(false);
    }
  };

  const handleURLIngest = async () => {
    if (!ingestUrl.trim()) return;
    setIngesting(true);
    try {
      const resp = await axios.post('/api/v1/ingest/url', { url: ingestUrl });
      setIngestedFiles(prev => [resp.data, ...prev]);
      setSelectedIds(prev => [...prev, resp.data.file_id]);
      setIngestUrl('');
      setShowUrlBar(false);
    } catch (e) {
      setErrorMsg('URL ingestion failed. Check the URL and try again.');
    } finally {
      setIngesting(false);
    }
  };

  const deleteFile = async (fileId: string, ev: React.MouseEvent) => {
    ev.stopPropagation();
    try {
      await axios.delete(`/api/v1/ingest/${fileId}`);
      setIngestedFiles(prev => prev.filter(f => f.file_id !== fileId));
      setSelectedIds(prev => prev.filter(id => id !== fileId));
    } catch (e) { console.error('Delete failed:', e); }
  };

  // ── Selection helpers ────────────────────────────────────────────────────────

  const toggleSelect = (id: string) =>
    setSelectedIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);

  const toggleOutputType = (id: OutputTypeId) =>
    setOutputTypes(prev => prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]);

  const allTypesSelected = outputTypes.length === OUTPUT_TYPES.length;
  const toggleAllTypes = () =>
    setOutputTypes(allTypesSelected ? [] : OUTPUT_TYPES.map(t => t.id) as OutputTypeId[]);

  // ── Generation ───────────────────────────────────────────────────────────────

  const handleGenerate = async () => {
    if (selectedIds.length === 0) { setErrorMsg('Select at least one knowledge base file.'); return; }
    if (outputTypes.length === 0) { setErrorMsg('Select at least one output type.'); return; }
    setErrorMsg(null);
    setGenerating(true);
    setResults([]);
    setStreamTokens({});
    setExpandedResults(new Set());

    const completed: SynthesisResult[] = [];

    for (const type of outputTypes) {
      try {
        const res = await fetch('/api/v1/synthesis/stream', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content_ids: selectedIds, output_type: type, instructions }),
        });

        if (!res.ok || !res.body) {
          // Fallback to non-streaming
          const resp = await axios.post('/api/v1/synthesis/generate', {
            content_ids: selectedIds, output_type: type, instructions,
          });
          completed.push({ ...resp.data, outputType: type });
          continue;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';
        let finalResult: SynthesisResult | null = null;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          const lines = buf.split('\n');
          buf = lines.pop() ?? '';
          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            try {
              const ev = JSON.parse(line.slice(6));
              if (ev.token !== undefined) {
                const tok: string = ev.token.replace(/\\n/g, '\n');
                setStreamTokens(prev => ({ ...prev, [type]: (prev[type] ?? '') + tok }));
              } else if (ev.done) {
                finalResult = {
                  output_id: ev.output_id,
                  output_url: ev.download_url,
                  content: '',
                  metadata: { type, format: 'md', title: type },
                  timestamp: ev.timestamp,
                  outputType: type,
                };
              }
            } catch { /* malformed line */ }
          }
        }

        if (finalResult) {
          // Swap accumulated stream text into content
          finalResult.content = (document.getElementById(`stream-${type}`) as HTMLElement | null)?.innerText ?? '';
          completed.push(finalResult);
        }
      } catch (e) {
        setErrorMsg(`Generation failed for ${type} — check the API server is running.`);
      }
    }

    setResults(completed);
    setExpandedResults(new Set([0]));
    setGenerating(false);
  };

  // ── Download ─────────────────────────────────────────────────────────────────

  const handleDownload = (result: SynthesisResult) => {
    const fmt = result.metadata?.format || 'json';
    const title = (result.metadata?.title || result.outputType).replace(/[^a-z0-9_\-]/gi, '_');
    const a = document.createElement('a');
    a.href = result.output_url;
    a.download = `${title}.${fmt}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleWebsitePreview = (content: string) => {
    setPreviewHtml(content);
  };

  // ── Textarea auto-resize ─────────────────────────────────────────────────────

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 180) + 'px';
  };

  const canGenerate = !generating && selectedIds.length > 0 && outputTypes.length > 0;

  // ── Render ───────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-8 pb-10">

      {/* Header */}
      <header>
        <h1 className="text-3xl @[440px]:text-4xl @[900px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">
          Synthesis <span className="text-aura">Studio</span>
        </h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">
          Multi-Modal AI Output Generation · Knowledge Base Synthesis · v2.0
        </p>
        <div className="mt-3"><FabricLink /></div>
      </header>

      {/* Error banner */}
      {errorMsg && (
        <div role="alert" className="flex items-center justify-between gap-4 px-5 py-3 rounded-2xl bg-vital/10 border border-vital/30 text-vital text-[10px] font-black uppercase tracking-widest">
          <span>{errorMsg}</span>
          <button type="button" onClick={() => setErrorMsg(null)} aria-label="Dismiss error" title="Dismiss" className="shrink-0 hover:text-white transition-colors">✕</button>
        </div>
      )}

      {/* History panel (collapsible) */}
      {showHistory && (
        <Card className="p-6 border-slate-800 bg-slate-950/30">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-black text-white uppercase tracking-widest flex items-center gap-2">
              <History size={14} className="text-aura" /> Synthesis History
            </h3>
            {loadingHistory && <Loader2 size={14} className="animate-spin text-aura" />}
          </div>
          {history.length === 0 && !loadingHistory && (
            <p className="text-[10px] text-slate-500 italic">No synthesis runs yet this session.</p>
          )}
          <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar pr-1">
            {history.map((h, i) => {
              const typeInfo = OUTPUT_TYPES.find(t => t.id === h.metadata?.type);
              return (
                <div
                  key={i}
                  className="flex items-center gap-3 p-3 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors cursor-pointer group"
                  onClick={() => {
                    setResults([{ ...h, outputType: h.metadata?.type as OutputTypeId }]);
                    setExpandedResults(new Set([0]));
                    setShowHistory(false);
                  }}
                >
                  {typeInfo && <typeInfo.icon size={14} className="text-aura shrink-0" />}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-white truncate">
                      {h.metadata?.title || h.metadata?.type}
                    </p>
                    <p className="text-[9px] text-slate-500 flex items-center gap-1 mt-0.5">
                      <Clock size={9} /> {formatTs(h.timestamp)}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); handleDownload({ ...h, outputType: h.metadata?.type as OutputTypeId }); }}
                    className="shrink-0 p-1.5 rounded-lg text-slate-600 hover:text-aura transition-colors opacity-0 group-hover:opacity-100"
                    title="Download"
                  >
                    <Download size={13} />
                  </button>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Results / Output area */}
      <Card className="p-8 border-slate-800 bg-slate-950/20 relative overflow-hidden flex flex-col min-h-[320px]">

        {results.length === 0 && !generating && (
          <div className="flex-1 flex flex-col items-center justify-center text-center space-y-5">
            <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
              <Play size={32} />
            </div>
            <div>
              <p className="text-lg font-black text-slate-700 uppercase tracking-tighter italic">Studio Offline</p>
              <p className="text-xs text-slate-500 font-bold max-w-xs mx-auto">
                Select knowledge base files and output types below, then hit Generate.
              </p>
            </div>
          </div>
        )}

        {generating && (
          <div className="flex-1 overflow-y-auto custom-scrollbar space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-6 h-6 rounded-full border-2 border-aura animate-spin border-t-transparent shrink-0" />
              <p className="text-aura font-black uppercase tracking-[0.3em] text-[10px]">Synthesising…</p>
            </div>
            {outputTypes.map(type => {
              const tokens = streamTokens[type] ?? '';
              return (
                <div key={type} className="border border-slate-800 rounded-2xl overflow-hidden">
                  <div className="flex items-center gap-2 px-4 py-2 border-b border-slate-800 bg-slate-900/40">
                    <span className="text-[9px] font-black uppercase tracking-widest text-aura">{type.replace('_', ' ')}</span>
                    {!tokens && <span className="text-[9px] text-slate-600 uppercase animate-pulse">waiting…</span>}
                  </div>
                  <pre
                    id={`stream-${type}`}
                    className="p-4 text-xs text-slate-300 font-mono whitespace-pre-wrap break-words max-h-64 overflow-y-auto"
                  >{tokens}<span className="inline-block w-1.5 h-3 bg-aura animate-pulse ml-0.5" /></pre>
                </div>
              );
            })}
          </div>
        )}

        {results.length > 0 && !generating && (
          <div className="flex-1 overflow-y-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
                <CheckCircle2 size={20} />
              </div>
              <div>
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Synthesis Complete</p>
                <h3 className="text-xl font-black text-white uppercase tracking-tight">
                  {results.length} Output{results.length > 1 ? 's' : ''} Generated
                </h3>
              </div>
            </div>

            <div className="space-y-4">
              {results.map((result, i) => {
                const typeInfo = OUTPUT_TYPES.find(t => t.id === result.outputType);
                const isExpanded = expandedResults.has(i);
                const fmt = result.metadata?.format || 'json';

                return (
                  <div key={i} className="border border-slate-800 rounded-2xl overflow-hidden">
                    {/* Result header */}
                    <div
                      className="flex items-center gap-3 p-4 cursor-pointer hover:bg-slate-900/40 transition-colors"
                      onClick={() => setExpandedResults(prev => {
                        const next = new Set(prev);
                        isExpanded ? next.delete(i) : next.add(i);
                        return next;
                      })}
                    >
                      {typeInfo && (
                        <div className="w-8 h-8 rounded-lg bg-aura/10 flex items-center justify-center shrink-0">
                          <typeInfo.icon size={14} className="text-aura" />
                        </div>
                      )}
                      <div className="flex-1 min-w-0">
                        <p className="text-[9px] font-black text-aura uppercase tracking-widest">
                          {typeInfo?.label || result.outputType}
                        </p>
                        <p className="text-sm font-black text-white truncate">
                          {result.metadata?.title || `${typeInfo?.label} Output`}
                        </p>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        {fmt === 'html' && (
                          <button
                            type="button"
                            onClick={(e) => { e.stopPropagation(); handleWebsitePreview(result.content); }}
                            className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:text-aura text-[9px] font-black uppercase tracking-wider transition-colors"
                            title="Preview website"
                          >
                            <ExternalLink size={10} /> Preview
                          </button>
                        )}
                        <button
                          type="button"
                          onClick={(e) => { e.stopPropagation(); handleDownload(result); }}
                          className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:text-white text-[9px] font-black uppercase tracking-wider transition-colors"
                          title={`Download ${fmt.toUpperCase()}`}
                        >
                          <Download size={10} /> {fmt.toUpperCase()}
                        </button>
                        <div className="text-slate-600">
                          {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                        </div>
                      </div>
                    </div>

                    {/* Result body (expanded) */}
                    {isExpanded && (
                      <div className="border-t border-slate-800">

                        {/* Presentation / video player */}
                        {(result.outputType === 'presentation' || result.outputType === 'video') && (
                          <div className="p-4 bg-aura/5 border-b border-slate-800 flex items-center justify-between gap-4">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full bg-aura flex items-center justify-center text-sovereign shrink-0">
                                <Play size={14} />
                              </div>
                              <p className="text-[10px] font-black text-aura uppercase tracking-widest">
                                {result.metadata?.slides_count} Slides · Web Player Ready
                              </p>
                            </div>
                            <button
                              type="button"
                              onClick={() => {
                                try { setActivePresentation(JSON.parse(result.content)); }
                                catch { setErrorMsg('Could not parse slide data.'); }
                              }}
                              className="px-4 py-2 rounded-xl bg-aura text-sovereign text-[9px] font-black uppercase tracking-widest hover:scale-105 transition-transform"
                            >
                              Launch Player
                            </button>
                          </div>
                        )}

                        {/* Business Model Dashboard */}
                        {result.outputType === 'simulation' && (() => {
                          try {
                            const data = JSON.parse(result.content);
                            return (
                              <div className="p-6 border-b border-slate-800">
                                <BusinessModelDashboard data={data} />
                              </div>
                            );
                          } catch { return null; }
                        })()}

                        {/* Business Model Canvas — structured display */}
                        {result.outputType === 'business_model' && (() => {
                          try {
                            const canvas = JSON.parse(result.content);
                            const sections = [
                              { label: 'Value Proposition', value: canvas.value_proposition },
                              { label: 'Customer Segments', value: Array.isArray(canvas.customer_segments) ? canvas.customer_segments.join(', ') : canvas.customer_segments },
                              { label: 'Revenue Streams', value: Array.isArray(canvas.revenue_streams) ? canvas.revenue_streams.join(', ') : canvas.revenue_streams },
                              { label: 'Key Resources', value: Array.isArray(canvas.key_resources) ? canvas.key_resources.join(', ') : canvas.key_resources },
                              { label: 'Key Activities', value: Array.isArray(canvas.key_activities) ? canvas.key_activities.join(', ') : canvas.key_activities },
                              { label: 'Key Partners', value: Array.isArray(canvas.key_partners) ? canvas.key_partners.join(', ') : canvas.key_partners },
                              { label: 'Channels', value: Array.isArray(canvas.channels) ? canvas.channels.join(', ') : canvas.channels },
                              { label: 'Cost Structure', value: Array.isArray(canvas.cost_structure) ? canvas.cost_structure.join(', ') : canvas.cost_structure },
                              { label: 'Market Opportunity', value: canvas.market_opportunity },
                              { label: 'Competitive Advantage', value: canvas.competitive_advantage },
                            ].filter(s => s.value);
                            return (
                              <div className="p-6 grid grid-cols-2 gap-3 border-b border-slate-800">
                                {sections.map((s, si) => (
                                  <div key={si} className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                    <p className="text-[8px] font-black text-aura uppercase tracking-widest mb-1">{s.label}</p>
                                    <p className="text-xs text-slate-300 leading-relaxed">{s.value}</p>
                                  </div>
                                ))}
                              </div>
                            );
                          } catch { return null; }
                        })()}

                        {/* Audiobook chapters */}
                        {result.outputType === 'audiobook' && (() => {
                          try {
                            const chapters = JSON.parse(result.content);
                            return (
                              <div className="p-6 space-y-3 border-b border-slate-800 max-h-72 overflow-y-auto custom-scrollbar">
                                {chapters.map((ch: any, ci: number) => (
                                  <div key={ci} className="flex gap-3 p-3 rounded-xl bg-slate-900 border border-slate-800">
                                    <div className="w-6 h-6 rounded-full bg-aura/10 flex items-center justify-center shrink-0 text-[9px] font-black text-aura">{ch.id}</div>
                                    <div>
                                      <p className="text-[10px] font-black text-white">{ch.title}</p>
                                      <p className="text-[9px] text-slate-500 mt-0.5">{ch.narration}</p>
                                      <p className="text-[8px] text-aura mt-1 font-bold">{ch.duration_sec}s</p>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            );
                          } catch { return null; }
                        })()}

                        {/* App / Agent / Product / Service structured display */}
                        {['app', 'agent', 'product', 'service'].includes(result.outputType) && (() => {
                          try {
                            const spec = JSON.parse(result.content);
                            return (
                              <div className="p-6 space-y-4 border-b border-slate-800">
                                {spec.description && (
                                  <p className="text-sm text-slate-300 leading-relaxed">{spec.description}</p>
                                )}
                                {spec.value_proposition && (
                                  <div className="p-3 rounded-xl bg-aura/5 border border-aura/20">
                                    <p className="text-[8px] font-black text-aura uppercase tracking-widest mb-1">Value Proposition</p>
                                    <p className="text-xs text-slate-300">{spec.value_proposition}</p>
                                  </div>
                                )}
                                <div className="grid grid-cols-2 gap-3">
                                  {spec.key_features && (
                                    <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                      <p className="text-[8px] font-black text-aura uppercase tracking-widest mb-2">Key Features</p>
                                      <ul className="space-y-1">
                                        {(spec.key_features as string[]).map((f, fi) => (
                                          <li key={fi} className="text-[9px] text-slate-400 flex gap-1.5">
                                            <span className="text-aura shrink-0">·</span>{f}
                                          </li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                  {spec.technical_stack && (
                                    <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                      <p className="text-[8px] font-black text-aura uppercase tracking-widest mb-2">Tech Stack</p>
                                      <div className="flex flex-wrap gap-1">
                                        {(spec.technical_stack as string[]).map((t, ti) => (
                                          <span key={ti} className="px-1.5 py-0.5 rounded bg-aura/10 text-aura text-[8px] font-bold">{t}</span>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                </div>
                                {spec.implementation_phases && (
                                  <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                    <p className="text-[8px] font-black text-aura uppercase tracking-widest mb-2">Implementation Phases</p>
                                    <div className="space-y-1.5">
                                      {(spec.implementation_phases as any[]).map((ph, pi) => (
                                        <div key={pi} className="flex items-start gap-2">
                                          <span className="text-[8px] font-black text-aura bg-aura/10 px-1.5 py-0.5 rounded shrink-0">{ph.phase || pi + 1}</span>
                                          <div>
                                            <p className="text-[9px] text-white font-bold">{ph.milestone}</p>
                                            {ph.timeline && <p className="text-[8px] text-slate-500">{ph.timeline}</p>}
                                          </div>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            );
                          } catch { return null; }
                        })()}

                        {/* Raw content — for markdown documents and JSON fallback */}
                        <div className="bg-slate-950/80 mx-4 mb-4 mt-4 rounded-2xl p-6 font-mono text-xs text-slate-400 max-h-96 overflow-y-auto custom-scrollbar leading-relaxed whitespace-pre-wrap">
                          {result.content}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </Card>

      {/* ── Unified Composer ─────────────────────────────────────────────────── */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">

        {/* Knowledge base */}
        <div className="px-5 pt-5 pb-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">
              Knowledge Base
              {selectedIds.length > 0 && (
                <span className="ml-2 text-aura">· {selectedIds.length} of {ingestedFiles.length} selected</span>
              )}
            </span>
            {selectedIds.length > 0 && (
              <button
                type="button"
                onClick={() => setSelectedIds([])}
                className="text-[9px] font-black text-slate-600 hover:text-red-400 uppercase tracking-widest transition-colors"
              >
                Clear selection
              </button>
            )}
          </div>

          {ingestedFiles.length === 0 ? (
            <p className="text-[10px] text-slate-600 italic">No files ingested yet — upload a file or paste a URL below.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {ingestedFiles.map(f => {
                const active = selectedIds.includes(f.file_id);
                return (
                  <button
                    key={f.file_id}
                    type="button"
                    onClick={() => toggleSelect(f.file_id)}
                    title={`${f.filename} · ${formatBytes(f.size)}\n${f.extracted_text?.slice(0, 120)}...`}
                    className={`group flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[10px] font-bold border transition-all ${
                      active
                        ? 'bg-aura/10 border-aura text-white'
                        : 'bg-slate-800 border-slate-700 text-slate-500 hover:border-slate-600 hover:text-slate-300'
                    }`}
                  >
                    <FileText size={9} className={active ? 'text-aura' : 'text-slate-600'} />
                    <span className="max-w-[120px] truncate">{f.filename}</span>
                    {active && <CheckSquare size={9} className="text-aura shrink-0" />}
                    <span
                      role="button"
                      tabIndex={0}
                      onClick={(e) => deleteFile(f.file_id, e)}
                      onKeyDown={(e) => e.key === 'Enter' && deleteFile(f.file_id, e as any)}
                      aria-label={`Remove ${f.filename} from knowledge base`}
                      className="ml-0.5 text-slate-600 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100 shrink-0"
                    >
                      <X size={9} />
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="border-t border-slate-800" />

        {/* Instructions textarea */}
        <div className="px-5 py-4">
          <textarea
            ref={textareaRef}
            value={instructions}
            onChange={(e) => { setInstructions(e.target.value); autoResize(); }}
            placeholder="Describe the topic, focus, or angle for the generated output... (leave blank to infer from file names)"
            rows={2}
            className="w-full bg-transparent text-sm text-white placeholder-slate-600 resize-none focus:outline-none leading-relaxed font-medium min-h-[48px] max-h-[180px]"
          />
        </div>

        <div className="border-t border-slate-800" />

        {/* URL bar (expanded inline) */}
        {showUrlBar && (
          <>
            <div className="px-5 py-3 flex items-center gap-2">
              <Link size={13} className="text-slate-500 shrink-0" />
              <input
                ref={urlInputRef}
                value={ingestUrl}
                onChange={(e) => setIngestUrl(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleURLIngest(); if (e.key === 'Escape') { setShowUrlBar(false); setIngestUrl(''); } }}
                placeholder="Paste DeepSeek / web URL..."
                className="flex-1 bg-transparent text-sm text-white placeholder-slate-600 outline-none min-w-0"
              />
              <button
                type="button"
                onClick={handleURLIngest}
                disabled={ingesting || !ingestUrl.trim()}
                className="shrink-0 px-3 py-1.5 rounded-xl bg-aura text-sovereign text-[10px] font-black uppercase tracking-wider disabled:opacity-40 transition-opacity"
              >
                {ingesting ? <Loader2 size={11} className="animate-spin" /> : 'Fetch'}
              </button>
              <button
                type="button"
                onClick={() => { setShowUrlBar(false); setIngestUrl(''); }}
                title="Dismiss URL input"
                aria-label="Dismiss URL input"
                className="shrink-0 p-1.5 rounded-lg text-slate-500 hover:text-white transition-colors"
              >
                <X size={13} />
              </button>
            </div>
            <div className="border-t border-slate-800" />
          </>
        )}

        {/* Output type grid — ALL 15 types visible */}
        <div className="px-5 py-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">
              Output Types
              {outputTypes.length > 0 && <span className="ml-2 text-aura">· {outputTypes.length} selected</span>}
            </span>
            <button
              type="button"
              onClick={toggleAllTypes}
              className="flex items-center gap-1 text-[9px] font-black text-slate-500 hover:text-white uppercase tracking-widest transition-colors"
              {...({ 'aria-pressed': allTypesSelected ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
            >
              {allTypesSelected ? <CheckSquare size={11} className="text-aura" /> : <Square size={11} />}
              {allTypesSelected ? 'Deselect All' : 'Select All'}
            </button>
          </div>
          <div className="grid grid-cols-3 @[420px]:grid-cols-5 gap-2">
            {OUTPUT_TYPES.map(t => {
              const active = outputTypes.includes(t.id);
              const pressedAttrs = { 'aria-pressed': active ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' };
              return (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => toggleOutputType(t.id)}
                  {...pressedAttrs}
                  className={`flex flex-col items-center gap-1.5 p-3 rounded-2xl border text-center transition-all ${
                    active
                      ? 'bg-aura text-sovereign border-aura shadow-lg shadow-aura/10'
                      : 'bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'
                  }`}
                >
                  <t.icon size={15} />
                  <span className="text-[8px] font-black uppercase tracking-wide leading-tight">{t.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="border-t border-slate-800" />

        {/* Bottom toolbar */}
        <div className="px-5 py-3 flex items-center gap-2 flex-wrap">

          {/* Upload */}
          <label className="cursor-pointer">
            <input type="file" className="hidden" onChange={handleFileUpload} disabled={ingesting} />
            <span className={`flex items-center gap-1.5 px-3 py-2 rounded-2xl border text-[10px] font-black uppercase tracking-wider transition-all select-none ${
              ingesting
                ? 'bg-aura/10 border-aura text-aura cursor-wait'
                : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600 cursor-pointer'
            }`}>
              {ingesting ? <Loader2 size={12} className="animate-spin" /> : <Upload size={12} />}
              {ingesting ? 'Ingesting...' : 'Upload File'}
            </span>
          </label>

          {/* URL toggle */}
          <button
            type="button"
            onClick={() => setShowUrlBar(v => !v)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-2xl border text-[10px] font-black uppercase tracking-wider transition-all ${
              showUrlBar
                ? 'bg-aura/10 border-aura text-aura'
                : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600'
            }`}
          >
            <Globe size={12} />
            URL
          </button>

          {/* History toggle */}
          <button
            type="button"
            onClick={() => setShowHistory(v => !v)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-2xl border text-[10px] font-black uppercase tracking-wider transition-all ${
              showHistory
                ? 'bg-aura/10 border-aura text-aura'
                : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600'
            }`}
          >
            <History size={12} />
            History
          </button>

          <div className="flex-1" />

          {/* Generate */}
          <button
            type="button"
            onClick={handleGenerate}
            disabled={!canGenerate}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all duration-150 ${
              canGenerate
                ? 'bg-white text-sovereign shadow-lg shadow-white/10 hover:scale-105 active:scale-95'
                : 'bg-slate-800 text-slate-600 cursor-not-allowed'
            }`}
          >
            {generating
              ? <Loader2 size={14} className="animate-spin" />
              : <Sparkles size={14} />
            }
            {generating
              ? 'Generating...'
              : outputTypes.length > 1
                ? `Generate ${outputTypes.length} Outputs`
                : 'Generate'
            }
          </button>
        </div>
      </div>

      {/* Presentation player overlay */}
      {activePresentation && (
        <PresentationPlayer
          slides={activePresentation}
          onClose={() => setActivePresentation(null)}
        />
      )}

      {/* Website preview overlay */}
      {previewHtml && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex flex-col">
          <div className="flex items-center justify-between px-6 py-4 bg-slate-900 border-b border-slate-800">
            <span className="text-xs font-black text-white uppercase tracking-widest">Website Preview</span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => {
                  const blob = new Blob([previewHtml], { type: 'text/html' });
                  const url = URL.createObjectURL(blob);
                  window.open(url, '_blank');
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:text-white text-[10px] font-black uppercase tracking-wider transition-colors"
              >
                <ExternalLink size={11} /> Open in Tab
              </button>
              <button
                type="button"
                onClick={() => setPreviewHtml(null)}
                aria-label="Close website preview"
                className="p-2 rounded-xl text-slate-500 hover:text-white transition-colors"
              >
                <X size={16} />
              </button>
            </div>
          </div>
          <iframe
            srcDoc={previewHtml}
            title="Generated website preview"
            className="flex-1 w-full border-0"
            sandbox="allow-scripts"
          />
        </div>
      )}
    </div>
  );
};
