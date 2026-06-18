import React, { useState, useRef, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Badge } from '@workstation/ui';
import { Database, Plus, Settings, Play, Square, Download, Loader2, CheckCircle2, X, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const PRODUCT_TYPES = [
  { id: 'business_model',   label: 'Business Model',    icon: Database  },
  { id: 'technical_spec',   label: 'Technical Spec',    icon: Settings  },
  { id: 'marketing_plan',   label: 'Marketing Plan',    icon: FileText  },
  { id: 'pitch_deck',       label: 'Pitch Deck',        icon: FileText  },
  { id: 'research_report',  label: 'Research Report',   icon: FileText  },
  { id: 'operational_plan', label: 'Operational Plan',  icon: Settings  },
] as const;

const DOMAINS = ['general','technology','enterprise','education','science','law','care','employment'];

interface ProductionLine {
  id: string;
  name: string;
  product_type: string;
  domain: string;
  description: string;
  status: 'idle' | 'running' | 'done' | 'error';
  output: string;
  run_id: string;
}

export const Factory: React.FC = () => {
  const [searchParams] = useSearchParams();
  const urlDomain = searchParams.get('domain') ?? 'general';
  const urlType   = searchParams.get('type')   ?? 'business_model';

  const [lines,       setLines]       = useState<ProductionLine[]>([]);
  const [showNew,     setShowNew]     = useState(searchParams.get('new') === '1');
  const [selected,    setSelected]    = useState<string | null>(null);
  // New line form
  const [name,        setName]        = useState('');
  const [productType, setProductType] = useState(
    PRODUCT_TYPES.some(t => t.id === urlType) ? urlType : 'business_model'
  );
  const [domain,      setDomain]      = useState(
    DOMAINS.includes(urlDomain) ? urlDomain : 'general'
  );
  const [description, setDescription] = useState('');

  const readerRefs = useRef<Map<string, ReadableStreamDefaultReader<Uint8Array>>>(new Map());

  const updateLine = useCallback((id: string, patch: Partial<ProductionLine>) => {
    setLines(ls => ls.map(l => l.id === id ? { ...l, ...patch } : l));
  }, []);

  const handleCreate = () => {
    if (!name.trim()) return;
    const id = `line-${Date.now()}`;
    setLines(ls => [...ls, {
      id, name, product_type: productType, domain, description,
      status: 'idle', output: '', run_id: '',
    }]);
    setName(''); setDescription(''); setShowNew(false);
    setSelected(id);
  };

  const handleRun = async (id: string) => {
    const line = lines.find(l => l.id === id);
    if (!line || line.status === 'running') return;

    updateLine(id, { status: 'running', output: '' });

    try {
      const response = await fetch('/api/v1/factory/produce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: line.name,
          product_type: line.product_type,
          domain: line.domain,
          description: line.description,
        }),
      });
      if (!response.ok || !response.body) throw new Error(`HTTP ${response.status}`);

      const reader = response.body.getReader();
      readerRefs.current.set(id, reader);
      const dec = new TextDecoder();
      let buf = '';
      let accumulated = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const rawLines = buf.split('\n');
        buf = rawLines.pop() ?? '';
        for (const raw of rawLines) {
          if (!raw.startsWith('data: ')) continue;
          try {
            const ev = JSON.parse(raw.slice(6));
            if (ev.token) {
              accumulated += ev.token.replace(/\\n/g, '\n');
              updateLine(id, { output: accumulated });
            } else if (ev.done) {
              updateLine(id, { status: 'done', run_id: ev.run_id ?? '' });
            } else if (ev.error) {
              updateLine(id, { status: 'error', output: accumulated + `\n\n[ERROR] ${ev.error}` });
            }
          } catch { /* skip */ }
        }
      }
    } catch (err: any) {
      updateLine(id, { status: 'error', output: `[ERROR] ${err.message}` });
    } finally {
      readerRefs.current.delete(id);
    }
  };

  const handleStop = (id: string) => {
    readerRefs.current.get(id)?.cancel();
    readerRefs.current.delete(id);
    updateLine(id, { status: 'idle' });
  };

  const handleExport = (line: ProductionLine) => {
    const content = `# ${line.name}\n**Type:** ${line.product_type}  |  **Domain:** ${line.domain}\n\n---\n\n${line.output}`;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${line.name.toLowerCase().replace(/\s+/g, '-')}-${line.run_id || Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const selectedLine = lines.find(l => l.id === selected);

  return (
    <div className="space-y-8 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black text-white uppercase tracking-tighter italic break-words">The Factory</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">AI Production Lines · Real Artefact Generation</p>
        </div>
        <button
          type="button"
          onClick={() => setShowNew(true)}
          className="flex items-center gap-2 px-5 py-2.5 bg-aura text-sovereign rounded-xl font-black text-xs uppercase tracking-widest hover:opacity-90 transition-opacity"
        >
          <Plus size={14} /> New Production Line
        </button>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
        {/* Production line list */}
        <main className="@[440px]:col-span-5 space-y-4">
          <Card className="p-6 space-y-4">
            <h3 className="text-base font-black text-white flex items-center gap-3 uppercase tracking-tight">
              <Database size={18} className="text-aura" /> Production Lines
            </h3>
            {lines.length === 0 && (
              <div className="py-8 text-center">
                <Database size={24} className="text-slate-700 mx-auto mb-3" />
                <p className="text-xs text-slate-500 font-bold">No production lines yet.</p>
                <p className="text-[9px] text-slate-600 mt-1">Click New Production Line to create your first AI artifact.</p>
              </div>
            )}
            {lines.map(line => (
              <motion.div
                key={line.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => setSelected(line.id)}
                className={`p-4 rounded-2xl border cursor-pointer transition-all ${selected === line.id ? 'border-aura bg-aura/5' : 'border-slate-800 bg-slate-950/50 hover:border-slate-700'}`}
              >
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center shrink-0">
                      <Settings size={14} className="text-aura" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-black text-white uppercase truncate">{line.name}</p>
                      <p className="text-[8px] text-slate-500 uppercase tracking-widest">{line.product_type.replace(/_/g,' ')} · {line.domain}</p>
                    </div>
                  </div>
                  <Badge color={
                    line.status === 'done' ? 'emerald-500'
                    : line.status === 'running' ? 'aura'
                    : line.status === 'error' ? 'vital'
                    : 'slate-500'
                  }>
                    {line.status === 'running' ? 'Producing…' : line.status}
                  </Badge>
                </div>
              </motion.div>
            ))}
          </Card>
        </main>

        {/* Output panel */}
        <div className="@[440px]:col-span-7">
          {selectedLine ? (
            <Card className="p-6 space-y-4 h-full flex flex-col">
              <div className="flex items-center justify-between shrink-0">
                <div>
                  <h4 className="text-sm font-black text-white uppercase">{selectedLine.name}</h4>
                  <p className="text-[9px] text-slate-500 capitalize mt-0.5">{selectedLine.product_type.replace(/_/g,' ')} · {selectedLine.domain}</p>
                </div>
                <div className="flex gap-2">
                  {selectedLine.status === 'running' ? (
                    <button type="button" onClick={() => handleStop(selectedLine.id)}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-vital text-white rounded-xl text-[9px] font-black uppercase tracking-widest">
                      <Square size={10} fill="currentColor" /> Stop
                    </button>
                  ) : (
                    <button type="button" onClick={() => handleRun(selectedLine.id)}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-aura text-sovereign rounded-xl text-[9px] font-black uppercase tracking-widest hover:opacity-90">
                      <Play size={10} /> Produce
                    </button>
                  )}
                  {selectedLine.output && (
                    <button type="button" onClick={() => handleExport(selectedLine)}
                      className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-700 text-slate-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:text-white hover:border-aura/50 transition-colors">
                      <Download size={10} /> Export
                    </button>
                  )}
                </div>
              </div>

              <div className="flex-1 bg-slate-950 rounded-2xl border border-slate-900 overflow-y-auto p-5 min-h-[300px]">
                {selectedLine.output ? (
                  <pre className="text-[10px] text-slate-300 font-mono leading-relaxed whitespace-pre-wrap">
                    {selectedLine.output}
                    {selectedLine.status === 'running' && <span className="text-aura animate-pulse">▌</span>}
                  </pre>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-center gap-3 opacity-40">
                    {selectedLine.status === 'running'
                      ? <><Loader2 size={28} className="text-aura animate-spin" /><p className="text-xs text-aura font-black uppercase tracking-widest">AI is producing your artefact…</p></>
                      : <><FileText size={28} /><p className="text-xs font-black uppercase tracking-widest">Click Produce to generate the artefact</p></>
                    }
                  </div>
                )}
              </div>
            </Card>
          ) : (
            <Card className="p-12 flex flex-col items-center justify-center text-center h-full opacity-40 min-h-[300px]">
              <Database size={36} className="mb-4" />
              <p className="text-sm font-black uppercase tracking-widest">Select a production line</p>
              <p className="text-[9px] text-slate-500 mt-2">or create a new one to get started</p>
            </Card>
          )}
        </div>
      </div>

      {/* New line modal */}
      <AnimatePresence>
        {showNew && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-6"
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              className="bg-slate-950 border border-slate-800 rounded-[2rem] p-8 w-full max-w-lg space-y-6"
            >
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-black text-white uppercase tracking-tight">New Production Line</h3>
                <button type="button" aria-label="Close" onClick={() => setShowNew(false)}
                  className="text-slate-500 hover:text-white"><X size={18} /></button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Line Name</label>
                  <input
                    value={name}
                    onChange={e => setName(e.target.value)}
                    placeholder="e.g. Enterprise Growth Strategy"
                    aria-label="Production line name"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-aura"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Product Type</label>
                    <select
                      value={productType}
                      onChange={e => setProductType(e.target.value)}
                      aria-label="Product type"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura"
                    >
                      {PRODUCT_TYPES.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Domain</label>
                    <select
                      value={domain}
                      onChange={e => setDomain(e.target.value)}
                      aria-label="Domain"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura"
                    >
                      {DOMAINS.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase()+d.slice(1)}</option>)}
                    </select>
                  </div>
                </div>
                <div>
                  <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Description (optional)</label>
                  <textarea
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    placeholder="Briefly describe the subject or goals of this production line…"
                    rows={3}
                    aria-label="Production line description"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-aura resize-none"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={handleCreate}
                disabled={!name.trim()}
                className="w-full py-3 bg-aura text-sovereign rounded-xl font-black uppercase tracking-widest text-xs hover:opacity-90 transition-opacity disabled:opacity-40"
              >
                Create Production Line
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
